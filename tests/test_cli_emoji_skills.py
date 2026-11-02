#!/usr/bin/env python3
"""Exercise skill-helper messages without network calls or privileged actions."""
import os
import json
import pty
import runpy
import select
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AgentOutputTests(unittest.TestCase):
    def env(self, extra=None):
        clean = {key: value for key, value in os.environ.items()
                 if not key.startswith('CODEX_') and key not in ('CLAUDECODE', 'CLI_PLAIN', 'NO_COLOR')}
        return {**clean, **(extra or {})}

    def run_output(self, command, extra=None, terminal=False):
        if not terminal:
            result = subprocess.run(command, capture_output=True, text=True, env=self.env(extra))
            return result.returncode, result.stdout, result.stderr
        master, slave = pty.openpty()
        process = subprocess.Popen(command, stdout=slave, stderr=subprocess.PIPE, env=self.env(extra))
        os.close(slave)
        chunks = []
        try:
            while True:
                self.assertTrue(select.select([master], [], [], 10)[0], 'terminal output timed out')
                try:
                    data = os.read(master, 65536)
                except OSError:
                    break
                if not data:
                    break
                chunks.append(data)
            _, error = process.communicate(timeout=10)
            return process.returncode, b''.join(chunks).decode(), error.decode()
        finally:
            os.close(master)
            if process.poll() is None:
                process.kill()
                process.wait()

    def test_real_terminal_human_agent_pipe_plain_and_no_color(self):
        commands = [
            ([sys.executable, str(ROOT / 'scripts/sync-vetted-skills'), '--check'], '📚'),
            ([sys.executable, str(ROOT / 'scripts/executable_ai-workflow-doctor'), '--help'], '🧰'),
            (['bash', str(ROOT / 'scripts/executable_readme-recruiter-sync'), '--help'], '📖'),
        ]
        modes = [(True, {}, True), (False, {}, False), (True, {'CODEX_TEST': ''}, False),
                 (True, {'CLAUDECODE': ''}, False), (True, {'CLI_PLAIN': '1'}, False),
                 (True, {'NO_COLOR': '1'}, True)]
        for command, icon in commands:
            for terminal, extra, decorated in modes:
                with self.subTest(script=command[1], terminal=terminal, env=extra):
                    code, output, error = self.run_output(command, extra, terminal)
                    self.assertEqual(code, 0, error)
                    self.assertEqual(icon in output, decorated)

    def test_inventory_summary_details_json_and_all_errors(self):
        command = [sys.executable, str(ROOT / 'scripts/sync-vetted-skills')]
        code, summary, error = self.run_output(command + ['--check', '--plain'])
        self.assertEqual(code, 0, error)
        self.assertLess(len(summary.splitlines()), 6)
        self.assertIn('--details', summary)
        code, details, error = self.run_output(command + ['--check', '--details', '--plain'])
        self.assertEqual(code, 0, error)
        self.assertIn('repo:lean-instructions', details)
        code, listing, _ = self.run_output(command + ['--plain'])
        self.assertEqual(code, 0)
        self.assertIn('repo:lean-instructions', listing)
        code, output, error = self.run_output(command + ['--check', '--json'])
        report = json.loads(output)
        self.assertEqual(code, 0, error)
        self.assertGreater(len(report['skills']), 27)
        script = ROOT / 'scripts/sync-vetted-skills'
        fixture = {'skills': [], 'errors': ['missing candidate alpha', 'stale active beta']}
        source = ("import runpy; m=runpy.run_path(" + repr(str(script)) + "); "
                  "m['main'].__globals__['audit']=lambda *args:" + repr(fixture) + "; "
                  "raise SystemExit(m['main']())")
        code, output, _ = self.run_output([sys.executable, '-c', source, '--check'])
        self.assertEqual(code, 1)
        for message in fixture['errors']:
            self.assertIn(message, output)

    def test_doctor_summary_details_plain_json_and_failure_status(self):
        files = runpy.run_path(str(ROOT / 'tests/test_ai_workflow_doctor.py'))['healthy_files']()
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            for name, content in files.items():
                target = repo / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
            (repo / 'AGENTS.md').write_text((repo / 'AGENTS.md').read_text() + '\n[broken](missing.md)\n')
            command = [sys.executable, str(ROOT / 'scripts/executable_ai-workflow-doctor'), '--repo', str(repo), '--check']
            code, summary, error = self.run_output(command + ['--plain'])
            self.assertEqual(code, 1, error)
            self.assertIn('Status: fail', summary)
            self.assertIn('Errors: 1', summary)
            self.assertIn('--details', summary)
            self.assertNotIn('target=missing.md', summary)
            code, detail, _ = self.run_output(command + ['--details', '--plain'])
            self.assertEqual(code, 1)
            self.assertIn('target=missing.md', detail)
            code, interactive, _ = self.run_output(command, terminal=True)
            self.assertEqual(code, 1)
            self.assertIn('target=missing.md', interactive)
            self.assertIn('🩺', interactive)
            code, output, _ = self.run_output(command + ['--format', 'json'])
            self.assertEqual(code, 1)
            self.assertEqual(json.loads(output)['findings'][0]['details']['target'], 'missing.md')

    def test_readme_protocol_status_and_explicit_plain(self):
        command = ['bash', str(ROOT / 'scripts/executable_readme-recruiter-sync')]
        for extra in ({}, {'CODEX_TEST': '1'}, {'CLI_PLAIN': '1'}):
            code, output, error = self.run_output(command + ['/nonexistent-readme-output-test'], extra)
            self.assertEqual(code, 2)
            self.assertEqual(output.splitlines()[0], 'blocked')
            self.assertIn('provided path is not a readable directory', output)
        code, output, error = self.run_output(command + ['--plain', '--help'], terminal=True)
        self.assertEqual(code, 0, error)
        self.assertNotIn('📖', output)


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
