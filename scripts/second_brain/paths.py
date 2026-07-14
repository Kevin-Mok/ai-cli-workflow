"""Repository, state, date, containment, locking, and atomic-write helpers."""

from __future__ import annotations

import fcntl
import os
import stat
import subprocess
import tempfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator
from zoneinfo import ZoneInfo

from .safe_contract import PathError, TargetExistsError
from .safe_create import atomic_create
from .safe_files import atomic_replace_if_unchanged, regular_file_bytes


class LockError(RuntimeError):
    """A mutation lock is already held."""


def resolve_repo() -> Path:
    override = os.environ.get("SECOND_BRAIN_REPO_ROOT")
    if override:
        repo = _validated_source_repo(Path(override).expanduser())
    else:
        repo = _repo_from_module()
        if repo is None:
            repo = _repo_from_chezmoi()
    return repo


def _known_repo_without_external_lookup() -> Path | None:
    override = os.environ.get("SECOND_BRAIN_REPO_ROOT")
    if override:
        try:
            return _validated_source_repo(Path(override).expanduser())
        except PathError:
            pass
    try:
        return _repo_from_module()
    except PathError:
        return None


def _repo_from_module() -> Path | None:
    module = Path(__file__).resolve()
    for parent in module.parents:
        if (parent / ".git").exists():
            return _validated_source_repo(parent)
    return None


def _repo_from_chezmoi() -> Path:
    applied_front_door = Path.home() / "second-brain" / "README.md"
    try:
        completed = subprocess.run(
            ["chezmoi", "source-path", str(applied_front_door)],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise PathError("Second Brain repository could not be resolved") from error
    front_door = Path(completed.stdout.strip()).expanduser()
    if not front_door.is_absolute() or front_door.is_symlink():
        raise PathError("chezmoi returned an invalid Second Brain path")
    if front_door.name != "README.md" or front_door.parent.name != "second-brain":
        raise PathError("chezmoi returned an invalid Second Brain path")
    return _validated_source_repo(front_door.parents[1])


def _validated_source_repo(candidate: Path) -> Path:
    if not candidate.is_absolute():
        raise PathError("Second Brain repository path must be absolute")
    lexical = candidate.expanduser().absolute()
    try:
        resolved = lexical.resolve(strict=True)
    except OSError as error:
        raise PathError("Second Brain repository could not be resolved") from error
    if resolved != lexical:
        raise PathError(
            "Second Brain repository path must not contain symlinks or aliases"
        )
    vault = lexical / "second-brain"
    if not (lexical / ".git").exists():
        raise PathError("Second Brain source checkout is not a Git repository")
    if vault.is_symlink():
        raise PathError("Second Brain vault root must not be a symlink")
    front_door = vault / "README.md"
    if not front_door.is_file() or front_door.is_symlink():
        raise PathError("Second Brain repository could not be resolved")
    return resolved


def state_root(*, require_repository: bool = True) -> Path:
    base = Path(
        os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local" / "state"))
    ).expanduser()
    if not base.is_absolute():
        raise PathError("XDG_STATE_HOME must be an absolute path")
    if base.resolve(strict=False) != base.absolute():
        raise PathError("XDG_STATE_HOME must not contain symlinks")
    root = base / "second-brain"
    if root.is_symlink():
        raise PathError("Second Brain state root must not be a symlink")
    resolved_root = root.resolve(strict=False)
    repo = (
        resolve_repo()
        if require_repository
        else _known_repo_without_external_lookup()
    )
    protected_paths = [Path(__file__).resolve().parents[1]]
    if repo is not None:
        protected_paths.extend((repo.resolve(), (repo / "second-brain").resolve()))
    for protected in protected_paths:
        if _paths_overlap(resolved_root, protected):
            raise PathError("Second Brain state must stay outside the repository")
    if (root / "README.md").is_file():
        raise PathError("Second Brain state must not reuse a vault directory")
    return root


def _paths_overlap(first: Path, second: Path) -> bool:
    return (
        first == second
        or first in second.parents
        or second in first.parents
    )


def local_now() -> datetime:
    override = os.environ.get("SECOND_BRAIN_NOW")
    if override:
        try:
            parsed = datetime.fromisoformat(override)
        except ValueError as error:
            raise PathError("SECOND_BRAIN_NOW must be ISO 8601") from error
        if parsed.tzinfo is None:
            raise PathError("SECOND_BRAIN_NOW must include a UTC offset")
        return parsed.astimezone(ZoneInfo("America/Toronto"))
    return datetime.now(ZoneInfo("America/Toronto"))


def safe_vault_path(repo: Path, relative: str) -> Path:
    if not relative or Path(relative).is_absolute():
        raise PathError("target path must be vault-relative")
    vault_path = repo / "second-brain"
    if vault_path.is_symlink() or not vault_path.is_dir():
        raise PathError("Second Brain vault root is missing or invalid")
    vault = vault_path.resolve()
    relative_path = Path(relative)
    current = vault_path
    for part in relative_path.parts[:-1]:
        current /= part
        if current.is_symlink():
            raise PathError("target path must not contain symlinks")
    candidate = vault_path.joinpath(*relative_path.parts)
    resolved_parent = candidate.parent.resolve()
    if resolved_parent != vault and vault not in resolved_parent.parents:
        raise PathError("target path escapes the vault")
    if candidate.is_symlink():
        raise PathError("target path must not be a symlink")
    return candidate


def ensure_private_directory(
    path: Path,
    *,
    require_repository: bool = True,
) -> None:
    root = state_root(require_repository=require_repository)
    try:
        relative = path.relative_to(root)
    except ValueError as error:
        raise PathError("private state path escapes the state root") from error
    current = root
    for part in (".", *relative.parts):
        if part != ".":
            current /= part
        if current.is_symlink():
            raise PathError("private state directories must not be symlinks")
        try:
            current.mkdir(parents=True, exist_ok=True, mode=0o700)
            current.chmod(0o700)
        except OSError as error:
            raise PathError("private state directory could not be prepared") from error


def atomic_write(path: Path, content: str, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


@contextmanager
def mutation_lock() -> Iterator[None]:
    lock_dir = state_root() / "locks"
    ensure_private_directory(lock_dir)
    lock_path = lock_dir / "mutation.lock"
    if lock_path.is_symlink():
        raise PathError("private state lock must not be a symlink")
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(lock_path, flags, 0o600)
    except OSError as error:
        raise PathError("private state lock could not be opened") from error
    with os.fdopen(descriptor, "a+", encoding="utf-8") as stream:
        metadata = os.fstat(stream.fileno())
        if not stat.S_ISREG(metadata.st_mode):
            raise PathError("private state lock must be a regular file")
        if hasattr(os, "getuid") and metadata.st_uid != os.getuid():
            raise PathError("private state lock must be owned by the current user")
        os.fchmod(stream.fileno(), 0o600)
        try:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise LockError(
                "another Second Brain mutation is already running"
            ) from error
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
