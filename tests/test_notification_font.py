#!/usr/bin/env python3
"""Exercise the comparison CLI without sending real desktop notifications."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/executable_notification-font-test"

class NotificationFontTest(unittest.TestCase):
    def test_global_font_increase(self):
        import configparser
        config = configparser.ConfigParser(interpolation=None, strict=False)
        config.read(ROOT / "dot_config/dunst/dunstrc")
        self.assertEqual(config["global"]["font"], "Hack Nerd Font Mono 23.25")
        self.assertEqual(config["global"]["width"], "467")
        self.assertEqual(config["global"]["height"], "600")
        self.assertNotIn("geometry", config["global"])
        self.assertNotIn("notification_height", config["global"])

    def run_sample(self, *args):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = root / "calls.jsonl"
            fake = root / "notify-send"
            fake.write_text("#!" + sys.executable + "\nimport json,os,sys\nwith open(os.environ['NOTIFICATION_TEST_LOG'], 'a') as stream: stream.write(json.dumps(sys.argv[1:]) + '\\n')\n")
            fake.chmod(0o755)
            result = subprocess.run([sys.executable, str(SCRIPT), *args], env={**os.environ, "PATH": str(root) + os.pathsep + os.environ["PATH"], "NOTIFICATION_TEST_LOG": str(log)}, capture_output=True, text=True)
            calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
            return result, calls

    def test_default_sends_both_comparisons(self):
        result, calls = self.run_sample()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([call[call.index("--app-name") + 1] for call in calls], ["Codex", "Discord"])
        for call in calls:
            self.assertNotIn('size="8192"', call[-1])
            self.assertNotIn('Before', call[-1])
            self.assertIn("--expire-time=15000", call)
        self.assertIn("✅", result.stdout)
        self.assertIn("23.25 pt", result.stdout)

    def test_explicit_old_new_comparison(self):
        result, calls = self.run_sample("--compare", "--app", "codex")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(calls), 1)
        self.assertIn('size="23808"', calls[0][-1])
        self.assertIn('size="15872"', calls[0][-1])

    def test_single_plain_sample(self):
        result, calls = self.run_sample("--app", "discord", "--plain")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(calls), 1)
        self.assertIn("Discord", calls[0])
        self.assertTrue(result.stdout.isascii())

    def test_help_sends_nothing(self):
        result, calls = self.run_sample("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, [])
        self.assertIn("--app", result.stdout)

if __name__ == "__main__":
    unittest.main()
