#!/usr/bin/env python3
"""Exercise private memory behavior with synthetic temporary directories only."""

import copy
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "dot_agents/skills/personal-context/scripts/context_store.py"
)


def entry(identifier="layout-1", key="design.layout", **changes):
    value = {
        "id": identifier,
        "key": key,
        "topic": "design",
        "statement": "Synthetic preference: spacious layouts.",
        "basis": "user_stated",
        "source": {"ref": "discussion:synthetic-1", "as_of": "2026-01-01"},
        "scope": "personal prototypes",
        "implication": "Explore spacious layouts when the audience permits.",
    }
    value.update(changes)
    return value


class PersonalContextStoreTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="personal-context-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "ai-context/context.json"

    def run_store(self, *args, payload=None, root=None, child_umask=-1):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--root", str(root or self.root), *args],
            input=json.dumps(payload) if payload is not None else None,
            capture_output=True,
            text=True,
            check=False,
            umask=child_umask,
        )

    def update(self, payload):
        result = self.run_store("update", "--payload", "-", payload=payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def read(self, *args):
        result = self.run_store("read", *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_missing_read_does_not_create_root_or_store(self):
        root = self.root / "absent"
        result = self.run_store("read", root=root)
        self.assertEqual(result.returncode, 0, result.stderr)
        value = json.loads(result.stdout)
        self.assertEqual(value["entries"], [])
        self.assertEqual(value["revision"], 0)
        self.assertIsNone(value["updated_at"])
        self.assertFalse(root.exists())
        validation = self.run_store("validate")
        self.assertNotEqual(validation.returncode, 0)
        self.assertFalse((self.root / "ai-context").exists())

    def test_updates_filter_topics_and_print_only_metadata(self):
        second = entry("workflow-1", "workflow.review", topic="workflow")
        output = self.update({"entries": [entry(), second]})
        self.assertTrue(output["changed"])
        self.assertEqual(output["revision"], 1)
        self.assertNotIn("Synthetic preference", json.dumps(output))
        self.assertNotIn("design.layout", json.dumps(output))
        result = self.read("--topic", "workflow")
        self.assertEqual([item["id"] for item in result["entries"]], ["workflow-1"])
        self.assertTrue(result["entries"][0]["recorded_at"].endswith("Z"))
        validation = self.run_store("validate")
        self.assertEqual(validation.returncode, 0, validation.stderr)
        self.assertNotIn("Synthetic preference", validation.stdout)
        self.assertEqual(json.loads(validation.stdout)["entries"], 2)

    def test_inference_stays_unconfirmed_and_direct_correction_supersedes(self):
        self.update({"entries": [entry()]})
        self.update({"entries": [entry("layout-inference", basis="inferred")]})
        entries = {item["id"]: item for item in self.read()["entries"]}
        self.assertEqual(entries["layout-1"]["status"], "active")
        self.assertEqual(entries["layout-inference"]["status"], "unconfirmed")
        self.update({"entries": [entry("layout-source", basis="source_reported", statement="Old source preference.")]})
        imported = {item["id"]: item for item in self.read()["entries"]}
        self.assertEqual(imported["layout-1"]["status"], "active")
        self.assertEqual(imported["layout-source"]["status"], "unconfirmed")
        self.update({"entries": [entry("layout-correction", statement="Compact layouts.")]})
        self.assertEqual([item["id"] for item in self.read()["entries"]], ["layout-correction"])
        statuses = {item["id"]: item["status"] for item in self.read("--include-inactive")["entries"]}
        self.assertEqual(statuses, {"layout-1": "superseded", "layout-inference": "superseded", "layout-source": "superseded", "layout-correction": "active"})
        before = self.path.read_bytes()
        invalid = self.run_store("update", "--payload", "-", payload={"entries": [entry("bad-inference", basis="inferred", status="active")]})
        self.assertNotEqual(invalid.returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)

    def test_replaying_stale_entry_is_idempotent_and_conflicting_id_is_rejected(self):
        original = entry()
        self.update({"entries": [original]})
        self.update({"entries": [entry("layout-2", statement="Dense layouts.")]})
        before = self.path.read_bytes()
        result = self.update({"entries": [original]})
        self.assertFalse(result["changed"])
        self.assertEqual(result["revision"], 2)
        self.assertEqual(self.path.read_bytes(), before)
        conflict = self.run_store("update", "--payload", "-", payload={"entries": [entry(statement="Changed ID payload.")]})
        self.assertNotEqual(conflict.returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)

    def test_backdated_correction_cannot_replace_current_user_guidance(self):
        self.update({"entries": [entry("current", recorded_at="2026-10-04T12:00:00Z")]})
        before = self.path.read_bytes()
        older = entry(
            "backdated",
            statement="Older synthetic preference.",
            recorded_at="2026-10-03T12:00:00Z",
            source={"ref": "discussion:synthetic-older", "as_of": "2026-10-05"},
        )
        result = self.run_store("update", "--payload", "-", payload={"entries": [older]})
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual([item["id"] for item in self.read()["entries"]], ["current"])

    def test_questions_remember_answered_and_declined_statuses(self):
        question = {"id": "q-layout", "topic": "design", "question": "What helped you decide?", "reason": "Improve design tradeoffs.", "status": "open"}
        self.update({"questions": [question]})
        question["status"] = "declined"
        self.update({"questions": [question]})
        another = dict(question, id="q-workflow", topic="workflow", status="answered")
        self.update({"questions": [another]})
        self.assertEqual([item["status"] for item in self.read("--topic", "design")["questions"]], ["declined"])
        self.assertEqual([item["status"] for item in self.read("--topic", "workflow")["questions"]], ["answered"])
        self.assertEqual(len(self.read()["questions"]), 2)
        before = self.path.read_bytes()
        self.assertFalse(self.update({"questions": [another]})["changed"])
        self.assertEqual(self.path.read_bytes(), before)

    def test_stale_open_question_cannot_reopen_a_declined_question(self):
        question = {"id": "q-design", "topic": "design", "question": "Synthetic topic?", "reason": "Clarify a tradeoff.", "status": "declined"}
        self.update({"questions": [question]})
        before = self.path.read_bytes()
        result = self.run_store("update", "--payload", "-", payload={"questions": [dict(question, status="open")]})
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)

    def test_forgetting_removes_history_and_blocks_reimport(self):
        self.update({"entries": [entry()]})
        self.update({"entries": [entry("layout-2")]})
        self.update({"forget_keys": ["design.layout"]})
        result = self.read("--include-inactive")
        self.assertEqual(result["entries"], [])
        self.assertEqual(result["forgotten_keys"], ["design.layout"])
        before = self.path.read_bytes()
        retry = self.run_store("update", "--payload", "-", payload={"entries": [entry("source-reimport", basis="source_reported")]})
        self.assertNotEqual(retry.returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertNotIn("design.layout", retry.stderr)

    def test_forgetting_also_erases_related_questions_and_blocks_replay(self):
        question = {"id": "q-layout", "topic": "design", "question": "Synthetic personal detail?", "reason": "Related private implication.", "status": "answered"}
        self.update({"entries": [entry()], "questions": [question]})
        self.update({"forget_keys": ["design.layout"], "forget_question_ids": ["q-layout"]})
        result = self.read("--include-inactive")
        self.assertEqual(result["entries"], [])
        self.assertEqual(result["questions"], [])
        self.assertEqual(result["forgotten_question_ids"], ["q-layout"])
        self.assertNotIn("Related private implication", self.path.read_text())
        before = self.path.read_bytes()
        replay = self.run_store("update", "--payload", "-", payload={"entries": [entry("new", "workflow.new")], "questions": [question]})
        self.assertNotEqual(replay.returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertNotIn("q-layout", replay.stderr)

    def test_bad_payloads_are_atomic_and_do_not_echo_private_values(self):
        self.update({"entries": [entry()]})
        before = self.path.read_bytes()
        for payload in (
            {"unknown-private-marker": "private-value"},
            {"entries": "private-value"},
            {"entries": [entry("duplicate"), entry("duplicate")]},
            {"entries": [entry("valid"), entry("invalid", basis="private-value")]},
            {"entries": [entry("wrong-source", source={"ref": "private-value"})]},
            {"entries": [entry("wrong-type", topic=True)]},
            {"entries": [entry("extra", extra="private-value")]},
            {"entries": [entry("date", recorded_at="yesterday")]},
            {"entries": [entry("unicode", statement="private-value\ud800")]},
            {"forget_keys": ["design.layout"], "entries": [entry("conflict")]},
        ):
            with self.subTest(payload=payload):
                result = self.run_store("update", "--payload", "-", payload=payload)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.path.read_bytes(), before)
                self.assertNotIn("private-value", result.stderr + result.stdout)
                self.assertNotIn("private-marker", result.stderr + result.stdout)
                self.assertTrue(result.stderr.startswith('{"ok": false,'), result.stderr)

    def test_invalid_persisted_data_is_never_overwritten(self):
        self.update({"entries": [entry()]})
        original = json.loads(self.path.read_text())
        invalid_documents = [b'{"private-marker":', b'{"schema_version":1,"schema_version":1}']
        for transform in (
            lambda value: value.update(schema_version=99),
            lambda value: value.update(revision=True),
            lambda value: value["entries"].append(copy.deepcopy(value["entries"][0])),
            lambda value: value.update(extra="private-marker"),
        ):
            document = copy.deepcopy(original)
            transform(document)
            invalid_documents.append(json.dumps(document).encode())
        for invalid in invalid_documents:
            with self.subTest(invalid=invalid):
                self.path.write_bytes(invalid)
                for args in (("read",), ("validate",), ("update", "--payload", "-")):
                    result = self.run_store(*args, payload={"entries": [entry("new")]})
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(self.path.read_bytes(), invalid)
                    self.assertNotIn("private-marker", result.stderr + result.stdout)

    def test_concurrent_updates_keep_all_entries(self):
        processes = []
        for index in range(10):
            process = subprocess.Popen(
                [sys.executable, "-B", str(SCRIPT), "--root", str(self.root), "update", "--payload", "-"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            process.stdin.write(json.dumps({"entries": [entry(f"entry-{index}", f"topic.key-{index}")]}))
            process.stdin.close()
            process.stdin = None
            processes.append(process)
        outputs = [process.communicate(timeout=15) for process in processes]
        for process, (stdout, stderr) in zip(processes, outputs):
            self.assertEqual(process.returncode, 0, stderr)
            self.assertTrue(json.loads(stdout)["changed"])
        result = self.read()
        self.assertEqual(len(result["entries"]), 10)
        self.assertEqual(result["revision"], 10)

    def test_symlink_and_hardlink_destinations_are_rejected(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.root / "ai-context").symlink_to(outside, target_is_directory=True)
        result = self.run_store("update", "--payload", "-", payload={"entries": [entry()]})
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])
        (self.root / "ai-context").unlink()
        self.update({"entries": [entry()]})
        for name in ("context.json", ".context.lock"):
            destination = self.path.parent / name
            original = destination.read_bytes()
            target = outside / name
            target.write_bytes(original)
            destination.unlink()
            for create_link in (lambda: destination.symlink_to(target), lambda: os.link(target, destination)):
                create_link()
                result = self.run_store("update", "--payload", "-", payload={"entries": [entry("next")]})
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(target.read_bytes(), original)
                destination.unlink()
            destination.write_bytes(original)

    def test_symlink_root_and_repository_or_installed_skill_roots_are_rejected(self):
        self.update({"entries": [entry()]})
        fixture = self.root / "fixture"
        fixture.mkdir()
        link = self.root / "link"
        link.symlink_to(fixture, target_is_directory=True)
        repo = self.root / "repo"
        repo.mkdir()
        (repo / ".git").write_text("gitdir: synthetic")
        nested = repo / "private"
        nested.mkdir()
        installed = self.root / ".agents/skills/private"
        installed.mkdir(parents=True)
        for destination in (link, nested, installed):
            with self.subTest(destination=destination):
                result = self.run_store("update", "--payload", "-", root=destination, payload={"entries": [entry()]})
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((destination / "ai-context").exists())

    def test_designated_root_may_own_git_metadata_without_allowing_ancestor_or_nested_repos(self):
        spec = importlib.util.spec_from_file_location("personal_context_store", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        git_marker = self.root / ".git"
        git_marker.mkdir()
        sentinel = git_marker / "synthetic-marker"
        sentinel.write_text("Private Git metadata remains unchanged.\n")
        with mock.patch.object(module, "DEFAULT_ROOT", self.root):
            try:
                output = module.update_store(self.root, {"entries": [entry()]})
            except module.StoreError as error:
                self.fail(f"The designated external root must allow its own Git marker: {error}")
            self.assertTrue(output["changed"])
            self.assertEqual(len(module.read_store(self.root)["entries"]), 1)
            before = self.path.read_bytes()
            (self.path.parent / ".git").mkdir()
            with self.assertRaises(module.StoreError):
                module.update_store(self.root, {"entries": [entry("new")]})
            self.assertEqual(self.path.read_bytes(), before)
        nested = self.root / "private"
        nested.mkdir()
        with mock.patch.object(module, "DEFAULT_ROOT", nested):
            with self.assertRaises(module.StoreError):
                module.update_store(nested, {"entries": [entry()]})
            self.assertFalse((nested / "ai-context").exists())
        self.assertEqual(sentinel.read_text(), "Private Git metadata remains unchanged.\n")

    def test_store_and_lock_permissions_are_private(self):
        self.update({"entries": [entry()]})
        for path, expected in ((self.path.parent, 0o700), (self.path, 0o600), (self.path.parent / ".context.lock", 0o600)):
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), expected)
        os.chmod(self.path.parent, 0o755)
        os.chmod(self.path, 0o644)
        os.chmod(self.path.parent / ".context.lock", 0o644)
        self.assertFalse(self.update({"entries": [entry()]})["changed"])
        self.assertEqual(stat.S_IMODE(self.path.parent.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(self.path.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE((self.path.parent / ".context.lock").stat().st_mode), 0o600)

    def test_reads_and_validation_reject_public_store_permissions(self):
        self.update({"entries": [entry()]})
        for path, wide, private in (
            (self.path.parent, 0o755, 0o700),
            (self.path, 0o644, 0o600),
            (self.path.parent / ".context.lock", 0o644, 0o600),
        ):
            with self.subTest(path=path):
                os.chmod(path, wide)
                before = self.path.read_bytes()
                for command in ("read", "validate"):
                    result = self.run_store(command)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(self.path.read_bytes(), before)
                    self.assertNotIn("Synthetic preference", result.stdout + result.stderr)
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), wide)
                os.chmod(path, private)

    def test_restrictive_umask_supports_initial_and_later_updates(self):
        for identifier in ("first", "second"):
            result = self.run_store(
                "update", "--payload", "-", payload={"entries": [entry(identifier)]}, child_umask=0o277,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["changed"])
            self.assertEqual(stat.S_IMODE(self.path.parent.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE(self.path.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE((self.path.parent / ".context.lock").stat().st_mode), 0o600)
        self.assertEqual([item["id"] for item in self.read()["entries"]], ["second"])
        self.assertEqual(self.read()["revision"], 2)

    def test_failed_atomic_replace_preserves_original_and_removes_temporary_file(self):
        self.update({"entries": [entry()]})
        before = self.path.read_bytes()
        spec = importlib.util.spec_from_file_location("personal_context_store", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with mock.patch.object(module.os, "replace", side_effect=OSError("synthetic disk failure")):
            with self.assertRaises(module.StoreError):
                module.update_store(self.root, {"entries": [entry("new")]})
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual({path.name for path in self.path.parent.iterdir()}, {"context.json", ".context.lock"})


if __name__ == "__main__":
    unittest.main()
