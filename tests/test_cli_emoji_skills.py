#!/usr/bin/env python3
"""Exercise skill-helper messages without network calls or privileged actions."""
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SkillOutputTests(unittest.TestCase):
    def test_skill_help_has_emoji_and_plain_escape(self):
        for relative in ('metaprompt/scripts/update_upstream.py',):
            helper = ROOT / 'dot_agents/skills' / relative
            default = subprocess.run([sys.executable, str(helper), '--help'], env=dict(os.environ, CLI_PLAIN='0'), text=True, capture_output=True)
            plain = subprocess.run([sys.executable, str(helper), '--help'], env=dict(os.environ, CLI_PLAIN='1'), text=True, capture_output=True)
            with self.subTest(helper=relative):
                self.assertEqual(default.returncode, 0, default.stderr)
                self.assertEqual(plain.returncode, 0, plain.stderr)
                self.assertIn('📖', default.stdout)
                self.assertNotIn('📖', plain.stdout)
                self.assertIn('usage:', plain.stdout)
    def test_benchmark_cli_help_has_plain_escape(self):
        for name in ('metaprompt-benchmark.py', 'metaprompt-selection.py'):
            helper = ROOT / 'scripts' / name
            for plain in (False, True):
                with self.subTest(helper=name, plain=plain):
                    result = subprocess.run([sys.executable, str(helper), '--help'], env=dict(os.environ, CLI_PLAIN='1' if plain else '0'), text=True, capture_output=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual('📖' in result.stdout, not plain)

    def test_playwright_missing_dependency_error_has_plain_escape(self):
        helper = ROOT / 'dot_agents/skills/playwright/scripts/playwright_cli.sh'
        for plain in (False, True):
            env = dict(os.environ, PATH='/nonexistent', CLI_PLAIN='1' if plain else '0')
            proc = subprocess.run(['/bin/bash', str(helper), '--help'], env=env, text=True, capture_output=True)
            self.assertEqual(proc.returncode, 1)
            self.assertEqual(proc.stdout, '')
            self.assertEqual(proc.stderr, ('' if plain else '❌ ') + 'Error: npx is required but not found on PATH.\n')


if __name__ == '__main__':
    unittest.main()
