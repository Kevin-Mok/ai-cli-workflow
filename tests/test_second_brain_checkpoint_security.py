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

from second_brain import checkpoint, config_snapshot
from second_brain.config_snapshot import ConfigSnapshotError


class SecondBrainCheckpointSecurityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)

    def test_intent_to_add_counts_as_a_dirty_index(self) -> None:
        repo = self.root / "repo"
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        subprocess.run(
            ["git", "-C", str(repo), "config", "user.name", "Test"],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(repo),
                "config",
                "user.email",
                "test@example.invalid",
            ],
            check=True,
        )
        (repo / "base").write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", "base"], check=True)
        subprocess.run(
            ["git", "-C", str(repo), "commit", "-qm", "init"],
            check=True,
        )
        (repo / "planned").write_text("planned\n", encoding="utf-8")
        subprocess.run(
            ["git", "-C", str(repo), "add", "-N", "planned"],
            check=True,
        )

        self.assertTrue(checkpoint._index_is_dirty(repo))

    def test_snapshot_errors_are_normalized_for_content_safe_cli_handling(self) -> None:
        with mock.patch(
            "second_brain.config_snapshot.snapshot_codex_config",
            side_effect=ConfigSnapshotError("fixture failure"),
        ):
            with self.assertRaisesRegex(checkpoint.CheckpointError, "config snapshot"):
                checkpoint._snapshot_config(self.root / "repo", dry_run=False)

    def test_checkpoint_snapshot_rejects_another_repository_target(self) -> None:
        checkpoint_repo = self.root / "checkpoint-repo"
        expected = checkpoint_repo / "dot_codex" / "config.toml"
        expected.parent.mkdir(parents=True)
        expected.write_text('model = "checkpoint"\n', encoding="utf-8")
        outside = self.root / "other-repo" / "dot_codex" / "config.toml"
        outside.parent.mkdir(parents=True)
        outside.write_text('model = "outside"\n', encoding="utf-8")
        outside_before = outside.read_bytes()
        home = self.root / "home"
        source = home / ".codex" / "config.toml"
        source.parent.mkdir(parents=True)
        source.write_text('model = "live"\n', encoding="utf-8")

        with (
            mock.patch.dict(os.environ, {"HOME": str(home)}, clear=False),
            mock.patch.object(
                config_snapshot.subprocess,
                "run",
                return_value=subprocess.CompletedProcess(
                    ["chezmoi"],
                    0,
                    stdout=f"{outside}\n",
                ),
            ),
            self.assertRaisesRegex(checkpoint.CheckpointError, "config snapshot"),
        ):
            checkpoint._snapshot_config(checkpoint_repo, dry_run=False)

        self.assertEqual(outside.read_bytes(), outside_before)

    def test_oversized_worktree_text_is_rejected_before_it_is_read(self) -> None:
        repo = self.root / "repo"
        target = repo / "second-brain/01 Inbox/Large.md"
        target.parent.mkdir(parents=True)
        with target.open("wb") as stream:
            stream.truncate(1_000_000)

        with mock.patch.object(
            Path,
            "read_bytes",
            side_effect=AssertionError("oversized file was read"),
        ):
            with self.assertRaisesRegex(
                checkpoint.CheckpointError,
                "oversized content",
            ):
                checkpoint._scan_worktree(
                    repo,
                    ["second-brain/01 Inbox/Large.md"],
                )

    def test_symlinked_worktree_parent_is_rejected(self) -> None:
        repo = self.root / "repo"
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "Escaped.md").write_text("# Escaped\n", encoding="utf-8")
        inbox = repo / "second-brain/01 Inbox"
        inbox.parent.mkdir(parents=True)
        inbox.symlink_to(outside, target_is_directory=True)

        with self.assertRaisesRegex(
            checkpoint.CheckpointError,
            "unsafe filesystem path",
        ):
            checkpoint._scan_worktree(
                repo,
                ["second-brain/01 Inbox/Escaped.md"],
            )

    def test_oversized_staged_text_is_rejected_without_loading_the_blob(self) -> None:
        repo = self.root / "repo"
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        target = repo / "second-brain/01 Inbox/Large.md"
        target.parent.mkdir(parents=True)
        with target.open("wb") as stream:
            stream.truncate(1_000_000)
        subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
        real_git = checkpoint._git

        def guard(repo_path, *arguments, **kwargs):
            if arguments and arguments[0] == "show":
                raise AssertionError("oversized staged blob was loaded")
            return real_git(repo_path, *arguments, **kwargs)

        with mock.patch.object(checkpoint, "_git", side_effect=guard):
            with self.assertRaisesRegex(
                checkpoint.CheckpointError,
                "oversized content",
            ):
                checkpoint._scan_staged(
                    repo,
                    ["second-brain/01 Inbox/Large.md"],
                )


if __name__ == "__main__":
    unittest.main()
