"""Descriptor-relative regular-file safety primitives."""

from __future__ import annotations

import ctypes
import fcntl
import hashlib
import os
import secrets
import signal
import stat
import unicodedata
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterator

from .safe_contract import PathError, TargetExistsError, relative_target_parts


@contextmanager
def _open_relative_parent(
    root: Path,
    target: Path,
    *,
    create_parents: bool,
    portable_unique: bool = False,
    tracked_ancestors: list[tuple[int, str, os.stat_result, bool]] | None = None,
) -> Iterator[tuple[int, str]]:
    parts = relative_target_parts(root, target)
    directory_flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        directory_flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        directory_flags |= os.O_NOFOLLOW
    try:
        current = os.open(root, directory_flags)
    except OSError as error:
        raise PathError("safe filesystem boundary could not be opened") from error
    opened = [current]
    ancestors: list[tuple[int, str, os.stat_result, bool]] = []
    try:
        for part in parts[:-1]:
            created = False
            if create_parents:
                if portable_unique and _portable_name_collision(current, part):
                    raise TargetExistsError(
                        "safe filesystem parent has a portable-name collision"
                    )
                try:
                    os.mkdir(part, 0o755, dir_fd=current)
                    created = True
                except FileExistsError:
                    pass
                except OSError as error:
                    raise PathError(
                        "safe filesystem parent could not be prepared"
                    ) from error
            try:
                child = os.open(part, directory_flags, dir_fd=current)
            except OSError as error:
                raise PathError(
                    "safe filesystem parent is missing or unsafe"
                ) from error
            metadata = os.fstat(child)
            if not stat.S_ISDIR(metadata.st_mode):
                os.close(child)
                raise PathError("safe filesystem parent is not a directory")
            if portable_unique and _portable_name_collision(current, part):
                os.close(child)
                if created:
                    try:
                        os.rmdir(part, dir_fd=current)
                    except OSError:
                        pass
                raise TargetExistsError(
                    "safe filesystem parent has a portable-name collision"
                )
            ancestors.append((current, part, metadata, created))
            if tracked_ancestors is not None:
                tracked_ancestors.append(ancestors[-1])
            opened.append(child)
            current = child
        yield current, parts[-1]
    except BaseException:
        _rollback_created_parents(ancestors)
        raise
    finally:
        for descriptor in reversed(opened):
            os.close(descriptor)


def _rollback_created_parents(
    ancestors: list[tuple[int, str, os.stat_result, bool]],
) -> None:
    for parent_fd, name, expected, created in reversed(ancestors):
        if not created:
            continue
        try:
            current = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            if not _same_directory_identity(current, expected):
                continue
            os.rmdir(name, dir_fd=parent_fd)
            os.fsync(parent_fd)
        except OSError:
            pass


def _same_directory_identity(
    first: os.stat_result,
    second: os.stat_result,
) -> bool:
    return (
        stat.S_ISDIR(first.st_mode)
        and stat.S_ISDIR(second.st_mode)
        and (first.st_dev, first.st_ino) == (second.st_dev, second.st_ino)
    )


def _write_temp_at(
    parent_fd: int,
    target_name: str,
    content: bytes,
    mode: int,
) -> str:
    temporary_name = f".{target_name}.{secrets.token_hex(12)}.tmp"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(
            temporary_name,
            flags,
            mode,
            dir_fd=parent_fd,
        )
    except OSError as error:
        raise PathError("safe temporary file could not be created") from error
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
            os.fchmod(stream.fileno(), mode)
    except BaseException:
        try:
            os.unlink(temporary_name, dir_fd=parent_fd)
        except OSError:
            pass
        raise
    return temporary_name


def _portable_name_collision(parent_fd: int, target_name: str) -> bool:
    target_key = unicodedata.normalize("NFKC", target_name).casefold()
    try:
        names = os.listdir(parent_fd)
    except OSError as error:
        raise PathError("safe filesystem parent could not be inspected") from error
    return any(
        name != target_name
        and unicodedata.normalize("NFKC", name).casefold() == target_key
        for name in names
    )


def _read_regular_at(parent_fd: int, target_name: str) -> tuple[bytes, os.stat_result]:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(target_name, flags, dir_fd=parent_fd)
    except OSError as error:
        raise PathError("safe regular file could not be opened") from error
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise PathError("safe filesystem target must be one regular file")
        return _read_descriptor(descriptor)
    finally:
        os.close(descriptor)


def _read_descriptor(descriptor: int) -> tuple[bytes, os.stat_result]:
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while chunk := os.read(descriptor, 1024 * 1024):
        chunks.append(chunk)
    return b"".join(chunks), os.fstat(descriptor)


