"""Delivered real-fzf startup fixture with disposable, provider-free archives."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tests/scripts/codex_startup_live_check.py'


@unittest.skipUnless(shutil.which('fzf'), 'real fzf is required')
class StartupLiveFixtureTest(unittest.TestCase):
    def test_all_provider_free_actual_cli_startup_scenarios(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--scenario', 'all', '--plain'],
                                cwd=ROOT, env={**os.environ, 'CLI_PLAIN': '1'},
                                capture_output=True, text=True, timeout=40)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        for scenario in ('cold', 'cached', 'locked', 'malformed', 'malformed-details'):
            self.assertIn('PASS ' + scenario + ':', result.stdout)
        self.assertIn('Provider calls: 0; exact UUID/cwd resume; source bytes unchanged; cleanup passed.',
                      result.stdout)
        self.assertNotIn('malformed/incomplete', result.stderr)
        self.assertTrue(result.stdout.isascii(), result.stdout)


if __name__ == '__main__':
    unittest.main()
