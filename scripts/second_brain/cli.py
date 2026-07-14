"""Command-line parsing and content-safe exit handling."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Sequence

from .paths import LockError, PathError
from .schema import ValidationError, load_payload
from .vault import capture, closeout, focus, status_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="second-brain",
        description=(
            "Safely capture, retrieve, validate, and checkpoint the Second Brain."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    capture_parser = subparsers.add_parser(
        "capture", help="Capture a versioned JSON event."
    )
    capture_parser.add_argument("--kind", required=True)
    capture_parser.add_argument("--payload", required=True)

    closeout_parser = subparsers.add_parser(
        "closeout", help="Apply a confirmed boss-readable session closeout."
    )
    closeout_parser.add_argument("--payload", required=True)

    focus_parser = subparsers.add_parser(
        "focus", help="Persist one confirmed measurable ExampleProject outcome."
    )
    focus_parser.add_argument("--payload", required=True)

    status_parser = subparsers.add_parser(
        "status", help="Show active projects, Inbox state, and recent Daily Notes."
    )
    status_parser.add_argument(
        "--format", choices=("text", "json"), default="text"
    )
    return parser


def _print_json(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))


def _print_status_text(report: dict[str, Any]) -> None:
    print(f"Second Brain status for {report['date']}")
    print("Active projects:")
    for project in report["active_projects"]:
        print(f"- {project}")
    print(
        f"Inbox: {report['inbox']['count']} reviewed item(s) "
        f"at {report['inbox']['path']}"
    )
    print("Latest Daily Notes: " + ", ".join(report["latest_daily_notes"]))


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "status":
            report = status_report()
            if args.format == "json":
                _print_json(report)
            else:
                _print_status_text(report)
            return 0
        if args.command == "capture":
            payload = load_payload(args.payload)
            _print_json(capture(args.kind, payload))
            return 0
        if args.command == "focus":
            payload = load_payload(args.payload)
            _print_json(focus(payload))
            return 0
        if args.command == "closeout":
            payload = load_payload(args.payload)
            _print_json(closeout(payload))
            return 0
        parser.error("unsupported command")
    except (ValidationError, PathError, LockError) as error:
        print(f"second-brain: {error}", file=sys.stderr)
        return 2
    except ValueError as error:
        print(f"second-brain: {error}", file=sys.stderr)
        return 2
    except (OSError, UnicodeError):
        print(
            "second-brain: filesystem operation failed; "
            "check vault and state permissions",
            file=sys.stderr,
        )
        return 2
    return 2
