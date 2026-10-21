"""Exercise the timer installer without changing the real user manager."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / 'scripts/executable_setup-screensaver-timer'
sys.path.insert(0, str(ROOT / 'scripts'))
from media_screensaver import main


class TimerTests(unittest.TestCase):
    def test_install_repeat_and_disable(self):
        self.assertTrue(INSTALLER.exists(), 'daily timer installer is missing')
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            (home / 'scripts').mkdir()
            launcher = home / 'scripts/media-screensaver'
            launcher.write_text('#!/bin/sh\necho scheduled\n')
            launcher.chmod(0o755)
            calls = []
            def execute(command, **kwargs):
                calls.append(command)
                if command == [str(launcher), '--plain', '--help']:
                    return subprocess.CompletedProcess(command, 0, 'scheduled', '')
                self.assertEqual(command[:2], ['systemctl', '--user'])
                self.assertIn(command[2:], [
                    ['daemon-reload'], ['import-environment', 'DISPLAY', 'XAUTHORITY', 'XDG_SESSION_ID'],
                    ['enable', '--now', 'media-screensaver-daily.timer'],
                    ['disable', '--now', 'media-screensaver-daily.timer']])
                return subprocess.CompletedProcess(command, 0, '', '')
            import runpy
            module = runpy.run_path(str(INSTALLER))
            env = dict(HOME=directory, XDG_CONFIG_HOME=directory+'/.config', DISPLAY=':99',
                       XAUTHORITY='/tmp/auth', XDG_SESSION_ID='example')
            with patch.dict(os.environ, env), patch.object(subprocess, 'run', side_effect=execute):
                for _ in range(2):
                    self.assertEqual(module['main'](['--plain']), 0)
                units = home / '.config/systemd/user'
                timer = (units / 'media-screensaver-daily.timer').read_text()
                service = (units / 'media-screensaver-daily.service').read_text()
                self.assertIn('OnCalendar=*-*-* 10:00:00', timer)
                self.assertIn('Persistent=false', timer)
                self.assertIn('ExecStart=%h/scripts/media-screensaver scheduled', service)
                self.assertNotIn('Restart=always', service)
                self.assertEqual(module['main'](['--disable', '--plain']), 0)
            self.assertEqual(calls[-1][2:], ['disable', '--now', 'media-screensaver-daily.timer'])

    def test_missing_or_old_launcher_and_missing_display_do_not_install(self):
        import runpy
        module = runpy.run_path(str(INSTALLER))
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            env = dict(HOME=directory, XDG_CONFIG_HOME=directory+'/.config', DISPLAY='')
            with patch.dict(os.environ, env):
                self.assertEqual(module['main'](['--plain']), 1)
                launcher = home / 'scripts/media-screensaver'
                launcher.parent.mkdir()
                launcher.write_text('#!/bin/sh\necho preview\n')
                launcher.chmod(0o755)
                self.assertEqual(module['main'](['--plain']), 1)
                launcher.write_text('#!/bin/sh\necho scheduled\n')
                self.assertEqual(module['main'](['--plain']), 1)
                self.assertFalse((home / '.config/systemd/user').exists())

    def test_active_preview_prevents_duplicate_daily_or_idle_playback(self):
        import fcntl
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as directory:
            lock = Path(directory) / 'preview.lock'
            with lock.open('a') as held:
                fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
                with patch.object(main.bridge, 'runtime_dir', return_value=Path(directory)), patch.object(main, 'scan', side_effect=AssertionError('duplicate playback started')):
                    self.assertEqual(main.preview(SimpleNamespace(plain=True, details=False)), 0)

    def test_scheduled_skips_locked_session_and_keeps_automatic_gate(self):
        with patch.object(main, 'locked', return_value=True), patch.object(main, 'preview') as preview:
            self.assertEqual(main.main(['scheduled', '--plain']), 0)
            preview.assert_not_called()
        with patch.object(main, 'locked', return_value=False), patch.object(main, 'preview', return_value=0) as preview:
            self.assertEqual(main.main(['scheduled', '--plain']), 0)
            self.assertTrue(preview.call_args.kwargs['automatic'])


if __name__ == '__main__':
    unittest.main()
