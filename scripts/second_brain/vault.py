"""Status, capture, and closeout operations for the tracked vault."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .paths import (
    PathError,
    atomic_write,
    ensure_private_directory,
    local_now,
    mutation_lock,
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


SECRET_PATTERNS = (
    re.compile(
        r"-----BEGIN [^-\r\n]*PRIVATE KEY-----.*?"
        r"-----END [^-\r\n]*PRIVATE KEY-----",
        re.DOTALL,
    ),
    re.compile(r"(?i)\bauthorization\s*:\s*bearer\s+[^\s,;]+"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(
        r"(?i)\b[A-Za-z0-9_.-]*(?:api[_ -]?key|password|token|secret)"
        r"\s*[:=]\s*[^\s,;]+"
    ),
)
EVENT_MARKER = "<!-- second-brain:event:{event_id} -->"
FOCUS_MARKER = "<!-- second-brain:focus:{event_id} -->"
FOCUS_MARKER_PREFIX = "<!-- second-brain:focus:"


def redact(text: str) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def _reject_tracked_secrets(payload: dict[str, Any], fields: tuple[str, ...]) -> None:
    for field in fields:
        value = payload[field]
        values = value if isinstance(value, list) else [value]
        if any(redact(item) != item for item in values):
            raise ValidationError("tracked content contains a likely secret")


def status_report() -> dict[str, Any]:
    repo = resolve_repo()
    vault = repo / "second-brain"
    projects = []
    for path in sorted((vault / "02 Projects").glob("*.md")):
        content = path.read_text(encoding="utf-8")
        if re.search(r"(?m)^status: active$", content):
            projects.append(path.stem)
    daily_notes = sorted(
        (path.stem for path in (vault / "05 Daily Notes").glob("????-??-??.md")),
        reverse=True,
    )[:3]
    inbox_path = vault / "01 Inbox" / "Brain Dump.md"
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
    date_value = payload["timestamp"][:10]
    raw_path = raw_dir / f"{date_value}.jsonl"
    with mutation_lock():
        ensure_private_directory(raw_dir)
        if raw_path.is_symlink():
            raise PathError("raw event file must not be a symlink")
        existing = raw_path.read_text(encoding="utf-8") if raw_path.exists() else ""
        if f'"event_id": "{event_id}"' in existing:
            return {"schema_version": 1, "command": "capture", "result": "noop"}
        safe_payload = dict(payload)
        safe_payload["text"] = redact(payload["text"])
        line = json.dumps(safe_payload, ensure_ascii=False, sort_keys=True) + "\n"
        atomic_write(raw_path, existing + line, mode=0o600)
    return {"schema_version": 1, "command": "capture", "result": "created"}


def _capture_personal_decision(payload: dict[str, Any]) -> dict[str, Any]:
    _reject_tracked_secrets(payload, ("title", "summary", "links"))
    repo = resolve_repo()
    marker = EVENT_MARKER.format(event_id=payload["event_id"])
    links = " ".join(payload["links"])
    block = (
        f"{marker}\n\n"
        f"### {payload['timestamp'][:10]} - {payload['title']}\n\n"
        f"{payload['summary']}\n"
    )
    if links:
        block += f"\nLinks: {links}\n"
    with mutation_lock():
        target = safe_vault_path(repo, payload["target"])
        if not target.is_file():
            raise PathError(
                "authorized capture target is missing or not a regular file"
            )
        content = target.read_text(encoding="utf-8")
        if marker in content:
            return {"schema_version": 1, "command": "capture", "result": "noop"}
        updated = _append_to_section(content, "## Entries", block)
        atomic_write(target, updated)
    return {"schema_version": 1, "command": "capture", "result": "updated"}


def focus(payload: dict[str, Any]) -> dict[str, Any]:
    payload = validate_focus(payload)
    _reject_tracked_secrets(payload, ("project", "outcome", "done_when", "evidence"))
    repo = resolve_repo()
    marker = FOCUS_MARKER.format(event_id=payload["event_id"])
    block = (
        f"{marker}\n\n"
        f"- **Outcome:** {payload['outcome']}\n"
        f"- **Done when:** {payload['done_when']}\n"
        f"- **Evidence:** {payload['evidence']}\n"
    )
    with mutation_lock():
        daily_path = safe_vault_path(
            repo, f"05 Daily Notes/{payload['date']}.md"
        )
        if not daily_path.is_file():
            raise PathError("daily focus date does not have a Daily Note")
        daily = daily_path.read_text(encoding="utf-8")
        focus_body = _section_body(daily, "## Focus")
        if marker in focus_body:
            return {"schema_version": 1, "command": "focus", "result": "noop"}
        if FOCUS_MARKER_PREFIX in focus_body:
            raise ValueError("a ExampleProject focus is already confirmed for this date")
        daily = _replace_section(daily, "## Focus", block)
        atomic_write(daily_path, daily)
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
    done_block = (
        f"{marker}\n\n"
        f"### {project_name} closeout\n\n"
        f"- **Planned:** {payload['planned']}\n"
        f"- **Completed:** {payload['completed']}\n"
        f"- **Evidence:** {payload['evidence']}\n"
        f"- **Blocker:** {payload['blocker'] or 'None reported.'}\n"
    )
    progress_block = (
        f"{marker}\n\n"
        f"### {payload['date']}\n\n"
        f"- Completed: {payload['completed']}\n"
        f"- Evidence: {payload['evidence']}\n"
        f"- Blocker: {payload['blocker'] or 'None reported.'}\n"
    )
    with mutation_lock():
        daily_path = safe_vault_path(
            repo, f"05 Daily Notes/{payload['date']}.md"
        )
        project_path = safe_vault_path(repo, "02 Projects/ExampleProject.md")
        if not daily_path.is_file():
            raise PathError("closeout date does not have a Daily Note")
        if not project_path.is_file():
            raise PathError("ExampleProject project note is missing or invalid")
        daily = daily_path.read_text(encoding="utf-8")
        project = project_path.read_text(encoding="utf-8")
        focus_body = _section_body(daily, "## Focus")
        outcome_match = re.search(
            r"(?m)^- \*\*Outcome:\*\* (.+)$",
            focus_body,
        )
        if FOCUS_MARKER_PREFIX not in focus_body or not outcome_match:
            raise ValidationError("closeout requires a confirmed daily ExampleProject focus")
        if outcome_match.group(1) != payload["planned"]:
            raise ValidationError("closeout planned result must match the daily focus")
        if marker in daily and marker in project:
            return {"schema_version": 1, "command": "closeout", "result": "noop"}
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
            atomic_write(daily_path, daily)
        if marker not in project:
            project = _append_to_section(project, "## Progress", progress_block)
            atomic_write(project_path, project)
    return {"schema_version": 1, "command": "closeout", "result": "updated"}


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
