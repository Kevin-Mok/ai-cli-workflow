"""Read-only, deterministic inventory for text-only migration candidates."""

from __future__ import annotations

import os
import re
import stat
from pathlib import Path
from typing import Any, Sequence

from .migration_common import (
    MAX_TEXT_BYTES,
    MigrationError,
    canonical_source,
    is_canonical_relative,
    paths_overlap,
    secure_source_bytes,
    sha256_bytes,
    source_name_reason,
)
from .paths import resolve_repo
from .content_security import redact


HEADING_RE = re.compile(r"(?m)^#\s+(.+?)\s*$")


def source_roots(values: Sequence[str]) -> list[Path]:
    if not values:
        raise MigrationError("at least one migration source is required")
    repo = resolve_repo()
    roots = sorted({canonical_source(value, repo) for value in values})
    if len(roots) != len(values):
        raise MigrationError("migration source roots overlap or repeat")
    for index, first in enumerate(roots):
        for second in roots[index + 1 :]:
            if paths_overlap(first, second):
                raise MigrationError("migration source roots overlap or repeat")
    return roots


def rejected(
    source_id: str, path: str, entry_type: str, reason: str
) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "path": path,
        "type": entry_type,
        "status": "rejected",
        "reason": reason,
    }


def title_for(text: str, path: Path) -> str:
    heading = HEADING_RE.search(text)
    title = heading.group(1).strip() if heading else path.stem
    return title[:200]


def inventory_source(root: Path, source_id: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if (root / ".git").exists():
        return [rejected(source_id, ".", "directory", "nested_git_repository")]
    for directory, directory_names, file_names in os.walk(root, followlinks=False):
        parent = Path(directory)
        retained: list[str] = []
        for name in sorted(directory_names):
            path = parent / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                entries.append(rejected(source_id, relative, "directory", "symlink"))
            elif (reason := source_name_reason(name, directory=True)) is not None:
                entries.append(rejected(source_id, relative, "directory", reason))
            elif (path / ".git").exists():
                entries.append(
                    rejected(source_id, relative, "directory", "nested_git_repository")
                )
            else:
                retained.append(name)
        directory_names[:] = retained

        for name in sorted(file_names):
            path = parent / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                entries.append(rejected(source_id, relative, "file", "symlink"))
                continue
            try:
                metadata = path.lstat()
            except OSError:
                entries.append(
                    rejected(source_id, relative, "file", "non_regular_file")
                )
                continue
            if not stat.S_ISREG(metadata.st_mode):
                entries.append(
                    rejected(source_id, relative, "file", "non_regular_file")
                )
                continue
            if metadata.st_nlink != 1:
                entries.append(rejected(source_id, relative, "file", "hard_link"))
                continue
            reason = source_name_reason(name, directory=False)
            if reason is not None:
                entries.append(rejected(source_id, relative, "file", reason))
                continue
            if metadata.st_size >= MAX_TEXT_BYTES:
                entries.append(rejected(source_id, relative, "file", "too_large"))
                continue
            try:
                content = secure_source_bytes(root, relative, metadata.st_size)
            except MigrationError:
                entries.append(
                    rejected(source_id, relative, "file", "non_regular_file")
                )
                continue
            try:
                text = content.decode("utf-8")
            except UnicodeError:
                entries.append(rejected(source_id, relative, "file", "invalid_utf8"))
                continue
            if "\x00" in text:
                entries.append(rejected(source_id, relative, "file", "nul_byte"))
                continue
            if redact(text) != text:
                entries.append(rejected(source_id, relative, "file", "likely_secret"))
                continue
            entries.append(
                {
                    "source_id": source_id,
                    "path": relative,
                    "type": "text",
                    "status": "eligible",
                    "bytes": len(content),
                    "sha256": sha256_bytes(content),
                    "title": title_for(text, path),
                }
            )
    return entries


def build_inventory(source_values: Sequence[str]) -> dict[str, Any]:
    roots = source_roots(source_values)
    sources = [
        {"id": f"source-{index:03d}", "path": str(root)}
        for index, root in enumerate(roots, start=1)
    ]
    entries: list[dict[str, Any]] = []
    for source in sources:
        entries.extend(inventory_source(Path(source["path"]), source["id"]))
    entries.sort(key=lambda item: (item["source_id"], item["path"]))
    eligible = [entry for entry in entries if entry["status"] == "eligible"]
    return {
        "schema_version": 1,
        "command": "migrate inventory",
        "sources": sources,
        "entries": entries,
        "summary": {
            "eligible_files": len(eligible),
            "eligible_bytes": sum(entry["bytes"] for entry in eligible),
            "rejected_entries": len(entries) - len(eligible),
        },
    }


def validate_inventory(inventory: dict[str, Any]) -> None:
    if type(inventory.get("schema_version")) is not int or inventory.get(
        "schema_version"
    ) != 1:
        raise MigrationError("inventory schema_version must be 1")
    if inventory.get("command") != "migrate inventory":
        raise MigrationError("migration inventory command is invalid")
    if set(inventory) != {
        "schema_version",
        "command",
        "sources",
        "entries",
        "summary",
    }:
        raise MigrationError("migration inventory fields are invalid")
    if not isinstance(inventory["sources"], list) or not isinstance(
        inventory["entries"], list
    ):
        raise MigrationError("migration inventory collections are invalid")
    source_ids: set[str] = set()
    for source in inventory["sources"]:
        if not isinstance(source, dict) or set(source) != {"id", "path"}:
            raise MigrationError("migration inventory source is invalid")
        if not isinstance(source["id"], str) or source["id"] in source_ids:
            raise MigrationError("migration inventory source IDs are invalid")
        path_value = source.get("path")
        if not isinstance(path_value, str) or not Path(path_value).is_absolute():
            raise MigrationError("migration inventory source path is invalid")
        source_ids.add(source["id"])
    for entry in inventory["entries"]:
        if not isinstance(entry, dict) or entry.get("source_id") not in source_ids:
            raise MigrationError("migration inventory entry is invalid")
        relative = entry.get("path")
        if not is_canonical_relative(relative):
            raise MigrationError("migration inventory entry path is invalid")
        if entry.get("status") == "eligible":
            if set(entry) != {
                "source_id",
                "path",
                "type",
                "status",
                "bytes",
                "sha256",
                "title",
            }:
                raise MigrationError("eligible migration inventory entry is invalid")
            if (
                entry.get("type") != "text"
                or type(entry.get("bytes")) is not int
                or not 0 <= entry["bytes"] < MAX_TEXT_BYTES
                or not re.fullmatch(r"[0-9a-f]{64}", str(entry.get("sha256", "")))
                or not isinstance(entry.get("title"), str)
            ):
                raise MigrationError("eligible migration inventory entry is invalid")
        elif entry.get("status") == "rejected":
            if set(entry) != {
                "source_id",
                "path",
                "type",
                "status",
                "reason",
            }:
                raise MigrationError("rejected migration inventory entry is invalid")
        else:
            raise MigrationError("migration inventory entry status is invalid")
    eligible = [
        entry for entry in inventory["entries"] if entry.get("status") == "eligible"
    ]
    expected_summary = {
        "eligible_files": len(eligible),
        "eligible_bytes": sum(entry["bytes"] for entry in eligible),
        "rejected_entries": len(inventory["entries"]) - len(eligible),
    }
    if inventory.get("summary") != expected_summary:
        raise MigrationError("migration inventory summary is invalid")


_validate_inventory = validate_inventory
