"""Asynchronous recent-session picker; inference belongs to the recap manager."""
import json
import math
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import os
from pathlib import Path
import re
import secrets
import shlex
import signal
import stat
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request

from codex_search_index import SearchError, atomic_json, secure_file, session_id, visible

STATUSES = {'missing', 'queued', 'stale', 'generating', 'unavailable', 'ready'}


def paragraph(value):
    if isinstance(value, list):
        return '\n'.join('- ' + visible(str(item)) for item in value)
    return visible(str(value or 'Not established by the conversation.'))


def activity_time(value, compact=False):
    """Render source activity in Toronto, including its seasonal UTC offset."""
    if not value:
        return ''
    try:
        stamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=timezone.utc)
        local = stamp.astimezone(ZoneInfo('America/Toronto'))
        if compact:
            month = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')[local.month - 1]
            return f'{month} {local.day} {local:%H:%M}'
        precision = 'milliseconds' if '.' in value and local.microsecond % 1000 == 0 else 'auto'
        return local.isoformat(' ', timespec=precision) + ' (' + local.strftime('%Z') + ')'
    except (ValueError, OverflowError):
        return value


def compact_directory(value):
    """Keep the basename readable while abbreviating parent directories."""
    if not value:
        return '(directory not recorded)'
    parts = [part for part in value.split('/') if part]
    if not parts:
        return '/>'
    prefix = '/' if value.startswith('/') else ''
    return prefix + '/'.join([part[0] for part in parts[:-1]] + parts[-1:]) + '>'


def generic_title(title):
    return title.strip().casefold() in ('', '(untitled)', 'guardian review')


def recap_title(title, status):
    """Give generic rows a descriptive cached headline."""
    recap = status.get('recap')
    headline = recap.get('headline') if isinstance(recap, dict) else None
    if (generic_title(title) and
            isinstance(headline, str) and headline.strip()):
        return headline.strip()
    return title if title.strip() else '(untitled)'


def recap_progress(status):
    state = status.get('status')
    seconds = status.get('elapsed_seconds')
    if (state not in ('queued', 'generating') or type(seconds) not in (int, float) or
            not math.isfinite(seconds) or seconds < 0):
        return ''
    minutes, seconds = divmod(int(seconds), 60)
    elapsed = f'{minutes}m{seconds:02}s' if minutes else f'{seconds}s'
    position = status.get('queue_position')
    queued = f' #{position}' if state == 'queued' and type(position) is int and position > 0 else ''
    return state + queued + ' ' + elapsed


def render_session(entry, title, status, local_dialogue=''):
    """All variable display text is escaped before it reaches the terminal."""
    state = status.get('status', 'missing')
    if state not in STATUSES:
        state = 'unavailable'
    partial = bool(status.get('partial'))
    label = state + ('; partial' if partial else '')
    recap = status.get('recap')
    headline = recap.get('headline', '') if isinstance(recap, dict) else ''
    display_title = recap_title(title, status)
    progress = recap_progress(status)
    row_title = display_title
    if generic_title(title):
        badge = progress
        if state == 'unavailable':
            badge = 'unavailable'
        elif state == 'missing':
            if status.get('generation_enabled') is True:
                badge = 'Ctrl-G'
            elif status.get('generation_enabled') is False:
                badge = 'recaps off'
        if badge:
            row_title += ' [' + badge + ']'
    activity = activity_time(entry.get('timestamp', ''))
    short_activity = activity_time(entry.get('timestamp', ''), compact=True)
    row = '\t'.join((entry['id'], visible(short_activity or '(activity unknown)'),
                     visible(compact_directory(entry.get('cwd', ''))),
                     visible(row_title),
                     visible('[' + label + '] ' + str(headline))))
    lines = [visible(display_title)]
    if display_title != (title or '(untitled)'):
        lines.append('Original title: ' + visible(title if title.strip() else '(untitled)'))
    lines.extend(['Directory: ' + visible(entry.get('cwd', '')),
                  'Activity: ' + visible(activity), 'AI recap: ' + label])
    if progress:
        lines.append('Recap progress: ' + progress)
    if status.get('detail'):
        lines.append(visible(str(status['detail'])))
    if isinstance(recap, dict):
        for label, field in (('Goal', 'goal'), ('Reported progress', 'progress'),
                             ('Current state', 'state'), ('Remaining work', 'next_steps')):
            lines.extend(('', label + ':', paragraph(recap.get(field))))
    else:
        lines.extend(('', 'Local dialogue (no current AI recap):'))
        lines.extend(visible(line) for line in local_dialogue.splitlines())
        if not local_dialogue:
            lines.append('No decoded dialogue available.')
    return row, '\n'.join(lines) + '\n'


