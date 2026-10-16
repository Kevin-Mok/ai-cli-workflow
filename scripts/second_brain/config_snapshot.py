"""Validate the Codex config boundary without importing private live settings."""

from __future__ import annotations

import os
import stat
import subprocess
import tomllib
from dataclasses import dataclass
from pathlib import Path

from .content_security import redact


MAX_CONFIG_BYTES = 1_000_000
READ_CHUNK_BYTES = 64 * 1024


class ConfigSnapshotError(RuntimeError):
    """A config snapshot precondition or atomic write failed."""


@dataclass(frozen=True)
class SnapshotResult:
    """Content-free outcome returned to interactive and checkpoint callers."""

    changed: bool
    dry_run: bool


def snapshot_codex_config(
    *,
    dry_run: bool = False,
    source_override: Path | None = None,
    target_override: Path | None = None,
    expected_target: Path | None = None,
) -> SnapshotResult:
    """Validate the legacy snapshot boundary; keep live settings out of source."""

    source = _source_path(source_override)
    target = _target_path(source, target_override)
    _validate_expected_mapping(source, target, expected_target)

    source_content, source_metadata = _read_regular(source, "source")
    _target_content, target_metadata = _read_regular(target, "target")
    if _same_identity(source_metadata, target_metadata):
        raise ConfigSnapshotError("source and target must be different files")
    _validate_toml(source_content)
    _validate_public_content(source_content)

    _assert_regular_unchanged(source, "source", source_metadata)
    _assert_regular_unchanged(target, "target", target_metadata)
    return SnapshotResult(changed=False, dry_run=dry_run)


def _source_path(override: Path | None) -> Path:
    if override is not None:
        return _absolute_path(override, "source")
    return _absolute_path(Path.home() / ".codex" / "config.toml", "source")


