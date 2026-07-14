"""Versioned JSON payload validation with content-safe errors."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, TextIO


MAX_PAYLOAD_BYTES = 1_000_000
EVENT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SOURCE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
RESERVED_MARKER = "<!-- second-brain:"
MARKDOWN_BLOCK_RE = re.compile(r"^\s*(?:#{1,6}\s|---\s*$|```|~~~|<!--)")


class ValidationError(ValueError):
    """An actionable validation error that never embeds payload content."""


def load_payload(payload_path: str, stdin: TextIO | None = None) -> dict[str, Any]:
    if payload_path == "-":
        stream = stdin if stdin is not None else sys.stdin
        raw = stream.read(MAX_PAYLOAD_BYTES + 1)
        if len(raw.encode("utf-8")) >= MAX_PAYLOAD_BYTES:
            raise ValidationError("payload must be smaller than 1,000,000 bytes")
    else:
        path = Path(payload_path).expanduser()
        try:
            size = path.stat().st_size
        except OSError as error:
            raise ValidationError(
                "payload path must name a readable regular file"
            ) from error
        if not path.is_file():
            raise ValidationError("payload path must name a readable regular file")
        if size >= MAX_PAYLOAD_BYTES:
            raise ValidationError("payload must be smaller than 1,000,000 bytes")
        try:
            raw = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise ValidationError("payload must be readable UTF-8 JSON") from error

    try:
        value = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValidationError("payload must be valid JSON") from error
    if not isinstance(value, dict):
        raise ValidationError("payload root must be a JSON object")
    return value


def _require_exact_keys(
    payload: dict[str, Any],
    required: set[str],
    optional: set[str] | None = None,
) -> None:
    optional = optional or set()
    missing = sorted(required - payload.keys())
    unknown = sorted(payload.keys() - required - optional)
    if missing:
        raise ValidationError(
            "payload is missing required fields: " + ", ".join(missing)
        )
    if unknown:
        raise ValidationError("payload contains unsupported fields")


def _require_string(
    payload: dict[str, Any],
    field: str,
    *,
    allow_empty: bool = False,
    max_length: int = 20_000,
) -> str:
    value = payload.get(field)
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a string")
    if "\x00" in value:
        raise ValidationError(f"{field} must not contain NUL bytes")
    if not allow_empty and not value.strip():
        raise ValidationError(f"{field} must not be empty")
    if len(value) > max_length:
        raise ValidationError(f"{field} is too long")
    return value


def _validate_common(payload: dict[str, Any]) -> None:
    if (
        type(payload.get("schema_version")) is not int
        or payload["schema_version"] != 1
    ):
        raise ValidationError("schema_version must be 1")
    event_id = _require_string(payload, "event_id", max_length=128)
    if not EVENT_ID_RE.fullmatch(event_id):
        raise ValidationError("event_id has an invalid format")
    source = _require_string(payload, "source", max_length=64)
    if not SOURCE_RE.fullmatch(source):
        raise ValidationError("source has an invalid format")
    timestamp = _require_string(payload, "timestamp", max_length=64)
    try:
        parsed = datetime.fromisoformat(timestamp)
    except ValueError as error:
        raise ValidationError("timestamp must be ISO 8601") from error
    if parsed.tzinfo is None:
        raise ValidationError("timestamp must include a UTC offset")


def _require_tracked_string(
    payload: dict[str, Any],
    field: str,
    *,
    allow_empty: bool = False,
    max_length: int = 20_000,
) -> str:
    value = _require_string(
        payload,
        field,
        allow_empty=allow_empty,
        max_length=max_length,
    )
    if "\n" in value or "\r" in value:
        raise ValidationError(f"{field} must be single-line tracked text")
    if RESERVED_MARKER in value.lower():
        raise ValidationError(f"{field} contains reserved Second Brain syntax")
    if value and MARKDOWN_BLOCK_RE.match(value):
        raise ValidationError(f"{field} must not start a Markdown control block")
    return value


def _require_tracked_list(
    payload: dict[str, Any],
    field: str,
    *,
    max_items: int = 50,
    max_length: int = 2_000,
) -> list[str]:
    value = payload.get(field)
    if not isinstance(value, list) or len(value) > max_items:
        raise ValidationError(f"{field} must be an array of tracked strings")
    validated = []
    for item in value:
        temporary = {field: item}
        validated.append(
            _require_tracked_string(temporary, field, max_length=max_length)
        )
    return validated


def validate_raw_session(payload: dict[str, Any]) -> dict[str, Any]:
    required = {
        "schema_version",
        "event_id",
        "source",
        "timestamp",
        "session_id",
        "role",
        "text",
    }
    _validate_common(payload)
    _require_exact_keys(payload, required)
    session_id = _require_string(payload, "session_id", max_length=128)
    if not EVENT_ID_RE.fullmatch(session_id):
        raise ValidationError("session_id has an invalid format")
    role = _require_string(payload, "role", max_length=32)
    if role not in {"user", "assistant", "system", "tool"}:
        raise ValidationError("role must be user, assistant, system, or tool")
    _require_string(payload, "text", allow_empty=True, max_length=900_000)
    return payload


def validate_personal_decision(payload: dict[str, Any]) -> dict[str, Any]:
    required = {
        "schema_version",
        "event_id",
        "source",
        "timestamp",
        "title",
        "summary",
        "target",
        "links",
        "visibility",
        "confirmed",
    }
    _validate_common(payload)
    _require_exact_keys(payload, required)
    if payload.get("confirmed") is not True:
        raise ValidationError("tracked capture requires explicit confirmation")
    _require_tracked_string(payload, "title", max_length=200)
    _require_tracked_string(payload, "summary")
    _require_string(payload, "target", max_length=200)
    if payload.get("target") != "00 Context/Decisions.md":
        raise ValidationError("target is not authorized for personal-decision")
    if payload.get("visibility") != "public-sanitized":
        raise ValidationError("visibility must be public-sanitized")
    _require_tracked_list(payload, "links", max_items=20, max_length=2_000)
    return payload


def validate_focus(payload: dict[str, Any]) -> dict[str, Any]:
    required = {
        "schema_version",
        "event_id",
        "source",
        "timestamp",
        "date",
        "project",
        "outcome",
        "done_when",
        "evidence",
        "confirmed",
    }
    _validate_common(payload)
    _require_exact_keys(payload, required)
    date_value = _require_string(payload, "date", max_length=10)
    try:
        datetime.strptime(date_value, "%Y-%m-%d")
    except ValueError as error:
        raise ValidationError("date must use YYYY-MM-DD") from error
    project = _require_tracked_string(payload, "project", max_length=100)
    if project != "ExampleProject":
        raise ValidationError("daily focus project must be ExampleProject")
    for field in ("outcome", "done_when", "evidence"):
        _require_tracked_string(payload, field)
    if payload.get("confirmed") is not True:
        raise ValidationError("daily focus requires explicit confirmation")
    return payload


def validate_closeout(payload: dict[str, Any]) -> dict[str, Any]:
    required = {
        "schema_version",
        "event_id",
        "source",
        "timestamp",
        "date",
        "project",
        "planned",
        "completed",
        "evidence",
        "blocker",
        "decisions",
        "open",
        "next",
        "confirmed",
    }
    _validate_common(payload)
    _require_exact_keys(payload, required)
    date_value = _require_string(payload, "date", max_length=10)
    try:
        datetime.strptime(date_value, "%Y-%m-%d")
    except ValueError as error:
        raise ValidationError("date must use YYYY-MM-DD") from error
    for field in ("project", "planned", "completed", "evidence", "next"):
        _require_tracked_string(payload, field)
    _require_tracked_string(payload, "blocker", allow_empty=True)
    for field in ("decisions", "open"):
        _require_tracked_list(payload, field)
    if payload.get("confirmed") is not True:
        raise ValidationError("closeout requires explicit confirmation")
    return payload
