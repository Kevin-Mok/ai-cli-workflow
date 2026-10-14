#!/usr/bin/env python3
"""Behavioral checks for the deterministic public-tree sanitizer."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SANITIZER = REPO_ROOT / "scripts" / "executable_sanitize-public-tree"


class PublicTreeSanitizerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.base = Path(self.directory.name)
        self.root = self.base / "tree"
        self.root.mkdir()
        self.rules = self.base / "rules.json"
        self.private_name = "Fixture" + " Private Person"
        self.rules.write_text(
            json.dumps(
                {
                    "drop_globs": ["private/**"],
                    "replace_literals": [
                        {
                            "label": "NAME_001",
                            "value": self.private_name,
                            "replacement": "Example Contributor",
                            "ignore_case": True,
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        self.rules.chmod(0o600)

    def run_tree(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SANITIZER),
                "--root",
                str(self.root),
                "--rules",
                str(self.rules),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_tree_mode_drops_private_paths_and_redacts_sensitive_values(self) -> None:
        secret = "sk-" + "live-fixture-0123456789abcdef"
        email = "person" + "@private.example"
        address = "8.8" + ".4.4"
        home = "/home/" + "private-user/work"
        encoded_key_header = (
            "LS0tLS1CRUdJTiBQ" + "UklWQVRFIEtFWS0tLS0tCg=="
        )
        (self.root / "settings.conf").write_text(
            "\n".join(
                [
                    "api_" + f"token={secret}",
                    f"email={email}",
                    f"host={address}",
                    f"workspace={home}",
                    "private_" + f"key={encoded_key_header}",
                    f"owner={self.private_name}",
                ]
            ),
            encoding="utf-8",
        )
        private = self.root / "private" / "history.txt"
        private.parent.mkdir()
        private.write_text("private navigation history\n", encoding="utf-8")
        binary = self.root / "asset.bin"
        binary.write_bytes(b"\x00\xff\x01unchanged")

        completed = self.run_tree()

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "")
        self.assertFalse(private.exists())
        self.assertEqual(binary.read_bytes(), b"\x00\xff\x01unchanged")
        sanitized = (self.root / "settings.conf").read_text(encoding="utf-8")
        self.assertIn("api_token=<redacted>", sanitized)
        self.assertIn("email=user@example.invalid", sanitized)
        self.assertIn("host=192.0.2.10", sanitized)
        self.assertIn("workspace=/home/example/work", sanitized)
        self.assertIn("private_key=<private-key-removed>", sanitized)
        self.assertIn("owner=Example Contributor", sanitized)
        for value in (secret, email, address, home, encoded_key_header, self.private_name):
            self.assertNotIn(value, sanitized)

    def test_tree_mode_never_reads_or_changes_git_directory(self) -> None:
        private_metadata = b"email=" + b"person" + b"@private.example\n"
        metadata = self.root / ".git" / "objects" / "fixture"
        metadata.parent.mkdir(parents=True)
        metadata.write_bytes(private_metadata)
        (self.root / "tracked.txt").write_text(
            "email=" + "person" + "@private.example\n", encoding="utf-8"
        )

        completed = self.run_tree()

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(metadata.read_bytes(), private_metadata)
        self.assertEqual(
            (self.root / "tracked.txt").read_text(encoding="utf-8"),
            "email=user@example.invalid\n",
        )

    def test_replacement_rule_can_match_case_insensitively(self) -> None:
        (self.root / "profile.txt").write_text(
            "owner=" + self.private_name.lower() + "\n", encoding="utf-8"
        )

        completed = self.run_tree()

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(
            (self.root / "profile.txt").read_text(encoding="utf-8"),
            "owner=Example Contributor\n",
        )


if __name__ == "__main__":
    unittest.main()
