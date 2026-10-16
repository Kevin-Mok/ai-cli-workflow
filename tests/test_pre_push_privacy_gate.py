#!/usr/bin/env python3
"""Real hook/remote fixtures; synthetic findings never leave temporary repos."""

import json
from unittest.mock import patch
from pathlib import Path
import subprocess
import sys
import unittest

from test_pre_commit_privacy_gate import PrivacyGateFixture, GATE

sys.path.insert(0, str(GATE.parent))
import privacy_gate


class PrePushPrivacyTests(PrivacyGateFixture):
    def setUp(self):
        super().setUp()
        self.remote = self.base / "remote.git"
        self.git("init", "--bare", "-q", str(self.remote))
        self.git("remote", "add", "origin", str(self.remote))
        self.baseline()
        self.git("push", "-q", "origin", "HEAD:refs/heads/main")
        self.base_oid = self.git("rev-parse", "HEAD").stdout.decode().strip()

    def push(self, *refs):
        return self.git("push", "-q", "origin", *refs, expected=None)

    def hook(self, records, *arguments):
        return self.invoke([sys.executable, str(GATE), "pre-push", "--plain", *arguments], input=records.encode())

    def record(self, local=None, remote=None, ref="main"):
        local = local or self.git("rev-parse", "HEAD").stdout.decode().strip()
        remote = remote or self.base_oid
        return f"refs/heads/{ref} {local} refs/heads/{ref} {remote}\n"

    def test_blocks_finding_removed_before_push_without_leaking_values(self):
        secret = "ghp_" + "aB7C9dE2" * 5
        self.stage("fixture.txt", secret)
        self.commit()
        self.stage("fixture.txt", "public repaired bytes\n")
        self.commit()
        self.install()
        result = self.push("HEAD:main")
        self.assertNotEqual(result.returncode, 0, "historical finding must block actual push")
        self.assertIn(b"provider_token", result.stdout + result.stderr)
        self.no_leak(result, secret)
        self.assertEqual(self.git("--git-dir=" + str(self.remote), "rev-parse", "main").stdout.decode().strip(), self.base_oid)

    def test_clean_range_ignores_unrelated_history(self):
        self.git("checkout", "-qb", "unrelated")
        self.stage("fixture.txt", "ghp_" + "aB7C9dE2" * 5)
        self.commit()
        self.git("checkout", "-q", "-")
        self.stage("safe.txt", "public update\n")
        self.commit()
        self.install()
        self.assertEqual(self.push("HEAD:main").returncode, 0)

    def test_range_excludes_old_findings_and_uses_supplied_tip_not_head(self):
        self.stage("fixture.txt", "ghp_" + "aB7C9dE2" * 5)
        self.commit()
        self.stage("fixture.txt", "public repaired bytes\n")
        self.commit()
        remote = self.git("rev-parse", "HEAD").stdout.decode().strip()
        self.stage("safe.txt", "public update\n")
        self.commit()
        local = self.git("rev-parse", "HEAD").stdout.decode().strip()
        self.stage("fixture.txt", "ghp_" + "aB7C9dE2" * 5)
        self.commit()
        self.assertEqual(self.hook(self.record(local=local, remote=remote)).returncode, 0)
        self.assertEqual(self.hook(self.record(local=remote, remote=remote)).returncode, 0)

    def test_private_paths_are_limited_to_selected_history(self):
        rules = self.base / "rules.json"
        rules.write_text(json.dumps({"forbidden_path_globs": ["fixture-private/**"]}))
        rules.chmod(0o600)
        self.git("config", "privacyGate.rules", str(rules))
        self.stage("fixture-private/record.txt", "public fixture\n")
        self.commit()
        self.git("rm", "-qr", "fixture-private")
        self.commit()
        clean = self.git("rev-parse", "HEAD").stdout.decode().strip()
        self.assertEqual(self.hook(self.record()).returncode, 1)
        self.assertEqual(self.hook(self.record(local=clean, remote=clean)).returncode, 0)

    def test_shallow_history_is_refused(self):
        shallow = self.base / "shallow"
        self.git("clone", "-q", "--depth=1", "file://" + str(self.repo), str(shallow))
        self.repo = shallow
        result = self.hook(self.record(remote="0" * 40))
        self.assertEqual(result.returncode, 2)
        self.no_leak(result, str(shallow), "Traceback")

    def test_new_branch_scans_full_ancestry_even_when_tip_is_clean(self):
        secret = "ghp_" + "aB7C9dE2" * 5
        self.stage("fixture.txt", secret)
        self.commit()
        self.stage("fixture.txt", "public repaired bytes\n")
        self.commit()
        self.install()
        result = self.push("HEAD:new-branch")
        self.assertNotEqual(result.returncode, 0, "new branch must scan older commits")
        self.no_leak(result, secret)

    def test_new_clean_branch_passes(self):
        self.install()
        self.assertEqual(self.push("HEAD:new-branch").returncode, 0)

    def test_deleted_branch_skips_audit_even_with_bad_history(self):
        self.stage("fixture.txt", "ghp_" + "aB7C9dE2" * 5)
        self.commit()
        self.git("push", "-q", "origin", "HEAD:delete-me")
        self.install()
        self.assertEqual(self.push(":delete-me").returncode, 0)
        self.assertEqual(self.hook(self.record(local="0" * 40, remote="f" * 40)).returncode, 0)

    def test_all_stdin_updates_are_checked(self):
        secret = "ghp_" + "aB7C9dE2" * 5
        self.stage("fixture.txt", secret)
        self.commit()
        result = self.hook(self.record(local=self.base_oid) + self.record(ref="other"))
        self.assertEqual(result.returncode, 1)
        self.no_leak(result, secret)

    def test_malformed_or_missing_objects_fail_closed_without_raw_errors(self):
        for records in ("private-ref garbage\n", self.record(local="a" * 40), self.record(remote="a" * 40)):
            result = self.hook(records)
            self.assertEqual(result.returncode, 2)
            self.no_leak(result, "private-ref", "Traceback", str(self.repo))
        self.assertEqual(self.hook("").returncode, 0)

    def test_approved_exact_identity_passes_but_message_and_blob_do_not(self):
        email = "fixture-owner" + "@private.example"
        rules = self.base / "rules.json"
        rules.write_text(json.dumps({"approved_public_identities": [{"name": "Example Maintainer", "email": email}]}))
        rules.chmod(0o600)
        self.git("config", "privacyGate.rules", str(rules))
        self.git("config", "user.email", email)
        self.stage("safe.txt", "public update\n")
        self.commit()
        clean_oid = self.git("rev-parse", "HEAD").stdout.decode().strip()
        self.install()
        self.assertEqual(self.push("HEAD:main").returncode, 0, "approved metadata identity should pass")
        self.git("-c", "core.hooksPath=/dev/null", "commit", "--allow-empty", "-qm", email)
        result = self.hook(self.record(remote=clean_oid))
        self.assertEqual(result.returncode, 1, "message email must not inherit metadata approval")
        self.no_leak(result, email)
        self.stage("fixture.txt", email)
        self.git("-c", "core.hooksPath=/dev/null", "commit", "-qm", "public fixture")
        result = self.hook(self.record(remote=clean_oid))
        self.assertEqual(result.returncode, 1)
        self.no_leak(result, email)

    def test_private_category_and_explicit_identity_prohibition_stay_safe(self):
        email = "fixture-owner" + "@private.example"
        category = "private-category-value"
        rules = self.base / "rules.json"
        rules.write_text(json.dumps({
            "approved_public_identities": [{"name": "Example Maintainer", "email": email}],
            "forbidden_literals": [{"value": email, "category": category}],
        }))
        rules.chmod(0o600)
        self.git("config", "privacyGate.rules", str(rules))
        self.git("config", "user.email", email)
        self.git("commit", "--allow-empty", "-qm", "public fixture")
        result = self.hook(self.record())
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"private_literal", result.stdout)
        self.no_leak(result, email, category)

    def test_existing_pre_push_receives_same_stdin_and_arguments_and_is_restored(self):
        hook = self.repo / ".git/hooks/pre-push"
        original = b'#!/bin/sh\ncat > hook-input\nprintf "%s\\n" "$@" > hook-args\nexit 7\n'
        hook.write_bytes(original)
        hook.chmod(0o751)
        self.install()
        self.install()
        result = self.push("HEAD:new-branch")
        self.assertNotEqual(result.returncode, 0)
        expected = self.record(remote="0" * 40, ref="new-branch").replace("refs/heads/new-branch", "HEAD", 1)
        self.assertEqual((self.repo / "hook-input").read_text(), expected)
        self.assertEqual((self.repo / "hook-args").read_text().splitlines(), ["origin", str(self.remote)])
        replay = self.invoke([str(hook), "origin", str(self.remote)], input=expected.encode())
        self.assertEqual(replay.returncode, 7, "preserved hook exit status must pass through unchanged")
        self.assertEqual(self.gate("uninstall").returncode, 0)
        self.assertEqual(hook.read_bytes(), original)
        self.assertEqual(hook.stat().st_mode & 0o777, 0o751)

    def test_install_upgrades_legacy_gate_and_status_checks_both_hooks(self):
        self.install()
        hook = self.repo / ".git/hooks/pre-push"
        self.assertTrue(hook.is_file(), "install must add pre-push alongside pre-commit")
        hook.unlink()  # Existing pre-commit-only installation from the prior version.
        self.assertEqual(self.gate("status").returncode, 1)
        self.install()
        self.assertEqual(self.gate("status").returncode, 0)
        hook.write_text("#!/bin/sh\nexit 0\n")
        self.assertEqual(self.gate("uninstall").returncode, 2)
        self.assertTrue((hook.parent / "pre-commit").exists(), "changed hook must not partially uninstall gate")

    def test_auditor_failure_diagnostics_are_not_forwarded(self):
        self.install()
        scanner = self.repo / ".git/hooks/privacy-gate.d/executable_audit-public-history"
        # The parent imports this scanner too; fail only in the CLI child.
        scanner.write_text(scanner.read_text().replace('if __name__ == "__main__":', 'if __name__ == "__main__":\n    raise RuntimeError("private-diagnostic-fixture")'))
        result = self.push("HEAD:new-branch")
        self.assertNotEqual(result.returncode, 0)
        self.no_leak(result, "private-diagnostic-fixture", "Traceback")

    def test_install_restores_non_executable_owned_hook(self):
        self.install()
        hook = self.repo / ".git/hooks/pre-push"
        hook.chmod(0o600)
        self.install()
        self.assertEqual(self.gate("status").returncode, 0)
        self.assertTrue(hook.stat().st_mode & 0o100)

    def test_failed_hook_publication_keeps_original_pre_push_active(self):
        hook = self.repo / ".git/hooks/pre-push"
        original = b'#!/bin/sh\nexit 9\n'
        hook.write_bytes(original)
        hook.chmod(0o751)
        original_open = Path.open
        original_replace = Path.replace
        def fail_open(path, *args, **kwargs):
            if path == hook and args and args[0] == "xb":
                raise OSError("synthetic hook publication failure")
            return original_open(path, *args, **kwargs)
        def fail_replace(path, target):
            if target == hook:
                raise OSError("synthetic hook publication failure")
            return original_replace(path, target)
        # Cover both legacy direct writes and prepared atomic publication.
        with patch.object(Path, "open", fail_open), patch.object(Path, "replace", fail_replace):
            with self.assertRaises(OSError):
                privacy_gate.install(self.repo)
        self.assertTrue(hook.is_file(), "a failed install must leave the original hook active")
        self.assertEqual(hook.read_bytes(), original)
        self.assertEqual(hook.stat().st_mode & 0o777, 0o751)


if __name__ == "__main__":
    unittest.main()
