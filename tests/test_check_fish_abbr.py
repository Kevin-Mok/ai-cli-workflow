"""Verify the local expansion CLI through real interactive fish, without executing mappings."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'scripts/executable_check-fish-abbr'

class CheckFishAbbrTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='abbr-check-')
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.catalog = self.home / '.config/fish/key_abbr.fish'
        self.catalog.parent.mkdir(parents=True)
        self.catalog.write_text('')

    def run_cli(self, *args):
        return subprocess.run(['python3', str(CLI), '--plain', *args],
                              env={**os.environ, 'HOME': str(self.home)},
                              capture_output=True, text=True, timeout=15)

    def test_temporary_trial_and_cleanup_preserve_catalog(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('removed', result.stdout)
        self.assertEqual(self.catalog.read_text(), '')

    def test_literal_expansion_never_executes_mapped_command(self):
        sentinel = self.home / 'must-not-exist'
        expansion = f'touch {sentinel}; echo $(whoami)'
        self.catalog.write_text(f"abbr --add trial '{expansion}'\n")
        result = self.run_cli('trial', expansion)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(sentinel.exists())
        self.assertNotIn('removed', result.stdout)

    def test_wrong_expected_expansion_fails(self):
        self.catalog.write_text("abbr --add trial 'cd /tmp'\n")
        result = self.run_cli('trial', 'cd /wrong')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('expansion', result.stderr.lower())

    def test_missing_abbreviation_fails(self):
        result = self.run_cli('absent', 'cd /tmp')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('absent', result.stderr)

if __name__ == '__main__':
    unittest.main()
