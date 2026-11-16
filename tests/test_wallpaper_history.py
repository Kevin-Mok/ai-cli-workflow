"""Wallpaper history CLI and wrapper integration, isolated from live settings."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/executable_wallpaper-history'
WRAPPER = ROOT / 'scripts/executable_apply-pywal-theme'


class WallpaperHistoryTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.cache = self.home / 'custom-cache'
        self.cache.mkdir()
        self.env = dict(os.environ, HOME=str(self.home),
                        XDG_STATE_HOME=str(self.home / 'state'),
                        PYWAL_CACHE_DIR=str(self.cache), CLI_PLAIN='1')
        self.history = self.home / 'state/wallpaper-history/history.jsonl'

    def run_cli(self, *args):
        return subprocess.run(['python3', str(SCRIPT), *args], env=self.env,
                              capture_output=True, text=True)

    def record(self, wallpaper):
        (self.cache / 'colors.json').write_text(json.dumps({'wallpaper': wallpaper}))
        result = self.run_cli('--record')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')
        self.assertEqual(result.stderr, '')

    def test_empty_history_does_not_create_state(self):
        result = self.run_cli('--plain')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('No wallpaper history', result.stdout)
        self.assertFalse(self.history.exists())

    def test_record_order_duplicates_spaces_and_private_state(self):
        first = str(self.home / 'first wallpaper.png')
        second = str(self.home / 'second.png')
        for wallpaper in (first, first, second, first):
            self.record(wallpaper)
        records = [json.loads(line) for line in self.history.read_text().splitlines()]
        self.assertEqual([item['wallpaper'] for item in records], [first, second, first])
        self.assertEqual(self.history.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.history.parent.stat().st_mode & 0o777, 0o700)
        result = self.run_cli('--plain')
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.splitlines()
        self.assertTrue(lines[-3].endswith(first), lines)
        self.assertTrue(lines[-2].endswith(second), lines)
        self.assertTrue(lines[-1].endswith(first), lines)
        self.assertRegex(lines[-1], r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
        self.assertTrue(result.stdout.isascii())

    def test_default_home_state_and_decorated_heading(self):
        self.env.pop('XDG_STATE_HOME')
        self.record('/pictures/one.png')
        self.assertTrue((self.home / '.local/state/wallpaper-history/history.jsonl').is_file())
        self.env.pop('CLI_PLAIN')
        self.assertIn('🖼', self.run_cli().stdout)

    def test_invalid_cache_is_actionable_and_does_not_record(self):
        for content in ('{}', '{', '[]', '{"wallpaper":""}', '{"wallpaper":3}'):
            with self.subTest(content=content):
                (self.cache / 'colors.json').write_text(content)
                result = self.run_cli('--record')
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(str(self.cache / 'colors.json'), result.stderr)
                self.assertFalse(self.history.exists())

    def test_invalid_history_is_not_silently_replaced(self):
        self.history.parent.mkdir(parents=True)
        for content in ('broken\n', '{"timestamp":"yesterday","wallpaper":"/one"}\n',
                        '{"timestamp":"2026-11-16T12:00:00+00:00","wallpaper":4}\n'):
            with self.subTest(content=content):
                self.history.write_text(content)
                (self.cache / 'colors.json').write_text('{"wallpaper":"/two"}')
                for args in ((), ('--record',)):
                    result = self.run_cli(*args)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(str(self.history), result.stderr)
                self.assertEqual(self.history.read_text(), content)

    def test_record_preserves_valid_final_line_without_newline(self):
        self.history.parent.mkdir(parents=True)
        self.history.write_text(json.dumps({'timestamp': '2026-11-16T12:00:00+00:00',
                                            'wallpaper': '/pictures/first.png'}))
        self.record('/pictures/second.png')
        records = [json.loads(line) for line in self.history.read_text().splitlines()]
        self.assertEqual([item['wallpaper'] for item in records],
                         ['/pictures/first.png', '/pictures/second.png'])

    def wrapper(self, exit_code=0):
        scripts = self.home / 'scripts'
        scripts.mkdir(exist_ok=True)
        shutil.copy(WRAPPER, scripts / 'apply-pywal-theme')
        if SCRIPT.exists():
            shutil.copy(SCRIPT, scripts / 'wallpaper-history')
        (scripts / 'pywal-readable').write_text(
            'import sys\n'
            f'sys.exit({exit_code})\n')
        for name in ('xrdb', 'kitty', 'i3-msg'):
            stub = scripts / name
            stub.write_text('#!/bin/sh\nexit 0\n')
            stub.chmod(0o700)
        env = dict(self.env, PATH=str(scripts) + ':' + self.env['PATH'])
        return subprocess.run(['bash', str(scripts / 'apply-pywal-theme'), '-R'],
                              env=env, capture_output=True, text=True)

    def test_successful_wrapper_records_effective_cache_wallpaper(self):
        (self.cache / 'colors.json').write_text('{"wallpaper":"/pictures/restored.png"}')
        result = self.wrapper()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.history.exists(), 'successful application must record history')
        self.assertEqual(json.loads(self.history.read_text())['wallpaper'], '/pictures/restored.png')

    def test_failed_wrapper_does_not_record_stale_cache(self):
        (self.cache / 'colors.json').write_text('{"wallpaper":"/pictures/stale.png"}')
        result = self.wrapper(exit_code=7)
        self.assertEqual(result.returncode, 7)
        self.assertFalse(self.history.exists())

    def test_history_io_failure_warns_without_failing_application(self):
        (self.cache / 'colors.json').write_text('{"wallpaper":"/pictures/one.png"}')
        (self.home / 'state').write_text('cannot create directory here')
        result = self.wrapper()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('wallpaper history', result.stderr.lower())
        self.assertIn('applied', result.stderr.lower())


if __name__ == '__main__':
    unittest.main()
