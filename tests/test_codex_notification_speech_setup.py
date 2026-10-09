"""Offline readiness and isolated installation contracts for Piper setup."""
import contextlib
import importlib.machinery
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import wave

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / 'scripts/executable_setup-codex-notification-speech'


class SpeechSetupTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(HELPER.is_file(), 'speech setup helper is not implemented')
        loader = importlib.machinery.SourceFileLoader('speech_setup', str(HELPER))
        spec = importlib.util.spec_from_loader('speech_setup', loader)
        self.helper = importlib.util.module_from_spec(spec)
        loader.exec_module(self.helper)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name) / 'data with spaces'
        self.root = self.data / 'codex-notification-speech'
        self.model = self.root / 'voices/en_US-Voice Contributor-high.onnx'
        self.config = self.model.with_suffix('.onnx.json')
        self.python = self.root / 'venv/bin/python'
        self.env = patch.dict(os.environ, {'XDG_DATA_HOME': str(self.data)})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.calls = []
        self.version = '1.8.0'

    def installed_files(self):
        self.python.parent.mkdir(parents=True)
        self.python.write_text('#!/bin/sh\n', encoding='utf-8')
        self.python.chmod(0o700)
        self.model.parent.mkdir(parents=True)
        self.model.write_bytes(b'onnx fixture')
        self.config.write_text(json.dumps({'audio': {'sample_rate': 22050}}), encoding='utf-8')

    def dependency(self, argv, **kwargs):
        self.calls.append((argv, kwargs))
        if '-c' in argv:
            return SimpleNamespace(returncode=0, stdout=self.version + '\n', stderr='')
        if 'venv' in argv:
            self.python.parent.mkdir(parents=True, exist_ok=True)
            self.python.write_text('#!/bin/sh\n', encoding='utf-8')
            self.python.chmod(0o700)
        elif 'piper.download_voices' in argv:
            directory = Path(argv[argv.index('--data-dir') + 1])
            self.assertEqual(argv[3], 'en_US-Voice Contributor-high')
            self.assertTrue(directory.is_relative_to(self.root))
            (directory / 'en_US-Voice Contributor-high.onnx').write_bytes(b'onnx fixture')
            (directory / 'en_US-Voice Contributor-high.onnx.json').write_text(json.dumps({'audio': {'sample_rate': 22050}}), encoding='utf-8')
        elif 'piper' in argv:
            self.assertEqual(argv[argv.index('--model') + 1], str(self.model))
            self.assertEqual(argv[argv.index('--config') + 1], str(self.config))
            self.assertEqual(argv[argv.index('--length-scale') + 1], '0.95')
            self.assertEqual(kwargs['timeout'], 30)
            self.assertIsInstance(kwargs['input'], str)
            self.assertNotIn(kwargs['input'], argv)
            destination = argv[argv.index('--output-file') + 1]
            with wave.open(destination, 'wb') as audio:
                audio.setnchannels(1)
                audio.setsampwidth(2)
                audio.setframerate(22050)
                audio.writeframes(b'\0\0' * 200)
        return SimpleNamespace(returncode=0, stdout='', stderr='')

    def run_helper(self, command, dependency=None):
        self.output = io.StringIO()
        self.errors = io.StringIO()
        with contextlib.redirect_stdout(self.output), contextlib.redirect_stderr(self.errors), patch.object(self.helper.subprocess, 'run', side_effect=dependency or self.dependency):
            return self.helper.main([command])

    def test_plain_and_details_control_setup_diagnostics(self):
        self.installed_files()
        for args, detailed in ((['--check'], False), (['--check', '--plain', '--details'], True)):
            output = io.StringIO()
            with contextlib.redirect_stdout(output), patch.object(self.helper.subprocess, 'run', side_effect=self.dependency):
                self.assertEqual(self.helper.main(args), 0)
            text = output.getvalue()
            self.assertIn('ready', text.lower())
            self.assertEqual(str(self.model) in text, detailed)
            if detailed:
                self.assertTrue(text.isascii())
            else:
                self.assertIn('✅', text)

    def test_check_missing_is_actionable_and_read_only(self):
        self.assertEqual(self.run_helper('--check'), 1)
        self.assertIn('--install', self.errors.getvalue())
        self.assertFalse(self.root.exists())
        self.assertEqual(self.calls, [])

    def test_check_proves_offline_synthesis_and_cleans_wav(self):
        self.installed_files()
        before = sorted(path.relative_to(self.root) for path in self.root.rglob('*'))
        self.assertEqual(self.run_helper('--check'), 0)
        self.assertIn('ready', self.output.getvalue().lower())
        self.assertIn('Voice Contributor high', self.output.getvalue())
        self.assertEqual(sorted(path.relative_to(self.root) for path in self.root.rglob('*')), before)
        self.assertEqual(len(self.calls), 2)
        self.assertTrue(all(call[0][0] == str(self.python) for call in self.calls))

    def test_check_rejects_wrong_version(self):
        self.installed_files()
        self.version = '1.7.0'
        self.assertEqual(self.run_helper('--check'), 1)
        self.assertIn('1.8.0', self.errors.getvalue())
        self.assertEqual(len(self.calls), 1)

    def test_check_rejects_corrupt_config_before_synthesis(self):
        self.installed_files()
        self.config.write_text('[]', encoding='utf-8')
        self.assertEqual(self.run_helper('--check'), 1)
        self.assertIn('config', self.errors.getvalue().lower())
        self.assertEqual(self.calls, [])

    def test_check_timeout_is_actionable_and_cleans_wav(self):
        self.installed_files()
        def timeout(argv, **kwargs):
            if 'piper' in argv:
                raise subprocess.TimeoutExpired(argv, 30)
            return self.dependency(argv, **kwargs)
        self.assertEqual(self.run_helper('--check', timeout), 1)
        self.assertIn('--install', self.errors.getvalue())
        self.assertFalse(list(self.root.rglob('*.wav')))

    def test_install_pins_piper_and_keeps_downloads_in_xdg_data(self):
        self.assertEqual(self.run_helper('--install'), 0)
        self.assertTrue(self.model.is_file())
        self.assertTrue(self.config.is_file())
        pip_calls = [(argv, options) for argv, options in self.calls if 'pip' in argv]
        self.assertEqual(len(pip_calls), 1)
        argv, options = pip_calls[0]
        self.assertEqual(argv[0], str(self.python))
        self.assertIn('piper-tts==1.8.0', argv)
        self.assertTrue(Path(options['env']['PIP_CACHE_DIR']).is_relative_to(self.root))
        self.assertTrue(Path(options['env']['TMPDIR']).is_relative_to(self.root))
        self.assertFalse(list(self.root.glob('voice-download-*')))
        self.assertIn('ready', self.output.getvalue().lower())


if __name__ == '__main__':
    unittest.main()
