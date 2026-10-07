"""Defining behavior: origin classification, safe playback and installed layout."""
import importlib.util
import importlib.machinery
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class OriginTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((ROOT / 'dot_config/kitty/notifications.py').exists(), 'Kitty callback not implemented')
        self.callback = load('sound_callback', ROOT / 'dot_config/kitty/notifications.py')
        self.window = SimpleNamespace(child=SimpleNamespace(foreground_processes=[{'pid': 123, 'cmdline': ['codex'], 'cwd': '/tmp'}]))
        self.boss = SimpleNamespace(window_id_map={7: self.window, 8: SimpleNamespace(child=SimpleNamespace(foreground_processes=[]))})
        self.kitty = patch.dict(sys.modules, {'kitty': SimpleNamespace(), 'kitty.fast_data_types': SimpleNamespace(get_boss=lambda: self.boss)})
        self.kitty.start()
        self.addCleanup(self.kitty.stop)

    def command(self, title):
        return SimpleNamespace(channel_id=7, application_name='', title=title, body='unchanged', actions=frozenset({'focus'}), only_when='unfocused', timeout=5000, identifier='abc')

    def test_completion_and_approval_only_change_appname(self):
        for title in ('Codex turn complete', 'Approval requested'):
            with self.subTest(title=title), patch.object(self.callback.os, 'readlink', return_value='/opt/codex/codex'):
                command = self.command(title)
                before = vars(command).copy()
                self.assertIs(self.callback.main(command), False)
                self.assertEqual(vars(command), {**before, 'application_name': 'codex-kitty'})

    def test_unrelated_text_and_arbitrary_codex_argument_do_not_match(self):
        for exe, argv in (('/usr/bin/bash', ['bash', 'codex']), ('/usr/bin/node', ['node', '/tmp/other.js', '/node_modules/@openai/codex/bin/codex.js']), ('/usr/bin/python3', ['python3', 'codex.py'])):
            self.window.child.foreground_processes[0]['cmdline'] = argv
            with self.subTest(exe=exe), patch.object(self.callback.os, 'readlink', return_value=exe):
                command = self.command('Codex approval requested')
                self.assertIs(self.callback.main(command), False)
                self.assertEqual(command.application_name, '')

    def test_origin_channel_is_used_instead_of_active_window(self):
        with patch.object(self.callback.os, 'readlink', return_value='/opt/codex/codex'):
            for channel in (0, 8, 99):
                command = self.command('Completion')
                command.channel_id = channel
                self.assertIs(self.callback.main(command), False)
                self.assertEqual(command.application_name, '')

    def test_process_exit_permission_and_api_errors_preserve_notification(self):
        for error in (FileNotFoundError(), PermissionError(), RuntimeError('API unavailable')):
            with patch.object(self.callback.os, 'readlink', side_effect=error):
                command = self.command('Complete')
                self.assertIs(self.callback.main(command), False)
                self.assertEqual(command.application_name, '')


class PlaybackTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((ROOT / 'scripts/executable_codex-notification-sound').exists(), 'Playback helper not implemented')
        self.helper = load('sound_helper', ROOT / 'scripts/executable_codex-notification-sound')
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.config = self.root / 'config'
        self.state = self.root / 'state'
        self.env = patch.dict(os.environ, {'XDG_CONFIG_HOME': str(self.config), 'XDG_STATE_HOME': str(self.state)}, clear=False)
        self.env.start()
        self.addCleanup(self.env.stop)
        self.clip = self.root / 'a clip; $(touch nope).mp3'
        self.clip.write_bytes(b'test fixture')
        self.setting = self.config / 'codex-notification-sound/sound.json'

    def configure(self):
        self.assertEqual(self.helper.main(['set', str(self.clip)]), 0)
        self.assertEqual(json.loads(self.setting.read_text()), {'path': str(self.clip)})

    def test_disabled_until_configured(self):
        with patch.object(self.helper.subprocess, 'run') as player:
            self.assertEqual(self.helper.main(['codex-kitty', 'Complete', '', '', 'NORMAL']), 0)
            player.assert_not_called()
        self.assertFalse(self.setting.exists())

    def test_notification_plays_once_as_safe_argv(self):
        self.configure()
        with patch.object(self.helper.shutil, 'which', return_value='/usr/bin/mpv'), patch.object(self.helper.subprocess, 'run', return_value=SimpleNamespace(returncode=0)) as player:
            self.assertEqual(self.helper.main(['codex-kitty', 'Approval; $(bad)', '', '', 'NORMAL']), 0)
            self.assertEqual(player.call_count, 1)
            args, kwargs = player.call_args
            self.assertEqual(args[0][-2:], ['--', str(self.clip)])
            self.assertEqual(args[0][0], '/usr/bin/mpv')
            self.assertIn('--no-config', args[0])
            self.assertFalse(kwargs.get('shell', False))

    def test_unrelated_app_never_plays(self):
        self.configure()
        with patch.object(self.helper.subprocess, 'run') as player:
            self.assertEqual(self.helper.main(['kitty', 'Codex approval', '', '', 'NORMAL']), 0)
            player.assert_not_called()

    def test_preview_reports_player_failure_but_popup_hook_succeeds(self):
        self.configure()
        with patch.object(self.helper.shutil, 'which', return_value='/usr/bin/mpv'), patch.object(self.helper.subprocess, 'run', return_value=SimpleNamespace(returncode=2)):
            self.assertEqual(self.helper.main(['preview']), 1)
            self.assertEqual(self.helper.main(['codex-kitty', 'Complete', '', '', 'NORMAL']), 0)
        self.assertIn('mpv', (self.state / 'codex-notification-sound/errors.log').read_text())

    def test_missing_clip_player_and_invalid_configuration_do_not_break_hook(self):
        for value in ('broken json', '[]', '{"path": false}', '{"path": "relative.mp3"}', '{"path": "/missing.mp3"}'):
            self.setting.parent.mkdir(parents=True, exist_ok=True)
            self.setting.write_text(value)
            with self.subTest(value=value), patch.object(self.helper.subprocess, 'run') as player:
                self.assertEqual(self.helper.main(['codex-kitty', 'Complete', '', '', 'NORMAL']), 0)
                player.assert_not_called()
        self.configure()
        with patch.object(self.helper.shutil, 'which', return_value=None):
            self.assertEqual(self.helper.main(['preview']), 1)
            self.assertEqual(self.helper.main(['codex-kitty', 'Complete', '', '', 'NORMAL']), 0)

    def test_player_spawn_and_timeout_errors_are_isolated(self):
        self.configure()
        for error in (OSError('spawn failed'), subprocess.TimeoutExpired('mpv', 60)):
            with patch.object(self.helper.shutil, 'which', return_value='/usr/bin/mpv'), patch.object(self.helper.subprocess, 'run', side_effect=error):
                self.assertEqual(self.helper.main(['codex-kitty', 'Complete', '', '', 'NORMAL']), 0)

    def test_disable_removes_only_setting(self):
        self.configure()
        self.assertEqual(self.helper.main(['disable']), 0)
        self.assertFalse(self.setting.exists())
        self.assertTrue(self.clip.is_file())

    def test_setting_is_local_private_and_invalid_set_preserves_it(self):
        self.configure()
        self.assertEqual(self.setting.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.helper.main(['set', str(self.root / 'missing.mp3')]), 1)
        self.assertEqual(json.loads(self.setting.read_text())['path'], str(self.clip))


class InstallationTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('chezmoi'), 'requires chezmoi')
    def test_real_chezmoi_install_in_empty_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / 'source'
            for relative in ('dot_config/kitty/notifications.py', 'dot_config/dunst/dunstrc', 'scripts/executable_codex-notification-sound', 'scripts/executable_codex-notification-activate'):
                self.assertTrue((ROOT / relative).exists(), f'Missing implementation: {relative}')
                target = source / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, target)
            dest = base / 'home'
            dest.mkdir()
            config = base / 'config.toml'
            config.write_text('')
            result = subprocess.run(['chezmoi', '--config', str(config), '--source', str(source), '--destination', str(dest), '--persistent-state', str(base / 'state'), 'apply'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            helper = dest / 'scripts/codex-notification-sound'
            self.assertTrue(os.access(helper, os.X_OK))
            self.assertTrue(os.access(dest / 'scripts/codex-notification-activate', os.X_OK))
            result = subprocess.run([str(helper), 'status'], env={**os.environ, 'XDG_CONFIG_HOME': str(dest / '.config')}, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('disabled', result.stdout)
            self.assertEqual((dest / '.config/kitty/notifications.py').read_bytes(), (ROOT / 'dot_config/kitty/notifications.py').read_bytes())


if __name__ == '__main__':
    unittest.main()
