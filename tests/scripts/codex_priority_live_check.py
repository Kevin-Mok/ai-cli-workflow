#!/usr/bin/env python3
"""Exercise live Guardian priority updates through the real CLI and fzf, without model calls."""
import argparse
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import pty
import select
import shutil
import signal
import struct
import sys
import tempfile
import termios
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / 'scripts/executable_codex-search'
ID1 = '00000000-0000-4000-8000-000000009001'
ID2 = '00000000-0000-4000-8000-000000009002'
MODEL = 'synthetic-priority-no-provider'
QUERY = 'priority-group'
UPDATE_TIME = '2026-10-09T12:01:00Z'
UPDATED_TITLE = 'Guardian verified complete'


def cli_message(message, icon='✅'):
    return ('' if os.environ.get('CLI_PLAIN') == '1' else icon + ' ') + message


def record(path, **value):
    """One append write keeps independently spawned fixture processes readable."""
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(descriptor, (json.dumps(value) + '\n').encode())
    finally:
        os.close(descriptor)


class LocalRuntime:
    """Replace only the external runtime; the production queue/cache stay intact."""
    def __init__(self, home, model_override=None):
        self.model = model_override or MODEL
        self.log = Path(os.environ['PRIORITY_FIXTURE_EVENTS'])

    def prepare(self):
        record(self.log, event='prepared', pid=os.getpid(), model=self.model)
        return self.model

    def cancel(self):
        record(self.log, event='cancelled', pid=os.getpid())

    def command(self, workdir, schema_path, output_path):
        return [sys.executable, str(Path(__file__).resolve()), '--synthetic-worker',
                str(output_path), str(self.log)], dict(os.environ)


def synthetic_worker(output_path, log):
    prompt = sys.stdin.read()
    dialogue = prompt.split('BEGIN INERT DIALOGUE\n', 1)[1].rsplit('\nEND INERT DIALOGUE', 1)[0]
    first = 'PRIORITY_LIVE_UUID_1' in dialogue
    sid = ID1 if first else ID2
    if not first and 'PRIORITY_LIVE_UUID_2' not in dialogue:
        raise AssertionError('fixture worker received no synthetic session marker')
    complete = 'Guardian verified complete' in dialogue
    priority = 'complete' if complete else 'urgent' if first else 'actionable'
    record(log, event='worker', pid=os.getpid(), id=sid, priority=priority,
           digest=hashlib.sha256(dialogue.encode()).hexdigest())
    time.sleep(0.4)
    recap = {'headline': 'Fixture verified complete' if complete else 'Fixture urgent repair' if first else 'Fixture actionable task',
             'goal': 'Verify a synthetic priority workflow.',
             'progress': 'The conversation reports verified completion.' if complete else 'The conversation reports unfinished work.',
             'state': 'Verified complete.' if complete else 'Current issue needs attention.' if first else 'A concrete next step is available.',
             'next_steps': 'No remaining action reported.' if complete else 'Advance the reported next step.',
             'priority': priority,
             'priority_reason': 'Guardian reports completion with verification.' if complete else 'Synthetic active harm needs immediate repair.' if first else 'Synthetic work can proceed now.'}
    Path(output_path).write_text(json.dumps(recap))
    record(log, event='result', pid=os.getpid(), id=sid, priority=priority)


def child_cli(arguments):
    import runpy
    command = Path(os.environ.get('PRIORITY_FIXTURE_COMMAND', str(COMMAND))).resolve()
    sys.path.insert(0, str(command.parent))
    import codex_search_runtime
    codex_search_runtime.IsolatedCodex = LocalRuntime
    sys.argv = [str(command), *arguments]
    runpy.run_path(str(command), run_name='__main__')


def process_children(parent):
    """Linux exposes children of the main thread and recap worker separately."""
    children = set()
    tasks = Path('/proc') / str(parent) / 'task'
    if tasks.exists():
        for task in tasks.iterdir():
            try:
                children.update(map(int, (task / 'children').read_text().split()))
            except FileNotFoundError:
                pass
    return children


def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


