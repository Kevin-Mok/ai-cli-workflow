"""Approval-bound migration copies backed by private resume ledgers."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .migration import validate_plan
from .migration_common import (
    MigrationError,
    canonical_source,
    destination_source_bytes,
    load_json_file,
    load_private_json_file,
    migration_destination_path,
    migration_entry_id,
    paths_overlap,
    sha256_bytes,
    wrapped_import,
)
from .paths import (
    PathError,
    TargetExistsError,
    atomic_create,
    atomic_replace_if_unchanged,
    ensure_private_directory,
    mutation_lock,
    regular_file_bytes,
    resolve_repo,
    state_root,
)


def _ledger_path(approval: str) -> Path:
    return state_root() / "migrations" / f"{approval}.json"


def _ledger_text(ledger: dict[str, Any]) -> str:
    return json.dumps(
        ledger,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def _new_ledger(plan: dict[str, Any]) -> dict[str, Any]:
    entries = [{**entry, "status": "pending"} for entry in plan["entries"]]
    return {
        "schema_version": 1,
        "kind": "second-brain-migration-ledger",
        "approval_sha256": plan["approval_sha256"],
        "plan": json.loads(json.dumps(plan)),
        "sources": plan["sources"],
        "entries": entries,
        "summary": {"copied": 0, "pending": len(entries)},
    }


def _validate_ledger(
    ledger: dict[str, Any], plan: dict[str, Any]
) -> dict[str, Any]:
    if set(ledger) != {
        "schema_version",
        "kind",
        "approval_sha256",
        "plan",
        "sources",
        "entries",
        "summary",
    }:
        raise MigrationError("migration ledger fields are invalid")
    if (
        type(ledger.get("schema_version")) is not int
        or ledger["schema_version"] != 1
        or ledger.get("kind") != "second-brain-migration-ledger"
        or ledger.get("approval_sha256") != plan["approval_sha256"]
        or ledger.get("plan") != plan
        or ledger.get("sources") != plan["sources"]
        or not isinstance(ledger.get("entries"), list)
        or len(ledger["entries"]) != len(plan["entries"])
    ):
        raise MigrationError("migration ledger does not match the approved plan")
    for recorded, planned in zip(ledger["entries"], plan["entries"]):
        if not isinstance(recorded, dict):
            raise MigrationError("migration ledger entry is invalid")
        status_value = recorded.get("status")
        without_status = dict(recorded)
        without_status.pop("status", None)
        if status_value not in {"pending", "copied"} or without_status != planned:
            raise MigrationError("migration ledger entry does not match the plan")
    copied = sum(entry["status"] == "copied" for entry in ledger["entries"])
    if ledger.get("summary") != {
        "copied": copied,
        "pending": len(ledger["entries"]) - copied,
    }:
        raise MigrationError("migration ledger summary is invalid")
    return ledger


def _read_ledger(
    path: Path,
    plan: dict[str, Any],
) -> tuple[dict[str, Any], bytes] | None:
    loaded = load_private_json_file(state_root(), path)
    if loaded is None:
        return None
    ledger, content = loaded
    return _validate_ledger(ledger, plan), content


def _source_roots(plan: dict[str, Any], repo: Path) -> dict[str, Path]:
    roots: dict[str, Path] = {}
    resolved_roots: list[Path] = []
    for source in plan["sources"]:
        canonical = canonical_source(source["path"], repo)
        if str(canonical) != source["path"]:
            raise MigrationError("migration source changed after approval")
        if any(paths_overlap(canonical, existing) for existing in resolved_roots):
            raise MigrationError("migration source roots overlap after approval")
        roots[source["id"]] = canonical
        resolved_roots.append(canonical)
    return roots


def _create_ledger(path: Path, ledger: dict[str, Any]) -> None:
    root = state_root()
    ensure_private_directory(path.parent)
    try:
        atomic_create(root, path, _ledger_text(ledger).encode("utf-8"), mode=0o600)
    except TargetExistsError as error:
        raise MigrationError("migration ledger appeared during apply") from error
    except PathError as error:
        raise MigrationError("migration ledger path is unsafe") from error


def _replace_ledger(
    path: Path,
    previous: dict[str, Any],
    updated: dict[str, Any],
) -> None:
    root = state_root()
    try:
        loaded = load_private_json_file(root, path)
        if loaded is None:
            raise MigrationError("migration ledger changed during apply")
        current_value, current = loaded
        if current_value != previous:
            raise MigrationError("migration ledger changed during apply")
        atomic_replace_if_unchanged(
            root,
            path,
            sha256_bytes(current),
            _ledger_text(updated).encode("utf-8"),
            mode=0o600,
        )
    except PathError as error:
        raise MigrationError("migration ledger path is unsafe") from error


def _preflight(
    plan: dict[str, Any],
    ledger: dict[str, Any] | None,
    repo: Path,
) -> list[tuple[dict[str, Any], bytes, Path, str]]:
    roots = _source_roots(plan, repo)
    prepared: list[tuple[dict[str, Any], bytes, Path, str]] = []
    ledger_status = {
        entry["entry_id"]: entry["status"] for entry in ledger["entries"]
    } if ledger else {}
    for entry in plan["entries"]:
        source_root = roots[entry["source_id"]]
        if entry["entry_id"] != migration_entry_id(
            source_root, entry["source_path"]
        ):
            raise MigrationError("migration plan source identity is invalid")
        content = destination_source_bytes(
            source_root,
            entry["source_path"],
            entry["source_bytes"],
            entry["source_sha256"],
        )
        wrapped = wrapped_import(content, entry["source_sha256"], plan["date"])
        if sha256_bytes(wrapped) != entry["destination_sha256"]:
            raise MigrationError("migration destination checksum is invalid")
        destination = migration_destination_path(repo, entry["destination"])
        vault = repo / "second-brain"
        status_value = ledger_status.get(entry["entry_id"], "pending")
        if destination.exists():
            try:
                existing_hash = sha256_bytes(regular_file_bytes(vault, destination))
            except PathError:
                existing_hash = None
            if (
                status_value == "copied"
                and existing_hash == entry["destination_sha256"]
            ):
                disposition = "skip"
            elif ledger is not None and existing_hash == entry["destination_sha256"]:
                disposition = "adopt"
            else:
                raise MigrationError("migration destination appeared or changed")
        elif status_value == "copied":
            raise MigrationError("migration destination is missing for a copied entry")
        else:
            disposition = "copy"
        prepared.append((entry, wrapped, destination, disposition))
    return prepared


def apply_migration(
    plan_path: str, approval: str
) -> dict[str, Any]:
    plan = validate_plan(load_json_file(plan_path))
    if not re.fullmatch(r"[0-9a-f]{64}", approval) or approval != plan[
        "approval_sha256"
    ]:
        raise MigrationError("migration approval does not match the plan")
    repo = resolve_repo()
    ledger_path = _ledger_path(approval)
    loaded_ledger = _read_ledger(ledger_path, plan)
    ledger_exists = loaded_ledger is not None
    ledger = loaded_ledger[0] if loaded_ledger is not None else None
    _preflight(plan, ledger, repo)

    copied = 0
    skipped = 0
    with mutation_lock():
        locked_plan = validate_plan(load_json_file(plan_path))
        if locked_plan["approval_sha256"] != approval:
            raise MigrationError("migration approval is stale")
        loaded_ledger = _read_ledger(ledger_path, locked_plan)
        ledger_exists = loaded_ledger is not None
        ledger = (
            loaded_ledger[0]
            if loaded_ledger is not None
            else _new_ledger(locked_plan)
        )
        prepared = _preflight(locked_plan, ledger if ledger_exists else None, repo)
        by_id = {entry["entry_id"]: entry for entry in ledger["entries"]}
        if not ledger_exists:
            _create_ledger(ledger_path, ledger)

        for entry, wrapped, destination, disposition in prepared:
            recorded = by_id[entry["entry_id"]]
            if disposition == "skip":
                skipped += 1
                continue
            if disposition == "copy":
                try:
                    atomic_create(
                        repo / "second-brain",
                        destination,
                        wrapped,
                        portable_unique=True,
                    )
                except TargetExistsError as error:
                    raise MigrationError(
                        "migration destination appeared during apply"
                    ) from error
                except PathError as error:
                    raise MigrationError(
                        "migration destination path is unsafe"
                    ) from error
                copied += 1
            else:
                skipped += 1
            previous_ledger = json.loads(json.dumps(ledger))
            recorded["status"] = "copied"
            complete = sum(item["status"] == "copied" for item in ledger["entries"])
            ledger["summary"] = {
                "copied": complete,
                "pending": len(ledger["entries"]) - complete,
            }
            _replace_ledger(ledger_path, previous_ledger, ledger)

    if copied == 0 and all(
        entry["status"] == "copied" for entry in ledger["entries"]
    ):
        result = "noop" if ledger_exists else "created"
    else:
        result = "updated" if ledger_exists else "created"
    return {
        "schema_version": 1,
        "command": "migrate apply",
        "result": result,
        "copied": copied,
        "skipped": skipped,
        "ledger": str(ledger_path),
    }
