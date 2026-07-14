"""Approval-bound, append-only upgrades for protected vault files."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from .paths import (
    PathError,
    TargetExistsError,
    atomic_create,
    atomic_replace_if_unchanged,
    local_now,
    mutation_lock,
    regular_file_bytes,
    resolve_repo,
    safe_vault_path,
)


class UpgradeError(ValueError):
    """A protected upgrade cannot be planned or applied safely."""


@dataclass(frozen=True)
class UpgradeSpec:
    """One append-only vault upgrade with a stable marker and fallback file."""

    id: str
    path: str
    reason: str
    create_content: str
    append_block: str


# Future upgrades append immutable entries here. The initial vault already has
# the complete v1 structure, so there is no pending default mutation.
UPGRADE_SPECS: tuple[UpgradeSpec, ...] = ()


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _approval(preview: dict[str, Any]) -> str:
    unsigned = dict(preview)
    unsigned.pop("approval_sha256", None)
    return _sha256(_canonical_bytes(unsigned))


def _validate_specs(specs: Sequence[UpgradeSpec]) -> tuple[UpgradeSpec, ...]:
    validated = tuple(specs)
    ids: set[str] = set()
    paths: set[str] = set()
    for spec in validated:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", spec.id):
            raise UpgradeError("upgrade specification ID is invalid")
        if spec.id in ids or spec.path in paths:
            raise UpgradeError("upgrade specifications must have unique IDs and paths")
        if not spec.reason.strip() or not spec.create_content:
            raise UpgradeError("upgrade specification content is incomplete")
        marker = f"<!-- second-brain:upgrade:{spec.id} -->"
        if marker not in spec.append_block or marker not in spec.create_content:
            raise UpgradeError("upgrade specification is missing its stable marker")
        ids.add(spec.id)
        paths.add(spec.path)
    return tuple(sorted(validated, key=lambda item: (item.path, item.id)))


def _append_block(original: bytes, block: str) -> bytes:
    encoded = block.encode("utf-8")
    if not encoded.endswith(b"\n"):
        encoded += b"\n"
    if original.endswith(b"\n\n"):
        separator = b""
    elif original.endswith(b"\n"):
        separator = b"\n"
    else:
        separator = b"\n\n"
    return original + separator + encoded


def _backup_relative(date_value: str, target: str) -> str:
    return f"06 Archive/backups/{date_value}/{target}"


def build_upgrade_preview(
    specs: Sequence[UpgradeSpec] = UPGRADE_SPECS,
) -> dict[str, Any]:
    repo = resolve_repo()
    vault = repo / "second-brain"
    date_value = local_now().date().isoformat()
    operations: list[dict[str, Any]] = []
    for spec in _validate_specs(specs):
        target = safe_vault_path(repo, spec.path)
        marker = f"<!-- second-brain:upgrade:{spec.id} -->".encode("utf-8")
        if target.exists():
            try:
                before = regular_file_bytes(vault, target)
            except PathError as error:
                raise UpgradeError(
                    "protected upgrade target is not a regular file"
                ) from error
            if marker in before:
                continue
            after = _append_block(before, spec.append_block)
            operations.append(
                {
                    "id": spec.id,
                    "path": spec.path,
                    "action": "update",
                    "reason": spec.reason,
                    "protected": True,
                    "backup": _backup_relative(date_value, spec.path),
                    "before_sha256": _sha256(before),
                    "after_sha256": _sha256(after),
                }
            )
        else:
            after = spec.create_content.encode("utf-8")
            operations.append(
                {
                    "id": spec.id,
                    "path": spec.path,
                    "action": "create",
                    "reason": spec.reason,
                    "protected": False,
                    "backup": None,
                    "before_sha256": None,
                    "after_sha256": _sha256(after),
                }
            )
    preview: dict[str, Any] = {
        "schema_version": 1,
        "command": "upgrade",
        "mode": "dry-run",
        "date": date_value,
        "operations": operations,
        "summary": {
            "create": sum(item["action"] == "create" for item in operations),
            "update": sum(item["action"] == "update" for item in operations),
        },
    }
    preview["approval_sha256"] = _approval(preview)
    return preview


def _write_backup(repo: Path, relative: str, content: bytes) -> Path:
    vault = repo / "second-brain"
    initial = safe_vault_path(repo, relative)
    stem = initial.stem
    suffix = initial.suffix
    counter = 1
    while True:
        candidate = (
            initial
            if counter == 1
            else initial.with_name(f"{stem} {counter}{suffix}")
        )
        try:
            atomic_create(vault, candidate, content)
            return candidate
        except TargetExistsError:
            counter += 1
        except PathError as error:
            raise UpgradeError("protected upgrade backup path is unsafe") from error


def apply_upgrade(
    specs: Sequence[UpgradeSpec], approval_sha256: str
) -> dict[str, Any]:
    preview = build_upgrade_preview(specs)
    if approval_sha256 != preview["approval_sha256"]:
        raise UpgradeError("upgrade approval does not match the current preview")
    if not preview["operations"]:
        return {
            "schema_version": 1,
            "command": "upgrade",
            "result": "noop",
            "created": 0,
            "updated": 0,
            "backups": 0,
        }

    repo = resolve_repo()
    vault = repo / "second-brain"
    by_id = {spec.id: spec for spec in _validate_specs(specs)}
    created = 0
    updated = 0
    backups = 0
    with mutation_lock():
        locked_preview = build_upgrade_preview(specs)
        if approval_sha256 != locked_preview["approval_sha256"]:
            raise UpgradeError("upgrade approval is stale for the protected files")

        prepared: list[tuple[dict[str, Any], Path, bytes, Path | None, bytes | None]] = []
        for operation in locked_preview["operations"]:
            spec = by_id[operation["id"]]
            target = safe_vault_path(repo, spec.path)
            backup: Path | None = None
            before: bytes | None = None
            if operation["action"] == "update":
                try:
                    before = regular_file_bytes(vault, target)
                except PathError as error:
                    raise UpgradeError(
                        "protected upgrade target changed after preview"
                    ) from error
                if _sha256(before) != operation["before_sha256"]:
                    raise UpgradeError("upgrade approval is stale for the protected files")
                after = _append_block(before, spec.append_block)
                try:
                    backup = safe_vault_path(repo, operation["backup"])
                except PathError as error:
                    raise UpgradeError(
                        "protected upgrade backup path is unsafe"
                    ) from error
            else:
                if target.exists():
                    raise UpgradeError("protected upgrade target appeared after preview")
                after = spec.create_content.encode("utf-8")
            if _sha256(after) != operation["after_sha256"]:
                raise UpgradeError("protected upgrade content changed after preview")
            prepared.append((operation, target, after, backup, before))

        for operation, target, after, backup, before in prepared:
            if backup is not None and before is not None:
                _write_backup(
                    repo,
                    backup.relative_to(vault).as_posix(),
                    before,
                )
                backups += 1
            if operation["action"] == "create":
                try:
                    atomic_create(vault, target, after)
                except TargetExistsError as error:
                    raise UpgradeError(
                        "protected upgrade target appeared after preview"
                    ) from error
                except PathError as error:
                    raise UpgradeError(
                        "protected upgrade target path is unsafe"
                    ) from error
                created += 1
            else:
                try:
                    atomic_replace_if_unchanged(
                        vault,
                        target,
                        operation["before_sha256"],
                        after,
                    )
                except PathError as error:
                    raise UpgradeError(
                        "protected upgrade target changed after preview"
                    ) from error
                updated += 1
    return {
        "schema_version": 1,
        "command": "upgrade",
        "result": "updated",
        "created": created,
        "updated": updated,
        "backups": backups,
    }
