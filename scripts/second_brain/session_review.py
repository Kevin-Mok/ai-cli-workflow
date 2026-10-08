"""Discover recent safe conversations independently of the background queue."""
from __future__ import annotations

from datetime import datetime
import hashlib
import os
from pathlib import Path
import re
import shutil
import stat
import textwrap
from zoneinfo import ZoneInfo

from . import sessions
from .session_digest_input import clean, epoch, native_titles, parse
from .paths import PathError, local_now
from .session_digest_runtime import InferenceError

TORONTO = ZoneInfo('America/Toronto')
LEGACY_HELPER = re.compile(r'^(?:guardian\s+review\b|(?:spawned\s+)?(?:subagent|helper)(?:\s+session|\s+agent)?\s*(?:$|[:/—-]))', re.I)


def fingerprint(metadata):
    return [metadata.st_size, metadata.st_mtime_ns, metadata.st_ctime_ns,
            metadata.st_dev, metadata.st_ino]


def source_paths(home, v):
    """Inventory physical owned files; the parser anchors subsequent reads."""
    paths = {}
    source_keys = {entry['source']: key for key, entry in v['sessions'].items() if entry['source']}
    failed = 0
    def onerror(error):
        nonlocal failed
        failed += 1
    for folder in ('sessions', 'archived_sessions'):
        base = home / folder
        if base.is_symlink():
            failed += 1
            continue
        if not base.exists():
            continue
        for dirname, dirs, files in os.walk(base, followlinks=False, onerror=onerror):
            dirs[:] = [name for name in dirs if not (Path(dirname) / name).is_symlink()]
            for name in sorted(files):
                if not name.endswith('.jsonl'):
                    continue
                path = Path(dirname) / name
                try:
                    metadata = path.lstat()
                    if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1 or metadata.st_uid != os.geteuid():
                        raise OSError('unsafe source')
                except OSError:
                    failed += 1
                    continue
                key = source_keys.get(str(path), hashlib.sha256(str(path.relative_to(home)).encode()).hexdigest())
                paths[key] = (path, fingerprint(metadata))
    return paths, failed


def discard_queue(v, key):
    if key in v['queue']:
        v['queue'].remove(key)


def screen(v, key, path, stamp, home, titles, current_sources=None):
    """Refresh metadata without asserting that an older recap is fresh."""
    old = v['sessions'].get(key)
    entry = parse(path, home, exclude_helpers=True)
    if old is None and entry['id'] and current_sources is not None:
        # Archiving changes the source pathname, not conversation identity.
        # Keep the original state key so persisted check IDs remain valid.
        prior = next((value for value in v['sessions'].values()
                      if value['id'] == entry['id'] and value['source'] not in current_sources), None)
        if prior is not None:
            key, old = prior['key'], prior
    entry['key'] = key
    dialogue = entry.pop('dialogue')
    entry.update(title='', summary=None, checks=[], summarized_at=None)
    entry.setdefault('reason', '')
    if entry['status'] == 'skipped':
        # Unscreenable sources must not display a cached title/recap. Keep old
        # dispositions privately for transient size/read failures only.
        if old and entry['reason'] not in ('private_context', 'unsafe_source', 'helper_session'):
            entry.update(summary=old['summary'], checks=old['checks'], summarized_at=old['summarized_at'])
        else:
            v['summary_hashes'].pop(key, None)
        discard_queue(v, key)
    else:
        entry['title'] = titles.get(entry['id'], '')
        if old:
            entry.update(summary=old['summary'], checks=old['checks'], summarized_at=old['summarized_at'])
        fresh = entry['summary'] is not None and v['summary_hashes'].get(key) == entry['hash']
        entry.update(status=('partial' if entry['partial'] else 'ready') if fresh else ('stale' if entry['summary'] else 'pending'),
                     reason='' if fresh else ('changed_source' if entry['summary'] else 'not_summarized'))
        if fresh:
            discard_queue(v, key)
    v['sessions'][key] = entry
    # The complete signature catches same-size rewrites with restored mtime.
    # Never cache a parse if its pathname changed while it was being read.
    try:
        stable = stamp == fingerprint(path.lstat()) and entry['reason'] != 'changed_during_read'
    except OSError:
        stable = False
    if stable:
        v['screened'][key] = stamp
    else:
        v['screened'].pop(key, None)
        entry.update(status='stale' if entry['summary'] else 'pending', reason='changed_during_read')
    return entry, dialogue


