#!/usr/bin/env python3

import hashlib
import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "executable_second-brain"
SOURCE_VAULT = REPO_ROOT / "second-brain"
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def preview_approval(preview: dict[str, object]) -> str:
    unsigned = dict(preview)
    unsigned.pop("approval_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def append_block(original: bytes, block: str) -> bytes:
    encoded = block.encode("utf-8")
    if not encoded.endswith(b"\n"):
        encoded += b"\n"
    if original.endswith(b"\n\n"):
        separator = b""
    elif original.endswith(b"\n"):
        separator = b"\n"
    else:
        separator = b"\n\n"
    return original + separator + encoded


class SecondBrainUpgradeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        (self.repo / ".git").mkdir()
        shutil.copytree(SOURCE_VAULT, self.repo / "second-brain")
        self.outside = self.root / "outside"
        self.outside.mkdir()
        self.state_home = self.root / "state"
        self.env = {
            **os.environ,
            "HOME": str(self.root / "home"),
            "XDG_STATE_HOME": str(self.state_home),
            "SECOND_BRAIN_REPO_ROOT": str(self.repo),
            "SECOND_BRAIN_NOW": "2026-07-14T09:30:00-04:00",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        Path(self.env["HOME"]).mkdir()
        self.privacy_relative = "00 Context/Audience and Privacy.md"
        self.privacy_path = self.repo / "second-brain" / self.privacy_relative
        self.safety_relative = "00 Context/Safety Checklist.md"
        self.safety_path = self.repo / "second-brain" / self.safety_relative
        self.unrelated = self.repo / "second-brain" / "04 Resources" / "User Note.md"
        self.unrelated.write_text(
            "# User-owned note\n\nUNRELATED_USER_CONTENT\n",
            encoding="utf-8",
        )
        self.privacy_block = (
            "<!-- second-brain:upgrade:privacy-v2 -->\n\n"
            "## Privacy v2 safety rule\n\n"
            "Never promote private raw session text into tracked notes.\n"
        )
        self.safety_content = (
            "---\n"
            "tags: [context, safety]\n"
            "date: 2026-07-14\n"
            "visibility: public-sanitized\n"
            "---\n\n"
            "# Safety Checklist\n\n"
            "<!-- second-brain:upgrade:safety-template-v1 -->\n\n"
            "- Confirm tracked content is sanitized.\n"
        )

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
    def tree_snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
        snapshot: dict[str, tuple[bytes, int]] = {}
        if not root.exists():
            return snapshot
        for path in sorted(root.rglob("*")):
            if path.is_file() and not path.is_symlink():
                snapshot[path.relative_to(root).as_posix()] = (
                    path.read_bytes(),
                    path.stat().st_mtime_ns,
                )
        return snapshot

    def require_upgrade_module(self) -> ModuleType:
        try:
            return importlib.import_module("second_brain.upgrade")
        except ModuleNotFoundError as error:
            self.fail(
                "scripts/second_brain/upgrade.py is required for protected "
                f"upgrade contracts: {error}"
            )
        raise AssertionError("unreachable")

    def specs(self, upgrade: ModuleType) -> tuple[object, object]:
        return (
            upgrade.UpgradeSpec(
                id="privacy-v2",
                path=self.privacy_relative,
                reason="add privacy-v2 safety rule",
                create_content=self.privacy_block,
                append_block=self.privacy_block,
            ),
            upgrade.UpgradeSpec(
                id="safety-template-v1",
                path=self.safety_relative,
                reason="add missing safety checklist template",
                create_content=self.safety_content,
                append_block=(
                    "<!-- second-brain:upgrade:safety-template-v1 -->\n\n"
                    "- Confirm tracked content is sanitized.\n"
                ),
            ),
        )

    def call_preview(self, upgrade: ModuleType, specs: tuple[object, ...]) -> dict:
        with mock.patch.dict(os.environ, self.env, clear=True):
            return upgrade.build_upgrade_preview(specs)

    def call_apply(
        self,
        upgrade: ModuleType,
        specs: tuple[object, ...],
        approval_sha256: str,
    ) -> dict:
        with mock.patch.dict(os.environ, self.env, clear=True):
            return upgrade.apply_upgrade(specs, approval_sha256)

    def test_help_exposes_protected_upgrade_command(self) -> None:
        completed = self.run_command("--help")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("upgrade", completed.stdout)

    def test_dry_preview_is_deterministic_and_does_not_change_protected_files(
        self,
    ) -> None:
        upgrade = self.require_upgrade_module()
        specs = self.specs(upgrade)
        before = self.tree_snapshot(self.repo)
        privacy_before = self.privacy_path.read_bytes()
        expected_privacy = append_block(privacy_before, self.privacy_block)

        first = self.call_preview(upgrade, specs)
        second = self.call_preview(upgrade, specs)

        self.assertEqual(first, second)
        self.assertEqual(first["schema_version"], 1)
        self.assertEqual(first["command"], "upgrade")
        self.assertEqual(first["mode"], "dry-run")
        self.assertEqual(first["date"], "2026-07-14")
        self.assertEqual(first["summary"], {"create": 1, "update": 1})
        self.assertEqual(
            [operation["path"] for operation in first["operations"]],
            sorted((self.privacy_relative, self.safety_relative)),
        )
        operations = {operation["id"]: operation for operation in first["operations"]}
        self.assertEqual(
            operations["privacy-v2"],
            {
                "id": "privacy-v2",
                "path": self.privacy_relative,
                "action": "update",
                "reason": "add privacy-v2 safety rule",
                "protected": True,
                "backup": (
                    "06 Archive/backups/2026-07-14/"
                    "00 Context/Audience and Privacy.md"
                ),
                "before_sha256": sha256_bytes(privacy_before),
                "after_sha256": sha256_bytes(expected_privacy),
            },
        )
        self.assertEqual(
            operations["safety-template-v1"],
            {
                "id": "safety-template-v1",
                "path": self.safety_relative,
                "action": "create",
                "reason": "add missing safety checklist template",
                "protected": False,
                "backup": None,
                "before_sha256": None,
                "after_sha256": sha256_bytes(self.safety_content.encode("utf-8")),
            },
        )
        self.assertEqual(first["approval_sha256"], preview_approval(first))
        self.assertEqual(self.tree_snapshot(self.repo), before)
        self.assertFalse(self.safety_path.exists())

    def test_apply_rejects_wrong_or_stale_approval_before_any_change(self) -> None:
        upgrade = self.require_upgrade_module()
        specs = self.specs(upgrade)
        before = self.tree_snapshot(self.repo)

        with self.assertRaises(upgrade.UpgradeError) as wrong_context:
            self.call_apply(upgrade, specs, "0" * 64)
        self.assertIn("approval", str(wrong_context.exception).lower())
        self.assertEqual(self.tree_snapshot(self.repo), before)

        preview = self.call_preview(upgrade, specs)
        self.privacy_path.write_text(
            self.privacy_path.read_text(encoding="utf-8")
            + "\nPRIVATE_CHANGE_AFTER_PREVIEW\n",
            encoding="utf-8",
        )
        stale_before = self.tree_snapshot(self.repo)
        with self.assertRaises(upgrade.UpgradeError) as stale_context:
            self.call_apply(upgrade, specs, preview["approval_sha256"])
        self.assertIn("approval", str(stale_context.exception).lower())
        self.assertNotIn("PRIVATE_CHANGE_AFTER_PREVIEW", str(stale_context.exception))
        self.assertEqual(self.tree_snapshot(self.repo), stale_before)
        self.assertFalse(self.safety_path.exists())

    def test_approved_upgrade_creates_missing_file_updates_with_marker_and_backs_up(
        self,
    ) -> None:
        upgrade = self.require_upgrade_module()
        specs = self.specs(upgrade)
        privacy_before = self.privacy_path.read_bytes()
        unrelated_before = self.unrelated.read_bytes()
        preview = self.call_preview(upgrade, specs)

        result = self.call_apply(upgrade, specs, preview["approval_sha256"])

        self.assertEqual(
            result,
            {
                "schema_version": 1,
                "command": "upgrade",
                "result": "updated",
                "created": 1,
                "updated": 1,
                "backups": 1,
            },
        )
        self.assertEqual(
            self.privacy_path.read_bytes(),
            append_block(privacy_before, self.privacy_block),
        )
        self.assertEqual(self.privacy_path.read_text(encoding="utf-8").count(
            "<!-- second-brain:upgrade:privacy-v2 -->"
        ), 1)
        self.assertEqual(
            self.safety_path.read_text(encoding="utf-8"),
            self.safety_content,
        )
        backup = (
            self.repo
            / "second-brain"
            / "06 Archive"
            / "backups"
            / "2026-07-14"
            / "00 Context"
            / "Audience and Privacy.md"
        )
        self.assertEqual(backup.read_bytes(), privacy_before)
        self.assertEqual(self.unrelated.read_bytes(), unrelated_before)

    def test_dated_backup_collision_uses_suffix_without_overwrite(self) -> None:
        upgrade = self.require_upgrade_module()
        privacy_spec = (self.specs(upgrade)[0],)
        backup = (
            self.repo
            / "second-brain"
            / "06 Archive"
            / "backups"
            / "2026-07-14"
            / "00 Context"
            / "Audience and Privacy.md"
        )
        backup.parent.mkdir(parents=True)
        backup.write_bytes(b"EXISTING_BACKUP_SENTINEL\n")
        privacy_before = self.privacy_path.read_bytes()
        unrelated_before = self.unrelated.read_bytes()
        preview = self.call_preview(upgrade, privacy_spec)

        result = self.call_apply(
            upgrade,
            privacy_spec,
            preview["approval_sha256"],
        )

        self.assertEqual(result["result"], "updated")
        self.assertEqual(backup.read_bytes(), b"EXISTING_BACKUP_SENTINEL\n")
        suffixed = backup.with_name("Audience and Privacy 2.md")
        self.assertEqual(suffixed.read_bytes(), privacy_before)
        self.assertEqual(self.unrelated.read_bytes(), unrelated_before)

    def test_backup_symlink_is_rejected_without_touching_protected_or_outside_files(
        self,
    ) -> None:
        upgrade = self.require_upgrade_module()
        privacy_spec = (self.specs(upgrade)[0],)
        backups = self.repo / "second-brain" / "06 Archive" / "backups"
        dated = backups / "2026-07-14"
        outside_backup = self.root / "outside-backup"
        outside_backup.mkdir()
        outside_sentinel = outside_backup / "DO_NOT_TOUCH"
        outside_sentinel.write_bytes(b"OUTSIDE_BACKUP_SENTINEL\n")
        dated.symlink_to(outside_backup, target_is_directory=True)
        privacy_before = self.privacy_path.read_bytes()
        unrelated_before = self.unrelated.read_bytes()
        outside_before = self.tree_snapshot(outside_backup)
        preview = self.call_preview(upgrade, privacy_spec)

        with self.assertRaises(upgrade.UpgradeError) as context:
            self.call_apply(upgrade, privacy_spec, preview["approval_sha256"])

        self.assertIn("backup", str(context.exception).lower())
        self.assertEqual(self.privacy_path.read_bytes(), privacy_before)
        self.assertEqual(self.unrelated.read_bytes(), unrelated_before)
        self.assertEqual(self.tree_snapshot(outside_backup), outside_before)

    def test_create_race_never_overwrites_late_target(self) -> None:
        upgrade = self.require_upgrade_module()
        create_spec = (self.specs(upgrade)[1],)
        preview = self.call_preview(upgrade, create_spec)
        real_atomic_create = upgrade.atomic_create

        def inject_late_target(root, target, content, mode=0o644):
            if target == self.safety_path:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"LATE_TARGET_SENTINEL\n")
            return real_atomic_create(root, target, content, mode)

        with mock.patch.object(
            upgrade,
            "atomic_create",
            side_effect=inject_late_target,
        ):
            with self.assertRaises(upgrade.UpgradeError) as context:
                self.call_apply(
                    upgrade,
                    create_spec,
                    preview["approval_sha256"],
                )

        self.assertIn("target", str(context.exception).lower())
        self.assertEqual(self.safety_path.read_bytes(), b"LATE_TARGET_SENTINEL\n")

    def test_backup_race_uses_suffix_without_overwriting_late_file(self) -> None:
        upgrade = self.require_upgrade_module()
        privacy_spec = (self.specs(upgrade)[0],)
        privacy_before = self.privacy_path.read_bytes()
        preview = self.call_preview(upgrade, privacy_spec)
        expected_backup = (
            self.repo
            / "second-brain"
            / "06 Archive"
            / "backups"
            / "2026-07-14"
            / "00 Context"
            / "Audience and Privacy.md"
        )
        real_atomic_create = upgrade.atomic_create
        injected = False

        def inject_late_backup(root, target, content, mode=0o644):
            nonlocal injected
            if target == expected_backup and not injected:
                injected = True
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"LATE_BACKUP_SENTINEL\n")
            return real_atomic_create(root, target, content, mode)

        with mock.patch.object(
            upgrade,
            "atomic_create",
            side_effect=inject_late_backup,
        ):
            result = self.call_apply(
                upgrade,
                privacy_spec,
                preview["approval_sha256"],
            )

        self.assertEqual(result["result"], "updated")
        self.assertEqual(expected_backup.read_bytes(), b"LATE_BACKUP_SENTINEL\n")
        suffixed = expected_backup.with_name("Audience and Privacy 2.md")
        self.assertEqual(suffixed.read_bytes(), privacy_before)

    def test_successful_upgrade_rerun_is_noop_without_rewriting_any_file(self) -> None:
        upgrade = self.require_upgrade_module()
        specs = self.specs(upgrade)
        initial = self.call_preview(upgrade, specs)
        first = self.call_apply(upgrade, specs, initial["approval_sha256"])
        self.assertEqual(first["result"], "updated")
        before = self.tree_snapshot(self.repo)

        repeated_preview = self.call_preview(upgrade, specs)
        self.assertEqual(repeated_preview["operations"], [])
        self.assertEqual(repeated_preview["summary"], {"create": 0, "update": 0})
        repeated = self.call_apply(
            upgrade,
            specs,
            repeated_preview["approval_sha256"],
        )

        self.assertEqual(
            repeated,
            {
                "schema_version": 1,
                "command": "upgrade",
                "result": "noop",
                "created": 0,
                "updated": 0,
                "backups": 0,
            },
        )
        self.assertEqual(self.tree_snapshot(self.repo), before)
        self.assertEqual(
            self.unrelated.read_text(encoding="utf-8"),
            "# User-owned note\n\nUNRELATED_USER_CONTENT\n",
        )


if __name__ == "__main__":
    unittest.main()
