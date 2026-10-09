#!/usr/bin/env python3
"""Verify prompt Codex picker startup using real fzf and disposable archives only."""
import argparse
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import pty
import shutil
import struct
import subprocess
import sys
import tempfile
import termios
import time
import urllib.error

from codex_priority_live_check import (COMMAND, ID1, ID2, Picker, encoded, message,
                                       process_children, read_events)

OLD_ID = '00000000-0000-4000-8000-000000009003'
MALFORMED_MARKER = 'STARTUP_PRIVATE_MALFORMED_PAYLOAD'
STARTUP_SECONDS = 2.0
PHASE_SECONDS = 8.0


def progress(text, icon='⏳', *, plain=False, error=False):
    print(('' if plain else icon + ' ') + text,
          file=sys.stderr if error else sys.stdout, flush=True)


class StartupPicker(Picker):
    """Reuse fzf API and cleanup checks, but launch the unmodified selected CLI."""
    def __init__(self, base, environment, arguments, resume_path, command, plain):
        self.base = base
        self.log = Path(environment['PRIORITY_FIXTURE_EVENTS'])
        self.resume_path = resume_path
        self.connection = None
        self.transcript = bytearray()
        self.children = set()
        self.finished = False
        self.plain = plain
        self.started = time.monotonic()
        self.child, self.master = pty.fork()
        if self.child == 0:
            fcntl.ioctl(0, termios.TIOCSWINSZ, struct.pack('HHHH', 36, 160, 0, 0))
            os.execvpe(sys.executable, [sys.executable, str(command), *arguments],
                       {**environment, 'PRIORITY_FIXTURE_RESUME': str(resume_path)})

    def wait(self, predicate, description, timeout=PHASE_SECONDS):
        started = time.monotonic()
        deadline, next_progress = started + timeout, started + 1
        while time.monotonic() < deadline:
            self.drain()
            try:
                result = predicate()
                if result:
                    return result
            except (FileNotFoundError, ConnectionError, json.JSONDecodeError,
                    urllib.error.URLError, TimeoutError):
                pass
            if time.monotonic() >= next_progress:
                progress(f'{description}: {int(time.monotonic() - started)}s elapsed',
                         plain=self.plain, error=True)
                next_progress = time.monotonic() + 1
            time.sleep(.025)
        raise AssertionError(description + '\n' +
                             self.transcript.decode('utf-8', 'replace')[-5000:])

    def discover(self, expected):
        def listener():
            for directory in self.base.glob('codex-search-picker-*'):
                port = directory / 'port.json'
                if port.exists():
                    return (directory, json.loads((directory / 'manifest.json').read_text()),
                            json.loads(port.read_text()))
        self.connection = self.wait(listener, 'Actual CLI listener not ready within 2s',
                                    timeout=STARTUP_SECONDS)
        remaining = STARTUP_SECONDS - (time.monotonic() - self.started)
        assert remaining > 0, 'fzf listener exceeded the startup deadline'
        self.wait(lambda: set(self.order()) == set(expected),
                  'Healthy UUIDs not visible within 2s', timeout=remaining)
        elapsed = time.monotonic() - self.started
        assert elapsed < STARTUP_SECONDS, f'Visible healthy rows took {elapsed:.3f}s'
        self.wait(lambda: any('codex_search_watch.py' in self.commandline(pid)
                             for pid in process_children(self.child)),
                  'Background source watcher did not start')
        return elapsed

    def select(self, sid):
        position = self.wait(lambda: self.order().index(sid) + 1,
                             'Visible UUID position could not be read')
        try:
            self.state(f'pos({position})')
        except (TimeoutError, urllib.error.URLError):
            # The action may already have executed; observe identity without replay.
            pass
        self.wait(lambda: (self.state().get('current') or {}).get('text', '').startswith(sid + '\t'),
                  'Visible UUID selection did not settle')

    def preview(self, sid, command, environment):
        result = subprocess.run([sys.executable, str(command.parent / 'codex_search_recent.py'),
                                 '--helper', 'preview', str(self.connection[0]), sid],
                                env=environment, capture_output=True, text=True, timeout=2)
        assert result.returncode == 0, result.stderr
        return result.stdout


def source_bytes(sid, cwd, stamp, text):
    return (encoded({'type': 'session_meta', 'timestamp': stamp,
                     'payload': {'id': sid, 'cwd': str(cwd)}})
            + encoded(message(text, stamp, 'user'))
            + encoded(message('Synthetic unfinished work remains resumable.', stamp)))


