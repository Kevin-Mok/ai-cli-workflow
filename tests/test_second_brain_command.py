#!/usr/bin/env python3

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

    def test_help_exposes_task_one_commands(self) -> None:
        completed = self.run_command("--help")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        for command in ("status", "capture", "focus", "closeout"):
            self.assertIn(command, completed.stdout)

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
        self.assertEqual(report["latest_daily_notes"], ["2026-07-14"])
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


if __name__ == "__main__":
    unittest.main()
