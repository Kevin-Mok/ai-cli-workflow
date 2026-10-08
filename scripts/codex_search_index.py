#!/usr/bin/env python3
"""Private incremental index and normalized dialogue for local Codex sessions."""
import base64
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import uuid

CACHE_VERSION = 2
SNIPPETS = 5
TOOL_ITEMS = {'function_call', 'function_call_output', 'custom_tool_call',
              'custom_tool_call_output', 'local_shell_call', 'mcp_tool_call',
              'mcp_tool_call_output', 'web_search_call', 'tool_search_call', 'tool_search_output'}
TOOL_EVENTS = {'exec_command_begin', 'exec_command_end', 'mcp_tool_call_begin',
               'mcp_tool_call_end', 'web_search_begin', 'web_search_end'}
CONTEXT_PREFIXES = ('# AGENTS.md instructions', '<user_instructions>', '<environment_context>',
                    '<environments_instructions>', '<permissions instructions>',
                    '<developer_instructions>', '<system_instructions>', '<skills_instructions>',
                    '<apps_instructions>', '<plugins_instructions>')


class SearchError(Exception):
    pass


def visible(text):
    """Keep terminal controls in private logs from becoming terminal commands."""
    return ''.join(c if c.isprintable() else ('\\t' if c == '\t' else '\\n' if c == '\n'
                   else '\\r' if c == '\r' else f'\\x{ord(c):02x}') for c in text)


def warn(text):
    print('codex-search: ' + visible(text), file=sys.stderr)


def session_id(value):
    if not isinstance(value, str):
        return None
    try:
        return str(uuid.UUID(value))
    except ValueError:
        return None


def epoch(value):
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return dt.replace(tzinfo=timezone.utc).timestamp() if dt.tzinfo is None else dt.timestamp()
    except (ValueError, OverflowError):
        return 0.0


def signature(path):
    info = path.stat()
    return [info.st_size, info.st_mtime_ns, info.st_ctime_ns, info.st_dev, info.st_ino]


def secure_directory(path):
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid():
        raise SearchError(f'unsafe cache directory: {path} (must be owned by you, without symlinks)')
    path.chmod(0o700)


def secure_file(path):
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_nlink != 1:
        raise SearchError(f'unsafe cache file: {path}')
    path.chmod(0o600)


