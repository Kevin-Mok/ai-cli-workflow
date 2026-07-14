"""Bounded path, secret, and Git LFS checks for checkpoint candidates."""

from __future__ import annotations

import os
import stat
from pathlib import Path, PurePosixPath

from .checkpoint_contract import (
    ALLOWLIST,
    LFS_POINTER,
    MEDIA_SUFFIXES,
    SENSITIVE_PARTS,
    CheckpointError,
)
from .checkpoint_git import decode, git
from .content_security import MAX_SECRET_SCAN_BYTES, likely_secret_name, redact


def _is_allowed(path: str) -> bool:
    return path == ALLOWLIST[-1] or any(
        path.startswith(prefix) for prefix in ALLOWLIST[:-1]
    )


def validate_allowed_paths(paths: list[str]) -> None:
    if any(not _is_allowed(path) for path in paths):
        raise CheckpointError("checkpoint staged path is outside the allowlist")
    if any(redact(path) != path for path in paths):
        raise CheckpointError("checkpoint rejected secret-like path")


def _sensitive_path(path: str) -> bool:
    pure = PurePosixPath(path)
    if likely_secret_name(pure.name):
        return True
    for part in pure.parts:
        lowered = part.casefold()
        if (
            lowered in SENSITIVE_PARTS
            or Path(part).stem.casefold() in SENSITIVE_PARTS
        ):
            return True
    return False


def _lfs_tracked(repo: Path, path: str, tree: str | None = None) -> bool:
    source = (f"--source={tree}",) if tree is not None else ("--cached",)
    completed = git(repo, "check-attr", *source, "filter", "--", path)
    try:
        output = completed.stdout.decode("utf-8").rstrip()
    except UnicodeError as error:
        raise CheckpointError("checkpoint Git LFS attribute is invalid") from error
    return output.endswith(": lfs")


def _validate_content(
    repo: Path,
    path: str,
    content: bytes,
    *,
    staged: bool,
    tree: str | None = None,
) -> None:
    if _sensitive_path(path):
        raise CheckpointError(f"checkpoint rejected sensitive path: {path}")
    if PurePosixPath(path).suffix.casefold() in MEDIA_SUFFIXES:
        if not _lfs_tracked(repo, path, tree) or (
            staged and not LFS_POINTER.fullmatch(content)
        ):
            raise CheckpointError(f"checkpoint requires Git LFS for media: {path}")
        return
    if len(content) >= MAX_SECRET_SCAN_BYTES:
        raise CheckpointError(f"checkpoint cannot audit oversized content: {path}")
    try:
        text = content.decode("utf-8")
    except UnicodeError as error:
        raise CheckpointError(f"checkpoint rejected non-text content: {path}") from error
    if "\0" in text:
        raise CheckpointError(f"checkpoint rejected non-text content: {path}")
    if redact(text) != text:
        raise CheckpointError(f"checkpoint rejected likely secret content: {path}")


def scan_worktree(repo: Path, paths: list[str]) -> None:
    for path in paths:
        relative = PurePosixPath(path)
        ancestor = repo
        for part in relative.parts[:-1]:
            ancestor /= part
            try:
                ancestor_metadata = ancestor.lstat()
            except OSError as error:
                raise CheckpointError(
                    f"checkpoint could not inspect path: {path}"
                ) from error
            if not stat.S_ISDIR(ancestor_metadata.st_mode):
                raise CheckpointError(
                    f"checkpoint rejected unsafe filesystem path: {path}"
                )
        target = repo / relative
        if not target.exists() and not target.is_symlink():
            continue
        try:
            metadata = target.lstat()
        except OSError as error:
            raise CheckpointError(
                f"checkpoint could not inspect path: {path}"
            ) from error
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise CheckpointError(
                f"checkpoint rejected unsafe filesystem path: {path}"
            )
        if _sensitive_path(path):
            raise CheckpointError(f"checkpoint rejected sensitive path: {path}")
        if relative.suffix.casefold() in MEDIA_SUFFIXES:
            _validate_content(repo, path, b"", staged=False)
            continue
        if metadata.st_size >= MAX_SECRET_SCAN_BYTES:
            raise CheckpointError(
                f"checkpoint cannot audit oversized content: {path}"
            )
        try:
            with target.open("rb") as stream:
                opened = os.fstat(stream.fileno())
                if (
                    not stat.S_ISREG(opened.st_mode)
                    or opened.st_nlink != 1
                    or (opened.st_dev, opened.st_ino)
                    != (metadata.st_dev, metadata.st_ino)
                ):
                    raise CheckpointError(
                        f"checkpoint rejected unsafe filesystem path: {path}"
                    )
                content = stream.read(MAX_SECRET_SCAN_BYTES)
        except OSError as error:
            raise CheckpointError(f"checkpoint could not read path: {path}") from error
        _validate_content(repo, path, content, staged=False)


def _tree_modes(repo: Path, tree: str, paths: list[str]) -> dict[str, str]:
    modes: dict[str, str] = {}
    for path in paths:
        output = git(repo, "ls-tree", "-z", tree, "--", path).stdout
        for record in output.split(b"\0"):
            if not record:
                continue
            try:
                metadata, encoded_path = record.split(b"\t", 1)
                mode, object_type, _object_id = metadata.split(b" ", 2)
                decoded_path = encoded_path.decode("utf-8")
                decoded_mode = mode.decode("ascii")
            except (ValueError, UnicodeError) as error:
                raise CheckpointError(
                    "checkpoint could not inspect committed tree mode"
                ) from error
            if object_type == b"blob" and decoded_path == path:
                modes[path] = decoded_mode
    return modes


def scan_staged(repo: Path, paths: list[str], *, tree: str | None = None) -> None:
    immutable_tree = tree or decode(git(repo, "write-tree").stdout, "staged tree")
    modes = _tree_modes(repo, immutable_tree, paths)
    for path in paths:
        mode = modes.get(path)
        if mode is None:
            continue
        if mode not in {"100644", "100755"}:
            raise CheckpointError(f"checkpoint rejected unsafe staged path: {path}")
        is_media = PurePosixPath(path).suffix.casefold() in MEDIA_SUFFIXES
        if is_media and not _lfs_tracked(repo, path, immutable_tree):
            raise CheckpointError(f"checkpoint requires Git LFS for media: {path}")
        try:
            size = int(
                decode(
                    git(
                        repo,
                        "cat-file",
                        "-s",
                        f"{immutable_tree}:{path}",
                    ).stdout,
                    "staged size",
                )
            )
        except ValueError as error:
            raise CheckpointError("checkpoint staged size is invalid") from error
        if is_media and size >= 512:
            raise CheckpointError(f"checkpoint requires Git LFS for media: {path}")
        if not is_media and size >= MAX_SECRET_SCAN_BYTES:
            raise CheckpointError(
                f"checkpoint cannot audit oversized content: {path}"
            )
        content = git(repo, "show", f"{immutable_tree}:{path}").stdout
        _validate_content(
            repo,
            path,
            content,
            staged=True,
            tree=immutable_tree,
        )
