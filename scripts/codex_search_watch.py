"""Cancellable local index refresh for an open recent-session picker."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

from codex_search_index import (SearchError, atomic_json, recent_entries, refresh,
                                secure_directory, secure_file, session_id, titles, warn)
from codex_search_recaps import file_lock, maintain_cache, stop_process

POLL_SECONDS = 2.0


class SessionWatcher:
    """A private child process keeps slow source parsing off the picker thread."""
    def __init__(self, root, home, directory, interval=POLL_SECONDS, *, details=False, plain=False):
        self.root, self.home, self.directory = Path(root), Path(home), Path(directory)
        self.interval = interval
        self.details, self.plain = details, plain
        self.process = None
        self._signature = None
        self._snapshot = None

    def start(self):
        if self.process is None:
            log = self.directory / 'watcher.log'
            descriptor = os.open(log, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
            with os.fdopen(descriptor, 'w') as diagnostics:
                secure_file(log)
                environment = dict(os.environ)
                if self.plain:
                    environment['CLI_PLAIN'] = '1'
                self.process = subprocess.Popen(
                    [sys.executable, str(Path(__file__).resolve()), '--worker',
                     str(self.root), str(self.home), str(self.directory), str(self.interval),
                     '1' if self.details else '0'],
                    stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                    stderr=diagnostics, env=environment, start_new_session=True)

    def read(self):
        path = self.directory / 'updates.json'
        try:
            info = path.stat()
            signature = (info.st_ino, info.st_mtime_ns, info.st_size)
            if signature == self._signature:
                return self._snapshot
            secure_file(path)
            value = json.loads(path.read_text())
        except FileNotFoundError:
            return self._snapshot
        if not isinstance(value, dict) or set(value) != {'entries', 'names'}:
            raise SearchError('invalid session refresh snapshot')
        entries, names = value['entries'], value['names']
        if not isinstance(entries, list) or not isinstance(names, dict):
            raise SearchError('invalid session refresh metadata')
        ids = set()
        for entry in entries:
            if not isinstance(entry, dict):
                raise SearchError('invalid refreshed session')
            sid = entry.get('id')
            if not isinstance(sid, str) or session_id(sid) != sid or sid in ids:
                raise SearchError('invalid refreshed session UUID')
            ids.add(sid)
            pending = entry.get('index_pending', False)
            if type(pending) is not bool:
                raise SearchError('invalid refreshed indexing status')
            if not all(isinstance(entry.get(k), str) for k in ('cwd', 'timestamp', 'dialogue', 'dialogue_hash')):
                raise SearchError('invalid refreshed session evidence')
            provisional = pending and entry['dialogue'] == '' and entry['dialogue_hash'] == ''
            if (not provisional and
                    (not re.fullmatch(r'[0-9a-f]{32}\.dialogue\.jsonl', entry['dialogue']) or
                     not re.fullmatch(r'[0-9a-f]{64}', entry['dialogue_hash']))):
                raise SearchError('invalid refreshed session evidence')
        if any(not isinstance(sid, str) or session_id(sid) != sid or not isinstance(title, str)
               for sid, title in names.items()):
            raise SearchError('invalid refreshed session title')
        self._signature, self._snapshot = signature, value
        return value

    def detail(self):
        def message(value, icon):
            return ('' if self.plain else icon + ' ') + value
        if self.process is not None and self.process.poll() is not None:
            return message('Live session updates unavailable; reopen the picker to retry.', '⚠️')
        path = self.directory / 'watch-status.json'
        try:
            secure_file(path)
            value = json.loads(path.read_text())
            lines = []
            if value.get('error'):
                lines.append(message('Local refresh paused; usable sessions remain available.', '⚠️'))
            elif value.get('waiting'):
                lines.append(message('Waiting for local index lock; sessions remain resumable.', '⏳'))
            elif value.get('scanning') or value.get('pending'):
                elapsed = max(0, int(time.monotonic() - value['started']))
                total, pending = value.get('total'), value.get('pending')
                count = f"{total - pending}/{total} sources ready; " if type(total) is int and type(pending) is int else ''
                lines.append(message(f'Indexing local sessions: {count}{elapsed}s elapsed.', '⏳'))
            if value.get('skipped') or value.get('unreadable'):
                lines.append(message('Some records skipped; usable sessions shown.', '⚠️'))
            if self.details:
                log = self.directory / 'watcher.log'
                secure_file(log)
                with log.open('rb') as source:
                    source.seek(max(0, log.stat().st_size - 4096))
                    tail = source.read().decode('utf-8', 'replace').splitlines()[-4:]
                lines.extend(tail)
            return '\n'.join(lines)
        except (OSError, ValueError, KeyError, TypeError):
            pass
        return ''

    def close(self):
        if self.process is not None:
            stop_process(self.process)


def watch(root, home, directory, interval, details=False):
    secure_directory(root)
    secure_directory(directory)
    previous = None
    seed_path = directory / 'initial-entries.json'
    seed = {}
    if seed_path.exists():
        secure_file(seed_path)
        for entry in json.loads(seed_path.read_text()):
            if isinstance(entry, dict) and isinstance(entry.get('source'), str):
                seed[entry['source']] = entry
    started = time.monotonic()
    statistics = {}
    while True:
        acquired = False
        atomic_json(directory / 'watch-status.json', {**statistics, 'scanning': True, 'started': started})
        try:
            with file_lock(root / '.lock', blocking=False) as acquired:
                if acquired:
                    requests = {}
                    for request in directory.glob('index-request-*'):
                        if session_id(request.name.removeprefix('index-request-')):
                            secure_file(request)
                            source = json.loads(request.read_text())
                            if isinstance(source, str):
                                requests[request] = source
                    statistics = {}
                    indexed = refresh(root, home, details=details, max_updates=20,
                                      stats=statistics, preferred_sources=requests.values())
                    inventory = set(statistics['sources'])
                    inaccessible = [Path(folder) for folder in statistics.get('unreadable_directories', [])]
                    seed = {source: entry for source, entry in seed.items()
                            if source in inventory or any(Path(source).is_relative_to(folder) for folder in inaccessible)}
                    merged = {**seed, **{source: dict(entry, source=source) for source, entry in indexed.items()}}
                    entries = [entry for entry, _ in recent_entries(merged)]
                    names = titles(home, details=details)
                    if not statistics['pending'] and not statistics.get('discovery_incomplete'):
                        maintain_cache(root, {entry['id'] for entry in entries})
                    value = {'entries': entries, 'names': names}
                    encoded = json.dumps(value, sort_keys=True)
                    if encoded != previous:
                        atomic_json(directory / 'updates.json', value)
                        previous = encoded
                    pending = set(statistics['pending_sources'])
                    for request, source in requests.items():
                        if source not in inventory or source not in pending:
                            request.unlink(missing_ok=True)
            atomic_json(directory / 'watch-status.json', {
                **statistics, 'scanning': False, 'waiting': not acquired, 'started': started})
        except (OSError, ValueError, SearchError) as error:
            atomic_json(directory / 'watch-status.json', {
                **statistics, 'scanning': False, 'error': True, 'started': started})
            if details:
                warn('local session refresh paused: ' + str(error))
        # Release the lock between batches so previews and recap input can proceed.
        time.sleep(.05 if statistics.get('pending') and statistics.get('refreshed') and acquired else interval)


if __name__ == '__main__':
    if len(sys.argv) not in (6, 7) or sys.argv[1] != '--worker':
        raise SystemExit('Internal codex-search session watcher; use codex-search --recent --pick.')
    watch(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), max(.05, float(sys.argv[5])),
          details=len(sys.argv) == 7 and sys.argv[6] == '1')
