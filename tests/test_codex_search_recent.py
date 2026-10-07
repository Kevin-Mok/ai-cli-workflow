"""Recent-mode CLI contracts using invented sessions only."""
import json
import os
from pathlib import Path
import unittest
import test_codex_search as fixture


class RecentCLITest(unittest.TestCase):
    setUp = fixture.CodexSearchTest.setUp
    stub = fixture.CodexSearchTest.stub
    def session(self, *args, **kwargs):
        path = fixture.CodexSearchTest.session(self, *args, **kwargs)
        sid = json.loads(path.read_text().splitlines()[0])['payload']['id']
        with (self.home / 'session_index.jsonl').open('a') as index:
            index.write(json.dumps({'id': sid, 'thread_name': 'Synthetic task ' + sid}) + '\n')
        return path

    run_cli = fixture.CodexSearchTest.run_cli
    manifest = fixture.CodexSearchTest.manifest

    def test_recent_defaults_to_twenty_even_in_pipe_and_limit_zero_means_all(self):
        for i in range(24):
            sid = '00000000-0000-4000-8000-' + str(i).zfill(12)
            self.session(sid=sid, stamp=f'2026-10-{i+1:02d}T12:00:00Z', name=f'{i}.jsonl')
        result = self.run_cli('--recent')
        self.assertEqual(result.stdout.count('Resume: '), 20)
        self.assertEqual(self.run_cli('--recent', '--limit', '0').stdout.count('Resume: '), 24)
        self.assertEqual(self.run_cli('--recent', '--limit', '2').stdout.count('Resume: '), 2)
        self.assertFalse(self.log.exists(), 'listing must not invoke Codex')

    def test_recent_cross_directory_activity_dedup_and_title(self):
        other = self.base / 'other'; other.mkdir()
        self.session(stamp='2025-01-01T00:00:00Z', extra=[fixture.record('event_msg', {'type':'task_complete'}, '2026-10-07T10:00:00Z')])
        self.session(fixture.ID2, name='two.jsonl', cwd=str(other), stamp='2026-10-06T10:00:00Z')
        self.session(name='copy.jsonl', stamp='2026-10-02T10:00:00Z')
        with (self.home/'session_index.jsonl').open('a') as index:
            index.write(json.dumps({'id':fixture.ID1,'thread_name':'Recent synthetic task'})+'\n')
        output = self.run_cli('--recent').stdout
        self.assertEqual(output.count('Session: '+fixture.ID1), 1)
        self.assertLess(output.index('Session: '+fixture.ID1), output.index('Session: '+fixture.ID2))
        for value in ('Recent synthetic task', str(other), str(self.project), 'missing'):
            self.assertIn(value, output)

    def test_recent_no_summaries_and_zero_count_listing_never_run_codex(self):
        self.session()
        for args in [('--recent',), ('--recent','--no-summaries'), ('--recent','--summary-count','0'), ('--recent','--summary-model','synthetic-model')]:
            with self.subTest(args=args):
                self.run_cli(*args)
                self.assertFalse(self.log.exists())

    def test_recent_hides_untitled_and_guardian_before_limit_and_picker(self):
        titles = [None, '', ' Untitled ', '(UNTITLED)', 'Guardian review', 'guardian safety check', 'Visible task']
        ids = []
        for i, title in enumerate(titles):
            sid = '00000000-0000-4000-8000-' + str(i + 10).zfill(12)
            ids.append(sid)
            fixture.CodexSearchTest.session(self, sid=sid, name=f'filter-{i}.jsonl', stamp=f'2026-10-{20-i:02d}T12:00:00Z')
            if title is not None:
                with (self.home / 'session_index.jsonl').open('a') as index:
                    index.write(json.dumps({'id': sid, 'thread_name': title}) + '\n')
        before = {p: p.read_bytes() for p in self.sessions.rglob('*.jsonl')}
        output = self.run_cli('--recent', '--limit', '1').stdout
        self.assertEqual(output.count('Session: '), 1)
        self.assertIn(ids[-1], output)
        for sid in ids[:-1]:
            self.assertNotIn(sid, output)
        self.stub('fzf', "import sys,os\nfrom pathlib import Path\nrows=sys.stdin.read().splitlines()\nPath(os.environ['PICK_LOG']).write_text('\\n'.join(rows))\nprint(rows[0])")
        self.run_cli('--recent', '--pick', '--no-summaries')
        rows = (self.base / 'pick.txt').read_text().splitlines()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].split('\t')[0], ids[-1])
        self.assertEqual(json.loads(self.log.read_text()), ['resume', '-C', str(self.project), ids[-1]])
        for path, original in before.items():
            self.assertEqual(path.read_bytes(), original)

    def test_recent_all_hidden_skips_picker_but_pattern_search_still_finds_them(self):
        fixture.CodexSearchTest.session(self)
        self.run_cli('--recent', expected=1)
        self.stub('fzf', "raise AssertionError('empty recent results must not open picker')")
        self.run_cli('--recent', '--pick', '--no-summaries', expected=1)
        self.assertFalse(self.log.exists())
        self.assertIn(fixture.ID1, self.run_cli('-F', 'Needle').stdout)

    def test_recent_help_and_invalid_combinations(self):
        for args in [(),('--help',)]:
            output = self.run_cli(*args).stdout
            for option in ('--recent','--summary-count','--summary-model','--no-summaries'):
                self.assertIn(option, output)
        for args in [('--recent','pattern'),('--recent','--summary-count','-1'),('--recent','--clear-cache')]:
            self.run_cli(*args, expected=2)

    def test_recent_picker_disabled_summaries_exact_resume_and_all_rows(self):
        self.session()
        self.session(fixture.ID2,name='two.jsonl')
        self.stub('fzf', "import sys,os\nfrom pathlib import Path\nrows=sys.stdin.read().splitlines()\nPath(os.environ['PICK_LOG']).write_text('\\n'.join(rows))\nprint(rows[0])")
        self.run_cli('--recent','--pick','--no-summaries','--limit','1')
        self.assertEqual(len((self.base/'pick.txt').read_text().splitlines()),2)
        sid=(self.base/'pick.txt').read_text().split('\t')[0]
        self.assertEqual(json.loads(self.log.read_text()),['resume','-C',str(self.project),sid])

    def test_recent_cancel_never_resumes_or_changes_source(self):
        path=self.session(); before=path.read_bytes()
        self.stub('fzf','import sys\nsys.stdin.read()\nsys.exit(130)')
        self.run_cli('--recent','--pick','--no-summaries')
        self.assertFalse(self.log.exists())
        self.assertEqual(path.read_bytes(),before)

    def test_recent_forged_selection_is_rejected(self):
        self.session()
        self.stub('fzf',"import sys\nsys.stdin.read()\nprint('00000000-0000-4000-8000-000000000099\\tforged')")
        self.run_cli('--recent','--pick','--no-summaries',expected=2)
        self.assertFalse(self.log.exists())

    def test_cli_index_lock_is_free_while_real_manager_inference_is_active(self):
        import subprocess
        import sys
        self.session()
        started=self.base/'generation-started'
        self.stub('fzf', '''import fcntl,json,os,sys,time
from pathlib import Path
sys.stdin.read()
marker=Path(os.environ['RECAP_STARTED'])
end=time.monotonic()+5
while not marker.exists() and time.monotonic()<end:time.sleep(.01)
if not marker.exists():sys.exit(3)
root=next(Path(os.environ['XDG_CACHE_HOME']).glob('codex-search/*'))
with (root/'.lock').open('r+') as lock:
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
Path(os.environ['PICK_LOG']).write_text('index lock free during active inference')
sys.exit(130)
''')
        code='''import os,sys,runpy
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import codex_search_runtime
class Runtime:
    def __init__(self,*args):pass
    def prepare(self):return 'synthetic'
    def cancel(self):pass
    def command(self,workdir,schema,output):
        program="import os,time;from pathlib import Path;Path(os.environ['RECAP_STARTED']).write_text(str(os.getpid()));time.sleep(60)"
        return [sys.executable,'-c',program],dict(os.environ)
codex_search_runtime.IsolatedCodex=Runtime
sys.argv=[str(Path(sys.argv[1])/'executable_codex-search'),'--recent','--pick','--summary-model','synthetic']
runpy.run_path(sys.argv[0],run_name='__main__')
'''
        env={**self.env,'RECAP_STARTED':str(started)}
        result=subprocess.run([sys.executable,'-c',code,str(fixture.ROOT/'scripts')],env=env,capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual((self.base/'pick.txt').read_text(),'index lock free during active inference')
        with self.assertRaises(ProcessLookupError):os.kill(int(started.read_text()),0)
        self.assertFalse(self.log.exists())