def eligible(entry):
    summary = entry['summary']
    title = entry['title'] or (summary['title'] if summary else '')
    return bool(entry['id']) and entry['status'] != 'skipped' and not LEGACY_HELPER.search(' '.join(title.split()))


def select(v, paths, limit):
    entries = [entry for key, entry in v['sessions'].items()
               if key in paths and v['screened'].get(key) == paths[key][1] and eligible(entry)]
    entries.sort(key=lambda entry: (-epoch(entry['last_activity']), entry['id'], entry['key']))
    unique = {}
    for entry in entries:
        unique.setdefault(entry['id'], entry)
    return list(unique.values())[:limit]


def discover(v, home, titles):
    paths, scan_failed = source_paths(home, v)
    current_sources = {str(path) for path, stamp in paths.values()}
    for key, (path, stamp) in list(paths.items()):
        entry = v['sessions'].get(key)
        if entry is not None and v['screened'].get(key) == stamp:
            if entry['status'] != 'skipped':
                entry['title'] = titles.get(entry['id'], '')
            continue
        try:
            screened, _ = screen(v, key, path, stamp, home, titles, current_sources)
            if screened['key'] != key:
                paths[screened['key']] = paths.pop(key)
        except (OSError, ValueError):
            scan_failed += 1
            v['screened'].pop(key, None)
            if entry is not None:
                entry.update(status='failed', reason='scan')
    for key, entry in v['sessions'].items():
        if key not in paths:
            v['screened'].pop(key, None)
            if entry['status'] != 'skipped':
                entry.update(status='stale', reason='source_unavailable')
    v['queue'] = [key for key in v['queue'] if key in paths]
    return paths, scan_failed


def review(limit=None, refresh_limit=None, *, all_sessions=False):
    if limit is not None and (type(limit) is not int or not 1 <= limit <= 20):
        raise ValueError('review limit must be between 1 and 20')
    if type(all_sessions) is not bool or (all_sessions and limit is not None):
        raise ValueError('--all cannot be combined with an explicit display limit')
    display_limit = None if all_sessions else (5 if limit is None else limit)
    budget = refresh_limit if refresh_limit is not None else (display_limit or 20)
    if type(budget) is not int or not 0 <= budget <= 20:
        raise ValueError('review refresh limit must be between 0 and 20')
    with sessions.lock() as (root, directory):
        v = sessions.load(root, directory)
        home = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))).expanduser()
        if not home.is_absolute() or home.resolve() != home.absolute():
            raise PathError('CODEX_HOME must be an absolute physical directory')
        titles = native_titles(home)
        paths, scan_failed = discover(v, home, titles)
        v['error'] = 'scan' if scan_failed else None
        selected = select(v, paths, display_limit)
        calls = 0
        for entry in selected:
            key = entry['key']
            if entry['summary'] is not None and v['summary_hashes'].get(key) == entry['hash']:
                continue
            if calls >= budget:
                break
            path, stamp = paths[key]
            try:
                # No transcript is retained in the metadata cache. Re-screen
                # selected input before inference, including privacy changes.
                entry, dialogue = screen(v, key, path, stamp, home, titles)
                if not eligible(entry) or v['screened'].get(key) != stamp:
                    continue
                calls += 1
                sessions.summarize(entry, dialogue)
                v['summary_hashes'][key] = entry['hash']
                v['seen'][key] = entry['hash']
                discard_queue(v, key)
            except (InferenceError, ValueError, OSError) as error:
                category = error.category if isinstance(error, InferenceError) else ('scan' if isinstance(error, OSError) else 'invalid_summary')
                entry.update(status='failed', reason=category)
                v['error'] = category
                if category in ('authentication', 'quota', 'isolation'):
                    break
        # Model calls can take minutes. Revalidate cached entries before they
        # enter any output: a conversation may have become private meanwhile.
        paths, final_scan_failed = discover(v, home, native_titles(home))
        scan_failed = max(scan_failed, final_scan_failed)
        if scan_failed and v['error'] is None:
            v['error'] = 'scan'
        selected = select(v, paths, display_limit)
        v['refreshed_at'] = local_now().isoformat()
        all_entries = list(v['sessions'].values())
        v['coverage'] = {
            'skipped': sum(entry['status'] == 'skipped' for entry in all_entries),
            'failed': scan_failed + sum(entry['status'] == 'failed' for entry in all_entries),
            'partial': sum(entry['status'] == 'partial' for entry in all_entries),
            'unknown': sum(entry['summary'] is None and entry['status'] != 'skipped' for entry in all_entries),
            'stale': sum(entry['status'] == 'stale' for entry in all_entries),
            'hidden': len(all_entries) - len(selected),
        }
        sessions.save(root, directory, v)
        return sessions.report(v, calls, entries=selected)


