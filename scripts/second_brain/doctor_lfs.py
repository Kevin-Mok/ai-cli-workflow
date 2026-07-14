"""Git LFS attribute inspection for Second Brain doctor checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .safe_contract import PathError


def lfs_tracked(repo: Path, path: Path) -> bool:
    relative = path.relative_to(repo).as_posix()
    try:
        completed = subprocess.run(
            ["git", "check-attr", "filter", "--", relative],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise PathError("Git LFS attributes could not be inspected") from error
    return completed.stdout.rstrip().endswith(": lfs")