def regular_file_bytes(root: Path, target: Path) -> bytes:
    """Read one regular, single-link file through an anchored parent."""

    with _open_relative_parent(root, target, create_parents=False) as (
        parent_fd,
        target_name,
    ):
        content, _ = _read_regular_at(parent_fd, target_name)
        return content


@contextmanager
def _leased_regular_at(
    parent_fd: int,
    target_name: str,
) -> Iterator[tuple[bytes, os.stat_result, Callable[[], bool], int]]:
    flags = os.O_RDWR
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(target_name, flags, dir_fd=parent_fd)
    except OSError as error:
        raise PathError("safe regular file could not be opened") from error

    lease_held = False
    lease_broken = False
    previous_handler = None
    handler_installed = False

    def mark_lease_break(_signum, _frame) -> None:
        nonlocal lease_broken
        lease_broken = True

    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise PathError("safe filesystem target must be one regular file")
        try:
            previous_handler = signal.getsignal(signal.SIGIO)
            signal.signal(signal.SIGIO, mark_lease_break)
            handler_installed = True
            fcntl.fcntl(descriptor, fcntl.F_SETOWN, os.getpid())
            fcntl.fcntl(descriptor, fcntl.F_SETLEASE, fcntl.F_WRLCK)
            lease_held = True
        except (AttributeError, OSError, ValueError) as error:
            raise PathError(
                "safe filesystem target is open or leases are unavailable"
            ) from error

        content, metadata = _read_descriptor(descriptor)
        yield content, metadata, lambda: lease_broken, descriptor
    finally:
        if lease_held:
            try:
                fcntl.fcntl(descriptor, fcntl.F_SETLEASE, fcntl.F_UNLCK)
            except OSError:
                pass
        if handler_installed and previous_handler is not None:
            try:
                signal.signal(signal.SIGIO, previous_handler)
            except ValueError:
                pass
        os.close(descriptor)


def _acquire_additional_write_lease_at(
    parent_fd: int,
    target_name: str,
) -> tuple[int, os.stat_result]:
    flags = os.O_RDWR
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(target_name, flags, dir_fd=parent_fd)
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise PathError("safe filesystem target must be one regular file")
        fcntl.fcntl(descriptor, fcntl.F_SETOWN, os.getpid())
        fcntl.fcntl(descriptor, fcntl.F_SETLEASE, fcntl.F_WRLCK)
        return descriptor, metadata
    except (AttributeError, OSError, ValueError) as error:
        if "descriptor" in locals():
            os.close(descriptor)
        raise PathError(
            "safe filesystem target is open or leases are unavailable"
        ) from error


def _release_write_lease(descriptor: int) -> None:
    try:
        fcntl.fcntl(descriptor, fcntl.F_SETLEASE, fcntl.F_UNLCK)
    except OSError:
        pass
    os.close(descriptor)


def _read_installed_prepared(
    parent_fd: int,
    target_name: str,
    descriptor: int,
    prepared: os.stat_result,
) -> tuple[bytes, os.stat_result]:
    try:
        named = os.stat(
            target_name,
            dir_fd=parent_fd,
            follow_symlinks=False,
        )
    except OSError as error:
        raise PathError("safe filesystem installed target is missing") from error
    content, metadata = _read_descriptor(descriptor)
    try:
        named_after = os.stat(
            target_name,
            dir_fd=parent_fd,
            follow_symlinks=False,
        )
    except OSError as error:
        raise PathError("safe filesystem installed target is missing") from error
    if (
        not _same_file_identity(named, prepared)
        or not _same_file_identity(named_after, prepared)
        or not _same_file_identity(metadata, prepared)
    ):
        raise PathError("safe filesystem installed target changed")
    return content, metadata


