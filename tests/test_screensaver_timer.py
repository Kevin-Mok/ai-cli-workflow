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
    def test_ten_second_test_wakes_then_previews_without_changing_timer(self):
        import runpy
        module = runpy.run_path(str(INSTALLER))
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            launcher = home / 'scripts/media-screensaver'
            launcher.parent.mkdir()
            launcher.write_text('#!/bin/sh\necho scheduled\n')
            launcher.chmod(0o755)
            events = []
            def execute(command, **kwargs):
                events.append(command)
                return subprocess.CompletedProcess(command, 0, 'scheduled', '')
            def pause(seconds):
                events.append(['sleep', seconds])
            with patch.dict(os.environ, dict(HOME=directory, XDG_CONFIG_HOME=directory+'/.config', DISPLAY=':99')), patch.object(subprocess, 'run', side_effect=execute), patch.object(subprocess, 'call', side_effect=lambda command: events.append(command) or 0), patch('time.sleep', side_effect=pause):
                self.assertEqual(module['main'](['--test', '--plain']), 0)
            self.assertEqual(events[1:], [
                ['xset', '+dpms'], ['xset', 'dpms', 'force', 'off'], ['sleep', 10],
                ['xset', 'dpms', 'force', 'on'], [str(launcher), 'preview', '--plain']])
            self.assertFalse((home / '.config/systemd/user').exists())
            events.clear()
            with patch.dict(os.environ, dict(HOME=directory, XDG_CONFIG_HOME=directory+'/.config', DISPLAY=':99')), patch.object(subprocess, 'run', side_effect=execute), patch.object(subprocess, 'call') as preview, patch('time.sleep', side_effect=KeyboardInterrupt):
                self.assertEqual(module['main'](['--test', '--plain']), 130)
                preview.assert_not_called()
            self.assertEqual(events[-1], ['xset', 'dpms', 'force', 'on'])

    def test_blackout_arms_wake_before_stopping_idle_and_powering_off(self):
        import runpy
        module = runpy.run_path(str(INSTALLER))
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            launcher = home / 'scripts/media-screensaver'
            launcher.parent.mkdir()
            launcher.write_text('#!/bin/sh\necho scheduled\n')
            launcher.chmod(0o755)
            calls = []
            def execute(command, **kwargs):
                calls.append(command)
                return subprocess.CompletedProcess(command, 0, 'scheduled', '')
            env = dict(HOME=directory, XDG_CONFIG_HOME=directory+'/.config', DISPLAY=':99')
            with patch.dict(os.environ, env), patch.object(subprocess, 'run', side_effect=execute):
                self.assertEqual(module['main'](['--black-until-10', '--plain']), 0)
            self.assertEqual(calls[-4:], [
                ['systemctl', '--user', 'enable', '--now', 'media-screensaver-daily.timer'],
                ['systemctl', '--user', 'stop', 'media-screensaver.service', 'media-screensaver-daily.service'],
                ['xset', '+dpms'], ['xset', 'dpms', 'force', 'off']])
            service = (home / '.config/systemd/user/media-screensaver-daily.service').read_text()
            self.assertIn('ExecStartPre=/usr/bin/xset dpms force on', service)
            self.assertIn('ExecStartPre=/usr/bin/systemctl --user start media-screensaver.service', service)

    def test_failed_timer_setup_never_powers_off(self):
        import runpy
        module = runpy.run_path(str(INSTALLER))
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            launcher = home / 'scripts/media-screensaver'
            launcher.parent.mkdir()
            launcher.write_text('#!/bin/sh\necho scheduled\n')
            launcher.chmod(0o755)
            calls = []
            def execute(command, **kwargs):
                calls.append(command)
                return subprocess.CompletedProcess(command, int(command[0] == 'systemctl'), 'scheduled', '')
            with patch.dict(os.environ, dict(HOME=directory, XDG_CONFIG_HOME=directory+'/.config', DISPLAY=':99')), patch.object(subprocess, 'run', side_effect=execute):
                self.assertEqual(module['main'](['--black-until-10', '--plain']), 1)
            self.assertFalse(any(command[0] == 'xset' for command in calls))

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

    def test_scheduled_skips_locked_session_and_uses_explicit_preview(self):
        with patch.object(main, 'locked', return_value=True), patch.object(main, 'preview') as preview:
            self.assertEqual(main.main(['scheduled', '--plain']), 0)
            preview.assert_not_called()
        with patch.object(main, 'locked', return_value=False), patch.object(main, 'preview', return_value=0) as preview:
            self.assertEqual(main.main(['scheduled', '--plain']), 0)
            self.assertFalse(preview.call_args.kwargs.get('automatic', False))

    def test_scheduled_stays_awake_during_playback_and_releases_on_error(self):
        from types import SimpleNamespace
        from unittest.mock import MagicMock
        from media_screensaver import desktop, renderer
        args = SimpleNamespace(command='scheduled', report=None, seconds=0, plain=True, details=False)
        awake = MagicMock()
        with tempfile.TemporaryDirectory() as directory, patch.object(main, 'scan', return_value=[]), patch.object(main, 'monitors', return_value=[{}, {}]), patch.object(main.bridge, 'runtime_dir', return_value=Path(directory)), patch.object(desktop, 'keep_awake', return_value=awake, create=True), patch.object(renderer, 'run', side_effect=RuntimeError('decoder failed')) as run:
            def playback(*args, **kwargs):
                awake.__enter__.assert_called_once()
                self.assertFalse(kwargs['automatic'])
                raise RuntimeError('decoder failed')
            run.side_effect = playback
            with self.assertRaisesRegex(RuntimeError, 'decoder failed'):
                main._preview(args)
        awake.__exit__.assert_called_once()


if __name__ == '__main__':
    unittest.main()