def atomic_text(path, text):
    fd, name = tempfile.mkstemp(dir=path.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as output:
            output.write(text)
            output.flush()
            os.fsync(output.fileno())
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def read_json(path):
    secure_file(path)
    return json.loads(path.read_text(encoding='utf-8'))


def runtime_manifest(directory):
    path = Path(directory).absolute()
    info = path.lstat()
    if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or
            stat.S_IMODE(info.st_mode) & 0o077 or not path.name.startswith('codex-search-picker-')):
        raise SearchError('invalid private picker directory')
    manifest = read_json(path / 'manifest.json')
    if (not isinstance(manifest, dict) or not isinstance(manifest.get('ids'), list) or
            any(not isinstance(sid, str) or session_id(sid) != sid for sid in manifest['ids'])):
        raise SearchError('invalid picker manifest')
    return path, manifest


def local_dialogue(root, entry):
    name = entry.get('dialogue', '')
    if not isinstance(name, str) or not re.fullmatch(r'[0-9a-f]{32}\.dialogue\.jsonl', name):
        return ''
    try:
        from codex_search_recaps import bounded_dialogue
        text, partial = bounded_dialogue(root, entry)
        lines = []
        for line in text.splitlines():
            try:
                item = json.loads(line)
            except ValueError:
                lines.append(line)
            else:
                if isinstance(item, dict) and item.get('role') in ('user', 'assistant'):
                    lines.append(item['role'].capitalize() + ': ' + str(item.get('text', '')))
                else:
                    lines.append(line)
        return ('[Partial local dialogue]\n' if partial else '') + '\n'.join(lines)
    except (OSError, ValueError, SearchError):
        return 'Local dialogue is unavailable; refresh the session index to retry.'


