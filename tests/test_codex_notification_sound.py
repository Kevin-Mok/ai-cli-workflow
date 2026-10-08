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

    def test_mp3_then_title_stdin_timeout_and_cleanup(self):
        self.configure()
        title = 'Fix café $(touch nope); "quotes"'
        calls = []
        def run(argv, **kwargs):
            calls.append((argv, kwargs))
            if '-m' in argv:
                Path(argv[argv.index('--output_file') + 1]).write_bytes(b'RIFFfixture')
            return SimpleNamespace(returncode=0)
        with patch.object(self.helper.shutil, 'which', return_value='/usr/bin/mpv'), patch.object(self.helper, 'voice_ready', return_value=True, create=True), patch.object(self.helper.subprocess, 'run', side_effect=run):
            self.assertEqual(self.helper.main(['preview', '--title', title, '--plain', '--details']), 0)
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0][0][-1], str(self.clip))
        self.assertEqual(calls[1][1]['input'], title + '\n')
        self.assertEqual(calls[1][1]['timeout'], 30)
        self.assertNotIn(title, calls[1][0])
        self.assertEqual(calls[2][1]['timeout'], 60)
        self.assertFalse(Path(calls[2][0][-1]).exists())

    def test_synthesis_failure_keeps_mp3(self):
        self.configure()
        calls = []
        def run(argv, **kwargs):
            calls.append(argv)
            if '-m' in argv:
                raise subprocess.TimeoutExpired('piper', 30)
            return SimpleNamespace(returncode=0)
        with patch.object(self.helper.shutil, 'which', return_value='/usr/bin/mpv'), patch.object(self.helper, 'voice_ready', return_value=True, create=True), patch.object(self.helper.subprocess, 'run', side_effect=run):
            self.assertEqual(self.helper.main(['preview', '--title', 'Exact title']), 0)
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][-1], str(self.clip))

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
        model = data / 'voices/en_US-lessac-medium.onnx'
        model.parent.mkdir()
        model.write_bytes(b'fixture')
        model.with_suffix('.onnx.json').write_text('{}')
        binary = self.root / 'bin'
        binary.mkdir()
        player = binary / 'mpv'
        events = self.root / 'playbacks'
        player.write_text('#!/usr/bin/python3\nimport os,pathlib,sys,time\np=pathlib.Path(sys.argv[-1])\nv="clip" if p.suffix==".mp3" else p.read_text().strip()\nf=open(os.environ["EVENTS"],"a",buffering=1)\nf.write("start "+v+"\\n")\ntime.sleep(.08)\nf.write("end "+v+"\\n")\n')
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
                input=json.dumps({'type': 'agent-turn-complete', 'thread-id': identity}),
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

    def test_missing_title_identity_or_external_path_means_clip_only(self):
        path = self.transcript(self.A)
        for event in ({'type': 'agent-turn-complete', 'thread-id': self.A}, {'type': 'agent-turn-complete', 'thread-id': self.B}, {'hook_event_name': 'PermissionRequest', 'transcript_path': '/tmp/outside.jsonl'}, {'hook_event_name': 'PermissionRequest', 'transcript_path': str(path), 'agent_id': 'bad'}):
            self.assertEqual(self.bridge.resolve_event(event), (True, None))

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

    def test_worker_nickname_is_not_internal_provenance(self):
        self.names()
        self.transcript(self.A, {'subagent': {'thread_spawn': {'agent_role': 'worker', 'agent_nickname': 'review'}}})
        self.assertEqual(self.bridge.resolve_event({'type': 'agent-turn-complete', 'thread-id': self.A}), (True, 'Renamed café; $(no)'))

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
            self.assertEqual(self.bridge.main([json.dumps({'type': 'agent-turn-complete', 'thread-id': self.A})]), 0)
            self.assertTrue(spawn.call_args.kwargs['start_new_session'])
            self.assertEqual(json.loads(spawn.return_value.stdin.write.call_args.args[0]), 'Renamed café; $(no)')


if __name__ == '__main__':
    unittest.main()
