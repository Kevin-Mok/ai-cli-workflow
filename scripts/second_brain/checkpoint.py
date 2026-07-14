"""Locked, allowlisted, content-safe daily Git checkpoints."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from .checkpoint_contract import ALLOWLIST, CheckpointError
from .checkpoint_git import (
    candidate_paths as _candidate_paths,
    decode as _decode,
    git as _git,
    head_commit as _head_commit,
    index_is_dirty as _index_is_dirty,
    push_destination as _push_destination,
    tree_paths as _tree_paths,
    validate_repository as _validate_repository,
    write_tree as _write_tree,
)
from .checkpoint_scan import (
    scan_staged as _scan_staged,
    scan_worktree as _scan_worktree,
    validate_allowed_paths as _validate_allowed_paths,
)
from .paths import LockError, local_now, mutation_lock, resolve_repo


def _snapshot_config(repo: Path, *, dry_run: bool) -> Any:
    from .config_snapshot import ConfigSnapshotError, snapshot_codex_config

    try:
        return snapshot_codex_config(
            dry_run=dry_run,
            expected_target=repo / "dot_codex" / "config.toml",
        )
    except ConfigSnapshotError as error:
        raise CheckpointError("checkpoint config snapshot failed") from error


def _run_doctor_gate(repo: Path) -> None:
    del repo
    from .doctor import build_report

    report = build_report()
    if report["summary"]["errors"]:
        raise CheckpointError("checkpoint Second Brain doctor reported errors")


def _run_readme_gate(repo: Path) -> None:
    gate = repo / "scripts/executable_readme-recruiter-sync"
    try:
        completed = subprocess.run(
            [str(gate), str(repo)],
            cwd=repo,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        raise CheckpointError("checkpoint README gate could not run") from error
    lines = completed.stdout.splitlines()
    if completed.returncode != 0 or not lines or lines[0] != "pass_no_change":
        raise CheckpointError("checkpoint README recruiter gate did not pass")


def _unstage_allowlist(repo: Path) -> None:
    _git(repo, "restore", "--staged", "--", *ALLOWLIST)


def _cleanup_failed_commit(repo: Path, parent: str, tree: str) -> None:
    current_head = _git(repo, "rev-parse", "HEAD", check=False)
    current_tree = _git(repo, "write-tree", check=False)
    if (
        current_head.returncode == 0
        and current_tree.returncode == 0
        and current_head.stdout.strip() == parent.encode("ascii")
        and current_tree.stdout.strip() == tree.encode("ascii")
    ):
        _unstage_allowlist(repo)


def _report(
    *,
    result: str,
    date: str,
    branch: str,
    upstream: str,
    paths: list[str],
    commit: str | None = None,
    pushed: bool = False,
) -> dict[str, Any]:
    return {
        "branch": branch,
        "command": "checkpoint",
        "commit": commit,
        "date": date,
        "paths": paths,
        "pushed": pushed,
        "result": result,
        "schema_version": 1,
        "upstream": upstream,
    }


def run_checkpoint(
    *,
    dry_run: bool = False,
    no_push: bool = False,
) -> dict[str, Any]:
    """Validate, stage, commit, and optionally push one daily checkpoint."""

    with mutation_lock():
        repo = resolve_repo()
        branch, upstream = _validate_repository(repo)
        if _index_is_dirty(repo):
            raise CheckpointError("checkpoint refuses an already-dirty Git index")
        parent = _head_commit(repo)
        push_remote, push_ref = _push_destination(repo, branch)
        snapshot = _snapshot_config(repo, dry_run=dry_run)
        _run_doctor_gate(repo)
        _run_readme_gate(repo)
        paths = _candidate_paths(repo)
        if dry_run and getattr(snapshot, "changed", False):
            paths = sorted(set(paths) | {"dot_codex/config.toml"})
        _validate_allowed_paths(paths)
        _scan_worktree(repo, paths)
        date = local_now().date().isoformat()
        if dry_run:
            return _report(
                result="dry-run",
                date=date,
                branch=branch,
                upstream=upstream,
                paths=paths,
            )

        try:
            _git(repo, "add", "-A", "--", *ALLOWLIST)
            tree = _write_tree(repo)
            paths = _tree_paths(repo, parent, tree)
            _validate_allowed_paths(paths)
            _scan_staged(repo, paths, tree=tree)
        except CheckpointError:
            _unstage_allowlist(repo)
            raise
        if not paths:
            return _report(
                result="noop",
                date=date,
                branch=branch,
                upstream=upstream,
                paths=[],
            )

        subject = f"chore(second-brain): checkpoint {date}"
        try:
            commit = _decode(
                _git(
                    repo,
                    "commit-tree",
                    tree,
                    "-p",
                    parent,
                    "-m",
                    subject,
                ).stdout,
                "commit",
            )
            _git(
                repo,
                "update-ref",
                "-m",
                subject,
                f"refs/heads/{branch}",
                commit,
                parent,
            )
        except CheckpointError:
            _cleanup_failed_commit(repo, parent, tree)
            raise
        if no_push:
            return _report(
                result="committed",
                date=date,
                branch=branch,
                upstream=upstream,
                paths=paths,
                commit=commit,
            )
        lfs_upload = _git(
            repo,
            "lfs",
            "push",
            push_remote,
            commit,
            check=False,
        )
        if lfs_upload.returncode != 0:
            raise CheckpointError(
                f"checkpoint Git LFS upload failed; local commit {commit} "
                "is preserved"
            )
        pushed = _git(
            repo,
            "push",
            "--no-all",
            "--no-mirror",
            "--no-tags",
            "--no-follow-tags",
            "--no-prune",
            "--no-force",
            "--no-verify",
            "--signed=no",
            "--recurse-submodules=no",
            "--",
            push_remote,
            f"{commit}:{push_ref}",
            check=False,
        )
        if pushed.returncode != 0:
            raise CheckpointError(
                f"checkpoint push failed; local commit {commit} is preserved"
            )
        return _report(
            result="committed",
            date=date,
            branch=branch,
            upstream=upstream,
            paths=paths,
            commit=commit,
            pushed=True,
        )
