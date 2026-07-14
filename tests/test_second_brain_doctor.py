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
SCRIPTS_ROOT = REPO_ROOT / "scripts"
SCRIPT = REPO_ROOT / "scripts" / "executable_second-brain"
PACKAGE = REPO_ROOT / "scripts" / "second_brain"
SOURCE_VAULT = REPO_ROOT / "second-brain"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

TOP_LEVEL_KEYS = ["command", "findings", "schema_version", "summary"]
SUMMARY_KEYS = ["errors", "status", "warnings"]
FINDING_KEYS = ["code", "details", "key", "locations", "message", "severity"]
LOCATION_KEYS = ["line", "path"]

CANONICAL_LESSON = (
    "A canonical engineering lesson stays in tasks/lessons.md so every future "
    "session can find one authoritative record. The curated vault may link to "
    "that owner, but it must not copy this complete paragraph into a Second "
    "Brain note because parallel copies drift and create conflicting guidance."
)


def tree_snapshot(root: Path) -> dict[str, tuple[int, str | bytes]]:
    snapshot: dict[str, tuple[int, str | bytes]] = {}
    for directory, directory_names, file_names in os.walk(
        root, followlinks=False
    ):
        parent = Path(directory)
        for name in sorted((*directory_names, *file_names)):
            path = parent / name
            relative = path.relative_to(root).as_posix()
            metadata = path.lstat()
            mode = stat.S_IFMT(metadata.st_mode) | stat.S_IMODE(metadata.st_mode)
            if path.is_symlink():
                content: str | bytes = os.readlink(path)
            elif path.is_file():
                content = path.read_bytes()
            else:
                content = b""
            snapshot[relative] = (mode, content)
    return snapshot


class SecondBrainDoctorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        subprocess.run(
            ["git", "init", "--quiet"],
            cwd=self.repo,
            check=True,
            capture_output=True,
            text=True,
        )

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

        lessons = self.repo / "tasks" / "lessons.md"
        lessons.parent.mkdir()
        lessons.write_text(
            f"# Lessons\n\n{CANONICAL_LESSON}\n",
            encoding="utf-8",
        )
        feedback = (
            self.repo
            / "dot_agents"
            / "skills"
            / "feedback-memory"
            / "feedback.log"
        )
        feedback.parent.mkdir(parents=True)
        feedback.write_text(
            "Keep durable workflow preferences in this canonical fixture.\n",
            encoding="utf-8",
        )
        (self.repo / "plans").mkdir()

        self.home = self.root / "home"
        self.home.mkdir()
        self.state_home = self.root / "state"
        self.outside = self.root / "outside"
        self.outside.mkdir()
        self.env = {
            **os.environ,
            "HOME": str(self.home),
            "XDG_STATE_HOME": str(self.state_home),
            "SECOND_BRAIN_REPO_ROOT": str(self.repo),
            "SECOND_BRAIN_NOW": "2026-07-14T09:30:00-04:00",
            "PYTHONDONTWRITEBYTECODE": "1",
        }

    def run_command(
        self,
        *arguments: str,
        expected_returncode: int,
    ) -> subprocess.CompletedProcess[str]:
        before = tree_snapshot(self.root)
        completed = subprocess.run(
            [sys.executable, "-B", str(self.script), *arguments],
            cwd=self.outside,
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            completed.returncode,
            expected_returncode,
            "unexpected doctor exit\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}",
        )
        self.assertEqual(
            tree_snapshot(self.root),
            before,
            "doctor must not modify the repository, vault, or private state",
        )
        return completed

    def json_report(
        self,
        *arguments: str,
        expected_returncode: int = 0,
    ) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
        completed = self.run_command(
            "doctor",
            "--format",
            "json",
            *arguments,
            expected_returncode=expected_returncode,
        )
        self.assertEqual(completed.stderr, "")
        report = json.loads(completed.stdout)
        self.assert_report_contract(report)
        return completed, report

    def assert_report_contract(self, report: dict[str, object]) -> None:
        self.assertEqual(list(report), TOP_LEVEL_KEYS)
        self.assertEqual(report["schema_version"], 1)
        self.assertEqual(report["command"], "doctor")

        summary = report["summary"]
        self.assertIsInstance(summary, dict)
        self.assertEqual(list(summary), SUMMARY_KEYS)

        findings = report["findings"]
        self.assertIsInstance(findings, list)
        finding_keys: list[str] = []
        for finding in findings:
            self.assertIsInstance(finding, dict)
            self.assertEqual(list(finding), FINDING_KEYS)
            self.assertIn(finding["severity"], ("error", "warning"))
            self.assertIsInstance(finding["message"], str)
            self.assertTrue(finding["message"])
            self.assertIsInstance(finding["details"], dict)
            self.assertEqual(
                list(finding["details"]), sorted(finding["details"])
            )
            self.assertIsInstance(finding["locations"], list)
            normalized_locations: list[tuple[str, int]] = []
            for location in finding["locations"]:
                self.assertIsInstance(location, dict)
                self.assertEqual(list(location), LOCATION_KEYS)
                self.assertIsInstance(location["path"], str)
                self.assertFalse(Path(location["path"]).is_absolute())
                self.assertIsInstance(location["line"], int)
                self.assertGreaterEqual(location["line"], 1)
                normalized_locations.append(
                    (location["path"], location["line"])
                )
            self.assertEqual(normalized_locations, sorted(normalized_locations))
            finding_keys.append(finding["key"])

        self.assertEqual(finding_keys, sorted(finding_keys))
        errors = sum(
            finding["severity"] == "error" for finding in findings
        )
        warnings = sum(
            finding["severity"] == "warning" for finding in findings
        )
        expected_status = "error" if errors else "warning" if warnings else "pass"
        self.assertEqual(
            summary,
            {
                "errors": errors,
                "status": expected_status,
                "warnings": warnings,
            },
        )
        self.assertNotIn(str(self.root), json.dumps(report, sort_keys=True))

    def assert_single_finding(
        self,
        report: dict[str, object],
        *,
        code: str,
        key: str,
        severity: str,
        paths: set[str],
    ) -> dict[str, object]:
        self.assertEqual(len(report["findings"]), 1)
        finding = report["findings"][0]
        self.assertEqual(finding["code"], code)
        self.assertEqual(finding["key"], key)
        self.assertEqual(finding["severity"], severity)
        self.assertEqual(
            {location["path"] for location in finding["locations"]},
            paths,
        )
        return finding

    def append_to_note(self, relative_path: str, content: str) -> None:
        path = self.repo / "second-brain" / relative_path
        path.write_text(
            path.read_text(encoding="utf-8") + f"\n{content}\n",
            encoding="utf-8",
        )

    def write_import(self, name: str, content: str) -> Path:
        path = (
            self.repo
            / "second-brain"
            / "06 Archive"
            / "Imports"
            / "fixture-source"
            / name
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    @staticmethod
    def import_note(
        body: str,
        *,
        visibility: str = "public-sanitized",
        include_source_sha256: bool = True,
        source_sha256: str | None = None,
    ) -> str:
        body_text = f"{body}\n"
        digest = source_sha256 or hashlib.sha256(
            body_text.encode("utf-8")
        ).hexdigest()
        source_field = (
            f"source_sha256: {digest}\n" if include_source_sha256 else ""
        )
        return (
            "---\n"
            "tags: [archive, imported]\n"
            "status: archived\n"
            "date: 2026-07-14\n"
            f"visibility: {visibility}\n"
            f"{source_field}"
            "---\n\n"
            f"{body_text}"
        )

    def test_untouched_vault_passes_with_repeatable_sorted_json(self) -> None:
        first, first_report = self.json_report()
        second, second_report = self.json_report()
        checked, checked_report = self.json_report(
            "--check", expected_returncode=0
        )

        self.assertEqual(first_report["findings"], [])
        self.assertEqual(
            first_report["summary"],
            {"errors": 0, "status": "pass", "warnings": 0},
        )
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first.stdout, checked.stdout)
        self.assertEqual(first_report, second_report)
        self.assertEqual(first_report, checked_report)

    def test_multiple_findings_are_sorted_by_stable_key(self) -> None:
        missing = self.repo / "second-brain" / "00 Context" / "Memory Map.md"
        missing.unlink()
        self.append_to_note(
            "04 Resources/Linux Automation.md",
            "{{PRIVATE_SORTING_PLACEHOLDER_MUST_NOT_LEAK}}",
        )

        first, report = self.json_report()
        second, repeated_report = self.json_report()

        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(report, repeated_report)
        self.assertEqual(
            [finding["key"] for finding in report["findings"]],
            [
                "missing_required_path:00 Context/Memory Map.md",
                "unresolved_placeholder:04 Resources/Linux Automation.md",
            ],
        )
        self.assertEqual(
            report["summary"],
            {"errors": 1, "status": "error", "warnings": 1},
        )
        self.assertNotIn("PRIVATE_SORTING_PLACEHOLDER", first.stdout)

    def test_missing_required_path_is_an_error_and_check_controls_exit(self) -> None:
        missing = self.repo / "second-brain" / "00 Context" / "Memory Map.md"
        missing.unlink()

        unchecked, report = self.json_report()
        checked, checked_report = self.json_report(
            "--check", expected_returncode=1
        )

        self.assertEqual(unchecked.stdout, checked.stdout)
        self.assertEqual(report, checked_report)
        self.assert_single_finding(
            report,
            code="missing_required_path",
            key="missing_required_path:00 Context/Memory Map.md",
            severity="error",
            paths={"second-brain/00 Context/Memory Map.md"},
        )

    def test_malformed_frontmatter_reports_one_non_cascading_error(self) -> None:
        about = self.repo / "second-brain" / "00 Context" / "About Me.md"
        content = about.read_text(encoding="utf-8")
        about.write_text(
            content.replace("\n---\n\n# About Me", "\n--\n\n# About Me", 1),
            encoding="utf-8",
        )

        _, report = self.json_report()
        self.assert_single_finding(
            report,
            code="malformed_frontmatter",
            key="malformed_frontmatter:00 Context/About Me.md",
            severity="error",
            paths={"second-brain/00 Context/About Me.md"},
        )

    def test_placeholder_warning_is_safe_and_does_not_fail_check(self) -> None:
        private_placeholder = "{{PRIVATE_PLACEHOLDER_CONTEXT_MUST_NOT_LEAK}}"
        self.append_to_note(
            "04 Resources/Linux Automation.md", private_placeholder
        )

        completed, report = self.json_report("--check", expected_returncode=0)
        self.assert_single_finding(
            report,
            code="unresolved_placeholder",
            key="unresolved_placeholder:04 Resources/Linux Automation.md",
            severity="warning",
            paths={"second-brain/04 Resources/Linux Automation.md"},
        )
        self.assertNotIn(private_placeholder, completed.stdout)

    def test_unsafe_visibility_is_an_error(self) -> None:
        relationship = (
            self.repo / "second-brain" / "03 Areas" / "Relationship.md"
        )
        content = relationship.read_text(encoding="utf-8")
        relationship.write_text(
            content.replace(
                "visibility: public-sanitized",
                "visibility: private",
                1,
            ),
            encoding="utf-8",
        )

        _, report = self.json_report()
        self.assert_single_finding(
            report,
            code="unsafe_visibility",
            key="unsafe_visibility:03 Areas/Relationship.md",
            severity="error",
            paths={"second-brain/03 Areas/Relationship.md"},
        )

    def test_likely_secret_is_reported_without_leaking_secret_content(self) -> None:
        secret = "api_key=<redacted>"
        self.append_to_note("00 Context/Learnings.md", secret)

        completed, report = self.json_report()
        self.assert_single_finding(
            report,
            code="likely_secret",
            key="likely_secret:00 Context/Learnings.md",
            severity="error",
            paths={"second-brain/00 Context/Learnings.md"},
        )
        self.assertNotIn(secret, completed.stdout)
        self.assertNotIn("DOCTOR_PRIVATE_SECRET", completed.stdout)

    def test_non_markdown_netrc_is_reported_without_leaking_content(self) -> None:
        secret = "DOCTOR_PRIVATE_NETRC_SECRET_MUST_NOT_LEAK"
        target = self.repo / "second-brain" / "00 Context" / ".netrc"
        target.write_text(
            "machine example.invalid\n"
            f"# {'x' * 1_001}\n"
            "login user\n"
            f"password {secret}\n",
            encoding="utf-8",
        )

        completed, report = self.json_report()
        self.assert_single_finding(
            report,
            code="likely_secret",
            key="likely_secret:00 Context/.netrc",
            severity="error",
            paths={"second-brain/00 Context/.netrc"},
        )
        self.assertNotIn(secret, completed.stdout)
        self.assertNotIn("DOCTOR_PRIVATE_NETRC", completed.stdout)

    def test_quoted_json_secret_key_is_reported_without_leaking_content(
        self,
    ) -> None:
        secret = "DOCTOR_PRIVATE_JSON_PASSWORD_MUST_NOT_LEAK"
        target = self.repo / "second-brain" / "00 Context" / "renamed.json"
        target.write_text(
            f'{{"password":"{secret}"}}\n',
            encoding="utf-8",
        )

        completed, report = self.json_report()
        self.assert_single_finding(
            report,
            code="likely_secret",
            key="likely_secret:00 Context/renamed.json",
            severity="error",
            paths={"second-brain/00 Context/renamed.json"},
        )
        self.assertNotIn(secret, completed.stdout)
        self.assertNotIn("DOCTOR_PRIVATE_JSON", completed.stdout)

    def test_duplicate_canonical_owner_paragraph_is_an_error_without_copy(self) -> None:
        self.append_to_note("00 Context/Learnings.md", CANONICAL_LESSON)

        completed, report = self.json_report()
        self.assert_single_finding(
            report,
            code="duplicate_canonical_owner",
            key=(
                "duplicate_canonical_owner:tasks/lessons.md:"
                "00 Context/Learnings.md"
            ),
            severity="error",
            paths={
                "tasks/lessons.md",
                "second-brain/00 Context/Learnings.md",
            },
        )
        self.assertNotIn(CANONICAL_LESSON, completed.stdout)

    def test_oversized_canonical_owner_is_a_content_safe_error(self) -> None:
        private = "DOCTOR_OVERSIZED_CANONICAL_OWNER_PRIVATE"
        owner = self.repo / "tasks" / "lessons.md"
        owner.write_bytes(
            b"x" * (1_000_000 - len(private.encode("utf-8")))
            + private.encode("utf-8")
        )

        completed, report = self.json_report()
        self.assert_single_finding(
            report,
            code="oversized_canonical_owner",
            key="oversized_canonical_owner:tasks/lessons.md",
            severity="error",
            paths={"tasks/lessons.md"},
        )
        self.assertNotIn(private, completed.stdout)

    def test_non_lfs_attachment_media_is_an_error(self) -> None:
        (self.repo / ".gitattributes").write_text(
            '"second-brain/07 Attachments/*.png" '
            "filter=lfs diff=lfs merge=lfs -text\n",
            encoding="utf-8",
        )
        attachment = (
            self.repo / "second-brain" / "07 Attachments" / "brief.pdf"
        )
        attachment.write_bytes(b"%PDF-1.7\n% non-lfs fixture\n")

        _, report = self.json_report()
        self.assert_single_finding(
            report,
            code="non_lfs_attachment",
            key="non_lfs_attachment:07 Attachments/brief.pdf",
            severity="error",
            paths={"second-brain/07 Attachments/brief.pdf"},
        )

    def test_large_lfs_attachment_is_not_loaded_for_secret_scanning(self) -> None:
        (self.repo / ".gitattributes").write_text(
            '"second-brain/07 Attachments/*.bin" '
            "filter=lfs diff=lfs merge=lfs -text\n",
            encoding="utf-8",
        )
        attachment = (
            self.repo / "second-brain" / "07 Attachments" / "large.bin"
        )
        with attachment.open("wb") as stream:
            stream.truncate(2_000_000)
        real_read_bytes = Path.read_bytes

        def guarded_read_bytes(path: Path) -> bytes:
            if path == attachment:
                raise AssertionError("large attachment was read into memory")
            return real_read_bytes(path)

        doctor = importlib.import_module("second_brain.doctor")
        with mock.patch.dict(os.environ, self.env, clear=True):
            with mock.patch.object(Path, "read_bytes", guarded_read_bytes):
                report = doctor.build_report()

        self.assertEqual(
            report["summary"],
            {"errors": 0, "status": "pass", "warnings": 0},
        )

    def test_hardlinked_vault_file_is_a_stable_error_without_content(self) -> None:
        body = "Hardlinked imported body must stay out of diagnostics."
        imported = self.write_import("hardlinked.md", self.import_note(body))
        os.link(imported, self.outside / "hardlinked-copy.md")

        first, report = self.json_report()
        second, repeated_report = self.json_report()

        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(report, repeated_report)
        self.assert_single_finding(
            report,
            code="vault_hard_link",
            key=(
                "vault_hard_link:"
                "06 Archive/Imports/fixture-source/hardlinked.md"
            ),
            severity="error",
            paths={
                "second-brain/06 Archive/Imports/fixture-source/hardlinked.md"
            },
        )
        self.assertNotIn(body, first.stdout)

    def test_import_without_frontmatter_is_a_safe_error(self) -> None:
        body = "Imported body without metadata must stay out of diagnostics."
        self.write_import("missing-frontmatter.md", f"# Imported\n\n{body}\n")

        completed, report = self.json_report()

        self.assert_single_finding(
            report,
            code="malformed_frontmatter",
            key=(
                "malformed_frontmatter:"
                "06 Archive/Imports/fixture-source/missing-frontmatter.md"
            ),
            severity="error",
            paths={
                "second-brain/06 Archive/Imports/fixture-source/"
                "missing-frontmatter.md"
            },
        )
        self.assertNotIn(body, completed.stdout)

    def test_import_with_malformed_frontmatter_is_a_safe_error(self) -> None:
        body = "Malformed imported metadata must stay out of diagnostics."
        self.write_import(
            "malformed-frontmatter.md",
            "---\ntags: [archive, imported]\n" f"# Imported\n\n{body}\n",
        )

        completed, report = self.json_report()

        self.assert_single_finding(
            report,
            code="malformed_frontmatter",
            key=(
                "malformed_frontmatter:"
                "06 Archive/Imports/fixture-source/malformed-frontmatter.md"
            ),
            severity="error",
            paths={
                "second-brain/06 Archive/Imports/fixture-source/"
                "malformed-frontmatter.md"
            },
        )
        self.assertNotIn(body, completed.stdout)

    def test_import_requires_source_hash_frontmatter_without_content_leak(self) -> None:
        body = "Imported body with incomplete metadata must stay private."
        self.write_import(
            "missing-source-hash.md",
            self.import_note(body, include_source_sha256=False),
        )

        completed, report = self.json_report()

        finding = self.assert_single_finding(
            report,
            code="missing_frontmatter_field",
            key=(
                "missing_frontmatter_field:"
                "06 Archive/Imports/fixture-source/missing-source-hash.md:"
                "source_sha256"
            ),
            severity="error",
            paths={
                "second-brain/06 Archive/Imports/fixture-source/"
                "missing-source-hash.md"
            },
        )
        self.assertEqual(finding["details"], {"field": "source_sha256"})
        self.assertNotIn(body, completed.stdout)

    def test_import_rejects_invalid_source_hash_without_content_leak(self) -> None:
        body = "PRIVATE_INVALID_HASH_BODY"
        self.write_import(
            "invalid-source-hash.md",
            self.import_note(body, source_sha256="not-a-sha256"),
        )

        completed, report = self.json_report()

        self.assert_single_finding(
            report,
            code="invalid_source_sha256",
            key=(
                "invalid_source_sha256:"
                "06 Archive/Imports/fixture-source/invalid-source-hash.md"
            ),
            severity="error",
            paths={
                "second-brain/06 Archive/Imports/fixture-source/"
                "invalid-source-hash.md"
            },
        )
        self.assertNotIn(body, completed.stdout)

    def test_import_rejects_body_changed_after_migration_without_leak(self) -> None:
        original = "Original imported body."
        body = "PRIVATE_TAMPERED_IMPORT_BODY"
        original_hash = hashlib.sha256(f"{original}\n".encode()).hexdigest()
        self.write_import(
            "tampered-body.md",
            self.import_note(body, source_sha256=original_hash),
        )

        completed, report = self.json_report()

        self.assert_single_finding(
            report,
            code="source_sha256_mismatch",
            key=(
                "source_sha256_mismatch:"
                "06 Archive/Imports/fixture-source/tampered-body.md"
            ),
            severity="error",
            paths={
                "second-brain/06 Archive/Imports/fixture-source/"
                "tampered-body.md"
            },
        )
        self.assertNotIn(body, completed.stdout)

    def test_import_with_private_visibility_is_a_safe_error(self) -> None:
        body = "Private imported body must stay out of diagnostics."
        self.write_import(
            "private-visibility.md",
            self.import_note(body, visibility="private"),
        )

        completed, report = self.json_report()

        self.assert_single_finding(
            report,
            code="unsafe_visibility",
            key=(
                "unsafe_visibility:"
                "06 Archive/Imports/fixture-source/private-visibility.md"
            ),
            severity="error",
            paths={
                "second-brain/06 Archive/Imports/fixture-source/"
                "private-visibility.md"
            },
        )
        self.assertNotIn(body, completed.stdout)

    def test_preserved_recovery_artifact_is_a_content_safe_error(self) -> None:
        private_body = "PRIVATE_RECOVERY_BYTES_MUST_NOT_LEAK"
        relative = (
            "00 Context/.Decisions.md."
            f"{'a' * 24}.tmp"
        )
        recovery = self.repo / "second-brain" / relative
        recovery.write_text(private_body, encoding="utf-8")

        completed, report = self.json_report()

        self.assert_single_finding(
            report,
            code="preserved_recovery_artifact",
            key=f"preserved_recovery_artifact:{relative}",
            severity="error",
            paths={f"second-brain/{relative}"},
        )
        self.assertNotIn(private_body, completed.stdout)

    def test_symlinked_vault_root_is_one_bounded_error(self) -> None:
        vault = self.repo / "second-brain"
        outside_vault = self.root / "outside-vault"
        vault.rename(outside_vault)
        vault.symlink_to(outside_vault, target_is_directory=True)

        _, report = self.json_report()
        self.assert_single_finding(
            report,
            code="vault_root_symlink",
            key="vault_root_symlink:second-brain",
            severity="error",
            paths={"second-brain"},
        )

    def test_invalid_doctor_arguments_exit_two_without_writes(self) -> None:
        completed = self.run_command(
            "doctor",
            "--format",
            "yaml",
            expected_returncode=2,
        )
        self.assertEqual(completed.stdout, "")
        self.assertIn("invalid choice: 'yaml'", completed.stderr)


if __name__ == "__main__":
    unittest.main()
