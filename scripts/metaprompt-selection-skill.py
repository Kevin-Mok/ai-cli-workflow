#!/usr/bin/env python3
"""Stage a verified local native skill, or remove an unchanged staged copy.

No downloads, model calls, default changes, or installed-skill edits are implicit.
Destination's parent directory must already exist and contain no symlink parents.
Linux renameat2 provides atomic publication without replacing an existing target.
"""
from __future__ import annotations

import argparse
import ctypes
import errno
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile

DEFAULT_ROOT = Path(__file__).resolve().parents[1] / 'benchmarks/metaprompt-selection'


def _safe_absolute(path: Path) -> Path:
    path = Path(path).expanduser()
    if '..' in path.parts:
        raise ValueError('Parent traversal is forbidden')
    path = path.absolute()
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError('Symlinks are forbidden: ' + str(part))
    return path


def _relative(text: str) -> Path:
    if not isinstance(text, str) or not text or '\\' in text:
        raise ValueError('Invalid inventory path')
    path = Path(text)
    if path.is_absolute() or '..' in path.parts or not path.parts or str(path) != text:
        raise ValueError('Only canonical relative inventory paths are accepted')
    return path


def _tree(root: Path) -> tuple[set[str], set[str]]:
    if not root.is_dir() or root.is_symlink():
        raise ValueError('Expected a real package directory')
    files, directories = set(), set()
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError('Package contains a symlink')
        relative = str(path.relative_to(root))
        if path.is_file():
            files.add(relative)
        elif path.is_dir():
            directories.add(relative)
        else:
            raise ValueError('Package contains a nonregular entry')
    return files, directories


def _verify(root: Path, hashes: dict[str, str]) -> None:
    expected_dirs = {str(parent) for filename in hashes for parent in Path(filename).parents
                     if str(parent) != '.'}
    files, directories = _tree(root)
    if files != set(hashes) or directories != expected_dirs:
        raise ValueError('Package has missing or extra files/directories')
    for filename, expected in hashes.items():
        if hashlib.sha256((root / filename).read_bytes()).hexdigest() != expected:
            raise ValueError('Pinned hash mismatch: ' + filename)


def _inventory(candidate: str, root: Path) -> tuple[Path, dict[str, str]]:
    root = _safe_absolute(root)
    manifest_path = _safe_absolute(root / 'sources.json')
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('schema_version') != 1:
        raise ValueError('Unsupported source inventory version')
    selected = [value for value in manifest.get('candidates', []) if value.get('id') == candidate]
    if len(selected) != 1 or selected[0].get('eligibility') not in ('eligible', True):
        raise ValueError('Candidate is not a unique eligible pinned finalist')
    source = selected[0]
    entry = _relative(source['entrypoint'])
    if entry.name != 'SKILL.md' or len(entry.parts) < 3 or entry.parts[0] != 'candidates':
        raise ValueError('Entrypoint must belong to a candidates/ package')
    package = _safe_absolute(root / entry.parent)
    hashes = {}
    for filename, expected in source['files'].items():
        relative = _relative(filename)
        if not relative.is_relative_to(entry.parent):
            raise ValueError('Inventory file is outside the selected native package')
        _safe_absolute(root / relative)
        native = str(relative.relative_to(entry.parent))
        if not re.fullmatch('[0-9a-f]{64}', expected):
            raise ValueError('Invalid pinned SHA-256')
        hashes[native] = expected
    if 'SKILL.md' not in hashes or not any(Path(name).name.upper().startswith(('LICENSE', 'COPYING')) for name in hashes):
        raise ValueError('Pinned package must include its native entrypoint and license')
    _verify(package, hashes)
    return package, hashes


def _rename_new(source: Path, destination: Path) -> None:
    """Linux atomic rename with RENAME_NOREPLACE, including empty destinations."""
    libc = ctypes.CDLL(None, use_errno=True)
    rename = getattr(libc, 'renameat2', None)
    if rename is None:
        raise ValueError('Atomic no-replace staging requires Linux renameat2')
    rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    if rename(-100, os.fsencode(source), -100, os.fsencode(destination), 1):
        error = ctypes.get_errno()
        if error in (errno.EEXIST, errno.ENOTEMPTY):
            raise ValueError('Destination already exists; it was preserved')
        raise OSError(error, os.strerror(error))


def _destination(destination: Path, root: Path) -> Path:
    destination = _safe_absolute(destination)
    if destination.is_relative_to(_safe_absolute(root)):
        raise ValueError("Destination must be outside the pinned benchmark source tree")
    if not destination.parent.is_dir():
        raise ValueError('Destination parent must already exist')
    return destination


def stage(candidate: str, destination: Path, root: Path = DEFAULT_ROOT) -> None:
    package, hashes = _inventory(candidate, root)
    destination = _destination(destination, root)
    if destination.exists():
        raise ValueError('Destination already exists; it was preserved')
    with tempfile.TemporaryDirectory(prefix='.skill-stage-', dir=destination.parent) as temp:
        pending = Path(temp) / 'package'
        pending.mkdir()
        for filename in hashes:
            target = pending / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(package / filename, target)
        _verify(pending, hashes)
        _rename_new(pending, destination)


def rollback(candidate: str, destination: Path, root: Path = DEFAULT_ROOT) -> None:
    _, hashes = _inventory(candidate, root)
    destination = _destination(destination, root)
    _verify(destination, hashes)
    # Move the verified directory aside and verify again before deleting. If a
    # concurrent change is detected, restore it without overwriting another path.
    temp = Path(tempfile.mkdtemp(prefix='.skill-rollback-', dir=destination.parent))
    quarantined = temp / 'package'
    try:
        _rename_new(destination, quarantined)
        try:
            _verify(quarantined, hashes)
        except Exception:
            _rename_new(quarantined, destination)
            raise
        shutil.rmtree(quarantined)
    finally:
        # Never remove a quarantined copy if validation/restoration failed.
        if not quarantined.exists():
            temp.rmdir()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('stage', 'rollback'))
    parser.add_argument('--candidate', required=True, help='Eligible ID in the local sources.json')
    parser.add_argument('--destination', required=True, type=Path, help='Explicit new skill directory; parent must exist')
    args = parser.parse_args()
    try:
        (stage if args.action == 'stage' else rollback)(args.candidate, args.destination)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, 'Refused: ' + str(exc) + '\n')
    print(('Staged verified skill: ' if args.action == 'stage' else 'Removed unchanged staged skill: ') + str(args.destination))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
