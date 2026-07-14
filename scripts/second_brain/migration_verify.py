"""Standalone validation and checksum verification for migration ledgers."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from .migration import validate_plan
from .migration_common import (
    MAX_TEXT_BYTES,
    MigrationError,
    canonical_source,
    destination_source_bytes,
    is_canonical_relative,
    load_private_json_file,
    migration_destination_path,
    migration_entry_id,
    paths_overlap,
    sha256_bytes,
)
from .paths import PathError, regular_file_bytes, resolve_repo, state_root


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
        and Path(value).suffix.casefold() == ".md"
    )


def _validate_ledger(ledger: dict[str, Any]) -> dict[str, Any]:
    required = {
        "schema_version",
        "kind",
        "approval_sha256",
        "plan",
        "sources",
        "entries",
        "summary",
    }
    if set(ledger) != required or ledger.get("kind") != (
        "second-brain-migration-ledger"
    ):
        raise MigrationError("migration ledger fields are invalid")
    if type(ledger.get("schema_version")) is not int or (
        ledger["schema_version"] != 1
    ):
        raise MigrationError("migration ledger schema_version is invalid")
    approval = ledger.get("approval_sha256")
    if not isinstance(approval, str) or not re.fullmatch(
        r"[0-9a-f]{64}", approval
    ):
        raise MigrationError("migration ledger approval is invalid")
    raw_plan = ledger.get("plan")
    if not isinstance(raw_plan, dict):
        raise MigrationError("migration ledger approved plan is invalid")
    plan = validate_plan(raw_plan)
    if approval != plan["approval_sha256"]:
        raise MigrationError("migration ledger approval is not bound to its plan")
    if (
        not isinstance(ledger.get("sources"), list)
        or not ledger["sources"]
        or not isinstance(ledger.get("entries"), list)
    ):
        raise MigrationError("migration ledger collections are invalid")
    if ledger["sources"] != plan["sources"]:
        raise MigrationError("migration ledger sources do not match its plan")
    if len(ledger["entries"]) != len(plan["entries"]):
        raise MigrationError("migration ledger entries do not match its plan")

    source_ids: set[str] = set()
    for source in ledger["sources"]:
        if not isinstance(source, dict) or set(source) != {"id", "path"}:
            raise MigrationError("migration ledger source is invalid")
        source_id = source.get("id")
        source_path = source.get("path")
        if (
            not isinstance(source_id, str)
            or not source_id
            or source_id in source_ids
            or not isinstance(source_path, str)
            or not Path(source_path).is_absolute()
        ):
            raise MigrationError("migration ledger source is invalid")
        source_ids.add(source_id)

    entry_fields = {
        "entry_id",
        "source_id",
        "source_path",
        "source_bytes",
        "source_sha256",
        "destination",
        "destination_sha256",
        "status",
    }
    entry_ids: set[str] = set()
    destinations: set[str] = set()
    for entry, planned in zip(ledger["entries"], plan["entries"]):
        without_status = dict(entry) if isinstance(entry, dict) else {}
        without_status.pop("status", None)
        if (
            not isinstance(entry, dict)
            or set(entry) != entry_fields
            or entry.get("source_id") not in source_ids
            or entry.get("status") not in {"pending", "copied"}
            or not _valid_relative(entry.get("source_path"))
            or not _valid_destination(entry.get("destination"))
            or not re.fullmatch(r"[0-9a-f]{16}", str(entry.get("entry_id", "")))
            or entry["entry_id"] in entry_ids
            or entry["destination"] in destinations
            or type(entry.get("source_bytes")) is not int
            or not 0 <= entry["source_bytes"] < MAX_TEXT_BYTES
            or not re.fullmatch(
                r"[0-9a-f]{64}", str(entry.get("source_sha256", ""))
            )
            or not re.fullmatch(
                r"[0-9a-f]{64}", str(entry.get("destination_sha256", ""))
            )
            or without_status != planned
        ):
            raise MigrationError("migration ledger entry is invalid")
        entry_ids.add(entry["entry_id"])
        destinations.add(entry["destination"])

    copied = sum(entry["status"] == "copied" for entry in ledger["entries"])
    expected_summary = {
        "copied": copied,
        "pending": len(ledger["entries"]) - copied,
    }
    summary = ledger.get("summary")
    if (
        not isinstance(summary, dict)
        or set(summary) != {"copied", "pending"}
        or type(summary.get("copied")) is not int
        or type(summary.get("pending")) is not int
        or summary != expected_summary
    ):
        raise MigrationError("migration ledger summary is invalid")
    return ledger


def _source_roots(ledger: dict[str, Any], repo: Path) -> dict[str, Path]:
    roots: dict[str, Path] = {}
    resolved_roots: list[Path] = []
    for source in ledger["sources"]:
        canonical = canonical_source(source["path"], repo)
        if str(canonical) != source["path"]:
            raise MigrationError("migration ledger source root is not canonical")
        if any(paths_overlap(canonical, existing) for existing in resolved_roots):
            raise MigrationError("migration ledger source roots overlap")
        roots[source["id"]] = canonical
        resolved_roots.append(canonical)
    for entry in ledger["entries"]:
        if entry["entry_id"] != migration_entry_id(
            roots[entry["source_id"]], entry["source_path"]
        ):
            raise MigrationError("migration ledger source identity is invalid")
    return roots


def verify_migration(ledger_value: str) -> dict[str, Any]:
    """Verify copied source and destination checksums without changing state."""

    root = state_root()
    expected_root = root / "migrations"
    path = Path(ledger_value).expanduser()
    lexical = Path(os.path.abspath(str(path))) if path.is_absolute() else None
    if lexical is None or lexical != path or path.parent != expected_root:
        raise MigrationError("migration ledger path is unsafe")
    loaded = load_private_json_file(root, path)
    if loaded is None:
        raise MigrationError("migration ledger path is not readable")
    repo = resolve_repo()
    ledger = _validate_ledger(loaded[0])
    if path.name != f"{ledger['approval_sha256']}.json":
        raise MigrationError("migration ledger approval does not match its filename")
    source_paths = _source_roots(ledger, repo)

    findings: list[dict[str, Any]] = []
    checked = 0
    for entry in ledger["entries"]:
        if entry["status"] != "copied":
            findings.append(
                {
                    "code": "migration_entry_pending",
                    "key": f"migration_entry_pending:{entry['entry_id']}",
                    "severity": "error",
                    "locations": [
                        {"path": f"migration-entry:{entry['entry_id']}"}
                    ],
                }
            )
            continue
        checked += 1
        try:
            source_content = destination_source_bytes(
                source_paths[entry["source_id"]],
                entry["source_path"],
                entry["source_bytes"],
                entry["source_sha256"],
            )
            source_hash = sha256_bytes(source_content)
        except MigrationError:
            source_hash = None
        if source_hash != entry["source_sha256"]:
            findings.append(
                {
                    "code": "migration_source_checksum_mismatch",
                    "key": (
                        "migration_source_checksum_mismatch:"
                        f"{entry['entry_id']}"
                    ),
                    "severity": "error",
                    "locations": [
                        {
                            "path": (
                                f"{entry['source_id']}:"
                                f"{entry['source_path']}"
                            )
                        }
                    ],
                }
            )
        try:
            destination = migration_destination_path(
                repo, entry["destination"]
            )
        except MigrationError:
            destination = None
        try:
            destination_hash = (
                sha256_bytes(
                    regular_file_bytes(repo / "second-brain", destination)
                )
                if destination is not None
                else None
            )
        except PathError:
            destination_hash = None
        if destination_hash != entry["destination_sha256"]:
            findings.append(
                {
                    "code": "migration_destination_checksum_mismatch",
                    "key": (
                        "migration_destination_checksum_mismatch:"
                        f"{entry['entry_id']}"
                    ),
                    "severity": "error",
                    "locations": [
                        {"path": f"second-brain/{entry['destination']}"}
                    ],
                }
            )

    findings.sort(key=lambda finding: finding["key"])
    errors = len(findings)
    return {
        "schema_version": 1,
        "command": "migrate verify",
        "summary": {
            "status": "fail" if errors else "pass",
            "checked": checked,
            "errors": errors,
        },
        "findings": findings,
    }
