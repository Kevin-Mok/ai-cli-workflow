"""Asynchronous recent-session picker; inference belongs to the recap manager."""
import json
from contextlib import ExitStack
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

from codex_search_index import SearchError, atomic_json, epoch, secure_file, session_id, visible

STATUSES = {'missing', 'queued', 'stale', 'generating', 'unavailable', 'ready', 'indexing'}


PRIORITY_ORDER = {'urgent': 0, 'actionable': 1, 'unknown': 2, 'waiting': 3, 'complete': 4}


def priority_value(status, current_only=False):
    recap = status.get('recap')
    value = recap.get('priority') if isinstance(recap, dict) else None
    if value not in PRIORITY_ORDER or (current_only and status.get('status') != 'ready'):
        return 'unknown'
    return value


def order_sessions(entries, statuses, sort='priority'):
    """Rank current AI evidence, then latest activity; stale evidence is unknown."""
    recent = sorted(entries, key=lambda entry: (epoch(entry.get('timestamp', '')), entry['id']), reverse=True)
    if sort == 'recent':
        return recent
    return sorted(recent, key=lambda entry:
        PRIORITY_ORDER[priority_value(statuses.get(entry['id'], {}), current_only=True)])


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
        elif state == 'indexing':
            badge = 'indexing'
        elif state == 'missing':
            if status.get('generation_enabled') is True:
                badge = 'Ctrl-G'
            elif status.get('generation_enabled') is False:
                badge = 'recaps off'
        if badge:
            row_title += ' [' + badge + ']'
    activity = activity_time(entry.get('timestamp', ''))
    short_activity = activity_time(entry.get('timestamp', ''), compact=True)
    priority = priority_value(status)
    if priority != 'unknown':
        row_title += ' [' + priority + ('; stale' if state != 'ready' else '') + ']'
    row = '\t'.join((entry['id'], visible(short_activity or '(activity unknown)'),
                     visible(compact_directory(entry.get('cwd', ''))),
                     visible(row_title),
                     visible('[' + label + '] ' + str(headline))))
    lines = [visible(display_title)]
    if display_title != (title or '(untitled)'):
        lines.append('Original title: ' + visible(title if title.strip() else '(untitled)'))
    lines.extend(['Directory: ' + visible(entry.get('cwd', '')),
                  'Activity: ' + visible(activity), 'AI recap: ' + label])
    freshness = ' (stale)' if priority != 'unknown' and state != 'ready' else ''
    lines.append('Priority: ' + priority + freshness)
    reason = recap.get('priority_reason') if isinstance(recap, dict) else None
    if reason:
        lines.append('Priority reason: ' + visible(str(reason)))
    elif priority == 'unknown':
        lines.append('Priority reason: No current AI priority evidence.')
    if status.get('watch_detail'):
        lines.append(visible(status['watch_detail']))
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
    if entry.get('index_pending'):
        return 'Indexing local dialogue; this session can already be resumed.'
    name = entry.get('dialogue', '')
    if not isinstance(name, str) or not re.fullmatch(r'[0-9a-f]{32}\.dialogue\.jsonl', name):
        return ''
    try:
        from codex_search_recaps import bounded_dialogue, file_lock
        with file_lock(root / '.lock', blocking=False) as acquired:
            if not acquired:
                return 'Refreshing local dialogue; preview will update shortly.'
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


def picker_header(sort, detail='', plain=False):
    heading = ('AI priority' if sort == 'priority' else 'Newest first')
    header = ('' if plain else '🧭 ') + heading + '; Enter resume; Ctrl-G recap; Ctrl-/ preview; Esc cancel'
    if detail:
        header += '\n' + '\n'.join(visible(line) for line in detail.splitlines()[:2])
    return header


