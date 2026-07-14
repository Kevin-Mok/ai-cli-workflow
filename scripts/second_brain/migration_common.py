"""Shared security, hashing, and source-read primitives for migration."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

from .content_security import likely_secret_name, redact
from .paths import PathError, safe_vault_path
from .state_private import private_file_bytes


MAX_TEXT_BYTES = 1_000_000
MAX_CONTROL_FILE_BYTES = 20_000_000
APP_DATA_DIRECTORIES = {
    ".cache",
    ".git",
    ".idea",
    ".obsidian",
    ".vscode",
    "__pycache__",
    "cache",
    "logs",
    "node_modules",
}
class MigrationError(ValueError):
    """Migration input or state is unsafe, stale, or malformed."""


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def migration_entry_id(source_root: Path, relative: str) -> str:
    """Return the stable identity shared by migration plans and ledgers."""

    identity = f"{source_root}\0{relative}".encode("utf-8")
    return sha256_bytes(identity)[:16]


def migration_destination_path(repo: Path, relative: str) -> Path:
    """Resolve a canonical Markdown destination inside the import archive."""

    parts = Path(relative).parts
    if (
        len(parts) < 4
        or parts[:2] != ("06 Archive", "Imports")
        or Path(relative).suffix.casefold() != ".md"
    ):
        raise MigrationError("migration destination is outside the import archive")
    try:
        return safe_vault_path(repo, relative)
    except PathError as error:
        raise MigrationError("migration destination path is unsafe") from error


def approval_sha256(value: dict[str, Any]) -> str:
    unsigned = dict(value)
    unsigned.pop("approval_sha256", None)
    return sha256_bytes(canonical_bytes(unsigned))


def wrapped_import(content: bytes, source_sha256: str, date_value: str) -> bytes:
    header = (
        "---\n"
        "tags: [archive, imported]\n"
        "status: archived\n"
        f"date: {date_value}\n"
        "visibility: public-sanitized\n"
        f"source_sha256: {source_sha256}\n"
        "---\n\n"
    ).encode("utf-8")
    return header + content


def load_json_file(path_value: str) -> dict[str, Any]:
    path = Path(path_value).expanduser()
    try:
        metadata = path.lstat()
    except OSError as error:
        raise MigrationError("migration control path is not a readable file") from error
    if path.is_symlink() or not stat.S_ISREG(metadata.st_mode):
        raise MigrationError("migration control path is not a regular file")
    if metadata.st_size >= MAX_CONTROL_FILE_BYTES:
        raise MigrationError("migration control file is too large")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise MigrationError("migration control file must be valid UTF-8 JSON") from error
    if not isinstance(value, dict):
        raise MigrationError("migration control JSON root must be an object")
    return value


def load_private_json_file(
    root: Path,
    path: Path,
) -> tuple[dict[str, Any], bytes] | None:
    try:
        content = private_file_bytes(
            root,
            path,
            max_bytes=MAX_CONTROL_FILE_BYTES,
        )
    except PathError as error:
        raise MigrationError("migration ledger path is unsafe") from error
    if content is None:
        return None
    try:
        value = json.loads(content.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise MigrationError("migration ledger must be valid private JSON") from error
    if not isinstance(value, dict):
        raise MigrationError("migration ledger JSON root must be an object")
    return value, content


def paths_overlap(first: Path, second: Path) -> bool:
    return first == second or first in second.parents or second in first.parents


def is_canonical_relative(value: object) -> bool:
    if not isinstance(value, str):
        return False
    path = Path(value)
    return (
        bool(path.parts)
        and not path.is_absolute()
        and ".." not in path.parts
        and path.as_posix() == value
    )


def state_base() -> Path:
    raw = os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local" / "state"))
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        raise MigrationError("XDG_STATE_HOME must be absolute")
    return candidate.resolve(strict=False)


def canonical_source(raw: str, repo: Path) -> Path:
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        raise MigrationError("migration source path must be absolute")
    if candidate.is_symlink():
        raise MigrationError("migration source root must not be a symlink")
    lexical = Path(os.path.abspath(str(candidate)))
    try:
        resolved = lexical.resolve(strict=True)
    except OSError as error:
        raise MigrationError("migration source root is not a readable directory") from error
    if resolved != lexical:
        raise MigrationError("migration source root must not contain symlinks")
    if not resolved.is_dir():
        raise MigrationError("migration source root must be a directory")

    home = Path.home().resolve(strict=False)
    state = state_base()
    coding = Path("/home/example/coding").resolve(strict=False)
    protected = (repo.resolve(), (repo / "second-brain").resolve(), state, coding)
    if any(paths_overlap(resolved, location) for location in protected):
        raise MigrationError("migration source overlaps a protected location")
    if resolved == home or resolved in home.parents:
        raise MigrationError("migration source overlaps a protected location")
    return resolved


def source_name_reason(name: str, *, directory: bool) -> str | None:
    lowered = name.casefold()
    if directory:
        if lowered == ".git":
            return "nested_git_repository"
        if lowered in APP_DATA_DIRECTORIES:
            return "app_data"
        return None
    if likely_secret_name(name):
        return "secret_name"
    if Path(name).suffix.casefold() == ".log":
        return "log_file"
    return None


def _contains_git_directory(directory_fd: int) -> bool:
    try:
        os.stat(".git", dir_fd=directory_fd, follow_symlinks=False)
    except FileNotFoundError:
        return False
    except OSError as error:
        raise MigrationError("migration source changed during inspection") from error
    return True


def secure_source_bytes(
    source_root: Path,
    relative: str,
    expected_size: int,
) -> bytes:
    path = Path(relative)
    if (
        path.is_absolute()
        or not path.parts
        or ".." in path.parts
        or source_name_reason(path.name, directory=False) is not None
    ):
        raise MigrationError("migration source violates eligibility policy")
    directory_flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        directory_flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        directory_flags |= os.O_NOFOLLOW
    try:
        current = os.open(source_root, directory_flags)
    except OSError as error:
        raise MigrationError("migration source changed during inspection") from error
    try:
        if _contains_git_directory(current):
            raise MigrationError("migration source violates eligibility policy")
        for part in path.parts[:-1]:
            if source_name_reason(part, directory=True) is not None:
                raise MigrationError("migration source violates eligibility policy")
            try:
                child = os.open(part, directory_flags, dir_fd=current)
            except OSError as error:
                raise MigrationError(
                    "migration source changed during inspection"
                ) from error
            metadata = os.fstat(child)
            if not stat.S_ISDIR(metadata.st_mode):
                os.close(child)
                raise MigrationError("migration source changed during inspection")
            os.close(current)
            current = child
            if _contains_git_directory(current):
                raise MigrationError("migration source violates eligibility policy")

        flags = os.O_RDONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            descriptor = os.open(path.name, flags, dir_fd=current)
        except OSError as error:
            raise MigrationError("migration source file could not be read safely") from error
        try:
            metadata = os.fstat(descriptor)
            if (
                not stat.S_ISREG(metadata.st_mode)
                or metadata.st_nlink != 1
                or metadata.st_size != expected_size
                or metadata.st_size >= MAX_TEXT_BYTES
            ):
                raise MigrationError("migration source file changed during inspection")
            chunks: list[bytes] = []
            remaining = MAX_TEXT_BYTES + 1
            while remaining > 0:
                chunk = os.read(descriptor, min(1024 * 1024, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            return b"".join(chunks)
        finally:
            os.close(descriptor)
    finally:
        os.close(current)


def destination_source_bytes(
    source_root: Path, relative: str, expected_size: int, expected_sha: str
) -> bytes:
    try:
        content = secure_source_bytes(source_root, relative, expected_size)
    except MigrationError as error:
        raise MigrationError("migration source changed after inventory") from error
    try:
        text = content.decode("utf-8")
    except UnicodeError as error:
        raise MigrationError("migration source changed after inventory") from error
    if "\x00" in text or redact(text) != text or sha256_bytes(content) != expected_sha:
        raise MigrationError("migration source changed after inventory")
    return content
