"""Numbered voice audition, replay, offline and clip ordering contracts."""
import contextlib
import importlib.machinery
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import wave

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / 'scripts/executable_codex-voice-auditions'


class AuditionTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(HELPER.is_file(), 'numbered voice audition helper is not implemented')
        loader = importlib.machinery.SourceFileLoader('voice_auditions', str(HELPER))
        spec = importlib.util.spec_from_loader('voice_auditions', loader)
        self.helper = importlib.util.module_from_spec(spec)
        loader.exec_module(self.helper)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name) / 'data with spaces'
        self.env = patch.dict(os.environ, {'XDG_DATA_HOME': str(self.data)})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.events = []
        self.inputs = []
        self.output = io.StringIO()
        self.errors = io.StringIO()
        self.root = self.data / 'codex-notification-speech'
        self.python = self.root / 'venv/bin/python'
        self.python.parent.mkdir(parents=True)
        self.python.write_text('#!/bin/sh\n')
        self.python.chmod(0o700)
        self.models = self.root / 'voices'
        self.models.mkdir()
        for voice in self.helper.VOICES:
            (self.models / (voice[1] + '.onnx')).write_bytes(b'model fixture')
            (self.models / (voice[1] + '.onnx.json')).write_text(json.dumps({'audio': {'sample_rate': 22050}}))
        self.out = Path(self.temp.name) / 'audio with spaces'

    def process(self, argv, **kwargs):
        events = self.events
        if '-c' in argv:
            stdout = '1.8.0\n'
        else:
            stdout = ''
        if 'piper' in argv:
            events.append('synthesis')
            self.inputs.append(kwargs['stdin'].read())
            wav = argv[argv.index('--output-file') + 1]
            with wave.open(wav, 'wb') as audio:
                audio.setnchannels(1)
                audio.setsampwidth(2)
                audio.setframerate(22050)
                audio.writeframes(b'\0\0' * 200)
        elif argv[0] == '/fake/mpv':
            events.append('speech' if argv[-1].endswith('.wav') else 'clip')
        class Process:
            returncode = 0
            def communicate(self, timeout=None):
                return stdout, ''
            def poll(self):
                return 0
            def kill(self):
                events.append('kill')
        return Process()

    def run_helper(self, args):
        with contextlib.redirect_stdout(self.output), contextlib.redirect_stderr(self.errors), patch.object(self.helper.subprocess, 'Popen', side_effect=self.process), patch.object(self.helper.shutil, 'which', return_value='/fake/mpv'):
            return self.helper.main(args + ['--plain'])

    def test_list_has_ten_numbered_alternatives_and_no_runtime_calls(self):
        self.assertEqual(self.run_helper(['--list']), 0)
        text = self.output.getvalue()
        self.assertIn(' 1 ', text)
        self.assertIn('10 ', text)
        self.assertIn('Amy', text)
        self.assertIn('Jenny', text)
        self.assertNotIn('lessac', text.lower())
        self.assertTrue(text.isascii())
        self.assertEqual(self.events, [])

    def test_custom_replay_starts_synthesis_before_clip_and_speech_after(self):
        text = 'All done! $(touch nope) stays literal.'
        self.assertEqual(self.run_helper(['--voice', '1', '--text', text, '--output-dir', str(self.out)]), 0)
        self.assertEqual(self.events, ['synthesis', 'clip', 'speech'])
        self.assertEqual(self.inputs, [text + '\n'])
        self.assertIn('1/10', self.output.getvalue())
        self.assertIn('Amy', self.output.getvalue())
        self.assertIn('Gap after clip', self.output.getvalue())
        self.assertEqual(len(list(self.out.glob('*.wav'))), 1)

    def test_render_all_produces_ten_valid_wavs_and_manifest_without_playback(self):
        self.assertEqual(self.run_helper(['--render-only', '--output-dir', str(self.out)]), 0)
        self.assertEqual(self.events, ['synthesis'] * 10)
        self.assertEqual(len(list(self.out.glob('*.wav'))), 10)
        manifest = json.loads((self.out / 'manifest.json').read_text())
        self.assertEqual(len(manifest['voices']), 10)
        self.assertEqual(manifest['text'] + '\n', self.inputs[0])
        self.assertTrue(all(value == self.inputs[0] for value in self.inputs))

    def test_offline_missing_model_is_actionable_without_download(self):
        (self.models / (self.helper.VOICES[0][1] + '.onnx')).unlink()
        self.assertEqual(self.run_helper(['--voice', '1', '--offline']), 1)
        self.assertIn('offline', self.errors.getvalue().lower())
        self.assertEqual(self.events, [])

    def test_name_selector_and_named_samples_work_in_dry_run(self):
        self.assertEqual(self.run_helper(['--voice', 'Voice Contributor', '--sample', 'celebrate', '--dry-run']), 0)
        self.assertIn('Voice Contributor', self.output.getvalue())
        self.assertIn('All done!', self.output.getvalue())
        self.assertEqual(self.events, [])

    def test_clip_failure_kills_owned_synthesis_and_preserves_old_wav(self):
        original = self.process
        events = self.events
        class ActiveProcess:
            returncode = None
            def poll(self):
                return self.returncode
            def communicate(self, timeout=None):
                return '', ''
            def kill(self):
                events.append('kill')
                self.returncode = -9
        child = ActiveProcess()
        def dependency(argv, **kwargs):
            if 'piper' in argv:
                events.append('synthesis')
                return child
            result = original(argv, **kwargs)
            if argv[0] == '/fake/mpv':
                result.returncode = 1
            return result
        self.out.mkdir()
        old = self.out / ('01-' + self.helper.VOICES[0][1] + '.wav')
        old.write_bytes(b'previous valid sample')
        with patch.object(self, 'process', side_effect=dependency):
            self.assertEqual(self.run_helper(['--voice', '1', '--output-dir', str(self.out)]), 1)
        self.assertEqual(events, ['synthesis', 'clip', 'kill'])
        self.assertEqual(old.read_bytes(), b'previous valid sample')
        self.assertFalse(list(self.out.glob('sample-*')))

    def test_watchdog_start_failure_reaps_owned_synthesis(self):
        original = self.process
        events = self.events
        class ActiveProcess:
            returncode = None
            def poll(self):
                return self.returncode
            def communicate(self, timeout=None):
                return '', ''
            def kill(self):
                events.append('kill')
                self.returncode = -9
        def dependency(argv, **kwargs):
            if 'piper' in argv:
                events.append('synthesis')
                return ActiveProcess()
            return original(argv, **kwargs)
        with patch.object(self, 'process', side_effect=dependency), patch.object(self.helper.threading.Timer, 'start', side_effect=RuntimeError('thread unavailable')):
            self.assertEqual(self.run_helper(['--voice', '1', '--render-only', '--output-dir', str(self.out)]), 1)
        self.assertIn('thread unavailable', self.errors.getvalue())
        self.assertEqual(events, ['synthesis', 'kill'])

    def test_truncated_wav_is_rejected_before_playback_or_publish(self):
        original = self.process
        def dependency(argv, **kwargs):
            result = original(argv, **kwargs)
            if 'piper' in argv:
                wav = Path(argv[argv.index('--output-file') + 1])
                wav.write_bytes(wav.read_bytes()[:44])
            return result
        with patch.object(self, 'process', side_effect=dependency):
            self.assertEqual(self.run_helper(['--voice', '1', '--output-dir', str(self.out)]), 1)
        self.assertEqual(self.events, ['synthesis', 'clip'])
        self.assertFalse(list(self.out.glob('*.wav')))

    def test_incomplete_download_is_not_published(self):
        original = self.process
        voice = self.helper.VOICES[0][1]
        (self.models / (voice + '.onnx')).unlink()
        def dependency(argv, **kwargs):
            if 'piper.download_voices' in argv:
                directory = Path(argv[argv.index('--data-dir') + 1])
                (directory / (voice + '.onnx')).write_bytes(b'partial')
            return original(argv, **kwargs)
        with patch.object(self, 'process', side_effect=dependency):
            self.assertEqual(self.run_helper(['--voice', '1', '--render-only']), 1)
        self.assertFalse((self.models / (voice + '.onnx')).exists())
        self.assertFalse(list(self.root.glob('audition-download-*')))
        self.assertEqual(self.events, [])

    def test_samples_are_visible_without_audio(self):
        self.assertEqual(self.run_helper(['--samples']), 0)
        self.assertIn('celebrate', self.output.getvalue())
        self.assertIn('technical', self.output.getvalue())
        self.assertEqual(self.events, [])


if __name__ == '__main__':
    unittest.main()