def helper(mode, directory, sid=None):
    path, manifest = runtime_manifest(directory)
    if mode == 'start' and sid is None:
        port = int(os.environ.get('FZF_PORT', '0'))
        if not 0 < port < 65536:
            raise SearchError('invalid picker port')
        atomic_json(path / 'port.json', port)
        return
    if mode in ('capture', 'restore', 'settled'):
        reload = read_json(path / 'reload.json')
        revision = reload.get('revision')
        if (type(revision) is not int or revision < 1 or
                reload.get('rows') != f'rows-{revision}' or type(reload.get('restore')) is not bool):
            raise SearchError('invalid picker reload snapshot')
        rows_path = path / reload['rows']
        secure_file(rows_path)
    if mode == 'settled':
        if sid != str(revision):
            raise SearchError('invalid completed picker revision')
        atomic_json(path / 'settled.json', {'revision': revision})
        return
    if mode == 'capture':
        atomic_json(path / 'focus.json', sid if sid in manifest['ids'] else None)
        print(rows_path.read_text(), end='')
        return
    if mode == 'restore':
        header = path / 'header'
        if header.exists():
            secure_file(header)
            print(header.read_text(), end='')
        else:
            print(picker_header(manifest.get('sort', 'priority'), plain=manifest.get('plain', False)))
        if not reload['restore']:
            atomic_json(path / 'loaded.json', {'revision': revision, 'action': 'refresh-preview'})
            return
        action = 'rebind(enter,ctrl-g)+refresh-preview'
        if reload['restore']:
            focus_path = path / 'focus.json'
            focus = read_json(focus_path) if focus_path.exists() else None
            if focus in manifest['ids']:
                # fzf filter returns transformed display text; retain UUID as
                # an excluded matching field so lookup uses stable identity.
                with rows_path.open('r', encoding='utf-8') as rows:
                    filtered = subprocess.run(['fzf', '--no-sort', '--delimiter=\t',
                        '--with-nth=1,3,4,2', '--nth=2..4', '--filter=' + (sid or '')],
                        stdin=rows, capture_output=True, text=True)
                if filtered.returncode not in (0, 1):
                    raise SearchError('cannot restore session selection')
                position = next((n for n, row in enumerate(filtered.stdout.splitlines(), 1)
                                 if row.split('\t', 1)[0] == focus), None)
                if position:
                    action = f'pos({position})+' + action
            atomic_json(focus_path, None)
        # The parent sends this action after the synchronous callback returns.
        # A concurrent listener GET can wait on fzf's event loop; calling POST
        # from this callback would then wait on that GET and deadlock the loop.
        atomic_json(path / 'loaded.json', {'revision': revision, 'action': action})
        return
    if mode == 'accept':
        if sid in manifest['ids']:
            atomic_json(path / 'accepted.json', sid)
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


