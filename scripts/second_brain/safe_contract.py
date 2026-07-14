"""Shared exception and lexical-boundary contract for safe filesystem work."""

from __future__ import annotations

from pathlib import Path


class PathError(RuntimeError):
    """A path or repository boundary is invalid."""


class TargetExistsError(PathError):
    """An exclusive target already exists."""


def relative_target_parts(root: Path, target: Path) -> tuple[str, ...]:
    if not root.is_absolute() or not target.is_absolute():
        raise PathError("safe filesystem boundary and target must be absolute")
    try:
        relative = target.relative_to(root)
    except ValueError as error:
        raise PathError("safe filesystem target escapes its boundary") from error
    if not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        raise PathError("safe filesystem target is invalid")
    return relative.parts