@contextmanager
def cache_lock(home):
    base = Path(os.environ.get('XDG_CACHE_HOME') or Path.home() / '.cache') / 'codex-search'
    secure_directory(base)
    root = base / hashlib.sha256(os.fsencode(home)).hexdigest()
    secure_directory(root)
    lock_path = root / '.lock'
    fd = os.open(lock_path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        secure_file(lock_path)
        with os.fdopen(fd, 'r+') as lock:
            fd = None
            fcntl.flock(lock, fcntl.LOCK_EX)
            yield root
    finally:
        if fd is not None:
            os.close(fd)


@contextmanager
def private_temp(root, suffix):
    fd, name = tempfile.mkstemp(dir=root, suffix=suffix)
    try:
        with os.fdopen(fd, 'w+', encoding='utf-8') as out:
            yield Path(name), out
    finally:
        Path(name).unlink(missing_ok=True)


def atomic_json(path, value):
    with private_temp(path.parent, '.tmp') as (tmp, out):
        json.dump(value, out, ensure_ascii=True, separators=(',', ':'))
        out.flush()
        os.fsync(out.fileno())
        os.replace(tmp, path)


def records(path, problems):
    """Malformed input never leaks its payload through diagnostics."""
    with path.open('rb') as source:
        for raw in source:
            if not raw.strip():
                continue
            try:
                row = json.loads(raw)
                if not isinstance(row, dict):
                    raise ValueError('not an object')
                yield row
            except (ValueError, UnicodeError, RecursionError):
                problems[0] += 1


def conversation_text(role, text):
    if role not in ('user', 'assistant') or not isinstance(text, str):
        return ''
    if role == 'user':
        # The IDE prepends context using this documented delimiter.
        marker = '## My request for Codex:'
        if marker in text:
            text = text.split(marker, 1)[1].strip()
        if text.lstrip().startswith(CONTEXT_PREFIXES):
            return ''
    return text


def tool_strings(value, depth=0):
    """Decode text and JSON-encoded arguments, excluding binary/opaque content."""
    if depth > 24:
        return
    if isinstance(value, str):
        if value.lstrip().startswith(('{', '[')):
            try:
                decoded = json.loads(value)
            except (ValueError, RecursionError):
                pass
            else:
                yield from tool_strings(decoded, depth + 1)
                return
        yield value
    elif isinstance(value, list):
        for child in value:
            yield from tool_strings(child, depth + 1)
    elif isinstance(value, dict):
        if value.get('type') in ('image', 'input_image', 'audio', 'input_audio'):
            return
        for key, child in value.items():
            if key not in ('data', 'image_url', 'audio_url', 'encrypted_content', 'call_id', 'id'):
                yield from tool_strings(child, depth + 1)


def extract(path, root, source_signature):
    token = uuid.uuid4().hex
    conversation = root / (token + '.conversation.txt')
    tools = root / (token + '.tools.txt')
    dialogue = root / (token + '.dialogue.jsonl')
    metadata = {'id': None, 'cwd': '', 'timestamp': '', 'signature': source_signature,
                'conversation': conversation.name, 'tools': tools.name,
                'dialogue': dialogue.name, 'dialogue_hash': '', 'skipped': 0}
    problems = [0]
    response_digests = set()
    dialogue_hash = hashlib.sha256()
    try:
        with private_temp(root, '.tmp') as (conv_tmp, conv), \
                private_temp(root, '.tmp') as (tool_tmp, tool), \
                private_temp(root, '.tmp') as (dialogue_tmp, decoded), \
                private_temp(root, '.tmp') as (_, messages):
            for row in records(path, problems):
                kind, payload = row.get('type'), row.get('payload')
                if not isinstance(payload, dict):
                    problems[0] += 1
                    continue
                if not isinstance(kind, str) or (kind in ('response_item', 'event_msg') and
                                                not isinstance(payload.get('type'), str)):
                    problems[0] += 1
                    continue
                try:
                    timestamp = row.get('timestamp')
                    if isinstance(timestamp, str) and epoch(timestamp) > epoch(metadata['timestamp']):
                        metadata['timestamp'] = timestamp
                    if kind == 'session_meta':
                        sid = session_id(payload.get('id'))
                        if sid:
                            if metadata['id'] and sid != metadata['id']:
                                problems[0] += 1
                                continue
                            metadata['id'] = sid
                            cwd = payload.get('cwd')
                            if isinstance(cwd, str):
                                metadata['cwd'] = cwd
                            timestamp = payload.get('timestamp')
                            if isinstance(timestamp, str) and epoch(timestamp) > epoch(metadata['timestamp']):
                                metadata['timestamp'] = timestamp
                    elif kind == 'response_item' and payload.get('type') == 'message':
                        role, content = payload.get('role'), payload.get('content')
                        if not isinstance(content, list):
                            problems[0] += 1
                            continue
                        parts = []
                        for part in content:
                            if not isinstance(part, dict):
                                problems[0] += 1
                            elif part.get('type') in ('input_text', 'output_text'):
                                if isinstance(part.get('text'), str):
                                    parts.append(part['text'])
                                else:
                                    problems[0] += 1
                        text = conversation_text(role, '\n'.join(parts))
                        if text:
                            assert isinstance(role, str)
                            digest = hashlib.sha256((role + '\0' + text).encode()).hexdigest()
                            response_digests.add(digest)
                            messages.write(json.dumps([True, digest, role, text], ensure_ascii=True) + '\n')
                    elif kind == 'event_msg' and payload.get('type') in ('user_message', 'agent_message'):
                        role = 'user' if payload['type'] == 'user_message' else 'assistant'
                        text = conversation_text(role, payload.get('message'))
                        if text:
                            assert isinstance(role, str)
                            digest = hashlib.sha256((role + '\0' + text).encode()).hexdigest()
                            messages.write(json.dumps([False, digest, role, text], ensure_ascii=True) + '\n')
                    elif (kind == 'response_item' and payload.get('type') in TOOL_ITEMS) or \
                            (kind == 'event_msg' and payload.get('type') in TOOL_EVENTS):
                        for text in tool_strings(payload):
                            tool.write(text + '\n')
                except UnicodeError:
                    # JSON permits isolated surrogates; UTF-8 cache text does not.
                    problems[0] += 1
            # Replay a disk spool to preserve chronology without holding dialogue
            # in memory. Mirrored events are omitted at their original positions.
            messages.flush()
            messages.seek(0)
            for line in messages:
                response, digest, role, text = json.loads(line)
                if response or digest not in response_digests:
                    conv.write(text + '\n')
                    canonical = json.dumps({'role': role, 'text': text}, ensure_ascii=False,
                                           separators=(',', ':')) + '\n'
                    decoded.write(canonical)
                    dialogue_hash.update(canonical.encode('utf-8'))
            for out in (conv, tool, decoded):
                out.flush()
                os.fsync(out.fileno())
            os.replace(conv_tmp, conversation)
            os.replace(tool_tmp, tools)
            os.replace(dialogue_tmp, dialogue)
    except BaseException:
        conversation.unlink(missing_ok=True)
        tools.unlink(missing_ok=True)
        dialogue.unlink(missing_ok=True)
        raise
    metadata['dialogue_hash'] = dialogue_hash.hexdigest()
    metadata['skipped'] = problems[0]
    if not metadata['id']:
        warn(f'skipped session without valid session_meta UUID: {path}')
    return metadata


def load_manifest(root, home):
    path = root / 'manifest.json'
    if not path.exists():
        return {}
    secure_file(path)
    try:
        data = json.loads(path.read_text())
        if not isinstance(data, dict) or data.get('version') != CACHE_VERSION or data.get('home') != str(home):
            warn('cache format changed; rebuilding index')
            return {}
        entries = data['sources']
        if not isinstance(entries, dict):
            raise ValueError('sources')
        for source, entry in entries.items():
            if not isinstance(source, str) or not isinstance(entry, dict):
                raise ValueError('source entry')
            if not isinstance(entry['signature'], list) or len(entry['signature']) != 5 or \
                    any(type(n) is not int for n in entry['signature']):
                raise ValueError('signature')
            if entry['id'] is not None and session_id(entry['id']) != entry['id']:
                raise ValueError('UUID')
            if any(not isinstance(entry[k], str) for k in ('cwd', 'timestamp')) or \
                    type(entry['skipped']) is not int or entry['skipped'] < 0:
                raise ValueError('metadata')
            for field, extension in (('conversation', 'txt'), ('tools', 'txt'), ('dialogue', 'jsonl')):
                pattern = r'[0-9a-f]{32}\.' + field + r'\.' + extension
                if not isinstance(entry[field], str) or not re.fullmatch(pattern, entry[field]):
                    raise ValueError('cache filename')
            if not isinstance(entry['dialogue_hash'], str) or not re.fullmatch(r'[0-9a-f]{64}', entry['dialogue_hash']):
                raise ValueError('dialogue hash')
        return entries
    except (ValueError, KeyError, TypeError, RecursionError):
        warn('invalid cache manifest; rebuilding index')
        return {}


def cleanup(root, keep=()):
    keep = set(keep) | {'.lock', 'recaps'}
    for path in root.iterdir():
        if path.name == 'recaps':
            # Recap maintenance owns its locks and concurrent-generation lifecycle.
            secure_directory(path)
        elif path.name not in keep:
            if path.is_dir() and not path.is_symlink():
                raise SearchError(f'unexpected directory in cache: {path}')
            path.unlink()


def refresh(root, home, rebuild=False):
    entries = {} if rebuild else load_manifest(root, home)
    sources = home / 'sessions'
    current = {}
    updated = 0
    if not sources.exists():
        warn(f'sessions directory does not exist: {sources}')
    def walk_error(error):
        # Do not discard cached sources when discovery is incomplete.
        raise SearchError(f'cannot discover sessions: {error}')
    for folder, _, names in os.walk(sources, onerror=walk_error, followlinks=False):
        for name in sorted(names):
            if not name.endswith('.jsonl'):
                continue
            path = Path(folder) / name
            if path.is_symlink() or not path.is_file():
                warn(f'skipped non-regular session source: {path}')
                continue
            key = str(path)
            try:
                sig = signature(path)
                entry = entries.get(key)
                valid_files = entry and all((root / entry[field]).exists() for field in ('conversation', 'tools', 'dialogue'))
                if valid_files and entry is not None:
                    for field in ('conversation', 'tools', 'dialogue'):
                        secure_file(root / entry[field])
                if entry is None or not valid_files or entry['signature'] != sig:
                    if updated == 0:
                        warn('refreshing local session index...')
                    entry = extract(path, root, sig)
                    # An append during parsing must be retried on the next invocation.
                    if signature(path) != sig:
                        entry['signature'] = [0, 0, 0, 0, 0]
                        warn(f'session changed while indexing; will refresh next search: {path}')
                    updated += 1
                    if updated % 100 == 0:
                        warn(f'indexed {updated} changed sessions')
                current[key] = entry
                if entry['skipped']:
                    warn(f"skipped {entry['skipped']} malformed/incomplete records in {path}")
            except FileNotFoundError:
                warn(f'session disappeared during indexing: {path}')
            except OSError as error:
                warn(f'cannot index session {path}: {error.strerror}')
                # Preserve existing data for recovery, but exclude stale matches.
    changed = rebuild or current != entries or not (root / 'manifest.json').exists()
    if changed:
        atomic_json(root / 'manifest.json', {'version': CACHE_VERSION, 'home': str(home), 'sources': current})
    keep = ['manifest.json'] + [entry[field] for entry in current.values() for field in ('conversation', 'tools', 'dialogue')]
    cleanup(root, keep)
    if updated:
        warn(f'index ready: {updated} refreshed, {len(current)} sources')
    return current


def titles(home):
    result = {}
    problems = [0]
    path = home / 'session_index.jsonl'
    if not path.exists():
        return result
    try:
        for row in records(path, problems):
            sid, title = session_id(row.get('id')), row.get('thread_name')
            if sid and isinstance(title, str) and title.strip():
                result[sid] = title.strip()
    except OSError as error:
        warn(f'cannot read optional title index: {error.strerror}')
    if problems[0]:
        warn(f'skipped {problems[0]} malformed/incomplete title index records')
    return result


def rg_text(value):
    return value['text'] if 'text' in value else base64.b64decode(value['bytes']).decode('utf-8', 'replace')


def search(root, entries, args):
    by_file = {entry[field]: entry for entry in entries.values() if entry['id']
               for field in ('conversation', 'tools') if field == 'conversation' or args.all_text}
    results = {}
    command = ['rg', '--no-config', '--json', '--text', '--color=never', '--glob', '*.conversation.txt']
    if args.all_text:
        command += ['--glob', '*.tools.txt']
    if args.ignore_case:
        command.append('-i')
    if args.fixed_strings:
        command.append('-F')
    command += ['-e', args.pattern, '--', str(root)]
    with tempfile.TemporaryFile(mode='w+', encoding='utf-8') as errors:
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=errors, text=True, encoding='utf-8') as process:
            assert process.stdout is not None
            for line in process.stdout:
                event = json.loads(line)
                if event['type'] != 'match':
                    continue
                data = event['data']
                name = Path(rg_text(data['path'])).name
                entry = by_file.get(name)
                if entry is None:
                    continue
                snippets = results.setdefault(entry['id'], [])
                if len(snippets) < SNIPPETS:
                    text = rg_text(data['lines']).removesuffix('\n')
                    # Submatch offsets are bytes, while presentation widths are characters.
                    first = data['submatches'][0]['start'] if data['submatches'] else 0
                    encoded = text.encode('utf-8')
                    start = max(0, len(encoded[:first].decode('utf-8', 'ignore')) - 80)
                    end = start + 240
                    start_byte = len(text[:start].encode('utf-8'))
                    end_byte = len(text[:end].encode('utf-8'))
                    prefix = '…' if start else ''
                    snippet_text = prefix + text[start:end] + ('…' if len(text) > end else '')
                    spans = []
                    for match in data['submatches']:
                        # rg orders submatches by byte position. Decode only this
                        # display window, never every prefix of a dense long line.
                        if match['start'] >= end_byte:
                            break
                        if match['end'] <= start_byte:
                            continue
                        left = len(encoded[start_byte:max(match['start'], start_byte)].decode('utf-8', 'ignore'))
                        right = len(encoded[start_byte:min(match['end'], end_byte)].decode('utf-8', 'ignore'))
                        spans.append((left + len(prefix), right + len(prefix)))
                    snippet = {'text': snippet_text, 'spans': spans}
                    if all(item['text'] != snippet_text for item in snippets):
                        snippets.append(snippet)
            code = process.wait()
        if code not in (0, 1):
            errors.seek(0)
            raise SearchError('rg search failed: ' + errors.read().strip())
    return [(entry, results[entry['id']]) for entry, _ in recent_entries(entries)
            if entry['id'] in results]


def recent_entries(entries):
    """Newest recorded activity first, with the same UUID resolution as search."""
    metadata = {}
    for entry in entries.values():
        sid = entry['id']
        if sid and (sid not in metadata or epoch(entry['timestamp']) > epoch(metadata[sid]['timestamp'])):
            metadata[sid] = entry
    return [(metadata[sid], []) for sid in sorted(metadata,
            key=lambda sid: (epoch(metadata[sid]['timestamp']), sid), reverse=True)]
