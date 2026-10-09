"""Prompt recent-picker startup with invented archives only."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

import test_codex_search as fixture


class StartupCLITest(unittest.TestCase):
    setUp = fixture.CodexSearchTest.setUp
    stub = fixture.CodexSearchTest.stub
    session = fixture.CodexSearchTest.session
    run_cli = fixture.CodexSearchTest.run_cli
    manifest = fixture.CodexSearchTest.manifest

    def test_cold_picker_starts_before_slow_archive_extraction(self):
        source = self.session(name='old-archive.jsonl')
        with source.open('a') as output:
            output.write('{"unfinished":\n')
        release = self.base / 'release'
        self.stub('fzf', "import os,sys\nfrom pathlib import Path\nPath(os.environ['PICK_LOG']).write_text(sys.stdin.read())\nsys.exit(130)")
        program = '''import os,runpy,sys,time
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import codex_search_index as index
original=index.extract
def slow_extract(*args, **kwargs):
    end=time.monotonic()+5
    while not Path(os.environ['STARTUP_RELEASE']).exists() and time.monotonic()<end:time.sleep(.01)
    return original(*args, **kwargs)
index.extract=slow_extract
sys.argv=[str(Path(sys.argv[1])/'executable_codex-search'),'--recent','--pick','--no-summaries']
runpy.run_path(sys.argv[0],run_name='__main__')
'''
        process = subprocess.Popen([sys.executable, '-c', program, str(fixture.ROOT / 'scripts')],
                                   env={**self.env, 'STARTUP_RELEASE': str(release)},
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            deadline = time.monotonic() + 1.5
            while not (self.base / 'pick.txt').exists() and time.monotonic() < deadline:
                time.sleep(.01)
            opened = (self.base / 'pick.txt').exists()
        finally:
            release.touch()
            stdout, stderr = process.communicate(timeout=8)
        self.assertTrue(opened, 'fzf waited for full archive parsing: ' + stderr)
        self.assertEqual(process.returncode, 0, stderr + stdout)
        self.assertIn(fixture.ID1, (self.base / 'pick.txt').read_text())
        self.assertNotIn('malformed/incomplete', stderr)
        self.assertFalse(self.log.exists())

    def test_cached_picker_does_not_wait_for_another_indexer_lock(self):
        self.session()
        self.run_cli('--recent')
        manifest, _ = self.manifest()
        self.stub('fzf', "import os,sys\nfrom pathlib import Path\nPath(os.environ['PICK_LOG']).write_text(sys.stdin.read())\nsys.exit(130)")
        import fcntl
        with (manifest.parent / '.lock').open('r+') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            process = subprocess.Popen([sys.executable, str(fixture.SCRIPT), '--recent', '--pick', '--no-summaries'],
                                       env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                deadline = time.monotonic() + 1.5
                while not (self.base / 'pick.txt').exists() and time.monotonic() < deadline:
                    time.sleep(.01)
                opened = (self.base / 'pick.txt').exists()
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)
                stdout, stderr = process.communicate(timeout=8)
        self.assertTrue(opened, 'cached fzf waited behind an archive index lock: ' + stderr)
        self.assertEqual(process.returncode, 0, stderr + stdout)

    def test_pending_dialogue_preview_explains_indexing(self):
        sys.path.insert(0, str(fixture.ROOT / 'scripts'))
        from codex_search_recent import local_dialogue, render_session
        entry = {'id': fixture.ID1, 'cwd': str(self.project), 'timestamp': '2026-10-09T00:00:00Z',
                 'index_pending': True, 'dialogue': '', 'dialogue_hash': ''}
        status = {'status': 'indexing', 'recap': None, 'partial': False,
                  'detail': 'Indexing local dialogue; recap will be available shortly.'}
        row, preview = render_session(entry, 'Recent work', status, local_dialogue(self.base, entry))
        self.assertIn('[indexing]', row)
        self.assertIn('AI recap: indexing', preview)
        self.assertIn('Indexing local dialogue', preview)
        self.assertNotIn('unavailable', row)

    def test_picker_header_explains_background_work_without_rows(self):
        sys.path.insert(0, str(fixture.ROOT / 'scripts'))
        from codex_search_recent import picker_header
        header = picker_header('priority', 'Indexing local sessions: 0/100 sources ready.', plain=True)
        self.assertIn('AI priority', header)
        self.assertIn('Enter resume', header)
        self.assertIn('0/100 sources ready', header)
        self.assertTrue(header.isascii())

    def test_background_warnings_do_not_write_over_picker_terminal(self):
        source = self.session()
        with source.open('a') as output:
            output.write('{"unfinished":\n')
        program = '''import sys,time
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from codex_search_watch import SessionWatcher
root=Path(sys.argv[2]);root.mkdir(mode=0o700)
directory=Path(sys.argv[3]);directory.mkdir(mode=0o700)
watcher=SessionWatcher(root,Path(sys.argv[4]),directory,interval=.05)
try:
    watcher.start()
    end=time.monotonic()+3
    while watcher.read() is None and time.monotonic()<end:time.sleep(.02)
    assert watcher.read() is not None,'watcher did not publish usable rows'
    time.sleep(.15)
finally:watcher.close()
'''
        result = subprocess.run([sys.executable, '-c', program, str(fixture.ROOT / 'scripts'),
                                 str(self.base / 'watch-cache'), str(self.base / 'codex-search-picker-test'),
                                 str(self.home)], env=self.env, capture_output=True, text=True, timeout=8)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('malformed/incomplete', result.stderr)
        self.assertNotIn(str(source), result.stderr)

    def test_empty_picker_recovers_when_first_sessions_directory_appears(self):
        self.sessions.rmdir()
        self.env['TMPDIR'] = str(self.base)
        self.env['STARTUP_UUID'] = fixture.ID1
        self.stub('fzf', '''import json,os,sys,time
from pathlib import Path
Path(os.environ['PICK_LOG']).write_text(sys.stdin.read())
deadline=time.monotonic()+5
while time.monotonic()<deadline:
    for snapshot in Path(os.environ['TMPDIR']).glob('codex-search-picker-*/updates.json'):
        try: value=json.loads(snapshot.read_text())
        except (OSError,ValueError): continue
        if any(entry['id']==os.environ['STARTUP_UUID'] for entry in value['entries']): sys.exit(130)
    time.sleep(.02)
sys.exit(2)
''')
        process = subprocess.Popen([sys.executable, str(fixture.SCRIPT), '--recent', '--pick', '--no-summaries'],
                                   env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            deadline = time.monotonic() + 1.5
            while not (self.base / 'pick.txt').exists() and time.monotonic() < deadline:
                time.sleep(.01)
            self.assertTrue((self.base / 'pick.txt').exists(), 'empty picker did not open')
            self.session()
            stdout, stderr = process.communicate(timeout=8)
            self.assertEqual(process.returncode, 0, stderr + stdout)
            self.assertFalse(self.log.exists())
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate(timeout=3)

    def test_partial_archive_scan_preserves_unknown_cached_recaps(self):
        sys.path.insert(0, str(fixture.ROOT / 'scripts'))
        import codex_search_watch as watch_module
        source = self.session()
        entry = {'id': fixture.ID1, 'cwd': str(self.project), 'timestamp': '2026-10-09T00:00:00Z',
                 'index_pending': True, 'dialogue': '', 'dialogue_hash': ''}
        def partial_refresh(root, home, **kwargs):
            kwargs['stats'].update(total=2, pending=1, refreshed=1, skipped=0,
                                   sources=[str(source)], pending_sources=[str(source)])
            return {str(source): entry}
        with patch.object(watch_module, 'refresh', side_effect=partial_refresh), \
                patch.object(watch_module, 'maintain_cache') as maintenance, \
                patch.object(watch_module.time, 'sleep', side_effect=StopIteration):
            with self.assertRaises(StopIteration):
                watch_module.watch(self.cache / 'watch', self.home, self.base / 'picker', .05)
            maintenance.assert_not_called()


if __name__ == '__main__':
    unittest.main()
