#!/usr/bin/env python3
"""A retired installer never restores the culled external skill bundle."""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HELPER = REPO_ROOT / "scripts" / "executable_sync-superpowers-release"
SETUP = REPO_ROOT / "scripts" / "executable_setup-superpowers-release-timer"


class SuperpowersRetirementTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.log = self.root / "calls.log"
        self.log.touch()
        for name in ("chezmoi", "git", "systemctl"):
            fake = self.bin / name
            fake.write_text(
                "#!/usr/bin/env bash\n"
                "{ printf '%s' \"$0\"; printf ' %s' \"$@\"; printf '\\n'; } >> \"$TEST_CALL_LOG\"\n"
                "if [ \"${TEST_SYSTEMCTL_STATUS:-0}\" != 0 ]; then\n"
                "  printf '%s\\n' \"$TEST_SYSTEMCTL_ERROR\" >&2\n"
                "  exit \"$TEST_SYSTEMCTL_STATUS\"\n"
                "fi\n",
                encoding="utf-8",
            )
            fake.chmod(0o755)
        self.env = {
            **os.environ, "HOME": str(self.root / "missing-home"),
            "LINUX_CONFIG_SOURCE": str(self.root / "missing-source"),
            "PATH": str(self.bin) + os.pathsep + os.environ["PATH"],
            "TEST_CALL_LOG": str(self.log),
        }

    def run_script(self, script: Path, *arguments: str, **environment: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(script), *arguments], cwd=self.root,
            env={**self.env, **environment}, capture_output=True, text=True, check=False,
        )

    def test_external_bundle_exposure_and_timer_sources_are_absent(self) -> None:
        externals = (REPO_ROOT / ".chezmoiexternal.toml.tmpl").read_text()
        self.assertNotIn('".codex/superpowers"', externals)
        self.assertFalse((REPO_ROOT / "dot_agents/skills/symlink_superpowers.tmpl").exists())
        for name in ("superpowers-release-sync.service", "superpowers-release-sync.timer"):
            self.assertFalse((REPO_ROOT / "dot_config/systemd/user" / name).exists())

    def test_sync_and_dry_run_need_no_home_or_source(self) -> None:
        for arguments in ((), ("--dry-run",), ("-n",)):
            with self.subTest(arguments=arguments):
                completed = self.run_script(HELPER, *arguments)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertIn("disabled", completed.stdout)
        self.assertEqual(self.log.read_text(), "")
        self.assertFalse(Path(self.env["HOME"]).exists())

    def test_sync_preserves_an_existing_bundle_and_discovery_link(self) -> None:
        home = self.root / "existing-home"
        skills = home / ".codex/superpowers/skills"
        skills.mkdir(parents=True)
        marker = skills / "SKILL.md"
        marker.write_text("preserve upstream bytes")
        link = home / ".agents/skills/superpowers"
        link.parent.mkdir(parents=True)
        link.symlink_to(skills, target_is_directory=True)

        completed = self.run_script(HELPER, HOME=str(home))

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(marker.read_text(), "preserve upstream bytes")
        self.assertEqual(link.readlink(), skills)
        self.assertEqual(self.log.read_text(), "")

    def test_check_is_read_only_and_enable_is_refused(self) -> None:
        check = self.run_script(SETUP, "--check")
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertIn("disabled", check.stdout)
        enable = self.run_script(SETUP, "--enable")
        self.assertEqual(enable.returncode, 2)
        self.assertIn("disabled", enable.stderr)
        self.assertIn("--disable", enable.stderr)
        self.assertEqual(self.log.read_text(), "")
        self.assertFalse(Path(self.env["HOME"]).exists())

    def test_disable_works_without_source_and_is_idempotent(self) -> None:
        for environment in ({}, {"TEST_SYSTEMCTL_STATUS": "1", "TEST_SYSTEMCTL_ERROR": "Unit superpowers-release-sync.timer is not loaded."}):
            completed = self.run_script(SETUP, "--disable", **environment)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("disabled", completed.stdout)
        calls = self.log.read_text().splitlines()
        self.assertEqual(len(calls), 2)
        for call in calls:
            self.assertTrue(call.endswith("systemctl --user disable --now superpowers-release-sync.timer"))

    def test_disable_failure_is_sanitized(self) -> None:
        completed = self.run_script(SETUP, "--disable", TEST_SYSTEMCTL_STATUS="1", TEST_SYSTEMCTL_ERROR="PRIVATE_CONFIG_MUST_NOT_LEAK")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("timer disable failed", completed.stderr)
        self.assertNotIn("PRIVATE_CONFIG", completed.stderr)

    def test_required_exclusive_action_and_unknown_option(self) -> None:
        for arguments in ((), ("--check", "--enable"), ("--unknown",)):
            self.assertEqual(self.run_script(SETUP, *arguments).returncode, 2)
        self.assertEqual(self.run_script(HELPER, "--unknown").returncode, 2)
        self.assertEqual(self.log.read_text(), "")

    def test_plain_output_omits_decoration(self) -> None:
        completed = self.run_script(SETUP, "--check", CLI_PLAIN="1")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(completed.stdout.isascii())
        self.assertIn("disabled", completed.stdout)


if __name__ == "__main__":
    unittest.main()
