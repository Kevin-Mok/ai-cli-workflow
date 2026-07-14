"""Content-safe Git inspection for daily checkpoints."""

from __future__ import annotations

import subprocess
from pathlib import Path, PurePosixPath

from .checkpoint_contract import ALLOWLIST, CheckpointError


def git(
    repo: Path,
    *arguments: str,
    check: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    try:
        completed = subprocess.run(
            ["git", *arguments],
            cwd=repo,
            check=False,
            capture_output=True,
        )
    except OSError as error:
        raise CheckpointError("checkpoint Git command could not run") from error
    if check and completed.returncode != 0:
        raise CheckpointError("checkpoint Git command failed")
    return completed


def decode(value: bytes, label: str) -> str:
    try:
        decoded = value.decode("utf-8").strip()
    except UnicodeError as error:
        raise CheckpointError(f"checkpoint {label} is not valid UTF-8") from error
    if not decoded:
        raise CheckpointError(f"checkpoint {label} is empty")
    return decoded


def _decode_paths(value: bytes) -> list[str]:
    paths: list[str] = []
    for encoded in value.split(b"\0"):
        if not encoded:
            continue
        try:
            path = encoded.decode("utf-8")
        except UnicodeError as error:
            raise CheckpointError("checkpoint path is not valid UTF-8") from error
        pure = PurePosixPath(path)
        if pure.is_absolute() or ".." in pure.parts or path != pure.as_posix():
            raise CheckpointError("checkpoint Git path is not canonical")
        paths.append(path)
    return sorted(set(paths))


def validate_repository(repo: Path) -> tuple[str, str]:
    worktree = git(repo, "rev-parse", "--is-inside-work-tree", check=False)
    if worktree.returncode != 0 or worktree.stdout.strip() != b"true":
        raise CheckpointError("checkpoint target must be a Git worktree")
    branch_result = git(
        repo,
        "symbolic-ref",
        "--quiet",
        "--short",
        "HEAD",
        check=False,
    )
    if branch_result.returncode != 0:
        raise CheckpointError("checkpoint refuses a detached Git HEAD")
    branch = decode(branch_result.stdout, "branch")
    upstream_result = git(
        repo,
        "rev-parse",
        "--abbrev-ref",
        "--symbolic-full-name",
        "@{upstream}",
        check=False,
    )
    if upstream_result.returncode != 0:
        raise CheckpointError("checkpoint current branch has no configured upstream")
    return branch, decode(upstream_result.stdout, "upstream")


def index_is_dirty(repo: Path) -> bool:
    result = git(
        repo,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=no",
    )
    records = result.stdout.split(b"\0")
    skip_path = False
    for record in records:
        if not record:
            continue
        if skip_path:
            skip_path = False
            continue
        if len(record) < 3:
            raise CheckpointError("checkpoint could not inspect the Git index")
        index_status, worktree_status = record[0:1], record[1:2]
        if index_status not in {b" ", b"?"} or (
            index_status == b" " and worktree_status == b"A"
        ):
            return True
        if index_status in {b"R", b"C"} or worktree_status in {b"R", b"C"}:
            skip_path = True
    return False


def candidate_paths(repo: Path) -> list[str]:
    tracked = git(
        repo,
        "diff",
        "--name-only",
        "--no-renames",
        "-z",
        "--",
        *ALLOWLIST,
    ).stdout
    untracked = git(
        repo,
        "ls-files",
        "--others",
        "--exclude-standard",
        "-z",
        "--",
        *ALLOWLIST,
    ).stdout
    return _decode_paths(tracked + untracked)


def staged_paths(repo: Path) -> list[str]:
    return _decode_paths(
        git(
            repo,
            "diff",
            "--cached",
            "--name-only",
            "--no-renames",
            "-z",
            "--",
        ).stdout
    )


def head_commit(repo: Path) -> str:
    return decode(git(repo, "rev-parse", "HEAD").stdout, "HEAD commit")


def write_tree(repo: Path) -> str:
    return decode(git(repo, "write-tree").stdout, "staged tree")


def tree_paths(repo: Path, parent: str, tree: str) -> list[str]:
    return _decode_paths(
        git(
            repo,
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "--no-renames",
            "-r",
            "-z",
            parent,
            tree,
        ).stdout
    )


def push_destination(repo: Path, branch: str) -> tuple[str, str]:
    result = git(
        repo,
        "for-each-ref",
        "--format=%(upstream:remotename)%00%(upstream:remoteref)",
        f"refs/heads/{branch}",
    )
    fields = result.stdout.rstrip(b"\n").split(b"\0")
    if len(fields) != 2:
        raise CheckpointError("checkpoint configured upstream is invalid")
    remote = decode(fields[0], "upstream remote")
    remote_ref = decode(fields[1], "upstream ref")
    if remote.startswith("-") or not remote_ref.startswith("refs/heads/"):
        raise CheckpointError("checkpoint configured upstream is invalid")
    if git(repo, "check-ref-format", remote_ref, check=False).returncode != 0:
        raise CheckpointError("checkpoint configured upstream is invalid")
    return remote, remote_ref
