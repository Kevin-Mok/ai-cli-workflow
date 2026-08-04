#!/usr/bin/env python3

import fcntl
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "executable_second-brain"
PACKAGE = REPO_ROOT / "scripts" / "second_brain"
SOURCE_VAULT = REPO_ROOT / "second-brain"


class SecondBrainCommandTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        (self.repo / ".git").mkdir()
        if SOURCE_VAULT.is_dir():
            shutil.copytree(SOURCE_VAULT, self.repo / "second-brain")
        fixture_scripts = self.repo / "scripts"
        fixture_scripts.mkdir()
        self.script = fixture_scripts / "executable_second-brain"
        shutil.copy2(SCRIPT, self.script)
        shutil.copytree(
            PACKAGE,
            fixture_scripts / "second_brain",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        self.home = self.root / "home"
        self.home.mkdir()
        self.state_home = self.root / "state"
        self.ignored_state_home = self.root / "ignored-state-override"
        self.outside = self.root / "outside"
        self.outside.mkdir()
        self.env = {
            **os.environ,
            "HOME": str(self.home),
            "XDG_STATE_HOME": str(self.state_home),
            "SECOND_BRAIN_STATE_HOME": str(self.ignored_state_home),
            "SECOND_BRAIN_NOW": "2026-07-14T09:30:00-04:00",
            "PYTHONDONTWRITEBYTECODE": "1",
        }

    def run_command(
        self,
        *arguments: str,
        payload: dict[str, object] | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(self.script), *arguments],
            cwd=self.outside,
            env=self.env if env is None else env,
            input=None if payload is None else json.dumps(payload),
            text=True,
            capture_output=True,
            check=False,
        )

    def vault_snapshot(self) -> dict[str, bytes]:
        vault = self.repo / "second-brain"
        snapshot: dict[str, bytes] = {}
        for path in vault.rglob("*"):
            if path.is_symlink():
                raise AssertionError(f"fixture vault contains a symlink: {path}")
            if path.is_file():
                snapshot[path.relative_to(vault).as_posix()] = path.read_bytes()
        return snapshot

    def common_payload(self, event_id: str) -> dict[str, object]:
        return {
            "schema_version": 1,
            "event_id": event_id,
            "source": "codex",
            "timestamp": "2026-07-14T09:30:00-04:00",
        }

    def focus_payload(
        self,
        event_id: str = "focus-001",
        outcome: str = "Validate 20 Grade 8 contest questions.",
    ) -> dict[str, object]:
        return {
            **self.common_payload(event_id),
            "date": "2026-07-14",
            "project": "ExampleProject",
            "outcome": outcome,
            "done_when": "20 of 20 question validations are complete.",
            "evidence": "https://example.invalid/example-project-evidence",
            "confirmed": True,
        }

    def deferred_payload(
        self,
        event_id: str = "deferred-001",
        *,
        target_date: str | None = "2026-07-14",
        text: str = "Review the deferred private reminder.",
    ) -> dict[str, object]:
        return {
            **self.common_payload(event_id),
            "target_date": target_date,
            "session_id": "session-deferred-001",
            "text": text,
        }

    def resolution_payload(self, event_id: str, resolution: str) -> dict[str, object]:
        return {**self.common_payload(event_id), "resolution": resolution}

    def schedule_payload(self, event_id: str, target_date: str) -> dict[str, object]:
        return {
            **self.common_payload(event_id),
            "target_date": target_date,
        }

    def test_help_exposes_task_one_commands(self) -> None:
        completed = self.run_command("--help")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        for command in (
            "status", "capture", "focus", "closeout", "defer",
            "schedule-deferred", "process-deferred", "list-deferred",
            "resolve-deferred",
        ):
            self.assertIn(command, completed.stdout)

    def test_defer_without_a_date_creates_a_private_someday_reminder(self) -> None:
        payload = self.deferred_payload(
            "someday-001",
            target_date=None,
            text="Document the low-priority ExampleProject smoke tests.",
        )
        vault_before = self.vault_snapshot()
        created = self.run_command("defer", "--payload", "-", payload=payload)
        self.assertEqual(created.returncode, 0, created.stderr)
        self.assertEqual(json.loads(created.stdout)["result"], "created")
        self.assertEqual(self.vault_snapshot(), vault_before)

        private_file = (
            self.state_home / "second-brain" / "deferred" / "reminders.json"
        )
        record = json.loads(private_file.read_text(encoding="utf-8"))["reminders"][0]
        self.assertEqual(record["state"], "someday")
        self.assertIsNone(record["target_date"])

        status = self.run_command("status", "--format", "json")
        self.assertEqual(status.returncode, 0, status.stderr)
        self.assertEqual(
            json.loads(status.stdout)["private_reminders"],
            {"someday": 1, "deferred": 0, "inbox": 0},
        )
        self.assertNotIn("Document the low-priority", status.stdout)

        listed = self.run_command(
            "list-deferred", "--state", "someday", "--format", "json"
        )
        self.assertEqual(listed.returncode, 0, listed.stderr)
        self.assertEqual(
            json.loads(listed.stdout)["reminders"][0]["event_id"], "someday-001"
        )

    def test_someday_reminder_requires_a_future_date_to_schedule(self) -> None:
        created = self.run_command(
            "defer",
            "--payload",
            "-",
            payload=self.deferred_payload("someday-schedule", target_date=None),
        )
        self.assertEqual(created.returncode, 0, created.stderr)

        scheduled = self.run_command(
            "schedule-deferred",
            "--payload",
            "-",
            payload=self.schedule_payload("someday-schedule", "2026-07-15"),
        )
        self.assertEqual(scheduled.returncode, 0, scheduled.stderr)
        self.assertEqual(json.loads(scheduled.stdout)["result"], "updated")

        repeated = self.run_command(
            "schedule-deferred",
            "--payload",
            "-",
            payload=self.schedule_payload("someday-schedule", "2026-07-15"),
        )
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(json.loads(repeated.stdout)["result"], "noop")

    def test_deferred_private_lifecycle_is_redacted_idempotent_and_vault_safe(self) -> None:
        payload = self.deferred_payload(
            "deferred-secret",
            target_date="2026-07-13",
            text="Remember token sk-abcdefghijklmnopqrstuv",
        )
        vault_before = self.vault_snapshot()
        created = self.run_command("defer", "--payload", "-", payload=payload)
        self.assertEqual(created.returncode, 0, created.stderr)
        self.assertEqual(json.loads(created.stdout)["result"], "created")
        self.assertEqual(self.vault_snapshot(), vault_before)

        private_file = (
            self.state_home / "second-brain" / "deferred" / "reminders.json"
        )
        stored = private_file.read_text(encoding="utf-8")
        self.assertIn("[REDACTED]", stored)
        self.assertNotIn("sk-abcdefghijklmnopqrstuv", stored)
        self.assertEqual(stat.S_IMODE(private_file.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(private_file.parent.stat().st_mode), 0o700)

        private_before = private_file.read_bytes()
        vault_before = self.vault_snapshot()
        repeated = self.run_command("defer", "--payload", "-", payload=payload)
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(json.loads(repeated.stdout)["result"], "noop")
        self.assertEqual(private_file.read_bytes(), private_before)
        self.assertEqual(self.vault_snapshot(), vault_before)

        vault_before = self.vault_snapshot()
        conflicting = self.run_command(
            "defer",
            "--payload",
            "-",
            payload={**payload, "text": "PRIVATE_CHANGED_REMINDER"},
        )
        self.assertEqual(conflicting.returncode, 2)
        self.assertIn("conflict", conflicting.stderr.lower())
        self.assertNotIn("PRIVATE_CHANGED_REMINDER", conflicting.stderr)
        self.assertEqual(private_file.read_bytes(), private_before)
        self.assertEqual(self.vault_snapshot(), vault_before)

        vault_before = self.vault_snapshot()
        processed = self.run_command("process-deferred")
        self.assertEqual(processed.returncode, 0, processed.stderr)
        self.assertEqual(json.loads(processed.stdout)["promoted"], 1)
        self.assertEqual(self.vault_snapshot(), vault_before)

        vault_before = self.vault_snapshot()
        listed = self.run_command("list-deferred", "--format", "json")
        self.assertEqual(listed.returncode, 0, listed.stderr)
        self.assertEqual(
            json.loads(listed.stdout)["reminders"][0]["event_id"], "deferred-secret"
        )
        self.assertEqual(self.vault_snapshot(), vault_before)

        vault_before = self.vault_snapshot()
        resolved = self.run_command(
            "resolve-deferred",
            "--payload",
            "-",
            payload=self.resolution_payload("deferred-secret", "focused"),
        )
        self.assertEqual(resolved.returncode, 0, resolved.stderr)
        self.assertEqual(json.loads(resolved.stdout)["result"], "updated")
        record = json.loads(private_file.read_text(encoding="utf-8"))["reminders"][0]
        self.assertEqual(record["state"], "resolved")
        self.assertEqual(record["resolution"], "focused")
        self.assertNotIn("text", record)
        self.assertEqual(self.vault_snapshot(), vault_before)

        vault_before = self.vault_snapshot()
        resolution_repeat = self.run_command(
            "resolve-deferred",
            "--payload",
            "-",
            payload=self.resolution_payload("deferred-secret", "focused"),
        )
        self.assertEqual(resolution_repeat.returncode, 0, resolution_repeat.stderr)
        self.assertEqual(json.loads(resolution_repeat.stdout)["result"], "noop")
        self.assertEqual(self.vault_snapshot(), vault_before)

    def test_deferred_rejects_invalid_dates_states_and_resolution_values(self) -> None:
        invalid_payloads = (
            self.deferred_payload("deferred-invalid-date", target_date="2026-02-30"),
            self.deferred_payload("deferred-invalid-type", target_date=123),  # type: ignore[arg-type]
            self.deferred_payload("deferred-invalid-text", text="PRIVATE_UNSAFE\x00TEXT"),
        )
        for invalid in invalid_payloads:
            with self.subTest(event_id=invalid["event_id"]):
                vault_before = self.vault_snapshot()
                result = self.run_command("defer", "--payload", "-", payload=invalid)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("PRIVATE_UNSAFE", result.stderr)
                self.assertEqual(self.vault_snapshot(), vault_before)

        payload = self.deferred_payload("deferred-pending", target_date="2026-07-15")
        vault_before = self.vault_snapshot()
        created = self.run_command("defer", "--payload", "-", payload=payload)
        self.assertEqual(created.returncode, 0, created.stderr)
        self.assertEqual(self.vault_snapshot(), vault_before)

        vault_before = self.vault_snapshot()
        wrong_state = self.run_command(
            "resolve-deferred",
            "--payload",
            "-",
            payload=self.resolution_payload("deferred-pending", "focused"),
        )
        self.assertEqual(wrong_state.returncode, 2)
        self.assertIn("inbox", wrong_state.stderr.lower())
        self.assertEqual(self.vault_snapshot(), vault_before)

        vault_before = self.vault_snapshot()
        wrong_resolution = self.run_command(
            "resolve-deferred",
            "--payload",
            "-",
            payload=self.resolution_payload("deferred-pending", "pending"),
        )
        self.assertEqual(wrong_resolution.returncode, 2)
        self.assertNotIn("pending", wrong_resolution.stderr)
        self.assertEqual(self.vault_snapshot(), vault_before)

    def test_deferred_allows_dismissed_resolution(self) -> None:
        payload = self.deferred_payload("deferred-dismissed", target_date="2026-07-13")
        vault_before = self.vault_snapshot()
        created = self.run_command("defer", "--payload", "-", payload=payload)
        self.assertEqual(created.returncode, 0, created.stderr)
        self.assertEqual(self.vault_snapshot(), vault_before)

        vault_before = self.vault_snapshot()
        promoted = self.run_command("process-deferred")
        self.assertEqual(promoted.returncode, 0, promoted.stderr)
        self.assertEqual(self.vault_snapshot(), vault_before)

        vault_before = self.vault_snapshot()
        dismissed = self.run_command(
            "resolve-deferred",
            "--payload",
            "-",
            payload=self.resolution_payload("deferred-dismissed", "dismissed"),
        )
        self.assertEqual(dismissed.returncode, 0, dismissed.stderr)
        self.assertEqual(json.loads(dismissed.stdout)["result"], "updated")
        self.assertEqual(self.vault_snapshot(), vault_before)

    def test_deferred_status_counts_and_late_promotion_remain_private(self) -> None:
        payload = self.deferred_payload(
            "deferred-late",
            target_date="2026-07-15",
            text="PRIVATE_STATUS_REMINDER",
        )
        vault_before = self.vault_snapshot()
        created = self.run_command("defer", "--payload", "-", payload=payload)
        self.assertEqual(created.returncode, 0, created.stderr)
        self.assertEqual(self.vault_snapshot(), vault_before)

        vault_before = self.vault_snapshot()
        status = self.run_command("status", "--format", "json")
        self.assertEqual(status.returncode, 0, status.stderr)
        self.assertEqual(
            json.loads(status.stdout)["private_reminders"],
            {"someday": 0, "deferred": 1, "inbox": 0},
        )
        self.assertNotIn("PRIVATE_STATUS_REMINDER", status.stdout)
        self.assertEqual(self.vault_snapshot(), vault_before)

        vault_before = self.vault_snapshot()
        late = self.run_command(
            "process-deferred",
            env={**self.env, "SECOND_BRAIN_NOW": "2026-07-16T04:00:00-04:00"},
        )
        self.assertEqual(late.returncode, 0, late.stderr)
        self.assertEqual(json.loads(late.stdout)["promoted"], 1)
        self.assertEqual(self.vault_snapshot(), vault_before)

        private_file = (
            self.state_home / "second-brain" / "deferred" / "reminders.json"
        )
        private_before = private_file.read_bytes()
        vault_before = self.vault_snapshot()
        repeat = self.run_command(
            "process-deferred",
            env={**self.env, "SECOND_BRAIN_NOW": "2026-07-16T04:00:00-04:00"},
        )
        self.assertEqual(repeat.returncode, 0, repeat.stderr)
        self.assertEqual(json.loads(repeat.stdout)["result"], "noop")
        self.assertEqual(private_file.read_bytes(), private_before)
        self.assertEqual(self.vault_snapshot(), vault_before)

        vault_before = self.vault_snapshot()
        text_status = self.run_command("status")
        self.assertEqual(text_status.returncode, 0, text_status.stderr)
        self.assertIn(
            "Private reminders: 0 someday, 0 deferred, 1 inbox", text_status.stdout
        )
        self.assertNotIn("PRIVATE_STATUS_REMINDER", text_status.stdout)
        self.assertEqual(self.vault_snapshot(), vault_before)
    def test_status_resolves_repo_independent_of_caller_cwd(self) -> None:
        completed = self.run_command("status", "--format", "json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["schema_version"], 1)
        self.assertEqual(report["date"], "2026-07-14")
        self.assertEqual(
            report["active_projects"],
            [
                "Beginner Python Teaching Sites",
                "ExampleProject",
                "Linux Config AI Workflow",
            ],
        )
        expected_daily_notes = sorted(
            (path.stem for path in (self.repo / "second-brain/05 Daily Notes").glob("????-??-??.md")),
            reverse=True,
        )[:3]
        self.assertEqual(report["latest_daily_notes"], expected_daily_notes)
        self.assertEqual(report["inbox"]["path"], "01 Inbox/Brain Dump.md")

    def test_installed_layout_mutates_chezmoi_source_not_applied_home_copy(self) -> None:
        installed_scripts = self.home / "scripts"
        installed_scripts.mkdir()
        installed_script = installed_scripts / "executable_second-brain"
        shutil.copy2(self.script, installed_script)
        shutil.copytree(
            self.repo / "scripts" / "second_brain",
            installed_scripts / "second_brain",
        )
        applied_vault = self.home / "second-brain"
        shutil.copytree(self.repo / "second-brain", applied_vault)
        fake_bin = self.root / "bin"
        fake_bin.mkdir()
        fake_chezmoi = fake_bin / "chezmoi"
        fake_chezmoi.write_text(
            "#!/bin/sh\n"
            "if [ \"$#\" -ne 2 ] || [ \"${1:-}\" != source-path ] || "
            "[ \"${2:-}\" != \"$HOME/second-brain/README.md\" ]; then\n"
            "  exit 64\n"
            "fi\n"
            f"printf '%s\\n' '{self.repo / 'second-brain' / 'README.md'}'\n",
            encoding="utf-8",
        )
        fake_chezmoi.chmod(0o755)
        env = {
            **self.env,
            "PATH": f"{fake_bin}{os.pathsep}{self.env['PATH']}",
        }
        source_decisions = (
            self.repo / "second-brain" / "00 Context" / "Decisions.md"
        )
        applied_decisions = applied_vault / "00 Context" / "Decisions.md"
        before = (source_decisions.read_bytes(), applied_decisions.read_bytes())
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(installed_script),
                "capture",
                "--kind",
                "personal-decision",
                "--payload",
                "-",
            ],
            cwd=self.outside,
            env=env,
            input=json.dumps(
                {
                    **self.common_payload("decision-installed-001"),
                    "title": "Use the tracked source",
                    "summary": "Installed commands update the chezmoi source repository.",
                    "target": "00 Context/Decisions.md",
                    "links": [],
                    "visibility": "public-sanitized",
                    "confirmed": True,
                }
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotEqual(source_decisions.read_bytes(), before[0])
        self.assertEqual(applied_decisions.read_bytes(), before[1])

    def test_raw_capture_is_private_redacted_and_idempotent(self) -> None:
        payload = {
            **self.common_payload("raw-001"),
            "session_id": "session-001",
            "role": "user",
            "text": "Keep this discussion. token sk-abcdefghijklmnopqrstuv",
        }
        payload_path = self.root / "raw-payload.json"
        payload_path.write_text(json.dumps(payload), encoding="utf-8")
        vault_before = self.vault_snapshot()
        first = self.run_command(
            "capture", "--kind", "raw-session", "--payload", str(payload_path)
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads(first.stdout)["result"], "created")

        raw_file = self.state_home / "second-brain" / "raw" / "2026-07-14.jsonl"
        self.assertTrue(raw_file.is_file())
        raw_text = raw_file.read_text(encoding="utf-8")
        self.assertIn("[REDACTED]", raw_text)
        self.assertNotIn("sk-abcdefghijklmnopqrstuv", raw_text)
        self.assertEqual(stat.S_IMODE(raw_file.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(raw_file.parent.stat().st_mode), 0o700)
        self.assertFalse(self.ignored_state_home.exists())
        self.assertEqual(self.vault_snapshot(), vault_before)

        before = raw_file.read_bytes()
        repeated = self.run_command(
            "capture", "--kind", "raw-session", "--payload", str(payload_path)
        )
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(json.loads(repeated.stdout)["result"], "noop")
        self.assertEqual(raw_file.read_bytes(), before)

    def test_raw_capture_redacts_complete_common_secret_shapes(self) -> None:
        payload = {
            **self.common_payload("raw-secrets-001"),
            "session_id": "session-secrets-001",
            "role": "user",
            "text": (
                "Authorization: Bearer bearer-value-that-must-disappear\n"
                "github_token=ghp_abcdefghijklmnopqrstuvwxyz1234567890\n"
                "<private-key-removed>"
            ),
        }
        result = self.run_command(
            "capture",
            "--kind",
            "raw-session",
            "--payload",
            "-",
            payload=payload,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        raw_file = self.state_home / "second-brain" / "raw" / "2026-07-14.jsonl"
        raw_text = raw_file.read_text(encoding="utf-8")
        self.assertIn("[REDACTED]", raw_text)
        for secret_fragment in (
            "bearer-value-that-must-disappear",
            "ghp_abcdefghijklmnopqrstuvwxyz1234567890",
            "PEM_BODY_MUST_DISAPPEAR",
            "BEGIN PRIVATE KEY",
            "END PRIVATE KEY",
        ):
            self.assertNotIn(secret_fragment, raw_text)

    def test_state_root_rejects_relative_and_symlinked_xdg_paths(self) -> None:
        payload = {
            **self.common_payload("raw-state-001"),
            "session_id": "session-state-001",
            "role": "user",
            "text": "private state boundary",
        }
        relative_env = {**self.env, "XDG_STATE_HOME": "relative-state"}
        relative = self.run_command(
            "capture",
            "--kind",
            "raw-session",
            "--payload",
            "-",
            payload=payload,
            env=relative_env,
        )
        self.assertEqual(relative.returncode, 2)
        self.assertNotIn("Traceback", relative.stderr)
        self.assertFalse((self.outside / "relative-state").exists())

        overlapping_state = self.repo / "private-state"
        overlap_env = {**self.env, "XDG_STATE_HOME": str(overlapping_state)}
        overlapping = self.run_command(
            "capture",
            "--kind",
            "raw-session",
            "--payload",
            "-",
            payload={**payload, "event_id": "raw-state-overlap-001"},
            env=overlap_env,
        )
        self.assertEqual(overlapping.returncode, 2)
        self.assertNotIn("Traceback", overlapping.stderr)
        self.assertFalse(overlapping_state.exists())

        outside_state = self.root / "outside-state"
        outside_state.mkdir()
        self.state_home.symlink_to(outside_state, target_is_directory=True)
        symlinked = self.run_command(
            "capture",
            "--kind",
            "raw-session",
            "--payload",
            "-",
            payload={**payload, "event_id": "raw-state-002"},
        )
        self.assertEqual(symlinked.returncode, 2)
        self.assertNotIn("Traceback", symlinked.stderr)
        self.assertEqual(list(outside_state.iterdir()), [])

    def test_lock_file_symlink_is_rejected_without_touching_target(self) -> None:
        lock_dir = self.state_home / "second-brain" / "locks"
        lock_dir.mkdir(parents=True, mode=0o700)
        outside_lock = self.root / "outside-lock"
        outside_lock.write_text("DO_NOT_TOUCH", encoding="utf-8")
        (lock_dir / "mutation.lock").symlink_to(outside_lock)
        payload = {
            **self.common_payload("raw-lock-001"),
            "session_id": "session-lock-001",
            "role": "user",
            "text": "private lock boundary",
        }
        result = self.run_command(
            "capture",
            "--kind",
            "raw-session",
            "--payload",
            "-",
            payload=payload,
        )
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(outside_lock.read_text(encoding="utf-8"), "DO_NOT_TOUCH")
        self.assertFalse((self.state_home / "second-brain" / "raw").exists())

    def test_capture_rejects_lock_contention_then_succeeds_after_release(self) -> None:
        lock_dir = self.state_home / "second-brain" / "locks"
        lock_dir.mkdir(parents=True, mode=0o700)
        lock_path = lock_dir / "mutation.lock"
        lock_path.touch(mode=0o600)
        payload = {
            **self.common_payload("decision-lock-contention-001"),
            "title": "Retry after lock contention",
            "summary": "A released mutation lock permits the same safe capture.",
            "target": "00 Context/Decisions.md",
            "links": [],
            "visibility": "public-sanitized",
            "confirmed": True,
        }
        before = self.vault_snapshot()

        with lock_path.open("a+", encoding="utf-8") as lock_stream:
            fcntl.flock(lock_stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            blocked = self.run_command(
                "capture",
                "--kind",
                "personal-decision",
                "--payload",
                "-",
                payload=payload,
            )

        self.assertEqual(blocked.returncode, 2)
        self.assertEqual(blocked.stdout, "")
        self.assertIn("already running", blocked.stderr)
        self.assertNotIn("Traceback", blocked.stderr)
        self.assertEqual(self.vault_snapshot(), before)

        retried = self.run_command(
            "capture",
            "--kind",
            "personal-decision",
            "--payload",
            "-",
            payload=payload,
        )
        self.assertEqual(retried.returncode, 0, retried.stderr)
        self.assertEqual(json.loads(retried.stdout)["result"], "updated")
        decisions = self.repo / "second-brain" / "00 Context" / "Decisions.md"
        self.assertIn(
            "<!-- second-brain:event:decision-lock-contention-001 -->",
            decisions.read_text(encoding="utf-8"),
        )

    def test_confirmed_personal_decision_updates_only_authorized_note(self) -> None:
        payload = {
            **self.common_payload("decision-001"),
            "title": "Keep interests separate from projects",
            "summary": "Ask before promoting an interest into a project or task.",
            "target": "00 Context/Decisions.md",
            "links": [],
            "visibility": "public-sanitized",
            "confirmed": True,
        }
        before = self.vault_snapshot()
        result = self.run_command(
            "capture",
            "--kind",
            "personal-decision",
            "--payload",
            "-",
            payload=payload,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["result"], "updated")

        decision_path = self.repo / "second-brain" / "00 Context" / "Decisions.md"
        content = decision_path.read_text(encoding="utf-8")
        self.assertIn("<!-- second-brain:event:decision-001 -->", content)
        self.assertIn("Keep interests separate from projects", content)
        self.assertIn("Ask before promoting", content)
        self.assertTrue(content.startswith("---\n"))
        after = self.vault_snapshot()
        changed = {path for path in before if before[path] != after[path]}
        self.assertEqual(changed, {"00 Context/Decisions.md"})

        before = decision_path.read_bytes()
        repeated = self.run_command(
            "capture",
            "--kind",
            "personal-decision",
            "--payload",
            "-",
            payload=payload,
        )
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(json.loads(repeated.stdout)["result"], "noop")
        self.assertEqual(decision_path.read_bytes(), before)

    def test_unconfirmed_or_invalid_tracked_capture_fails_without_payload_leak(self) -> None:
        payload = {
            **self.common_payload("decision-002"),
            "title": "PRIVATE_SHOULD_NOT_APPEAR",
            "summary": "PRIVATE_SHOULD_NOT_APPEAR",
            "target": "00 Context/Decisions.md",
            "links": [],
            "visibility": "private",
            "confirmed": False,
        }
        before = self.vault_snapshot()
        result = self.run_command(
            "capture",
            "--kind",
            "personal-decision",
            "--payload",
            "-",
            payload=payload,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("confirmation", result.stderr.lower())
        self.assertNotIn("PRIVATE_SHOULD_NOT_APPEAR", result.stderr)
        self.assertFalse((self.root / "outside.md").exists())
        self.assertEqual(self.vault_snapshot(), before)

    def test_missing_capture_target_has_content_safe_error(self) -> None:
        target = self.repo / "second-brain" / "00 Context" / "Decisions.md"
        target.unlink()
        payload = {
            **self.common_payload("decision-missing-001"),
            "title": "PRIVATE_TITLE_MUST_NOT_LEAK",
            "summary": "PRIVATE_SUMMARY_MUST_NOT_LEAK",
            "target": "00 Context/Decisions.md",
            "links": [],
            "visibility": "public-sanitized",
            "confirmed": True,
        }
        result = self.run_command(
            "capture",
            "--kind",
            "personal-decision",
            "--payload",
            "-",
            payload=payload,
        )
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn(str(self.root), result.stderr)
        self.assertNotIn("PRIVATE_TITLE_MUST_NOT_LEAK", result.stderr)
        self.assertNotIn("PRIVATE_SUMMARY_MUST_NOT_LEAK", result.stderr)
        self.assertIn("target", result.stderr.lower())

    def test_tracked_capture_rejects_symlinked_vault_root(self) -> None:
        vault = self.repo / "second-brain"
        outside_vault = self.root / "outside-vault"
        vault.rename(outside_vault)
        vault.symlink_to(outside_vault, target_is_directory=True)
        decisions = outside_vault / "00 Context" / "Decisions.md"
        before = decisions.read_bytes()
        payload = {
            **self.common_payload("decision-vault-link-001"),
            "title": "Do not follow vault links",
            "summary": "Tracked writes stay inside a real source vault.",
            "target": "00 Context/Decisions.md",
            "links": [],
            "visibility": "public-sanitized",
            "confirmed": True,
        }
        result = self.run_command(
            "capture",
            "--kind",
            "personal-decision",
            "--payload",
            "-",
            payload=payload,
        )
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn(str(self.root), result.stderr)
        self.assertEqual(decisions.read_bytes(), before)

    def test_focus_persists_exactly_one_confirmed_example-project_outcome(self) -> None:
        daily_path = self.repo / "second-brain" / "05 Daily Notes" / "2026-07-14.md"
        original = daily_path.read_bytes()
        unconfirmed_payload = {**self.focus_payload(), "confirmed": False}
        unconfirmed = self.run_command(
            "focus", "--payload", "-", payload=unconfirmed_payload
        )
        self.assertEqual(unconfirmed.returncode, 2)
        self.assertEqual(daily_path.read_bytes(), original)

        first = self.run_command(
            "focus", "--payload", "-", payload=self.focus_payload()
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads(first.stdout)["result"], "updated")
        content = daily_path.read_text(encoding="utf-8")
        focus_section = content.split("## Focus", 1)[1].split("## Done", 1)[0]
        for required in (
            "Validate 20 Grade 8 contest questions.",
            "20 of 20 question validations are complete.",
            "https://example.invalid/example-project-evidence",
        ):
            self.assertIn(required, focus_section)

        before_repeat = daily_path.read_bytes()
        repeated = self.run_command(
            "focus", "--payload", "-", payload=self.focus_payload()
        )
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(json.loads(repeated.stdout)["result"], "noop")
        self.assertEqual(daily_path.read_bytes(), before_repeat)

        second = self.run_command(
            "focus",
            "--payload",
            "-",
            payload=self.focus_payload(
                event_id="focus-002",
                outcome="Publish a different daily result.",
            ),
        )
        self.assertEqual(second.returncode, 2)
        self.assertIn("already", second.stderr.lower())
        self.assertEqual(daily_path.read_bytes(), before_repeat)

    def test_focus_and_closeout_reject_likely_secrets_before_writes(self) -> None:
        daily_path = self.repo / "second-brain" / "05 Daily Notes" / "2026-07-14.md"
        original = daily_path.read_bytes()
        unsafe_focus = self.run_command(
            "focus",
            "--payload",
            "-",
            payload=self.focus_payload(
                outcome="Validate questions with sk-abcdefghijklmnopqrstuvwxyz123456."
            ),
        )
        self.assertEqual(unsafe_focus.returncode, 2)
        self.assertNotIn("sk-abcdefghijklmnopqrstuvwxyz123456", unsafe_focus.stderr)
        self.assertEqual(daily_path.read_bytes(), original)

        focused = self.run_command(
            "focus", "--payload", "-", payload=self.focus_payload()
        )
        self.assertEqual(focused.returncode, 0, focused.stderr)
        before_closeout = self.vault_snapshot()
        unsafe_closeout = self.run_command(
            "closeout",
            "--payload",
            "-",
            payload={
                **self.common_payload("closeout-secret-001"),
                "date": "2026-07-14",
                "project": "ExampleProject",
                "planned": "Validate 20 Grade 8 contest questions.",
                "completed": "17 validated.",
                "evidence": "token=PRIVATE_CLOSEOUT_TOKEN",
                "blocker": "Three remain.",
                "decisions": [],
                "open": [],
                "next": "Finish three.",
                "confirmed": True,
            },
        )
        self.assertEqual(unsafe_closeout.returncode, 2)
        self.assertNotIn("PRIVATE_CLOSEOUT_TOKEN", unsafe_closeout.stderr)
        self.assertEqual(self.vault_snapshot(), before_closeout)

    def test_closeout_requires_matching_confirmed_example-project_focus(self) -> None:
        focused = self.run_command(
            "focus", "--payload", "-", payload=self.focus_payload()
        )
        self.assertEqual(focused.returncode, 0, focused.stderr)
        base_payload = {
            **self.common_payload("closeout-focus-guard-001"),
            "date": "2026-07-14",
            "project": "ExampleProject",
            "planned": "Validate 20 Grade 8 contest questions.",
            "completed": "17 validated and published.",
            "evidence": "https://example.invalid/example-project-evidence",
            "blocker": "Three questions remain.",
            "decisions": [],
            "open": [],
            "next": "Finish the remaining three questions.",
            "confirmed": True,
        }
        before = self.vault_snapshot()
        wrong_project = self.run_command(
            "closeout",
            "--payload",
            "-",
            payload={**base_payload, "project": "Linux Config AI Workflow"},
        )
        self.assertEqual(wrong_project.returncode, 2)
        self.assertEqual(self.vault_snapshot(), before)

        wrong_plan = self.run_command(
            "closeout",
            "--payload",
            "-",
            payload={
                **base_payload,
                "event_id": "closeout-focus-guard-002",
                "planned": "A different unconfirmed outcome.",
            },
        )
        self.assertEqual(wrong_plan.returncode, 2)
        self.assertEqual(self.vault_snapshot(), before)

    def test_closeout_writes_boss_readable_daily_and_project_progress_once(self) -> None:
        planned = "Validate 20 Grade 8 contest questions."
        focused = self.run_command(
            "focus",
            "--payload",
            "-",
            payload=self.focus_payload(outcome=planned),
        )
        self.assertEqual(focused.returncode, 0, focused.stderr)
        payload = {
            **self.common_payload("closeout-001"),
            "date": "2026-07-14",
            "project": "ExampleProject",
            "planned": planned,
            "completed": "17 validated and published.",
            "evidence": "https://example.invalid/example-project-evidence",
            "blocker": "Three questions require source verification.",
            "decisions": ["Use approved sources for contest questions."],
            "open": ["Verify three remaining sources."],
            "next": "Finish the remaining three questions.",
            "confirmed": True,
        }
        before_snapshot = self.vault_snapshot()
        first = self.run_command("closeout", "--payload", "-", payload=payload)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads(first.stdout)["result"], "updated")

        daily_path = self.repo / "second-brain" / "05 Daily Notes" / "2026-07-14.md"
        project_path = self.repo / "second-brain" / "02 Projects" / "ExampleProject.md"
        daily = daily_path.read_text(encoding="utf-8")
        project = project_path.read_text(encoding="utf-8")
        for required in (
            "**Planned:** Validate 20 Grade 8 contest questions.",
            "**Completed:** 17 validated and published.",
            "**Evidence:** https://example.invalid/example-project-evidence",
            "**Blocker:** Three questions require source verification.",
            "<!-- second-brain:event:closeout-001 -->",
        ):
            self.assertIn(required, daily)
        self.assertIn("17 validated and published.", project)
        self.assertIn("## Progress", project)
        self.assertIn("Use approved sources for contest questions.", daily)
        self.assertIn("Verify three remaining sources.", daily)
        self.assertIn("Finish the remaining three questions.", daily)
        open_section = daily.split("## Open", 1)[1].split("## Next", 1)[0]
        self.assertIn("Three questions require source verification.", open_section)
        after_snapshot = self.vault_snapshot()
        changed = {
            path
            for path in before_snapshot
            if before_snapshot[path] != after_snapshot[path]
        }
        self.assertEqual(
            changed,
            {
                "02 Projects/ExampleProject.md",
                "05 Daily Notes/2026-07-14.md",
            },
        )

        before = (daily_path.read_bytes(), project_path.read_bytes())
        repeated = self.run_command("closeout", "--payload", "-", payload=payload)
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(json.loads(repeated.stdout)["result"], "noop")
        self.assertEqual(
            (daily_path.read_bytes(), project_path.read_bytes()),
            before,
        )

    def test_unconfirmed_closeout_is_rejected_without_write_or_leak(self) -> None:
        payload = {
            **self.common_payload("closeout-002"),
            "date": "2026-07-14",
            "project": "ExampleProject",
            "planned": "PRIVATE_CLOSEOUT_TEXT",
            "completed": "Nothing recorded.",
            "evidence": "private-evidence",
            "blocker": "",
            "decisions": [],
            "open": [],
            "next": "Wait.",
            "confirmed": False,
        }
        before = self.vault_snapshot()
        result = self.run_command("closeout", "--payload", "-", payload=payload)
        self.assertEqual(result.returncode, 2)
        self.assertIn("confirmation", result.stderr.lower())
        self.assertNotIn("PRIVATE_CLOSEOUT_TEXT", result.stderr)
        self.assertEqual(self.vault_snapshot(), before)

    def test_closeout_rejects_symlinked_project_directory(self) -> None:
        projects = self.repo / "second-brain" / "02 Projects"
        example-project = projects / "ExampleProject.md"
        outside_projects = self.root / "outside-projects"
        outside_projects.mkdir()
        outside_example-project = outside_projects / "ExampleProject.md"
        outside_example-project.write_bytes(example-project.read_bytes())
        shutil.rmtree(projects)
        projects.symlink_to(outside_projects, target_is_directory=True)
        daily = self.repo / "second-brain" / "05 Daily Notes" / "2026-07-14.md"
        before = (daily.read_bytes(), outside_example-project.read_bytes())
        payload = {
            **self.common_payload("closeout-symlink-001"),
            "date": "2026-07-14",
            "project": "ExampleProject",
            "planned": "PRIVATE_PLAN_MUST_NOT_LEAK",
            "completed": "One safe result.",
            "evidence": "https://example.invalid/evidence",
            "blocker": "",
            "decisions": [],
            "open": [],
            "next": "Continue safely.",
            "confirmed": True,
        }
        result = self.run_command("closeout", "--payload", "-", payload=payload)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn(str(self.root), result.stderr)
        self.assertNotIn("PRIVATE_PLAN_MUST_NOT_LEAK", result.stderr)
        self.assertEqual((daily.read_bytes(), outside_example-project.read_bytes()), before)

    def test_payload_path_and_schema_errors_are_actionable_and_safe(self) -> None:
        invalid = self.run_command(
            "capture",
            "--kind",
            "raw-session",
            "--payload",
            "-",
            payload={
                **self.common_payload("raw-schema-001"),
                "schema_version": 99,
                "session_id": "session-schema-001",
                "role": "user",
                "text": "DO_NOT_ECHO",
            },
        )
        self.assertEqual(invalid.returncode, 2)
        self.assertIn("schema_version", invalid.stderr)
        self.assertNotIn("DO_NOT_ECHO", invalid.stderr)

        missing = self.run_command(
            "capture",
            "--kind",
            "raw-session",
            "--payload",
            str(self.root / "missing.json"),
        )
        self.assertEqual(missing.returncode, 2)
        self.assertIn("payload", missing.stderr.lower())

    def test_schema_version_type_and_unknown_fields_are_strict_and_safe(self) -> None:
        for index, invalid_version in enumerate((True, 1.0), start=1):
            with self.subTest(schema_version=invalid_version):
                payload = {
                    **self.common_payload(f"raw-version-{index}"),
                    "schema_version": invalid_version,
                    "session_id": f"session-version-{index}",
                    "role": "user",
                    "text": "PRIVATE_SCHEMA_TEXT",
                }
                result = self.run_command(
                    "capture",
                    "--kind",
                    "raw-session",
                    "--payload",
                    "-",
                    payload=payload,
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("schema_version", result.stderr)
                self.assertNotIn("PRIVATE_SCHEMA_TEXT", result.stderr)

        payload = {
            **self.common_payload("raw-unknown-001"),
            "session_id": "session-unknown-001",
            "role": "user",
            "text": "PRIVATE_UNKNOWN_TEXT",
            "PRIVATE_CALLER_FIELD_NAME": "PRIVATE_CALLER_FIELD_VALUE",
        }
        unknown = self.run_command(
            "capture",
            "--kind",
            "raw-session",
            "--payload",
            "-",
            payload=payload,
        )
        self.assertEqual(unknown.returncode, 2)
        self.assertIn("unsupported fields", unknown.stderr)
        self.assertNotIn("PRIVATE_CALLER_FIELD_NAME", unknown.stderr)
        self.assertNotIn("PRIVATE_CALLER_FIELD_VALUE", unknown.stderr)
        self.assertNotIn("PRIVATE_UNKNOWN_TEXT", unknown.stderr)

    def test_tracked_capture_rejects_secrets_markers_and_multiline_injection(self) -> None:
        decision_path = self.repo / "second-brain" / "00 Context" / "Decisions.md"
        before = decision_path.read_bytes()
        invalid_summaries = (
            "Credential sk-abcdefghijklmnopqrstuvwxyz123456 must stay private.",
            "Inject <!-- second-brain:event:future-event-001 --> marker.",
            "Safe first line.\n## Injected heading",
        )
        for index, summary in enumerate(invalid_summaries, start=1):
            with self.subTest(summary=summary):
                payload = {
                    **self.common_payload(f"decision-unsafe-{index}"),
                    "title": "Reject unsafe tracked content",
                    "summary": summary,
                    "target": "00 Context/Decisions.md",
                    "links": [],
                    "visibility": "public-sanitized",
                    "confirmed": True,
                }
                result = self.run_command(
                    "capture",
                    "--kind",
                    "personal-decision",
                    "--payload",
                    "-",
                    payload=payload,
                )
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("Traceback", result.stderr)
                self.assertNotIn(summary, result.stderr)
                self.assertEqual(decision_path.read_bytes(), before)

    def test_raw_capture_uses_toronto_calendar_date(self) -> None:
        payload = {
            **self.common_payload("raw-toronto-date-001"),
            "timestamp": "2026-07-15T01:30:00+00:00",
            "session_id": "session-toronto-date-001",
            "role": "user",
            "text": "Use the event instant in example-user's local timezone.",
        }
        result = self.run_command(
            "capture",
            "--kind",
            "raw-session",
            "--payload",
            "-",
            payload=payload,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            (self.state_home / "second-brain" / "raw" / "2026-07-14.jsonl").is_file()
        )
        self.assertFalse(
            (self.state_home / "second-brain" / "raw" / "2026-07-15.jsonl").exists()
        )

    def test_reused_event_id_with_changed_raw_payload_is_a_conflict(self) -> None:
        first_payload = {
            **self.common_payload("raw-conflict-001"),
            "session_id": "session-conflict-001",
            "role": "user",
            "text": "First body stays private.",
        }
        first = self.run_command(
            "capture",
            "--kind",
            "raw-session",
            "--payload",
            "-",
            payload=first_payload,
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        raw_path = self.state_home / "second-brain" / "raw" / "2026-07-14.jsonl"
        before = raw_path.read_bytes()

        changed = self.run_command(
            "capture",
            "--kind",
            "raw-session",
            "--payload",
            "-",
            payload={**first_payload, "text": "PRIVATE_CHANGED_BODY"},
        )
        self.assertEqual(changed.returncode, 2)
        self.assertEqual(changed.stdout, "")
        self.assertIn("event", changed.stderr.lower())
        self.assertIn("conflict", changed.stderr.lower())
        self.assertNotIn("PRIVATE_CHANGED_BODY", changed.stderr)
        self.assertEqual(raw_path.read_bytes(), before)

    def test_reused_event_id_with_changed_tracked_payload_is_a_conflict(self) -> None:
        payload = {
            **self.common_payload("decision-conflict-001"),
            "title": "Keep the first decision",
            "summary": "The original confirmed decision remains canonical.",
            "target": "00 Context/Decisions.md",
            "links": [],
            "visibility": "public-sanitized",
            "confirmed": True,
        }
        first = self.run_command(
            "capture",
            "--kind",
            "personal-decision",
            "--payload",
            "-",
            payload=payload,
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        target = self.repo / "second-brain" / "00 Context" / "Decisions.md"
        before = target.read_bytes()

        changed = self.run_command(
            "capture",
            "--kind",
            "personal-decision",
            "--payload",
            "-",
            payload={**payload, "summary": "PRIVATE_CHANGED_DECISION"},
        )
        self.assertEqual(changed.returncode, 2)
        self.assertEqual(changed.stdout, "")
        self.assertIn("event", changed.stderr.lower())
        self.assertIn("conflict", changed.stderr.lower())
        self.assertNotIn("PRIVATE_CHANGED_DECISION", changed.stderr)
        self.assertEqual(target.read_bytes(), before)

    def test_status_rejects_symlinked_required_note_without_reading_target(self) -> None:
        inbox = self.repo / "second-brain" / "01 Inbox" / "Brain Dump.md"
        outside = self.root / "outside-inbox.md"
        outside.write_text("- PRIVATE_STATUS_SENTINEL\n", encoding="utf-8")
        inbox.unlink()
        inbox.symlink_to(outside)
        before = outside.read_bytes()

        result = self.run_command("status", "--format", "json")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("PRIVATE_STATUS_SENTINEL", result.stderr)
        self.assertNotIn(str(self.root), result.stderr)
        self.assertEqual(outside.read_bytes(), before)

    def test_capture_rejects_malformed_protected_note(self) -> None:
        decisions = self.repo / "second-brain" / "00 Context" / "Decisions.md"
        malformed = decisions.read_text(encoding="utf-8").replace(
            "## Entries\n", "## Renamed Entries\n", 1
        )
        decisions.write_text(malformed, encoding="utf-8")
        before = decisions.read_bytes()
        payload = {
            **self.common_payload("decision-malformed-001"),
            "title": "PRIVATE_MALFORMED_TITLE",
            "summary": "PRIVATE_MALFORMED_SUMMARY",
            "target": "00 Context/Decisions.md",
            "links": [],
            "visibility": "public-sanitized",
            "confirmed": True,
        }

        result = self.run_command(
            "capture",
            "--kind",
            "personal-decision",
            "--payload",
            "-",
            payload=payload,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("structure", result.stderr.lower())
        self.assertNotIn("PRIVATE_MALFORMED", result.stderr)
        self.assertEqual(decisions.read_bytes(), before)

    def test_closeout_rolls_back_when_the_second_file_write_fails(self) -> None:
        focused = self.run_command(
            "focus", "--payload", "-", payload=self.focus_payload()
        )
        self.assertEqual(focused.returncode, 0, focused.stderr)
        daily = self.repo / "second-brain" / "05 Daily Notes" / "2026-07-14.md"
        project = self.repo / "second-brain" / "02 Projects" / "ExampleProject.md"
        before = (daily.read_bytes(), project.read_bytes())
        payload_path = self.root / "transactional-closeout.json"
        payload_path.write_text(
            json.dumps(
                {
                    **self.common_payload("closeout-transaction-001"),
                    "date": "2026-07-14",
                    "project": "ExampleProject",
                    "planned": "Validate 20 Grade 8 contest questions.",
                    "completed": "17 validated.",
                    "evidence": "https://example.invalid/evidence",
                    "blocker": "Three remain.",
                    "decisions": [],
                    "open": [],
                    "next": "Finish three.",
                    "confirmed": True,
                }
            ),
            encoding="utf-8",
        )
        code = (
            "from unittest import mock\n"
            "from second_brain import cli, vault\n"
            "original = vault.atomic_replace_if_unchanged\n"
            "calls = {'count': 0}\n"
            "def fail_second(root, path, expected, content, mode=0o644):\n"
            "    calls['count'] += 1\n"
            "    if calls['count'] == 2:\n"
            "        raise OSError('PRIVATE_FAILURE_DETAIL')\n"
            "    return original(root, path, expected, content, mode)\n"
            "with mock.patch.object(vault, 'atomic_replace_if_unchanged', side_effect=fail_second):\n"
            "    raise SystemExit(cli.main(['closeout', '--payload', '"
            + str(payload_path)
            + "']))\n"
        )
        env = {
            **self.env,
            "PYTHONPATH": str(self.repo / "scripts"),
        }
        result = subprocess.run(
            [sys.executable, "-B", "-c", code],
            cwd=self.outside,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("PRIVATE_FAILURE_DETAIL", result.stderr)
        self.assertEqual((daily.read_bytes(), project.read_bytes()), before)
        self.assertEqual(list(daily.parent.glob(f".{daily.name}.*")), [])
        self.assertEqual(list(project.parent.glob(f".{project.name}.*")), [])

    def test_symlinked_repo_override_is_rejected(self) -> None:
        repo_link = self.root / "repo-link"
        repo_link.symlink_to(self.repo, target_is_directory=True)
        env = {**self.env, "SECOND_BRAIN_REPO_ROOT": str(repo_link)}
        decisions = self.repo / "second-brain" / "00 Context" / "Decisions.md"
        before = decisions.read_bytes()
        payload = {
            **self.common_payload("decision-repo-link-001"),
            "title": "Do not trust repo links",
            "summary": "Repository overrides must be canonical source paths.",
            "target": "00 Context/Decisions.md",
            "links": [],
            "visibility": "public-sanitized",
            "confirmed": True,
        }
        result = self.run_command(
            "capture",
            "--kind",
            "personal-decision",
            "--payload",
            "-",
            payload=payload,
            env=env,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn(str(self.root), result.stderr)
        self.assertEqual(decisions.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
