#!/usr/bin/env python3

import hashlib
import importlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "executable_second-brain"
SOURCE_VAULT = REPO_ROOT / "second-brain"
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))
IMPORT_DATE = "2026-07-14"


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def approval_sha256(plan: dict[str, object]) -> str:
    unsigned = dict(plan)
    unsigned.pop("approval_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def wrapped_import(source: bytes, source_sha256: str) -> bytes:
    header = (
        "---\n"
        "tags: [archive, imported]\n"
        "status: archived\n"
        f"date: {IMPORT_DATE}\n"
        "visibility: public-sanitized\n"
        f"source_sha256: {source_sha256}\n"
        "---\n\n"
    ).encode("utf-8")
    return header + source


class SecondBrainMigrationApplyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        (self.repo / ".git").mkdir()
        shutil.copytree(SOURCE_VAULT, self.repo / "second-brain")

        self.source = self.root / "private-source"
        self.source.mkdir()
        self.state_home = self.root / "state"
        self.outside = self.root / "outside"
        self.outside.mkdir()
        self.plan_counter = 0
        self.env = {
            **os.environ,
            "HOME": str(self.root / "home"),
            "XDG_STATE_HOME": str(self.state_home),
            "SECOND_BRAIN_REPO_ROOT": str(self.repo),
            "SECOND_BRAIN_NOW": "2026-07-14T09:30:00-04:00",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        Path(self.env["HOME"]).mkdir()

    def run_command(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *arguments],
            cwd=self.outside,
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )

    @staticmethod
    def tree_snapshot(root: Path) -> dict[str, tuple[bytes, int, int]]:
        snapshot: dict[str, tuple[bytes, int, int]] = {}
        if not root.exists():
            return snapshot
        for path in sorted(root.rglob("*")):
            if path.is_file() and not path.is_symlink():
                metadata = path.stat()
                snapshot[path.relative_to(root).as_posix()] = (
                    path.read_bytes(),
                    stat.S_IMODE(metadata.st_mode),
                    metadata.st_mtime_ns,
                )
        return snapshot

    def write_source(self, relative: str, content: bytes) -> Path:
        path = self.source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        path.chmod(0o640)
        return path

    def entry_id(self, relative: str) -> str:
        identity = f"{self.source.resolve()}\0{relative}".encode("utf-8")
        return sha256_bytes(identity)[:16]

    def make_plan(
        self,
        files: list[tuple[str, str]],
    ) -> tuple[dict[str, object], Path, str]:
        entries: list[dict[str, object]] = []
        total_bytes = 0
        for relative, destination in files:
            source_content = (self.source / relative).read_bytes()
            source_hash = sha256_bytes(source_content)
            destination_content = wrapped_import(source_content, source_hash)
            entries.append(
                {
                    "entry_id": self.entry_id(relative),
                    "source_id": "source-001",
                    "source_path": relative,
                    "source_bytes": len(source_content),
                    "source_sha256": source_hash,
                    "destination": destination,
                    "destination_sha256": sha256_bytes(destination_content),
                }
            )
            total_bytes += len(source_content)

        inventory = {
            "schema_version": 1,
            "command": "migrate inventory",
            "sources": [{"id": "source-001", "path": str(self.source.resolve())}],
            "entries": [],
            "summary": {
                "eligible_files": len(entries),
                "eligible_bytes": total_bytes,
                "rejected_entries": 0,
            },
        }
        plan: dict[str, object] = {
            "schema_version": 1,
            "command": "migrate plan",
            "date": IMPORT_DATE,
            "inventory_sha256": sha256_bytes(canonical_json(inventory)),
            "sources": [{"id": "source-001", "path": str(self.source.resolve())}],
            "mappings": [
                {
                    "source_id": "source-001",
                    "target": "06 Archive/Imports/private-source",
                    "reason": "safe_archive_default",
                }
            ],
            "entries": entries,
            "summary": {"files": len(entries), "source_bytes": total_bytes},
        }
        approval = approval_sha256(plan)
        plan["approval_sha256"] = approval
        self.plan_counter += 1
        path = self.root / f"migration-plan-{self.plan_counter}.json"
        path.write_text(
            json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return plan, path, approval

    def expected_ledger_path(self, approval: str) -> Path:
        return (
            self.state_home
            / "second-brain"
            / "migrations"
            / f"{approval}.json"
        )

    @staticmethod
    def reapprove_plan(plan: dict[str, object], path: Path) -> str:
        plan.pop("approval_sha256", None)
        approval = approval_sha256(plan)
        plan["approval_sha256"] = approval
        path.write_text(
            json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return approval

    def assert_safe_error(
        self,
        completed: subprocess.CompletedProcess[str],
        keyword: str,
        *private_values: str,
    ) -> None:
        self.assertEqual(completed.returncode, 2, completed.stderr)
        self.assertEqual(completed.stdout, "")
        self.assertIn(keyword, completed.stderr.lower())
        self.assertNotIn("invalid choice", completed.stderr.lower())
        self.assertNotIn("Traceback", completed.stderr)
        for value in private_values:
            self.assertNotIn(value, completed.stderr)

    def apply(self, plan_path: Path, approval: str) -> subprocess.CompletedProcess[str]:
        return self.run_command(
            "migrate",
            "apply",
            "--plan",
            str(plan_path),
            "--approve",
            approval,
        )

    def verify(self, ledger_path: Path) -> subprocess.CompletedProcess[str]:
        return self.run_command(
            "migrate",
            "verify",
            "--ledger",
            str(ledger_path),
        )

    def test_help_exposes_migration_apply_and_verify(self) -> None:
        root_help = self.run_command("--help")
        self.assertEqual(root_help.returncode, 0, root_help.stderr)
        self.assertIn("migrate", root_help.stdout)

        migrate_help = self.run_command("migrate", "--help")
        self.assertEqual(migrate_help.returncode, 0, migrate_help.stderr)
        self.assertIn("apply", migrate_help.stdout)
        self.assertIn("verify", migrate_help.stdout)

    def test_apply_rejects_noncanonical_source_relative_path(self) -> None:
        self.write_source("note.md", b"# Safe\n")
        plan, plan_path, _ = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        plan["entries"][0]["source_path"] = "./note.md"
        plan["entries"][0]["entry_id"] = self.entry_id("./note.md")
        approval = self.reapprove_plan(plan, plan_path)

        completed = self.apply(plan_path, approval)

        self.assert_safe_error(completed, "plan")
        self.assertFalse(self.expected_ledger_path(approval).exists())
        self.assertFalse(
            (
                self.repo
                / "second-brain/06 Archive/Imports/private-source/note.md"
            ).exists()
        )

    def test_apply_rejects_noncanonical_mapping_target(self) -> None:
        self.write_source("note.md", b"# Safe\n")
        plan, plan_path, _ = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        plan["mappings"][0]["target"] = (
            "06 Archive/Imports/./private-source"
        )
        approval = self.reapprove_plan(plan, plan_path)

        completed = self.apply(plan_path, approval)

        self.assert_safe_error(completed, "plan")
        self.assertFalse(self.expected_ledger_path(approval).exists())

    def test_apply_rejects_noncanonical_destination_path(self) -> None:
        self.write_source("note.md", b"# Safe\n")
        plan, plan_path, _ = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        plan["entries"][0]["destination"] = (
            "06 Archive/Imports/private-source/./note.md"
        )
        approval = self.reapprove_plan(plan, plan_path)

        completed = self.apply(plan_path, approval)

        self.assert_safe_error(completed, "plan")
        self.assertFalse(self.expected_ledger_path(approval).exists())
        self.assertFalse(
            (
                self.repo
                / "second-brain/06 Archive/Imports/private-source/note.md"
            ).exists()
        )

    def test_apply_rejects_wrong_approval_without_changes(self) -> None:
        self.write_source("note.md", b"# Approved note\n\nSafe body.\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        repo_before = self.tree_snapshot(self.repo)
        source_before = self.tree_snapshot(self.source)

        completed = self.apply(plan_path, "0" * 64)

        self.assert_safe_error(completed, "approval", "Safe body.")
        self.assertEqual(self.tree_snapshot(self.repo), repo_before)
        self.assertEqual(self.tree_snapshot(self.source), source_before)
        self.assertFalse(self.expected_ledger_path(approval).exists())

    def test_apply_rejects_plan_tampering_without_changes(self) -> None:
        self.write_source("first.md", b"# First\n\nSafe first body.\n")
        self.write_source("second.md", b"# Second\n\nSafe second body.\n")
        plan, plan_path, approval = self.make_plan(
            [
                ("first.md", "06 Archive/Imports/private-source/first.md"),
                ("second.md", "06 Archive/Imports/private-source/second.md"),
            ]
        )
        plan["entries"][1]["destination"] = (
            "06 Archive/Imports/private-source/tampered.md"
        )
        plan_path.write_text(
            json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        repo_before = self.tree_snapshot(self.repo)
        source_before = self.tree_snapshot(self.source)

        completed = self.apply(plan_path, approval)

        self.assert_safe_error(completed, "approval")
        self.assertEqual(self.tree_snapshot(self.repo), repo_before)
        self.assertEqual(self.tree_snapshot(self.source), source_before)
        self.assertFalse(self.expected_ledger_path(approval).exists())

    def test_apply_rejects_reapproved_short_destination_without_changes(self) -> None:
        self.write_source("note.md", b"# Safe\n\nApproved body.\n")
        plan, plan_path, _ = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        plan["entries"][0]["destination"] = "short"
        approval = self.reapprove_plan(plan, plan_path)
        repo_before = self.tree_snapshot(self.repo)

        completed = self.apply(plan_path, approval)

        self.assert_safe_error(completed, "plan", "Approved body.")
        self.assertEqual(self.tree_snapshot(self.repo), repo_before)
        self.assertFalse(self.expected_ledger_path(approval).exists())

    def test_apply_rejects_reapproved_unsafe_mapping_without_changes(self) -> None:
        self.write_source("note.md", b"# Safe\n\nApproved body.\n")
        plan, plan_path, _ = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        plan["mappings"][0]["target"] = "01 Projects/escaped"
        approval = self.reapprove_plan(plan, plan_path)
        repo_before = self.tree_snapshot(self.repo)

        completed = self.apply(plan_path, approval)

        self.assert_safe_error(completed, "plan", "Approved body.")
        self.assertEqual(self.tree_snapshot(self.repo), repo_before)
        self.assertFalse(self.expected_ledger_path(approval).exists())

    def test_apply_rejects_reapproved_inconsistent_summary_without_changes(self) -> None:
        self.write_source("note.md", b"# Safe\n\nApproved body.\n")
        plan, plan_path, _ = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        plan["summary"]["files"] = 99
        approval = self.reapprove_plan(plan, plan_path)
        repo_before = self.tree_snapshot(self.repo)

        completed = self.apply(plan_path, approval)

        self.assert_safe_error(completed, "plan", "Approved body.")
        self.assertEqual(self.tree_snapshot(self.repo), repo_before)
        self.assertFalse(self.expected_ledger_path(approval).exists())

    def test_apply_rejects_reapproved_invalid_date_without_changes(self) -> None:
        self.write_source("note.md", b"# Safe\n\nApproved body.\n")
        plan, plan_path, _ = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        plan["date"] = "not-a-date"
        approval = self.reapprove_plan(plan, plan_path)
        repo_before = self.tree_snapshot(self.repo)

        completed = self.apply(plan_path, approval)

        self.assert_safe_error(completed, "plan", "Approved body.")
        self.assertEqual(self.tree_snapshot(self.repo), repo_before)
        self.assertFalse(self.expected_ledger_path(approval).exists())

    def test_apply_preflights_every_source_before_copying_any_entry(self) -> None:
        self.write_source("first.md", b"# First\n\nFirst safe body.\n")
        second = self.write_source("second.md", b"# Second\n\nOriginal body.\n")
        _, plan_path, approval = self.make_plan(
            [
                ("first.md", "06 Archive/Imports/private-source/first.md"),
                ("second.md", "06 Archive/Imports/private-source/second.md"),
            ]
        )
        second.write_bytes(b"# Second\n\nPRIVATE_CHANGED_AFTER_APPROVAL\n")
        changed_source = self.tree_snapshot(self.source)
        repo_before = self.tree_snapshot(self.repo)

        completed = self.apply(plan_path, approval)

        self.assert_safe_error(
            completed,
            "source",
            "PRIVATE_CHANGED_AFTER_APPROVAL",
        )
        self.assertEqual(self.tree_snapshot(self.repo), repo_before)
        self.assertEqual(self.tree_snapshot(self.source), changed_source)
        self.assertFalse(self.expected_ledger_path(approval).exists())

    def test_apply_never_overwrites_destination_created_after_plan(self) -> None:
        self.write_source("note.md", b"# Source\n\nApproved body.\n")
        destination_relative = "06 Archive/Imports/private-source/note.md"
        _, plan_path, approval = self.make_plan(
            [("note.md", destination_relative)]
        )
        destination = self.repo / "second-brain" / destination_relative
        destination.parent.mkdir(parents=True)
        destination.write_bytes(b"DO_NOT_OVERWRITE_DESTINATION\n")
        destination_before = destination.read_bytes()
        source_before = self.tree_snapshot(self.source)

        completed = self.apply(plan_path, approval)

        self.assert_safe_error(completed, "destination", "Approved body.")
        self.assertEqual(destination.read_bytes(), destination_before)
        self.assertEqual(self.tree_snapshot(self.source), source_before)
        self.assertFalse(self.expected_ledger_path(approval).exists())

    def test_apply_never_overwrites_destination_created_after_preflight(
        self,
    ) -> None:
        self.write_source("note.md", b"# Source\n\nApproved body.\n")
        destination_relative = "06 Archive/Imports/private-source/note.md"
        _, plan_path, approval = self.make_plan(
            [("note.md", destination_relative)]
        )
        destination = self.repo / "second-brain" / destination_relative
        source_before = self.tree_snapshot(self.source)
        migration_apply = importlib.import_module("second_brain.migration_apply")
        real_atomic_create = migration_apply.atomic_create

        def inject_late_destination(root, target, content, mode=0o644, **kwargs):
            if target == destination:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"LATE_DESTINATION_SENTINEL\n")
            return real_atomic_create(root, target, content, mode, **kwargs)

        with mock.patch.dict(os.environ, self.env, clear=True):
            with mock.patch.object(
                migration_apply,
                "atomic_create",
                side_effect=inject_late_destination,
            ):
                with self.assertRaises(migration_apply.MigrationError):
                    migration_apply.apply_migration(str(plan_path), approval)

        self.assertEqual(
            destination.read_bytes(),
            b"LATE_DESTINATION_SENTINEL\n",
        )
        self.assertEqual(self.tree_snapshot(self.source), source_before)

    def test_apply_rejects_portable_sibling_created_after_preflight(self) -> None:
        self.write_source("note.md", b"# Source\n\nApproved body.\n")
        destination_relative = "06 Archive/Imports/private-source/note.md"
        _, plan_path, approval = self.make_plan(
            [("note.md", destination_relative)]
        )
        destination = self.repo / "second-brain" / destination_relative
        sibling = destination.with_name("NOTE.md")
        migration_apply = importlib.import_module("second_brain.migration_apply")
        real_atomic_create = migration_apply.atomic_create

        def inject_late_sibling(root, target, content, mode=0o644, **kwargs):
            if target == destination:
                sibling.parent.mkdir(parents=True, exist_ok=True)
                sibling.write_bytes(b"LATE_PORTABLE_SIBLING\n")
            return real_atomic_create(root, target, content, mode, **kwargs)

        with mock.patch.dict(os.environ, self.env, clear=True):
            with mock.patch.object(
                migration_apply,
                "atomic_create",
                side_effect=inject_late_sibling,
            ):
                with self.assertRaises(migration_apply.MigrationError):
                    migration_apply.apply_migration(str(plan_path), approval)

        self.assertFalse(destination.exists())
        self.assertEqual(sibling.read_bytes(), b"LATE_PORTABLE_SIBLING\n")

    def test_apply_rejects_reapproved_overlapping_source_roots(self) -> None:
        child = self.source / "nested"
        child.mkdir()
        self.write_source("note.md", b"# Safe\n\nApproved body.\n")
        plan, plan_path, _ = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        plan["sources"].append({"id": "source-002", "path": str(child.resolve())})
        plan["mappings"].append(
            {
                "source_id": "source-002",
                "target": "06 Archive/Imports/nested",
                "reason": "safe_archive_default",
            }
        )
        approval = self.reapprove_plan(plan, plan_path)

        completed = self.apply(plan_path, approval)

        self.assert_safe_error(completed, "overlap")
        self.assertFalse(self.expected_ledger_path(approval).exists())
        self.assertFalse(
            (
                self.repo
                / "second-brain/06 Archive/Imports/private-source/note.md"
            ).exists()
        )

    def test_apply_rejects_portable_parent_namespace_collision(self) -> None:
        self.write_source("first.md", b"# First\n")
        self.write_source("second.md", b"# Second\n")
        _, plan_path, approval = self.make_plan(
            [
                ("first.md", "06 Archive/Imports/private-source/Dir/a.md"),
                ("second.md", "06 Archive/Imports/private-source/dir/b.md"),
            ]
        )

        completed = self.apply(plan_path, approval)

        self.assert_safe_error(completed, "plan")
        self.assertFalse(self.expected_ledger_path(approval).exists())
        self.assertFalse(
            (self.repo / "second-brain/06 Archive/Imports/private-source").exists()
        )

    def test_apply_rejects_file_directory_ancestor_conflict_before_copy(self) -> None:
        self.write_source("first.md", b"# First\n")
        self.write_source("second.md", b"# Second\n")
        _, plan_path, approval = self.make_plan(
            [
                ("first.md", "06 Archive/Imports/private-source/node.md"),
                (
                    "second.md",
                    "06 Archive/Imports/private-source/node.md/child.md",
                ),
            ]
        )

        completed = self.apply(plan_path, approval)

        self.assert_safe_error(completed, "plan")
        self.assertFalse(self.expected_ledger_path(approval).exists())
        self.assertFalse(
            (self.repo / "second-brain/06 Archive/Imports/private-source").exists()
        )

    def test_apply_rejects_existing_portable_parent_sibling(self) -> None:
        self.write_source("note.md", b"# Safe\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        imports = self.repo / "second-brain/06 Archive/Imports"
        existing = imports / "PRIVATE-SOURCE"
        existing.mkdir(parents=True)

        completed = self.apply(plan_path, approval)

        self.assert_safe_error(completed, "destination")
        self.assertFalse((imports / "private-source").exists())
        self.assertTrue(existing.is_dir())

    def test_apply_wraps_exact_body_writes_private_ledger_and_preserves_source(
        self,
    ) -> None:
        source_content = (
            b"# Imported note\n\n"
            b"Exact source body with no tracked absolute source path.\n"
        )
        self.write_source("nested/note.md", source_content)
        destination_relative = "06 Archive/Imports/private-source/nested/note.md"
        plan, plan_path, approval = self.make_plan(
            [("nested/note.md", destination_relative)]
        )
        source_before = self.tree_snapshot(self.source)
        repo_before = self.tree_snapshot(self.repo)

        completed = self.apply(plan_path, approval)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        ledger_path = self.expected_ledger_path(approval)
        self.assertEqual(
            json.loads(completed.stdout),
            {
                "schema_version": 1,
                "command": "migrate apply",
                "result": "created",
                "copied": 1,
                "skipped": 0,
                "ledger": str(ledger_path),
            },
        )
        destination = self.repo / "second-brain" / destination_relative
        expected = wrapped_import(source_content, sha256_bytes(source_content))
        self.assertEqual(destination.read_bytes(), expected)
        self.assertEqual(
            destination.read_bytes()[len(expected) - len(source_content) :],
            source_content,
        )
        self.assertNotIn(str(self.source).encode("utf-8"), destination.read_bytes())
        self.assertEqual(self.tree_snapshot(self.source), source_before)

        changed_repo_paths = {
            path
            for path, value in self.tree_snapshot(self.repo).items()
            if repo_before.get(path) != value
        }
        self.assertEqual(
            changed_repo_paths,
            {f"second-brain/{destination_relative}"},
        )
        self.assertTrue(ledger_path.is_file())
        self.assertEqual(stat.S_IMODE(ledger_path.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(ledger_path.parent.stat().st_mode), 0o700)
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        self.assertEqual(ledger["schema_version"], 1)
        self.assertEqual(ledger["kind"], "second-brain-migration-ledger")
        self.assertEqual(ledger["approval_sha256"], approval)
        self.assertEqual(ledger["entries"][0]["status"], "copied")
        self.assertEqual(ledger["entries"][0]["entry_id"], plan["entries"][0]["entry_id"])

    def test_apply_resumes_private_partial_ledger_without_rewriting_completed_entry(
        self,
    ) -> None:
        first_content = b"# First\n\nAlready copied before interruption.\n"
        second_content = b"# Second\n\nPending after interruption.\n"
        self.write_source("first.md", first_content)
        self.write_source("second.md", second_content)
        plan, plan_path, approval = self.make_plan(
            [
                ("first.md", "06 Archive/Imports/private-source/first.md"),
                ("second.md", "06 Archive/Imports/private-source/second.md"),
            ]
        )
        entries = plan["entries"]
        assert isinstance(entries, list)
        first_entry = dict(entries[0])
        second_entry = dict(entries[1])
        first_entry["status"] = "copied"
        second_entry["status"] = "pending"

        first_destination = (
            self.repo / "second-brain" / str(first_entry["destination"])
        )
        first_destination.parent.mkdir(parents=True)
        first_destination.write_bytes(
            wrapped_import(first_content, str(first_entry["source_sha256"]))
        )
        first_before = (
            first_destination.read_bytes(),
            first_destination.stat().st_mtime_ns,
        )
        ledger_path = self.expected_ledger_path(approval)
        ledger_path.parent.mkdir(parents=True, mode=0o700)
        (self.state_home / "second-brain").chmod(0o700)
        ledger_path.parent.chmod(0o700)
        ledger = {
            "schema_version": 1,
            "kind": "second-brain-migration-ledger",
            "approval_sha256": approval,
            "plan": plan,
            "sources": plan["sources"],
            "entries": [first_entry, second_entry],
            "summary": {"copied": 1, "pending": 1},
        }
        ledger_path.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        ledger_path.chmod(0o600)
        source_before = self.tree_snapshot(self.source)

        completed = self.apply(plan_path, approval)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(
            json.loads(completed.stdout),
            {
                "schema_version": 1,
                "command": "migrate apply",
                "result": "updated",
                "copied": 1,
                "skipped": 1,
                "ledger": str(ledger_path),
            },
        )
        self.assertEqual(
            (first_destination.read_bytes(), first_destination.stat().st_mtime_ns),
            first_before,
        )
        second_destination = (
            self.repo / "second-brain" / str(second_entry["destination"])
        )
        self.assertEqual(
            second_destination.read_bytes(),
            wrapped_import(second_content, str(second_entry["source_sha256"])),
        )
        completed_ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        self.assertEqual(
            [entry["status"] for entry in completed_ledger["entries"]],
            ["copied", "copied"],
        )
        self.assertEqual(completed_ledger["summary"], {"copied": 2, "pending": 0})
        self.assertEqual(self.tree_snapshot(self.source), source_before)

    def test_apply_and_verify_reject_symlinked_ledger_parent(self) -> None:
        self.write_source("note.md", b"# Private ledger\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        ledger_path = self.expected_ledger_path(approval)
        outside_ledgers = self.root / "outside-ledgers"
        ledger_path.parent.rename(outside_ledgers)
        ledger_path.parent.symlink_to(outside_ledgers, target_is_directory=True)
        escaped_ledger = outside_ledgers / ledger_path.name
        escaped_ledger.chmod(0o644)
        before = escaped_ledger.read_bytes()

        verified = self.verify(ledger_path)
        repeated = self.apply(plan_path, approval)

        self.assert_safe_error(verified, "ledger")
        self.assert_safe_error(repeated, "ledger")
        self.assertEqual(escaped_ledger.read_bytes(), before)

    def test_apply_and_verify_reject_insecure_ledger_modes(self) -> None:
        self.write_source("note.md", b"# Private modes\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        ledger_path = self.expected_ledger_path(approval)

        ledger_path.chmod(0o644)
        self.assert_safe_error(self.verify(ledger_path), "ledger")
        self.assert_safe_error(self.apply(plan_path, approval), "ledger")

        ledger_path.chmod(0o600)
        ledger_path.parent.chmod(0o755)
        self.assert_safe_error(self.verify(ledger_path), "ledger")
        self.assert_safe_error(self.apply(plan_path, approval), "ledger")

    def test_apply_and_verify_reject_hardlinked_ledger(self) -> None:
        self.write_source("note.md", b"# Private link count\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        ledger_path = self.expected_ledger_path(approval)
        os.link(ledger_path, self.outside / "ledger-copy.json")

        self.assert_safe_error(self.verify(ledger_path), "ledger")
        self.assert_safe_error(self.apply(plan_path, approval), "ledger")

    def test_completed_apply_rerun_is_byte_and_mtime_stable_noop(self) -> None:
        self.write_source("note.md", b"# Stable\n\nNo rewrite on rerun.\n")
        plan, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        first = self.apply(plan_path, approval)
        self.assertEqual(first.returncode, 0, first.stderr)
        ledger_path = self.expected_ledger_path(approval)
        entry = plan["entries"][0]
        destination = self.repo / "second-brain" / str(entry["destination"])
        before = {
            "destination": (destination.read_bytes(), destination.stat().st_mtime_ns),
            "ledger": (ledger_path.read_bytes(), ledger_path.stat().st_mtime_ns),
            "source": self.tree_snapshot(self.source),
        }

        repeated = self.apply(plan_path, approval)

        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(
            json.loads(repeated.stdout),
            {
                "schema_version": 1,
                "command": "migrate apply",
                "result": "noop",
                "copied": 0,
                "skipped": 1,
                "ledger": str(ledger_path),
            },
        )
        self.assertEqual(
            (destination.read_bytes(), destination.stat().st_mtime_ns),
            before["destination"],
        )
        self.assertEqual(
            (ledger_path.read_bytes(), ledger_path.stat().st_mtime_ns),
            before["ledger"],
        )
        self.assertEqual(self.tree_snapshot(self.source), before["source"])

    def test_verify_passes_without_mutating_source_destination_or_ledger(self) -> None:
        self.write_source("note.md", b"# Verify\n\nUntouched verification body.\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        ledger_path = self.expected_ledger_path(approval)
        before = {
            "repo": self.tree_snapshot(self.repo),
            "source": self.tree_snapshot(self.source),
            "state": self.tree_snapshot(self.state_home),
        }

        completed = self.verify(ledger_path)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(
            json.loads(completed.stdout),
            {
                "schema_version": 1,
                "command": "migrate verify",
                "summary": {"status": "pass", "checked": 1, "errors": 0},
                "findings": [],
            },
        )
        self.assertEqual(self.tree_snapshot(self.repo), before["repo"])
        self.assertEqual(self.tree_snapshot(self.source), before["source"])
        self.assertEqual(self.tree_snapshot(self.state_home), before["state"])

    def test_verify_reports_destination_checksum_mismatch_with_exit_one(self) -> None:
        self.write_source("note.md", b"# Verify destination\n\nSafe body.\n")
        plan, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        entry = plan["entries"][0]
        destination = self.repo / "second-brain" / str(entry["destination"])
        destination.write_bytes(b"TAMPERED_DESTINATION_SENTINEL\n")
        ledger_path = self.expected_ledger_path(approval)
        before = {
            "repo": self.tree_snapshot(self.repo),
            "source": self.tree_snapshot(self.source),
            "state": self.tree_snapshot(self.state_home),
        }

        completed = self.verify(ledger_path)

        self.assertEqual(completed.returncode, 1, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(
            report["summary"],
            {"status": "fail", "checked": 1, "errors": 1},
        )
        self.assertEqual(len(report["findings"]), 1)
        finding = report["findings"][0]
        self.assertEqual(
            finding["key"],
            f"migration_destination_checksum_mismatch:{entry['entry_id']}",
        )
        self.assertEqual(finding["code"], "migration_destination_checksum_mismatch")
        self.assertEqual(finding["severity"], "error")
        self.assertEqual(
            finding["locations"],
            [{"path": f"second-brain/{entry['destination']}"}],
        )
        self.assertNotIn("TAMPERED_DESTINATION_SENTINEL", completed.stdout)
        self.assertEqual(self.tree_snapshot(self.repo), before["repo"])
        self.assertEqual(self.tree_snapshot(self.source), before["source"])
        self.assertEqual(self.tree_snapshot(self.state_home), before["state"])

    def test_verify_reports_source_checksum_mismatch_without_absolute_path(self) -> None:
        source = self.write_source(
            "note.md",
            b"# Verify source\n\nOriginal source body.\n",
        )
        plan, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        source.write_bytes(b"PRIVATE_CHANGED_SOURCE_SENTINEL\n")
        entry = plan["entries"][0]
        ledger_path = self.expected_ledger_path(approval)
        before = {
            "repo": self.tree_snapshot(self.repo),
            "source": self.tree_snapshot(self.source),
            "state": self.tree_snapshot(self.state_home),
        }

        completed = self.verify(ledger_path)

        self.assertEqual(completed.returncode, 1, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(
            report["summary"],
            {"status": "fail", "checked": 1, "errors": 1},
        )
        finding = report["findings"][0]
        self.assertEqual(
            finding["key"],
            f"migration_source_checksum_mismatch:{entry['entry_id']}",
        )
        self.assertEqual(finding["code"], "migration_source_checksum_mismatch")
        self.assertEqual(finding["severity"], "error")
        self.assertEqual(
            finding["locations"],
            [{"path": "source-001:note.md"}],
        )
        self.assertNotIn(str(self.source), completed.stdout)
        self.assertNotIn("PRIVATE_CHANGED_SOURCE_SENTINEL", completed.stdout)
        self.assertEqual(self.tree_snapshot(self.repo), before["repo"])
        self.assertEqual(self.tree_snapshot(self.source), before["source"])
        self.assertEqual(self.tree_snapshot(self.state_home), before["state"])

    def test_verify_rejects_ledger_entry_with_extra_field(self) -> None:
        self.write_source("note.md", b"# Exact shape\n\nSafe body.\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        ledger_path = self.expected_ledger_path(approval)
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["entries"][0]["private_note"] = "PRIVATE_LEDGER_SENTINEL"
        ledger_path.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        completed = self.verify(ledger_path)

        self.assert_safe_error(completed, "ledger", "PRIVATE_LEDGER_SENTINEL")

    def test_verify_rejects_noncanonical_destination_path(self) -> None:
        self.write_source("note.md", b"# Destination path\n\nSafe body.\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        ledger_path = self.expected_ledger_path(approval)
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["entries"][0]["destination"] = (
            "06 Archive/Imports/private-source/../escaped.md"
        )
        ledger_path.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        completed = self.verify(ledger_path)

        self.assert_safe_error(completed, "ledger")

    def test_verify_rejects_malformed_ledger_hash(self) -> None:
        self.write_source("note.md", b"# Hash shape\n\nSafe body.\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        ledger_path = self.expected_ledger_path(approval)
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["entries"][0]["source_sha256"] = "not-a-sha256"
        ledger_path.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        completed = self.verify(ledger_path)

        self.assert_safe_error(completed, "ledger")

    def test_verify_rejects_inconsistent_ledger_summary(self) -> None:
        self.write_source("note.md", b"# Summary\n\nSafe body.\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        ledger_path = self.expected_ledger_path(approval)
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["summary"] = {"copied": 0, "pending": 1}
        ledger_path.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        completed = self.verify(ledger_path)

        self.assert_safe_error(completed, "summary")

    def test_verify_rejects_boolean_ledger_summary_counts(self) -> None:
        self.write_source("note.md", b"# Summary types\n\nSafe body.\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        ledger_path = self.expected_ledger_path(approval)
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["summary"] = {"copied": True, "pending": False}
        ledger_path.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        completed = self.verify(ledger_path)

        self.assert_safe_error(completed, "summary")

    def test_verify_rejects_source_path_traversal(self) -> None:
        self.write_source("note.md", b"# Traversal\n\nSafe body.\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        ledger_path = self.expected_ledger_path(approval)
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["entries"][0]["source_path"] = "../private-source/note.md"
        ledger_path.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        completed = self.verify(ledger_path)

        self.assert_safe_error(completed, "ledger")

    def test_verify_rejects_filename_that_does_not_match_ledger_approval(self) -> None:
        self.write_source("note.md", b"# Approval filename\n\nSafe body.\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        original_path = self.expected_ledger_path(approval)
        renamed_path = original_path.with_name(f"{'0' * 64}.json")
        original_path.rename(renamed_path)

        completed = self.verify(renamed_path)

        self.assert_safe_error(completed, "approval")

    def test_verify_rejects_forged_hashes_with_arbitrary_approval_name(self) -> None:
        self.write_source("note.md", b"# Bound plan\n\nSafe body.\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        original = self.expected_ledger_path(approval)
        ledger = json.loads(original.read_text(encoding="utf-8"))
        forged = "b" * 64
        ledger["approval_sha256"] = forged
        ledger["entries"][0]["source_sha256"] = "c" * 64
        ledger["entries"][0]["destination_sha256"] = "d" * 64
        forged_path = self.expected_ledger_path(forged)
        forged_path.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        forged_path.chmod(0o600)

        completed = self.verify(forged_path)

        self.assert_safe_error(completed, "approval")

    def test_verify_reports_pending_entry_without_private_content(self) -> None:
        private_body = "PRIVATE_PENDING_LEDGER_SENTINEL"
        self.write_source("note.md", f"# Pending\n\n{private_body}\n".encode())
        plan, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        ledger_path = self.expected_ledger_path(approval)
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["entries"][0]["status"] = "pending"
        ledger["summary"] = {"copied": 0, "pending": 1}
        ledger_path.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        entry = plan["entries"][0]

        completed = self.verify(ledger_path)

        self.assertEqual(completed.returncode, 1, completed.stderr)
        self.assertEqual(completed.stderr, "")
        report = json.loads(completed.stdout)
        self.assertEqual(
            report["summary"],
            {"status": "fail", "checked": 0, "errors": 1},
        )
        self.assertEqual(
            report["findings"],
            [
                {
                    "code": "migration_entry_pending",
                    "key": f"migration_entry_pending:{entry['entry_id']}",
                    "severity": "error",
                    "locations": [
                        {"path": f"migration-entry:{entry['entry_id']}"}
                    ],
                }
            ],
        )
        self.assertNotIn(str(self.source), completed.stdout)
        self.assertNotIn(private_body, completed.stdout)

    def test_verify_rejects_noncanonical_source_root(self) -> None:
        self.write_source("note.md", b"# Canonical source\n\nSafe body.\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        ledger_path = self.expected_ledger_path(approval)
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["sources"][0]["path"] = str(
            self.source / ".." / self.source.name
        )
        ledger_path.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        completed = self.verify(ledger_path)

        self.assert_safe_error(completed, "source")

    def test_verify_rejects_protected_source_root(self) -> None:
        self.write_source("note.md", b"# Protected source\n\nSafe body.\n")
        _, plan_path, approval = self.make_plan(
            [("note.md", "06 Archive/Imports/private-source/note.md")]
        )
        applied = self.apply(plan_path, approval)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        ledger_path = self.expected_ledger_path(approval)
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["sources"][0]["path"] = str(self.repo)
        ledger_path.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        completed = self.verify(ledger_path)

        self.assert_safe_error(completed, "source")


if __name__ == "__main__":
    unittest.main()