def helper(mode, directory, sid=None):
    path, manifest = runtime_manifest(directory)
    if mode == 'start' and sid is None:
        port = int(os.environ.get('FZF_PORT', '0'))
        if not 0 < port < 65536:
            raise SearchError('invalid picker port')
        atomic_json(path / 'port.json', port)
        return
    if mode not in ('preview', 'request') or not isinstance(sid, str) or session_id(sid) != sid or sid not in manifest['ids']:
        raise SearchError('invalid picker callback session')
    if mode == 'request':
        try:
            descriptor = os.open(path / ('request-' + sid),
                                 os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        except FileExistsError:
            return
        os.close(descriptor)
    else:
        value = read_json(path / 'sessions.json')[sid]
        if value['entry']['id'] != sid:
            raise SearchError('invalid picker preview session')
        dialogue = ''
        if not isinstance(value['status'].get('recap'), dict):
            dialogue = local_dialogue(Path(manifest['root']), value['entry'])
        print(render_session(value['entry'], value['title'], value['status'], dialogue)[1], end='')


def send_action(port, token, action):
    request = urllib.request.Request('http://127.0.0.1:' + str(port) + '/',
                                     data=action.encode('utf-8'), headers={'x-api-key': token})
    # Ignore proxy configuration for this process-local control channel.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=0.3) as response:
        response.read()


def stop_picker(process):
    if process is not None and process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def pick_recent(results, names, root, manager):
    """Return a trusted entry after all background work has been reaped."""
    entries = [entry for entry, _ in results]
    by_id = {entry['id']: entry for entry in entries}
    if len(by_id) != len(entries) or any(not isinstance(sid, str) or session_id(sid) != sid for sid in by_id):
        manager.close()
        raise SearchError('invalid or duplicate recent-session UUID')
    process = None
    previous_handlers = {}
    if threading.current_thread() is threading.main_thread():
        def interrupted(signum, _frame):
            raise SystemExit(128 + signum)
        for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            previous_handlers[signum] = signal.signal(signum, interrupted)
    try:
        with tempfile.TemporaryDirectory(prefix='codex-search-picker-') as temporary, \
                tempfile.TemporaryFile(mode='w+', encoding='utf-8') as selected_output:
            directory = Path(temporary)
            directory.chmod(0o700)
            token = secrets.token_urlsafe(32)
            atomic_json(directory / 'manifest.json', {'ids': list(by_id), 'root': str(root), 'api_key': token})
            seen_rows = set()
            last_states = None

            def publish():
                nonlocal last_states
                states = [manager.status(entry) for entry in entries]
                encoded = json.dumps(states, ensure_ascii=True, sort_keys=True)
                if encoded == last_states:
                    return False
                rows = []
                sessions = {}
                for entry, status in zip(entries, states):
                    title = names.get(entry['id'], '')
                    row, _ = render_session(entry, title, status)
                    rows.append(row)
                    seen_rows.add(row)
                    sessions[entry['id']] = {'entry': entry, 'title': title, 'status': status}
                atomic_json(directory / 'sessions.json', sessions)
                # Input indexes never change in this opening. fzf 0.44 tracks
                # those indexes, not UUIDs or full row text, across reloads.
                atomic_text(directory / 'rows', '\n'.join(rows) + '\n')
                last_states = encoded
                return True

            publish()
            callback = shlex.join([sys.executable, str(Path(__file__).resolve()), '--helper'])
            location = shlex.quote(str(directory))
            env = dict(os.environ)
            for name in ('FZF_DEFAULT_OPTS', 'FZF_DEFAULT_OPTS_FILE', 'FZF_DEFAULT_COMMAND'):
                env.pop(name, None)
            env.update(FZF_API_KEY=token, SHELL='/bin/sh')
            command = ['fzf', '--no-multi', '--no-sort', '--track', '--delimiter=\t',
                       '--with-nth=3,4,2', '--nth=1..3', '--tabstop=1', '--no-hscroll', '--listen=127.0.0.1:0',
                       '--prompt=Recent Codex> ', '--header=Enter resume; Ctrl-G recap; Ctrl-/ preview; Esc cancel',
                       '--preview=' + callback + ' preview ' + location + ' {1}',
                       '--preview-window=right:60%:wrap:<70(down:60%:wrap)',
                       '--bind=start:execute-silent:' + callback + ' start ' + location,
                       '--bind=ctrl-g:execute-silent:' + callback + ' request ' + location + ' {1}',
                       '--bind=load:refresh-preview', '--bind=ctrl-/:toggle-preview']
            with (directory / 'rows').open('r', encoding='utf-8') as initial:
                process = subprocess.Popen(command, stdin=initial, stdout=selected_output, env=env)
            manager.start(entries)
            port = None
            pending_refresh = False
            while process.poll() is None:
                if port is None and (directory / 'port.json').exists():
                    port = read_json(directory / 'port.json')
                    if type(port) is not int or not 0 < port < 65536:
                        raise SearchError('invalid picker port')
                for request in directory.glob('request-*'):
                    sid = request.name.removeprefix('request-')
                    if sid in by_id:
                        secure_file(request)
                        request.unlink()
                        manager.request(by_id[sid])
                pending_refresh = publish() or pending_refresh
                if port is not None and pending_refresh:
                    # Keep the query and track the highlighted input index while
                    # it still matches. Updated titles are re-filtered normally.
                    action = 'reload-sync(cat ' + shlex.quote(str(directory / 'rows')) + ')+refresh-preview'
                    try:
                        send_action(port, token, action)
                    except (OSError, urllib.error.URLError):
                        # A late reply may race a normal picker exit. Retry only
                        # while this same picker is alive, never restart it.
                        pass
                    else:
                        pending_refresh = False
                time.sleep(0.05)
            code = process.wait()
            if code in (1, 130):
                return None
            if code != 0:
                raise SearchError(f'fzf failed (exit {code}); see its terminal error above')
            selected_output.seek(0)
            selected = selected_output.read().rstrip('\n')
            if selected not in seen_rows:
                raise SearchError('fzf returned an invalid selection; nothing was launched')
            return by_id[selected.split('\t', 1)[0]]
    finally:
        for signum in previous_handlers:
            signal.signal(signum, signal.SIG_IGN)
        try:
            stop_picker(process)
        finally:
            try:
                manager.close()
            finally:
                for signum, handler in previous_handlers.items():
                    signal.signal(signum, handler)


if __name__ == '__main__':
    try:
        if len(sys.argv) not in (4, 5) or sys.argv[1] != '--helper':
            raise SearchError('this module is an internal codex-search picker helper')
        helper(*sys.argv[2:])
    except (SearchError, OSError, ValueError, KeyError, TypeError) as error:
        print('codex-search picker: ' + visible(str(error)), file=sys.stderr)
        sys.exit(2)
