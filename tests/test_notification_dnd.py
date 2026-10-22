"""Isolated real-player boundary checks for i3blocks DND and automatic TTS."""
import importlib.machinery
import importlib.util
import io
import json
import os
import subprocess
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class DndTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        loader = importlib.machinery.SourceFileLoader('dnd_sound', str(ROOT / 'scripts/executable_codex-notification-sound'))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        self.helper = importlib.util.module_from_spec(spec)
        loader.exec_module(self.helper)
        self.pause = self.root / 'paused'
        self.pause.write_text('true')
        self.log = self.root / 'played'
        binary = self.root / 'bin'
        binary.mkdir()
        scripts = {
            'dunstctl': '#!/bin/sh\ncat "$DND_FIXTURE/paused"\n',
            'mpv': '''#!/usr/bin/python3
import os,pathlib,sys
root=pathlib.Path(os.environ['DND_FIXTURE'])
with (root/'played').open('a') as output: output.write(pathlib.Path(sys.argv[-1]).suffix+'\\n')
if os.environ.get('PAUSE_AFTER_CLIP')=='1': (root/'paused').write_text('true')
''',
            'piper-python': '''#!/usr/bin/python3
import pathlib,sys
pathlib.Path(sys.argv[sys.argv.index('--output_file')+1]).write_bytes(b'wave')
''',
        }
        for name, content in scripts.items():
            path = binary / name
            path.write_text(content)
            path.chmod(0o755)
        env = patch.dict(os.environ, {'PATH': str(binary), 'DND_FIXTURE': str(self.root),
                                    'XDG_CONFIG_HOME': str(self.root / 'config'),
                                    'XDG_STATE_HOME': str(self.root / 'state')})
        env.start()
        self.addCleanup(env.stop)
        # dunstctl uses an absolute cat because the fixture PATH is isolated.
        (binary / 'dunstctl').write_text('#!/bin/sh\n/bin/cat "$DND_FIXTURE/paused"\n')
        clip = self.root / 'intro.mp3'
        clip.write_bytes(b'clip')
        setting = self.helper.setting_path()
        setting.parent.mkdir(parents=True)
        setting.write_text(json.dumps({'path': str(clip)}))
        setting.with_name('speech.json').write_text('{"enabled":true}')
        for name, value in [('voice_ready', True), ('voice_paths', (binary / 'piper-python', self.root / 'voice.onnx'))]:
            dependency = patch.object(self.helper, name, return_value=value)
            dependency.start()
            self.addCleanup(dependency.stop)

    def event(self):
        with patch('sys.stdin', io.StringIO('"DND test"')):
            self.assertEqual(self.helper.main(['event-play']), 0)

    def test_paused_event_is_silent_and_resumed_event_plays(self):
        self.event()
        self.assertFalse(self.log.exists(), 'DND must suppress automatic clip and TTS')
        self.pause.write_text('false')
        self.event()
        self.assertEqual(self.log.read_text().splitlines(), ['.mp3', '.wav'])

    def test_preview_remains_available_while_paused(self):
        self.assertEqual(self.helper.main(['preview', '--speech-only', '--title', 'Preview']), 0)
        self.assertEqual(self.log.read_text().splitlines(), ['.wav'])

    def test_pause_while_waiting_for_lock_discards_queued_audio(self):
        self.pause.write_text('false')
        with patch.object(self.helper.fcntl, 'flock', side_effect=lambda *args: self.pause.write_text('true')):
            self.event()
        self.assertFalse(self.log.exists())

    def test_pause_during_clip_suppresses_following_speech(self):
        self.pause.write_text('false')
        with patch.dict(os.environ, {'PAUSE_AFTER_CLIP': '1'}):
            self.event()
        self.assertEqual(self.log.read_text().splitlines(), ['.mp3'])

    def test_failed_or_timed_out_dunst_preserves_audio(self):
        run = self.helper.subprocess.run
        for failure in (subprocess.CompletedProcess(['dunstctl'], 1, 'true', 'offline'),
                        subprocess.TimeoutExpired('dunstctl', 1)):
            with self.subTest(failure=failure):
                self.log.unlink(missing_ok=True)
                def query(command, **kwargs):
                    if command[0] == 'dunstctl':
                        self.assertEqual(kwargs['timeout'], 1)
                        if isinstance(failure, Exception):
                            raise failure
                        return failure
                    return run(command, **kwargs)
                with patch.object(self.helper.subprocess, 'run', side_effect=query):
                    self.event()
                self.assertEqual(self.log.read_text().splitlines(), ['.mp3', '.wav'])

    def test_unavailable_dunst_preserves_audio(self):
        (self.root / 'bin/dunstctl').unlink()
        self.event()
        self.assertEqual(self.log.read_text().splitlines(), ['.mp3', '.wav'])


if __name__ == '__main__':
    unittest.main()
