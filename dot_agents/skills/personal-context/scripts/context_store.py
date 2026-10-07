#!/usr/bin/env python3
"""Read and atomically update relevant private personal and project context.

Retrieval commands return private content; update/foundation/validate return counters.
Only the designated external root may own its own Git marker; alternate
repository roots, ancestor repositories, and installed skills stay forbidden.
"""

from __future__ import annotations

import argparse
import copy
from datetime import date, datetime, timezone
import fcntl
import json
import importlib.util
from types import ModuleType, SimpleNamespace
import os
from pathlib import Path
import re
import secrets
import stat
import sys
from typing import NoReturn, Protocol, TypedDict, cast, override
from contextlib import AbstractContextManager


DEFAULT_ROOT = Path("/home/example/coding/personal-context")
STORE_NAME = "context.json"
LOCK_NAME = ".context.lock"
MAX_BYTES = 2 * 1024 * 1024
SLUG = re.compile(r"[a-z0-9][a-z0-9._:-]{0,119}\Z")
UTC_TIME = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z\Z")
ENTRY_FIELDS = {"id", "key", "topic", "statement", "basis", "source", "scope"}
ENTRY_OPTIONAL = {"recorded_at", "status", "implication"}
QUESTION_FIELDS = {"id", "topic", "question", "reason", "status"}


class StoreError(Exception):
    """A diagnostic containing no submitted or persisted personal values."""


def _object(value: object, required: set[str], optional: set[str] | None = None) -> dict[str, object]:
    if not isinstance(value, dict) or not required <= value.keys() or value.keys() - required - (optional or set()):
        raise StoreError("Invalid object fields; consult the versioned storage reference.")
    return cast(dict[str, object], value)


def _text(value: object, limit: int = 4096) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit or "\0" in value:
        raise StoreError("Invalid text field; use nonempty text within the documented limit.")
    try:
        _ = value.encode("utf-8")
    except UnicodeError:
        raise StoreError("Invalid Unicode text; use valid UTF-8 characters.") from None
    return value


def _slug(value: object) -> str:
    if not isinstance(value, str) or not SLUG.fullmatch(value):
        raise StoreError("Invalid identifier; use a lowercase slug of at most 120 characters.")
    return value


def _timestamp(value: object) -> str:
    if not isinstance(value, str) or not UTC_TIME.fullmatch(value):
        raise StoreError("Invalid timestamp; use an ISO UTC timestamp ending in Z.")
    try:
        _ = datetime.fromisoformat(value)
    except ValueError:
        raise StoreError("Invalid calendar value in timestamp.") from None
    return value


def _as_of(value: object) -> None:
    if value is None:
        return
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        try:
            _ = date.fromisoformat(value)
            return
        except ValueError:
            raise StoreError("Invalid calendar value in source date.") from None
    _ = _timestamp(value)


def _array(value: object) -> list[object]:
    if not isinstance(value, list):
        raise StoreError("Invalid collection; expected a JSON array.")
    return cast(list[object], value)


def _entries(value: object, *, stored: bool) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    identifiers: set[str] = set()
    for item in _array(value):
        required = ENTRY_FIELDS | ENTRY_OPTIONAL if stored else ENTRY_FIELDS
        record = _object(item, required, set() if stored else ENTRY_OPTIONAL)
        for field in ("id", "key", "topic"):
            _ = _slug(record[field])
        if record["id"] in identifiers:
            raise StoreError("Duplicate entry identifiers are not allowed.")
        identifiers.add(cast(str, record["id"]))
        _ = _text(record["statement"])
        _ = _text(record["scope"], 512)
        if record["basis"] not in ("user_stated", "source_reported", "observed", "inferred"):
            raise StoreError("Invalid evidence basis; use a documented basis value.")
        source = _object(record["source"], {"ref", "as_of"})
        _ = _text(source["ref"], 1024)
        _as_of(source["as_of"])
        status = record.get("status", "unconfirmed" if record["basis"] == "inferred" else "active")
        if status not in ("active", "unconfirmed", "superseded") or (not stored and status == "superseded"):
            raise StoreError("Invalid entry status; new entries must be active or unconfirmed.")
        if record["basis"] == "inferred" and status == "active":
            raise StoreError("Interpretations must remain unconfirmed until replaced by user confirmation.")
        if "recorded_at" in record:
            _ = _timestamp(record["recorded_at"])
        if record.get("implication") is not None:
            _ = _text(record["implication"])
        result.append(copy.deepcopy(record))
    return result


