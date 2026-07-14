#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unicodedata
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "executable_second-brain"
SOURCE_VAULT = REPO_ROOT / "second-brain"
MAX_TEXT_BYTES = 1_000_000

INVENTORY_KEYS = {
    "schema_version",
    "command",
    "sources",
    "entries",
    "summary",
}
INVENTORY_SOURCE_KEYS = {"id", "path"}
ELIGIBLE_ENTRY_KEYS = {
    "source_id",
    "path",
    "type",
    "status",
    "bytes",
    "sha256",
    "title",
}
REJECTED_ENTRY_KEYS = {
    "source_id",
    "path",
    "type",
    "status",
    "reason",
}
INVENTORY_SUMMARY_KEYS = {
    "eligible_files",
    "eligible_bytes",
    "rejected_entries",
}
PLAN_KEYS = {
    "schema_version",
    "command",
    "date",
    "inventory_sha256",
    "sources",
    "mappings",
    "entries",
    "summary",
    "approval_sha256",
}
PLAN_MAPPING_KEYS = {"source_id", "target", "reason"}
PLAN_ENTRY_KEYS = {
    "entry_id",
    "source_id",
    "source_path",
    "source_bytes",
    "source_sha256",
    "destination",
    "destination_sha256",
}
PLAN_SUMMARY_KEYS = {"files", "source_bytes"}


class SecondBrainMigrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)

        self.repo = self.root / "repo"
        self.repo.mkdir()
        (self.repo / ".git").mkdir()
        shutil.copytree(SOURCE_VAULT, self.repo / "second-brain")

        self.home = self.root / "home"
        self.home.mkdir()
        self.state_home = self.root / "state"
        self.state_home.mkdir()
        self.external = self.root / "external"
        self.external.mkdir()
        self.outputs = self.root / "outputs"
        self.outputs.mkdir()
        self.caller = self.root / "caller"
        self.caller.mkdir()

        self.env = {
            **os.environ,
            "HOME": str(self.home),
            "XDG_STATE_HOME": str(self.state_home),
            "SECOND_BRAIN_REPO_ROOT": str(self.repo),
            "SECOND_BRAIN_NOW": "2026-07-14T09:30:00-04:00",
            "PYTHONDONTWRITEBYTECODE": "1",
        }

    def run_migrate(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                "-B",
                str(SCRIPT),
                "migrate",
                *arguments,
            ],
            cwd=self.caller,
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )

    @staticmethod
    def canonical_json(value: Any) -> str:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )

    def assert_canonical_output(
        self, completed: subprocess.CompletedProcess[str]
    ) -> dict[str, Any]:
        self.assertEqual(completed.returncode, 0, completed.stderr)
        value = json.loads(completed.stdout)
        self.assertEqual(completed.stdout, self.canonical_json(value) + "\n")
        return value

    @staticmethod
    def tree_snapshot(root: Path) -> dict[str, tuple[Any, ...]]:
        snapshot: dict[str, tuple[Any, ...]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                snapshot[relative] = ("symlink", os.readlink(path))
            elif path.is_file():
                metadata = path.stat()
                snapshot[relative] = (
                    "file",
                    stat.S_IMODE(metadata.st_mode),
                    metadata.st_size,
                    metadata.st_mtime_ns,
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                )
            elif path.is_dir():
                metadata = path.stat()
                snapshot[relative] = (
                    "directory",
                    stat.S_IMODE(metadata.st_mode),
                    metadata.st_mtime_ns,
                )
        return snapshot

    @staticmethod
    def source_id(inventory: dict[str, Any], source: Path) -> str:
        canonical = str(source.resolve())
        for record in inventory["sources"]:
            if record["path"] == canonical:
                return record["id"]
        raise AssertionError(f"missing source record for {canonical}")

    @staticmethod
    def normalized_name(path: str) -> str:
        return unicodedata.normalize("NFKC", Path(path).name).casefold()

    def test_inventory_accepts_repeatable_sources_and_is_canonical(self) -> None:
        alpha = self.external / "alpha" / "Notes"
        beta = self.external / "beta" / "Journal"
        alpha.mkdir(parents=True)
        beta.mkdir(parents=True)
        alpha_note = alpha / "Contest Prep.md"
        beta_note = beta / "lesson.txt"
        alpha_note.write_text(
            "# Contest Prep\n\nA public-safe planning note.\n",
            encoding="utf-8",
        )
        beta_note.write_text("A plain-text teaching note.\n", encoding="utf-8")
        before = {
            str(alpha): self.tree_snapshot(alpha),
            str(beta): self.tree_snapshot(beta),
        }

        alias_anchor = alpha.parent / "alias-anchor"
        alias_anchor.mkdir()
        alpha_alias = alias_anchor / ".." / alpha.name
        first = self.run_migrate(
            "inventory",
            "--source",
            str(beta),
            "--source",
            str(alpha_alias),
        )
        second = self.run_migrate(
            "inventory",
            "--source",
            str(alpha),
            "--source",
            str(beta),
        )
        inventory = self.assert_canonical_output(first)
        self.assertEqual(first.stdout, second.stdout)

        self.assertEqual(set(inventory), INVENTORY_KEYS)
        self.assertEqual(inventory["schema_version"], 1)
        self.assertEqual(inventory["command"], "migrate inventory")
        self.assertEqual(
            [source["path"] for source in inventory["sources"]],
            sorted((str(alpha.resolve()), str(beta.resolve()))),
        )
        self.assertTrue(
            all(set(source) == INVENTORY_SOURCE_KEYS for source in inventory["sources"])
        )
        self.assertEqual(
            len({source["id"] for source in inventory["sources"]}),
            2,
        )

        entries = inventory["entries"]
        self.assertEqual(len(entries), 2)
        self.assertTrue(all(set(entry) == ELIGIBLE_ENTRY_KEYS for entry in entries))
        self.assertTrue(all(entry["status"] == "eligible" for entry in entries))
        self.assertTrue(all(entry["type"] == "text" for entry in entries))
        alpha_id = self.source_id(inventory, alpha)
        alpha_entry = next(
            entry
            for entry in entries
            if entry["source_id"] == alpha_id
            and entry["path"] == "Contest Prep.md"
        )
        self.assertEqual(alpha_entry["title"], "Contest Prep")
        self.assertEqual(alpha_entry["bytes"], alpha_note.stat().st_size)
        self.assertEqual(
            alpha_entry["sha256"],
            hashlib.sha256(alpha_note.read_bytes()).hexdigest(),
        )
        self.assertEqual(set(inventory["summary"]), INVENTORY_SUMMARY_KEYS)
        self.assertEqual(
            inventory["summary"],
            {
                "eligible_files": 2,
                "eligible_bytes": alpha_note.stat().st_size
                + beta_note.stat().st_size,
                "rejected_entries": 0,
            },
        )
        self.assertEqual(
            before,
            {
                str(alpha): self.tree_snapshot(alpha),
                str(beta): self.tree_snapshot(beta),
            },
        )

    def test_inventory_rejects_protected_symlinked_and_overlapping_roots(self) -> None:
        valid = self.external / "valid"
        valid.mkdir()
        (valid / "note.md").write_text("# Safe\n", encoding="utf-8")

        source_link = self.external / "linked-source"
        source_link.symlink_to(valid, target_is_directory=True)
        linked = self.run_migrate(
            "inventory", "--source", str(source_link)
        )
        self.assertEqual(linked.returncode, 2)
        self.assertIn("symlink", linked.stderr.lower())
        self.assertNotIn(str(source_link), linked.stderr)

        relative = self.run_migrate(
            "inventory", "--source", "relative-source"
        )
        self.assertEqual(relative.returncode, 2)
        self.assertIn("absolute", relative.stderr.lower())
        self.assertNotIn("relative-source", relative.stderr)

        protected_roots = (
            self.repo,
            self.repo / "second-brain",
            self.state_home,
            self.home,
            self.root,
            Path("/home/example/coding"),
        )
        for protected in protected_roots:
            with self.subTest(protected=protected):
                completed = self.run_migrate(
                    "inventory", "--source", str(protected)
                )
                self.assertEqual(completed.returncode, 2)
                self.assertIn("protected", completed.stderr.lower())
                self.assertNotIn(str(protected), completed.stderr)
                self.assertNotIn("Traceback", completed.stderr)

        parent = self.external / "overlap"
        child = parent / "child"
        child.mkdir(parents=True)
        (child / "note.md").write_text("# Nested\n", encoding="utf-8")
        overlapping = self.run_migrate(
            "inventory",
            "--source",
            str(parent),
            "--source",
            str(child),
        )
        self.assertEqual(overlapping.returncode, 2)
        self.assertIn("overlap", overlapping.stderr.lower())
        self.assertNotIn(str(parent), overlapping.stderr)
        self.assertNotIn(str(child), overlapping.stderr)
        self.assertNotIn("Traceback", overlapping.stderr)

    def test_inventory_classifies_text_boundaries_without_rejected_leaks(self) -> None:
        source = self.external / "classification"
        source.mkdir()
        netrc = source / ".netrc"
        netrc.write_text(
            "machine example.invalid login user password PRIVATE_NETRC_SECRET\n",
            encoding="utf-8",
        )
        disguised_netrc = source / "notes.txt"
        disguised_netrc.write_text(
            "machine example.invalid login user password PRIVATE_DISGUISED_SECRET\n",
            encoding="utf-8",
        )
        multiline_netrc = source / "multiline-notes.txt"
        multiline_netrc.write_text(
            "machine example.invalid\n"
            "login user\n"
            "password PRIVATE_MULTILINE_NETRC_SECRET\n",
            encoding="utf-8",
        )
        commented_netrc = source / "commented-netrc-notes.txt"
        commented_netrc.write_text(
            "machine example.invalid\n"
            "# primary account\n"
            "login user\n"
            "password PRIVATE_COMMENTED_NETRC_SECRET\n",
            encoding="utf-8",
        )
        long_comment_netrc = source / "long-comment-netrc-notes.txt"
        long_comment_netrc.write_text(
            "machine example.invalid\n"
            f"# {'x' * 1_001}\n"
            "login user\n"
            "password PRIVATE_LONG_COMMENT_NETRC_SECRET\n",
            encoding="utf-8",
        )
        quoted_json_secret = source / "renamed-config.txt"
        quoted_json_secret.write_text(
            '{"api_key":"PRIVATE_QUOTED_JSON_SECRET"}\n',
            encoding="utf-8",
        )
        ordinary = source / "ordinary.md"
        ordinary.write_text(
            "# Ordinary Public Title\n\nPublic-safe body.\n",
            encoding="utf-8",
        )
        plain = source / "plain.txt"
        plain.write_text("A small plain-text note.\n", encoding="utf-8")
        boundary = source / "boundary.txt"
        boundary.write_bytes(b"x\n" + b"a" * (MAX_TEXT_BYTES - 3))
        oversized = source / "oversized.txt"
        oversized.write_bytes(b"b" * MAX_TEXT_BYTES)
        invalid_utf8 = source / "invalid-utf8.txt"
        invalid_utf8.write_bytes(b"\xff\xfePRIVATE_INVALID_UTF8")
        nul_file = source / "contains-nul.txt"
        nul_file.write_bytes(b"safe-prefix\x00PRIVATE_NUL_CONTENT")
        secret_name = source / ".env"
        secret_name.write_text(
            "DB_PASSWORD=PRIVATE_ENV_CONTENT\n", encoding="utf-8"
        )
        secret_content = source / "secret-content.md"
        secret_content.write_text(
            "# PRIVATE_REJECTED_TITLE\n"
            "Authorization: Bearer PRIVATE_BEARER_VALUE_123456789\n",
            encoding="utf-8",
        )
        log_file = source / "debug.log"
        log_file.write_text("PRIVATE_LOG_CONTENT\n", encoding="utf-8")

        app_data = source / ".obsidian"
        app_data.mkdir()
        (app_data / "workspace.json").write_text(
            "PRIVATE_APP_DATA", encoding="utf-8"
        )
        nested_git = source / "nested-repository"
        (nested_git / ".git").mkdir(parents=True)
        (nested_git / ".git" / "HEAD").write_text(
            "ref: refs/heads/main\n", encoding="utf-8"
        )
        (nested_git / "private-note.md").write_text(
            "# PRIVATE_NESTED_TITLE\n", encoding="utf-8"
        )

        outside_target = self.root / "PRIVATE_SYMLINK_TARGET.md"
        outside_target.write_text(
            "# PRIVATE_SYMLINK_TITLE\n", encoding="utf-8"
        )
        (source / "escaped-link.md").symlink_to(outside_target)
        hardlink_one = source / "hardlink-one.md"
        hardlink_two = source / "hardlink-two.md"
        hardlink_one.write_text("# PRIVATE_HARDLINK_TITLE\n", encoding="utf-8")
        os.link(hardlink_one, hardlink_two)

        before = self.tree_snapshot(source)
        completed = self.run_migrate(
            "inventory", "--source", str(source)
        )
        inventory = self.assert_canonical_output(completed)
        self.assertLess(len(completed.stdout.encode("utf-8")), 50_000)
        self.assertEqual(set(inventory), INVENTORY_KEYS)

        eligible = [
            entry for entry in inventory["entries"] if entry["status"] == "eligible"
        ]
        rejected = [
            entry for entry in inventory["entries"] if entry["status"] == "rejected"
        ]
        self.assertEqual(
            {entry["path"] for entry in eligible},
            {"ordinary.md", "plain.txt", "boundary.txt"},
        )
        self.assertTrue(all(set(entry) == ELIGIBLE_ENTRY_KEYS for entry in eligible))
        self.assertTrue(all(entry["type"] == "text" for entry in eligible))
        boundary_entry = next(
            entry for entry in eligible if entry["path"] == "boundary.txt"
        )
        self.assertEqual(boundary_entry["bytes"], MAX_TEXT_BYTES - 1)

        self.assertTrue(rejected)
        self.assertTrue(all(set(entry) == REJECTED_ENTRY_KEYS for entry in rejected))
        self.assertTrue(
            all(entry["type"] in {"file", "directory"} for entry in rejected)
        )
        reasons = {entry["reason"] for entry in rejected}
        self.assertTrue(
            {
                "too_large",
                "invalid_utf8",
                "nul_byte",
                "secret_name",
                "likely_secret",
                "app_data",
                "log_file",
                "nested_git_repository",
                "symlink",
                "hard_link",
            }.issubset(reasons),
            reasons,
        )
        self.assertEqual(set(inventory["summary"]), INVENTORY_SUMMARY_KEYS)
        self.assertEqual(inventory["summary"]["eligible_files"], 3)
        self.assertEqual(
            inventory["summary"]["eligible_bytes"],
            ordinary.stat().st_size + plain.stat().st_size + boundary.stat().st_size,
        )
        self.assertEqual(
            inventory["summary"]["rejected_entries"], len(rejected)
        )
        for private_fragment in (
            "PRIVATE_INVALID_UTF8",
            "PRIVATE_NUL_CONTENT",
            "PRIVATE_ENV_CONTENT",
            "PRIVATE_REJECTED_TITLE",
            "PRIVATE_BEARER_VALUE",
            "PRIVATE_LOG_CONTENT",
            "PRIVATE_APP_DATA",
            "PRIVATE_NESTED_TITLE",
            "PRIVATE_SYMLINK_TITLE",
            "PRIVATE_HARDLINK_TITLE",
            "PRIVATE_COMMENTED_NETRC_SECRET",
            "PRIVATE_LONG_COMMENT_NETRC_SECRET",
            "PRIVATE_QUOTED_JSON_SECRET",
        ):
            self.assertNotIn(private_fragment, completed.stdout)
            self.assertNotIn(private_fragment, completed.stderr)
        self.assertEqual(self.tree_snapshot(source), before)

    def test_plan_maps_eligible_text_with_stable_collisions_and_approval_hash(self) -> None:
        source_a = self.external / "a" / "Shared Notes"
        source_b = self.external / "b" / "Shared Notes"
        source_c = self.external / "c" / "ＳＨＡＲＥＤ ＮＯＴＥＳ"
        source_d = self.external / "d" / "Unsafe: Notes"
        for source in (source_a, source_b, source_c, source_d):
            source.mkdir(parents=True)

        for name in ("Topic.md", "topic.md", "Ｔｏｐｉｃ.md"):
            (source_a / name).write_text(
                f"# {Path(name).stem}\n\nPublic-safe body.\n",
                encoding="utf-8",
            )
        (source_b / "note.md").write_text("# B\n", encoding="utf-8")
        (source_c / "note.md").write_text("# C\n", encoding="utf-8")
        (source_d / "note.md").write_text("# D\n", encoding="utf-8")
        (source_d / ".env").write_text(
            "PASSWORD=<redacted>", encoding="utf-8"
        )
        sources = (source_a, source_b, source_c, source_d)
        source_before = {
            str(source): self.tree_snapshot(source) for source in sources
        }
        vault_before = self.tree_snapshot(self.repo / "second-brain")

        inventory_result = self.run_migrate(
            "inventory",
            *(argument for source in reversed(sources) for argument in ("--source", str(source))),
        )
        inventory = self.assert_canonical_output(inventory_result)
        inventory_path = self.outputs / "inventory.json"
        inventory_path.write_text(inventory_result.stdout, encoding="utf-8")

        first = self.run_migrate(
            "plan", "--inventory", str(inventory_path)
        )
        second = self.run_migrate(
            "plan", "--inventory", str(inventory_path)
        )
        plan = self.assert_canonical_output(first)
        self.assertEqual(first.stdout, second.stdout)

        self.assertEqual(set(plan), PLAN_KEYS)
        self.assertEqual(plan["schema_version"], 1)
        self.assertEqual(plan["command"], "migrate plan")
        self.assertEqual(plan["date"], "2026-07-14")
        expected_inventory_hash = hashlib.sha256(
            self.canonical_json(inventory).encode("utf-8")
        ).hexdigest()
        self.assertEqual(plan["inventory_sha256"], expected_inventory_hash)
        self.assertEqual(plan["sources"], inventory["sources"])

        self.assertTrue(
            all(set(mapping) == PLAN_MAPPING_KEYS for mapping in plan["mappings"])
        )
        self.assertEqual(len(plan["mappings"]), len(sources))
        mapping_by_source = {
            mapping["source_id"]: mapping["target"]
            for mapping in plan["mappings"]
        }
        self.assertTrue(
            all(
                mapping["reason"] == "safe_archive_default"
                for mapping in plan["mappings"]
            )
        )
        for destination in mapping_by_source.values():
            parts = Path(destination).parts
            self.assertEqual(parts[:2], ("06 Archive", "Imports"))
            self.assertEqual(len(parts), 3)
            self.assertNotIn(Path(destination).name, {"", ".", ".."})
            self.assertFalse(Path(destination).is_absolute())
        colliding_source_ids = [
            self.source_id(inventory, source)
            for source in (source_a, source_b, source_c)
        ]
        self.assertEqual(
            {
                self.normalized_name(mapping_by_source[source_id])
                for source_id in colliding_source_ids
            },
            {"shared notes", "shared notes 2", "shared notes 3"},
        )
        unsafe_source_id = self.source_id(inventory, source_d)
        self.assertNotIn(":", mapping_by_source[unsafe_source_id])

        self.assertEqual(len(plan["entries"]), 6)
        self.assertTrue(
            all(set(entry) == PLAN_ENTRY_KEYS for entry in plan["entries"])
        )
        self.assertEqual(
            len({entry["entry_id"] for entry in plan["entries"]}),
            len(plan["entries"]),
        )
        inventory_eligible = {
            (entry["source_id"], entry["path"]): entry
            for entry in inventory["entries"]
            if entry["status"] == "eligible"
        }
        self.assertEqual(
            {
                (entry["source_id"], Path(entry["source_path"]).name)
                for entry in plan["entries"]
            },
            {
                (source_id, Path(relative).name)
                for source_id, relative in inventory_eligible
            },
        )
        for entry in plan["entries"]:
            source_record = next(
                source
                for source in inventory["sources"]
                if source["id"] == entry["source_id"]
            )
            source_path = Path(entry["source_path"])
            self.assertFalse(source_path.is_absolute())
            self.assertNotIn("..", source_path.parts)
            self.assertEqual(
                (Path(source_record["path"]) / source_path).resolve().parent,
                Path(source_record["path"]),
            )
            inventory_entry = inventory_eligible[
                (entry["source_id"], source_path.as_posix())
            ]
            self.assertEqual(entry["source_bytes"], inventory_entry["bytes"])
            self.assertEqual(entry["source_sha256"], inventory_entry["sha256"])
            self.assertRegex(entry["destination_sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(
                entry["destination"].startswith(
                    mapping_by_source[entry["source_id"]] + "/"
                )
            )
        source_a_id = self.source_id(inventory, source_a)
        collision_destinations = {
            self.normalized_name(entry["destination"])
            for entry in plan["entries"]
            if entry["source_id"] == source_a_id
        }
        self.assertEqual(
            collision_destinations,
            {"topic.md", "topic 2.md", "topic 3.md"},
        )

        self.assertEqual(set(plan["summary"]), PLAN_SUMMARY_KEYS)
        self.assertEqual(plan["summary"]["files"], 6)
        self.assertEqual(
            plan["summary"]["source_bytes"],
            sum(entry["bytes"] for entry in inventory_eligible.values()),
        )
        unsigned_plan = dict(plan)
        approval_sha256 = unsigned_plan.pop("approval_sha256")
        self.assertEqual(
            approval_sha256,
            hashlib.sha256(
                self.canonical_json(unsigned_plan).encode("utf-8")
            ).hexdigest(),
        )
        self.assertNotIn("PRIVATE_PLAN_REJECTION", first.stdout)
        self.assertEqual(
            source_before,
            {str(source): self.tree_snapshot(source) for source in sources},
        )
        self.assertEqual(
            self.tree_snapshot(self.repo / "second-brain"), vault_before
        )

    def test_plan_rechecks_source_policy_after_inventory_tampering(self) -> None:
        cases = {
            "secret-name": ".env",
            "log-file": "debug.log",
            "app-data": ".obsidian/private.md",
            "nested-git": "nested/private.md",
        }
        vault_before = self.tree_snapshot(self.repo / "second-brain")
        for label, relative in cases.items():
            with self.subTest(label=label):
                source = self.external / label
                source_file = source / relative
                source_file.parent.mkdir(parents=True)
                source_file.write_text(
                    "# Public-looking\n\nSAFE_TEXT_ONLY\n",
                    encoding="utf-8",
                )
                if label == "nested-git":
                    (source / "nested" / ".git").mkdir()
                content = source_file.read_bytes()
                inventory = {
                    "schema_version": 1,
                    "command": "migrate inventory",
                    "sources": [
                        {
                            "id": "source-001",
                            "path": str(source.resolve()),
                        }
                    ],
                    "entries": [
                        {
                            "source_id": "source-001",
                            "path": relative,
                            "type": "text",
                            "status": "eligible",
                            "bytes": len(content),
                            "sha256": hashlib.sha256(content).hexdigest(),
                            "title": "Public-looking",
                        }
                    ],
                    "summary": {
                        "eligible_files": 1,
                        "eligible_bytes": len(content),
                        "rejected_entries": 0,
                    },
                }
                inventory_path = self.outputs / f"{label}.json"
                inventory_path.write_text(
                    self.canonical_json(inventory) + "\n",
                    encoding="utf-8",
                )

                completed = self.run_migrate(
                    "plan",
                    "--inventory",
                    str(inventory_path),
                )

                self.assertEqual(completed.returncode, 2, completed.stderr)
                self.assertIn("source", completed.stderr.lower())
                self.assertNotIn("SAFE_TEXT_ONLY", completed.stderr)
                self.assertNotIn(relative, completed.stderr)
                self.assertNotIn("Traceback", completed.stderr)
                self.assertEqual(
                    self.tree_snapshot(self.repo / "second-brain"),
                    vault_before,
                )

    def test_plan_rejects_noncanonical_inventory_entry_path(self) -> None:
        source = self.external / "canonical-inventory"
        source.mkdir()
        (source / "note.md").write_text("# Safe\n", encoding="utf-8")
        inventory_result = self.run_migrate(
            "inventory",
            "--source",
            str(source),
        )
        inventory = self.assert_canonical_output(inventory_result)
        inventory["entries"][0]["path"] = "./note.md"
        inventory_path = self.outputs / "noncanonical-inventory.json"
        inventory_path.write_text(
            self.canonical_json(inventory) + "\n",
            encoding="utf-8",
        )

        completed = self.run_migrate(
            "plan",
            "--inventory",
            str(inventory_path),
        )

        self.assertEqual(completed.returncode, 2)
        self.assertIn("inventory", completed.stderr.lower())
        self.assertEqual(completed.stdout, "")


if __name__ == "__main__":
    unittest.main()
