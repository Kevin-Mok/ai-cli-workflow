"""Disposable progress/stream/log checks; no mounts or production backups."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_backup_pc import load_tool, fixture

HELPER=Path(__file__).resolve().parents[1]/'scripts/backup-pc-progress.py'


def load_progress():
    if not HELPER.is_file(): raise AssertionError('backup progress helper is missing')
    spec=importlib.util.spec_from_file_location('backup_progress',HELPER)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


class ProgressTests(unittest.TestCase):
    def setUp(self):
        self.p=load_progress()
        self.tmp=tempfile.TemporaryDirectory(prefix='backup-progress-test-')
        self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)
        self.root=self.base/'root';self.root.mkdir();fixture(self.root)
        self.b=load_tool()

    def session(self, clock=None):
        bundle=self.base/'bundle';bundle.mkdir(exist_ok=True)
        ui=self.p.Session(bundle,stream=io.StringIO(),clock=clock)
        self.addCleanup(ui.close)
        return ui

    def test_estimate_excludes_runtime_home_caches_and_literal_mounts(self):
        dynamic=['./mnt/unrelated[1]']
        before=self.p.estimate_root(self.root,self.b.EXCLUDES,dynamic)
        for name in ('tmp/big','home/alice/big','root/.cache/big','var/cache/apt/archives/big','mnt/unrelated[1]/big'):
            path=self.root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b'x'*2**20)
        self.assertEqual(self.p.estimate_root(self.root,self.b.EXCLUDES,dynamic),before)
        (self.root/'opt/app/keep').write_bytes(b'x'*2**20)
        self.assertGreater(self.p.estimate_root(self.root,self.b.EXCLUDES,dynamic),before+2**20)

    def test_estimate_counts_hardlink_data_once_and_sparse_extents(self):
        file=self.root/'opt/app/large';file.write_bytes(b'x'*2**20)
        before=self.p.estimate_root(self.root,self.b.EXCLUDES,[])
        os.link(file,file.with_name('hardlink'))
        with (self.root/'opt/app/sparse').open('wb') as stream:
            stream.seek(100*2**30);stream.write(b'end')
        after=self.p.estimate_root(self.root,self.b.EXCLUDES,[])
        self.assertLess(after-before,65536)

    def test_root_checkpoint_percentage_eta_and_finish_are_distinct(self):
        now=[0.0];ui=self.session(lambda:now[0]);ui.start('root',1024000)
        now[0]=20;ui.record('root','tar: BACKUP_PC_ROOT_RECORD=50','stderr')
        ui.render(force=True)
        text=ui.stream.getvalue()
        self.assertIn('Root',text);self.assertIn('50.0%',text);self.assertIn('ETA 00:00:20',text)
        now[0]=40;ui.record('root','tar: BACKUP_PC_ROOT_RECORD=100','stderr');ui.render(force=True)
        self.assertIn('99.0%',ui.stream.getvalue());self.assertNotIn('100.0%',ui.stream.getvalue())
        self.assertIn('finishing',ui.stream.getvalue())
        ui.finish('root');self.assertIn('100.0%',ui.stream.getvalue())

    def test_tty_bars_fit_normal_terminal_width_without_wrapped_stale_rows(self):
        import pty,termios,re
        master,slave=pty.openpty();termios.tcsetwinsize(slave,(24,80))
        self.addCleanup(os.close,master)
        stream=os.fdopen(slave,'w');self.addCleanup(stream.close)
        bundle=self.base/'tty';bundle.mkdir()
        now=[0.0];ui=self.p.Session(bundle,stream=stream,clock=lambda:now[0])
        self.addCleanup(ui.close)
        ui.start('root',1024000);now[0]=10
        ui.record('root','tar: BACKUP_PC_ROOT_RECORD=50','stderr')
        ui.record('root','./usr/share/'+('very-long-filename-'*12),'stdout')
        ui.render(force=True)
        data=os.read(master,8192).decode()
        rows=[re.sub(r'\x1b\[[0-9;]*[A-Za-z]','',row) for row in re.split(r'[\r\n]',data)]
        self.assertTrue(all(len(row)<=80 for row in rows),rows)
        self.assertIn('50.0%',data);self.assertIn('Home',data);self.assertIn('elapsed',data)

    def test_home_native_percentage_and_current_file_are_logged(self):
        now=[0.0];ui=self.session(lambda:now[0]);ui.start('home')
        now[0]=5;ui.record('home','BACKUP_PC_FILE:alice/file with spaces','stdout')
        ui.record('home','   800,000  40%  1.0MB/s  0:00:07 (xfr#1, to-chk=2/4)','stdout')
        ui.render(force=True)
        self.assertIn('40.0%',ui.stream.getvalue());self.assertIn('ETA 00:00:07',ui.stream.getvalue())
        log=ui.log_path.read_text();self.assertIn('alice/file with spaces',log)
        self.assertEqual(ui.log_path.stat().st_mode & 0o777,0o600)
        self.assertRegex(log,r'\d{4}-\d{2}-\d{2}T')

    def test_home_completion_record_elapsed_time_is_not_mislabeled_remaining(self):
        now=[0.0];ui=self.session(lambda:now[0]);ui.start('home')
        now[0]=10
        ui.record('home',' 1,000,000 25% 1.0MB/s 0:00:15 (xfr#1, to-chk=3/4)','stdout')
        ui.render(force=True)
        self.assertIn('ETA 00:00:30',ui.stream.getvalue())
        self.assertNotIn('ETA 00:00:15',ui.stream.getvalue())

    def test_stream_drains_both_pipes_and_keeps_progress_out_of_diagnostics(self):
        ui=self.session();ui.start('root',1024000)
        program="import sys;sys.stdout.write('./opt/app/file with spaces\\n'+('x'*100000)+'\\n');sys.stdout.flush();sys.stderr.write('tar: BACKUP_PC_ROOT_RECORD=50\\ntar: ./private: Warning: Cannot open: Permission denied\\n');sys.exit(2)"
        result=ui.command([sys.executable,'-c',program],'root',self.b.command_env())
        self.assertEqual(result.returncode,2)
        self.assertNotIn('BACKUP_PC_ROOT_RECORD',result.stderr)
        self.assertIn('Permission denied',result.stderr)
        self.assertIn('file with spaces',ui.log_path.read_text())
        self.assertNotIn('100.0%',ui.stream.getvalue())

    def test_streamed_diagnostics_still_reject_real_read_errors(self):
        ui=self.session();ui.start('root',100)
        self.b.ACTIVE_PROGRESS=ui
        self.addCleanup(setattr,self.b,'ACTIVE_PROGRESS',None)
        program="import sys;sys.stderr.write('tar: ./private: Warning: Cannot open: Permission denied\\n')"
        with self.assertRaises(self.b.BackupError):
            self.b.copy_command([sys.executable,'-c',program],live=True)
        self.assertIn('Permission denied',ui.log_path.read_text())
        self.assertNotIn('100.0%',ui.stream.getvalue())

    def test_interruption_terminates_and_reaps_only_created_process(self):
        ui=self.session();ui.start('root',100)
        processes=[];original=self.p.subprocess.Popen
        def spawn(*args,**kwargs):
            proc=original(*args,**kwargs);processes.append(proc);return proc
        with patch.object(self.p.subprocess,'Popen',side_effect=spawn),patch.object(ui,'render',side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                ui.command([sys.executable,'-c','import time; time.sleep(30)'],'root',self.b.command_env())
        self.assertEqual(len(processes),1);self.assertIsNotNone(processes[0].poll())
        self.assertIn('interrupted',ui.log_path.read_text().lower())

    def test_log_write_failure_still_terminates_and_reaps_copy_process(self):
        ui=self.session();ui.start('root',100)
        processes=[];original=self.p.subprocess.Popen
        def spawn(*args,**kwargs):
            proc=original(*args,**kwargs);processes.append(proc);return proc
        def cleanup():
            for proc in processes:
                if proc.poll() is None:
                    import signal
                    os.killpg(proc.pid,signal.SIGKILL);proc.wait()
        self.addCleanup(cleanup)
        program="import time; print('./file',flush=True); time.sleep(30)"
        with patch.object(self.p.subprocess,'Popen',side_effect=spawn),patch.object(ui,'log',side_effect=OSError('fixture disk full')):
            with self.assertRaises(OSError):ui.command([sys.executable,'-c',program],'root',self.b.command_env())
        self.assertIsNotNone(processes[0].poll())

    def test_selector_setup_failure_leaves_no_copy_running(self):
        ui=self.session();ui.start('root',100)
        processes=[];original=self.p.subprocess.Popen
        def spawn(*args,**kwargs):
            proc=original(*args,**kwargs);processes.append(proc);return proc
        def cleanup():
            import signal
            for proc in processes:
                if proc.poll() is None:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
                if proc.stdout:proc.stdout.close()
                if proc.stderr:proc.stderr.close()
        self.addCleanup(cleanup)
        with patch.object(self.p.subprocess,'Popen',side_effect=spawn),patch.object(self.p.selectors,'DefaultSelector',side_effect=OSError('fixture descriptor exhaustion')):
            with self.assertRaises(OSError):
                ui.command([sys.executable,'-c','import time; time.sleep(30)'],'root',self.b.command_env())
        self.assertTrue(all(proc.poll() is not None for proc in processes))

    def test_sigterm_stops_detached_copy_instead_of_leaving_it_running(self):
        import signal,time
        bundle=self.base/'signal-bundle';bundle.mkdir()
        pidfile=bundle/'child.pid'
        child="import os,time;from pathlib import Path;Path("+repr(str(pidfile))+").write_text(str(os.getpid()));time.sleep(30)"
        program=("import importlib.util;from pathlib import Path;import sys;"
                 "spec=importlib.util.spec_from_file_location('progress',"+repr(str(HELPER))+");"
                 "p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p);"
                 "ui=p.Session(Path("+repr(str(bundle))+"));ui.start('root',100);"
                 "ui.command([sys.executable,'-c',"+repr(child)+"],'root',dict(__import__('os').environ))")
        parent=subprocess.Popen([sys.executable,'-c',program],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        def cleanup():
            if parent.poll() is None:parent.kill();parent.wait()
            if pidfile.exists():
                try:os.killpg(int(pidfile.read_text()),signal.SIGKILL)
                except ProcessLookupError:pass
        self.addCleanup(cleanup)
        deadline=time.monotonic()+5
        while not pidfile.exists() and time.monotonic()<deadline:time.sleep(.02)
        self.assertTrue(pidfile.exists(),'disposable child failed to start')
        childpid=int(pidfile.read_text())
        parent.terminate();parent.wait(timeout=5)
        deadline=time.monotonic()+2
        def active():
            status=Path('/proc')/str(childpid)/'stat'
            return status.exists() and status.read_text().split()[2]!='Z'
        while active() and time.monotonic()<deadline:time.sleep(.02)
        self.assertFalse(active(),'copy survived parent SIGTERM')
        self.assertIn('interrupted',(bundle/'backup.log').read_text().lower())

    def test_resume_log_appends_existing_history(self):
        bundle=self.base/'append-log';bundle.mkdir()
        (bundle/'backup.log').write_text('old history\n')
        ui=self.p.Session(bundle,stream=io.StringIO(),append=True)
        ui.message('resumed');ui.close()
        log=(bundle/'backup.log').read_text()
        self.assertTrue(log.startswith('old history\n'))
        self.assertIn('resumed',log)

    def test_published_backup_is_not_misreported_incomplete_on_final_log_error(self):
        import types
        dest=self.base/'final-log-error'
        args=types.SimpleNamespace(source_root=str(self.root),destination=str(dest),dry_run=False,live=True)
        meta={'source_disks':[],'swap_bytes':0,'excludes':[],'consistency':'live-nonatomic'}
        original=self.p.Session.message
        def message(ui,text):
            if text.startswith('BACKUP COMPLETE:'):raise OSError('fixture final log failure')
            return original(ui,text)
        # Patch loader to provide the actual helper class with this reporting fault.
        original_module=self.b.importlib.util.module_from_spec
        def module(spec):
            result=original_module(spec)
            original_exec=spec.loader.exec_module
            def execute(target):
                original_exec(target)
                target.Session.message=message
            spec.loader.exec_module=execute
            return result
        with patch.object(self.b,'require_root'),patch.object(self.b,'require_tools'),patch.object(self.b,'source_preflight',return_value=meta),patch.object(self.b,'destination_preflight'),patch.object(self.b.importlib.util,'module_from_spec',side_effect=module),contextlib.redirect_stdout(io.StringIO()) as output,contextlib.redirect_stderr(io.StringIO()) as errors:
            with self.assertRaises(OSError):self.b.backup(args)
        bundle=next(dest.iterdir());self.b.verify_bundle(bundle/'system.tar.xz')
        self.assertNotIn('BACKUP INCOMPLETE',output.getvalue()+errors.getvalue())
        self.assertIn(str(bundle),errors.getvalue())

    def test_real_backup_publishes_log_and_checksummed_progress_helper(self):
        dest=self.base/'backups'
        import types
        args=types.SimpleNamespace(source_root=str(self.root),destination=str(dest),dry_run=True,live=True)
        meta={'source_disks':[],'swap_bytes':0,'excludes':[],'consistency':'live-nonatomic'}
        with patch.object(self.b,'require_root'),patch.object(self.b,'require_tools'),patch.object(self.b,'source_preflight',return_value=meta),patch.object(self.b,'destination_preflight'),contextlib.redirect_stdout(io.StringIO()) as output:
            self.b.backup(args);self.assertFalse(dest.exists())
            args.dry_run=False;self.b.backup(args)
        bundle=next(dest.iterdir());self.b.verify_bundle(bundle/'system.tar.xz')
        self.assertIn('Root',output.getvalue());self.assertIn('Home',output.getvalue())
        self.assertIn('backup-pc-progress.py',(bundle/'SHA256SUMS').read_text())
        log=(bundle/'backup.log').read_text();self.assertIn('BACKUP COMPLETE',log)
        self.assertIn('file with spaces',log);self.assertIn('Verifying',log)
        self.assertEqual((bundle/'backup.log').stat().st_mode & 0o777,0o600)
        result=subprocess.run(['bash',str(bundle/'backup-pc'),'backup','--help'],capture_output=True,text=True,cwd='/tmp')
        self.assertEqual(result.returncode,0,result.stderr)


if __name__=='__main__': unittest.main()
