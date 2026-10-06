"""CLI contract tests; all session content is synthetic."""
import concurrent.futures
import errno
import fcntl
import hashlib
import json
import os
import pty
import re
from pathlib import Path
import shlex
import shutil
import stat
import struct
import subprocess
import sys
import tempfile
import termios
import threading
import unicodedata
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/executable_codex-search'
ID1 = '00000000-0000-4000-8000-000000000001'
ID2 = '00000000-0000-4000-8000-000000000002'


def record(kind, payload, timestamp='2026-10-01T12:00:00Z'):
    return {'timestamp': timestamp, 'type': kind, 'payload': payload}


def message(role, text):
    return record('response_item', {'type': 'message', 'role': role,
                  'content': [{'type': 'input_text' if role == 'user' else 'output_text', 'text': text}]})


class CodexSearchTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='codex-search-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / 'codex home'
        self.sessions = self.home / 'sessions'
        self.sessions.mkdir(parents=True)
        self.cache = self.base / 'cache'
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        self.project = self.base / "project spaces ' $(touch NEVER) ;"
        self.project.mkdir()
        self.env = {**os.environ, 'CODEX_HOME': str(self.home), 'XDG_CACHE_HOME': str(self.cache),
                    'PATH': str(self.bin) + os.pathsep + os.environ['PATH'],
                    'NO_COLOR': '1', 'PYTHONDONTWRITEBYTECODE': '1'}
        self.env.pop('RIPGREP_CONFIG_PATH', None)
        self.log = self.base / 'resume.json'
        self.env['RESUME_LOG'] = str(self.log)
        self.env['PICK_LOG'] = str(self.base / 'pick.txt')
        self.stub('codex', "import json,os,sys\nfrom pathlib import Path\nPath(os.environ['RESUME_LOG']).write_text(json.dumps(sys.argv[1:]))")

    def stub(self, name, code):
        path = self.bin / name
        path.write_text('#!' + sys.executable + '\n' + code + '\n')
        path.chmod(0o755)

    def session(self, sid=ID1, text='Needle café 😀\nsecond line', cwd=None, stamp='2026-10-01T12:00:00Z', name='one.jsonl', extra=()):
        path = self.sessions / 'nested' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        data = [record('session_meta', {'id': sid, 'cwd': str(self.project) if cwd is None else cwd, 'timestamp': stamp}, stamp),
                message('user', text), message('assistant', 'Answer alpha42')]
        data.extend(extra)
        path.write_text(''.join(json.dumps(row, ensure_ascii=True) + '\n' for row in data))
        return path

    def run_cli(self, *args, expected=0, env=None):
        self.assertTrue(SCRIPT.is_file(), 'codex-search implementation is missing')
        result = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.base,
                                env=env or self.env, text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, expected, result.stderr + result.stdout)
        return result

    def run_terminal(self, *args, width=80, env=None):
        master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', 24, width, 0, 0))
        chunks = []
        def read_output():
            try:
                while True:
                    chunk = os.read(master, 65536)
                    if not chunk:
                        break
                    chunks.append(chunk)
            except OSError as error:
                if error.errno != errno.EIO:
                    raise
        try:
            with subprocess.Popen([sys.executable, str(SCRIPT), *args], cwd=self.base,
                                  env=env or self.env, stdout=slave, stderr=subprocess.PIPE) as process:
                os.close(slave)
                slave = None
                reader = threading.Thread(target=read_output, daemon=True)
                reader.start()
                _, errors = process.communicate(timeout=30)
                reader.join(timeout=5)
                self.assertFalse(reader.is_alive(), 'terminal reader did not finish')
                output = b''.join(chunks).decode().replace('\r\n', '\n')
                self.assertEqual(process.returncode, 0, errors.decode() + output)
                return output, errors.decode()
        finally:
            os.close(master)
            if slave is not None:
                os.close(slave)

    def manifest(self):
        manifests = list(self.cache.glob('codex-search/*/manifest.json'))
        self.assertEqual(len(manifests), 1)
        return manifests[0], json.loads(manifests[0].read_text())

    def picker(self, cancel=False):
        self.stub('fzf', "import os,sys\nfrom pathlib import Path\nrows=sys.stdin.read()\nPath(os.environ['PICK_LOG']).write_text(rows)\n" +
                  ('sys.exit(130)' if cancel else "print(rows.splitlines()[0])"))

    def test_usage_without_indexing(self):
        result = self.run_cli()
        self.assertIn('Usage:', result.stdout)
        self.assertIn('--pick', result.stdout)
        self.assertIn('--clear-cache', result.stdout)
        self.assertFalse(self.cache.exists())

    def test_help_flags_without_dependencies_or_indexing(self):
        env = {**self.env, 'PATH': str(self.bin)}
        for flag in ('-h', '--help'):
            with self.subTest(flag=flag):
                result = self.run_cli(flag, env=env)
                self.assertIn('ignore case', result.stdout)
                self.assertIn('literal text', result.stdout)
                self.assertIn('codex-search --pick "bug"', result.stdout)
                self.assertIn('docs/smoke-tests.md', result.stdout)
                self.assertEqual('', result.stderr)
                self.assertFalse(self.cache.exists())
                self.assertFalse(self.log.exists())

    def test_terminal_broad_search_is_bounded_and_compact(self):
        for i in range(24):
            sid = '00000000-0000-4000-8000-' + str(i).zfill(12)
            self.session(sid=sid, text='root first snippet\nroot extra snippet',
                         stamp=f'2026-10-{i + 1:02d}T12:00:00Z', name=str(i) + '.jsonl')
        output, errors = self.run_terminal('root')
        self.assertEqual(output.count('codex resume -C'), 20)
        self.assertIn('20 of 24', errors)
        self.assertIn('--limit 0', errors)
        self.assertIn('--pick', errors)
        self.assertNotIn('Title: (untitled)', output)
        self.assertNotIn('root extra snippet', output)
        self.assertIn('2026-10-24 12:00 UTC', output)
        self.assertNotIn('2026-10-24T12:00:00Z', output)
        self.assertIn('00000000-0000-4000-8000-000000000023', output)
        self.assertNotIn('00000000-0000-4000-8000-000000000000', output)
        self.assertLess(len(output.splitlines()), 100)
        self.assertEqual(self.run_cli('root').stdout.count('Resume: '), 24)

    def test_terminal_excerpt_fits_unicode_width_and_highlights_rg_match(self):
        self.session(text='漢字 😀 ' * 30 + 'Café [x]' + ' trailing' * 50)
        env = {**self.env, 'TERM': 'xterm-256color'}
        env.pop('NO_COLOR', None)
        output, _ = self.run_terminal('-iF', 'café [x]', width=54, env=env)
        self.assertRegex(output, r'\x1b\[[0-9;]+mCafé \[x\]\x1b\[0m')
        plain = re.sub(r'\x1b\[[0-9;]*m', '', output)
        line = next(x for x in plain.splitlines() if 'Café [x]' in x)
        cells = sum(0 if unicodedata.combining(c) else 2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1 for c in line)
        self.assertLessEqual(cells, 54)
        disabled, _ = self.run_terminal('-iF', 'café [x]', width=54, env={**env, 'NO_COLOR': '1'})
        self.assertNotIn('\x1b', disabled)
        self.assertIn('Café [x]', disabled)
        self.assertNotIn('\x1b', self.run_cli('-iF', 'café [x]', env=env).stdout)

    def test_trailing_carriage_return_match_keeps_safe_snippet_offsets(self):
        self.session(text='carriage\r')
        result = self.run_cli(r'\r')
        self.assertIn(ID1, result.stdout)
        self.assertIn(r'carriage\r', result.stdout)
        output, _ = self.run_terminal(r'\r')
        self.assertIn(r'carriage\r', output)

    def test_dense_matches_outside_excerpt_do_not_delay_search(self):
        self.session(text='x' * 160000)
        self.run_cli('--rebuild-index')
        try:
            result = subprocess.run([sys.executable, str(SCRIPT), 'x'], cwd=self.base,
                                    env=self.env, capture_output=True, text=True, timeout=5)
        except subprocess.TimeoutExpired:
            self.fail('Dense matches outside the displayed excerpt delayed search beyond 5 seconds')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(ID1, result.stdout)
        self.assertLess(len(result.stdout), 1000)

    def test_very_narrow_terminal_header_does_not_wrap(self):
        self.session()
        output, _ = self.run_terminal('Needle', width=20)
        header = output.splitlines()[0]
        self.assertLessEqual(len(header), 20)

    def test_details_limits_and_picker_keep_complete_matches(self):
        self.session(text='root first\nroot second')
        self.session(ID2, text='root other', stamp='2026-10-05T12:00:00Z', name='two.jsonl')
        output, _ = self.run_terminal('--details', '--limit', '0', 'root')
        self.assertIn('Title: (untitled)', output)
        self.assertIn('Session: ' + ID1, output)
        self.assertIn('root second', output)
        self.assertEqual(output.count('Resume: '), 2)
        limited = self.run_cli('--limit', '1', 'root')
        self.assertIn(ID2, limited.stdout)
        self.assertNotIn(ID1, limited.stdout)
        self.assertIn('1 of 2', limited.stderr)
        self.assertEqual(self.run_terminal('--limit', '0', 'root')[0].count('codex resume -C'), 2)
        self.run_cli('--limit', '-1', 'root', expected=2)
        self.picker(cancel=True)
        self.run_cli('--pick', '--limit', '1', 'root')
        self.assertEqual(len((self.base / 'pick.txt').read_text().splitlines()), 2)
        self.assertFalse(self.log.exists())

    def test_default_conversation_excludes_instructions_tools_and_reasoning(self):
        self.session(extra=[message('system', 'SystemUnique'), message('developer', 'DeveloperUnique'),
                           message('user', '# AGENTS.md instructions for /tmp\n<INSTRUCTIONS>InjectedUnique</INSTRUCTIONS>'),
                           message('user', '<environment_context>EnvironmentUnique</environment_context>'),
                           record('turn_context', {'developer_instructions': 'ContextUnique'}),
                           record('response_item', {'type': 'reasoning', 'summary': [{'text': 'ReasonUnique'}]}),
                           record('response_item', {'type': 'function_call', 'name': 'shell', 'arguments': '{"cmd":"ToolCallUnique"}'}),
                           record('response_item', {'type': 'function_call_output', 'call_id': '1', 'output': 'ToolOutputUnique'})])
        self.assertIn(ID1, self.run_cli('Needle').stdout)
        self.assertIn(ID1, self.run_cli('alpha42').stdout)
        for term in ('SystemUnique', 'DeveloperUnique', 'InjectedUnique', 'EnvironmentUnique', 'ContextUnique', 'ReasonUnique', 'ToolCallUnique', 'ToolOutputUnique'):
            with self.subTest(term=term):
                self.assertEqual('', self.run_cli(term, expected=1).stdout)
        for term in ('ToolCallUnique', 'ToolOutputUnique'):
            self.assertIn(ID1, self.run_cli('--all-text', term).stdout)
        self.assertEqual('', self.run_cli('--all-text', 'SystemUnique', expected=1).stdout)

    def test_rg_regex_literal_case_and_unicode_decoding(self):
        self.session(text='Needle café 😀\nWindows C:\\tmp\\x and a.b [square] tab\there')
        for args in [('alpha[0-9]+',), ('-i', 'needle'), ('café 😀',), ('-F', 'C:\\tmp\\x'), ('^Windows',), ('-F', '[square]'), ('tab\there',)]:
            with self.subTest(args=args):
                self.assertIn(ID1, self.run_cli(*args).stdout)
        self.run_cli('needle', expected=1)
        self.run_cli('-F', 'alpha[0-9]+', expected=1)
        self.run_cli('[', expected=2)
        self.session(text='-flag')
        self.assertIn(ID1, self.run_cli('--', '-flag').stdout)

    def test_titles_are_optional_latest_nonempty_index_entry_wins(self):
        self.session()
        self.session(ID2, name='two.jsonl')
        (self.home / 'session_index.jsonl').write_text('\n'.join(json.dumps(x) for x in [
            {'id': ID1, 'thread_name': 'Old'}, {'id': ID1, 'thread_name': 'New title'},
            {'id': ID1, 'thread_name': ''}, {'id': 'not-a-source', 'thread_name': 'ghost'}]) + '\n')
        out = self.run_cli('Needle').stdout
        self.assertIn('New title', out)
        self.assertNotIn('Old', out)
        self.assertNotIn('ghost', out)
        self.assertIn(ID2, out)
        (self.home / 'session_index.jsonl').write_text(json.dumps({'id': ID1, 'thread_name': 'Renamed'}) + '\n')
        self.assertIn('Renamed', self.run_cli('Needle').stdout)

    def test_newest_first_multiple_directories_and_duplicate_uuid(self):
        self.session(stamp='2026-09-01T12:00:00Z')
        other = self.base / 'second project'
        other.mkdir()
        self.session(ID2, cwd=str(other), stamp='2026-10-05T12:00:00Z', name='two.jsonl')
        self.session(name='duplicate.jsonl', stamp='2026-09-02T12:00:00Z')
        out = self.run_cli('Needle').stdout
        self.assertEqual(out.count('Session: ' + ID1), 1)
        self.assertEqual(out.count('Session: ' + ID2), 1)
        self.assertLess(out.index('Session: ' + ID2), out.index('Session: ' + ID1))
        self.assertIn(str(other), out)
        self.assertIn(str(self.project), out)

    def test_event_only_and_mirrored_messages_do_not_duplicate_snippets(self):
        self.session(text='MirrorUnique', extra=[record('event_msg', {'type': 'user_message', 'message': 'MirrorUnique'}),
                                             record('event_msg', {'type': 'agent_message', 'message': 'EventOnlyUnique'})])
        out = self.run_cli('MirrorUnique').stdout
        self.assertEqual(out.count('MirrorUnique'), 1)
        self.assertIn('EventOnlyUnique', self.run_cli('EventOnlyUnique').stdout)
        path = self.sessions / 'events.jsonl'
        path.write_text(json.dumps(record('session_meta', {'id': ID2, 'cwd': str(self.project)})) + '\n' +
                        json.dumps(record('event_msg', {'type': 'user_message', 'message': 'LegacyUnique'})) + '\n')
        self.assertIn(ID2, self.run_cli('LegacyUnique').stdout)

    def test_malformed_records_and_incomplete_tail_warn_without_payloads(self):
        path = self.session()
        with path.open('a') as out:
            out.write('{secret-payload\n[]\n' + json.dumps(record('response_item', {'type': 'message', 'role': 'user', 'content': None})) + '\n{"unfinished":')
        result = self.run_cli('Needle')
        self.assertIn('skipped', result.stderr.lower())
        self.assertNotIn('secret-payload', result.stderr)
        self.assertIn(ID1, result.stdout)
        with path.open('a') as out:
            out.write('true}\n' + json.dumps(message('user', 'CompletedAppend')) + '\n')
        self.assertIn(ID1, self.run_cli('CompletedAppend').stdout)

    def test_malformed_discriminants_do_not_abort_valid_search(self):
        self.session(extra=[record('response_item', {'type': ['malformed']}),
                            record('event_msg', {'type': {'bad': True}})])
        result = self.run_cli('Needle')
        self.assertIn(ID1, result.stdout)
        self.assertIn('skipped', result.stderr)

    def test_unpaired_surrogates_do_not_abort_valid_search(self):
        self.session(extra=[message('user', 'bad \ud800'),
                            record('event_msg', {'type': 'agent_message', 'message': '\ud800'}),
                            record('response_item', {'type': 'function_call_output', 'output': '\ud800'})])
        result = self.run_cli('Needle')
        self.assertIn(ID1, result.stdout)
        self.assertIn('skipped', result.stderr)

    def test_incremental_refresh_and_deleted_sources(self):
        path = self.session()
        self.run_cli('Needle')
        manifest, _ = self.manifest()
        files = {p: p.stat().st_mtime_ns for p in manifest.parent.rglob('*.txt')}
        self.assertTrue(files)
        self.run_cli('Needle')
        self.assertEqual(files, {p: p.stat().st_mtime_ns for p in manifest.parent.rglob('*.txt')})
        with path.open('a') as out:
            out.write(json.dumps(message('user', 'FreshUnique')) + '\n')
        self.assertIn('FreshUnique', self.run_cli('FreshUnique').stdout)
        path.unlink()
        self.run_cli('FreshUnique', expected=1)
        self.assertEqual([], list(manifest.parent.rglob('*.txt')))

    def test_cache_permissions_separation_version_rebuild_and_clear(self):
        self.session()
        self.run_cli('Needle')
        manifest, data = self.manifest()
        for p in self.cache.rglob('*'):
            self.assertEqual(stat.S_IMODE(p.stat().st_mode), 0o700 if p.is_dir() else 0o600, str(p))
        data['version'] = -1
        manifest.write_text(json.dumps(data))
        self.assertIn('Needle', self.run_cli('Needle').stdout)
        self.assertNotEqual(self.manifest()[1]['version'], -1)
        self.run_cli('--rebuild-index')
        self.run_cli('--clear-cache')
        self.assertFalse(manifest.exists())
        self.assertEqual([], list(manifest.parent.rglob('*.txt')))
        self.run_cli('Needle')
        other_home = self.base / 'other-codex'
        (other_home / 'sessions').mkdir(parents=True)
        self.run_cli('--rebuild-index', env={**self.env, 'CODEX_HOME': str(other_home)})
        self.assertEqual(len(list(self.cache.glob('codex-search/*/manifest.json'))), 2)

    def test_concurrent_refresh_and_clear_are_consistent(self):
        self.session()
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda _: self.run_cli('Needle'), range(8)))
        self.assertTrue(all(ID1 in r.stdout for r in results))
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            list(pool.map(lambda args: self.run_cli(*args), [('Needle',), ('--clear-cache',)]))
        self.assertIn(ID1, self.run_cli('Needle').stdout)

    def test_pick_exact_arguments_and_shell_quoting(self):
        self.session()
        self.picker()
        out = self.run_cli('Needle').stdout
        cmd = next(x.removeprefix('Resume: ') for x in out.splitlines() if x.startswith('Resume: '))
        self.assertEqual(shlex.split(cmd), ['codex', 'resume', '-C', str(self.project), ID1])
        self.run_cli('--pick', 'Needle')
        self.assertEqual(json.loads(self.log.read_text()), ['resume', '-C', str(self.project), ID1])
        self.assertFalse((self.base / 'NEVER').exists())
        self.assertIn(str(self.project), (self.base / 'pick.txt').read_text())

    def test_picker_ui_stderr_reaches_terminal(self):
        self.session()
        self.stub('fzf', "import sys\nprint('Synthetic picker UI',file=sys.stderr)\nprint(sys.stdin.read().splitlines()[0])")
        result = self.run_cli('--pick', 'Needle')
        self.assertIn('Synthetic picker UI', result.stderr)

    def test_pick_cancel_no_results_and_unavailable_dependency_launch_nothing(self):
        self.session()
        self.picker(cancel=True)
        self.run_cli('--pick', 'Needle')
        self.assertFalse(self.log.exists())
        self.run_cli('--pick', 'absent', expected=1)
        self.assertFalse(self.log.exists())
        (self.bin / 'fzf').unlink()
        # Keep the test independent of a developer's installed fzf.
        isolated = self.base / 'isolated'
        isolated.mkdir()
        (isolated / 'rg').symlink_to(shutil.which('rg'))
        result = self.run_cli('--pick', 'Needle', expected=2, env={**self.env, 'PATH': str(isolated)})
        self.assertIn('fzf', result.stderr)
        self.assertIn('install', result.stderr.lower())
        self.assertFalse(self.log.exists())

    def test_missing_relative_or_unrecorded_cwd_never_resumes(self):
        self.picker()
        for cwd in ('', 'relative', str(self.base / 'missing')):
            with self.subTest(cwd=cwd):
                self.session(cwd=cwd)
                self.run_cli('--pick', 'Needle', expected=2)
                self.assertFalse(self.log.exists())

    def test_invalid_unicode_and_control_cwd_are_safe_and_unresumable(self):
        self.picker()
        for cwd in ('bad \ud800', str(self.base / 'control \x1b[31m directory')):
            with self.subTest(cwd=repr(cwd)):
                if '\x1b' in cwd:
                    Path(cwd).mkdir()
                self.session(cwd=cwd)
                result = self.run_cli('Needle')
                self.assertIn('Resume unavailable', result.stdout)
                self.assertNotIn('\x1b', result.stdout)
                self.run_cli('--pick', 'Needle', expected=2)
                self.assertFalse(self.log.exists())

    def test_pipe_consumer_cancellation_is_quiet(self):
        for i in range(100):
            sid = '00000000-0000-4000-8000-' + str(i).zfill(12)
            self.session(sid=sid, name=str(i) + '.jsonl')
        self.run_cli('--rebuild-index')
        process = subprocess.Popen([sys.executable, str(SCRIPT), 'Needle'], env=self.env,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.stdout.readline()
        process.stdout.close()
        errors = process.stderr.read()
        process.stderr.close()
        self.assertEqual(process.wait(timeout=30), 0, errors.decode())
        self.assertNotIn(b'Broken pipe', errors)

    def test_picker_rejects_forged_selection_and_ignores_default_binds(self):
        self.session()
        self.stub('fzf', "import os,sys\nassert 'FZF_DEFAULT_OPTS' not in os.environ\nassert 'FZF_DEFAULT_OPTS_FILE' not in os.environ\nsys.stdin.read()\nprint('forged selection')")
        result = self.run_cli('--pick', 'Needle', expected=2,
                              env={**self.env, 'FZF_DEFAULT_OPTS': '--bind=enter:execute(echo bad)',
                                   'FZF_DEFAULT_OPTS_FILE': '/missing'})
        self.assertIn('invalid selection', result.stderr)
        self.assertFalse(self.log.exists())

    def test_ide_prefix_and_tool_json_are_decoded(self):
        self.session(text='context-hidden\n## My request for Codex:\nactual request', extra=[
            record('response_item', {'type': 'custom_tool_call', 'input': json.dumps({'path': r'C:\tmp', 'note': 'café'})}),
            record('response_item', {'type': 'mcp_tool_call_output', 'output': {'content': [{'type': 'text', 'text': 'MCP unique'}]}})])
        self.run_cli('context-hidden', expected=1)
        self.assertIn(ID1, self.run_cli('actual request').stdout)
        self.assertIn(ID1, self.run_cli('--all-text', '-F', 'C:\\tmp').stdout)
        self.assertIn(ID1, self.run_cli('--all-text', 'MCP unique').stdout)

    def test_sessions_are_read_only_and_rg_config_cannot_change_matching(self):
        path = self.session()
        before = (path.read_bytes(), path.stat().st_mtime_ns)
        config = self.base / 'rg-config'
        config.write_text('--invert-match\n--ignore-case\n')
        self.assertIn(ID1, self.run_cli('Needle', env={**self.env, 'RIPGREP_CONFIG_PATH': str(config)}).stdout)
        self.run_cli('--all-text', 'absent', expected=1)
        self.assertEqual(before, (path.read_bytes(), path.stat().st_mtime_ns))

    def test_invalid_cache_manifest_recovers_and_symlink_cache_is_rejected(self):
        self.session()
        self.run_cli('Needle')
        manifest, _ = self.manifest()
        manifest.write_text('{broken')
        result = self.run_cli('Needle')
        self.assertIn('cache', result.stderr.lower())
        self.run_cli('--clear-cache')
        shutil.rmtree(manifest.parent)
        manifest.parent.symlink_to(self.base / 'bin')
        self.run_cli('Needle', expected=2)


if __name__ == '__main__':
    unittest.main()
