"""Content-safe secret detection shared by capture, doctor, and migration."""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path


MAX_SECRET_SCAN_BYTES = 1_000_000
SECRET_NAMES = {
    ".env",
    ".netrc",
    "_netrc",
    "credentials",
    "credentials.json",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
    "secrets",
    "secrets.json",
    "token",
    "token.txt",
}
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
        r"[\"']?\s*[:=]\s*[^\s,;]+"
    ),
)


def likely_secret_name(name: str) -> bool:
    """Return whether a filename is reserved for likely credential material."""

    lowered = name.casefold()
    return lowered in SECRET_NAMES or lowered.startswith(".env.")


def bounded_utf8(path: Path) -> tuple[str | None, bool]:
    """Return bounded UTF-8 text and whether the strict size limit was hit."""

    with path.open("rb") as stream:
        content = stream.read(MAX_SECRET_SCAN_BYTES + 1)
    if len(content) >= MAX_SECRET_SCAN_BYTES:
        return None, True
    try:
        return content.decode("utf-8"), False
    except UnicodeError:
        return None, False


def _netrc_tokens(text: str) -> Iterator[str]:
    """Yield netrc-style tokens in one linear pass, ignoring comments."""

    token: list[str] = []
    quote = ""
    escaped = False
    comment = False
    for character in text:
        if comment:
            if character in "\r\n":
                comment = False
            continue
        if escaped:
            token.append(character)
            escaped = False
            continue
        if character == "\\":
            escaped = True
            continue
        if quote:
            if character == quote:
                quote = ""
            else:
                token.append(character)
            continue
        if character in {"'", '"'}:
            quote = character
            continue
        if character == "#":
            if token:
                yield "".join(token)
                token.clear()
            comment = True
            continue
        if character.isspace():
            if token:
                yield "".join(token)
                token.clear()
            continue
        token.append(character)
    if escaped:
        token.append("\\")
    if token:
        yield "".join(token)


def _contains_netrc_credentials(text: str) -> bool:
    tokens = iter(_netrc_tokens(text))
    in_stanza = False
    for token in tokens:
        keyword = token.casefold()
        if keyword == "machine":
            in_stanza = next(tokens, None) is not None
            continue
        if keyword == "default":
            in_stanza = True
            continue
        if keyword == "macdef":
            in_stanza = False
            continue
        if in_stanza and keyword == "password":
            return next(tokens, None) is not None
    return False


def redact(text: str) -> str:
    """Redact supported credential shapes without returning matched content."""

    if _contains_netrc_credentials(text):
        return "[REDACTED]"
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted
