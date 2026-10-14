#!/usr/bin/env python3
"""Behavioral checks for the public-history audit CLI."""

import base64
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDITOR = REPO_ROOT / "scripts" / "executable_audit-public-history"


class PublicHistoryAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.repo = Path(self.directory.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)

    def commit(self, message: str) -> None:
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Example Maintainer",
                "-c",
                "user.email=maintainer@example.invalid",
                "commit",
                "-qm",
                message,
            ],
            cwd=self.repo,
            check=True,
        )

    def run_audit(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(AUDITOR),
                "--repo",
                str(self.repo),
                "--format",
                "json",
                *arguments,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_detects_sensitive_data_in_historical_blob_without_echoing_values(self) -> None:
        secret = "sk-" + "test-0123456789abcdefghijklmnop"
        personal_email = "person" + "@private.example"
        public_ip = "8.8" + ".4.4"
        home_path = "/home/" + "private-user/work"
        encoded_key_header = base64.b64encode(
            b"-----BEGIN " + b"PRIVATE " + b"KEY-----\n"
        ).decode("ascii")
        (self.repo / "settings.txt").write_text(
            "\n".join(
                [
                    "api_" + f"token={secret}",
                    f"email={personal_email}",
                    f"host={public_ip}",
                    f"workspace={home_path}",
                    "private_" + "key=" + encoded_key_header,
                ]
            ),
            encoding="utf-8",
        )
        self.commit("add local settings")
        (self.repo / "settings.txt").write_text("safe=true\n", encoding="utf-8")
        self.commit("remove local settings")

        completed = self.run_audit()

        self.assertEqual(completed.returncode, 1, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["schema_version"], 1)
        self.assertEqual(report["summary"]["status"], "fail")
        self.assertEqual(report["coverage"]["commits"], 2)
        self.assertGreaterEqual(report["coverage"]["unique_blobs"], 2)
        categories = {finding["category"] for finding in report["findings"]}
        self.assertTrue(
            {"credential", "email", "ip_address", "home_path", "private_key"}
            <= categories
        )
        combined_output = completed.stdout + completed.stderr
        for value in (secret, personal_email, public_ip, home_path):
            self.assertNotIn(value, combined_output)

    def test_private_rules_detect_paths_and_literals_without_echoing_them(self) -> None:
        forbidden_name = "Fixture Private Person"
        forbidden_path = "private/account.json"
        target = self.repo / forbidden_path
        target.parent.mkdir(parents=True)
        target.write_text(
            json.dumps({"display_name": forbidden_name}), encoding="utf-8"
        )
        self.commit("add fixture profile")
        rules = self.repo.parent / "audit-rules.json"
        rules.write_text(
            json.dumps(
                {
                    "forbidden_literals": [
                        {
                            "label": "NAME_001",
                            "category": "personal_name",
                            "value": forbidden_name,
                        }
                    ],
                    "forbidden_path_globs": ["private/**"],
                }
            ),
            encoding="utf-8",
        )
        rules.chmod(0o600)

        completed = self.run_audit("--rules", str(rules))

        self.assertEqual(completed.returncode, 1, completed.stderr)
        report = json.loads(completed.stdout)
        categories = {finding["category"] for finding in report["findings"]}
        self.assertTrue({"personal_name", "sensitive_path"} <= categories)
        combined_output = completed.stdout + completed.stderr
        self.assertNotIn(forbidden_name, combined_output)
        self.assertNotIn(forbidden_path, combined_output)

    def test_private_literal_rule_can_match_case_insensitively(self) -> None:
        forbidden_name = "Fixture Private Person"
        (self.repo / "profile.txt").write_text(
            "display_name=" + forbidden_name.lower() + "\n", encoding="utf-8"
        )
        self.commit("add fixture profile")
        rules = self.repo.parent / "audit-rules.json"
        rules.write_text(
            json.dumps(
                {
                    "forbidden_literals": [
                        {
                            "label": "NAME_001",
                            "category": "personal_name",
                            "value": forbidden_name,
                            "ignore_case": True,
                        }
                    ],
                    "forbidden_path_globs": [],
                }
            ),
            encoding="utf-8",
        )
        rules.chmod(0o600)

        completed = self.run_audit("--rules", str(rules))

        self.assertEqual(completed.returncode, 1, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertIn(
            "personal_name",
            {finding["category"] for finding in report["findings"]},
        )

    def test_private_literal_rule_can_limit_matching_to_blobs(self) -> None:
        account_identifier = "fixture-calendar-user"
        (self.repo / "safe.txt").write_text("safe=true\n", encoding="utf-8")
        self.commit("configure " + account_identifier)
        rules = self.repo.parent / "audit-rules.json"
        rules.write_text(
            json.dumps(
                {
                    "forbidden_literals": [
                        {
                            "label": "ACCOUNT_001",
                            "category": "account_identifier",
                            "value": account_identifier,
                            "ignore_case": True,
                            "locations": ["blob"],
                        }
                    ],
                    "forbidden_path_globs": [],
                }
            ),
            encoding="utf-8",
        )
        rules.chmod(0o600)

        completed = self.run_audit("--rules", str(rules))

        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["summary"]["status"], "pass")
        self.assertEqual(report["findings"], [])

    def test_private_path_rule_can_allow_exact_reviewed_placeholder(self) -> None:
        placeholder = self.repo / "private" / "README.md"
        placeholder.parent.mkdir()
        placeholder.write_text("Public placeholder only.\n", encoding="utf-8")
        self.commit("add reviewed placeholder")
        rules = self.repo.parent / "audit-rules.json"
        rules.write_text(
            json.dumps(
                {
                    "forbidden_literals": [],
                    "forbidden_path_globs": ["private/**"],
                    "allowed_paths": ["private/README.md"],
                }
            ),
            encoding="utf-8",
        )
        rules.chmod(0o600)

        completed = self.run_audit("--rules", str(rules))

        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["summary"]["status"], "pass")
        self.assertEqual(report["findings"], [])

    def test_all_object_scope_detects_unreachable_sensitive_blob(self) -> None:
        (self.repo / "safe.txt").write_text("safe=true\n", encoding="utf-8")
        self.commit("add safe settings")
        dangling_secret = b"api_token=" + b"sk-" + b"live-unreachable-fixture-value"
        subprocess.run(
            ["git", "hash-object", "-w", "--stdin"],
            cwd=self.repo,
            input=dangling_secret,
            capture_output=True,
            check=True,
        )

        completed = self.run_audit("--scope", "all")

        self.assertEqual(completed.returncode, 1, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["coverage"]["scope"], "all")
        self.assertIn(
            "credential",
            {finding["category"] for finding in report["findings"]},
        )
        self.assertNotIn(
            dangling_secret.decode("ascii"), completed.stdout + completed.stderr
        )

    def test_documentation_placeholders_pass_without_findings(self) -> None:
        (self.repo / "example.conf").write_text(
            "\n".join(
                [
                    "email=user@example.invalid",
                    "host=192.0.2.10",
                    "workspace=/home/example/work",
                    "api_token={{ .apiToken }}",
                ]
            ),
            encoding="utf-8",
        )
        self.commit("add public example")

        completed = self.run_audit()

        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["summary"]["status"], "pass")
        self.assertEqual(report["findings"], [])

    def test_binary_payload_is_counted_without_text_regex_false_positives(self) -> None:
        forbidden = "Fixture Private Person"
        payload = (
            b"\x89PNG\r\n\x1a\n\x00compressed:"
            + forbidden.encode()
            + b"@private"
            + b".example"
        )
        (self.repo / "fixture.png").write_bytes(payload)
        self.commit("add binary fixture")
        rules = self.repo.parent / "audit-rules.json"
        rules.write_text(
            json.dumps(
                {
                    "forbidden_literals": [
                        {
                            "label": "NAME_001",
                            "category": "personal_name",
                            "value": forbidden,
                        }
                    ],
                    "forbidden_path_globs": [],
                }
            ),
            encoding="utf-8",
        )
        rules.chmod(0o600)

        completed = self.run_audit("--rules", str(rules))

        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["summary"]["status"], "pass")
        self.assertEqual(report["coverage"]["binary_blobs"], 1)


if __name__ == "__main__":
    unittest.main()