def _questions(value: object, *, stored: bool) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    identifiers: set[str] = set()
    for item in _array(value):
        record = _object(item, QUESTION_FIELDS | ({"updated_at"} if stored else set()))
        _ = _slug(record["id"])
        _ = _slug(record["topic"])
        if record["id"] in identifiers:
            raise StoreError("Duplicate question identifiers are not allowed.")
        identifiers.add(cast(str, record["id"]))
        _ = _text(record["question"])
        _ = _text(record["reason"])
        if record["status"] not in ("open", "answered", "declined"):
            raise StoreError("Invalid question status; use open, answered, or declined.")
        if stored:
            _ = _timestamp(record["updated_at"])
        result.append(copy.deepcopy(record))
    return result


def empty_store() -> dict[str, object]:
    """Return an uninitialized schema without touching the filesystem."""
    return {"schema_version": 1, "revision": 0, "updated_at": None, "entries": [], "questions": [], "forgotten_keys": [], "forgotten_question_ids": []}


def validate_store(value: object) -> dict[str, object]:
    """Validate persisted schema without repairing or mutating it."""
    record = _object(value, set(empty_store()))
    if type(record["schema_version"]) is not int or record["schema_version"] != 1:
        raise StoreError("Unsupported schema version; preserve the store and migrate it explicitly.")
    if type(record["revision"]) is not int or record["revision"] < 0:
        raise StoreError("Invalid store revision; expected a nonnegative integer.")
    if record["updated_at"] is not None:
        _ = _timestamp(record["updated_at"])
    elif record["revision"] != 0:
        raise StoreError("An initialized store requires an update timestamp.")
    entries = _entries(record["entries"], stored=True)
    questions = _questions(record["questions"], stored=True)
    forgotten = [_slug(key) for key in _array(record["forgotten_keys"])]
    if len(set(forgotten)) != len(forgotten):
        raise StoreError("Duplicate forgotten keys are not allowed.")
    if any(item["key"] in forgotten for item in entries):
        raise StoreError("The store contains a forgotten key; preserve it for explicit repair.")
    forgotten_questions = [_slug(identifier) for identifier in _array(record["forgotten_question_ids"])]
    if len(set(forgotten_questions)) != len(forgotten_questions):
        raise StoreError("Duplicate forgotten question identifiers are not allowed.")
    if any(item["id"] in forgotten_questions for item in questions):
        raise StoreError("The store contains a forgotten question; preserve it for explicit repair.")
    return copy.deepcopy(record)


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise StoreError("Duplicate JSON object fields are not allowed.")
        result[key] = value
    return result


def _reject_constant(_: str) -> NoReturn:
    raise StoreError("Nonfinite JSON values are not allowed.")


def _decode(raw: bytes, *, max_bytes: int = MAX_BYTES) -> object:
    if len(raw) > max_bytes:
        raise StoreError("The JSON input exceeds its documented storage limit.")
    try:
        return cast(object, json.loads(raw, object_pairs_hook=_pairs, parse_constant=_reject_constant))
    except (ValueError, UnicodeError, RecursionError):
        raise StoreError("Invalid JSON; preserve the input and correct it before retrying.") from None


def _exists_at(directory: int, name: str) -> bool:
    try:
        _ = os.stat(name, dir_fd=directory, follow_symlinks=False)
        return True
    except FileNotFoundError:
        return False