def activity_label(value):
    timestamp = epoch(value)
    if not timestamp:
        return 'Activity unknown'
    local = datetime.fromtimestamp(timestamp, TORONTO)
    return f"{local:%b} {local.day}, {local.year} at {local.strftime('%I:%M %p %Z').lstrip('0')}"


def next_step(entry):
    summary = entry['summary']
    if not summary:
        return ''
    remaining = summary.get('remaining', [])
    if remaining:
        return remaining[0]
    current = {check['key'] for check in summary.get('checks', [])}
    return next((check['text'] for check in entry['checks']
                 if check['key'] in current and check['disposition'] == 'open'), '')


def render_terminal(report, width=None, *, plain=False):
    width = max(40, min(88, width if width is not None else shutil.get_terminal_size((88, 24)).columns))
    lines = []
    def add(text, prefix='', max_lines=None):
        text = ' '.join(clean(str(text)).split())
        if plain:
            text = text.encode('ascii', errors='backslashreplace').decode()
        lines.extend(textwrap.wrap(text, width=width,
                     initial_indent=prefix, subsequent_indent=' ' * len(prefix),
                     max_lines=max_lines, placeholder='...' if plain else '…'))
    add('Recent work sessions' if plain else '🗂️ Recent work sessions')
    add('Conversation reports; not independently verified.')
    for number, entry in enumerate(report.get('sessions', []), 1):
        lines.append('')
        summary = entry['summary']
        title = entry['title'] or (summary['title'] if summary else 'Untitled session')
        add(title, prefix=f'{number}. ')
        add(entry['cwd'] or 'Unknown project', prefix='   ')
        add(activity_label(entry['last_activity']), prefix='   ')
        if summary:
            progress = '; '.join(summary.get('accomplishments', [])) or summary['goal']
            add(progress, prefix='   Recap: ', max_lines=2)
            step = next_step(entry)
            if step:
                add(step, prefix='   Next: ', max_lines=1)
        else:
            add('Recap not generated.', prefix='   ')
        if entry['status'] in ('failed', 'stale'):
            label = 'Recap stale' if summary else 'Recap unavailable'
            add(label + ': ' + (entry['reason'] or entry['status']).replace('_', ' '), prefix='   ' if plain else '   ⚠ ')
        elif entry.get('partial', entry['status'] == 'partial'):
            add('Recap based on partial conversation.', prefix='   ')
    if not report.get('sessions'):
        lines.append('')
        add('No work sessions available.')
    lines.append('')
    add('Full evidence and check IDs: use --details.')
    return '\n'.join(lines) + '\n'
