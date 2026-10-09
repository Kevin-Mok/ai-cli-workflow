#!/usr/bin/env python3
"""Check upstream or stage an immutable candidate for review; never auto-apply."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen
import os


def _cli_message(text: str, emoji: str) -> str:
    """Decorate authored prose without changing machine-readable output."""
    return text if os.environ.get("CLI_PLAIN") == "1" else f"{emoji} {text}"


REPOSITORY = "getsentry/skills"
SOURCE_PATH = "skills/prompt-optimizer"
API = f"https://api.github.com/repos/{REPOSITORY}"
SKILL_ROOT = Path(__file__).resolve().parents[1]


def fetch_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "linux-config-metaprompt-updater"})
    with urlopen(request, timeout=30) as response:
        return response.read()


def fetch_json(url: str):
    return json.loads(fetch_bytes(url))


def latest_revision() -> str:
    commits = fetch_json(f"{API}/commits?path={SOURCE_PATH}&per_page=1")
    return commits[0]["sha"]


def stage_candidate(destination: Path, revision: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("revision must be a full lowercase 40-character commit SHA")
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"candidate destination already exists: {destination}")
    tree = fetch_json(f"{API}/git/trees/{revision}?recursive=1")
    if tree.get("truncated"):
        raise ValueError("upstream tree was truncated; refusing an incomplete candidate")
    files = {}
    payloads = {}
    for entry in tree["tree"]:
        source = entry["path"]
        if not (source.startswith(SOURCE_PATH + "/") or source == "LICENSE"):
            continue
        if entry["type"] == "tree":
            continue
        if entry["type"] != "blob" or entry.get("mode") not in {"100644", "100755"}:
            raise ValueError(f"upstream entry is not a regular file: {source}")
        parts = PurePosixPath(source).parts
        if source.startswith("/") or ".." in parts or "\\" in source:
            raise ValueError(f"unsafe upstream path: {source}")
        relative = source.removeprefix(SOURCE_PATH + "/")
        name = {"SKILL.md": "UPSTREAM.md", "agents/openai.yaml": "UPSTREAM.openai.yaml",
                "LICENSE": "LICENSE.txt"}.get(relative, relative)
        if name in payloads:
            raise ValueError(f"duplicate mapped path: {name}")
        url = f"https://raw.githubusercontent.com/{REPOSITORY}/{revision}/{quote(source)}"
        content = fetch_bytes(url)
        payloads[name] = content
        files[name] = {"source": source, "sha256": hashlib.sha256(content).hexdigest()}
    if not {"UPSTREAM.md", "LICENSE.txt"}.issubset(payloads):
        raise ValueError("candidate is missing its entrypoint or license")
    manifest = {"repository": REPOSITORY, "revision": revision, "source_path": SOURCE_PATH,
                "retrieved_at": datetime.now(timezone.utc).date().isoformat(), "files": files}
    destination.mkdir(parents=True, exist_ok=False)
    for name, content in payloads.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(content)
    with (destination / "UPSTREAM.json").open("x", encoding="utf-8") as stream:
        json.dump(manifest, stream, indent=2)
        stream.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=_cli_message(__doc__, "📖"))
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true", help="Compare pinned and latest skill commits")
    action.add_argument("--stage", type=Path, metavar="NEW_DIRECTORY", help="Download a candidate into a new review directory")
    parser.add_argument("--revision", help="Stage this full commit SHA instead of the latest skill commit")
    args = parser.parse_args(argv)
    if args.check and args.revision:
        parser.error("--revision is only valid with --stage")
    try:
        current = json.loads((SKILL_ROOT / "UPSTREAM.json").read_text())["revision"]
        revision = args.revision or latest_revision()
        if args.check:
            print(_cli_message(f"Pinned: {current}\nLatest skill commit: {revision}", 'ℹ️'))
            print(_cli_message("Up to date." if revision == current else "Update available; stage and review before applying.", '⚠️'))
        else:
            stage_candidate(args.stage, revision)
            print(_cli_message(f"Candidate staged: {args.stage}\nRevision: {revision}\nReview using SOURCE.md; tracked and installed skills were not changed.", 'ℹ️'))
    except (OSError, ValueError, KeyError, IndexError) as exc:
        print(_cli_message(f"metaprompt update: {exc}", '❌'), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
