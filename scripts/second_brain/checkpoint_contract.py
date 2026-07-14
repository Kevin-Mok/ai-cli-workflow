"""Stable policy constants and errors for daily checkpoints."""

from __future__ import annotations

import re


ALLOWLIST = (
    "second-brain/00 Context/",
    "second-brain/01 Inbox/",
    "second-brain/02 Projects/",
    "second-brain/03 Areas/",
    "second-brain/04 Resources/",
    "second-brain/05 Daily Notes/",
    "second-brain/06 Archive/",
    "second-brain/07 Attachments/",
    "dot_codex/config.toml",
)
MEDIA_SUFFIXES = {
    ".aac",
    ".avif",
    ".avi",
    ".flac",
    ".gif",
    ".jpeg",
    ".jpg",
    ".m4a",
    ".mkv",
    ".mov",
    ".mp3",
    ".mp4",
    ".ogg",
    ".opus",
    ".pdf",
    ".png",
    ".svg",
    ".wav",
    ".webm",
    ".webp",
}
SENSITIVE_PARTS = {
    ".aws",
    ".azure",
    ".git",
    ".gnupg",
    ".kube",
    ".ssh",
    "credentials",
    "private",
    "raw",
    "raw-session",
    "secrets",
}
LFS_POINTER = re.compile(
    rb"version https://git-lfs.github.com/spec/v1\n"
    rb"oid sha256:[0-9a-f]{64}\n"
    rb"size [0-9]+\n?\Z"
)


class CheckpointError(RuntimeError):
    """A checkpoint precondition or safety validation failed."""