def _reject_repository(directory: int, *, allow_git_marker: bool = False) -> None:
    if (_exists_at(directory, ".git") and not allow_git_marker) or all(_exists_at(directory, name) for name in ("HEAD", "objects", "refs")):
        raise StoreError("Private context cannot be stored inside a Git repository.")


def _root_fd(root: Path) -> int | None:
    if not root.is_absolute() or ".." in root.parts:
        raise StoreError("Use an absolute private root without parent traversal.")
    parts = root.parts[1:]
    for first, second in zip(parts, parts[1:]):
        if first in (".agents", ".codex", ".claude", ".cursor") and second in ("skills", "plugins"):
            raise StoreError("Private context cannot be stored inside installed agent skills or plugins.")
    directory = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        _reject_repository(directory)
        for index, part in enumerate(parts):
            try:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            except FileNotFoundError:
                os.close(directory)
                return None
            os.close(directory)
            directory = child
            _reject_repository(directory, allow_git_marker=root == DEFAULT_ROOT and index == len(parts) - 1)
        return directory
    except BaseException:
        os.close(directory)
        raise


def _directory_fd(root: Path, *, create: bool) -> int | None:
    root_fd = _root_fd(root)
    if root_fd is None:
        if create:
            raise StoreError("The private root is missing; restore it before updating context.")
        return None
    try:
        if create:
            try:
                os.mkdir("ai-context", 0o700, dir_fd=root_fd)
            except FileExistsError:
                pass
        try:
            directory = os.open("ai-context", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=root_fd)
        except FileNotFoundError:
            return None
        try:
            if os.fstat(directory).st_uid != os.geteuid():
                raise StoreError("The private store directory must be owned by the current user.")
            _reject_repository(directory)
            if create:
                os.fchmod(directory, 0o700)
            elif stat.S_IMODE(os.fstat(directory).st_mode) != 0o700:
                raise StoreError("Private store directory permissions must be 0700; an authorized update can repair them.")
            return directory
        except BaseException:
            os.close(directory)
            raise
    finally:
        os.close(root_fd)


def _regular_fd(directory: int, name: str, flags: int, *, private: bool = True) -> int:
    descriptor = os.open(name, flags | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600, dir_fd=directory)
    info = os.fstat(descriptor)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.geteuid():
        os.close(descriptor)
        raise StoreError("Store and lock destinations must be owned regular files without hardlinks.")
    if private and stat.S_IMODE(info.st_mode) != 0o600:
        os.close(descriptor)
        raise StoreError("Private store and lock permissions must be 0600; an authorized update can repair them.")
    return descriptor


def _load(directory: int | None, *, required: bool, private: bool = True) -> dict[str, object]:
    if directory is not None:
        try:
            descriptor = _regular_fd(directory, STORE_NAME, os.O_RDONLY, private=private)
        except FileNotFoundError:
            descriptor = None
        if descriptor is not None:
            with os.fdopen(descriptor, "rb") as handle:
                return validate_store(_decode(handle.read(MAX_BYTES + 1)))
    if required:
        raise StoreError("No private store exists; initialize it through an authorized update.")
    return empty_store()


def read_store(root: Path, *, topic: str | None = None, include_inactive: bool = False, required: bool = False) -> dict[str, object]:
    """Read selected memory without creating files, directories, or locks."""
    if topic is not None:
        _ = _slug(topic)
    directory = None
    try:
        directory = _directory_fd(root, create=False)
        if directory is not None and _exists_at(directory, LOCK_NAME):
            lock = _regular_fd(directory, LOCK_NAME, os.O_RDONLY)
            os.close(lock)
        record = _load(directory, required=required)
        record["entries"] = [item for item in cast(list[dict[str, object]], record["entries"]) if (topic is None or item["topic"] == topic) and (include_inactive or item["status"] != "superseded")]
        record["questions"] = [item for item in cast(list[dict[str, object]], record["questions"]) if topic is None or item["topic"] == topic]
        return record
    except OSError:
        raise StoreError("Cannot safely read private storage; check access, ownership, and symlinks.") from None
    finally:
        if directory is not None:
            os.close(directory)