def _target_path(source: Path, override: Path | None) -> Path:
    if override is not None:
        return _absolute_path(override, "target")
    try:
        completed = subprocess.run(
            ["chezmoi", "source-path", str(source)],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise ConfigSnapshotError("chezmoi target could not be resolved") from error
    lines = completed.stdout.splitlines()
    if len(lines) != 1 or not lines[0].strip():
        raise ConfigSnapshotError("chezmoi returned an invalid target")
    return _absolute_path(Path(lines[0].strip()), "target")


def _absolute_path(path: Path, label: str) -> Path:
    expanded = path.expanduser()
    if not expanded.is_absolute():
        raise ConfigSnapshotError(f"{label} path must be absolute")
    return expanded.absolute()


def _validate_expected_mapping(
    source: Path,
    target: Path,
    expected_target: Path | None = None,
) -> None:
    if source.parts[-2:] != (".codex", "config.toml"):
        raise ConfigSnapshotError("unexpected source config mapping")
    if target.parts[-2:] != ("dot_codex", "config.toml"):
        raise ConfigSnapshotError("unexpected target config mapping")
    if expected_target is not None:
        expected = _absolute_path(expected_target, "expected target")
        if target != expected:
            raise ConfigSnapshotError(
                "target does not match the expected repository"
            )


def _read_regular(path: Path, label: str) -> tuple[bytes, os.stat_result]:
    try:
        resolved = path.resolve(strict=True)
        parent_before = os.stat(path.parent, follow_symlinks=False)
        before = os.stat(path, follow_symlinks=False)
    except OSError as error:
        raise ConfigSnapshotError(f"{label} must be one regular file") from error
    if (
        resolved != path
        or not stat.S_ISDIR(parent_before.st_mode)
        or not _private_regular_file(before)
    ):
        raise ConfigSnapshotError(f"{label} must be one regular file")
    _validate_size(before, label)

    directory_flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        directory_flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        directory_flags |= os.O_NOFOLLOW
    file_flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        file_flags |= os.O_NOFOLLOW
    try:
        parent_descriptor = os.open(path.parent, directory_flags)
    except OSError as error:
        raise ConfigSnapshotError(f"{label} must be one regular file") from error
    try:
        opened_parent = os.fstat(parent_descriptor)
        if not _same_directory_identity(parent_before, opened_parent):
            raise ConfigSnapshotError(f"{label} path changed while reading")
        try:
            descriptor = os.open(path.name, file_flags, dir_fd=parent_descriptor)
        except OSError as error:
            raise ConfigSnapshotError(
                f"{label} must be one regular file"
            ) from error
        try:
            opened = os.fstat(descriptor)
            if not _same_snapshot(before, opened):
                raise ConfigSnapshotError(
                    f"{label} regular file changed while reading"
                )
            content = _read_bounded(descriptor, label)
            after = os.fstat(descriptor)
            named = os.stat(
                path.name,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            parent_after = os.stat(path.parent, follow_symlinks=False)
            path_after = os.stat(path, follow_symlinks=False)
        except OSError as error:
            raise ConfigSnapshotError(
                f"{label} regular file changed while reading"
            ) from error
        finally:
            os.close(descriptor)
        if (
            not _same_snapshot(before, after)
            or not _same_snapshot(before, named)
            or not _same_snapshot(before, path_after)
            or not _same_directory_identity(parent_before, parent_after)
            or not _same_directory_identity(parent_before, opened_parent)
        ):
            raise ConfigSnapshotError(
                f"{label} regular file changed while reading"
            )
        return content, after
    finally:
        os.close(parent_descriptor)


def _read_bounded(descriptor: int, label: str) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        remaining = MAX_CONFIG_BYTES - total
        if remaining <= 0:
            raise ConfigSnapshotError(f"{label} config is too large")
        chunk = os.read(descriptor, min(READ_CHUNK_BYTES, remaining))
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)
        total += len(chunk)
        if total >= MAX_CONFIG_BYTES:
            raise ConfigSnapshotError(f"{label} config is too large")


def _validate_size(metadata: os.stat_result, label: str) -> None:
    if metadata.st_size >= MAX_CONFIG_BYTES:
        raise ConfigSnapshotError(f"{label} config is too large")


def _assert_regular_unchanged(
    path: Path,
    label: str,
    expected: os.stat_result,
) -> None:
    _content, current = _read_regular(path, label)
    if not _same_snapshot(expected, current):
        raise ConfigSnapshotError(f"{label} regular file changed after preflight")


def _private_regular_file(metadata: os.stat_result) -> bool:
    return (
        stat.S_ISREG(metadata.st_mode)
        and metadata.st_nlink == 1
        and (not hasattr(os, "getuid") or metadata.st_uid == os.getuid())
    )


def _same_identity(first: os.stat_result, second: os.stat_result) -> bool:
    return (first.st_dev, first.st_ino) == (second.st_dev, second.st_ino)


def _same_directory_identity(
    first: os.stat_result,
    second: os.stat_result,
) -> bool:
    return (
        stat.S_ISDIR(first.st_mode)
        and stat.S_ISDIR(second.st_mode)
        and _same_identity(first, second)
    )


def _same_snapshot(first: os.stat_result, second: os.stat_result) -> bool:
    return (
        _private_regular_file(second)
        and _same_identity(first, second)
        and first.st_mode == second.st_mode
        and first.st_uid == second.st_uid
        and first.st_gid == second.st_gid
        and first.st_nlink == second.st_nlink
        and first.st_size == second.st_size
        and first.st_mtime_ns == second.st_mtime_ns
        and first.st_ctime_ns == second.st_ctime_ns
    )


def _validate_toml(content: bytes) -> None:
    try:
        decoded = content.decode("utf-8")
        document = tomllib.loads(decoded)
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as error:
        raise ConfigSnapshotError("source must contain valid TOML") from error
    if not isinstance(document, dict):
        raise ConfigSnapshotError("source must contain valid TOML")


def _validate_public_content(content: bytes) -> None:
    try:
        decoded = content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ConfigSnapshotError("source must contain valid TOML") from error
    if redact(decoded) != decoded:
        raise ConfigSnapshotError("source config contains a likely secret")
