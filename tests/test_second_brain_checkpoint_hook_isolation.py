#!/usr/bin/env python3

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from second_brain import checkpoint


class SecondBrainCheckpointHookIsolationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.repo = self.root / "repo"
        self.remote = self.root / "remote.git"
        self.home = self.root / "home"
        self.home.mkdir()
        subprocess.run(
            ["git", "init", "--bare", str(self.remote)],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "init", "-b", "main", str(self.repo)],
            check=True,
            capture_output=True,
        )
        self.git("config", "user.name", "Checkpoint Hook Isolation Test")
        self.git("config", "user.email", "hook-isolation@example.invalid")
        (self.repo / "second-brain").mkdir()
        (self.repo / "second-brain/README.md").write_text(
            "# Fixture\n",
            encoding="utf-8",
        )
        for prefix in checkpoint.ALLOWLIST[:-1]:
            directory = self.repo / prefix
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "Seed.md").write_text("# Seed\n", encoding="utf-8")
        (self.repo / "dot_codex").mkdir()
        (self.repo / "dot_codex/config.toml").write_text(
            'model = "fixture"\n',
            encoding="utf-8",
        )
        self.readme = self.repo / "README.md"
        self.readme.write_text("# Original README\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "chore: initialize fixture")
        self.git("remote", "add", "origin", str(self.remote))
        self.git("push", "-u", "origin", "main")
        self.env = {
            **os.environ,
            "HOME": str(self.home),
            "XDG_STATE_HOME": str(self.root / "state"),
            "SECOND_BRAIN_REPO_ROOT": str(self.repo),
            "SECOND_BRAIN_NOW": "2026-07-14T16:20:00-04:00",
            "PYTHONDONTWRITEBYTECODE": "1",
        }

    def git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *arguments],
            cwd=self.repo,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_successful_mutating_hook_cannot_expand_checkpoint_commit(self) -> None:
        hook = self.repo / ".git/hooks/pre-commit"
        hook.write_text(
            "#!/bin/sh\ngit add README.md\n",
            encoding="utf-8",
        )
        hook.chmod(0o755)
        readme_content = "# Unrelated user README edit\n"
        self.readme.write_text(readme_content, encoding="utf-8")
        allowed = "second-brain/01 Inbox/Hook Isolation.md"
        (self.repo / allowed).write_text("# Allowed checkpoint\n", encoding="utf-8")

        with (
            mock.patch.dict(os.environ, self.env, clear=True),
            mock.patch.object(checkpoint, "_snapshot_config"),
            mock.patch.object(checkpoint, "_run_doctor_gate"),
            mock.patch.object(checkpoint, "_run_readme_gate"),
        ):
            report = checkpoint.run_checkpoint(no_push=True)

        committed = self.git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            "HEAD",
        ).stdout.splitlines()
        self.assertEqual(committed, [allowed])
        self.assertEqual(report["paths"], [allowed])
        self.assertEqual(self.readme.read_text(encoding="utf-8"), readme_content)
        self.assertIn(" M README.md", self.git("status", "--short").stdout)
        self.assertEqual(self.git("diff", "--cached", "--name-only").stdout, "")

    def test_index_mutation_after_scan_cannot_expand_checkpoint_commit(self) -> None:
        readme_content = "# Concurrent staged README edit\n"
        self.readme.write_text(readme_content, encoding="utf-8")
        allowed = "second-brain/01 Inbox/Index Race.md"
        (self.repo / allowed).write_text("# Scanned checkpoint\n", encoding="utf-8")
        real_scan = checkpoint._scan_staged

        def stage_unrelated_after_scan(
            repo: Path,
            paths: list[str],
            *,
            tree: str | None = None,
        ) -> None:
            real_scan(repo, paths, tree=tree)
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=repo,
                check=True,
                capture_output=True,
            )

        with (
            mock.patch.dict(os.environ, self.env, clear=True),
            mock.patch.object(checkpoint, "_snapshot_config"),
            mock.patch.object(checkpoint, "_run_doctor_gate"),
            mock.patch.object(checkpoint, "_run_readme_gate"),
            mock.patch.object(
                checkpoint,
                "_scan_staged",
                side_effect=stage_unrelated_after_scan,
            ),
        ):
            report = checkpoint.run_checkpoint(no_push=True)

        committed = self.git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            "HEAD",
        ).stdout.splitlines()
        self.assertEqual(committed, [allowed])
        self.assertEqual(report["paths"], [allowed])
        self.assertEqual(self.readme.read_text(encoding="utf-8"), readme_content)
        self.assertEqual(
            self.git("diff", "--cached", "--name-only").stdout,
            "README.md\n",
        )


if __name__ == "__main__":
    unittest.main()