def _payload(value: object) -> tuple[list[dict[str, object]], list[dict[str, object]], list[str], list[str]]:
    payload = _object(value, set(), {"entries", "questions", "forget_keys", "forget_question_ids"})
    entries = _entries(payload.get("entries", []), stored=False)
    questions = _questions(payload.get("questions", []), stored=False)
    forgotten = [_slug(key) for key in _array(payload.get("forget_keys", []))]
    if len(set(forgotten)) != len(forgotten):
        raise StoreError("Duplicate forgotten keys are not allowed.")
    forgotten_questions = [_slug(identifier) for identifier in _array(payload.get("forget_question_ids", []))]
    if len(set(forgotten_questions)) != len(forgotten_questions):
        raise StoreError("Duplicate forgotten question identifiers are not allowed.")
    return entries, questions, forgotten, forgotten_questions


def _merge(record: dict[str, object], incoming: list[dict[str, object]], questions: list[dict[str, object]], forgotten: list[str], forgotten_questions: list[str], now: str) -> dict[str, object]:
    result = copy.deepcopy(record)
    suppressed = set(cast(list[str], result["forgotten_keys"])) | set(forgotten)
    entries = [item for item in cast(list[dict[str, object]], result["entries"]) if item["key"] not in suppressed]
    by_id = {item["id"]: item for item in entries}
    for new in incoming:
        if new["key"] in suppressed:
            raise StoreError("An update would restore forgotten context; explicit restoration is not supported.")
        previous = by_id.get(new["id"])
        if previous is not None:
            compared = ENTRY_FIELDS | {"implication"}
            if any(previous.get(field) != new.get(field) for field in compared) or ("recorded_at" in new and previous["recorded_at"] != new["recorded_at"]):
                raise StoreError("An entry identifier was reused with different evidence; use a new identifier.")
            continue
        new["recorded_at"] = new.get("recorded_at", now)
        new["implication"] = new.get("implication")
        new["status"] = new.get("status", "unconfirmed" if new["basis"] == "inferred" else "active")
        same_key = [item for item in entries if item["key"] == new["key"]]
        if new["basis"] == "user_stated" and new["status"] == "active":
            recorded = datetime.fromisoformat(cast(str, new["recorded_at"]))
            if any(recorded < datetime.fromisoformat(cast(str, old["recorded_at"])) for old in same_key if old["basis"] == "user_stated" and old["status"] == "active"):
                raise StoreError("A backdated correction cannot supersede newer user evidence; ask for current confirmation.")
            for old in same_key:
                old["status"] = "superseded"
        elif any(old["basis"] == "user_stated" and old["status"] == "active" for old in same_key):
            new["status"] = "unconfirmed"
        entries.append(new)
        by_id[new["id"]] = new
    result["entries"] = entries
    result["forgotten_keys"] = sorted(suppressed)
    suppressed_questions = set(cast(list[str], result["forgotten_question_ids"])) | set(forgotten_questions)
    all_questions = [item for item in cast(list[dict[str, object]], result["questions"]) if item["id"] not in suppressed_questions]
    by_question = {item["id"]: index for index, item in enumerate(all_questions)}
    for question in questions:
        if question["id"] in suppressed_questions:
            raise StoreError("An update would restore a forgotten question; explicit restoration is not supported.")
        index = by_question.get(question["id"])
        if index is not None and all_questions[index]["status"] in ("answered", "declined") and question["status"] == "open":
            raise StoreError("A completed question cannot be reopened by replay; use a new question only after an explicit revisit request.")
        if index is not None and all(all_questions[index][field] == question[field] for field in QUESTION_FIELDS):
            continue
        question["updated_at"] = now
        if index is None:
            by_question[question["id"]] = len(all_questions)
            all_questions.append(question)
        else:
            all_questions[index] = question
    result["questions"] = all_questions
    result["forgotten_question_ids"] = sorted(suppressed_questions)
    return result


