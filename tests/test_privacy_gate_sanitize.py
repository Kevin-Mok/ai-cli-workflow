#!/usr/bin/env python3
"""Disposable-repository checks for `privacy-gate sanitize`.

Only obviously fake synthetic values are used; captured output is never attached
to assertion messages.
"""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts" / "executable_privacy-gate"
FAKE_AWS = "AKIA" + "IOSFODNN7EXAMPLE"
FAKE_EMAIL = "fake.person" + "@" + "corp-example.org"
FAKE_HOME = "/home/" + "fakeuser/project"
FAKE_IP = "10.20" + ".30.40"
SECRETS = (FAKE_AWS, FAKE_EMAIL, "fakeuser", FAKE_IP, "hunter2fakepass")


class SanitizeTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        base = Path(self.directory.name)
        self.repo = base / "repo"
        self.repo.mkdir()
        (base / "home").mkdir()
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(HOME=str(base / "home"), XDG_CONFIG_HOME=str(base / "home/.config"), GIT_CONFIG_NOSYSTEM="1")
        self.git("init", "-q")
        self.git("config", "user.name", "Example Maintainer")
        self.git("config", "user.email", "maintainer@example.invalid")
        self.write("README.md", "hello\n")
        self.write("config.env.sh", f"export AWS_KEY={FAKE_AWS}\npassword=hunter2fakepass\ncontact {FAKE_EMAIL}\ncd {FAKE_HOME}\nssh {FAKE_IP}\n")
        self.write("NIGHT_NOTE.md", "private notes\n")
        self.git("add", "-A")

    def run_cmd(self, command):
        return subprocess.run(command, cwd=self.repo, env=self.env, capture_output=True, text=True)

    def git(self, *args):
        result = self.run_cmd(["git", *args])
        self.assertEqual(result.returncode, 0, "git fixture failed (output suppressed)")
        return result.stdout

    def gate(self, *args):
        return self.run_cmd([sys.executable, str(GATE), *args, "--repo", str(self.repo), "--plain"])

    def write(self, name, text):
        (self.repo / name).write_text(text, encoding="utf-8")

    def assert_no_secrets(self, text):
        for value in SECRETS:
            self.assertNotIn(value, text, "secret leaked (value suppressed)")

    def snapshot(self):
        files = {p.relative_to(self.repo).as_posix(): p.read_bytes() for p in self.repo.rglob("*") if p.is_file() and ".git" not in p.parts}
        return files, self.git("ls-files", "--stage")

    def test_gate_blocks_before_sanitize(self):
        self.assertEqual(self.gate("check").returncode, 1)

    def test_dry_run_changes_nothing_and_masks(self):
        before = self.snapshot()
        result = self.gate("sanitize")
        self.assertEqual(result.returncode, 0)
        self.assertIn("DRY-RUN", result.stdout)
        self.assertIn("NIGHT_NOTE.md", result.stdout)
        self.assert_no_secrets(result.stdout + result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_apply_ignores_redacts_and_passes_scan(self):
        result = self.gate("sanitize", "--apply")
        self.assert_no_secrets(result.stdout + result.stderr)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Re-scan of staged candidate: clean", result.stdout)
        tracked = self.git("ls-files").split()
        # Private file ignored and untracked, working copy kept.
        self.assertNotIn("NIGHT_NOTE.md", tracked)
        self.assertTrue((self.repo / "NIGHT_NOTE.md").exists())
        self.assertIn("/NIGHT_NOTE.md", (self.repo / ".gitignore").read_text())
        # Value file: original untracked+ignored, sanitized copy tracked.
        self.assertNotIn("config.env.sh", tracked)
        self.assertIn("config.env.sh.example", tracked)
        self.assertIn(FAKE_AWS, (self.repo / "config.env.sh").read_text())
        example = (self.repo / "config.env.sh.example").read_text()
        for placeholder in ("<REDACTED_TOKEN>", "<API_KEY>", "<EMAIL>", "$HOME", "<IP_ADDRESS>"):
            self.assertIn(placeholder, example)
        self.assert_no_secrets(example)
        mapping = (self.repo / "SANITIZED.md").read_text()
        self.assertIn("<REDACTED_TOKEN>", mapping)
        self.assert_no_secrets(mapping)
        self.assertEqual(self.gate("check").returncode, 0)

    def test_exclude_keeps_gitignore_clean(self):
        self.assertEqual(self.gate("sanitize", "--apply", "--exclude").returncode, 0)
        self.assertFalse((self.repo / ".gitignore").exists())
        self.assertIn("/NIGHT_NOTE.md", (self.repo / ".git/info/exclude").read_text())


if __name__ == "__main__":
    unittest.main()
