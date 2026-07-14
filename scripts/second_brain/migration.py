"""Approval-bound planning for deterministic text migration."""

from __future__ import annotations

import os
import re
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from .migration_common import (
    MAX_TEXT_BYTES,
    MigrationError,
    approval_sha256,
    canonical_source,
    canonical_bytes,
    destination_source_bytes,
    is_canonical_relative,
    load_json_file,
    paths_overlap,
    sha256_bytes,
    wrapped_import,
)
from .migration_inventory import build_inventory, validate_inventory
from .paths import local_now, resolve_repo


WINDOWS_DEVICES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}
FORBIDDEN_NAME_RE = re.compile(r"[\x00-\x1f<>:\"/\\|?*]")


def sanitize_component(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value)
    normalized = FORBIDDEN_NAME_RE.sub("-", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip(" .")
    if not normalized or normalized in {".", ".."}:
        normalized = "Untitled"
    if Path(normalized).stem.upper() in WINDOWS_DEVICES:
        normalized = f"{normalized}-file"
    return normalized


def _name_key(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold()


def _unique_component(value: str, used: set[str], *, file_name: bool) -> str:
    candidate = sanitize_component(value)
    if _name_key(candidate) not in used:
        used.add(_name_key(candidate))
        return candidate
    if file_name:
        suffix = Path(candidate).suffix
        stem = candidate[: -len(suffix)] if suffix else candidate
    else:
        stem = candidate
        suffix = ""
    counter = 2
    while True:
        alternate = f"{stem} {counter}{suffix}"
        if _name_key(alternate) not in used:
            used.add(_name_key(alternate))
            return alternate
        counter += 1


def _existing_children(repo: Path) -> dict[str, set[str]]:
    root = repo / "second-brain" / "06 Archive" / "Imports"
    children: dict[str, set[str]] = defaultdict(set)
    if not root.exists():
        return children
    if root.is_symlink() or not root.is_dir():
        raise MigrationError("migration destination root is unsafe")
    vault = repo / "second-brain"
    for directory, directory_names, file_names in os.walk(root, followlinks=False):
        parent = Path(directory)
        parent_key = _name_key(parent.relative_to(vault).as_posix())
        for name in sorted((*directory_names, *file_names)):
            path = parent / name
            if path.is_symlink():
                raise MigrationError("migration destination contains a symlink")
            children[parent_key].add(_name_key(name))
    return children


def build_plan(inventory_path: str) -> dict[str, Any]:
    inventory = load_json_file(inventory_path)
    validate_inventory(inventory)
    repo = resolve_repo()
    date_value = local_now().date().isoformat()
    inventory_hash = sha256_bytes(canonical_bytes(inventory))
    source_by_id: dict[str, Path] = {}
    source_roots: list[Path] = []
    for source in inventory["sources"]:
        root = canonical_source(source["path"], repo)
        if str(root) != source["path"] or any(
            paths_overlap(root, existing) for existing in source_roots
        ):
            raise MigrationError("migration inventory sources changed or overlap")
        source_by_id[source["id"]] = root
        source_roots.append(root)
    children = _existing_children(repo)
    imports_parent = "06 Archive/Imports"
    root_used = children[_name_key(imports_parent)]
    mappings: list[dict[str, Any]] = []
    target_by_source: dict[str, str] = {}
    for source in inventory["sources"]:
        source_name = _unique_component(
            Path(source["path"]).name, root_used, file_name=False
        )
        target = f"{imports_parent}/{source_name}"
        target_by_source[source["id"]] = target
        mappings.append(
            {
                "source_id": source["id"],
                "target": target,
                "reason": "safe_archive_default",
            }
        )

    directory_assignments: dict[tuple[str, tuple[str, ...]], str] = {}
    entries: list[dict[str, Any]] = []
    eligible = sorted(
        (entry for entry in inventory["entries"] if entry["status"] == "eligible"),
        key=lambda entry: (entry["source_id"], entry["path"]),
    )
    for entry in eligible:
        source_id = entry["source_id"]
        relative = Path(entry["path"])
        destination_parent = target_by_source[source_id]
        original_parent: tuple[str, ...] = ()
        for component in relative.parts[:-1]:
            original_parent = (*original_parent, component)
            assignment_key = (source_id, original_parent)
            if assignment_key not in directory_assignments:
                parent_key = _name_key(destination_parent)
                directory_assignments[assignment_key] = _unique_component(
                    component,
                    children[parent_key],
                    file_name=False,
                )
            destination_parent = (
                f"{destination_parent}/{directory_assignments[assignment_key]}"
            )
        file_name = sanitize_component(relative.name)
        if Path(file_name).suffix.casefold() != ".md":
            file_name = f"{file_name}.md"
        file_name = _unique_component(
            file_name,
            children[_name_key(destination_parent)],
            file_name=True,
        )
        destination = f"{destination_parent}/{file_name}"
        source_root = source_by_id[source_id]
        content = destination_source_bytes(
            source_root,
            entry["path"],
            entry["bytes"],
            entry["sha256"],
        )
        wrapped = wrapped_import(content, entry["sha256"], date_value)
        identity = f"{source_root}\0{entry['path']}".encode("utf-8")
        entries.append(
            {
                "entry_id": sha256_bytes(identity)[:16],
                "source_id": source_id,
                "source_path": entry["path"],
                "source_bytes": entry["bytes"],
                "source_sha256": entry["sha256"],
                "destination": destination,
                "destination_sha256": sha256_bytes(wrapped),
            }
        )
    plan: dict[str, Any] = {
        "schema_version": 1,
        "command": "migrate plan",
        "date": date_value,
        "inventory_sha256": inventory_hash,
        "sources": inventory["sources"],
        "mappings": mappings,
        "entries": entries,
        "summary": {
            "files": len(entries),
            "source_bytes": sum(entry["source_bytes"] for entry in entries),
        },
    }
    plan["approval_sha256"] = approval_sha256(plan)
    return plan


def _valid_date(value: object) -> bool:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _valid_relative(value: object) -> bool:
    return is_canonical_relative(value)


def _valid_destination(value: object) -> bool:
    if not _valid_relative(value):
        return False
    assert isinstance(value, str)
    parts = Path(value).parts
    return (
        len(parts) >= 4
        and parts[:2] == ("06 Archive", "Imports")
        and all(sanitize_component(component) == component for component in parts[2:])
        and Path(value).suffix.casefold() == ".md"
    )


def _validate_sources(sources: object) -> set[str]:
    if not isinstance(sources, list) or not sources:
        raise MigrationError("migration plan sources are invalid")
    source_ids: set[str] = set()
    for source in sources:
        if not isinstance(source, dict) or set(source) != {"id", "path"}:
            raise MigrationError("migration plan source is invalid")
        source_id = source.get("id")
        path_value = source.get("path")
        if (
            not isinstance(source_id, str)
            or not source_id
            or source_id in source_ids
            or not isinstance(path_value, str)
            or not Path(path_value).is_absolute()
        ):
            raise MigrationError("migration plan source is invalid")
        source_ids.add(source_id)
    return source_ids


def _validate_mappings(
    mappings: object, source_ids: set[str]
) -> dict[str, tuple[str, ...]]:
    if not isinstance(mappings, list) or len(mappings) != len(source_ids):
        raise MigrationError("migration plan mappings are invalid")
    targets: dict[str, tuple[str, ...]] = {}
    used_targets: set[str] = set()
    for mapping in mappings:
        if not isinstance(mapping, dict) or set(mapping) != {
            "source_id",
            "target",
            "reason",
        }:
            raise MigrationError("migration plan mapping is invalid")
        source_id = mapping.get("source_id")
        target = mapping.get("target")
        target_parts = Path(target).parts if isinstance(target, str) else ()
        target_key = _name_key(str(target))
        if (
            source_id not in source_ids
            or source_id in targets
            or mapping.get("reason") != "safe_archive_default"
            or not is_canonical_relative(target)
            or len(target_parts) != 3
            or target_parts[:2] != ("06 Archive", "Imports")
            or sanitize_component(target_parts[2]) != target_parts[2]
            or target_key in used_targets
        ):
            raise MigrationError("migration plan mapping is invalid")
        targets[source_id] = target_parts
        used_targets.add(target_key)
    if set(targets) != source_ids:
        raise MigrationError("migration plan mappings are invalid")
    return targets


def _validate_destination_namespace(destinations: list[str]) -> None:
    literal_by_key: dict[tuple[str, ...], tuple[str, ...]] = {}
    directory_keys: set[tuple[str, ...]] = set()
    file_keys: set[tuple[str, ...]] = set()
    for destination in destinations:
        parts = Path(destination).parts
        normalized = tuple(_name_key(part) for part in parts)
        for length in range(1, len(parts)):
            key = normalized[:length]
            literal = parts[:length]
            previous = literal_by_key.setdefault(key, literal)
            if previous != literal:
                raise MigrationError(
                    "migration plan destination namespace is invalid"
                )
            directory_keys.add(key)
        file_key = normalized
        previous = literal_by_key.setdefault(file_key, parts)
        if previous != parts:
            raise MigrationError("migration plan destination namespace is invalid")
        file_keys.add(file_key)
    if file_keys & directory_keys:
        raise MigrationError("migration plan destination namespace is invalid")


def validate_plan(plan: dict[str, Any]) -> dict[str, Any]:
    if set(plan) != {
        "schema_version",
        "command",
        "date",
        "inventory_sha256",
        "sources",
        "mappings",
        "entries",
        "summary",
        "approval_sha256",
    }:
        raise MigrationError("migration plan fields are invalid")
    if type(plan.get("schema_version")) is not int or plan.get("schema_version") != 1:
        raise MigrationError("migration plan schema_version must be 1")
    if plan.get("command") != "migrate plan":
        raise MigrationError("migration plan command is invalid")
    if not _valid_date(plan.get("date")):
        raise MigrationError("migration plan date is invalid")
    if not re.fullmatch(r"[0-9a-f]{64}", str(plan.get("inventory_sha256", ""))):
        raise MigrationError("migration plan inventory hash is invalid")
    stored_approval = plan.get("approval_sha256")
    if (
        not isinstance(stored_approval, str)
        or not re.fullmatch(r"[0-9a-f]{64}", stored_approval)
        or stored_approval != approval_sha256(plan)
    ):
        raise MigrationError("migration plan approval hash is invalid")

    source_ids = _validate_sources(plan.get("sources"))
    target_by_source = _validate_mappings(plan.get("mappings"), source_ids)
    entries = plan.get("entries")
    if not isinstance(entries, list):
        raise MigrationError("migration plan entries are invalid")

    entry_ids: set[str] = set()
    destinations: set[str] = set()
    destination_values: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {
            "entry_id",
            "source_id",
            "source_path",
            "source_bytes",
            "source_sha256",
            "destination",
            "destination_sha256",
        }:
            raise MigrationError("migration plan entry is invalid")
        source_id = entry.get("source_id")
        destination = entry.get("destination")
        destination_parts = (
            Path(destination).parts if isinstance(destination, str) else ()
        )
        destination_key = _name_key(str(destination))
        if (
            source_id not in source_ids
            or not _valid_relative(entry.get("source_path"))
            or not _valid_destination(destination)
            or destination_parts[:3] != target_by_source[source_id]
            or not re.fullmatch(r"[0-9a-f]{16}", str(entry.get("entry_id", "")))
            or entry["entry_id"] in entry_ids
            or destination_key in destinations
            or type(entry.get("source_bytes")) is not int
            or not 0 <= entry["source_bytes"] < MAX_TEXT_BYTES
            or not re.fullmatch(r"[0-9a-f]{64}", str(entry.get("source_sha256", "")))
            or not re.fullmatch(
                r"[0-9a-f]{64}", str(entry.get("destination_sha256", ""))
            )
        ):
            raise MigrationError("migration plan entry is invalid")
        entry_ids.add(entry["entry_id"])
        destinations.add(destination_key)
        destination_values.append(destination)

    _validate_destination_namespace(destination_values)

    expected_summary = {
        "files": len(entries),
        "source_bytes": sum(entry["source_bytes"] for entry in entries),
    }
    if plan.get("summary") != expected_summary:
        raise MigrationError("migration plan summary is invalid")
    return plan