def _write(directory: int, record: dict[str, object], *, name: str = STORE_NAME, max_bytes: int = MAX_BYTES) -> None:
    temporary = ".context-" + secrets.token_hex(12) + ".tmp"
    raw = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if len(raw) > max_bytes:
        raise StoreError("The updated context exceeds its documented storage limit.")
    try:
        descriptor = _regular_fd(directory, temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, private=False)
        with os.fdopen(descriptor, "wb") as handle:
            os.fchmod(handle.fileno(), 0o600)
            _ = handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        # Recheck the destination immediately before replacement.
        try:
            previous = _regular_fd(directory, name, os.O_RDONLY, private=False)
        except FileNotFoundError:
            previous = None
        if previous is not None:
            os.close(previous)
        os.replace(temporary, name, src_dir_fd=directory, dst_dir_fd=directory)
        os.fsync(directory)
    finally:
        try:
            os.unlink(temporary, dir_fd=directory)
        except FileNotFoundError:
            pass


def metadata(record: dict[str, object]) -> dict[str, object]:
    """Return counters only; keys, topics, statements, and questions are private."""
    return {"ok": True, "schema_version": 1, "revision": record["revision"], "entries": len(cast(list[object], record["entries"])), "questions": len(cast(list[object], record["questions"])), "forgotten_keys": len(cast(list[object], record["forgotten_keys"])), "forgotten_question_ids": len(cast(list[object], record["forgotten_question_ids"]))}


class ProjectEnvelope(TypedDict):
    schema_version: int
    revision: int
    updated_at: str | None
    projects: list[dict[str, object]]
    findings: list[dict[str, object]]


class _Knowledge(Protocol):
    """Typed boundary for a bundled module loaded by its absolute file path."""
    def load_projects(self, directory: int | None, *, private: bool = True) -> ProjectEnvelope: ...
    def after_personal_update(self, directory: int, personal: dict[str, object], projects: ProjectEnvelope) -> None: ...
    def locked(self, root: Path, *, write: bool) -> AbstractContextManager[int | None]: ...
    def foundation(self, root: Path, coding_root: Path, *, batch_size: int = 8, project: str | None = None) -> dict[str, object]: ...
    def retrieve(self, root: Path, command: str, *, topic: str | None = None, project: str | None = None, query: str | None = None, identifier: str | None = None, limit: int = 8, char_budget: int = 6000) -> dict[str, object]: ...


