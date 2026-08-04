"""Command-line parsing and content-safe exit handling."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Sequence

from .deferred import defer, list_reminders, process_due, resolve, schedule
from .checkpoint import CheckpointError, run_checkpoint
from .doctor import build_report as build_doctor_report
from .doctor import text_report as doctor_text_report
from .migration import build_inventory, build_plan
from .migration_apply import apply_migration
from .migration_verify import verify_migration
from .paths import LockError, PathError
from .schema import ValidationError, load_payload
from .upgrade import UPGRADE_SPECS, apply_upgrade, build_upgrade_preview
from .vault import capture, closeout, focus, status_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="second-brain",
        description=(
            "Safely capture, retrieve, validate, and migrate the Second Brain."
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

    defer_parser = subparsers.add_parser(
        "defer", help="Store one private reminder for a future local date."
    )
    defer_parser.add_argument("--payload", required=True)
    schedule_parser = subparsers.add_parser(
        "schedule-deferred", help="Schedule one private unscheduled reminder."
    )
    schedule_parser.add_argument("--payload", required=True)
    subparsers.add_parser(
        "process-deferred", help="Promote due private reminders to the inbox."
    )
    list_deferred_parser = subparsers.add_parser(
        "list-deferred", help="List private inbox reminders as JSON."
    )
    list_deferred_parser.add_argument(
        "--format", choices=("json",), required=True
    )
    list_deferred_parser.add_argument(
        "--state", choices=("inbox", "someday"), default="inbox"
    )
    resolve_deferred_parser = subparsers.add_parser(
        "resolve-deferred", help="Resolve one private inbox reminder."
    )
    resolve_deferred_parser.add_argument("--payload", required=True)
    status_parser = subparsers.add_parser(
        "status", help="Show active projects, Inbox state, and recent Daily Notes."
    )
    status_parser.add_argument(
        "--format", choices=("text", "json"), default="text"
    )
    doctor_parser = subparsers.add_parser(
        "doctor", help="Audit vault structure, privacy, ownership, and LFS state."
    )
    doctor_parser.add_argument(
        "--format", choices=("text", "json"), default="text"
    )
    doctor_parser.add_argument("--check", action="store_true")
    checkpoint_parser = subparsers.add_parser(
        "checkpoint", help="Validate and ship one safe daily checkpoint."
    )
    checkpoint_parser.add_argument("--dry-run", action="store_true")
    checkpoint_parser.add_argument("--no-push", action="store_true")
    upgrade_parser = subparsers.add_parser(
        "upgrade", help="Preview or apply approval-bound protected vault upgrades."
    )
    upgrade_mode = upgrade_parser.add_mutually_exclusive_group(required=True)
    upgrade_mode.add_argument("--dry-run", action="store_true")
    upgrade_mode.add_argument("--apply", action="store_true")
    upgrade_parser.add_argument("--approve")

    migrate_parser = subparsers.add_parser(
        "migrate", help="Inventory, plan, apply, or verify safe text migrations."
    )
    migrate_commands = migrate_parser.add_subparsers(
        dest="migrate_command", required=True
    )
    inventory_parser = migrate_commands.add_parser(
        "inventory", help="Inventory external text sources without writing."
    )
    inventory_parser.add_argument("--source", action="append", required=True)
    plan_parser = migrate_commands.add_parser(
        "plan", help="Build a deterministic approval-bound migration plan."
    )
    plan_parser.add_argument("--inventory", required=True)
    apply_parser = migrate_commands.add_parser(
        "apply", help="Copy an approved plan with a private resume ledger."
    )
    apply_parser.add_argument("--plan", required=True)
    apply_parser.add_argument("--approve", required=True)
    verify_parser = migrate_commands.add_parser(
        "verify", help="Verify copied source and destination checksums."
    )
    verify_parser.add_argument("--ledger", required=True)
    return parser


def _print_json(value: dict[str, Any]) -> None:
    print(
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )


def _print_status_text(report: dict[str, Any]) -> None:
    print(f"Second Brain status for {report['date']}")
    print("Active projects:")
    for project in report["active_projects"]:
        print(f"- {project}")
    print(
        f"Inbox: {report['inbox']['count']} reviewed item(s) "
        f"at {report['inbox']['path']}"
    )
    private = report["private_reminders"]
    print(
        f"Private reminders: {private['someday']} someday, "
        f"{private['deferred']} deferred, {private['inbox']} inbox"
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
        if args.command == "defer":
            _print_json(defer(load_payload(args.payload)))
            return 0
        if args.command == "schedule-deferred":
            _print_json(schedule(load_payload(args.payload)))
            return 0
        if args.command == "process-deferred":
            _print_json(process_due())
            return 0
        if args.command == "list-deferred":
            _print_json(
                {
                    "schema_version": 1,
                    "command": "list-deferred",
                    "reminders": list_reminders(args.state),
                }
            )
            return 0
        if args.command == "resolve-deferred":
            _print_json(resolve(load_payload(args.payload)))
            return 0

        if args.command == "doctor":
            report = build_doctor_report()
            if args.format == "json":
                _print_json(report)
            else:
                sys.stdout.write(doctor_text_report(report))
            if args.check and report["summary"]["errors"]:
                return 1
            return 0
        if args.command == "checkpoint":
            _print_json(
                run_checkpoint(dry_run=args.dry_run, no_push=args.no_push)
            )
            return 0
        if args.command == "upgrade":
            if args.dry_run:
                if args.approve:
                    raise ValidationError("upgrade dry-run does not accept approval")
                _print_json(build_upgrade_preview())
                return 0
            if not args.approve:
                raise ValidationError("upgrade apply requires --approve SHA256")
            _print_json(apply_upgrade(UPGRADE_SPECS, args.approve))
            return 0
        if args.command == "migrate":
            if args.migrate_command == "inventory":
                _print_json(build_inventory(args.source))
                return 0
            if args.migrate_command == "plan":
                _print_json(build_plan(args.inventory))
                return 0
            if args.migrate_command == "apply":
                _print_json(apply_migration(args.plan, args.approve))
                return 0
            if args.migrate_command == "verify":
                report = verify_migration(args.ledger)
                _print_json(report)
                return 1 if report["summary"]["errors"] else 0
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
    except (ValidationError, PathError, LockError, CheckpointError) as error:
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
