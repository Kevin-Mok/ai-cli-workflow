"""Deterministic, read-only health checks for the tracked Second Brain."""

from __future__ import annotations

import hashlib
import os
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterable

from .content_security import MAX_SECRET_SCAN_BYTES, bounded_utf8, likely_secret_name, redact
from .doctor_contract import (
    CANONICAL_OWNERS,
    IMPORT_PREFIX,
    PLACEHOLDER_RE,
    RECOVERY_NAME_RE,
    REQUIRED_PATHS,
    STATUS_PREFIXES,
)
from .doctor_lfs import lfs_tracked
from .paths import PathError, resolve_repo


def _finding(
    code: str,
    key: str,
    severity: str,
    message: str,
    paths: Iterable[tuple[str, int]],
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    locations = [
        {"line": line, "path": path}
        for path, line in sorted(paths, key=lambda item: (item[0], item[1]))
    ]
    return {
        "code": code,
        "details": details or {},
        "key": key,
        "locations": locations,
        "message": message,
        "severity": severity,
    }


def _doctor_repo() -> Path:
    override = os.environ.get("SECOND_BRAIN_REPO_ROOT")
    if override:
        candidate = Path(override).expanduser()
        if not candidate.is_absolute():
            raise PathError("Second Brain repository path must be absolute")
        lexical = candidate.absolute()
        try:
            resolved = lexical.resolve(strict=True)
        except OSError as error:
            raise PathError("Second Brain repository could not be resolved") from error
        if resolved != lexical or not (resolved / ".git").exists():
            raise PathError("Second Brain repository path is invalid")
        return resolved
    module = Path(__file__).resolve()
    for parent in module.parents:
        if (parent / ".git").exists():
            return parent
    return resolve_repo()


def _vault_entries(vault: Path) -> tuple[list[Path], list[Path], list[Path]]:
    files: list[Path] = []
    symlinks: list[Path] = []
    hard_links: list[Path] = []
    for directory, directory_names, file_names in os.walk(vault, followlinks=False):
        parent = Path(directory)
        retained_directories = []
        for name in sorted(directory_names):
            path = parent / name
            if path.is_symlink():
                symlinks.append(path)
            else:
                retained_directories.append(name)
        directory_names[:] = retained_directories
        for name in sorted(file_names):
            path = parent / name
            if path.is_symlink():
                symlinks.append(path)
            elif path.is_file():
                if path.stat().st_nlink > 1:
                    hard_links.append(path)
                else:
                    files.append(path)
    return sorted(files), sorted(symlinks), sorted(hard_links)


def _frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    closing = text.find("\n---\n", 4)
    if closing < 0:
        return None
    values: dict[str, str] = {}
    for line in text[4:closing].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values


def _import_body(content: bytes) -> bytes | None:
    if not content.startswith(b"---\n"):
        return None
    closing = content.find(b"\n---\n\n", 4)
    if closing < 0:
        return None
    return content[closing + len(b"\n---\n\n") :]


def _paragraphs(text: str) -> list[tuple[int, str]]:
    paragraphs: list[tuple[int, str]] = []
    buffer: list[str] = []
    start = 1
    for number, line in enumerate(text.splitlines(), start=1):
        if line.strip():
            if not buffer:
                start = number
            buffer.append(line)
        elif buffer:
            paragraphs.append((start, "\n".join(buffer)))
            buffer = []
    if buffer:
        paragraphs.append((start, "\n".join(buffer)))
    return paragraphs


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value)).strip().casefold()


def _line_for(text: str, pattern: re.Pattern[str]) -> int:
    match = pattern.search(text)
    if not match:
        return 1
    return text.count("\n", 0, match.start()) + 1


