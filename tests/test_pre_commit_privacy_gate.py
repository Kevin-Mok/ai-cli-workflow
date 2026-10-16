#!/usr/bin/env python3
"""Disposable-repository checks for the staged privacy gate and Git hook.

All synthetic sensitive bytes stay in temporary directories. Captured subprocess
output is never attached to assertions, including deliberately refused commits.
"""

import json
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts" / "executable_privacy-gate"


class PrivacyGateTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.base = Path(self.directory.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        home = self.base / "home"
        home.mkdir()
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        self.env.update(HOME=str(home), XDG_CONFIG_HOME=str(home / ".config"), GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0")
        self.git("init", "-q")
        self.git("config", "user.name", "Example Maintainer")
        self.git("config", "user.email", "maintainer@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.autocrlf", "false")

    def invoke(self, command, *, input=None):
        return subprocess.run(command, cwd=self.repo, env=self.env, input=input, capture_output=True)

    def git(self, *arguments, input=None, expected=0):
        result = self.invoke(["git", *arguments], input=input)
        if expected is not None:
            self.assertEqual(result.returncode, expected, "Git fixture operation failed (output suppressed)")
        return result

    def gate(self, *arguments):
        return self.invoke([sys.executable, str(GATE), "--repo", str(self.repo), *arguments])

    def write(self, name, content):
        target = self.repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def stage(self, name, content):
        target = self.write(name, content)
        self.git("add", "--", name)
        return target

    def install(self):
        self.assertEqual(self.gate("install").returncode, 0, "gate installation failed (output suppressed)")

    def commit(self, expected=0):
        return self.git("commit", "-qm", "fixture update", expected=expected)

    def baseline(self):
        self.stage("safe.txt", "public example\n")
        self.commit()

    def no_leak(self, result, *values):
        output = result.stdout + result.stderr
        for value in values:
            self.assertTrue(value.encode() not in output, "sensitive fixture leaked into captured output")

    def blocked(self, *values):
        before_head = self.git("rev-parse", "--verify", "HEAD", expected=None).stdout
        before_index = self.git("ls-files", "--stage", "-z").stdout
        result = self.commit(expected=1)
        self.no_leak(result, *values)
        self.assertEqual(self.git("rev-parse", "--verify", "HEAD", expected=None).stdout, before_head)
        self.assertEqual(self.git("ls-files", "--stage", "-z").stdout, before_index)
        return result

    def test_gate_entry_point_exists(self):
        self.assertTrue(GATE.is_file(), "privacy gate entry point is absent")

    def test_initial_safe_commit_and_repair_succeed(self):
        self.install()
        self.stage("safe.txt", "email=user@example.com\nsession_id=00000000-0000-0000-0000-000000000000\n")
        self.commit()
        secret = "sk-proj-" + "aB7C9dE2" * 8
        self.stage("safe.txt", secret)
        self.blocked(secret)
        self.stage("safe.txt", "repaired public example\n")
        self.commit()
        self.assertEqual(self.gate().returncode, 0)

    def test_provider_tokens_block_actual_commit_without_leaking_filename(self):
        self.install()
        for prefix, body in (("sk-proj-", "aB7C9dE2" * 8), ("ghp_", "aB7C9dE2" * 5), ("AKIA", "A7B8C9D0E1F2G3H4")):
            secret = prefix + body
            name = "private-" + secret + ".txt"
            self.stage(name, "value=" + secret + "\n")
            details = self.gate("check", "--details")
            self.assertEqual(details.returncode, 1, "details scan failed to refuse token")
            self.no_leak(details, secret, name)
            self.blocked(secret, name)
            self.git("rm", "--cached", "--", name)
            (self.repo / name).unlink()

    def test_quoted_json_credential_blocks(self):
        self.install()
        secret = "credential-" + "8eAf4bCD" * 5
        self.stage("settings.json", json.dumps({"api_" + "key": secret}))
        self.blocked(secret)

    def test_private_key_blocks(self):
        self.install()
        marker = "-----BEGIN " + "PRIVATE KEY-----"
        self.stage("key.txt", marker + "\n" + "ZmFrZWtleWJ5dGVz" * 8 + "\n")
        self.blocked(marker)

    def test_nested_runtime_json_blocks(self):
        self.install()
        for depth in range(3):
            identifier = str(uuid.uuid4())
            payload = json.dumps({"thread_id": identifier})
            for _ in range(depth):
                payload = json.dumps({"response": payload})
            self.stage("runtime.json", payload)
            self.blocked(identifier)

    def test_private_paths_block_even_safe_bytes_and_force_add(self):
        self.install()
        for name in ("benchmarks/metaprompt/runs/one/raw.json", "benchmarks/metaprompt-selection/runs/one/raw.json", ".env", "recovery/snapshot.json"):
            self.write(name, "public placeholder\n")
            self.git("add", "-f", "--", name)
            self.blocked(name)
            self.git("rm", "--cached", "--", name)
            (self.repo / name).unlink()

    def test_identity_email_in_content_is_not_globally_exempt(self):
        self.install()
        address = "person" + "@private.example"
        self.git("config", "user.email", address)
        self.stage("contact.txt", "email=" + address + "\n")
        self.blocked(address)

    def test_staged_secret_blocks_when_worktree_repaired(self):
        self.install()
        secret = "ghp_" + "aB7C9dE2" * 5
        target = self.stage("candidate.txt", secret)
        target.write_text("safe public bytes\n")
        self.blocked(secret)

    def test_safe_stage_passes_with_unstaged_secret(self):
        self.install()
        target = self.stage("candidate.txt", "safe public bytes\n")
        target.write_text("ghp_" + "aB7C9dE2" * 5)
        self.commit()
        self.assertEqual(self.git("show", "HEAD:candidate.txt").stdout, b"safe public bytes\n")

    def test_safe_rename_and_deletion_pass(self):
        self.baseline()
        self.install()
        self.git("mv", "safe.txt", "renamed.txt")
        self.commit()
        self.git("rm", "renamed.txt")
        self.commit()

    def test_rename_into_private_path_blocks(self):
        self.baseline()
        self.install()
        self.git("mv", "safe.txt", ".env")
        self.blocked(".env")

    def test_whitespace_newline_unicode_and_optionlike_names(self):
        self.install()
        for name in ("name with spaces.txt", "line\nbreak.txt", "caf\u00e9.txt", "--option.txt"):
            self.stage(name, "safe public bytes\n")
        self.commit()
        identifier = str(uuid.uuid4())
        name = "private\nfile-" + identifier + ".txt"
        self.stage(name, json.dumps({"session_id": identifier}))
        self.blocked(name, identifier)

    def test_private_literal_rules_are_local_and_redacted(self):
        literal = "Private Fixture Person"
        rules = self.base / "private-rules.json"
        rules.write_text(json.dumps({"forbidden_literals": [{"label": "NAME_001", "category": "personal_name", "value": literal}], "forbidden_path_globs": []}))
        rules.chmod(0o600)
        self.git("config", "privacyGate.rules", str(rules))
        self.install()
        self.stage("profile.txt", literal)
        self.blocked(literal, str(rules))

    def test_unreadable_rules_fail_closed_without_echoing_path(self):
        private_path = str(self.base / "private-sensitive-name.json")
        self.git("config", "privacyGate.rules", private_path)
        self.stage("safe.txt", "public example\n")
        result = self.gate("check", "--details")
        self.assertEqual(result.returncode, 2, "missing rules must fail closed")
        self.no_leak(result, private_path, "private-sensitive-name.json")

    def test_malformed_rules_fail_closed_without_echoing_contents(self):
        rules = self.base / "private-rules.json"
        secret = "ghp_" + "aB7C9dE2" * 5
        rules.write_text("not-json:" + secret)
        rules.chmod(0o600)
        self.git("config", "privacyGate.rules", str(rules))
        self.stage("safe.txt", "public example\n")
        result = self.gate("check", "--details")
        self.assertEqual(result.returncode, 2, "malformed rules must fail closed")
        self.no_leak(result, secret, str(rules))

    def test_unresolved_index_conflict_fails_closed(self):
        self.stage("safe.txt", "public example\n")
        oid = self.git("rev-parse", ":safe.txt").stdout.strip()
        self.git("update-index", "--force-remove", "safe.txt")
        records = b"".join(b"100644 " + oid + b" " + str(stage).encode() + b"\tsafe.txt\n" for stage in (1, 2, 3))
        self.git("update-index", "--index-info", input=records)
        result = self.gate("check", "--details")
        self.assertEqual(result.returncode, 2, "unresolved index must fail closed")
        self.no_leak(result, "safe.txt")

    def test_missing_staged_object_fails_closed(self):
        name = "sensitive-filename.txt"
        fake_oid = "a" * 40
        self.git("update-index", "--add", "--cacheinfo", "100644," + fake_oid + "," + name)
        result = self.gate("check", "--details")
        self.assertEqual(result.returncode, 2, "unreadable blob must fail closed")
        self.no_leak(result, name)

    def test_existing_hook_runs_and_is_restored_on_uninstall(self):
        hooks = Path(self.git("rev-parse", "--git-path", "hooks").stdout.decode().strip())
        if not hooks.is_absolute():
            hooks = self.repo / hooks
        hooks.mkdir(exist_ok=True)
        hook = hooks / "pre-commit"
        original = b"#!/bin/sh\nprintf ran >> hook-ran\n"
        hook.write_bytes(original)
        hook.chmod(0o755)
        self.install()
        self.install()
        self.stage("safe.txt", "public example\n")
        self.commit()
        self.assertEqual((self.repo / "hook-ran").read_text(), "ran")
        self.assertEqual(self.gate("uninstall").returncode, 0)
        self.assertEqual(hook.read_bytes(), original)
        self.assertEqual(self.git("config", "--get", "core.hooksPath", expected=None).returncode, 1)

    def test_existing_rejecting_hook_remains_enforced(self):
        hooks = self.repo / ".git" / "hooks"
        hook = hooks / "pre-commit"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
        self.install()
        self.stage("safe.txt", "public example\n")
        self.blocked()

    def test_configured_hookspath_is_preserved_and_enforced(self):
        hooks = self.base / "custom-hooks"
        hooks.mkdir()
        self.git("config", "core.hooksPath", str(hooks))
        self.install()
        self.assertTrue((hooks / "pre-commit").is_file())
        self.assertEqual(self.git("config", "--get", "core.hooksPath").stdout.decode().strip(), str(hooks))
        self.stage("safe.txt", "public example\n")
        self.commit()
        self.stage("bad.txt", "ghp_" + "aB7C9dE2" * 5)
        self.blocked()

    def test_linked_worktree_install_and_actual_commit(self):
        self.baseline()
        linked = self.base / "linked"
        self.git("worktree", "add", "-qb", "fixture-branch", str(linked))
        self.repo = linked
        self.install()
        self.stage("safe.txt", "safe linked change\n")
        self.commit()
        self.stage("bad.txt", "ghp_" + "aB7C9dE2" * 5)
        self.blocked()

    def test_status_plain_and_reactivation(self):
        self.install()
        status = self.gate("status", "--plain")
        self.assertEqual(status.returncode, 0)
        self.assertTrue((status.stdout + status.stderr).isascii(), "--plain output must be ASCII")
        self.assertEqual(self.gate("uninstall").returncode, 0)
        self.install()
        self.stage("bad.txt", "ghp_" + "aB7C9dE2" * 5)
        self.blocked()

    def test_binary_raw_token_is_refused(self):
        self.install()
        secret = "ghp_" + "aB7C9dE2" * 5
        (self.repo / "payload.bin").write_bytes(b"\x00binary\xff" + secret.encode() + b"\x00")
        self.git("add", "--", "payload.bin")
        self.blocked(secret)

    def lfs_pointer(self, content, *, store=True):
        oid = hashlib.sha256(content).hexdigest()
        if store:
            environment = self.git("lfs", "env").stdout.splitlines()
            media = [line.split(b"=", 1)[1] for line in environment if line.startswith(b"LocalMediaDir=")]
            self.assertEqual(len(media), 1, "LFS media storage was not discoverable")
            payload = Path(os.fsdecode(media[0])) / oid[:2] / oid[2:4] / oid
            payload.parent.mkdir(parents=True, exist_ok=True)
            payload.write_bytes(content)
        pointer = "version https://git-lfs.github.com/spec/v1\noid sha256:" + oid + "\nsize " + str(len(content)) + "\n"
        self.stage("asset.txt", pointer)

    def test_lfs_local_safe_payload_commits(self):
        self.install()
        self.lfs_pointer(b"safe public LFS payload\n")
        self.commit()

    def test_lfs_local_token_payload_is_refused(self):
        self.install()
        secret = "ghp_" + "aB7C9dE2" * 5
        self.lfs_pointer(secret.encode())
        self.blocked(secret)

    def test_missing_lfs_payload_fails_closed(self):
        self.lfs_pointer(b"missing local LFS payload\n", store=False)
        result = self.gate("check", "--details")
        self.assertEqual(result.returncode, 2, "missing LFS bytes must fail closed without download")
        self.no_leak(result, "asset.txt", str(self.repo))

    def test_public_identity_exception_is_exact_and_metadata_only(self):
        name = "Example Public Maintainer"
        address = "public" + "@private.example"
        rules = self.base / "identity-rules.json"
        rules.write_text(json.dumps({"forbidden_literals": [], "forbidden_path_globs": [], "approved_public_identities": [{"name": name, "email": address}]}))
        rules.chmod(0o600)
        self.git("config", "privacyGate.rules", str(rules))
        self.git("config", "user.name", name)
        self.git("config", "user.email", address)
        self.install()
        self.stage("safe.txt", "public example\n")
        self.commit()
        self.stage("contact.txt", "email=" + address)
        self.blocked(address)
        self.git("rm", "--cached", "--", "contact.txt")
        self.stage("safe.txt", "updated public example\n")
        self.git("config", "user.name", "Different Public Maintainer")
        self.blocked(address)

    def test_installed_missing_scanner_fails_closed_without_traceback(self):
        self.install()
        hookdir = Path(os.fsdecode(self.git("rev-parse", "--path-format=absolute", "--git-path", "hooks").stdout.strip()))
        (hookdir / "privacy-gate.d" / "executable_audit-public-history").unlink()
        self.stage("safe.txt", "public example\n")
        result = self.git("commit", "-qm", "fixture update", expected=1)
        self.no_leak(result, "Traceback", str(self.repo), "FileNotFoundError")
        self.assertEqual(self.git("rev-parse", "--verify", "HEAD", expected=None).returncode, 128)

    def test_preserved_hook_cannot_add_unsafe_candidate_after_scan(self):
        secret = "ghp_" + "aB7C9dE2" * 5
        self.write("hook-payload.txt", secret)
        hook = self.repo / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\ngit add -- hook-payload.txt\n")
        hook.chmod(0o755)
        self.install()
        self.stage("safe.txt", "public example\n")
        result = self.commit(expected=1)
        self.no_leak(result, secret)
        self.assertEqual(self.git("rev-parse", "--verify", "HEAD", expected=None).returncode, 128)

    def test_inherited_git_index_file_is_the_candidate(self):
        self.baseline()
        self.install()
        default_index = self.repo / ".git" / "index"
        original = default_index.read_bytes()
        alternate = self.base / "alternate-index"
        shutil.copyfile(default_index, alternate)
        self.env["GIT_INDEX_FILE"] = str(alternate)
        secret = "ghp_" + "aB7C9dE2" * 5
        self.stage("candidate.txt", secret)
        self.blocked(secret)
        self.assertEqual(default_index.read_bytes(), original)
        self.stage("candidate.txt", "safe alternate bytes\n")
        self.commit()

    def test_example_substring_does_not_exempt_real_credential(self):
        self.install()
        secret = "prefix" + "example" + "8eAf4bCD" * 5
        self.stage("settings.json", json.dumps({"api_" + "key": secret}))
        self.blocked(secret)

    def test_submodule_candidate_mode_fails_closed(self):
        self.baseline()
        oid = self.git("rev-parse", "HEAD").stdout.decode().strip()
        name = "private-module-name"
        self.git("update-index", "--add", "--cacheinfo", "160000," + oid + "," + name)
        result = self.gate("check", "--details")
        self.assertEqual(result.returncode, 2, "unreviewed submodule content must fail closed")
        self.no_leak(result, name)

    def test_replace_ref_cannot_hide_unsafe_index_or_tree_blob(self):
        self.baseline()
        self.install()
        secret = "ghp_" + "aB7C9dE2" * 5
        self.stage("candidate.txt", secret)
        unsafe_oid = self.git("rev-parse", ":candidate.txt").stdout.decode().strip()
        safe_oid = self.git("hash-object", "-w", "--stdin", input=b"safe replacement bytes\n").stdout.decode().strip()
        tree = self.git("write-tree").stdout.decode().strip()
        self.git("replace", unsafe_oid, safe_oid)
        for arguments in (("check",), ("check", "--tree", tree)):
            result = self.gate(*arguments)
            self.assertEqual(result.returncode, 1, "replace refs must not hide original candidate bytes")
            self.no_leak(result, secret)
        self.blocked(secret)

    def test_crlf_lfs_pointer_is_refused(self):
        self.install()
        self.stage("asset.txt", "version https://git-lfs.github.com/spec/v1\r\noid sha256:" + "a" * 64 + "\r\nsize 10\r\n")
        result = self.gate("check", "--details")
        self.assertEqual(result.returncode, 2, "noncanonical LFS pointer must fail closed")
        self.no_leak(result, "asset.txt")

    def test_private_metadata_email_without_dotted_domain_is_refused(self):
        self.install()
        address = "private-fixture" + "@private-host"
        self.git("config", "user.email", address)
        self.stage("safe.txt", "public example\n")
        self.blocked(address)

    def test_commit_author_option_cannot_override_safe_config_with_private_identity(self):
        self.baseline()
        self.install()
        self.stage("safe.txt", "safe public update\n")
        address = "private-author" + "@private.example"
        head = self.git("rev-parse", "HEAD").stdout
        index = self.git("ls-files", "--stage", "-z").stdout
        result = self.git("commit", "-qm", "fixture update", "--author", "Private Fixture <" + address + ">", expected=1)
        self.no_leak(result, address)
        self.assertEqual(self.git("rev-parse", "HEAD").stdout, head)
        self.assertEqual(self.git("ls-files", "--stage", "-z").stdout, index)

    def test_commit_author_environment_cannot_override_safe_config_with_private_identity(self):
        self.baseline()
        self.install()
        self.stage("safe.txt", "safe public update\n")
        address = "private-author" + "@private.example"
        self.env["GIT_AUTHOR_EMAIL"] = address
        self.blocked(address)

    def test_reviewed_legacy_blob_passes_and_modified_token_is_refused(self):
        name = "dot_agents/skills/last30days/scripts/lib/bluesky.py"
        target = self.repo / name
        target.parent.mkdir(parents=True)
        target.write_bytes((ROOT / name).read_bytes())
        self.git("add", "--", name)
        self.assertEqual(self.gate("check").returncode, 0, "exact reviewed public source must pass")
        self.install()
        self.commit()
        secret = "ghp_" + "aB7C9dE2" * 5
        target.write_bytes(target.read_bytes() + b"\n" + secret.encode() + b"\n")
        self.git("add", "--", name)
        self.blocked(secret, name)

    def installed_bundle(self):
        hooks = Path(os.fsdecode(self.git("rev-parse", "--path-format=absolute", "--git-path", "hooks").stdout.strip()))
        return hooks / "privacy-gate.d"

    def reviewed_recovery_fixture(self):
        manifest_path = ROOT / "scripts" / "privacy_gate_approvals.json"
        self.assertTrue(manifest_path.is_file(), "reviewed manifest is absent")
        manifest = json.loads(manifest_path.read_bytes())
        entry = next((item for item in manifest["entries"] if "sensitive_path" in item["categories"]), None)
        self.assertTrue(entry is not None, "reviewed public recovery document approval is absent")
        listing = subprocess.run(["git", "--no-replace-objects", "ls-files", "--stage", "-z"], cwd=ROOT, capture_output=True)
        self.assertEqual(listing.returncode, 0, "source fixture inventory failed")
        selected = None
        for record in listing.stdout.split(b"\0"):
            if not record:
                continue
            metadata, raw_name = record.split(b"\t", 1)
            if hashlib.sha256(raw_name).hexdigest()[:12] == entry["path_ref"]:
                selected = raw_name, metadata.split()[1]
                break
        self.assertTrue(selected is not None, "reviewed fixture source is unavailable")
        raw_name, oid = selected
        blob = subprocess.run(["git", "--no-replace-objects", "cat-file", "blob", oid.decode("ascii")], cwd=ROOT, capture_output=True)
        self.assertEqual(blob.returncode, 0, "source fixture read failed")
        self.assertTrue(hashlib.sha256(blob.stdout).hexdigest() == entry["content_sha256"], "reviewed fixture content changed")
        return os.fsdecode(raw_name), blob.stdout

    def test_reviewed_recovery_document_approval_is_bound_to_exact_blob(self):
        name, content = self.reviewed_recovery_fixture()
        target = self.repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        self.git("add", "--", name)
        self.assertEqual(self.gate("check").returncode, 0, "exact reviewed recovery document must pass")
        self.install()
        self.commit()
        target.write_bytes(content + b"\nAdditional harmless public documentation.\n")
        self.git("add", "--", name)
        self.blocked(name)

    def test_public_blob_approval_cannot_override_private_literal_rule(self):
        name = "dot_agents/skills/last30days/scripts/lib/bluesky.py"
        target = self.repo / name
        target.parent.mkdir(parents=True)
        target.write_bytes((ROOT / name).read_bytes())
        self.git("add", "--", name)
        rules = self.base / "private-rules.json"
        literal = "json_" + "data"
        rules.write_text(json.dumps({"forbidden_literals": [{"label": "LOCAL_001", "category": "credential", "value": literal}], "forbidden_path_globs": []}))
        rules.chmod(0o600)
        self.git("config", "privacyGate.rules", str(rules))
        result = self.gate("check", "--details")
        self.assertEqual(result.returncode, 1, "public approval must not override private literal policy")
        self.no_leak(result, literal, name)
        self.install()
        self.blocked(literal, name)

    def test_public_path_approval_cannot_override_private_path_rule(self):
        name, content = self.reviewed_recovery_fixture()
        target = self.repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        self.git("add", "--", name)
        rules = self.base / "private-rules.json"
        rules.write_text(json.dumps({"forbidden_literals": [], "forbidden_path_globs": [name]}))
        rules.chmod(0o600)
        self.git("config", "privacyGate.rules", str(rules))
        result = self.gate("check", "--details")
        self.assertEqual(result.returncode, 1, "public approval must not override private path policy")
        self.no_leak(result, name)
        self.install()
        self.blocked(name)

    def test_public_identity_approval_cannot_override_private_literal_rule(self):
        name = "Example Public Maintainer"
        address = "approved-public" + "@private.example"
        rules = self.base / "private-rules.json"
        rules.write_text(json.dumps({"forbidden_literals": [{"label": "LOCAL_IDENTITY", "category": "email", "value": address}], "forbidden_path_globs": [], "approved_public_identities": [{"name": name, "email": address}]}))
        rules.chmod(0o600)
        self.git("config", "privacyGate.rules", str(rules))
        self.git("config", "user.name", name)
        self.git("config", "user.email", address)
        self.stage("safe.txt", "public example\n")
        result = self.gate("check", "--details")
        self.assertEqual(result.returncode, 1, "public identity approval must not override private literal policy")
        self.no_leak(result, address)
        self.install()
        self.blocked(address)

    def test_installer_copies_reviewed_manifest_and_missing_snapshot_fails_closed(self):
        self.install()
        bundle = self.installed_bundle()
        manifest = bundle / "privacy_gate_approvals.json"
        self.assertTrue(manifest.is_file(), "installed scanner must include reviewed manifest")
        self.assertTrue(manifest.read_bytes() == (ROOT / "scripts" / "privacy_gate_approvals.json").read_bytes(), "installed reviewed policy differs")
        manifest.unlink()
        self.stage("safe.txt", "public example\n")
        result = self.invoke([sys.executable, str(bundle / "executable_privacy-gate"), "--repo", str(self.repo), "check", "--details"])
        self.assertEqual(result.returncode, 2, "missing reviewed manifest must fail closed")
        self.no_leak(result, str(self.repo), "Traceback", "privacy_gate_approvals.json")
        refused = self.commit(expected=1)
        self.no_leak(refused, str(self.repo), "Traceback")

    def test_malformed_installed_approval_snapshot_fails_closed(self):
        self.install()
        bundle = self.installed_bundle()
        manifest = bundle / "privacy_gate_approvals.json"
        self.assertTrue(manifest.is_file(), "installed scanner must include reviewed manifest")
        secret = "ghp_" + "aB7C9dE2" * 5
        self.stage("safe.txt", "public example\n")
        for content in ("invalid-json:" + secret, json.dumps({"schema_version": 1, "entries": [{"path_ref": secret, "content_sha256": "a" * 64, "categories": ["credential"], "reason": "invalid path reference"}]}), json.dumps({"schema_version": 1, "entries": [{"path_ref": "a" * 12, "content_sha256": "b" * 64, "categories": ["email"], "reason": "unapproved category"}]})):
            manifest.write_text(content)
            result = self.invoke([sys.executable, str(bundle / "executable_privacy-gate"), "--repo", str(self.repo), "check", "--details"])
            self.assertEqual(result.returncode, 2, "malformed reviewed manifest must fail closed")
            self.no_leak(result, secret, str(self.repo), "Traceback", "privacy_gate_approvals.json")


if __name__ == "__main__":
    unittest.main()
