#!/usr/bin/env python3
"""Verify recent-picker updates and cleanup with real fzf and synthetic workers."""
import argparse
import errno
import fcntl
import json
import os
from pathlib import Path
import pty
import queue
import select
import shutil
import signal
import struct
import subprocess
import sys
import tempfile
import termios
import threading
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
ID1 = '00000000-0000-4000-8000-000000000001'
ID2 = '00000000-0000-4000-8000-000000000002'


class SyntheticManager:
    """A single deterministic Python subprocess stands in for each inference."""
    model = 'synthetic-no-provider'

    def __init__(self, log):
        self.log = log
        self.states = {}
        self.jobs = queue.Queue()
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.process = None
        self.thread = None

    def record(self, event, **data):
        with self.log.open('a', encoding='utf-8') as output:
            output.write(json.dumps({'event': event, **data}) + '\n')

    def start(self, entries):
        self.record('start')
        self.jobs.put(entries[0])
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def request(self, entry):
        self.record('request', id=entry['id'])
        self.jobs.put(entry)

    def status(self, entry):
        with self.lock:
            return self.states.get(entry['id'], {'status': 'missing', 'recap': None,
                                                  'partial': False, 'detail': ''}).copy()

    def run(self):
        while not self.stop.is_set():
            try:
                entry = self.jobs.get(timeout=0.05)
            except queue.Empty:
                continue
            sid = entry['id']
            with self.lock:
                if self.stop.is_set():
                    return
                self.states[sid] = {'status': 'generating', 'recap': None, 'partial': False, 'detail': ''}
                recap = {'headline': 'Ready ' + sid[-1], 'goal': 'SYNTHETIC GOAL ' + sid[-1],
                         'progress': ['SYNTHETIC PROGRESS'], 'state': 'Fixture response only.',
                         'next_steps': ['SYNTHETIC NEXT']}
                code = 'import time; time.sleep(0.6); print(' + repr(json.dumps(recap)) + ')'
                process = subprocess.Popen([sys.executable, '-c', code], stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, text=True, start_new_session=True)
                self.process = process
                self.record('worker', pid=process.pid, id=sid)
            stdout, _ = process.communicate()
            with self.lock:
                self.process = None
                if not self.stop.is_set() and process.returncode == 0:
                    self.states[sid] = {'status': 'ready', 'recap': json.loads(stdout),
                                        'partial': False, 'detail': ''}
            self.record('reaped', pid=process.pid)

    def close(self):
        self.stop.set()
        with self.lock:
            if self.process is not None and self.process.poll() is None:
                os.killpg(self.process.pid, signal.SIGTERM)
        if self.thread is not None:
            self.thread.join(timeout=3)
            if self.thread.is_alive():
                raise RuntimeError('synthetic worker was not reaped')
        self.record('closed')