def prepare(base, fzf, scenario, command, plain):
    home = base / 'codex'
    sources = home / 'sessions/2026/10/09'
    sources.mkdir(parents=True)
    bins = base / 'bin'; bins.mkdir()
    (bins / 'fzf').symlink_to(fzf)
    stub = bins / 'codex'
    stub.write_text('#!' + sys.executable + '\nimport json,os,sys\nfrom pathlib import Path\n'
                    'args=sys.argv[1:]\n'
                    'log=Path(os.environ["PRIORITY_FIXTURE_EVENTS"])\n'
                    'with log.open("a") as out:out.write(json.dumps({"event":"codex","args":args})+"\\n")\n'
                    'if not args or args[0]!="resume":raise SystemExit("Provider/runtime calls forbidden")\n'
                    'Path(os.environ["PRIORITY_FIXTURE_RESUME"]).write_text(json.dumps({"args":args}))\n'
                    'print("RESUME ARGS: " + json.dumps(args))\n')
    stub.chmod(0o755)
    environment = {**os.environ, 'TERM': 'xterm-256color', 'TMPDIR': str(base),
                   'CODEX_HOME': str(home), 'XDG_CACHE_HOME': str(base / 'cache'),
                   'PATH': str(bins) + os.pathsep + os.environ['PATH'],
                   'PRIORITY_FIXTURE_EVENTS': str(base / 'events.jsonl')}
    environment.pop('CODEX_THREAD_ID', None)
    environment.pop('CODEX_INTERNAL_ORIGINATOR_OVERRIDE', None)
    if plain:
        environment['CLI_PLAIN'] = '1'
    originals, projects = {}, {}
    for number, sid in enumerate((ID1, ID2), 1):
        cwd = base / f'startup project {number} with spaces'; cwd.mkdir()
        projects[sid] = cwd
        source = sources / (sid + '.jsonl')
        data = source_bytes(sid, cwd, f'2026-10-09T12:00:0{number}Z',
                            f'Startup healthy session {number}')
        if scenario == 'malformed' and number == 1:
            data += ('{"' + MALFORMED_MARKER + '":\n').encode() * 3
        source.write_bytes(data); originals[source] = data
    expected = [ID1, ID2]
    if scenario == 'cold':
        old = home / 'sessions/2020/01/01/old-archive.jsonl'
        old.parent.mkdir(parents=True)
        data = source_bytes(OLD_ID, projects[ID1], '2020-01-01T00:00:00Z',
                            'Large old archive metadata remains selectable.')
        # A full archive pass must parse many malformed records; initial metadata
        # needs only its bounded native header while the index lock is held.
        data += ('{"' + MALFORMED_MARKER + '":\n').encode() * 250000
        old.write_bytes(data); originals[old] = data
        expected.append(OLD_ID)
    elif scenario == 'malformed':
        neighbor = sources / 'unfinished-neighbor.jsonl'
        data = ('{"' + MALFORMED_MARKER + '":\n').encode() * 6
        neighbor.write_bytes(data); originals[neighbor] = data
    native_index = home / 'session_index.jsonl'
    native_index.write_bytes(b''.join(encoded({'id': sid, 'thread_name': 'Startup healthy session'})
                                      for sid in expected))
    originals[native_index] = native_index.read_bytes()
    cache = base / 'cache/codex-search' / hashlib.sha256(os.fsencode(home)).hexdigest()
    cache.mkdir(mode=0o700, parents=True)
    for parent in (cache, cache.parent):
        parent.chmod(0o700)
    return environment, originals, projects, expected, cache


