"""Status, capture, and closeout operations for the tracked vault."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from .content_security import redact
from .paths import (
    PathError,
    atomic_replace_if_unchanged,
    atomic_write,
    ensure_private_directory,
    local_now,
    mutation_lock,
    regular_file_bytes,
    resolve_repo,
    safe_vault_path,
    state_root,
)
from .schema import (
    ValidationError,
    validate_closeout,
    validate_focus,
    validate_personal_decision,
    validate_raw_session,
)


EVENT_MARKER = "<!-- second-brain:event:{event_id} -->"
FOCUS_MARKER = "<!-- second-brain:focus:{event_id} -->"
FOCUS_MARKER_PREFIX = "<!-- second-brain:focus:"
DIGEST_MARKER = "<!-- second-brain:digest:{digest} -->"


def _reject_tracked_secrets(payload: dict[str, Any], fields: tuple[str, ...]) -> None:
    for field in fields:
        value = payload[field]
        values = value if isinstance(value, list) else [value]
        if any(redact(item) != item for item in values):
            raise ValidationError("tracked content contains a likely secret")


def status_report() -> dict[str, Any]:
    repo = resolve_repo()
    projects_dir = safe_vault_path(repo, "02 Projects")
    daily_dir = safe_vault_path(repo, "05 Daily Notes")
    inbox_path = safe_vault_path(repo, "01 Inbox/Brain Dump.md")
    if not projects_dir.is_dir() or not daily_dir.is_dir():
        raise PathError("Second Brain status directories are missing or invalid")
    if not inbox_path.is_file():
        raise PathError("Second Brain Inbox note is missing or invalid")
    projects = []
    for path in sorted(projects_dir.glob("*.md")):
        if path.is_symlink() or not path.is_file():
            raise PathError("Second Brain project note is missing or invalid")
        content = path.read_text(encoding="utf-8")
        if re.search(r"(?m)^status: active$", content):
            projects.append(path.stem)
    daily_notes = []
    for path in daily_dir.glob("????-??-??.md"):
        if path.is_symlink() or not path.is_file():
            raise PathError("Second Brain Daily Note is missing or invalid")
        daily_notes.append(path.stem)
    daily_notes = sorted(daily_notes, reverse=True)[:3]
    inbox = inbox_path.read_text(encoding="utf-8")
    inbox_items = sum(
        1
        for line in inbox.splitlines()
        if line.startswith("- ") and "No reviewed inbox items" not in line
    )
    return {
        "schema_version": 1,
        "date": local_now().date().isoformat(),
        "active_projects": projects,
        "latest_daily_notes": daily_notes,
        "inbox": {"count": inbox_items, "path": "01 Inbox/Brain Dump.md"},
    }


def capture(kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    if kind == "raw-session":
        return _capture_raw(validate_raw_session(payload))
    if kind == "personal-decision":
        return _capture_personal_decision(validate_personal_decision(payload))
    raise ValueError("capture kind is not supported")


def _capture_raw(payload: dict[str, Any]) -> dict[str, Any]:
    raw_dir = state_root() / "raw"
    event_id = payload["event_id"]
    date_value = (
        datetime.fromisoformat(payload["timestamp"])
        .astimezone(ZoneInfo("America/Toronto"))
        .date()
        .isoformat()
    )
    raw_path = raw_dir / f"{date_value}.jsonl"
    with mutation_lock():
        ensure_private_directory(raw_dir)
        if raw_path.is_symlink():
            raise PathError("raw event file must not be a symlink")
        safe_payload = dict(payload)
        safe_payload["text"] = redact(payload["text"])
        existing = raw_path.read_text(encoding="utf-8") if raw_path.exists() else ""
        for line in existing.splitlines():
            try:
                recorded = json.loads(line)
            except json.JSONDecodeError as error:
                raise PathError("private raw session state is malformed") from error
            if not isinstance(recorded, dict):
                raise PathError("private raw session state is malformed")
            if recorded.get("event_id") != event_id:
                continue
            if recorded == safe_payload:
                return {
                    "schema_version": 1,
                    "command": "capture",
                    "result": "noop",
                }
            raise ValidationError("event ID conflicts with an existing raw capture")
        line = json.dumps(safe_payload, ensure_ascii=False, sort_keys=True) + "\n"
        atomic_write(raw_path, existing + line, mode=0o600)
    return {"schema_version": 1, "command": "capture", "result": "created"}


def _capture_personal_decision(payload: dict[str, Any]) -> dict[str, Any]:
    _reject_tracked_secrets(payload, ("title", "summary", "links"))
    repo = resolve_repo()
    marker = EVENT_MARKER.format(event_id=payload["event_id"])
    digest_marker = _digest_marker(payload)
    links = " ".join(payload["links"])
    block = (
        f"{marker}\n{digest_marker}\n\n"
        f"### {payload['timestamp'][:10]} - {payload['title']}\n\n"
        f"{payload['summary']}\n"
    )
    if links:
        block += f"\nLinks: {links}\n"
    with mutation_lock():
        vault = repo / "second-brain"
        target = safe_vault_path(repo, payload["target"])
        if not target.is_file():
            raise PathError(
                "authorized capture target is missing or not a regular file"
            )
        original, content = _read_tracked_note(vault, target)
        _require_note_structure(content, ("## Entries",))
        if marker in content:
            if _marker_has_digest(content, marker, digest_marker):
                return {
                    "schema_version": 1,
                    "command": "capture",
                    "result": "noop",
                }
            raise ValidationError("event ID conflicts with an existing capture")
        updated = _append_to_section(content, "## Entries", block)
        atomic_replace_if_unchanged(
            vault,
            target,
            hashlib.sha256(original).hexdigest(),
            updated.encode("utf-8"),
        )
    return {"schema_version": 1, "command": "capture", "result": "updated"}


def focus(payload: dict[str, Any]) -> dict[str, Any]:
    payload = validate_focus(payload)
    _reject_tracked_secrets(payload, ("project", "outcome", "done_when", "evidence"))
    repo = resolve_repo()
    marker = FOCUS_MARKER.format(event_id=payload["event_id"])
    digest_marker = _digest_marker(payload)
    block = (
        f"{marker}\n{digest_marker}\n\n"
        f"- **Outcome:** {payload['outcome']}\n"
        f"- **Done when:** {payload['done_when']}\n"
        f"- **Evidence:** {payload['evidence']}\n"
    )
    with mutation_lock():
        vault = repo / "second-brain"
        daily_path = safe_vault_path(
            repo, f"05 Daily Notes/{payload['date']}.md"
        )
        if not daily_path.is_file():
            raise PathError("daily focus date does not have a Daily Note")
        original, daily = _read_tracked_note(vault, daily_path)
        _require_note_structure(
            daily,
            ("## Focus", "## Done", "## Decisions", "## Open", "## Next"),
        )
        focus_body = _section_body(daily, "## Focus")
        if marker in focus_body:
            if digest_marker in focus_body:
                return {
                    "schema_version": 1,
                    "command": "focus",
                    "result": "noop",
                }
            raise ValidationError("event ID conflicts with an existing focus")
        if FOCUS_MARKER_PREFIX in focus_body:
            raise ValueError("a ExampleProject focus is already confirmed for this date")
        daily = _replace_section(daily, "## Focus", block)
        atomic_replace_if_unchanged(
            vault,
            daily_path,
            hashlib.sha256(original).hexdigest(),
            daily.encode("utf-8"),
        )
    return {"schema_version": 1, "command": "focus", "result": "updated"}


def closeout(payload: dict[str, Any]) -> dict[str, Any]:
    payload = validate_closeout(payload)
    _reject_tracked_secrets(
        payload,
        (
            "project",
            "planned",
            "completed",
            "evidence",
            "blocker",
            "decisions",
            "open",
            "next",
        ),
    )
    if payload["project"] != "ExampleProject":
        raise ValidationError("closeout project must be ExampleProject")
    repo = resolve_repo()
    project_name = payload["project"]
    marker = EVENT_MARKER.format(event_id=payload["event_id"])
    digest_marker = _digest_marker(payload)
    done_block = (
        f"{marker}\n{digest_marker}\n\n"
        f"### {project_name} closeout\n\n"
        f"- **Planned:** {payload['planned']}\n"
        f"- **Completed:** {payload['completed']}\n"
        f"- **Evidence:** {payload['evidence']}\n"
        f"- **Blocker:** {payload['blocker'] or 'None reported.'}\n"
    )
    progress_block = (
        f"{marker}\n{digest_marker}\n\n"
        f"### {payload['date']}\n\n"
        f"- Completed: {payload['completed']}\n"
        f"- Evidence: {payload['evidence']}\n"
        f"- Blocker: {payload['blocker'] or 'None reported.'}\n"
    )
    with mutation_lock():
        vault = repo / "second-brain"
        daily_path = safe_vault_path(
            repo, f"05 Daily Notes/{payload['date']}.md"
        )
        project_path = safe_vault_path(repo, "02 Projects/ExampleProject.md")
        if not daily_path.is_file():
            raise PathError("closeout date does not have a Daily Note")
        if not project_path.is_file():
            raise PathError("ExampleProject project note is missing or invalid")
        original_daily_bytes, daily = _read_tracked_note(vault, daily_path)
        original_project_bytes, project = _read_tracked_note(vault, project_path)
        _require_note_structure(
            daily,
            ("## Focus", "## Done", "## Decisions", "## Open", "## Next"),
        )
        _require_note_structure(project, ("## Progress",))
        focus_body = _section_body(daily, "## Focus")
        outcome_match = re.search(
            r"(?m)^- \*\*Outcome:\*\* (.+)$",
            focus_body,
        )
        if FOCUS_MARKER_PREFIX not in focus_body or not outcome_match:
            raise ValidationError("closeout requires a confirmed daily ExampleProject focus")
        if outcome_match.group(1) != payload["planned"]:
            raise ValidationError("closeout planned result must match the daily focus")
        if marker in daily and not _marker_has_digest(daily, marker, digest_marker):
            raise ValidationError("event ID conflicts with an existing closeout")
        if marker in project and not _marker_has_digest(
            project, marker, digest_marker
        ):
            raise ValidationError("event ID conflicts with an existing closeout")
        if marker in daily and marker in project:
            return {"schema_version": 1, "command": "closeout", "result": "noop"}
        original_daily = daily
        original_project = project
        if marker not in daily:
            daily = _append_to_section(daily, "## Done", done_block)
            if payload["decisions"]:
                daily = _append_to_section(
                    daily,
                    "## Decisions",
                    "\n".join(f"- {item}" for item in payload["decisions"]) + "\n",
                )
            open_items = []
            if payload["blocker"]:
                open_items.append(payload["blocker"])
            for item in payload["open"]:
                if item not in open_items:
                    open_items.append(item)
            if open_items:
                daily = _append_to_section(
                    daily,
                    "## Open",
                    "\n".join(f"- {item}" for item in open_items) + "\n",
                )
            daily = _append_to_section(
                daily, "## Next", f"- {payload['next']}\n"
            )
        if marker not in project:
            project = _append_to_section(project, "## Progress", progress_block)
        updates = []
        if daily != original_daily:
            updates.append(
                (daily_path, daily.encode("utf-8"), original_daily_bytes)
            )
        if project != original_project:
            updates.append(
                (project_path, project.encode("utf-8"), original_project_bytes)
            )
        written = []
        try:
            for path, updated, original in updates:
                atomic_replace_if_unchanged(
                    vault,
                    path,
                    hashlib.sha256(original).hexdigest(),
                    updated,
                )
                written.append((path, original, hashlib.sha256(updated).hexdigest()))
        except Exception:
            rollback_error = None
            for path, original, written_sha256 in reversed(written):
                try:
                    atomic_replace_if_unchanged(
                        vault,
                        path,
                        written_sha256,
                        original,
                    )
                except Exception as error:
                    rollback_error = error
            if rollback_error is not None:
                raise PathError(
                    "closeout rollback could not preserve every note"
                ) from rollback_error
            raise
    return {"schema_version": 1, "command": "closeout", "result": "updated"}


def _payload_digest(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _digest_marker(payload: dict[str, Any]) -> str:
    return DIGEST_MARKER.format(digest=_payload_digest(payload))


def _marker_has_digest(content: str, marker: str, digest_marker: str) -> bool:
    marker_index = content.find(marker)
    if marker_index < 0:
        return False
    next_heading = content.find("\n### ", marker_index + len(marker))
    block_end = len(content) if next_heading < 0 else next_heading
    return digest_marker in content[marker_index:block_end]


def _require_note_structure(content: str, headings: tuple[str, ...]) -> None:
    if not content.startswith("---\n"):
        raise PathError("protected note has invalid frontmatter structure")
    frontmatter_end = content.find("\n---\n", 4)
    if frontmatter_end < 0:
        raise PathError("protected note has invalid frontmatter structure")
    body_start = frontmatter_end + len("\n---\n")
    positions = []
    for heading in headings:
        matches = list(re.finditer(rf"(?m)^{re.escape(heading)}\s*$", content))
        if len(matches) != 1:
            raise PathError("protected note has invalid stable section structure")
        if matches[0].start() < body_start:
            raise PathError("protected note has invalid stable section structure")
        positions.append(matches[0].start())
    if positions != sorted(positions):
        raise PathError("protected note has invalid stable section structure")


def _read_tracked_note(vault: Path, target: Path) -> tuple[bytes, str]:
    content = regular_file_bytes(vault, target)
    try:
        return content, content.decode("utf-8")
    except UnicodeError as error:
        raise PathError("protected note must be valid UTF-8") from error


def _section_body(content: str, heading: str) -> str:
    heading_match = re.search(rf"(?m)^{re.escape(heading)}\s*$", content)
    if not heading_match:
        return ""
    section_start = heading_match.end()
    next_heading = re.search(r"(?m)^## ", content[section_start:])
    section_end = (
        section_start + next_heading.start()
        if next_heading
        else len(content)
    )
    return content[section_start:section_end]


def _replace_section(content: str, heading: str, block: str) -> str:
    heading_match = re.search(rf"(?m)^{re.escape(heading)}\s*$", content)
    if not heading_match:
        done_match = re.search(r"(?m)^## Done\s*$", content)
        if not done_match:
            raise PathError("Daily Note is missing its stable section structure")
        return (
            f"{content[:done_match.start()].rstrip()}\n\n"
            f"{heading}\n\n{block.rstrip()}\n\n"
            f"{content[done_match.start():].lstrip()}"
        )
    section_start = heading_match.end()
    next_heading = re.search(r"(?m)^## ", content[section_start:])
    section_end = (
        section_start + next_heading.start()
        if next_heading
        else len(content)
    )
    after = content[section_end:].lstrip("\n")
    result = f"{content[:section_start].rstrip()}\n\n{block.rstrip()}\n"
    if after:
        result += f"\n{after}"
    return result


def _append_to_section(content: str, heading: str, block: str) -> str:
    heading_match = re.search(
        rf"(?m)^{re.escape(heading)}\s*$",
        content,
    )
    if not heading_match:
        separator = "" if content.endswith("\n\n") else "\n"
        return f"{content}{separator}\n{heading}\n\n{block.rstrip()}\n"
    section_start = heading_match.end()
    next_heading = re.search(r"(?m)^## ", content[section_start:])
    insertion = (
        section_start + next_heading.start()
        if next_heading
        else len(content)
    )
    before = content[:insertion].rstrip()
    after = content[insertion:].lstrip("\n")
    result = f"{before}\n\n{block.rstrip()}\n"
    if after:
        result += f"\n{after}"
    return result
