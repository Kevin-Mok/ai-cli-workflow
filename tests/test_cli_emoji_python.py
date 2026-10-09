"""Human output is decorated while explicit plain output stays consumable."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class PythonEmojiTests(unittest.TestCase):
    def run_cli(self, script, *args, plain=False):
        env = dict(os.environ)
        env.pop('CLI_PLAIN', None)
        if plain:
            env['CLI_PLAIN'] = '1'
        return subprocess.run([sys.executable, str(ROOT / 'scripts' / script), *args], env=env, capture_output=True, text=True)

    def test_file_size_results_and_errors_have_icons_and_plain_escape(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, 'sample').write_text('abc')
            result = self.run_cli('executable_largest-day-file-size', folder)
            self.assertEqual(result.returncode, 0)
            self.assertTrue(result.stdout.startswith('📅 '), result.stdout)
            plain = self.run_cli('executable_largest-day-file-size', folder, plain=True)
            self.assertEqual(result.stdout.removeprefix('📅 '), plain.stdout)
            missing = self.run_cli('executable_largest-day-file-size', folder + '/missing')
            self.assertEqual(missing.returncode, 1)
            self.assertTrue(missing.stderr.startswith('❌ '), missing.stderr)

    def test_concat_failure_is_human_facing_without_altering_exit_status(self):
        with tempfile.TemporaryDirectory() as folder:
            result = self.run_cli('executable_concat-timestamped-videos', folder, folder + '/out.mp4')
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(result.stderr.startswith('❌ '), result.stderr)
            plain = self.run_cli('executable_concat-timestamped-videos', folder, folder + '/out.mp4', plain=True)
            self.assertEqual(result.stderr.removeprefix('❌ '), plain.stderr)

    def test_redshift_smoke_success_and_plain_escape(self):
        result = self.run_cli('smoke_redshift_keys.py', str(ROOT / 'dot_config/i3/config.tmpl'))
        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.stdout.startswith('✅ PASS:'), result.stdout)
        plain = self.run_cli('smoke_redshift_keys.py', str(ROOT / 'dot_config/i3/config.tmpl'), plain=True)
        self.assertEqual(result.stdout.removeprefix('✅ '), plain.stdout)

    def test_python_help_has_decorated_description_and_plain_escape(self):
        result = self.run_cli('executable_largest-day-file-size', '--help')
        self.assertEqual(result.returncode, 0)
        self.assertIn('📅 Show the top three', result.stdout)
        plain = self.run_cli('executable_largest-day-file-size', '--help', plain=True)
        self.assertEqual(plain.returncode, 0)
        self.assertTrue(plain.stdout.isascii())
        self.assertIn('Show the top three', plain.stdout)

    def test_workflow_doctor_json_stays_machine_readable(self):
        with tempfile.TemporaryDirectory() as folder:
            result = self.run_cli('executable_ai-workflow-doctor', '--repo', folder, '--format', 'json')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('summary', json.loads(result.stdout))
            plain = self.run_cli('executable_ai-workflow-doctor', '--repo', folder, '--format', 'json', plain=True)
            self.assertEqual(result.stdout, plain.stdout)

    def test_existing_voice_presentation_honors_plain_environment(self):
        result = self.run_cli('executable_codex-voice-auditions', '--list')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith('🎙️ '))
        plain = self.run_cli('executable_codex-voice-auditions', '--list', plain=True)
        self.assertEqual(plain.returncode, 0, plain.stderr)
        self.assertTrue(plain.stdout.isascii(), plain.stdout)
        self.assertIn('Ten local voice alternatives', plain.stdout)

    def test_second_brain_doctor_text_renderer_respects_plain_environment(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        from second_brain.doctor import text_report
        report = {'summary': {'status': 'ok', 'errors': 0, 'warnings': 0}, 'findings': []}
        previous = os.environ.pop('CLI_PLAIN', None)
        try:
            self.assertTrue(text_report(report).startswith('🩺 '))
            os.environ['CLI_PLAIN'] = '1'
            self.assertTrue(text_report(report).startswith('Second Brain doctor:'))
        finally:
            os.environ.pop('CLI_PLAIN', None)
            if previous is not None:
                os.environ['CLI_PLAIN'] = previous

if __name__ == '__main__':
    unittest.main()