def exercise(base, fzf, scenario, command, plain, details=False):
    base.mkdir()
    environment, originals, projects, expected, cache = prepare(base, fzf, scenario, command, plain)
    if scenario in ('cached', 'locked'):
        warm = subprocess.run([sys.executable, str(command), '--recent', '--plain'],
                              env=environment, capture_output=True, text=True, timeout=8)
        assert warm.returncode == 0, warm.stderr
        assert (cache / 'manifest.json').is_file(), 'warm invocation did not create the index'
        manifest = json.loads((cache / 'manifest.json').read_text())
        assert {entry['id'] for entry in manifest['sources'].values()} == set(expected), warm.stdout
    lock = None
    if scenario in ('cold', 'locked'):
        lock = (cache / '.lock').open('a+')
        (cache / '.lock').chmod(0o600)
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if scenario == 'cold':
            assert not (cache / 'manifest.json').exists(), 'cold fixture already had a manifest'
    arguments = ['--recent', '--pick', '--no-summaries']
    if plain:
        arguments.append('--plain')
    if details:
        arguments.append('--details')
    picker = StartupPicker(base, environment, arguments, base / 'resume.json', command, plain)
    try:
        elapsed = picker.discover(expected)
        if lock is not None:
            picker.wait(lambda: json.loads((picker.connection[0] / 'watch-status.json').read_text()).get('waiting'),
                        'Watcher did not report the held index lock')
            assert not read_events(picker.log), 'CLI invoked codex before exact resume'
            if scenario == 'cold':
                assert not (cache / 'manifest.json').exists(), 'full indexing ran before the lock release'
                assert picker.sessions()[ID1]['entry'].get('index_pending'), 'cold row was not pending'
                assert 'Indexing local dialogue' in picker.preview(ID1, command, environment)
        if scenario == 'malformed':
            picker.wait(lambda: json.loads((picker.connection[0] / 'watch-status.json').read_text()).get('skipped') == 9,
                        'Background index did not retain all nine skipped-record counts')
            picker.wait(lambda: 'Some records skipped' in picker.preview(ID1, command, environment),
                        'Usable-row preview did not disclose limited record accuracy')
            preview = picker.preview(ID1, command, environment)
            if details:
                picker.wait(lambda: '3 malformed/incomplete' in picker.preview(ID1, command, environment)
                            and '6 malformed/incomplete' in picker.preview(ID1, command, environment),
                            'Details preview omitted per-source skipped counts')
            else:
                assert 'malformed/incomplete' not in preview, 'Default preview exposed raw diagnostics'
            assert MALFORMED_MARKER not in preview, 'Malformed payload leaked to preview'
        picker.select(ID1)
        picker.finish(ID1, projects[ID1])
        # Locked cases resume/cancel while another indexer still owns the lock.
        assert all(path.read_bytes() == data for path, data in originals.items()), 'CLI modified source bytes'
        events = read_events(picker.log)
        assert len(events) == 1 and events[0]['args'][0] == 'resume', events
        if not details:
            terminal = picker.transcript.decode('utf-8', 'replace')
            assert 'malformed/incomplete' not in terminal, 'Malformed warning flood reached fzf'
            assert MALFORMED_MARKER not in terminal, 'Malformed payload leaked to terminal'
    finally:
        picker.close()
        if lock is not None:
            fcntl.flock(lock, fcntl.LOCK_UN)
            lock.close()
    label = scenario + ('-details' if details else '')
    progress(f'PASS {label}: listener + healthy UUIDs in {elapsed:.3f}s (limit 2s); exact resume + cleanup.',
             '✅', plain=plain)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario', choices=('all', 'cold', 'cached', 'malformed', 'locked'), default='all')
    parser.add_argument('--command', type=Path, default=COMMAND,
                        help='actual source (default) or installed codex-search command')
    parser.add_argument('--fzf', default=shutil.which('fzf'), help='trusted real fzf executable')
    parser.add_argument('--plain', action='store_true', help='ASCII progress output')
    args = parser.parse_args()
    plain = args.plain or os.environ.get('CLI_PLAIN') == '1'
    if not args.fzf:
        parser.error('real fzf is required; no sudo or provider is needed')
    fzf, command = Path(args.fzf).expanduser().resolve(), args.command.expanduser().resolve()
    if not fzf.is_file() or not os.access(fzf, os.X_OK):
        parser.error('--fzf must point to a trusted executable')
    if not command.is_file():
        parser.error('--command must point to the actual source or installed script')
    scenarios = ('cold', 'cached', 'locked', 'malformed') if args.scenario == 'all' else (args.scenario,)
    progress('Checking actual CLI + real fzf startup; disposable archives, summaries disabled.', plain=plain)
    with tempfile.TemporaryDirectory(prefix='codex-startup-live-') as temporary:
        root = Path(temporary)
        for scenario in scenarios:
            progress(f'Checking {scenario} startup...', plain=plain)
            exercise(root / scenario, fzf, scenario, command, plain)
            if scenario == 'malformed':
                progress('Checking malformed details preview...', plain=plain)
                exercise(root / 'malformed-details', fzf, scenario, command, plain, details=True)
    progress('Provider calls: 0; exact UUID/cwd resume; source bytes unchanged; cleanup passed.', '✅', plain=plain)


if __name__ == '__main__':
    main()