class Picker:
    def __init__(self, base, environment, arguments, resume_path):
        self.base = base
        self.log = Path(environment['PRIORITY_FIXTURE_EVENTS'])
        self.resume_path = resume_path
        self.connection = None
        self.transcript = bytearray()
        self.children = set()
        self.finished = False
        self.child, self.master = pty.fork()
        if self.child == 0:
            fcntl.ioctl(0, termios.TIOCSWINSZ, struct.pack('HHHH', 36, 160, 0, 0))
            os.execvpe(sys.executable, [sys.executable, str(Path(__file__).resolve()),
                       '--child-cli', *arguments],
                       {**environment, 'PRIORITY_FIXTURE_RESUME': str(resume_path)})

    def drain(self):
        self.children.update(process_children(self.child))
        while select.select([self.master], [], [], 0)[0]:
            try:
                self.transcript.extend(os.read(self.master, 65536))
            except OSError as error:
                if error.errno != errno.EIO:
                    raise
                break

    def wait(self, predicate, description, timeout=12):
        began = time.monotonic()
        deadline = began + timeout
        progress = began + 3
        while time.monotonic() < deadline:
            if time.monotonic() >= progress:
                print(cli_message(f"Waiting: {description} ({int(time.monotonic() - began)}s elapsed)", '⏳'),
                      file=sys.stderr, flush=True)
                progress = time.monotonic() + 3
            self.drain()
            try:
                value = predicate()
                if value:
                    return value
            except (FileNotFoundError, ConnectionError, json.JSONDecodeError,
                    urllib.error.URLError, TimeoutError):
                pass
            time.sleep(0.025)
        evidence = ''
        if self.connection is not None:
            try:
                state = self.state()
                evidence = json.dumps({'query': state.get('query'), 'current': state.get('current'),
                                       'matches': state.get('matches'), 'sessions': self.sessions()}, indent=2)
            except (OSError, ValueError, urllib.error.URLError) as error:
                evidence = 'Listener diagnostic unavailable: ' + str(error)
            for name in ('reload.json', 'loaded.json', 'callback-error.json'):
                path = self.connection[0] / name
                if path.exists():
                    evidence += '\n' + name + ': ' + path.read_text()
        raise AssertionError(description + '\n' + evidence + '\n' +
                             self.transcript.decode('utf-8', 'replace')[-5000:])

    def discover(self):
        def listener():
            for directory in self.base.glob('codex-search-picker-*'):
                port = directory / 'port.json'
                if port.exists():
                    manifest = json.loads((directory / 'manifest.json').read_text())
                    return directory, manifest, json.loads(port.read_text())
        self.connection = self.wait(listener, 'real CLI did not publish the fzf listener')
        self.wait(lambda: self.state()['totalCount'] == 2, 'fzf did not display both synthetic sessions')
        self.wait(lambda: any('codex_search_watch.py' in self.commandline(pid)
                             for pid in process_children(self.child)),
                  'production source watcher did not start')

    @staticmethod
    def commandline(pid):
        try:
            return (Path('/proc') / str(pid) / 'cmdline').read_bytes().decode('utf-8', 'replace')
        except FileNotFoundError:
            return ''

    def state(self, action=None):
        _, manifest, port = self.connection
        request = urllib.request.Request('http://127.0.0.1:' + str(port),
                  data=None if action is None else action.encode(),
                  headers={'x-api-key': manifest['api_key']})
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(request, timeout=0.5) as response:
            data = response.read()
            return json.loads(data) if action is None else data

    def sessions(self):
        return json.loads((self.connection[0] / 'sessions.json').read_text())

    def ready(self, sid, priority):
        status = self.sessions()[sid]['status']
        return status['status'] == 'ready' and status['recap']['priority'] == priority

    def identity(self, sid):
        state = self.state()
        return (state['query'] == QUERY and state.get('current') is not None
                and state['current']['text'].startswith(sid + '\t'))

    def order(self):
        return [item['text'].split('\t', 1)[0] for item in self.state()['matches']]

    def filter_and_select(self, sid):
        os.write(self.master, QUERY.encode())
        self.wait(lambda: self.state()['query'] == QUERY and self.state()['matchCount'] == 2,
                  'directory query did not match both sessions')
        position = self.wait(lambda: self.order().index(sid) + 1,
                             'visible UUID position could not be read')
        try:
            self.state(f'pos({position})')
        except (TimeoutError, urllib.error.URLError):
            pass  # Observe identity below; a lost reply does not justify replay.
        self.wait(lambda: self.identity(sid), 'fixture selected the wrong UUID')

    def finish(self, sid, cwd):
        os.write(self.master, b'\r')
        self.wait(self.resume_path.exists, 'Enter did not invoke the normal codex executable')
        _, status = os.waitpid(self.child, 0)
        self.finished = True
        self.drain()
        assert os.waitstatus_to_exitcode(status) == 0, self.transcript.decode('utf-8', 'replace')
        observed = json.loads(self.resume_path.read_text())
        assert observed['args'] == ['resume', '-C', str(cwd), sid], observed
        assert not list(self.base.glob('codex-search-picker-*')), 'private picker directory survived resume'
        assert not list(self.base.glob('codex-recap-*')), 'private inference directory survived resume'
        for pid in self.children:
            assert not alive(pid), f'picker/watcher/worker PID survived resume: {pid}'
        for event in read_events(self.log):
            if event['event'] == 'worker':
                assert not alive(event['pid']), f'inference worker survived resume: {event["pid"]}'

    def close(self):
        if not self.finished:
            if self.connection is not None:
                try:
                    self.state('abort')
                except (OSError, urllib.error.URLError):
                    pass
            deadline = time.monotonic() + 3
            while time.monotonic() < deadline:
                self.drain()
                finished, _ = os.waitpid(self.child, os.WNOHANG)
                if finished:
                    self.finished = True
                    break
                time.sleep(0.025)
            if not self.finished:
                try:
                    os.killpg(self.child, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                os.waitpid(self.child, 0)
            for pid in self.children:
                try:
                    os.killpg(pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
        os.close(self.master)


def read_events(log):
    return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []


def encoded(record):
    return (json.dumps(record) + '\n').encode()


def message(text, stamp, role='assistant'):
    return {'type': 'response_item', 'timestamp': stamp, 'payload': {
        'type': 'message', 'role': role,
        'content': [{'type': 'input_text' if role == 'user' else 'output_text', 'text': text}]}}


def exercise(base, fzf, scenario, command=COMMAND):
    home = base / 'codex'
    sources = home / 'sessions/2026/10/09'
    sources.mkdir(parents=True)
    bins = base / 'bin'
    bins.mkdir()
    (bins / 'fzf').symlink_to(fzf)
    stub = bins / 'codex'
    stub.write_text('#!' + sys.executable + '\nimport json,os,sys\nfrom pathlib import Path\n'
                    'Path(os.environ["PRIORITY_FIXTURE_RESUME"]).write_text('
                    'json.dumps({"args":sys.argv[1:]}))\n'
                    'print("RESUME ARGS: " + json.dumps(sys.argv[1:]))\n')
    stub.chmod(0o755)
    log = base / 'events.jsonl'
    projects = {}
    originals = {}
    for number, sid in enumerate((ID1, ID2), 1):
        cwd = base / f'{QUERY} project {number} with spaces'
        cwd.mkdir()
        projects[sid] = cwd
        stamp = f'2026-10-09T12:00:0{number}Z'
        source = sources / (sid + '.jsonl')
        data = encoded({'type': 'session_meta', 'timestamp': stamp,
                        'payload': {'id': sid, 'cwd': str(cwd)}})
        data += encoded(message(f'PRIORITY_LIVE_UUID_{number} synthetic work', stamp, 'user'))
        data += encoded(message('Active harm requires immediate repair.' if number == 1 else
                                'Concrete next step remains actionable.', stamp))
        source.write_bytes(data)
        originals[source] = data
    index = home / 'session_index.jsonl'
    initial_index = b''.join(encoded({'id': sid, 'thread_name': 'Guardian review'}) for sid in (ID1, ID2))
    index.write_bytes(initial_index)
    env = {**os.environ, 'TERM': 'xterm-256color', 'TMPDIR': str(base),
           'CODEX_HOME': str(home), 'XDG_CACHE_HOME': str(base / 'cache'),
           'PATH': str(bins) + os.pathsep + os.environ['PATH'],
           'PRIORITY_FIXTURE_EVENTS': str(log), 'PRIORITY_FIXTURE_COMMAND': str(command)}
    env.pop('CODEX_THREAD_ID', None)
    env.pop('CODEX_INTERNAL_ORIGINATOR_OVERRIDE', None)
    arguments = ['--recent', '--pick', '--summary-count', '2', '--summary-model', MODEL]
    picker = Picker(base, env, arguments, base / 'live-resume.json')
    try:
        picker.discover()
        picker.wait(lambda: picker.ready(ID1, 'urgent') and picker.ready(ID2, 'actionable'),
                    'actual SummaryManager did not publish initial validated priorities')
        picker.wait(lambda: picker.order() == [ID1, ID2], 'urgent session did not sort first')
        picker.filter_and_select(ID1)
        initial = picker.sessions()[ID1]['entry']
        initial_digest = initial['dialogue_hash']
        original1 = sources / (ID1 + '.jsonl')
        update = encoded(message('Guardian verified complete: synthetic fix and regression checks passed; no remaining action.', UPDATE_TIME))
        with original1.open('ab') as output:
            output.write(update)
        rename = encoded({'id': ID1, 'thread_name': UPDATED_TITLE, 'updated_at': UPDATE_TIME})
        with index.open('ab') as output:
            output.write(rename)
        def refreshed():
            current = picker.sessions()[ID1]
            return (current['entry']['timestamp'] == UPDATE_TIME and
                    current['entry']['dialogue_hash'] != initial_digest and
                    current['title'] == UPDATED_TITLE)
        picker.wait(refreshed, 'live Guardian dialogue/activity/title changes were not published')
        picker.wait(lambda: picker.ready(ID1, 'complete'), 'changed dialogue did not regenerate priority')
        picker.wait(lambda: picker.order() == [ID2, ID1] and picker.identity(ID1),
                    'complete session reorder lost its selected UUID or query')
        picker.wait(lambda: UPDATED_TITLE in picker.state()['current']['text'],
                    'renamed native title did not reach the selected fzf row')
        workers = [event for event in read_events(log) if event['event'] == 'worker']
        assert [(item['id'], item['priority']) for item in workers].count((ID1, 'urgent')) == 1, workers
        assert [(item['id'], item['priority']) for item in workers].count((ID1, 'complete')) == 1, workers
        assert len(workers) == 3, workers
        picker.finish(ID1, projects[ID1])
        assert original1.read_bytes() == originals[original1] + update, 'CLI modified synthetic source beyond fixture append'
        assert (sources / (ID2 + '.jsonl')).read_bytes() == originals[sources / (ID2 + '.jsonl')]
        assert index.read_bytes() == initial_index + rename, 'CLI modified the native title index'
    finally:
        picker.close()
    print(cli_message('Guardian append + rename refreshed activity/digest/title; urgent -> complete moved below actionable.'))
    print(cli_message('Query + selected UUID survived reorder; Enter resumed exact UUID/cwd; watcher/workers removed.'))
    modes = []
    if scenario in ('all', 'cached'):
        modes.append(('cached', 'priority', [ID2, ID1]))
    if scenario in ('all', 'recent'):
        modes.append(('recent', 'recent', [ID1, ID2]))
    count = len([event for event in read_events(log) if event['event'] == 'worker'])
    for label, order, expected in modes:
        arguments = ['--recent', '--pick', '--no-summaries', '--summary-model', MODEL, '--sort', order]
        second = Picker(base, env, arguments, base / (label + '-resume.json'))
        try:
            second.discover()
            second.wait(lambda: second.ready(ID1, 'complete') and second.ready(ID2, 'actionable'),
                        'cached validated priorities were not loaded')
            second.wait(lambda: second.order() == expected, 'cached/recent option showed the wrong order')
            second.filter_and_select(ID1)
            os.write(second.master, b'\x07')
            time.sleep(0.25)
            second.finish(ID1, projects[ID1])
            assert len([event for event in read_events(log) if event['event'] == 'worker']) == count, 'disabled generation called runtime'
            assert original1.read_bytes() == originals[original1] + update
            assert index.read_bytes() == initial_index + rename
        finally:
            second.close()
        print(cli_message(f'{label.capitalize()} order + Ctrl-G reused cache with zero additional model calls; exact resume + cleanup passed.'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fzf', default=shutil.which('fzf'), help='trusted fzf executable (no sudo or provider needed)')
    parser.add_argument('--command', type=Path, default=COMMAND,
                        help='actual source or installed codex-search command; sibling modules are exercised')
    parser.add_argument('--scenario', choices=('all', 'live', 'cached', 'recent'), default='all',
                        help='live update, optionally followed by cached/recent no-summaries verification')
    args = parser.parse_args()
    if not args.fzf:
        parser.error('fzf is required for this disposable PTY check')
    fzf = Path(args.fzf).resolve()
    if not fzf.is_file() or not os.access(fzf, os.X_OK):
        parser.error('--fzf must point to a trusted executable')
    command = args.command.expanduser().resolve()
    if not command.is_file():
        parser.error('--command must point to the source or installed codex-search script')
    print(cli_message("Checking disposable CLI/fzf Guardian refresh; no provider calls.", '⏳'), flush=True)
    with tempfile.TemporaryDirectory(prefix='codex-priority-live-') as temporary:
        exercise(Path(temporary), fzf, args.scenario, command)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--synthetic-worker':
        synthetic_worker(*sys.argv[2:])
    elif len(sys.argv) > 1 and sys.argv[1] == '--child-cli':
        child_cli(sys.argv[2:])
    else:
        main()
