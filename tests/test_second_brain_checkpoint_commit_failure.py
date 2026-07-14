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


class SecondBrainCheckpointCommitFailureTest(unittest.TestCase):
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
        self.git("config", "user.name", "Checkpoint Hook Test")
        self.git("config", "user.email", "hook@example.invalid")
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
        self.git("add", ".")
        self.git("commit", "-m", "chore: initialize fixture")
        self.git("remote", "add", "origin", str(self.remote))
        self.git("push", "-u", "origin", "main")
        self.initial_head = self.git("rev-parse", "HEAD").stdout.strip()
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

    def test_failed_commit_command_restores_index_and_preserves_worktree(self) -> None:
        private_failure = "PRIVATE_COMMIT_FAILURE_MUST_NOT_LEAK"
        real_git = checkpoint._git

        def fail_commit(repo, *arguments, **kwargs):
            if "commit" in arguments or "commit-tree" in arguments:
                raise checkpoint.CheckpointError(
                    "checkpoint Git command failed"
                ) from RuntimeError(private_failure)
            return real_git(repo, *arguments, **kwargs)

        relative = "second-brain/01 Inbox/Hook Failure.md"
        content = "# Worktree content survives commit failure\n"
        target = self.repo / relative
        target.write_text(content, encoding="utf-8")

        with (
            mock.patch.dict(os.environ, self.env, clear=True),
            mock.patch.object(checkpoint, "_snapshot_config"),
            mock.patch.object(checkpoint, "_run_doctor_gate"),
            mock.patch.object(checkpoint, "_run_readme_gate"),
            mock.patch.object(checkpoint, "_git", side_effect=fail_commit),
            self.assertRaises(checkpoint.CheckpointError) as raised,
        ):
            checkpoint.run_checkpoint(no_push=True)

        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.initial_head)
        self.assertEqual(self.git("diff", "--cached", "--name-only").stdout, "")
        self.assertEqual(target.read_text(encoding="utf-8"), content)
        self.assertIn(relative, self.git("status", "--short").stdout)
        self.assertNotIn(private_failure, str(raised.exception))


if __name__ == "__main__":
    unittest.main()
