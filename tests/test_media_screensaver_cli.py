#!/usr/bin/env python3
"""Install into a disposable home and exercise the installed entrypoint."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'scripts/executable_media-screensaver'

class CLITests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CLI.exists(), 'media-screensaver launcher is not implemented')

    def test_help_plain_and_missing_mount_are_actionable(self):
        p = subprocess.run([str(CLI), '--plain', '--help'], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('preview', p.stdout)
        p = subprocess.run([str(CLI), 'preview', '--plain', '--media', '/nonexistent/synthetic-media'], capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertIn('unavailable', p.stderr)
        self.assertIn('--media', p.stderr)
        self.assertTrue(p.stderr.isascii())

    def test_browser_gate_accepts_live_monitor_name_metadata(self):
        import sys
        import time
        sys.path.insert(0, str(ROOT / 'scripts'))
        from media_screensaver.main import gate
        with tempfile.TemporaryDirectory() as directory:
            snapshot = dict(version=1, healthy=True, windows=[dict(id=1, state='normal',
                bounds=dict(x=2048,y=0,width=3840,height=2160),
                videos=[dict(playing=True,rect=dict(x=2100,y=100,width=640,height=360))])])
            path = Path(directory) / 'bridge-123.json'
            path.write_text(json.dumps(dict(updated=time.time(),state=snapshot)))
            path.chmod(0o600)
            from unittest.mock import patch
            with patch('media_screensaver.desktop.browser_windows', return_value=[dict(snapshot['windows'][0]['bounds'],visible=True)]):
                allowed, reason = gate(Path(directory),dict(name='DP-2',x=2048,y=0,width=3840,height=2160))
            self.assertFalse(allowed)
            self.assertTrue(reason.startswith('playing video'), reason)

    def test_excessively_nested_bridge_state_suppresses_instead_of_crashing(self):
        import sys
        sys.path.insert(0, str(ROOT / 'scripts'))
        from media_screensaver import bridge
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bridge-123.json'
            path.write_text('[' * 10000 + '0' + ']' * 10000)
            path.chmod(0o600)
            previous = sys.getrecursionlimit()
            try:
                sys.setrecursionlimit(1000)
                allowed, reason = bridge.read_gate(Path(directory),dict(x=2048,y=0,width=3840,height=2160))
                self.assertFalse(allowed)
                self.assertTrue(reason)
            finally:
                sys.setrecursionlimit(previous)

    def test_daemon_waits_for_300_idle_seconds_and_reaps_owned_preview(self):
        import signal
        import sys
        from types import SimpleNamespace
        from unittest.mock import patch
        sys.path.insert(0,str(ROOT/'scripts'))
        from media_screensaver import main, renderer
        class Clock:
            last = None
            values = iter((299.9,300.0))
            def seconds(self): self.last = next(self.values); return self.last
            def close(self): pass
        class Stop:
            count = 0
            def is_set(self): return self.count >= 2
            def set(self): self.count = 2
            def wait(self,seconds): self.count += 1
        clock,stop = Clock(),Stop()
        launches = []
        original_popen = subprocess.Popen
        def launch(*args,**kwargs):
            process = original_popen([sys.executable,'-c','import time; time.sleep(60)'],start_new_session=True)
            launches.append((clock.last,process))
            return process
        previous = {sig: signal.getsignal(sig) for sig in (signal.SIGINT,signal.SIGTERM)}
        try:
            with tempfile.TemporaryDirectory() as directory, patch.object(main.bridge,'runtime_dir',return_value=Path(directory)), patch.object(renderer,'IdleClock',return_value=clock), patch.object(main.threading,'Event',return_value=stop), patch.object(main,'monitors',return_value=[{},dict(x=2048,y=0,width=3840,height=2160),{}]), patch.object(main,'gate',return_value=(True,'ready')), patch.object(main,'locked',return_value=False), patch.object(main.subprocess,'Popen',side_effect=launch):
                self.assertEqual(main.daemon(SimpleNamespace(media=Path(directory),plain=True,details=False)),0)
            self.assertEqual([idle for idle,_ in launches],[300.0])
            self.assertTrue(all(process.poll() is not None for _,process in launches))
        finally:
            for sig,handler in previous.items(): signal.signal(sig,handler)
            for _,process in launches:
                if process.poll() is None: process.kill(); process.wait()

    def test_service_imports_desktop_environment_before_start(self):
        import sys
        sys.path.insert(0, str(ROOT / 'scripts'))
        from media_screensaver import main
        from unittest.mock import patch
        calls = []
        def execute(command, **kwargs):
            calls.append(command)
            return subprocess.CompletedProcess(command, 0)
        with patch.dict(os.environ, DISPLAY=':99', XAUTHORITY='/tmp/test-auth', XDG_SESSION_ID='test'), patch.object(main.subprocess, 'run', side_effect=execute):
            self.assertEqual(main.main(['service', '--plain']), 0)
        self.assertEqual(calls, [
            ['systemctl', '--user', 'daemon-reload'],
            ['systemctl', '--user', 'import-environment', 'DISPLAY', 'XAUTHORITY', 'XDG_SESSION_ID'],
            ['systemctl', '--user', 'start', 'media-screensaver.service']])

    def test_install_and_native_manifest_use_stable_absolute_entrypoints(self):
        with tempfile.TemporaryDirectory() as directory:
            env = dict(os.environ, HOME=directory, XDG_CONFIG_HOME=directory + '/.config')
            i3 = Path(directory) / '.config/i3/config'
            i3.parent.mkdir(parents=True)
            i3.write_text('# existing lock and display settings\n' + f'exec --no-startup-id {directory}/scripts/media-screensaver daemon\n')
            p = subprocess.run([str(CLI), 'install', '--plain'], env=env, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            installed = Path(directory) / 'scripts/media-screensaver'
            self.assertTrue(installed.is_file())
            p = subprocess.run([str(installed), '--help'], env=env, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            for browser in ('google-chrome', 'chromium'):
                m = json.loads((Path(directory) / '.config' / browser / 'NativeMessagingHosts/org.kevin.media_screensaver.json').read_text())
                self.assertTrue(Path(m['path']).is_absolute())
                self.assertTrue(os.access(m['path'], os.X_OK))
                self.assertEqual(len(m['allowed_origins']), 1)
                self.assertTrue(m['allowed_origins'][0].startswith('chrome-extension://'))
            # Reinstall is safe and leaves unrelated package-directory files alone.
            unrelated = installed.parent / 'media_screensaver/local-note.txt'
            unrelated.write_text('keep')
            p = subprocess.run([str(CLI), 'install', '--plain'], env=env, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(unrelated.read_text(), 'keep')
            self.assertTrue(i3.read_text().startswith('# existing lock and display settings\n'))
            self.assertEqual(i3.read_text().count(str(installed) + ' service'), 1)
            self.assertNotIn(str(installed) + ' daemon', i3.read_text())
            unit = Path(directory) / '.config/systemd/user/media-screensaver.service'
            self.assertTrue(unit.is_file(), 'supervised idle service must be installed')
            self.assertIn('Restart=always', unit.read_text())
            self.assertIn('ExecStart=%h/scripts/media-screensaver daemon', unit.read_text())

if __name__ == '__main__': unittest.main()
