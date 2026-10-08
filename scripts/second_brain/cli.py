"""Command-line parsing and content-safe exit handling."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from pathlib import Path
import os
import shlex
import shutil
import subprocess
import tempfile
import threading
import time
import json
import sys
from typing import Any, Sequence

from . import sessions
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
    sessions_parser = subparsers.add_parser(
        "sessions", help="Refresh or explicitly review the private Codex work digest."
    )
    sessions_commands = sessions_parser.add_subparsers(
        dest="sessions_command", required=True
    )
    for operation in ("refresh", "review"):
        operation_parser = sessions_commands.add_parser(operation)
        operation_parser.add_argument(
            "--format", choices=("text", "json"), default="text"
        )
        if operation == "review":
            selection = operation_parser.add_mutually_exclusive_group()
            selection.add_argument(
                "--limit", type=int, choices=range(1, 21), default=None, metavar="N",
                help="Show the N most recently active directories, with three sessions each (1 to 20; default 5).",
            )
            selection.add_argument(
                "--all", dest="all_sessions", action="store_true",
                help="Show all eligible historical work sessions.",
            )
            operation_parser.add_argument(
                "--refresh-limit", type=int, choices=range(0, 21), default=None, metavar="N",
                help="Generate at most N selected recaps (0 to 20; default three per directory, capped at 20).",
            )
            operation_parser.add_argument(
                "--plain", action="store_true",
                help="Use ASCII text without emoji; escape non-ASCII content (JSON unchanged).",
            )
            operation_parser.add_argument(
                "--no-pager", action="store_true",
                help="Print text directly instead of opening bat/less.",
            )
            operation_parser.add_argument(
                "--details", action="store_true",
                help="Show the full prettified report (also the default).",
            )
        else:
            operation_parser.add_argument(
                "--limit", type=int, choices=range(1, 21), default=20, metavar="N",
                help="Refresh at most N queued changed sessions (1 to 20; default 20).",
            )
    sessions_resolve = sessions_commands.add_parser(
        "resolve", help="Record an explicitly requested check-in disposition."
    )
    sessions_resolve.add_argument("--payload", choices=("-",), required=True)
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
    digest = report["private_sessions"]
    print(
        f"Private sessions: {digest['pending_count']} pending check(s), "
        f"last refresh {digest['refreshed_at'] or 'never'}"
    )
    print("Latest Daily Notes: " + ", ".join(report["latest_daily_notes"]))


@contextmanager
def _review_progress(*, interval: float = 5.0, plain: bool = False):
    """Keep slow discovery/inference visible without polluting report stdout."""
    stopped = threading.Event()
    started = time.monotonic()
    stream = sys.stderr
    def update():
        while not stopped.wait(interval):
            elapsed = int(time.monotonic() - started)
            prefix = '' if plain else '⏳ '
            separator = ' - ' if plain else ' · '
            try:
                print(f'{prefix}Reviewing work sessions{separator}{elapsed}s elapsed', file=stream, flush=True)
            except (OSError, ValueError):
                return  # A closed diagnostic stream must not leak a thread traceback.
    worker = threading.Thread(target=update, daemon=True)
    worker.start()
    try:
        yield
    finally:
        stopped.set()
        worker.join()


def _write_review(output: str, *, plain: bool, no_pager: bool) -> bool:
    """Return True only when the interactive viewer explicitly requests refresh."""
    if not plain and not no_pager and sys.stdout.isatty() and sys.stdin.isatty():
        less = shutil.which('less')
        bat = shutil.which('bat') or shutil.which('batcat')
        if less:
            try:
                with tempfile.TemporaryDirectory(prefix='second-brain-review-pager-') as directory:
                    root = Path(directory)
                    keymap = root / 'keys'
                    status_file = root / 'status'
                    keymap.write_text('#command\nr quit R\nq quit\n')
                    pager = [less, '-R', '-+F', '--lesskey-src=' + str(keymap),
                             '-P r refresh recaps | Space scroll | / search | q quit']
                    argv = pager
                    if bat:
                        # bat discards less's exit status. A private wrapper records
                        # the refresh request; no report content enters control files.
                        wrapper = root / 'pager.py'
                        wrapper.write_text(
                            'import pathlib, subprocess, sys\n'
                            'try:\n'
                            '    code = subprocess.run(sys.argv[2:], check=False).returncode\n'
                            'except OSError:\n'
                            '    code = 1\n'
                            'pathlib.Path(sys.argv[1]).write_text(str(code))\n'
                            'raise SystemExit(0 if code == 82 else code)\n'
                        )
                        argv = [bat, '--style=plain', '--language=txt', '--paging=always',
                                '--color=never' if 'NO_COLOR' in os.environ else '--color=always',
                                '--pager', shlex.join([sys.executable, str(wrapper), str(status_file), *pager])]
                    result = subprocess.run(argv, input=output, text=True, check=False)
                    code = int(status_file.read_text()) if status_file.exists() else result.returncode
                    if code == 82:
                        return True
                    if code in (0, 141, -13, 130, -2):
                        return False
            except (BrokenPipeError, KeyboardInterrupt):
                return False  # q/interrupt must not redisplay or regenerate the report.
            except OSError:
                pass  # Missing/broken viewer still leaves the recap readable.
    sys.stdout.write(output)
    return False


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "sessions":
            if args.sessions_command == "resolve":
                _print_json(sessions.resolve(load_payload(args.payload)))
            else:
                operation = (
                    sessions.refresh if args.sessions_command == "refresh"
                    else sessions.review
                )
                if args.sessions_command == "refresh":
                    report = operation() if args.limit == 20 else operation(limit=args.limit)
                else:
                    options = {}
                    if args.limit is not None:
                        options["limit"] = args.limit
                    if args.refresh_limit is not None:
                        options["refresh_limit"] = args.refresh_limit
                    if args.all_sessions:
                        options["all_sessions"] = True
                    while True:
                        with _review_progress(plain=args.plain):
                            report = operation(**options)
                        if args.format == "json":
                            _print_json(report)
                            break
                        output = sessions.render_terminal(report, plain=args.plain)
                        if not _write_review(output, plain=args.plain, no_pager=args.no_pager):
                            break
                        # r is an explicit request to fill missing recaps even if
                        # the first snapshot used the zero-inference preview flag.
                        if options.get("refresh_limit") == 0:
                            options.pop("refresh_limit")
                    return 1 if report.get("error") else 0
                if args.sessions_command == "refresh":
                    # Timer stdout may enter the journal; review content stays opt-in.
                    report = {
                        key: report[key] for key in (
                            "schema_version", "refreshed_at", "summary_updated_at", "pending_count",
                            "backlog_count", "model_calls", "coverage", "error",
                        ) if key in report
                    }
                if args.format == "json":
                    _print_json(report)
                elif args.sessions_command == "refresh":
                    print(
                        f"Private session refresh: {report.get('refreshed_at') or 'never'}; "
                        f"{report.get('pending_count', 0)} open checks; "
                        f"{report.get('backlog_count', 0)} queued; "
                        f"{report.get('model_calls', 0)} model calls"
                    )
                    print("Coverage: " + ", ".join(
                        f"{key}={count}" for key, count in report.get("coverage", {}).items()
                    ))
                    if report.get("error"):
                        print("Refresh issue: " + report["error"])
                return 1 if report.get("error") else 0
            return 0
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