def exercise(base, mode, fzf, columns=150):
    cancel = mode != 'select'
    fixture = base / (mode + '-' + str(columns))
    fixture.mkdir(mode=0o700)
    cache = fixture / 'cache'
    cache.mkdir(mode=0o700)
    bins = fixture / 'bin'
    bins.mkdir()
    (bins / 'fzf').symlink_to(fzf)
    log = fixture / 'events.jsonl'
    result_path = fixture / 'result.json'
    entries = []
    for n, sid in enumerate((ID1, ID2), 1):
        token = str(n) * 32
        dialogue = token + '.dialogue.jsonl'
        (cache / dialogue).write_text(json.dumps({'role': 'user', 'text': 'SYNTHETIC INITIAL'}) + '\n' +
                                      json.dumps({'role': 'assistant', 'text': 'SYNTHETIC LATEST'}) + '\n')
        (cache / dialogue).chmod(0o600)
        entries.append({'id': sid, 'cwd': str(fixture), 'timestamp': '2026-10-07T15:00:0' + str(3-n) + 'Z',
                        'dialogue': dialogue, 'dialogue_hash': '0' * 64})
    child, master = pty.fork()
    if child == 0:
        try:
            fcntl.ioctl(0, termios.TIOCSWINSZ, struct.pack('HHHH', 30, columns, 0, 0))
            os.environ.update(TERM='xterm-256color', TMPDIR=str(fixture),
                              PATH=str(bins) + os.pathsep + os.environ['PATH'])
            tempfile.tempdir = str(fixture)
            from codex_search_recent import pick_recent
            manager = SyntheticManager(log)
            selected = pick_recent([(entry, []) for entry in entries],
                                   {ID1: 'group Implement fast directory sizes',
                                    ID2: 'group Review complete session titles'}, cache, manager)
            result_path.write_text(json.dumps(None if selected is None else selected['id']))
            os._exit(0)
        except SystemExit as error:
            result_path.write_text(json.dumps({'signal': error.code}))
            os._exit(0)
        except BaseException:
            import traceback
            traceback.print_exc()
            os._exit(1)
    transcript = bytearray()
    finished = False
    connection = None

    def drain():
        while select.select([master], [], [], 0)[0]:
            try:
                transcript.extend(os.read(master, 65536))
            except OSError as error:
                if error.errno != errno.EIO:
                    raise
                break

    def wait_for(predicate, description):
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            drain()
            try:
                value = predicate()
                if value:
                    return value
            except (OSError, ValueError, KeyError):
                pass
            time.sleep(0.025)
        raise AssertionError(description + '\n' + transcript.decode('utf-8', 'replace')[-1800:])

    def events():
        return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []

    def request(action=None):
        directory, manifest, port = connection
        req = urllib.request.Request('http://127.0.0.1:' + str(port),
                                     data=None if action is None else action.encode(),
                                     headers={'x-api-key': manifest['api_key']})
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(req, timeout=0.5) as response:
            payload = response.read()
            return json.loads(payload) if action is None else payload

    try:
        def discover():
            for directory in fixture.glob('codex-search-picker-*'):
                if (directory / 'port.json').exists():
                    return directory, json.loads((directory / 'manifest.json').read_text()), json.loads((directory / 'port.json').read_text())
            return None
        connection = wait_for(discover, 'picker listener did not start')
        wait_for(lambda: request()['totalCount'] == 2, 'picker did not display both sessions')
        wait_for(lambda: any(event['event'] == 'worker' for event in events()), 'synthetic worker did not start')
        if cancel:
            # Interrupt while the deterministic subprocess is still running.
            if mode == 'signal':
                os.kill(child, signal.SIGTERM)
            else:
                os.write(master, b'\x1b' if mode == 'escape' else b'\x03')
        else:
            os.write(master, b'group')
            wait_for(lambda: request()['query'] == 'group', 'query was not entered')
            request('pos(2)')
            wait_for(lambda: request()['current']['text'].startswith(ID2), 'second UUID not highlighted')
            wait_for(lambda: 'Ready 1' in request()['matches'][0]['text'], 'automatic recap did not update the row')
            state = request()
            assert state['query'] == 'group', state
            assert state['current']['text'].startswith(ID2), state
            # Ctrl-G requests the highlighted session outside automatic newest-one.
            os.write(master, b'\x07')
            wait_for(lambda: any(event.get('event') == 'request' and event.get('id') == ID2 for event in events()),
                     'Ctrl-G did not request the highlighted UUID')
            wait_for(lambda: 'Ready 2' in request()['current']['text'], 'selected recap did not update')
            state = request()
            assert state['query'] == 'group' and state['current']['text'].startswith(ID2), state
            wait_for(lambda: b'SYNTHETIC NEXT' in transcript, 'updated recap was not visible in the preview')
            os.write(master, b'\r')
        wait_for(result_path.exists, 'picker did not return')
        _, status = os.waitpid(child, 0)
        finished = True
        assert os.waitstatus_to_exitcode(status) == 0, transcript.decode('utf-8', 'replace')
        expected = {'signal': 128 + signal.SIGTERM} if mode == 'signal' else None if cancel else ID2
        assert json.loads(result_path.read_text()) == expected
        observed = events()
        assert observed[-1]['event'] == 'closed', observed
        worker_pids = {item['pid'] for item in observed if item['event'] == 'worker'}
        reaped_pids = {item['pid'] for item in observed if item['event'] == 'reaped'}
        assert worker_pids == reaped_pids, observed
        for pid in worker_pids:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                pass
            else:
                raise AssertionError('synthetic worker still exists: ' + str(pid))
        assert not list(fixture.glob('codex-search-picker-*')), 'private picker directory was not removed'
    finally:
        if not finished:
            if connection is not None:
                try:
                    request('abort')
                except (OSError, ValueError):
                    pass
            time.sleep(0.1)
            try:
                os.killpg(child, signal.SIGTERM)
            except ProcessLookupError:
                pass
            os.waitpid(child, 0)
            for event in events():
                if event['event'] == 'worker':
                    try:
                        os.killpg(event['pid'], signal.SIGTERM)
                    except ProcessLookupError:
                        pass
        os.close(master)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fzf', default=shutil.which('fzf'), help='trusted fzf executable; no model calls are made')
    args = parser.parse_args()
    if not args.fzf:
        parser.error('fzf is required for this synthetic terminal check')
    fzf = str(Path(args.fzf).resolve())
    with tempfile.TemporaryDirectory(prefix='codex-recent-live-') as temporary:
        for mode in ('select', 'escape', 'ctrl-c', 'signal'):
            exercise(Path(temporary), mode, fzf)
        exercise(Path(temporary), 'select', fzf, columns=80)
    print('query, selection, Ctrl-G, cancellation and worker cleanup passed')


if __name__ == '__main__':
    main()
