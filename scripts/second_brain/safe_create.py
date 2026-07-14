"""Portable-name-aware, exclusive regular-file creation."""

from __future__ import annotations

import os
import stat
from pathlib import Path

from .safe_contract import PathError, TargetExistsError
from .safe_files import (
    _open_relative_parent,
    _portable_name_collision,
    _write_temp_at,
)


def _validate_portable_ancestors(
    ancestors: list[tuple[int, str, os.stat_result, bool]],
) -> None:
    for parent_fd, name, expected, _created in ancestors:
        if _portable_name_collision(parent_fd, name):
            raise TargetExistsError(
                "safe filesystem parent has a portable-name collision"
            )
        try:
            current = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except OSError as error:
            raise PathError("safe filesystem parent changed during creation") from error
        if not (
            stat.S_ISDIR(current.st_mode)
            and stat.S_ISDIR(expected.st_mode)
            and (current.st_dev, current.st_ino)
            == (expected.st_dev, expected.st_ino)
        ):
            raise PathError("safe filesystem parent changed during creation")


def atomic_create(
    root: Path,
    target: Path,
    content: bytes,
    mode: int = 0o644,
    *,
    portable_unique: bool = False,
) -> None:
    """Atomically create a regular file without following or replacing names."""

    ancestors: list[tuple[int, str, os.stat_result, bool]] = []
    with _open_relative_parent(
        root,
        target,
        create_parents=True,
        portable_unique=portable_unique,
        tracked_ancestors=ancestors,
    ) as (
        parent_fd,
        target_name,
    ):
        if portable_unique and _portable_name_collision(parent_fd, target_name):
            raise TargetExistsError(
                "safe filesystem target has a portable-name collision"
            )
        temporary_name = _write_temp_at(parent_fd, target_name, content, mode)
        prepared = os.stat(
            temporary_name,
            dir_fd=parent_fd,
            follow_symlinks=False,
        )
        try:
            try:
                os.link(
                    temporary_name,
                    target_name,
                    src_dir_fd=parent_fd,
                    dst_dir_fd=parent_fd,
                    follow_symlinks=False,
                )
            except FileExistsError as error:
                raise TargetExistsError(
                    "safe filesystem target already exists"
                ) from error
            except OSError as error:
                raise PathError(
                    "safe filesystem target could not be created"
                ) from error
            _created_target_metadata(parent_fd, target_name, prepared)
            if portable_unique and _portable_name_collision(parent_fd, target_name):
                _remove_created_target(parent_fd, target_name, prepared)
                raise TargetExistsError(
                    "safe filesystem target has a portable-name collision"
                )
            if portable_unique:
                try:
                    _validate_portable_ancestors(ancestors)
                except (PathError, TargetExistsError):
                    _remove_created_target(parent_fd, target_name, prepared)
                    raise
            _created_target_metadata(parent_fd, target_name, prepared)
            os.unlink(temporary_name, dir_fd=parent_fd)
            os.fsync(parent_fd)
            _created_target_metadata(parent_fd, target_name, prepared)
            if portable_unique:
                try:
                    _validate_portable_ancestors(ancestors)
                except (PathError, TargetExistsError):
                    _remove_created_target(parent_fd, target_name, prepared)
                    raise
        finally:
            try:
                os.unlink(temporary_name, dir_fd=parent_fd)
            except FileNotFoundError:
                pass


def _created_target_metadata(
    parent_fd: int,
    target_name: str,
    prepared: os.stat_result,
) -> os.stat_result:
    try:
        current = os.stat(
            target_name,
            dir_fd=parent_fd,
            follow_symlinks=False,
        )
    except OSError as error:
        raise PathError("safe filesystem target changed during creation") from error
    if not _same_regular_inode(current, prepared):
        raise PathError("safe filesystem target changed during creation")
    return current


def _remove_created_target(
    parent_fd: int,
    target_name: str,
    prepared: os.stat_result,
) -> None:
    _created_target_metadata(parent_fd, target_name, prepared)
    os.unlink(target_name, dir_fd=parent_fd)
    os.fsync(parent_fd)


def _same_regular_inode(first: os.stat_result, second: os.stat_result) -> bool:
    return (
        stat.S_ISREG(first.st_mode)
        and stat.S_ISREG(second.st_mode)
        and (first.st_dev, first.st_ino) == (second.st_dev, second.st_ino)
    )
