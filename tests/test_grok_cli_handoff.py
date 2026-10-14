"""Exercise the shared handoff CLI against disposable Git checkouts."""

import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "dot_agents/skills/grok-cli-handoff"
HELPER = SKILL / "scripts/handoff.py"


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(HELPER.is_file(), "shared handoff CLI is missing")
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo with spaces"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "fixture", str(self.repo)], check=True)

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(HELPER), *map(str, args)],
                              capture_output=True, text=True)

    def preflight(self, *args):
        return self.run_cli("--plain", "preflight", "--repo", self.repo,
                            "--branch", "fixture", "--task", "example", *args)

    def test_clear_checkout_is_read_only_and_does_not_authorize(self):
        before = sorted(p.relative_to(self.repo) for p in self.repo.rglob("*"))
        result = self.preflight()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ready:", result.stdout)
        self.assertIn("not authorization", result.stdout)
        self.assertEqual(before, sorted(p.relative_to(self.repo) for p in self.repo.rglob("*")))

    def test_project_stop_prevents_launch_without_reading_payload(self):
        marker = self.repo / ".harness/STOP"
        marker.parent.mkdir()
        marker.write_text("FAKE_SECRET_MUST_NOT_BE_PRINTED")
        result = self.preflight()
        self.assertEqual(result.returncode, 3)
        self.assertIn("Stopped:", result.stderr)
        self.assertNotIn("FAKE_SECRET", result.stdout + result.stderr)

    def test_task_stop_is_scoped(self):
        marker = self.repo / ".harness/other/STOP"
        marker.parent.mkdir(parents=True)
        marker.touch()
        self.assertEqual(self.preflight().returncode, 0)
        result = self.preflight("--task", "other")
        self.assertEqual(result.returncode, 3)

    def test_directory_and_dangling_symlink_markers_stop(self):
        marker = self.repo / ".harness/STOP"
        marker.parent.mkdir()
        marker.mkdir()
        self.assertEqual(self.preflight().returncode, 3)
        marker.rmdir()
        marker.symlink_to(self.repo / "absent")
        self.assertEqual(self.preflight().returncode, 3)

    def test_symlinked_harness_marker_stops(self):
        outside = Path(self.tmp.name) / "markers"
        outside.mkdir()
        (outside / "STOP").touch()
        (self.repo / ".harness").symlink_to(outside, target_is_directory=True)
        self.assertEqual(self.preflight().returncode, 3)

    def test_wrong_branch_fails_closed(self):
        result = self.preflight("--branch", "wrong")
        self.assertEqual(result.returncode, 2)
        self.assertIn("branch mismatch", result.stderr)

    def test_subdirectory_is_not_an_accepted_checkout(self):
        nested = self.repo / "nested"
        nested.mkdir()
        result = self.preflight("--repo", nested)
        self.assertEqual(result.returncode, 2)
        self.assertIn("checkout root", result.stderr)

    def test_non_git_directory_and_missing_directory_fail_closed(self):
        for path in (Path(self.tmp.name), Path(self.tmp.name) / "missing"):
            with self.subTest(path=path):
                result = self.preflight("--repo", path)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("Traceback", result.stderr)

    def test_invalid_task_cannot_escape_task_directory(self):
        for task in ("../escape", "UPPER", "", "a/b", "a\nSTOP", "x" * 65):
            with self.subTest(task=task):
                self.assertEqual(self.preflight("--task", task).returncode, 2)

    def test_default_output_has_emoji_and_plain_output_is_ascii(self):
        result = self.run_cli("preflight", "--repo", self.repo,
                              "--branch", "fixture", "--task", "example")
        self.assertEqual(result.returncode, 0)
        self.assertIn("✅", result.stdout)
        self.assertTrue(self.preflight().stdout.isascii())
        for args in (("--help",), ("--plain", "--help")):
            result = self.run_cli(*args)
            self.assertEqual(result.returncode, 0)
            self.assertEqual("🧭" in result.stdout, "--plain" not in args)

    def test_usage_errors_have_emoji_and_plain_escape(self):
        result = self.run_cli("template", "--task", "../escape")
        self.assertEqual(result.returncode, 2)
        self.assertIn("⚠️", result.stderr)
        result = self.run_cli("--plain", "template", "--task", "../escape")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("⚠️", result.stderr)

    def test_git_environment_cannot_redirect_checkout(self):
        env = os.environ.copy()
        env["GIT_WORK_TREE"] = self.tmp.name
        env["GIT_DIR"] = str(self.repo / ".git")
        result = subprocess.run([sys.executable, str(HELPER), "--plain", "preflight",
                                 "--repo", str(self.repo), "--branch", "fixture",
                                 "--task", "example"], env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_claude_hook_preserves_and_exposes_complete_skill(self):
        home = Path(self.tmp.name) / "home"
        skill_path = home / ".agents/skills/grok-cli-handoff"
        shutil.copytree(SKILL, skill_path)
        hook = (ROOT / "run_after_install-claude-skills.sh.tmpl").read_text()
        subprocess.run(["bash"], input=hook.replace("{{ .chezmoi.homeDir }}", str(home)),
                       text=True, check=True)
        installed = home / ".claude/skills/grok-cli-handoff"
        self.assertTrue(installed.is_symlink())
        result = subprocess.run([sys.executable, str(installed / "scripts/handoff.py"),
                                 "template", "--task", "installed"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Grok CLI handoff: installed", result.stdout)

    def test_template_preserves_machine_readable_markdown_and_task_id(self):
        result = self.run_cli("template", "--task", "example")
        plain = self.run_cli("--plain", "template", "--task", "example")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, plain.stdout)
        self.assertTrue(result.stdout.startswith("# Grok CLI handoff: example"))
        for required in ("Authorization", "Sender host", "Receiver host", "Repo root",
                         "Branch", "Protected state", "Evidence", "Next owner",
                         ".harness/example/STOP", ".harness/STOP"):
            self.assertIn(required, result.stdout)


if __name__ == "__main__":
    unittest.main()
