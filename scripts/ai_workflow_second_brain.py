"""Compose Second Brain findings into the repository workflow doctor."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any


def second_brain_findings(repo: Path) -> list[dict[str, Any]]:
    """Return stable Second Brain findings when the audited repo has a vault."""

    if not (repo / "second-brain").is_dir() or not (repo / ".git").exists():
        return []
    from second_brain.doctor import build_report as build_second_brain_report

    previous = os.environ.get("SECOND_BRAIN_REPO_ROOT")
    os.environ["SECOND_BRAIN_REPO_ROOT"] = str(repo)
    try:
        return build_second_brain_report()["findings"]
    finally:
        if previous is None:
            os.environ.pop("SECOND_BRAIN_REPO_ROOT", None)
        else:
            os.environ["SECOND_BRAIN_REPO_ROOT"] = previous