def pick_recent(results, names, root, manager, sort='priority'):
    """Return a trusted entry after all background work has been reaped."""
    entries = [entry for entry, _ in results]
    by_id = {entry['id']: entry for entry in entries}
    if len(by_id) != len(entries) or any(not isinstance(sid, str) or session_id(sid) != sid for sid in by_id):
        manager.close()
        raise SearchError('invalid or duplicate recent-session UUID')
    process = None
    watcher = None
    previous_handlers = {}
    if threading.current_thread() is threading.main_thread():
        def interrupted(signum, _frame):
            raise SystemExit(128 + signum)
        for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            previous_handlers[signum] = signal.signal(signum, interrupted)
    try:
        with tempfile.TemporaryDirectory(prefix='codex-search-picker-') as temporary, \
                tempfile.TemporaryFile(mode='w+', encoding='utf-8') as selected_output, \
                ExitStack() as resources:
            directory = Path(temporary)
            directory.chmod(0o700)
            token = secrets.token_urlsafe(32)
            plain = getattr(manager, 'plain', False)
            atomic_json(directory / 'manifest.json', {'ids': list(by_id), 'root': str(root), 'api_key': token, 'sort': sort, 'plain': plain})
            atomic_json(directory / 'initial-entries.json', entries)
            seen_rows = set()
            last_states = None
            revision = 0
            pending_order = []

            def publish():
                nonlocal last_states, revision, pending_order
                states = {entry['id']: manager.status(entry) for entry in entries}
                watch_detail = watcher.detail() if watcher else ''
                if watch_detail:
                    states = {sid: {**status, 'watch_detail': watch_detail} for sid, status in states.items()}
                encoded = json.dumps([entries, names, states, watch_detail], ensure_ascii=True, sort_keys=True)
                if encoded == last_states:
                    return False
                rows = []
                sessions = {}
                ordered = order_sessions(entries, states, sort)
                pending_order = [entry['id'] for entry in ordered]
                for entry in ordered:
                    status = states[entry['id']]
                    title = names.get(entry['id'], '')
                    row, _ = render_session(entry, title, status)
                    rows.append(row)
                    seen_rows.add(row)
                    sessions[entry['id']] = {'entry': entry, 'title': title, 'status': status}
                atomic_json(directory / 'sessions.json', sessions)
                atomic_text(directory / 'header', picker_header(sort, watch_detail, plain) + '\n')
                # Every reload captures/restores a UUID; fzf input positions
                # can change as priority or activity evidence arrives.
                revision += 1
                atomic_text(directory / f'rows-{revision}', '\n'.join(rows) + '\n')
                last_states = encoded
                return True

            publish()
            in_flight = revision
            in_flight_since = time.monotonic()
            in_flight_order = pending_order
            loaded_order = pending_order
            atomic_json(directory / 'reload.json', {'revision': revision, 'rows': f'rows-{revision}', 'restore': False})
            callback = shlex.join([sys.executable, str(Path(__file__).resolve()), '--helper'])
            location = shlex.quote(str(directory))
            env = dict(os.environ)
            for name in ('FZF_DEFAULT_OPTS', 'FZF_DEFAULT_OPTS_FILE', 'FZF_DEFAULT_COMMAND'):
                env.pop(name, None)
            env.update(FZF_API_KEY=token, SHELL='/bin/sh')
            command = ['fzf', '--no-multi', '--no-sort', '--track', '--delimiter=\t',
                       '--with-nth=3,4,2', '--nth=1..3', '--tabstop=1', '--no-hscroll', '--listen=127.0.0.1:0',
                       '--prompt=' + ('' if plain else '🧭 ') + 'Recent Codex> ',
                       '--header=' + picker_header(sort, plain=plain),
                       '--preview=' + callback + ' preview ' + location + ' {1}',
                       '--preview-window=right:60%:wrap:<70(down:60%:wrap)',
                       '--bind=start:execute-silent:' + callback + ' start ' + location,
                       '--bind=ctrl-g:execute-silent:' + callback + ' request ' + location + ' {1}',
                       '--bind=load:transform-header:' + callback + ' restore ' + location + ' {q}',
                       '--bind=enter:execute-silent(' + callback + ' accept ' + location + ' {1})+abort',
                       '--bind=ctrl-/:toggle-preview']
            if getattr(manager, 'plain', False):
                command.append('--no-unicode')
            with (directory / f'rows-{revision}').open('r', encoding='utf-8') as initial:
                process = subprocess.Popen(command, stdin=initial, stdout=selected_output, env=env)
            resources.callback(stop_picker, process)
            manager.start(entries)
            home = getattr(manager, 'home', None)
            if home is not None:
                from codex_search_watch import SessionWatcher
                watcher = SessionWatcher(root, home, directory,
                                         details=getattr(manager, 'details', False),
                                         plain=getattr(manager, 'plain', False))
                resources.callback(watcher.close)
                watcher.start()
            port = None
            latest_snapshot = None
            pending_refresh = False
            restoration_sent = False
            while process.poll() is None:
                if port is None and (directory / 'port.json').exists():
                    port = read_json(directory / 'port.json')
                    if type(port) is not int or not 0 < port < 65536:
                        raise SearchError('invalid picker port')
                if watcher is not None:
                    snapshot = watcher.read()
                    if snapshot is not None and snapshot is not latest_snapshot:
                        entries = snapshot['entries']
                        names = snapshot['names']
                        by_id = {entry['id']: entry for entry in entries}
                        atomic_json(directory / 'manifest.json', {
                            'ids': list(by_id), 'root': str(root), 'api_key': token, 'sort': sort, 'plain': plain})
                        manager.update(entries)
                        latest_snapshot = snapshot
                for request in directory.glob('request-*'):
                    sid = request.name.removeprefix('request-')
                    if sid in by_id:
                        secure_file(request)
                        request.unlink()
                        manager.request(by_id[sid])
                        if by_id[sid].get('index_pending') and by_id[sid].get('source'):
                            atomic_json(directory / ('index-request-' + sid), by_id[sid]['source'])
                callback_error = directory / 'callback-error.json'
                if callback_error.exists():
                    if process.poll() is not None:
                        break
                    raise SearchError('selection refresh failed; reopen the picker: ' + str(read_json(callback_error)))
                pending_refresh = publish() or pending_refresh
                loaded = directory / 'loaded.json'
                if in_flight is not None and port is not None and loaded.exists() and not restoration_sent:
                    completed = read_json(loaded)
                    if completed.get('revision') == in_flight:
                        if not isinstance(completed.get('action'), str) or not re.fullmatch(
                                r'(pos\([1-9][0-9]*\)\+)?(rebind\(enter,ctrl-g\)\+)?refresh-preview', completed['action']):
                            raise SearchError('invalid selection restoration action')
                        action = completed['action'] + '+execute-silent(' + callback + ' settled ' + location + ' ' + str(in_flight) + ')'
                        restoration_sent = True
                        try:
                            send_action(port, token, action)
                        except (OSError, urllib.error.URLError):
                            try:
                                process.wait(timeout=0.1)
                            except subprocess.TimeoutExpired:
                                pass  # A lost HTTP reply does not prove the action failed.
                            else:
                                break  # The listener can close just before fzf exits.
                settled = directory / 'settled.json'
                if in_flight is not None and restoration_sent and settled.exists():
                    if read_json(settled).get('revision') == in_flight:
                        loaded_order = in_flight_order
                        in_flight = None
                        restoration_sent = False
                if port is not None and pending_refresh and in_flight is None:
                    restore = pending_order != loaded_order
                    atomic_json(directory / 'reload.json', {
                        'revision': revision, 'rows': f'rows-{revision}', 'restore': restore})
                    if restore:
                        action = ('unbind(enter,ctrl-g)+reload-sync(' + callback + ' capture ' + location + ' {1})')
                    else:
                        action = 'reload-sync(cat ' + shlex.quote(str(directory / f'rows-{revision}')) + ')+refresh-preview'
                    # Delivery can be uncertain after an HTTP timeout. Retain
                    # this generation until its callback acknowledges it.
                    pending_refresh = False
                    in_flight = revision
                    in_flight_order = pending_order
                    restoration_sent = False
                    in_flight_since = time.monotonic()
                    try:
                        send_action(port, token, action)
                    except (OSError, urllib.error.URLError):
                        pass  # Keep immutable state even if the reply was lost.
                if in_flight is not None and time.monotonic() - in_flight_since > 10:
                    if process.poll() is not None:
                        break
                    raise SearchError('session order refresh did not finish; reopen the picker')
                # Keep the active immutable input and newest pending input only.
                for old_rows in directory.glob('rows-*'):
                    if old_rows.name not in {f'rows-{revision}', f'rows-{in_flight}'}:
                        old_rows.unlink(missing_ok=True)
                time.sleep(0.05)
            code = process.wait()
            accepted = directory / 'accepted.json'
            if accepted.exists():
                sid = read_json(accepted)
                if not isinstance(sid, str) or sid not in by_id:
                    raise SearchError('selected session disappeared; nothing was launched')
                return by_id[sid]
            if code in (1, 130):
                return None
            if code != 0:
                raise SearchError(f'fzf failed (exit {code}); see its terminal error above')
            selected_output.seek(0)
            selected = selected_output.read().rstrip('\n')
            if selected not in seen_rows:
                raise SearchError('fzf returned an invalid selection; nothing was launched')
            sid = selected.split('\t', 1)[0]
            if sid not in by_id:
                raise SearchError('selected session disappeared; nothing was launched')
            return by_id[sid]
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
        if len(sys.argv) >= 4 and sys.argv[2] in ('capture', 'restore', 'settled'):
            try:
                path, _ = runtime_manifest(sys.argv[3])
                atomic_json(path / 'callback-error.json', visible(str(error)))
            except (SearchError, OSError, ValueError, KeyError, TypeError):
                pass
        print(('' if os.environ.get('CLI_PLAIN') == '1' else '❌ ') + 'codex-search picker: ' + visible(str(error)), file=sys.stderr)
        sys.exit(2)