def atomic_replace_if_unchanged(
    root: Path,
    target: Path,
    expected_sha256: str,
    content: bytes,
    mode: int = 0o644,
) -> None:
    """Exchange a file only when the displaced bytes match the approved bytes."""

    with _open_relative_parent(root, target, create_parents=False) as (
        parent_fd,
        target_name,
    ):
        with _leased_regular_at(parent_fd, target_name) as (
            before,
            metadata,
            lease_was_broken,
            leased_descriptor,
        ):
            if hashlib.sha256(before).hexdigest() != expected_sha256:
                raise PathError("safe filesystem target changed after approval")
            temporary_name = _write_temp_at(parent_fd, target_name, content, mode)
            preserve_temporary = False
            prepared_descriptor: int | None = None
            try:
                prepared_descriptor, prepared = _acquire_additional_write_lease_at(
                    parent_fd,
                    temporary_name,
                )
                prepared_name = os.stat(
                    temporary_name,
                    dir_fd=parent_fd,
                    follow_symlinks=False,
                )
                if not _same_file_identity(prepared_name, prepared):
                    raise PathError("safe filesystem temporary file changed")
                current = os.stat(
                    target_name,
                    dir_fd=parent_fd,
                    follow_symlinks=False,
                )
                if lease_was_broken() or not _same_file_identity(current, metadata):
                    raise PathError("safe filesystem target changed after approval")
                _rename_exchange_at(parent_fd, temporary_name, target_name)
                preserve_temporary = True
                if lease_was_broken():
                    raise PathError(
                        "safe filesystem conflict recovery was preserved"
                    )
                displaced_name_metadata = os.stat(
                    temporary_name,
                    dir_fd=parent_fd,
                    follow_symlinks=False,
                )
                if not _same_file_identity(displaced_name_metadata, metadata):
                    preserve_temporary = True
                    os.fsync(parent_fd)
                    raise PathError(
                        "safe filesystem conflict recovery was preserved"
                    )
                displaced, displaced_metadata = _read_descriptor(leased_descriptor)
                if (
                    not _same_file_identity(displaced_metadata, metadata)
                    or hashlib.sha256(displaced).hexdigest() != expected_sha256
                ):
                    if lease_was_broken():
                        preserve_temporary = True
                        raise PathError(
                            "safe filesystem conflict recovery was preserved"
                        )
                    try:
                        _rename_exchange_at(parent_fd, temporary_name, target_name)
                    except PathError:
                        preserve_temporary = True
                        raise PathError(
                            "safe filesystem conflict recovery was preserved"
                        )
                    restored_temp = os.stat(
                        temporary_name,
                        dir_fd=parent_fd,
                        follow_symlinks=False,
                    )
                    if not _same_file_identity(restored_temp, prepared):
                        preserve_temporary = True
                        raise PathError(
                            "safe filesystem conflict recovery was preserved"
                        )
                    os.fsync(parent_fd)
                    preserve_temporary = False
                    raise PathError("safe filesystem target changed after approval")
                installed, installed_metadata = _read_installed_prepared(
                    parent_fd,
                    target_name,
                    prepared_descriptor,
                    prepared,
                )
                if (
                    lease_was_broken()
                    or not _same_file_identity(installed_metadata, prepared)
                    or installed != content
                ):
                    preserve_temporary = True
                    os.fsync(parent_fd)
                    raise PathError(
                        "safe filesystem conflict recovery was preserved"
                    )
                displaced_now, displaced_now_metadata = _read_descriptor(
                    leased_descriptor
                )
                if (
                    not _same_file_identity(displaced_now_metadata, metadata)
                    or hashlib.sha256(displaced_now).hexdigest() != expected_sha256
                ):
                    preserve_temporary = True
                    os.fsync(parent_fd)
                    raise PathError(
                        "safe filesystem conflict recovery was preserved"
                    )
                final_displaced_name = os.stat(
                    temporary_name,
                    dir_fd=parent_fd,
                    follow_symlinks=False,
                )
                if (
                    lease_was_broken()
                    or not _same_file_identity(final_displaced_name, metadata)
                ):
                    preserve_temporary = True
                    os.fsync(parent_fd)
                    raise PathError(
                        "safe filesystem conflict recovery was preserved"
                    )
                os.unlink(temporary_name, dir_fd=parent_fd)
                os.fsync(parent_fd)
            finally:
                if not preserve_temporary:
                    try:
                        os.unlink(temporary_name, dir_fd=parent_fd)
                        os.fsync(parent_fd)
                    except FileNotFoundError:
                        pass
                if prepared_descriptor is not None:
                    _release_write_lease(prepared_descriptor)


def _same_file_identity(first: os.stat_result, second: os.stat_result) -> bool:
    return (
        stat.S_ISREG(first.st_mode)
        and stat.S_ISREG(second.st_mode)
        and first.st_nlink == 1
        and second.st_nlink == 1
        and (first.st_dev, first.st_ino) == (second.st_dev, second.st_ino)
    )


def _rename_exchange_at(parent_fd: int, first: str, second: str) -> None:
    """Atomically exchange two names in one anchored Linux directory."""

    try:
        renameat2 = ctypes.CDLL(None, use_errno=True).renameat2
    except AttributeError as error:
        raise PathError("safe filesystem atomic exchange is unavailable") from error
    renameat2.argtypes = (
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    )
    renameat2.restype = ctypes.c_int
    result = renameat2(
        parent_fd,
        os.fsencode(first),
        parent_fd,
        os.fsencode(second),
        2,
    )
    if result != 0:
        raise PathError("safe filesystem atomic exchange failed")
