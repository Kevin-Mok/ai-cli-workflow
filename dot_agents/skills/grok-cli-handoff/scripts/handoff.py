#!/usr/bin/env python3
"""Read-only checkout/STOP preflight and portable handoff template."""

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys


class HandoffError(Exception):
    pass


class HandoffParser(argparse.ArgumentParser):
    def error(self, message):
        super().error(("" if "--plain" in sys.argv else "⚠️ ") + message)


def task_slug(value):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", value):
        raise argparse.ArgumentTypeError("task must be 1-64 lowercase letters, digits or hyphens")
    return value


def git_read(repo, *args):
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE"):
        env.pop(key, None)
    try:
        result = subprocess.run(["git", "-C", str(repo), *args], env=env,
                                capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise HandoffError("Git check unavailable; verify Git and the checkout") from exc
    if result.returncode:
        raise HandoffError("Git check failed; verify checkout root and attached branch")
    return result.stdout.strip()


def preflight(repo, branch, task, plain):
    repo = repo.expanduser().resolve(strict=True)
    root = Path(git_read(repo, "rev-parse", "--show-toplevel")).resolve(strict=True)
    if repo != root:
        raise HandoffError("--repo must name the checkout root, not a subdirectory")
    actual_branch = git_read(repo, "symbolic-ref", "--short", "HEAD")
    if actual_branch != branch:
        raise HandoffError("branch mismatch; inspect local state before continuing")
    for marker in (root / ".harness/STOP", root / ".harness" / task / "STOP"):
        try:
            marker.lstat()  # Includes directories and dangling symlinks; never read content.
        except FileNotFoundError:
            continue
        print(("" if plain else "🛑 ") + f"Stopped: {marker}; await example-user's resume instruction",
              file=sys.stderr)
        return 3
    print(("" if plain else "✅ ") +
          f"Ready: {root} ({actual_branch}), task {task}; state check, not authorization")
    return 0


def main():
    plain = "--plain" in sys.argv
    parser = HandoffParser(
        description=("" if plain else "🧭 ") + "Grok CLI handoff: read-only template and preflight")
    parser.add_argument("--plain", action="store_true", help="ASCII human-facing output")
    commands = parser.add_subparsers(dest="command", required=True)
    template = commands.add_parser("template", help="print a Markdown handoff; writes no files")
    template.add_argument("--task", required=True, type=task_slug)
    check = commands.add_parser("preflight", help="check checkout, branch and STOP markers; does not launch")
    check.add_argument("--repo", required=True, type=Path)
    check.add_argument("--branch", required=True)
    check.add_argument("--task", required=True, type=task_slug)
    args = parser.parse_args()
    try:
        if args.command == "template":
            asset = Path(__file__).resolve().parents[1] / "assets/handoff.md"
            print(asset.read_text(encoding="utf-8").replace("{{TASK}}", args.task), end="")
            return 0
        return preflight(args.repo, args.branch, args.task, args.plain)
    except (HandoffError, OSError, RuntimeError) as exc:
        # Raw Git errors and marker contents are deliberately excluded.
        message = str(exc) if isinstance(exc, HandoffError) else "local path check failed; inspect checkout access"
        print(("" if args.plain else "⚠️ ") + "Blocked: " + message, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
