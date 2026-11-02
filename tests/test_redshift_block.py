"""Exercise the real controller and block with an isolated saved state/backend."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTROLLER = ROOT / 'scripts/executable_redshift-control'
BLOCK = ROOT / 'dot_config/i3blocks/scripts/executable_redshift'


class RedshiftBlock(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        (self.home / 'scripts').mkdir()
        (self.home / 'scripts/redshift-control').symlink_to(CONTROLLER)
        self.bin = self.home / 'bin'
        self.bin.mkdir()
        for name, body in {'redshift': 'exit "${FAIL_BACKEND:-0}"',
                           'notify-send': 'echo notify >> "$NOTIFICATION_LOG"; echo 1'}.items():
            path = self.bin / name
            path.write_text('#!/bin/sh\n' + body + '\n')
            path.chmod(0o755)
        self.env = {**os.environ, 'HOME': str(self.home), 'XDG_STATE_HOME': str(self.home / 'state'),
                    'PATH': str(self.bin) + ':' + os.environ['PATH'],
                    'NOTIFICATION_LOG': str(self.home / 'notifications')}
        self.state = self.home / 'state/redshift/temperature'

    def controller(self, *args):
        return subprocess.run([str(CONTROLLER), *args], env=self.env, capture_output=True, text=True)

    def block(self, button=''):
        return subprocess.run([str(BLOCK)], env={**self.env, 'BLOCK_BUTTON': button},
                              capture_output=True, text=True)

    def test_pywal_color_and_safe_fallback(self):
        colors = self.home / '.cache/wal/colors.sh'
        colors.parent.mkdir(parents=True)
        for palette, expected in [("color7='#bbaacc'\nexit 99\n", '#bbaacc'),
                                  ('color7="invalid"\n', '#cbe4ff'),
                                  ('', '#cbe4ff')]:
            with self.subTest(palette=palette):
                colors.write_text(palette)
                result = self.block()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.splitlines(), ['🌡️6500 K', '', expected])

    def test_status_without_state_is_read_only(self):
        result = self.controller('status')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '6500\n')
        self.assertFalse((self.home / 'state').exists())

    def test_wheel_updates_without_notification_but_direct_commands_notify(self):
        self.assertEqual(self.controller('set', '4500').returncode, 0)
        notifications = self.home / 'notifications'
        before = notifications.read_text()
        self.assertIn('4650 K', self.block('4').stdout)
        self.assertEqual(notifications.read_text(), before)
        self.assertIn('4500 K', self.block('5').stdout)
        self.assertEqual(notifications.read_text(), before)
        self.assertEqual(self.controller('adjust', '150').returncode, 0)
        self.assertEqual(notifications.read_text(), before + 'notify\n')

    def test_status_never_calls_backend_or_writes_existing_state(self):
        self.controller('set', '4500')
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.state.parent.iterdir()}
        for path in self.bin.iterdir():
            path.write_text('#!/bin/sh\nexit 99\n')
        result = self.controller('status')
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, '4500\n', ''))
        self.assertEqual(before, {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.state.parent.iterdir()})

    def test_wheels_presets_reset_bounds_and_ignored_buttons(self):
        self.assertEqual(self.block().stdout, '🌡️6500 K\n\n#cbe4ff\n')
        self.assertFalse(self.state.exists())
        self.controller('set', '4500')
        self.assertEqual(self.block('4').stdout, '🌡️4650 K\n\n#cbe4ff\n')
        self.assertEqual(self.block('5').stdout, '🌡️4500 K\n\n#cbe4ff\n')
        for button in ('1', '2', '3', '6', ''):
            self.assertEqual(self.block(button).stdout, '🌡️4500 K\n\n#cbe4ff\n')
        self.controller('set', '1000')
        self.assertEqual(self.block('5').stdout, '🌡️1000 K\n\n#cbe4ff\n')
        self.controller('reset')
        self.assertEqual(self.block('4').stdout, '🌡️6500 K\n\n#cbe4ff\n')
        self.controller('set', '2100')
        self.assertEqual(self.block().stdout, '🌡️2100 K\n\n#cbe4ff\n')

    def test_rapid_scroll_accumulates(self):
        self.controller('set', '3000')
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(self.block, ['4'] * 8))
        self.assertTrue(all(r.returncode == 0 and 'ERR' not in r.stdout for r in results))
        self.assertEqual(self.controller('status').stdout, '4200\n')

    def test_invalid_state_and_backend_failure_are_compact_errors(self):
        self.controller('set', '4500')
        self.env['FAIL_BACKEND'] = '1'
        result = self.block('4')
        self.assertEqual(result.stdout, '🌡️ERR\n\n#cbe4ff\n')
        self.assertEqual(self.state.read_text(), '4500\n')
        for invalid in (b'bad', b'999', b'6501', b'\xff'):
            self.state.write_bytes(invalid)
            self.assertNotEqual(self.controller('status').returncode, 0)
            self.assertEqual(self.block().stdout, '🌡️ERR\n\n#cbe4ff\n')
            self.assertEqual(self.state.read_bytes(), invalid)


if __name__ == '__main__':
    unittest.main()