def _content_findings(
    repo: Path,
    vault: Path,
    files: list[Path],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    markdown: dict[str, tuple[str, Path]] = {}
    for path in files:
        relative = path.relative_to(vault).as_posix()
        secret_named = likely_secret_name(path.name)
        if secret_named:
            findings.append(
                _finding(
                    "likely_secret",
                    f"likely_secret:{relative}",
                    "error",
                    "Tracked file has a secret-like name.",
                    [(f"second-brain/{relative}", 1)],
                )
            )
        try:
            file_size = path.stat().st_size
        except OSError:
            file_size = MAX_SECRET_SCAN_BYTES
        if file_size >= MAX_SECRET_SCAN_BYTES:
            if path.suffix.lower() == ".md":
                findings.append(
                    _finding(
                        "oversized_text",
                        f"oversized_text:{relative}",
                        "error",
                        "Tracked Markdown exceeds the safe text-audit limit.",
                        [(f"second-brain/{relative}", 1)],
                    )
                )
            continue
        try:
            with path.open("rb") as stream:
                content = stream.read(MAX_SECRET_SCAN_BYTES + 1)
            if len(content) >= MAX_SECRET_SCAN_BYTES:
                if path.suffix.lower() == ".md":
                    findings.append(
                        _finding(
                            "oversized_text",
                            f"oversized_text:{relative}",
                            "error",
                            "Tracked Markdown exceeds the safe text-audit limit.",
                            [(f"second-brain/{relative}", 1)],
                        )
                    )
                continue
            text = content.decode("utf-8")
        except UnicodeError:
            if path.suffix.lower() == ".md":
                findings.append(
                    _finding(
                        "invalid_utf8",
                        f"invalid_utf8:{relative}",
                        "error",
                        "Tracked Markdown must be valid UTF-8.",
                        [(f"second-brain/{relative}", 1)],
                    )
                )
            continue
        if not secret_named and redact(text) != text:
            findings.append(
                _finding(
                    "likely_secret",
                    f"likely_secret:{relative}",
                    "error",
                    "Tracked file contains likely credential material.",
                    [(f"second-brain/{relative}", 1)],
                )
            )
        if path.suffix.lower() != ".md":
            continue
        markdown[relative] = (text, path)
        expected_fields: tuple[str, ...] = ()
        if relative.startswith("00 Context/"):
            expected_fields = ("tags", "date", "visibility")
        elif relative.startswith(STATUS_PREFIXES):
            expected_fields = ("tags", "status", "date", "visibility")
        elif relative.startswith(IMPORT_PREFIX):
            expected_fields = (
                "tags",
                "status",
                "date",
                "visibility",
                "source_sha256",
            )
        if expected_fields:
            metadata = _frontmatter(text)
            if metadata is None:
                findings.append(
                    _finding(
                        "malformed_frontmatter",
                        f"malformed_frontmatter:{relative}",
                        "error",
                        "Tracked note frontmatter is missing or malformed.",
                        [(f"second-brain/{relative}", 1)],
                    )
                )
            else:
                for field in expected_fields:
                    if field not in metadata:
                        findings.append(
                            _finding(
                                "missing_frontmatter_field",
                                f"missing_frontmatter_field:{relative}:{field}",
                                "error",
                                "Tracked note frontmatter is missing a required field.",
                                [(f"second-brain/{relative}", 1)],
                                {"field": field},
                            )
                        )
                if metadata.get("visibility") != "public-sanitized":
                    findings.append(
                        _finding(
                            "unsafe_visibility",
                            f"unsafe_visibility:{relative}",
                            "error",
                            "Tracked note visibility is not public-sanitized.",
                            [(f"second-brain/{relative}", 1)],
                        )
                    )
                if relative.startswith(IMPORT_PREFIX) and "source_sha256" in metadata:
                    source_sha256 = metadata["source_sha256"]
                    if not re.fullmatch(r"[0-9a-f]{64}", source_sha256):
                        findings.append(
                            _finding(
                                "invalid_source_sha256",
                                f"invalid_source_sha256:{relative}",
                                "error",
                                "Imported note source checksum is invalid.",
                                [(f"second-brain/{relative}", 1)],
                            )
                        )
                    else:
                        body = _import_body(content)
                        body_sha256 = (
                            hashlib.sha256(body).hexdigest()
                            if body is not None
                            else None
                        )
                        if body_sha256 != source_sha256:
                            findings.append(
                                _finding(
                                    "source_sha256_mismatch",
                                    f"source_sha256_mismatch:{relative}",
                                    "error",
                                    (
                                        "Imported note body does not match its "
                                        "source checksum."
                                    ),
                                    [(f"second-brain/{relative}", 1)],
                                )
                            )
        if PLACEHOLDER_RE.search(text):
            findings.append(
                _finding(
                    "unresolved_placeholder",
                    f"unresolved_placeholder:{relative}",
                    "warning",
                    "Tracked note contains an unresolved placeholder.",
                    [(f"second-brain/{relative}", _line_for(text, PLACEHOLDER_RE))],
                )
            )
    findings.extend(_duplicate_owner_findings(repo, markdown))
    return findings


def _duplicate_owner_findings(
    repo: Path, markdown: dict[str, tuple[str, Path]]
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    vault_paragraphs: dict[str, list[tuple[int, str]]] = {
        relative: [
            (line, normalized)
            for line, paragraph in _paragraphs(text)
            if len(normalized := _normalize(paragraph)) >= 120
        ]
        for relative, (text, _path) in markdown.items()
    }
    for owner_relative in CANONICAL_OWNERS:
        owner = repo / owner_relative
        if not owner.is_file() or owner.is_symlink():
            continue
        try:
            owner_text, oversized = bounded_utf8(owner)
        except OSError:
            continue
        if oversized:
            findings.append(_finding(
                "oversized_canonical_owner",
                f"oversized_canonical_owner:{owner_relative}", "error",
                "Canonical owner exceeds the safe content-audit limit.",
                [(owner_relative, 1)],
            ))
            continue
        if owner_text is None:
            continue
        for owner_line, paragraph in _paragraphs(owner_text):
            normalized = _normalize(paragraph)
            if len(normalized) < 120:
                continue
            for relative, candidates in vault_paragraphs.items():
                matches = [
                    line
                    for line, candidate in candidates
                    if candidate == normalized
                ]
                if not matches:
                    continue
                findings.append(
                    _finding(
                        "duplicate_canonical_owner",
                        f"duplicate_canonical_owner:{owner_relative}:{relative}",
                        "error",
                        "A canonical owner paragraph is duplicated in the vault.",
                        [
                            (owner_relative, owner_line),
                            (f"second-brain/{relative}", matches[0]),
                        ],
                        {"matches": len(matches), "owner": owner_relative},
                    )
                )
    return findings


def build_report() -> dict[str, Any]:
    repo = _doctor_repo()
    vault = repo / "second-brain"
    findings: list[dict[str, Any]] = []
    if vault.is_symlink():
        findings.append(
            _finding(
                "vault_root_symlink",
                "vault_root_symlink:second-brain",
                "error",
                "Second Brain vault root must not be a symlink.",
                [("second-brain", 1)],
            )
        )
        return _report(findings)
    if not vault.is_dir():
        findings.append(
            _finding(
                "missing_vault",
                "missing_vault:second-brain",
                "error",
                "Second Brain vault root is missing.",
                [("second-brain", 1)],
            )
        )
        return _report(findings)

    for relative in REQUIRED_PATHS:
        path = vault / relative
        if not path.is_file() or path.is_symlink():
            findings.append(
                _finding(
                    "missing_required_path",
                    f"missing_required_path:{relative}",
                    "error",
                    "A required Second Brain path is missing.",
                    [(f"second-brain/{relative}", 1)],
                )
            )
    files, symlinks, hard_links = _vault_entries(vault)
    for path in symlinks:
        relative = path.relative_to(vault).as_posix()
        findings.append(
            _finding(
                "vault_symlink",
                f"vault_symlink:{relative}",
                "error",
                "Tracked vault entries must not be symlinks.",
                [(f"second-brain/{relative}", 1)],
            )
        )
    for path in hard_links:
        relative = path.relative_to(vault).as_posix()
        findings.append(
            _finding(
                "vault_hard_link",
                f"vault_hard_link:{relative}",
                "error",
                "Tracked vault entries must not be hard links.",
                [(f"second-brain/{relative}", 1)],
            )
        )
    for path in files:
        if not RECOVERY_NAME_RE.fullmatch(path.name):
            continue
        relative = path.relative_to(vault).as_posix()
        findings.append(
            _finding(
                "preserved_recovery_artifact",
                f"preserved_recovery_artifact:{relative}",
                "error",
                "A preserved concurrent-write recovery artifact needs review.",
                [(f"second-brain/{relative}", 1)],
            )
        )
    findings.extend(_content_findings(repo, vault, files))
    attachments = vault / "07 Attachments"
    for path in files:
        if attachments not in path.parents or path.suffix.lower() == ".md":
            continue
        relative = path.relative_to(vault).as_posix()
        if not lfs_tracked(repo, path):
            findings.append(
                _finding(
                    "non_lfs_attachment",
                    f"non_lfs_attachment:{relative}",
                    "error",
                    "Attachment media is not tracked through Git LFS.",
                    [(f"second-brain/{relative}", 1)],
                )
            )
    return _report(findings)


def _report(findings: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(findings, key=lambda finding: finding["key"])
    errors = sum(finding["severity"] == "error" for finding in ordered)
    warnings = sum(finding["severity"] == "warning" for finding in ordered)
    status = "error" if errors else "warning" if warnings else "pass"
    return {
        "schema_version": 1,
        "command": "doctor",
        "summary": {"status": status, "errors": errors, "warnings": warnings},
        "findings": ordered,
    }


def text_report(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        f"Second Brain doctor: {summary['status']}",
        f"Errors: {summary['errors']}",
        f"Warnings: {summary['warnings']}",
    ]
    if report["findings"]:
        lines.append("Findings:")
        for finding in report["findings"]:
            location = finding["locations"][0]["path"]
            lines.append(
                f"- {finding['severity'].upper()} {finding['code']}: "
                f"{finding['message']} [{location}]"
            )
    else:
        lines.append("Findings: none")
    return "\n".join(lines) + "\n"
