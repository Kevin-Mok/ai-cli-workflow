#!/usr/bin/env python3
"""Behavioral checks for the public-history audit CLI."""

import base64
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import uuid


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

    def test_runtime_identifiers_in_historical_and_nested_json_are_redacted(self) -> None:
        identifiers = []
        for key in (
            "x-codex-installation-id", "root_turn_id", "thread_id", "turn_id",
            "session_id", "prompt_cache_key",
        ):
            for encoding_depth in range(3):
                identifier = str(uuid.uuid4())
                identifiers.append(identifier)
                payload = json.dumps({key: identifier})
                for _ in range(encoding_depth):
                    payload = json.dumps({"response": payload})
                (self.repo / f"{key}-{encoding_depth}.json").write_text(
                    payload, encoding="utf-8"
                )
        self.commit("add runtime recordings")
        for path in self.repo.glob("*.json"):
            path.write_text("{}\n", encoding="utf-8")
        self.commit("remove runtime recordings")

        completed = self.run_audit()

        self.assertEqual(completed.returncode, 1, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["coverage"]["commits"], 2)
        self.assertEqual(
            report["summary"]["categories"], {"runtime_identifier": len(identifiers)}
        )
        self.assertEqual(
            {finding["location_type"] for finding in report["findings"]}, {"blob"}
        )
        outputs = completed.stdout + completed.stderr
        for arguments in (("--format", "text"), ("--format", "text", "--plain")):
            text_result = self.run_audit(*arguments)
            self.assertEqual(text_result.returncode, 1, text_result.stderr)
            self.assertIn("runtime_identifier", text_result.stdout)
            outputs += text_result.stdout + text_result.stderr
        for identifier in identifiers:
            self.assertNotIn(identifier, outputs)

    def test_runtime_identifier_in_commit_metadata_is_redacted(self) -> None:
        identifier = str(uuid.uuid4())
        (self.repo / "safe.txt").write_text("safe=true\n", encoding="utf-8")
        self.commit(json.dumps({"session_id": identifier}))

        completed = self.run_audit()

        self.assertEqual(completed.returncode, 1, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["summary"]["categories"], {"runtime_identifier": 1})
        self.assertEqual(report["findings"][0]["location_type"], "commit")
        self.assertNotIn(identifier, completed.stdout + completed.stderr)

    def test_runtime_identifier_in_unreachable_blob_is_redacted(self) -> None:
        identifier = str(uuid.uuid4())
        (self.repo / "safe.txt").write_text("safe=true\n", encoding="utf-8")
        self.commit("add safe settings")
        subprocess.run(
            ["git", "hash-object", "-w", "--stdin"],
            cwd=self.repo,
            input=json.dumps({"root_turn_id": identifier}).encode("utf-8"),
            capture_output=True,
            check=True,
        )

        completed = self.run_audit("--scope", "all")

        self.assertEqual(completed.returncode, 1, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["summary"]["categories"], {"runtime_identifier": 1})
        self.assertEqual(report["findings"][0]["location_type"], "blob")
        self.assertNotIn(identifier, completed.stdout + completed.stderr)

    def test_unrelated_uuids_and_nil_runtime_placeholders_pass(self) -> None:
        (self.repo / "example.json").write_text(
            json.dumps(
                {
                    "fixture_id": str(uuid.uuid4()),
                    "other_session_id": str(uuid.uuid4()),
                    "session_id": str(uuid.UUID(int=0)),
                    "thread_id": "REDACTED",
                    "notes": str(uuid.uuid4()),
                }
            ),
            encoding="utf-8",
        )
        self.commit("add public examples")

        completed = self.run_audit()

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["findings"], [])

    def test_raw_benchmark_runs_are_ignored_but_public_summaries_can_be_staged(self) -> None:
        (self.repo / ".gitignore").write_bytes((REPO_ROOT / ".gitignore").read_bytes())
        for benchmark in ("metaprompt", "metaprompt-selection"):
            run = self.repo / "benchmarks" / benchmark / "runs" / "trial" / "raw.json"
            run.parent.mkdir(parents=True)
            run.write_text("{}\n", encoding="utf-8")
            (run.parents[2] / "summary.json").write_text("{}\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)

        staged = subprocess.run(
            ["git", "ls-files"], cwd=self.repo, capture_output=True, text=True, check=True
        ).stdout.splitlines()

        for benchmark in ("metaprompt", "metaprompt-selection"):
            self.assertNotIn(f"benchmarks/{benchmark}/runs/trial/raw.json", staged)
            self.assertIn(f"benchmarks/{benchmark}/summary.json", staged)

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

    def test_replacement_refs_cannot_hide_original_history_bytes(self) -> None:
        secret = "ghp_" + "aB7C9dE2" * 5
        target = self.repo / "settings.txt"
        target.write_text(secret)
        self.commit("fixture original")
        original = subprocess.run(["git", "rev-parse", "HEAD:settings.txt"], cwd=self.repo, capture_output=True, check=True).stdout.strip().decode()
        safe = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=self.repo, input=b"safe public bytes\n", capture_output=True, check=True).stdout.strip().decode()
        subprocess.run(["git", "replace", original, safe], cwd=self.repo, capture_output=True, check=True)
        result = self.run_audit("--scope", "all")
        self.assertEqual(result.returncode, 1, "original history bytes must remain visible")
        self.assertIn("provider_token", json.loads(result.stdout)["summary"]["categories"])
        self.assertTrue(secret not in result.stdout + result.stderr, "fixture value leaked")


if __name__ == "__main__":
    unittest.main()
