"""Wrapper contracts and optional real-Dust accounting on disposable trees."""
import json
import importlib.util
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/executable_directory-sizes'


class DirectorySizesTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='directory-sizes-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.target = self.base / "- odd ' ; directory\nname"
        self.target.mkdir()
        self.backend = self.base / 'dust'
        self.backend.write_text('''#!/usr/bin/python3
import os, sys, time, json
from pathlib import Path
Path(os.environ['CALL_LOG']).write_text(json.dumps({'args':sys.argv[1:],'cwd':os.getcwd()}))
mode=os.environ.get('STUB_MODE','ok')
if mode=='slow':
 Path(os.environ['PID_LOG']).write_text(str(os.getpid()))
 print('\\rIndexing: . 17 files, 4K ... -', file=sys.stderr, flush=True, end='')
 time.sleep(30)
if mode=='error':
 print('Did not have permissions for directory secret',file=sys.stderr)
print(json.dumps({'size':'4096B','name':'.','children':[{'size':'0B','name':'./line\\nname','children':[]}]}))
if mode=='nonzero': sys.exit(3)
''')
        self.backend.chmod(0o755)
        self.env = {**os.environ, 'CALL_LOG':str(self.base/'calls.json'),
                    'PID_LOG':str(self.base/'pid')}

    def run_script(self, *args, mode='ok'):
        return subprocess.run([sys.executable, str(SCRIPT), '--backend', str(self.backend),
                               *args], env={**self.env,'STUB_MODE':mode}, capture_output=True,
                              text=True, timeout=5)

    def test_executable_exists(self):
        self.assertTrue(SCRIPT.is_file(), 'directory-sizes implementation is absent')

    def test_safe_path_and_single_scan(self):
        p = self.run_script('--depth','2','--',str(self.target))
        self.assertEqual(p.returncode,0,p.stderr)
        call=json.loads((self.base/'calls.json').read_text())
        self.assertEqual(call['cwd'],str(self.target))
        self.assertEqual(call['args'][-2:],['--','.'])
        self.assertIn('--print-errors',call['args'])
        self.assertNotIn('--dereference-links',call['args'])
        self.assertNotIn('--apparent-size',call['args'])
        self.assertIn('4.00 KiB',p.stdout)

    def test_readable_paths_escape_newlines(self):
        p=self.run_script(str(self.target))
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn("'./line\\nname'",p.stdout)
        self.assertEqual(len(p.stdout.splitlines()),2)

    def test_depth_zero_and_logical_mode(self):
        p=self.run_script('--depth','0','--apparent-size',str(self.target))
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn('logical',p.stderr.lower())
        args=json.loads((self.base/'calls.json').read_text())['args']
        self.assertIn('--apparent-size',args)
        self.assertEqual(args[args.index('--depth')+1],'0')

    def test_invalid_inputs_and_missing_dependency(self):
        for args in [('--depth','-1'),('--threads','0'),('--depth','x'),(str(self.base/'missing'),)]:
            p=self.run_script(*args)
            self.assertNotEqual(p.returncode,0)
            self.assertEqual(p.stdout,'')
        p=subprocess.run([sys.executable,str(SCRIPT),'--backend',str(self.base/'missing'),str(self.target)],capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0)
        self.assertIn('setup-directory-sizes',p.stderr)

    def test_incomplete_scans_never_publish_totals(self):
        for mode in ['error','nonzero']:
            p=self.run_script(str(self.target),mode=mode)
            self.assertNotEqual(p.returncode,0)
            self.assertEqual(p.stdout,'')
            self.assertIn('incomplete',p.stderr.lower())

    def test_interruption_reaps_backend_and_preserves_progress(self):
        p=subprocess.Popen([sys.executable,str(SCRIPT),'--backend',str(self.backend),str(self.target)],env={**self.env,'STUB_MODE':'slow'},stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        try:
            limit=time.monotonic()+3
            while not (self.base/'pid').exists() and time.monotonic()<limit:
                time.sleep(.02)
            self.assertTrue((self.base/'pid').exists())
            time.sleep(.2)
            p.send_signal(signal.SIGINT)
            out,err=p.communicate(timeout=3)
            self.assertEqual(out,'')
            self.assertEqual(p.returncode,130)
            self.assertIn('17 files',err)
            pid=int((self.base/'pid').read_text())
            with self.assertRaises(ProcessLookupError): os.kill(pid,0)
        finally:
            if p.poll() is None: p.kill(); p.wait()

    def test_benchmark_interruption_reaps_separate_backend_session(self):
        spec=importlib.util.spec_from_file_location('benchmark',ROOT/'tests/scripts/directory_sizes_benchmark.py')
        benchmark=importlib.util.module_from_spec(spec);spec.loader.exec_module(benchmark)
        previous=dict(os.environ)
        os.environ.update(self.env);os.environ['STUB_MODE']='slow'
        def interrupt(signum, frame): raise KeyboardInterrupt
        old=signal.signal(signal.SIGALRM,interrupt)
        started=time.monotonic()
        signal.setitimer(signal.ITIMER_REAL,.4)
        try:
            with self.assertRaises(KeyboardInterrupt):
                benchmark.probe([sys.executable,str(SCRIPT),'--backend',str(self.backend),str(self.target)])
            self.assertLess(time.monotonic()-started,3)
            pid=int((self.base/'pid').read_text())
            with self.assertRaises(ProcessLookupError):os.kill(pid,0)
        finally:
            signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old)
            if (self.base/'pid').exists():
                try:os.kill(int((self.base/'pid').read_text()),signal.SIGTERM)
                except ProcessLookupError:pass
            os.environ.clear();os.environ.update(previous)

    @unittest.skipUnless(os.environ.get('DIRECTORY_SIZES_REAL_BACKEND'), 'set DIRECTORY_SIZES_REAL_BACKEND for real accounting')
    def test_real_backend_matches_du_with_nested_sparse_links_and_empty(self):
        backend=os.environ['DIRECTORY_SIZES_REAL_BACKEND']
        (self.target/'nested').mkdir(); (self.target/'empty').mkdir()
        (self.target/'nested'/'ordinary').write_bytes(b'x'*12000)
        with (self.target/'sparse').open('wb') as f: f.truncate(32*1024*1024)
        os.link(self.target/'nested'/'ordinary',self.target/'hardlink')
        os.symlink('nested',self.target/'symlink')
        os.symlink('/does/not/exist',self.target/'broken')
        for logical in [False,True]:
            args=[sys.executable,str(SCRIPT),'--backend',backend,'--depth','3','--json']
            du=['du','--block-size=1','--summarize']
            if logical: args+=['--apparent-size']; du+=['--apparent-size','--count-links']
            p=subprocess.run(args+['--',str(self.target)],capture_output=True,text=True,timeout=10)
            self.assertEqual(p.returncode,0,p.stderr)
            data=json.loads(p.stdout)
            actual=int(data['size'].removesuffix('B'))
            expected=int(subprocess.check_output(du+['--',str(self.target)]).split(b'\t')[0])
            if logical:
                # Dust includes directory st_size; GNU du apparent mode omits it.
                expected += sum(d.stat().st_size for d in [self.target, self.target/'nested', self.target/'empty'])
            self.assertEqual(actual,expected)
            names={Path(c['name']).name for c in data['children']}
            self.assertTrue({'nested','empty'}<=names)
        # Followed symlinks would count data outside this tree; test unchanged metadata.
        self.assertTrue((self.target/'symlink').is_symlink())


if __name__=='__main__': unittest.main()
