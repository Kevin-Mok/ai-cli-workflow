#!/usr/bin/env python3
"""Exercise skill-helper messages without network calls or privileged actions."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(relative):
    spec = importlib.util.spec_from_file_location('emoji_skill_' + Path(relative).stem, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SkillOutputTests(unittest.TestCase):
    def test_api_warnings_have_default_emoji_and_plain_escape(self):
        for relative in ('imagegen/scripts/image_gen.py', 'transcribe/scripts/transcribe_diarize.py'):
            module = load('dot_agents/skills/' + relative)
            for plain in (False, True):
                with self.subTest(helper=relative, plain=plain), patch.dict(os.environ, {'CLI_PLAIN': '1' if plain else '0'}):
                    out = io.StringIO()
                    with contextlib.redirect_stderr(out):
                        module._warn('dry-run only')
                    self.assertEqual(out.getvalue(), ('' if plain else '⚠️ ') + 'Warning: dry-run only\n')

    def test_check_report_is_decorated_and_plain_preserves_text(self):
        module = load('dot_agents/skills/gh-fix-ci/scripts/inspect_pr_checks.py')
        result = [{'name': 'unit', 'status': 'failure', 'note': 'Inspect failing check'}]
        for plain in (False, True):
            with self.subTest(plain=plain), patch.dict(os.environ, {'CLI_PLAIN': '1' if plain else '0'}):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    module.render_results('7', result)
                text = out.getvalue()
                self.assertIn(('' if plain else '🔎 ') + 'PR #7: 1 failing checks analyzed.', text)
                self.assertIn('Check: unit', text)
                if plain:
                    self.assertTrue(text.isascii())

    def test_skill_help_has_emoji_and_plain_escape(self):
        for relative in ('imagegen/scripts/image_gen.py', 'transcribe/scripts/transcribe_diarize.py', 'gh-fix-ci/scripts/inspect_pr_checks.py', 'screenshot/scripts/take_screenshot.py', 'metaprompt/scripts/update_upstream.py', 'leetcode-init/scripts/init_leetcode_problem.py'):
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

    def test_image_dry_run_stdout_remains_json(self):
        helper = ROOT / 'dot_agents/skills/imagegen/scripts/image_gen.py'
        env = dict(os.environ)
        env.pop('OPENAI_API_KEY', None)
        proc = subprocess.run([sys.executable, str(helper), 'generate', '--prompt', 'a blue circle', '--dry-run'], env=env, text=True, capture_output=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload['endpoint'], '/v1/images/generations')
        self.assertIn('⚠️', proc.stderr)

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
