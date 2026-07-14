"""Descriptor-anchored, permission-strict private-state reads."""

from __future__ import annotations

import os
import stat
from pathlib import Path

from .safe_contract import PathError


def _relative_parts(root: Path, target: Path) -> tuple[str, ...]:
    if not root.is_absolute() or not target.is_absolute():
        raise PathError("private state paths must be absolute")
    try:
        relative = target.relative_to(root)
    except ValueError as error:
        raise PathError("private state file escapes its root") from error
    if not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        raise PathError("private state file path is invalid")
    return relative.parts


def _directory_is_private(metadata: os.stat_result) -> bool:
    return (
        stat.S_ISDIR(metadata.st_mode)
        and metadata.st_uid == os.geteuid()
        and stat.S_IMODE(metadata.st_mode) == 0o700
    )


def _file_is_private(metadata: os.stat_result, max_bytes: int) -> bool:
    return (
        stat.S_ISREG(metadata.st_mode)
        and metadata.st_nlink == 1
        and metadata.st_uid == os.geteuid()
        and stat.S_IMODE(metadata.st_mode) == 0o600
        and metadata.st_size < max_bytes
    )


def _unchanged_file(first: os.stat_result, second: os.stat_result) -> bool:
    return (
        _file_is_private(second, first.st_size + 1)
        and (first.st_dev, first.st_ino) == (second.st_dev, second.st_ino)
        and first.st_size == second.st_size
        and first.st_mtime_ns == second.st_mtime_ns
    )


def private_file_bytes(
    root: Path,
    target: Path,
    *,
    max_bytes: int,
) -> bytes | None:
    """Read a private file, returning None only when its safe path is absent."""

    parts = _relative_parts(root, target)
    directory_flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        directory_flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        directory_flags |= os.O_NOFOLLOW
    try:
        current = os.open(root, directory_flags)
    except FileNotFoundError:
        return None
    except OSError as error:
        raise PathError("private state root is unsafe") from error

    descriptors = [current]
    try:
        if not _directory_is_private(os.fstat(current)):
            raise PathError("private state directory permissions are unsafe")
        for part in parts[:-1]:
            try:
                child = os.open(part, directory_flags, dir_fd=current)
            except FileNotFoundError:
                return None
            except OSError as error:
                raise PathError("private state parent is unsafe") from error
            descriptors.append(child)
            current = child
            if not _directory_is_private(os.fstat(current)):
                raise PathError("private state directory permissions are unsafe")

        file_flags = os.O_RDONLY
        if hasattr(os, "O_NOFOLLOW"):
            file_flags |= os.O_NOFOLLOW
        try:
            descriptor = os.open(parts[-1], file_flags, dir_fd=current)
        except FileNotFoundError:
            return None
        except OSError as error:
            raise PathError("private state file is unsafe") from error
        descriptors.append(descriptor)
        before = os.fstat(descriptor)
        if not _file_is_private(before, max_bytes):
            raise PathError("private state file permissions are unsafe")
        chunks: list[bytes] = []
        total = 0
        while total < max_bytes:
            chunk = os.read(descriptor, min(1024 * 1024, max_bytes - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
        content = b"".join(chunks)
        after = os.fstat(descriptor)
        if total >= max_bytes or not _unchanged_file(before, after):
            raise PathError("private state file changed while being read")
        return content
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)