def _sibling(name: str) -> ModuleType:
    """Load portable bundled code by file path, independent of cwd/sys.path."""
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    if spec is None or spec.loader is None:
        raise StoreError("A bundled helper is missing; reinstall the complete skill.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _knowledge() -> _Knowledge:
    module = _sibling("knowledge_store")
    setattr(module, "c", SimpleNamespace(**globals()))
    return cast(_Knowledge, cast(object, module))


def update_store(root: Path, payload: object) -> dict[str, object]:
    """Merge one fully validated operation while holding an exclusive lock."""
    incoming, questions, forgotten, forgotten_questions = _payload(payload)
    directory = lock = None
    try:
        directory = _directory_fd(root, create=True)
        if directory is None:
            raise StoreError("The private store directory is unavailable.")
        lock = _regular_fd(directory, LOCK_NAME, os.O_RDWR | os.O_CREAT, private=False)
        os.fchmod(lock, 0o600)
        fcntl.flock(lock, fcntl.LOCK_EX)
        record = _load(directory, required=False, private=False)
        knowledge = _knowledge()
        projects = knowledge.load_projects(directory, private=False)
        now = datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")
        result = _merge(record, incoming, questions, forgotten, forgotten_questions, now)
        changed = result != record
        if changed:
            result["revision"] = cast(int, record["revision"]) + 1
            result["updated_at"] = now
            _ = validate_store(result)
            _write(directory, result)
        elif _exists_at(directory, STORE_NAME):
            existing = _regular_fd(directory, STORE_NAME, os.O_RDONLY, private=False)
            try:
                os.fchmod(existing, 0o600)
            finally:
                os.close(existing)
        knowledge.after_personal_update(directory, result, projects)
        return {**metadata(result), "changed": changed}
    except OSError:
        raise StoreError("Private storage update failed; check access, ownership, symlinks, and free space. Re-read before retrying.") from None
    finally:
        if lock is not None:
            os.close(lock)
        if directory is not None:
            os.close(directory)


class _Parser(argparse.ArgumentParser):
    @override
    def error(self, message: str) -> NoReturn:
        raise StoreError("Invalid command arguments; run --help for supported syntax.")


class _Arguments(argparse.Namespace):
    root: Path = DEFAULT_ROOT
    command: str = ""
    topic: str | None = None
    include_inactive: bool = False
    coding_root: Path = Path("/home/example/coding")
    batch_size: int = 8
    project: str | None = None
    query: str | None = None
    id: str | None = None
    limit: int = 8
    char_budget: int = 6000


def main(argv: list[str] | None = None) -> int:
    """Run the CLI, keeping diagnostics free of private payloads and paths."""
    parser = _Parser(description=__doc__)
    _ = parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Absolute private root; override only for synthetic fixtures.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    read = subparsers.add_parser("read")
    _ = read.add_argument("--topic")
    _ = read.add_argument("--include-inactive", action="store_true")
    _ = subparsers.add_parser("validate")
    update = subparsers.add_parser("update")
    _ = update.add_argument("--payload", choices=["-"], required=True, help="Read the operation JSON from standard input.")
    for command in ("topics", "projects", "brief"):
        compact = subparsers.add_parser(command)
        _ = compact.add_argument("--limit", type=int, default=8)
        _ = compact.add_argument("--char-budget", type=int, default=6000)
        if command == "projects": _ = compact.add_argument("--query")
        if command == "brief":
            _ = compact.add_argument("--topic")
            _ = compact.add_argument("--project")
    detail = subparsers.add_parser("detail")
    _ = detail.add_argument("--id", required=True)
    foundation = subparsers.add_parser("foundation")
    _ = foundation.add_argument("--coding-root", type=Path, default=Path("/home/example/coding"))
    _ = foundation.add_argument("--batch-size", type=int, default=8)
    _ = foundation.add_argument("--project")
    try:
        args = parser.parse_args(argv, namespace=_Arguments())
        if args.command == "update":
            output = update_store(args.root, _decode(sys.stdin.buffer.read(MAX_BYTES + 1)))
        elif args.command == "validate":
            knowledge = _knowledge()
            with knowledge.locked(args.root, write=False) as directory:
                personal = _load(directory, required=False)
                projects = knowledge.load_projects(directory)
                if personal["revision"] == 0 and projects["revision"] == 0:
                    raise StoreError("No authoritative private store exists; initialize through update or foundation.")
                output = {**metadata(personal), "projects": len(projects["projects"]), "findings": len(projects["findings"])}
        elif args.command == "foundation":
            knowledge = _knowledge()
            output = knowledge.foundation(args.root, args.coding_root, batch_size=args.batch_size, project=args.project)
        elif args.command in ("topics", "projects", "brief", "detail"):
            knowledge = _knowledge()
            output = knowledge.retrieve(args.root, args.command, topic=args.topic, project=args.project, query=args.query, identifier=args.id, limit=args.limit, char_budget=args.char_budget)
        else:
            output = read_store(args.root, topic=args.topic, include_inactive=args.include_inactive)
        print(json.dumps(output, ensure_ascii=False, separators=(",", ":")) if args.command in ("topics", "projects", "brief") else json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError):
        print(json.dumps({"ok": False, "error": "Cannot safely inspect source evidence; check root access, containment and readable project files."}), file=sys.stderr)
        return 1
    except StoreError as error:
        print(json.dumps({"ok": False, "error": str(error)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    _ = sys.modules.setdefault("context_store", sys.modules[__name__])
    raise SystemExit(main())
