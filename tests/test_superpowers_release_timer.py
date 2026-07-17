#!/usr/bin/env python3

from __future__ import annotations

import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
UNIT_DIR = REPO_ROOT / "dot_config" / "systemd" / "user"
SERVICE = UNIT_DIR / "superpowers-release-sync.service"
TIMER = UNIT_DIR / "superpowers-release-sync.timer"
HELPER = REPO_ROOT / "scripts" / "executable_sync-superpowers-release"
SCRIPT = REPO_ROOT / "scripts" / "executable_setup-superpowers-release-timer"


class SuperpowersReleaseTimerTest(unittest.TestCase):
    def test_service_runs_installed_helper_with_standard_environment(self) -> None:
        service = SERVICE.read_text(encoding="utf-8")

        self.assertIn("Type=oneshot", service)
        self.assertIn("ExecStart=%h/scripts/sync-superpowers-release", service)
        self.assertIn("Environment=LINUX_CONFIG_SOURCE=%h/linux-config", service)
        self.assertIn(
            'Environment="PATH=%h/.local/bin:/usr/local/bin:/usr/bin:/bin"',
            service,
        )
        self.assertIn("StandardOutput=journal", service)
        self.assertIn("StandardError=journal", service)

    def test_timer_runs_service_daily_at_five_and_is_persistent(self) -> None:
        timer = TIMER.read_text(encoding="utf-8")

        self.assertIn("OnCalendar=*-*-* 05:00:00", timer)
        self.assertIn("Persistent=true", timer)
        self.assertIn("AccuracySec=1s", timer)
        self.assertIn("Unit=superpowers-release-sync.service", timer)
        self.assertIn("WantedBy=timers.target", timer)

    def test_units_pass_systemd_verification(self) -> None:
        completed = subprocess.run(
            ["systemd-analyze", "verify", str(SERVICE), str(TIMER)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)


class SuperpowersReleaseTimerSetupTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.home = self.root / "home"
        self.source = self.root / "linux-config"
        self.home.mkdir()
        self.source.mkdir()
        self.helper = self.home / "scripts" / "sync-superpowers-release"
        self.helper.parent.mkdir()
        self.helper.write_bytes(HELPER.read_bytes())
        self.helper.chmod(0o755)
        self.units = self.home / ".config" / "systemd" / "user"
        self.units.mkdir(parents=True)
        self.service = self.units / SERVICE.name
        self.timer = self.units / TIMER.name
        self.service.write_bytes(SERVICE.read_bytes())
        self.timer.write_bytes(TIMER.read_bytes())
        self.sources = self.root / "managed-sources"
        self.sources.mkdir()
        self.helper_source = self.sources / "executable_sync-superpowers-release"
        self.service_source = self.sources / SERVICE.name
        self.timer_source = self.sources / TIMER.name
        for source, managed in ((self.helper_source, HELPER), (self.service_source, SERVICE), (self.timer_source, TIMER)):
            shutil.copy2(managed, source)
        self.helper_source.chmod(0o755)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.log = self.root / "calls.log"
        self.log.touch()
        self._write_fakes()
        self.env = {
            **os.environ, "HOME": str(self.home), "LINUX_CONFIG_SOURCE": str(self.source),
            "XDG_STATE_HOME": str(self.root / "state"),
            "PATH": str(self.bin) + os.pathsep + os.environ["PATH"],
            "TEST_CALL_LOG": str(self.log), "TEST_HELPER": str(self.helper),
            "TEST_SERVICE": str(self.service), "TEST_TIMER": str(self.timer),
            "TEST_HELPER_SOURCE": str(self.helper_source),
            "TEST_SERVICE_SOURCE": str(self.service_source),
            "TEST_TIMER_SOURCE": str(self.timer_source), "PYTHONDONTWRITEBYTECODE": "1",
        }

    def _write(self, name: str, content: str) -> None:
        path = self.bin / name
        path.write_text(content, encoding="utf-8")
        path.chmod(0o755)

    def _write_fakes(self) -> None:
        self._write("chezmoi", """#!/usr/bin/env bash
set -euo pipefail
{ printf 'chezmoi'; printf ' %s' "$@"; printf '\n'; } >> "$TEST_CALL_LOG"
case "${1:-}" in
-S)
  [ "$2" = "${TEST_EXPECTED_SOURCE:-$LINUX_CONFIG_SOURCE}" ] || exit 64
  case "${3:-}" in
  source-path) case "${4:-}" in
    "$TEST_HELPER") printf '%s\n' "$TEST_HELPER_SOURCE" ;;
    "$TEST_SERVICE") printf '%s\n' "$TEST_SERVICE_SOURCE" ;;
    "$TEST_TIMER") printf '%s\n' "$TEST_TIMER_SOURCE" ;; *) exit 64 ;; esac ;;
  apply) [ "$#" = 7 ] && [ "$4" = --parent-dirs ] &&
    [ "$5" = "$TEST_HELPER" ] && [ "$6" = "$TEST_SERVICE" ] &&
    [ "$7" = "$TEST_TIMER" ] || exit 64 ;;
  *) exit 64 ;;
  esac ;;
*) exit 64 ;;
esac
""")
        self._write("systemd-analyze", """#!/usr/bin/env bash
set -euo pipefail
{ printf 'systemd-analyze'; printf ' %s' "$@"; printf '\n'; } >> "$TEST_CALL_LOG"
[ "$#" = 4 ] && [ "$1" = --user ] && [ "$2" = verify ] &&
[ "$3" = "$TEST_SERVICE" ] && [ "$4" = "$TEST_TIMER" ] || exit 64
if [ "${TEST_ANALYZE_FAIL:-0}" = 1 ]; then
printf 'PRIVATE_NOTE_AND_CONFIG_CONTENT_MUST_NOT_LEAK\n' >&2; exit 1; fi
""")
        self._write("systemctl", """#!/usr/bin/env bash
set -euo pipefail
{ printf 'systemctl'; printf ' %s' "$@"; printf '\n'; } >> "$TEST_CALL_LOG"
case "$*" in
'--user daemon-reload') [ "${TEST_SYSTEMCTL_FAIL:-0}" != 1 ] || {
printf 'PRIVATE_NOTE_AND_CONFIG_CONTENT_MUST_NOT_LEAK\n' >&2; exit 1; } ;;
'--user enable --now superpowers-release-sync.timer') ;;
'--user disable --now superpowers-release-sync.timer')
[ "${TEST_ALREADY_DISABLED:-0}" != 1 ] || { printf 'Unit superpowers-release-sync.timer is not loaded.\n' >&2; exit 1; } ;;
*) exit 64 ;; esac
""")

    def run_script(self, *arguments: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run([str(SCRIPT), *arguments], cwd=self.root,
            env=self.env if env is None else env, text=True, capture_output=True, check=False)

    def calls(self) -> list[str]:
        return self.log.read_text(encoding="utf-8").splitlines()

    def test_action_is_required_and_exclusive(self) -> None:
        self.assertEqual(self.run_script().returncode, 2)
        self.assertEqual(self.run_script("--check", "--enable").returncode, 2)
        self.assertEqual(self.calls(), [])

    def test_check_resolves_sources_and_verifies_installed_units(self) -> None:
        completed = self.run_script("--check")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "Superpowers release timer units are valid.\n")
        self.assertEqual(self.calls(), [
            f"chezmoi -S {self.source} source-path {self.helper}",
            f"chezmoi -S {self.source} source-path {self.service}",
            f"chezmoi -S {self.source} source-path {self.timer}",
            f"systemd-analyze --user verify {self.service} {self.timer}",
        ])

    def test_enable_applies_exact_targets_before_activation(self) -> None:
        completed = self.run_script("--enable")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "Superpowers release timer enabled.\n")
        self.assertEqual(self.calls(), [
            f"chezmoi -S {self.source} source-path {self.helper}",
            f"chezmoi -S {self.source} source-path {self.service}",
            f"chezmoi -S {self.source} source-path {self.timer}",
            f"chezmoi -S {self.source} apply --parent-dirs {self.helper} {self.service} {self.timer}",
            "systemctl --user daemon-reload",
            "systemctl --user enable --now superpowers-release-sync.timer",
            f"systemd-analyze --user verify {self.service} {self.timer}",
        ])

    def test_disable_is_idempotent_without_chezmoi_or_source(self) -> None:
        env = {**self.env, "LINUX_CONFIG_SOURCE": str(self.root / "missing"), "TEST_ALREADY_DISABLED": "1"}
        first, second = self.run_script("--disable", env=env), self.run_script("--disable", env=env)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout, "Superpowers release timer disabled.\n")
        self.assertEqual(self.calls(), [
            "systemctl --user disable --now superpowers-release-sync.timer",
            "systemctl --user disable --now superpowers-release-sync.timer",
        ])

    def test_check_rejects_symlinked_or_missing_unit_sources(self) -> None:
        for mode in ("symlink", "missing"):
            with self.subTest(mode=mode):
                if mode == "symlink":
                    outside = self.root / "outside.service"
                    outside.write_text("[Service]\n", encoding="utf-8")
                    self.service_source.unlink()
                    self.service_source.symlink_to(outside)
                else:
                    self.service_source.unlink()
                completed = self.run_script("--check")
                self.assertEqual(completed.returncode, 2)
                self.assertIn("chezmoi managed source is", completed.stderr)
                self.assertFalse(any("systemd-analyze" in call for call in self.calls()))
                self.log.write_text("", encoding="utf-8")
                if self.service_source.is_symlink():
                    self.service_source.unlink()
                shutil.copy2(SERVICE, self.service_source)

    def test_child_failures_are_sanitized_and_actionable(self) -> None:
        for arguments, env, error in (
            (("--check",), {**self.env, "TEST_ANALYZE_FAIL": "1"}, "systemd unit validation failed"),
            (("--enable",), {**self.env, "TEST_SYSTEMCTL_FAIL": "1"}, "systemd user daemon reload failed"),
        ):
            with self.subTest(arguments=arguments):
                completed = self.run_script(*arguments, env=env)
                self.assertEqual(completed.returncode, 2)
                self.assertIn(error, completed.stderr)
                self.assertNotIn("PRIVATE_NOTE_AND_CONFIG_CONTENT", completed.stderr)
                self.log.write_text("", encoding="utf-8")

    def test_enable_rejects_non_executable_helper_source_and_creates_private_lock(self) -> None:
        self.helper_source.chmod(0o644)
        failed = self.run_script("--check")
        self.assertEqual(failed.returncode, 2)
        self.assertIn("chezmoi helper source is not executable", failed.stderr)
        self.helper_source.chmod(0o755)
        completed = self.run_script("--enable")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        lock = self.root / "state" / "superpowers-release-sync" / "locks" / "timer-setup.lock"
        self.assertEqual(stat.S_IMODE(lock.parent.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(lock.stat().st_mode), 0o600)

    def test_check_does_not_create_state(self) -> None:
        state_home = Path(self.env["XDG_STATE_HOME"])
        self.assertFalse(state_home.exists())

        completed = self.run_script("--check")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertFalse(state_home.exists())

    def test_check_rejects_mismatched_chezmoi_source(self) -> None:
        env = {
            **self.env,
            "TEST_EXPECTED_SOURCE": str(self.root / "different-source"),
        }

        completed = self.run_script("--check", env=env)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("chezmoi managed source resolution failed", completed.stderr)
        self.assertEqual(
            self.calls(),
            [f"chezmoi -S {self.source} source-path {self.helper}"],
        )

    def test_check_rejects_executable_prefix_for_units(self) -> None:
        for source, key in (
            (self.service_source, "TEST_SERVICE_SOURCE"),
            (self.timer_source, "TEST_TIMER_SOURCE"),
        ):
            with self.subTest(source=source.name):
                renamed = source.with_name(f"executable_{source.name}")
                source.rename(renamed)
                env = {**self.env, key: str(renamed)}

                completed = self.run_script("--check", env=env)

                self.assertEqual(completed.returncode, 2)
                self.assertIn("chezmoi managed source is unsafe", completed.stderr)
                self.log.write_text("", encoding="utf-8")
                renamed.rename(source)

if __name__ == "__main__":
    unittest.main()
