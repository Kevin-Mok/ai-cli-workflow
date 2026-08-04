"""Private, redacted deferred-reminder storage and lifecycle operations."""

from __future__ import annotations

import json
from datetime import date
from typing import Any

from .content_security import redact
from .paths import PathError, atomic_write, ensure_private_directory, local_now, mutation_lock, state_root
from .schema import (
    ValidationError,
    validate_deferred,
    validate_deferred_resolution,
    validate_deferred_schedule,
)
from .state_private import private_file_bytes


STORE_VERSION = 1
STORE_MAX_BYTES = 1_000_000
STORE_DIRECTORY = "deferred"
STORE_FILENAME = "reminders.json"
ACTIVE_STATES = {"someday", "deferred", "inbox"}
LISTABLE_STATES = {"someday", "inbox"}
RESOLVED_STATE = "resolved"


def _store_path() -> tuple[Any, Any]:
    root = state_root()
    return root, root / STORE_DIRECTORY / STORE_FILENAME


def _canonical_store(reminders: list[dict[str, Any]]) -> str:
    value = {
        "schema_version": STORE_VERSION,
        "reminders": sorted(reminders, key=lambda item: item["event_id"]),
    }
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ) + "\n"


def _read_store() -> tuple[Any, list[dict[str, Any]]]:
    root, path = _store_path()
    raw = private_file_bytes(root, path, max_bytes=STORE_MAX_BYTES)
    if raw is None:
        return path, []
    try:
        value = json.loads(raw)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise PathError("private deferred reminder state is malformed") from error
    if (
        not isinstance(value, dict)
        or set(value) != {"schema_version", "reminders"}
        or value.get("schema_version") != STORE_VERSION
        or not isinstance(value["reminders"], list)
    ):
        raise PathError("private deferred reminder state is malformed")
    reminders: list[dict[str, Any]] = []
    for record in value["reminders"]:
        reminders.append(_validated_record(record))
    if len({record["event_id"] for record in reminders}) != len(reminders):
        raise PathError("private deferred reminder state is malformed")
    return path, reminders


def _validated_record(record: object) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise PathError("private deferred reminder state is malformed")
    state = record.get("state")
    if state in ACTIVE_STATES:
        try:
            payload = validate_deferred({key: value for key, value in record.items() if key != "state"})
        except ValidationError as error:
            raise PathError("private deferred reminder state is malformed") from error
        if set(record) != set(payload) | {"state"}:
            raise PathError("private deferred reminder state is malformed")
        return dict(record)
    if state == RESOLVED_STATE:
        if (
            set(record) != {"schema_version", "event_id", "state", "resolution"}
            or type(record.get("schema_version")) is not int
            or record["schema_version"] != STORE_VERSION
            or not isinstance(record.get("event_id"), str)
            or record.get("resolution") not in {"focused", "dismissed"}
        ):
            raise PathError("private deferred reminder state is malformed")
        return dict(record)
    raise PathError("private deferred reminder state is malformed")


def _result(command: str, result: str, **metadata: int) -> dict[str, Any]:
    return {"schema_version": STORE_VERSION, "command": command, "result": result, **metadata}


def defer(payload: dict[str, Any]) -> dict[str, Any]:
    validated = validate_deferred(payload)
    state = "someday" if validated["target_date"] is None else "deferred"
    record = {**validated, "text": redact(validated["text"]), "state": state}
    with mutation_lock():
        path, reminders = _read_store()
        for existing in reminders:
            if existing["event_id"] != record["event_id"]:
                continue
            if existing == record:
                return _result("defer", "noop")
            raise ValidationError("event ID conflicts with an existing deferred reminder")
        ensure_private_directory(path.parent)
        atomic_write(path, _canonical_store([*reminders, record]), mode=0o600)
    return _result("defer", "created")


def schedule(payload: dict[str, Any]) -> dict[str, Any]:
    validated = validate_deferred_schedule(payload)
    target_date = validated["target_date"]
    if date.fromisoformat(target_date) <= local_now().date():
        raise ValidationError("target_date must be a future local date")
    event_id = validated["event_id"]
    with mutation_lock():
        path, reminders = _read_store()
        for index, existing in enumerate(reminders):
            if existing["event_id"] != event_id:
                continue
            if existing["state"] == "deferred" and existing["target_date"] == target_date:
                return _result("schedule-deferred", "noop")
            if existing["state"] != "someday":
                raise ValidationError("deferred reminder must be unscheduled")
            reminders[index] = {
                **existing,
                "target_date": target_date,
                "state": "deferred",
            }
            ensure_private_directory(path.parent)
            atomic_write(path, _canonical_store(reminders), mode=0o600)
            return _result("schedule-deferred", "updated")
    raise ValidationError("deferred reminder was not found")


def process_due() -> dict[str, Any]:
    today = local_now().date()
    with mutation_lock():
        path, reminders = _read_store()
        promoted = 0
        updated: list[dict[str, Any]] = []
        for record in reminders:
            if record["state"] == "deferred" and date.fromisoformat(record["target_date"]) <= today:
                updated.append({**record, "state": "inbox"})
                promoted += 1
            else:
                updated.append(record)
        if not promoted:
            return _result("process-deferred", "noop", promoted=0)
        ensure_private_directory(path.parent)
        atomic_write(path, _canonical_store(updated), mode=0o600)
    return _result("process-deferred", "updated", promoted=promoted)


def list_inbox() -> list[dict[str, Any]]:
    return list_reminders("inbox")


def list_reminders(state: str) -> list[dict[str, Any]]:
    if state not in LISTABLE_STATES:
        raise ValidationError("private reminder state is not listable")
    _, reminders = _read_store()
    return [dict(record) for record in reminders if record["state"] == state]


def resolve(payload: dict[str, Any]) -> dict[str, Any]:
    validated = validate_deferred_resolution(payload)
    event_id = validated["event_id"]
    resolution = validated["resolution"]
    with mutation_lock():
        path, reminders = _read_store()
        for index, existing in enumerate(reminders):
            if existing["event_id"] != event_id:
                continue
            if existing["state"] == RESOLVED_STATE:
                if existing["resolution"] == resolution:
                    return _result("resolve-deferred", "noop")
                raise ValidationError("deferred reminder resolution conflicts")
            if existing["state"] != "inbox":
                raise ValidationError("deferred reminder must be in the private inbox")
            reminders[index] = {
                "schema_version": STORE_VERSION,
                "event_id": event_id,
                "state": RESOLVED_STATE,
                "resolution": resolution,
            }
            ensure_private_directory(path.parent)
            atomic_write(path, _canonical_store(reminders), mode=0o600)
            return _result("resolve-deferred", "updated")
    raise ValidationError("deferred reminder was not found")


def counts() -> dict[str, int]:
    _, reminders = _read_store()
    return {
        "someday": sum(record["state"] == "someday" for record in reminders),
        "deferred": sum(record["state"] == "deferred" for record in reminders),
        "inbox": sum(record["state"] == "inbox" for record in reminders),
    }
