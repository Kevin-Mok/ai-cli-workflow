from __future__ import annotations

import hashlib
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.second_brain import config_snapshot
from scripts.second_brain.config_snapshot import (
    ConfigSnapshotError,
    snapshot_codex_config,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINT = REPO_ROOT / "scripts" / "executable_snapshot-codex-config"


class ConfigSnapshotTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.home = self.root / "home"
        self.source = self.home / ".codex" / "config.toml"
        self.target = self.root / "repo" / "dot_codex" / "config.toml"
        self.source.parent.mkdir(parents=True)
        self.target.parent.mkdir(parents=True)
        self.source.write_text('model = "source"\n', encoding="utf-8")
        self.target.write_text('model = "target"\n', encoding="utf-8")

    def test_default_target_is_resolved_through_chezmoi(self) -> None:
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        calls = self.root / "chezmoi.calls"
        fake_chezmoi = bin_dir / "chezmoi"
        fake_chezmoi.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "printf '%s\\n' \"$*\" >> \"$TEST_CHEZMOI_CALLS\"\n"
            "printf '%s\\n' \"$TEST_CODEX_TARGET\"\n",
            encoding="utf-8",
        )
        fake_chezmoi.chmod(0o755)
        old_target = self.target.read_bytes()
        environment = {
            "HOME": str(self.home),
            "PATH": f"{bin_dir}:{os.environ.get('PATH', '')}",
            "TEST_CHEZMOI_CALLS": str(calls),
            "TEST_CODEX_TARGET": str(self.target),
        }
        with mock.patch.dict(os.environ, environment, clear=False):
            os.environ.pop("SECOND_BRAIN_CODEX_CONFIG_SOURCE", None)
            os.environ.pop("SECOND_BRAIN_CODEX_CONFIG_TARGET", None)
            result = snapshot_codex_config(dry_run=True)

        self.assertTrue(result.dry_run)
        self.assertTrue(result.changed)
        self.assertEqual(old_target, self.target.read_bytes())
        self.assertEqual(
            f"source-path {self.source}\n",
            calls.read_text(encoding="utf-8"),
        )

    def test_explicit_arguments_skip_chezmoi_resolution(self) -> None:
        with mock.patch(
            "scripts.second_brain.config_snapshot.subprocess.run"
        ) as run:
            result = snapshot_codex_config(
                dry_run=True,
                source_override=self.source,
                target_override=self.target,
            )

        self.assertTrue(result.changed)
        run.assert_not_called()

    def test_ambient_fixture_overrides_do_not_redirect_snapshot(self) -> None:
        decoy_source = self.root / "decoy" / ".codex" / "config.toml"
        decoy_target = self.root / "decoy-repo" / "dot_codex" / "config.toml"
        decoy_source.parent.mkdir(parents=True)
        decoy_target.parent.mkdir(parents=True)
        decoy_source.write_text('model = "decoy-source"\n', encoding="utf-8")
        decoy_target.write_text('model = "decoy-target"\n', encoding="utf-8")
        decoy_before = decoy_target.read_bytes()
        environment = {
            "HOME": str(self.home),
            "SECOND_BRAIN_CODEX_CONFIG_SOURCE": str(decoy_source),
            "SECOND_BRAIN_CODEX_CONFIG_TARGET": str(decoy_target),
        }
        with mock.patch.dict(os.environ, environment, clear=False), mock.patch(
            "scripts.second_brain.config_snapshot.subprocess.run",
            return_value=subprocess.CompletedProcess(
                ["chezmoi"], 0, stdout=f"{self.target}\n"
            ),
        ) as run:
            result = snapshot_codex_config(dry_run=True)

        self.assertTrue(result.changed)
        run.assert_called_once_with(
            ["chezmoi", "source-path", str(self.source)],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(decoy_before, decoy_target.read_bytes())

    def test_fixture_override_must_be_absolute(self) -> None:
        with self.assertRaisesRegex(ConfigSnapshotError, "must be absolute"):
            snapshot_codex_config(
                dry_run=True,
                source_override=Path(".codex/config.toml"),
                target_override=self.target,
            )

    def test_target_must_match_dot_codex_config_mapping(self) -> None:
        unexpected = self.root / "repo" / "somewhere" / "config.toml"
        unexpected.parent.mkdir()
        unexpected.write_text('model = "untouched"\n', encoding="utf-8")

        with self.assertRaisesRegex(ConfigSnapshotError, "unexpected target"):
            snapshot_codex_config(
                source_override=self.source,
                target_override=unexpected,
            )

        self.assertEqual(
            'model = "untouched"\n',
            unexpected.read_text(encoding="utf-8"),
        )

    def test_expected_target_rejects_another_repository_before_write(self) -> None:
        outside = self.root / "other-repo" / "dot_codex" / "config.toml"
        outside.parent.mkdir(parents=True)
        outside.write_text('model = "outside"\n', encoding="utf-8")
        before = outside.read_bytes()

        with self.assertRaisesRegex(ConfigSnapshotError, "expected repository"):
            snapshot_codex_config(
                source_override=self.source,
                target_override=outside,
                expected_target=self.target,
            )

        self.assertEqual(outside.read_bytes(), before)

    def test_source_must_be_one_regular_file(self) -> None:
        real_source = self.source.parent / "real.toml"
        self.source.rename(real_source)
        self.source.symlink_to(real_source)

        with self.assertRaisesRegex(ConfigSnapshotError, "regular file"):
            snapshot_codex_config(
                source_override=self.source,
                target_override=self.target,
            )

    def test_target_must_be_one_regular_file(self) -> None:
        real_target = self.target.parent / "real.toml"
        self.target.rename(real_target)
        self.target.symlink_to(real_target)

        with self.assertRaisesRegex(ConfigSnapshotError, "regular file"):
            snapshot_codex_config(
                source_override=self.source,
                target_override=self.target,
            )

    def test_hard_link_target_is_rejected(self) -> None:
        extra_link = self.target.parent / "config-copy.toml"
        os.link(self.target, extra_link)

        with self.assertRaisesRegex(ConfigSnapshotError, "regular file"):
            snapshot_codex_config(
                source_override=self.source,
                target_override=self.target,
            )

    def test_invalid_toml_is_rejected_before_target_changes(self) -> None:
        secret = "do-not-print-this-secret"
        self.source.write_text(f'api_key = "<redacted>', encoding="utf-8")
        before = self.target.read_bytes()

        with self.assertRaisesRegex(ConfigSnapshotError, "valid TOML") as error:
            snapshot_codex_config(
                source_override=self.source,
                target_override=self.target,
            )

        self.assertNotIn(secret, str(error.exception))
        self.assertEqual(before, self.target.read_bytes())

    def test_likely_secret_is_rejected_during_dry_run(self) -> None:
        secret = "sk-" + ("s" * 40)
        self.source.write_text(f'api_key = "<redacted>"\n', encoding="utf-8")
        before = self.target.read_bytes()

        with self.assertRaisesRegex(ConfigSnapshotError, "likely secret") as error:
            snapshot_codex_config(
                dry_run=True,
                source_override=self.source,
                target_override=self.target,
            )

        self.assertNotIn(secret, str(error.exception))
        self.assertEqual(before, self.target.read_bytes())

    def test_likely_secret_is_rejected_before_target_write(self) -> None:
        secret = "sk-" + ("s" * 40)
        self.source.write_text(f'api_key = "<redacted>"\n', encoding="utf-8")
        before = self.target.read_bytes()

        with self.assertRaisesRegex(ConfigSnapshotError, "likely secret") as error:
            snapshot_codex_config(
                source_override=self.source,
                target_override=self.target,
            )

        self.assertNotIn(secret, str(error.exception))
        self.assertEqual(before, self.target.read_bytes())

    def test_dry_run_validates_without_copying(self) -> None:
        before = self.target.read_bytes()

        result = snapshot_codex_config(
            dry_run=True,
            source_override=self.source,
            target_override=self.target,
        )

        self.assertTrue(result.dry_run)
        self.assertTrue(result.changed)
        self.assertEqual(before, self.target.read_bytes())

    def test_identical_content_is_a_noop(self) -> None:
        self.target.write_bytes(self.source.read_bytes())
        with mock.patch(
            "scripts.second_brain.config_snapshot.atomic_replace_if_unchanged"
        ) as replace:
            result = snapshot_codex_config(
                source_override=self.source,
                target_override=self.target,
            )

        self.assertFalse(result.changed)
        self.assertFalse(result.dry_run)
        replace.assert_not_called()

    def test_copy_uses_checksum_bound_atomic_replacement(self) -> None:
        old_target = self.target.read_bytes()
        target_mode = stat.S_IMODE(self.target.stat().st_mode)
        with mock.patch(
            "scripts.second_brain.config_snapshot.atomic_replace_if_unchanged"
        ) as replace:
            result = snapshot_codex_config(
                source_override=self.source,
                target_override=self.target,
            )

        self.assertTrue(result.changed)
        replace.assert_called_once_with(
            self.target.parent,
            self.target,
            hashlib.sha256(old_target).hexdigest(),
            self.source.read_bytes(),
            mode=target_mode,
            expected_mode=target_mode,
        )

    def test_copy_preserves_exact_bytes_and_target_mode(self) -> None:
        self.source.write_bytes(b'title = "caf\xc3\xa9"\n')
        self.target.chmod(0o640)

        result = snapshot_codex_config(
            source_override=self.source,
            target_override=self.target,
        )

        self.assertTrue(result.changed)
        self.assertEqual(self.source.read_bytes(), self.target.read_bytes())
        self.assertEqual(0o640, stat.S_IMODE(self.target.stat().st_mode))

    def test_transient_source_parent_swap_is_rejected(self) -> None:
        original_parent = self.source.parent
        saved_parent = self.home / ".codex-saved"
        alternate_parent = self.home / ".codex-alternate"
        alternate_parent.mkdir()
        (alternate_parent / "config.toml").write_text(
            'model = "attacker"\n', encoding="utf-8"
        )
        before = self.target.read_bytes()
        real_open = os.open
        swapped = False

        def transient_swap(path, *args, **kwargs):
            nonlocal swapped
            if not swapped and Path(path) == original_parent:
                original_parent.rename(saved_parent)
                alternate_parent.rename(original_parent)
                descriptor = real_open(path, *args, **kwargs)
                original_parent.rename(alternate_parent)
                saved_parent.rename(original_parent)
                swapped = True
                return descriptor
            return real_open(path, *args, **kwargs)

        with mock.patch.object(config_snapshot.os, "open", side_effect=transient_swap):
            with self.assertRaisesRegex(ConfigSnapshotError, "changed|unsafe"):
                snapshot_codex_config(
                    source_override=self.source,
                    target_override=self.target,
                )

        self.assertEqual(before, self.target.read_bytes())

    def test_exactly_one_million_source_bytes_is_rejected(self) -> None:
        self.source.write_bytes(b"#" + (b"a" * 999_998) + b"\n")
        before = self.target.read_bytes()

        with self.assertRaisesRegex(ConfigSnapshotError, "too large"):
            snapshot_codex_config(
                source_override=self.source,
                target_override=self.target,
            )

        self.assertEqual(before, self.target.read_bytes())

    def test_source_below_one_million_bytes_remains_valid(self) -> None:
        self.source.write_bytes(b"#" + (b"a" * 999_997) + b"\n")

        result = snapshot_codex_config(
            dry_run=True,
            source_override=self.source,
            target_override=self.target,
        )

        self.assertTrue(result.changed)
        self.assertTrue(result.dry_run)

    def test_target_mode_drift_after_preflight_is_rejected(self) -> None:
        self.target.chmod(0o640)
        before = self.target.read_bytes()
        original_validate = config_snapshot._validate_toml

        def drift_target_mode(content: bytes) -> None:
            original_validate(content)
            self.target.chmod(0o600)

        with mock.patch.object(
            config_snapshot,
            "_validate_toml",
            side_effect=drift_target_mode,
        ):
            with self.assertRaisesRegex(ConfigSnapshotError, "target.*changed"):
                snapshot_codex_config(
                    source_override=self.source,
                    target_override=self.target,
                )

        self.assertEqual(before, self.target.read_bytes())
        self.assertEqual(0o600, stat.S_IMODE(self.target.stat().st_mode))

    def test_target_mode_drift_at_atomic_boundary_is_rejected(self) -> None:
        self.target.chmod(0o640)
        before = self.target.read_bytes()
        real_replace = config_snapshot.atomic_replace_if_unchanged

        def drift_target_mode(
            root,
            target,
            expected_sha256,
            content,
            mode=0o644,
            expected_mode=None,
        ):
            self.target.chmod(0o600)
            return real_replace(
                root,
                target,
                expected_sha256,
                content,
                mode,
                expected_mode,
            )

        with mock.patch.object(
            config_snapshot,
            "atomic_replace_if_unchanged",
            side_effect=drift_target_mode,
        ):
            with self.assertRaisesRegex(
                ConfigSnapshotError,
                "atomic config snapshot failed",
            ):
                snapshot_codex_config(
                    source_override=self.source,
                    target_override=self.target,
                )

        self.assertEqual(before, self.target.read_bytes())
        self.assertEqual(0o600, stat.S_IMODE(self.target.stat().st_mode))

    def test_cli_output_never_contains_config_content(self) -> None:
        secret = "do-not-print-this-secret"
        self.source.write_text(f'api_key = "<redacted>', encoding="utf-8")
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        fake_chezmoi = bin_dir / "chezmoi"
        fake_chezmoi.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "printf '%s\\n' \"$TEST_CODEX_TARGET\"\n",
            encoding="utf-8",
        )
        fake_chezmoi.chmod(0o755)
        environment = os.environ.copy()
        environment.update(
            {
                "HOME": str(self.home),
                "PATH": f"{bin_dir}:{environment.get('PATH', '')}",
                "TEST_CODEX_TARGET": str(self.target),
            }
        )
        environment.pop("SECOND_BRAIN_CODEX_CONFIG_SOURCE", None)
        environment.pop("SECOND_BRAIN_CODEX_CONFIG_TARGET", None)

        completed = subprocess.run(
            [str(ENTRYPOINT), "--dry-run"],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )

        self.assertEqual(2, completed.returncode)
        self.assertNotIn(secret, completed.stdout)
        self.assertNotIn(secret, completed.stderr)
        self.assertEqual("", completed.stdout)
        self.assertEqual(
            "❌ snapshot-codex-config: snapshot validation failed\n",
            completed.stderr,
        )


if __name__ == "__main__":
    unittest.main()
