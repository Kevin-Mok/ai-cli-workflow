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
import textwrap
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


class DeploymentTests(unittest.TestCase):
    def test_completion_callback_is_deployed_without_permission_audio_hook(self):
        import tomllib
        config = tomllib.loads((ROOT / 'dot_codex/config.toml').read_text())
        self.assertEqual(config.get('notify'), ['python3', '/home/example/scripts/codex-notification-event'])
        path = ROOT / 'dot_codex/hooks.json'
        self.assertTrue(path.exists(), 'Permission hook missing')
        hooks = json.loads(path.read_text())['hooks']
        self.assertNotIn('PermissionRequest', hooks)


class InstallationTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('chezmoi'), 'requires chezmoi')
    def test_real_chezmoi_install_in_empty_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / 'source'
            for relative in ('dot_config/kitty/notifications.py', 'dot_config/dunst/dunstrc', 'scripts/executable_codex-notification-sound', 'scripts/executable_codex-notification-activate', 'scripts/executable_codex-notification-event', 'scripts/executable_setup-codex-notification-speech', 'dot_codex/hooks.json'):
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
            self.assertTrue(os.access(dest / 'scripts/codex-notification-event', os.X_OK))
            self.assertTrue(os.access(dest / 'scripts/setup-codex-notification-speech', os.X_OK))
            self.assertTrue((dest / '.codex/hooks.json').exists())
            result = subprocess.run([str(helper), 'status'], env={**os.environ, 'XDG_CONFIG_HOME': str(dest / '.config')}, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('disabled', result.stdout)
            self.assertEqual((dest / '.config/kitty/notifications.py').read_bytes(), (ROOT / 'dot_config/kitty/notifications.py').read_bytes())


class SpeechTests(PlaybackTests):
    def enable(self):
        self.configure()
        self.assertEqual(self.helper.main(['speech', 'enable']), 0)

    def speech_only_preview(self, title=None):
        arguments = ['preview', '--speech-only', '--plain', '--details']
        if title is not None:
            arguments.extend(['--title', title])
        try:
            return self.helper.main(arguments)
        except SystemExit as error:
            return error.code  # Preserve the CLI exit status for RED parsing.

    def test_speech_only_ignores_absent_or_invalid_clip_settings(self):
        title = f'Hi, I am Voice Contributor! café $(touch {self.root / "nope"})'
        for configuration in (None, 'not json', '{"path":"/missing.mp3"}'):
            with self.subTest(configuration=configuration):
                self.setting.parent.mkdir(parents=True, exist_ok=True)
                if configuration is None:
                    self.setting.unlink(missing_ok=True)
                else:
                    self.setting.write_text(configuration)
                (self.root / 'events').unlink(missing_ok=True)
                env, player, ready, voice = self.speech_fixture(synthesis='immediate')
                with env, player, ready, voice:
                    self.assertEqual(self.speech_only_preview(title), 0)
                events = (self.root / 'events').read_text().splitlines()
                self.assertEqual(events, ['synthesis start', 'synthesis end', 'title '+title])
                args = json.loads((self.root / 'synthesis.args').read_text())
                self.assertEqual(args[args.index('--length-scale')+1], '0.95')
                self.assertFalse(Path((self.root / 'wav-path').read_text()).exists())
                self.assertFalse((self.root / 'nope').exists())

    def test_speech_only_rejects_missing_or_blank_title_before_children(self):
        import contextlib
        import io
        for title in (None, '', ' \t\n '):
            with self.subTest(title=title), contextlib.redirect_stderr(io.StringIO()) as errors:
                self.assertEqual(self.speech_only_preview(title), 1)
                self.assertIn('nonblank --title', errors.getvalue())
                self.assertFalse((self.state / 'codex-notification-sound/playback.lock').exists())

    def test_speech_only_unavailable_voice_fails_without_playing_clip(self):
        self.configure()
        env, player, ready, voice = self.speech_fixture(synthesis='immediate')
        with env, player, ready, voice, patch.object(self.helper, 'voice_ready', return_value=False):
            self.assertEqual(self.speech_only_preview('Voice Contributor says hello'), 1)
        self.assertFalse((self.root / 'events').exists())
        self.assertIn('--install', (self.state / 'codex-notification-sound/errors.log').read_text())

    def test_speech_only_failed_or_empty_synthesis_returns_error_without_clip(self):
        for mode in ('failed', 'empty'):
            with self.subTest(mode=mode):
                (self.root / 'events').unlink(missing_ok=True)
                env, player, ready, voice = self.speech_fixture(synthesis=mode)
                with env, player, ready, voice:
                    self.assertEqual(self.speech_only_preview('Voice Contributor says hello'), 1)
                events = (self.root / 'events').read_text().splitlines()
                self.assertEqual(events.count('synthesis start'), 1)
                self.assertNotIn('clip start', events)
                self.assertNotIn('title Voice Contributor says hello', events)
                pid = int((self.root / 'synthesis.pid').read_text())
                with self.assertRaises(ProcessLookupError):
                    os.kill(pid, 0)

    def test_speech_only_timeout_kills_and_reaps_child(self):
        env, player, ready, voice = self.speech_fixture(synthesis='blocked')
        with env, player, ready, voice, patch.object(self.helper, 'SYNTHESIS_TIMEOUT', .2):
            self.assertEqual(self.speech_only_preview('Voice Contributor says hello'), 1)
        events = (self.root / 'events').read_text().splitlines()
        self.assertNotIn('clip start', events)
        self.assertNotIn('title Voice Contributor says hello', events)
        pid = int((self.root / 'synthesis.pid').read_text())
        with self.assertRaises(ProcessLookupError):
            os.kill(pid, 0)
        self.assertIn('timed out', (self.state / 'codex-notification-sound/errors.log').read_text())

    def test_speech_only_synthesis_start_failure_reports_error(self):
        env, player, ready, voice = self.speech_fixture(synthesis='immediate')
        with env, player, ready, voice, patch.object(self.helper, 'voice_paths', return_value=(self.root / 'missing-python', self.root / 'voice.onnx')):
            self.assertEqual(self.speech_only_preview('Voice Contributor says hello'), 1)
        self.assertFalse((self.root / 'events').exists())
        self.assertIn('missing-python', (self.state / 'codex-notification-sound/errors.log').read_text())

    def test_speech_only_playback_failure_reports_error_and_cleans_wav(self):
        env, player, ready, voice = self.speech_fixture(synthesis='speech-playback-failed')
        with env, player, ready, voice:
            self.assertEqual(self.speech_only_preview('Voice Contributor says hello'), 1)
        self.assertEqual((self.root / 'events').read_text().splitlines(), ['synthesis start', 'synthesis end', 'title Voice Contributor says hello'])
        self.assertFalse(Path((self.root / 'wav-path').read_text()).exists())
        self.assertIn('mpv playback failed', (self.state / 'codex-notification-sound/errors.log').read_text())

    def test_speech_only_waits_for_shared_playback_lock(self):
        import fcntl
        import time
        env, _player, _ready, _voice = self.speech_fixture(synthesis='immediate')
        data = self.root / 'data'
        python = data / 'codex-notification-speech/venv/bin/python'
        python.parent.mkdir(parents=True)
        shutil.copy2(self.root / 'piper-python', python)
        model = data / 'codex-notification-speech/voices/en_US-Voice Contributor-high.onnx'
        model.parent.mkdir()
        model.write_bytes(b'fixture')
        model.with_suffix('.onnx.json').write_text('{}')
        lock = self.state / 'codex-notification-sound/playback.lock'
        lock.parent.mkdir(parents=True)
        with env, patch.dict(os.environ, {'XDG_DATA_HOME': str(data), 'PATH': str(self.root)+':'+os.environ['PATH']}), lock.open('a') as owner:
            fcntl.flock(owner, fcntl.LOCK_EX)
            worker = subprocess.Popen([sys.executable, str(ROOT / 'scripts/executable_codex-notification-sound'), 'preview', '--speech-only', '--title', 'Voice Contributor says hello'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                deadline = time.monotonic()+.3
                while not (self.root / 'events').exists() and time.monotonic()<deadline:
                    time.sleep(.01)
                self.assertFalse((self.root / 'events').exists())
                self.assertIsNone(worker.poll())
                fcntl.flock(owner, fcntl.LOCK_UN)
                stdout, stderr = worker.communicate(timeout=5)
                self.assertEqual(worker.returncode, 0, stdout+stderr)
            finally:
                if worker.poll() is None:
                    worker.kill()
                worker.communicate()
        self.assertEqual((self.root / 'events').read_text().splitlines(), ['synthesis start', 'synthesis end', 'title Voice Contributor says hello'])

    def test_selected_voice_is_Voice Contributor_high(self):
        with patch.dict(os.environ, {'XDG_DATA_HOME': str(self.root / 'data')}):
            python, model = self.helper.voice_paths()
        self.assertEqual(model.name, 'en_US-Voice Contributor-high.onnx')
        self.assertEqual(python.name, 'python')

    def test_selected_voice_uses_celebrate_audition_pace(self):
        self.configure()
        env, player, ready, voice = self.speech_fixture()
        with env, player, ready, voice:
            self.assertEqual(self.helper.main(['preview', '--title', 'All done! Take a look at what I built.']), 0)
        args = json.loads((self.root / 'synthesis.args').read_text())
        self.assertIn('--length-scale', args)
        self.assertEqual(args[args.index('--length-scale') + 1], '0.95')

    def test_status_names_selected_voice_and_pace(self):
        import contextlib
        import io
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(self.helper.main(['status', '--plain']), 0)
        self.assertIn('Voice Contributor', output.getvalue())
        self.assertIn('0.95', output.getvalue())

    def test_speech_switch_preserves_clip_and_suppresses_dunst(self):
        self.enable()
        with patch.object(self.helper.subprocess, 'run') as player:
            self.assertEqual(self.helper.main(['codex-kitty', 'Complete', '', '', 'NORMAL']), 0)
            player.assert_not_called()
        self.assertEqual(json.loads(self.setting.read_text())['path'], str(self.clip))
        self.assertEqual(self.helper.main(['speech', 'disable']), 0)
        with patch.object(self.helper.shutil, 'which', return_value='/usr/bin/mpv'), patch.object(self.helper.subprocess, 'run', return_value=SimpleNamespace(returncode=0)) as player:
            self.helper.main(['codex-kitty', 'Complete', '', '', 'NORMAL'])
            self.assertEqual(player.call_count, 1)

    def speech_fixture(self, synthesis='success', clip_failure=False):
        """Run actual children with controlled synthesis and playback side effects."""
        python = self.root / 'piper-python'
        python.write_text(textwrap.dedent("""\
            #!/usr/bin/python3
            import json,os,pathlib,sys,time
            root=pathlib.Path(os.environ['FIXTURE_ROOT'])
            def event(value):
                with (root/'events').open('a') as output:
                    output.write(value+'\\n')
            (root/'synthesis.pid').write_text(str(os.getpid()))
            text=sys.stdin.read()
            (root/'synthesis.args').write_text(json.dumps(sys.argv[1:]))
            event('synthesis start')
            (root/'synthesis-started').touch()
            mode=os.environ['SYNTHESIS_MODE']
            if mode=='blocked':
                while True: time.sleep(.05)
            if mode=='success':
                while not (root/'clip-ended').exists(): time.sleep(.01)
            if mode=='delayed':
                while not (root/'clip-ended').exists(): time.sleep(.01)
                time.sleep(.15)
            if mode=='past-deadline': time.sleep(.8)
            if mode=='failed': sys.exit(2)
            if mode!='empty':
                pathlib.Path(sys.argv[sys.argv.index('--output_file')+1]).write_text(text)
            event('synthesis end')
        """))
        python.chmod(0o755)
        model = self.root / 'voice.onnx'
        player = self.root / 'mpv'
        player.write_text(textwrap.dedent("""\
            #!/usr/bin/python3
            import json,os,pathlib,sys,time
            root=pathlib.Path(os.environ['FIXTURE_ROOT'])
            def event(value):
                with (root/'events').open('a') as output:
                    output.write(value+'\\n')
            path=pathlib.Path(sys.argv[-1])
            if path.suffix=='.mp3':
                event('clip start')
                deadline=time.monotonic()+.6
                while not (root/'synthesis-started').exists() and time.monotonic()<deadline:
                    time.sleep(.01)
                if (root/'synthesis-started').exists(): event('synthesis overlaps clip')
                if os.environ['SYNTHESIS_MODE']=='past-deadline':
                    time.sleep(.4)
                    pid=(root/'synthesis.pid').read_text()
                    status=pathlib.Path('/proc')/pid/'stat'
                    if not status.exists() or status.read_text().split()[2]=='Z':
                        event('synthesis stopped during clip')
                event('clip end')
                (root/'clip-ended').touch()
                if os.environ['CLIP_FAILURE']=='1': sys.exit(2)
            else:
                event('title '+path.read_text().rstrip('\\n'))
                (root/'wav-path').write_text(str(path))
                if os.environ['SYNTHESIS_MODE']=='speech-playback-failed': sys.exit(2)
        """))
        player.chmod(0o755)
        return (patch.dict(os.environ, {'FIXTURE_ROOT': str(self.root),
                    'SYNTHESIS_MODE': synthesis, 'CLIP_FAILURE': str(int(clip_failure))}),
                patch.object(self.helper.shutil, 'which', return_value=str(player)),
                patch.object(self.helper, 'voice_ready', return_value=True),
                patch.object(self.helper, 'voice_paths', return_value=(python, model)))

    def test_synthesis_overlaps_clip_but_title_plays_after_once(self):
        self.configure()
        title = f'Fix café $(touch {self.root / "nope"}); "quotes"'
        env, player, ready, voice = self.speech_fixture()
        with env, player, ready, voice:
            self.assertEqual(self.helper.main(['preview', '--title', title, '--plain', '--details']), 0)
        events = (self.root / 'events').read_text().splitlines()
        self.assertIn('synthesis overlaps clip', events)
        self.assertLess(events.index('synthesis start'), events.index('clip end'))
        self.assertGreater(events.index('synthesis end'), events.index('clip end'))
        self.assertEqual(events.count('clip start'), 1)
        self.assertEqual(events.count('title '+title), 1)
        self.assertGreater(events.index('title '+title), events.index('clip end'))
        self.assertGreater(events.index('title '+title), events.index('synthesis end'))
        self.assertFalse(Path((self.root / 'wav-path').read_text()).exists())
        self.assertFalse((self.root / 'nope').exists())

    def test_clip_failure_stops_and_reaps_owned_synthesis(self):
        self.configure()
        env, player, ready, voice = self.speech_fixture(synthesis='blocked', clip_failure=True)
        with env, player, ready, voice:
            self.assertEqual(self.helper.main(['preview', '--title', 'Exact title']), 1)
        self.assertTrue((self.root / 'synthesis.pid').exists())
        pid = int((self.root / 'synthesis.pid').read_text())
        with self.assertRaises(ProcessLookupError):
            os.kill(pid, 0)
        events = (self.root / 'events').read_text().splitlines()
        self.assertEqual(events.count('clip start'), 1)
        self.assertNotIn('title Exact title', events)

    def test_synthesis_deadline_includes_clip_time(self):
        self.configure()
        env, player, ready, voice = self.speech_fixture(synthesis='delayed')
        with env, player, ready, voice, patch.object(self.helper, 'time', SimpleNamespace(monotonic=iter([0, 0, 31]).__next__), create=True):
            self.assertEqual(self.helper.main(['preview', '--title', 'Exact title']), 0)
        events = (self.root / 'events').read_text().splitlines()
        self.assertEqual(events.count('clip start'), 1)
        self.assertNotIn('title Exact title', events)
        pid = int((self.root / 'synthesis.pid').read_text())
        with self.assertRaises(ProcessLookupError):
            os.kill(pid, 0)
        self.assertIn('timed out', (self.state / 'codex-notification-sound/errors.log').read_text())

    def test_hard_synthesis_deadline_expires_during_long_clip(self):
        self.configure()
        env, player, ready, voice = self.speech_fixture(synthesis='past-deadline')
        with env, player, ready, voice, patch.object(self.helper, 'SYNTHESIS_TIMEOUT', .2, create=True):
            self.assertEqual(self.helper.play('Exact title'), 0)
        events = (self.root / 'events').read_text().splitlines()
        self.assertIn('synthesis stopped during clip', events)
        self.assertLess(events.index('synthesis stopped during clip'), events.index('clip end'))
        self.assertEqual(events.count('clip start'), 1)
        self.assertNotIn('title Exact title', events)
        pid = int((self.root / 'synthesis.pid').read_text())
        with self.assertRaises(ProcessLookupError):
            os.kill(pid, 0)
        self.assertIn('timed out', (self.state / 'codex-notification-sound/errors.log').read_text())

    def test_synthesis_failure_keeps_mp3(self):
        for mode in ('failed', 'empty'):
            with self.subTest(mode=mode):
                self.configure()
                (self.root / 'events').unlink(missing_ok=True)
                env, player, ready, voice = self.speech_fixture(synthesis=mode)
                with env, player, ready, voice:
                    self.assertEqual(self.helper.main(['preview', '--title', 'Exact title']), 0)
                events = (self.root / 'events').read_text().splitlines()
                self.assertEqual(events.count('clip start'), 1)
                self.assertNotIn('title Exact title', events)

    def test_absent_title_and_unavailable_voice_keep_clip_only(self):
        self.configure()
        env, player, ready, voice = self.speech_fixture()
        with env, player, ready, voice:
            for title, available in ((None, True), ('', True), ('Exact title', False)):
                with self.subTest(title=title, available=available):
                    (self.root / 'events').unlink(missing_ok=True)
                    with patch.object(self.helper, 'voice_ready', return_value=available):
                        self.assertEqual(self.helper.play(title), 0)
                    self.assertEqual((self.root / 'events').read_text().splitlines(), ['clip start', 'clip end'])
                    self.assertFalse((self.root / 'synthesis.pid').exists())

    def test_synthesis_start_failure_keeps_clip_once(self):
        self.configure()
        env, player, ready, voice = self.speech_fixture()
        with env, player, ready, voice, patch.object(self.helper, 'voice_paths', return_value=(self.root / 'missing-python', self.root / 'voice.onnx')):
            self.assertEqual(self.helper.play('Exact title'), 0)
        self.assertEqual((self.root / 'events').read_text().splitlines(), ['clip start', 'clip end'])
        self.assertFalse((self.root / 'synthesis.pid').exists())
        self.assertIn('missing-python', (self.state / 'codex-notification-sound/errors.log').read_text())

    def test_malformed_speech_setting_keeps_dunst_mp3(self):
        self.configure()
        speech = self.setting.with_name('speech.json')
        for value in ('[]', '{"enabled": "yes"}', 'bad', '{"enabled": 1}'):
            speech.write_text(value)
            with patch.object(self.helper.shutil, 'which', return_value='/usr/bin/mpv'), patch.object(self.helper.subprocess, 'run', return_value=SimpleNamespace(returncode=0)) as player:
                self.helper.main(['codex-kitty', 'Complete', '', '', 'NORMAL'])
                self.assertEqual(player.call_count, 1)


    def test_readable_status_plain_details_and_narrow_terminal(self):
        import contextlib
        import io
        self.configure()
        for args, detailed in ((['status'], False), (['status', '--plain', '--details'], True)):
            output = io.StringIO()
            with contextlib.redirect_stdout(output), patch.dict(os.environ, {'COLUMNS': '40', 'NO_COLOR': '1'}):
                self.assertEqual(self.helper.main(args), 0)
            text = output.getvalue()
            self.assertIn('Speech', text)
            self.assertIn('Voice', text)
            if detailed:
                self.assertTrue(text.isascii())
                self.assertIn(str(self.setting), text)
            else:
                self.assertNotIn(str(self.setting), text)
                self.assertIn('🔊', text)
                self.assertTrue(all(len(line) <= 40 for line in text.splitlines()))
            self.assertNotIn('\x1b', text)

    def test_concurrent_sequences_never_overlap(self):
        self.configure()
        data = self.root / 'data/codex-notification-speech'
        python = data / 'venv/bin/python'
        python.parent.mkdir(parents=True)
        python.write_text('#!/usr/bin/python3\nimport pathlib,sys\ntext=sys.stdin.read()\npathlib.Path(sys.argv[sys.argv.index("--output_file")+1]).write_text(text)\n')
        python.chmod(0o755)
        model = data / 'voices/en_US-Voice Contributor-high.onnx'
        model.parent.mkdir()
        model.write_bytes(b'fixture')
        model.with_suffix('.onnx.json').write_text('{}')
        binary = self.root / 'bin'
        binary.mkdir()
        player = binary / 'mpv'
        events = self.root / 'playbacks'
        player.write_text('#!/usr/bin/python3\nimport json,os,pathlib,sys,time\np=pathlib.Path(sys.argv[-1])\nv="clip" if p.suffix==".mp3" else p.read_text().strip()\nf=open(os.environ["EVENTS"],"a",buffering=1)\nf.write("start "+v+"\\n")\ntime.sleep(.08)\nf.write("end "+v+"\\n")\n')
        player.chmod(0o755)
        env = {**os.environ, 'XDG_DATA_HOME': str(self.root / 'data'), 'PATH': str(binary)+':'+os.environ['PATH'], 'EVENTS': str(events)}
        workers = [subprocess.Popen([sys.executable, str(ROOT / 'scripts/executable_codex-notification-sound'), 'preview', '--title', title], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for title in ('Title A', 'Title B')]
        for worker in workers:
            stdout, stderr = worker.communicate(timeout=10)
            self.assertEqual(worker.returncode, 0, stdout + stderr)
        lines = events.read_text().splitlines()
        self.assertEqual(len(lines), 8)
        self.assertEqual(lines[:2], ['start clip', 'end clip'])
        self.assertEqual(lines[4:6], ['start clip', 'end clip'])
        titles = [lines[2].removeprefix('start '), lines[6].removeprefix('start ')]
        self.assertEqual(set(titles), {'Title A', 'Title B'})
        self.assertEqual(lines[3], 'end '+titles[0])
        self.assertEqual(lines[7], 'end '+titles[1])

        # Exercise a real completion bridge while audio is queued, then rename.
        import fcntl
        import time
        self.assertEqual(self.helper.main(['speech', 'enable']), 0)
        codex = self.root / 'codex'
        (codex / 'sessions').mkdir(parents=True)
        identity = '33333333-3333-4333-8333-333333333333'
        transcript = codex / 'sessions/rollout-separate-uuid.jsonl'
        transcript.write_text(json.dumps({'type': 'session_meta', 'payload': {'id': identity, 'source': 'cli'}})+'\n')
        index = codex / 'session_index.jsonl'
        index.write_text(json.dumps({'id': identity, 'thread_name': 'Queued café; $(no)'})+'\n')
        env['CODEX_HOME'] = str(codex)
        lock = self.state / 'codex-notification-sound/playback.lock'
        with lock.open('a') as owner:
            fcntl.flock(owner, fcntl.LOCK_EX)
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/executable_codex-notification-event')],
                input=json.dumps({'type': 'agent-turn-complete', 'thread-id': identity, 'last-assistant-message': 'Ready to read.'}),
                text=True, capture_output=True, env=env, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, '')  # Never returns an approval decision.
            index.write_text(json.dumps({'id': identity, 'thread_name': 'Renamed after queue'})+'\n')
        deadline = time.monotonic()+5
        while len(events.read_text().splitlines()) < 12 and time.monotonic() < deadline:
            time.sleep(.02)
        self.assertEqual(events.read_text().splitlines()[8:], ['start clip', 'end clip', 'start Queued café; $(no)', 'end Queued café; $(no)'])


class EventBridgeTests(unittest.TestCase):
    A = '11111111-1111-4111-8111-111111111111'
    B = '22222222-2222-4222-8222-222222222222'

    def setUp(self):
        path = ROOT / 'scripts/executable_codex-notification-event'
        self.assertTrue(path.exists(), 'Exact-ID event bridge missing')
        self.bridge = load('event_bridge', path)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / 'codex'
        self.home.mkdir()
        self.env = patch.dict(os.environ, {'CODEX_HOME': str(self.home)})
        self.env.start()
        self.addCleanup(self.env.stop)

    def transcript(self, identity, source='cli', filename=None):
        path = self.home / 'sessions' / (filename or ('rollout-' + identity + '.jsonl'))
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps({'type': 'session_meta', 'payload': {'id': identity, 'source': source}}) + '\n')
        return path

    def names(self):
        (self.home / 'session_index.jsonl').write_text('\n'.join(json.dumps(x) for x in [
            {'id': self.A, 'thread_name': 'Old A'}, {'id': self.B, 'thread_name': 'Visible B'},
            {'id': self.A, 'thread_name': 'Renamed café; $(no)'}]) + '\n')

    def test_completion_uses_exact_thread_and_latest_title(self):
        self.transcript(self.A)
        self.transcript(self.B)
        self.names()
        self.assertEqual(self.bridge.resolve_event({'type': 'agent-turn-complete', 'thread-id': self.A}) , (True, 'Renamed café; $(no)'))

    def test_permission_uses_first_metadata_not_parent_session_or_filename(self):
        path = self.transcript(self.B, {'subagent': {'thread_spawn': {'parent_thread_id': self.A}}}, 'rollout-' + self.A + '.jsonl')
        self.names()
        event = {'hook_event_name': 'PermissionRequest', 'transcript_path': str(path), 'session_id': self.A, 'agent_id': self.B}
        self.assertEqual(self.bridge.resolve_event(event), (True, 'Visible B'))
        event['agent_id'] = self.A
        self.assertEqual(self.bridge.resolve_event(event), (True, None))

    def test_separate_rollout_uuid_and_copied_metadata_do_not_override_id(self):
        path = self.transcript(self.A, filename='rollout-' + self.B + '.jsonl')
        self.names()
        self.assertEqual(self.bridge.resolve_event({'type': 'agent-turn-complete', 'thread-id': self.A}), (True, 'Renamed café; $(no)'))
        self.assertEqual(self.bridge.resolve_event({'hook_event_name': 'PermissionRequest', 'agent_id': self.B, 'transcript_path': str(path)}), (True, None))

    def test_missing_title_for_known_root_means_clip_only(self):
        self.transcript(self.A)
        self.assertEqual(self.bridge.resolve_event({'type': 'agent-turn-complete', 'thread-id': self.A}), (True, None))

    def test_unknown_completion_identity_stays_silent(self):
        self.names()
        for identity in (self.B, 'bad', None):
            self.assertEqual(self.bridge.resolve_event({'type': 'agent-turn-complete', 'thread-id': identity}), (False, None))

    def test_internal_system_and_reviewers_are_silent(self):
        self.names()
        for source in ('review', 'guardian', {'subagent': 'guardian'}, {'subagent': {'thread_spawn': {'agent_role': 'reviewer'}}}, {'subagent': 'session_review'}, {'subagent': {'other': 'guardian'}}, {'subagent': {'other': 'session_review'}}, 'system'):
            self.transcript(self.A, source)
            self.assertEqual(self.bridge.resolve_event({'type': 'agent-turn-complete', 'thread-id': self.A}), (False, None))
        self.assertEqual(self.bridge.resolve_event({'type': 'something-else'}), (False, None))

    def test_duplicate_internal_metadata_stays_silent(self):
        self.names()
        self.transcript(self.A, 'guardian')
        self.transcript(self.A, 'cli', 'copied-metadata.jsonl')
        self.assertEqual(self.bridge.resolve_event({'type': 'agent-turn-complete', 'thread-id': self.A}), (False, None))

    def test_worker_completion_is_silent_even_with_nonblank_inherited_answer(self):
        self.names()
        meta = {'subagent': {'thread_spawn': {'agent_role': 'worker', 'agent_nickname': 'review'}}}
        path = self.transcript(self.A, meta)
        with path.open('a') as stream:
            stream.write(json.dumps({'type': 'event_msg', 'payload': {'type': 'task_complete', 'last_agent_message': 'Copied parent answer'}})+'\n')
        self.assertFalse(self.bridge.internal({'source': meta}))  # Nickname remains user data.
        with patch.object(self.bridge, 'speech_enabled', return_value=True), patch.object(self.bridge.subprocess, 'Popen') as spawn:
            self.assertEqual(self.bridge.main([json.dumps({'type': 'agent-turn-complete', 'thread-id': self.A, 'last-assistant-message': 'Worker finished'})]), 0)
            spawn.assert_not_called()

    def test_missing_or_blank_final_response_never_spawns_audio(self):
        self.transcript(self.A)
        self.names()
        for answer in (None, '', ' \t\n\u00a0\u2003 ', [], {}):
            event = {'type': 'agent-turn-complete', 'thread-id': self.A, 'last-assistant-message': answer}
            with self.subTest(answer=answer), patch.object(self.bridge, 'speech_enabled', return_value=True), patch.object(self.bridge.subprocess, 'Popen') as spawn:
                self.assertEqual(self.bridge.main([json.dumps(event)]), 0)
                spawn.assert_not_called()
        with patch.object(self.bridge, 'speech_enabled', return_value=True), patch.object(self.bridge.subprocess, 'Popen') as spawn:
            self.assertEqual(self.bridge.main([json.dumps({'type': 'agent-turn-complete', 'thread-id': self.A})]), 0)
            spawn.assert_not_called()

    def test_parent_provenance_overrides_root_shaped_source(self):
        self.names()
        for key in ('parent_thread_id', 'parent_session_id'):
            path = self.transcript(self.A)
            path.write_text(json.dumps({'type': 'session_meta', 'payload': {'id': self.A, 'source': 'cli', key: self.B}})+'\n')
            self.assertEqual(self.bridge.resolve_event({'type': 'agent-turn-complete', 'thread-id': self.A}), (False, None))

    def test_unknown_or_malformed_source_is_silent(self):
        self.names()
        for source in (None, 'unknown', 'future-source', {}, {'cli': {}}, {'subagent': {}}):
            with self.subTest(source=source):
                self.transcript(self.A, source)
                self.assertEqual(self.bridge.resolve_event({'type': 'agent-turn-complete', 'thread-id': self.A}), (False, None))

    def test_conflicting_duplicate_root_metadata_is_silent(self):
        self.names()
        self.transcript(self.A, 'cli')
        self.transcript(self.A, 'vscode', 'duplicate.jsonl')
        self.assertEqual(self.bridge.resolve_event({'type': 'agent-turn-complete', 'thread-id': self.A}), (False, None))

    def test_vscode_completion_with_answer_captures_title(self):
        self.transcript(self.A, 'vscode')
        self.names()
        with patch.object(self.bridge, 'speech_enabled', return_value=True), patch.object(self.bridge.subprocess, 'Popen') as spawn:
            self.assertEqual(self.bridge.main([json.dumps({'type': 'agent-turn-complete', 'thread-id': self.A, 'last-assistant-message': 'Finished café'})]), 0)
            self.assertEqual(json.loads(spawn.return_value.stdin.write.call_args.args[0]), 'Renamed café; $(no)')

    def test_permission_requests_never_spawn_speech_during_work(self):
        path = self.transcript(self.A)
        self.names()
        with patch.object(self.bridge, 'speech_enabled', return_value=True), patch.object(self.bridge.subprocess, 'Popen') as spawn:
            for _ in range(3):
                event = {'hook_event_name': 'PermissionRequest', 'transcript_path': str(path), 'agent_id': self.A}
                self.assertEqual(self.bridge.main([json.dumps(event)]), 0)
            spawn.assert_not_called()

    def test_title_captured_before_detached_worker(self):
        self.transcript(self.A)
        self.names()
        with patch.object(self.bridge, 'speech_enabled', return_value=True), patch.object(self.bridge.subprocess, 'Popen') as spawn:
            self.assertEqual(self.bridge.main([json.dumps({'type': 'agent-turn-complete', 'thread-id': self.A, 'last-assistant-message': 'Ready to read.'})]), 0)
            self.assertTrue(spawn.call_args.kwargs['start_new_session'])
            self.assertEqual(json.loads(spawn.return_value.stdin.write.call_args.args[0]), 'Renamed café; $(no)')


class EventProbeTests(unittest.TestCase):
    def test_real_event_cli_probe_exercises_audio_and_silent_paths(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/smoke_codex_notification_events.py'), '--plain'], capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn('PASS completion: 1 playback', result.stdout)
        for kind in ('worker', 'empty', 'missing', 'unknown', 'ambiguous', 'parent', 'permission'):
            self.assertIn(f'PASS {kind}: 0 playback', result.stdout)


if __name__ == '__main__':
    unittest.main()
