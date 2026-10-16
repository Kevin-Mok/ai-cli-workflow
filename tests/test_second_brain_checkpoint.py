#!/usr/bin/env python3

import fcntl
import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "executable_second-brain"
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))


ALLOWLIST = (
    "second-brain/00 Context/",
    "second-brain/01 Inbox/",
    "second-brain/02 Projects/",
    "second-brain/03 Areas/",
    "second-brain/04 Resources/",
    "second-brain/05 Daily Notes/",
    "second-brain/06 Archive/",
    "second-brain/07 Attachments/",
    "dot_codex/config.toml",
)


class SecondBrainCheckpointTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.repo = self.root / "repo"
        self.remote = self.root / "remote.git"
        self.home = self.root / "home"
        self.state_home = self.root / "state"
        self.home.mkdir()
        self.run_process("git", "init", "--bare", str(self.remote))
        self.run_process("git", "init", "-b", "main", str(self.repo))
        self.git("config", "user.name", "Checkpoint Test")
        self.git("config", "user.email", "checkpoint@example.invalid")

        (self.repo / "second-brain").mkdir()
        (self.repo / "second-brain/README.md").write_text(
            "# Fixture Second Brain\n",
            encoding="utf-8",
        )
        for prefix in ALLOWLIST[:-1]:
            directory = self.repo / prefix
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "Seed.md").write_text(
                "---\nvisibility: public-sanitized\n---\n\n# Seed\n",
                encoding="utf-8",
            )
        (self.repo / "dot_codex").mkdir()
        (self.repo / "dot_codex/config.toml").write_text(
            'model = "fixture"\n',
            encoding="utf-8",
        )
        (self.repo / "README.md").write_text(
            "# Fixture repository\n",
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
            "XDG_STATE_HOME": str(self.state_home),
            "SECOND_BRAIN_REPO_ROOT": str(self.repo),
            "SECOND_BRAIN_NOW": "2026-07-14T16:20:00-04:00",
            "PYTHONDONTWRITEBYTECODE": "1",
        }

    @staticmethod
    def run_process(
        *arguments: str,
        cwd: Path | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            arguments,
            cwd=cwd,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )

    def git(
        self,
        *arguments: str,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *arguments],
            cwd=self.repo,
            check=check,
            capture_output=True,
            text=True,
        )

    def require_checkpoint_module(self) -> ModuleType:
        try:
            return importlib.import_module("second_brain.checkpoint")
        except ModuleNotFoundError as error:
            self.fail(
                "scripts/second_brain/checkpoint.py is required for safe "
                f"daily Git checkpoint contracts: {error}"
            )
        raise AssertionError("unreachable")

    @staticmethod
    def unchanged_snapshot(repo: Path, *, dry_run: bool = False) -> None:
        del repo, dry_run

    def run_checkpoint(
        self,
        checkpoint: ModuleType,
        *,
        dry_run: bool = False,
        no_push: bool = False,
        snapshot=None,
        privacy_gate=None,
    ) -> dict:
        snapshot_effect = snapshot or self.unchanged_snapshot
        with (
            mock.patch.dict(os.environ, self.env, clear=True),
            mock.patch.object(
                checkpoint,
                "_snapshot_config",
                side_effect=snapshot_effect,
            ),
            mock.patch.object(checkpoint, "_run_doctor_gate"),
            mock.patch.object(checkpoint, "_run_readme_gate"),
            # Private-vault mechanics are isolated from the public-repo policy;
            # test_checkpoint_privacy_gate exercises the real shared gate.
            mock.patch.object(checkpoint, "_run_privacy_gate", side_effect=privacy_gate),
        ):
            return checkpoint.run_checkpoint(dry_run=dry_run, no_push=no_push)

    def test_public_gate_blocks_private_vault_before_plumbing_commit(self) -> None:
        checkpoint = self.require_checkpoint_module()
        scripts = self.repo / "scripts"
        scripts.mkdir(exist_ok=True)
        for name in ("executable_privacy-gate", "privacy_gate.py", "executable_audit-public-history", "privacy_gate_approvals.json"):
            shutil.copyfile(SCRIPTS_ROOT / name, scripts / name)
        self.write_allowed("second-brain/00 Context/Decisions.md", "public fixture bytes\n")
        real_gate = checkpoint._run_privacy_gate
        with self.assertRaisesRegex(checkpoint.CheckpointError, "privacy gate"):
            self.run_checkpoint(checkpoint, no_push=True, privacy_gate=real_gate)
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.initial_head)
        self.assertEqual(self.git("diff", "--cached", "--name-only").stdout, "")

    def write_allowed(self, relative: str, content: str) -> Path:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def remote_head(self) -> str:
        return self.run_process(
            "git",
            "--git-dir",
            str(self.remote),
            "rev-parse",
            "refs/heads/main",
        ).stdout.strip()

    def test_cli_exposes_frozen_checkpoint_flags(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "checkpoint", "--help"],
            cwd=self.root,
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("--dry-run", completed.stdout)
        self.assertIn("--no-push", completed.stdout)

    def test_allowlist_contract_is_exact(self) -> None:
        checkpoint = self.require_checkpoint_module()

        self.assertEqual(checkpoint.ALLOWLIST, ALLOWLIST)

    def test_lock_contention_aborts_before_snapshot_or_git_changes(self) -> None:
        checkpoint = self.require_checkpoint_module()
        snapshot = mock.Mock(side_effect=self.unchanged_snapshot)

        with mock.patch.dict(os.environ, self.env, clear=True):
            with checkpoint.mutation_lock():
                with self.assertRaises(checkpoint.LockError):
                    self.run_checkpoint(
                        checkpoint,
                        no_push=True,
                        snapshot=snapshot,
                    )

        snapshot.assert_not_called()
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.initial_head)
        self.assertEqual(self.git("status", "--short").stdout, "")

    def test_non_worktree_is_rejected(self) -> None:
        checkpoint = self.require_checkpoint_module()
        shutil.rmtree(self.repo / ".git")
        (self.repo / ".git").mkdir()

        with self.assertRaisesRegex(checkpoint.CheckpointError, "Git worktree"):
            self.run_checkpoint(checkpoint, no_push=True)

    def test_detached_head_is_rejected_before_snapshot(self) -> None:
        checkpoint = self.require_checkpoint_module()
        self.git("checkout", "--detach")
        snapshot = mock.Mock(side_effect=self.unchanged_snapshot)

        with self.assertRaisesRegex(checkpoint.CheckpointError, "detached"):
            self.run_checkpoint(checkpoint, no_push=True, snapshot=snapshot)

        snapshot.assert_not_called()
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.initial_head)

    def test_missing_upstream_is_rejected_before_snapshot(self) -> None:
        checkpoint = self.require_checkpoint_module()
        self.git("branch", "--unset-upstream")
        snapshot = mock.Mock(side_effect=self.unchanged_snapshot)

        with self.assertRaisesRegex(checkpoint.CheckpointError, "upstream"):
            self.run_checkpoint(checkpoint, no_push=True, snapshot=snapshot)

        snapshot.assert_not_called()
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.initial_head)

    def test_dirty_index_aborts_without_consuming_staged_work(self) -> None:
        checkpoint = self.require_checkpoint_module()
        target = self.write_allowed(
            "second-brain/00 Context/Seed.md",
            "# User staged work\n",
        )
        self.git("add", target.relative_to(self.repo).as_posix())
        staged_before = self.git("diff", "--cached", "--name-only").stdout
        snapshot = mock.Mock(side_effect=self.unchanged_snapshot)

        with self.assertRaisesRegex(checkpoint.CheckpointError, "index"):
            self.run_checkpoint(checkpoint, no_push=True, snapshot=snapshot)

        snapshot.assert_not_called()
        self.assertEqual(
            self.git("diff", "--cached", "--name-only").stdout,
            staged_before,
        )
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.initial_head)

    def test_config_snapshot_change_is_included(self) -> None:
        checkpoint = self.require_checkpoint_module()
        expected = 'model = "snapshotted"\n'

        def snapshot(repo: Path, *, dry_run: bool = False) -> None:
            self.assertEqual(repo, self.repo)
            self.assertFalse(dry_run)
            (self.repo / "dot_codex/config.toml").write_text(
                expected,
                encoding="utf-8",
            )

        report = self.run_checkpoint(checkpoint, no_push=True, snapshot=snapshot)

        self.assertEqual(report["result"], "committed")
        self.assertEqual(report["paths"], ["dot_codex/config.toml"])
        committed = self.git("show", "HEAD:dot_codex/config.toml").stdout
        self.assertEqual(committed, expected)

    def test_secret_content_is_rejected_without_echoing_it(self) -> None:
        checkpoint = self.require_checkpoint_module()
        secret = "api_key=" + ("f" * 32)
        self.write_allowed(
            "second-brain/01 Inbox/Unsafe.md",
            f"# Unsafe\n\n{secret}\n",
        )

        with self.assertRaises(checkpoint.CheckpointError) as raised:
            self.run_checkpoint(checkpoint, no_push=True)

        self.assertIn("likely secret content", str(raised.exception))
        self.assertNotIn(secret, str(raised.exception))
        self.assertEqual(self.git("diff", "--cached", "--name-only").stdout, "")
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.initial_head)

    def test_sensitive_filename_is_rejected_stably(self) -> None:
        checkpoint = self.require_checkpoint_module()
        path = "second-brain/01 Inbox/.netrc"
        self.write_allowed(path, "machine example.invalid login user\n")

        with self.assertRaises(checkpoint.CheckpointError) as raised:
            self.run_checkpoint(checkpoint, no_push=True)

        self.assertEqual(
            str(raised.exception),
            f"checkpoint rejected sensitive path: {path}",
        )
        self.assertEqual(self.git("diff", "--cached", "--name-only").stdout, "")

    def test_secret_shaped_filename_is_rejected_without_echoing_it(self) -> None:
        checkpoint = self.require_checkpoint_module()
        secret = "sk-" + ("p" * 32)
        path = f"second-brain/01 Inbox/{secret}.md"
        self.write_allowed(path, "# Safe body\n")

        with self.assertRaises(checkpoint.CheckpointError) as raised:
            self.run_checkpoint(checkpoint, no_push=True)

        self.assertEqual(
            str(raised.exception),
            "checkpoint rejected secret-like path",
        )
        self.assertNotIn(secret, str(raised.exception))
        self.assertEqual(self.git("diff", "--cached", "--name-only").stdout, "")
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.initial_head)

    def test_media_without_lfs_is_rejected_stably(self) -> None:
        checkpoint = self.require_checkpoint_module()
        path = self.repo / "second-brain/07 Attachments/example.png"
        path.write_bytes(b"\x89PNG\r\n\x1a\nfixture")

        with self.assertRaises(checkpoint.CheckpointError) as raised:
            self.run_checkpoint(checkpoint, no_push=True)

        self.assertEqual(
            str(raised.exception),
            "checkpoint requires Git LFS for media: "
            "second-brain/07 Attachments/example.png",
        )
        self.assertEqual(self.git("diff", "--cached", "--name-only").stdout, "")

    def test_exact_allowlist_preserves_unrelated_unstaged_changes(self) -> None:
        checkpoint = self.require_checkpoint_module()
        allowed = "second-brain/05 Daily Notes/2026-07-14.md"
        self.write_allowed(allowed, "# Daily progress\n")
        (self.repo / "README.md").write_text(
            "# Unrelated user README edit\n",
            encoding="utf-8",
        )
        (self.repo / "unrelated.txt").write_text(
            "unrelated untracked work\n",
            encoding="utf-8",
        )

        report = self.run_checkpoint(checkpoint, no_push=True)

        changed = self.git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            "HEAD",
        ).stdout.splitlines()
        self.assertEqual(changed, [allowed])
        self.assertEqual(report["paths"], [allowed])
        status = self.git("status", "--short").stdout
        self.assertIn(" M README.md", status)
        self.assertIn("?? unrelated.txt", status)
        self.assertEqual(self.git("diff", "--cached", "--name-only").stdout, "")

    def test_noop_does_not_commit_or_push(self) -> None:
        checkpoint = self.require_checkpoint_module()
        remote_before = self.remote_head()

        report = self.run_checkpoint(checkpoint)

        self.assertEqual(report["result"], "noop")
        self.assertEqual(report["paths"], [])
        self.assertFalse(report["pushed"])
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.initial_head)
        self.assertEqual(self.remote_head(), remote_before)

    def test_dry_run_reports_paths_without_staging_or_committing(self) -> None:
        checkpoint = self.require_checkpoint_module()
        allowed = "second-brain/02 Projects/Progress.md"
        self.write_allowed(allowed, "# Progress\n")
        snapshot = mock.Mock(side_effect=self.unchanged_snapshot)

        report = self.run_checkpoint(
            checkpoint,
            dry_run=True,
            snapshot=snapshot,
        )

        snapshot.assert_called_once_with(self.repo, dry_run=True)
        self.assertEqual(report["result"], "dry-run")
        self.assertEqual(report["paths"], [allowed])
        self.assertEqual(self.git("diff", "--cached", "--name-only").stdout, "")
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.initial_head)

    def test_commit_uses_exact_dated_subject(self) -> None:
        checkpoint = self.require_checkpoint_module()
        self.write_allowed(
            "second-brain/02 Projects/Progress.md",
            "# Progress\n",
        )

        report = self.run_checkpoint(checkpoint, no_push=True)

        subject = self.git("log", "-1", "--format=%s").stdout.strip()
        self.assertEqual(
            subject,
            "chore(second-brain): checkpoint 2026-07-14",
        )
        self.assertEqual(report["commit"], self.git("rev-parse", "HEAD").stdout.strip())
        self.assertFalse(report["pushed"])

    def test_checkpoint_pushes_only_the_exact_configured_upstream_ref(self) -> None:
        checkpoint = self.require_checkpoint_module()
        self.write_allowed(
            "second-brain/03 Areas/Work.md",
            "# Work update\n",
        )

        report = self.run_checkpoint(checkpoint)

        local_head = self.git("rev-parse", "HEAD").stdout.strip()
        self.assertTrue(report["pushed"])
        self.assertEqual(report["upstream"], "origin/main")
        self.assertEqual(self.remote_head(), local_head)

    def test_push_ignores_pushdefault_and_targets_configured_upstream(self) -> None:
        checkpoint = self.require_checkpoint_module()
        backup = self.root / "backup.git"
        self.run_process("git", "init", "--bare", str(backup))
        self.git("remote", "add", "backup", str(backup))
        self.git("config", "remote.pushDefault", "backup")
        self.git("config", "push.default", "current")
        self.write_allowed(
            "second-brain/03 Areas/Configured Upstream.md",
            "# Configured upstream only\n",
        )

        report = self.run_checkpoint(checkpoint)

        local_head = self.git("rev-parse", "HEAD").stdout.strip()
        backup_head = subprocess.run(
            [
                "git",
                "--git-dir",
                str(backup),
                "rev-parse",
                "--verify",
                "refs/heads/main",
            ],
            cwd=self.root,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertTrue(report["pushed"])
        self.assertEqual(report["upstream"], "origin/main")
        self.assertEqual(self.remote_head(), local_head)
        self.assertNotEqual(backup_head.returncode, 0)

    def test_push_does_not_follow_unrelated_tags(self) -> None:
        checkpoint = self.require_checkpoint_module()
        self.git("tag", "-a", "unrelated-release", "-m", "unrelated tag")
        self.git("config", "push.followTags", "true")
        self.write_allowed(
            "second-brain/03 Areas/Tag Isolation.md",
            "# No unrelated tags\n",
        )

        report = self.run_checkpoint(checkpoint)

        remote_tag = subprocess.run(
            [
                "git",
                "--git-dir",
                str(self.remote),
                "rev-parse",
                "--verify",
                "refs/tags/unrelated-release",
            ],
            cwd=self.root,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertTrue(report["pushed"])
        self.assertNotEqual(remote_tag.returncode, 0)

    def test_push_bypasses_local_pre_push_hooks(self) -> None:
        checkpoint = self.require_checkpoint_module()
        marker = self.root / "pre-push-hook-ran"
        hook = self.repo / ".git/hooks/pre-push"
        hook.write_text(
            f"#!/bin/sh\nprintf ran > '{marker}'\nexit 1\n",
            encoding="utf-8",
        )
        hook.chmod(0o755)
        self.write_allowed(
            "second-brain/03 Areas/Push Hook Isolation.md",
            "# No local push hooks\n",
        )

        report = self.run_checkpoint(checkpoint)

        self.assertTrue(report["pushed"])
        self.assertFalse(marker.exists())
        self.assertEqual(
            self.remote_head(),
            self.git("rev-parse", "HEAD").stdout.strip(),
        )

    def test_checkpoint_uploads_reachable_lfs_media_before_ref_push(self) -> None:
        checkpoint = self.require_checkpoint_module()
        self.git("lfs", "install", "--local")
        (self.repo / ".gitattributes").write_text(
            '"second-brain/07 Attachments/**/*.png" '
            "filter=lfs diff=lfs merge=lfs -text\n",
            encoding="utf-8",
        )
        self.git("add", ".gitattributes")
        self.git("commit", "-m", "chore: configure fixture LFS")
        self.git("push", "origin", "main")

        relative = "second-brain/07 Attachments/Media/checkpoint.png"
        payload = b"\x89PNG\r\n\x1a\n" + (b"checkpoint-media" * 128)
        (self.repo / relative).parent.mkdir()
        (self.repo / relative).write_bytes(payload)

        local_only = self.run_checkpoint(checkpoint, no_push=True)
        remote_before = self.remote_head()
        marker = self.root / "pre-push-hook-ran-for-lfs"
        hook = self.repo / ".git/hooks/pre-push"
        hook.write_text(
            f"#!/bin/sh\nprintf ran > '{marker}'\nexit 1\n",
            encoding="utf-8",
        )
        hook.chmod(0o755)
        self.write_allowed(
            "second-brain/03 Areas/After Local LFS.md",
            "# Push the complete local history\n",
        )

        report = self.run_checkpoint(checkpoint)

        clone = self.root / "fresh-clone"
        clone_env = {**os.environ, "GIT_LFS_SKIP_SMUDGE": "1"}
        cloned = subprocess.run(
            ["git", "clone", str(self.remote), str(clone)],
            cwd=self.root,
            env=clone_env,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(cloned.returncode, 0, cloned.stderr)
        pulled = subprocess.run(
            ["git", "lfs", "pull"],
            cwd=clone,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertFalse(local_only["pushed"])
        self.assertNotEqual(local_only["commit"], remote_before)
        self.assertTrue(report["pushed"])
        self.assertFalse(marker.exists())
        self.assertEqual(pulled.returncode, 0, pulled.stderr)
        self.assertEqual((clone / relative).read_bytes(), payload)

    def test_failed_lfs_upload_preserves_local_commit_and_remote_ref(self) -> None:
        checkpoint = self.require_checkpoint_module()
        secret = "https://example.invalid/lfs"
        real_git = checkpoint._git

        def fail_lfs_upload(repo, *arguments, **kwargs):
            if arguments[:2] == ("lfs", "push"):
                return subprocess.CompletedProcess(
                    ["git", *arguments],
                    1,
                    stdout=b"",
                    stderr=secret.encode("utf-8"),
                )
            return real_git(repo, *arguments, **kwargs)

        self.write_allowed(
            "second-brain/04 Resources/LFS Failure.md",
            "# Preserve this local checkpoint\n",
        )

        with (
            mock.patch.object(checkpoint, "_git", side_effect=fail_lfs_upload),
            self.assertRaises(checkpoint.CheckpointError) as raised,
        ):
            self.run_checkpoint(checkpoint)

        local_head = self.git("rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(local_head, self.initial_head)
        self.assertEqual(self.remote_head(), self.initial_head)
        self.assertIn("Git LFS upload failed", str(raised.exception))
        self.assertIn(local_head, str(raised.exception))
        self.assertNotIn(secret, str(raised.exception))

    def test_failed_push_preserves_the_local_checkpoint_commit(self) -> None:
        checkpoint = self.require_checkpoint_module()
        hook = self.remote / "hooks/pre-receive"
        hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        hook.chmod(0o755)
        self.write_allowed(
            "second-brain/04 Resources/Progress.md",
            "# Local progress\n",
        )

        with self.assertRaises(checkpoint.CheckpointError) as raised:
            self.run_checkpoint(checkpoint)

        local_head = self.git("rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(local_head, self.initial_head)
        self.assertEqual(self.remote_head(), self.initial_head)
        self.assertIn(local_head, str(raised.exception))
        self.assertIn("local commit", str(raised.exception))
        self.assertEqual(
            self.git("log", "-1", "--format=%s").stdout.strip(),
            "chore(second-brain): checkpoint 2026-07-14",
        )
        self.assertEqual(self.git("status", "--short").stdout, "")


if __name__ == "__main__":
    unittest.main()
