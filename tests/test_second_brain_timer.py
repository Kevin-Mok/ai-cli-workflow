#!/usr/bin/env python3

from __future__ import annotations

import fcntl
import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "executable_setup-second-brain-timer"
CHECKPOINT_LAUNCHER = REPO_ROOT / "scripts" / "executable_second-brain"
RUNTIME_PACKAGE = REPO_ROOT / "scripts" / "second_brain"
RUNTIME_MODULE_NAMES = tuple(
    sorted(
        path.name
        for path in RUNTIME_PACKAGE.glob("*.py")
        if not path.name.startswith("remove_")
    )
)
LEGACY_RUNTIME_TARGET_NAME = "state.py"
SERVICE = (
    REPO_ROOT
    / "dot_config"
    / "systemd"
    / "user"
    / "second-brain-checkpoint.service"
)
TIMER = (
    REPO_ROOT
    / "dot_config"
    / "systemd"
    / "user"
    / "second-brain-checkpoint.timer"
)


class SecondBrainTimerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.launcher_target = self.home / "scripts" / "second-brain"
        self.launcher_target.parent.mkdir()
        self.launcher_target.write_bytes(CHECKPOINT_LAUNCHER.read_bytes())
        self.launcher_target.chmod(0o755)
        self.runtime_package_target = self.launcher_target.parent / "second_brain"
        self.runtime_package_target.mkdir()
        for name in RUNTIME_MODULE_NAMES:
            shutil.copy2(
                RUNTIME_PACKAGE / name,
                self.runtime_package_target / name,
            )
        self.unit_target_dir = self.home / ".config" / "systemd" / "user"
        self.unit_target_dir.mkdir(parents=True)
        self.service_target = self.unit_target_dir / SERVICE.name
        self.timer_target = self.unit_target_dir / TIMER.name
        self.service_target.write_bytes(SERVICE.read_bytes())
        self.timer_target.write_bytes(TIMER.read_bytes())
        self.service_target.chmod(0o644)
        self.timer_target.chmod(0o644)
        self.state_home = self.root / "state"
        self.fake_bin = self.root / "bin"
        self.fake_bin.mkdir()
        self.call_log = self.root / "calls.log"
        self.call_log.touch()
        self._write_fake_commands()
        self.env = {
            **os.environ,
            "HOME": str(self.home),
            "XDG_STATE_HOME": str(self.state_home),
            "PATH": f"{self.fake_bin}{os.pathsep}{os.environ['PATH']}",
            "TEST_CALL_LOG": str(self.call_log),
            "TEST_LAUNCHER_SOURCE": str(CHECKPOINT_LAUNCHER),
            "TEST_LAUNCHER_TARGET": str(self.launcher_target),
            "TEST_RUNTIME_PACKAGE_SOURCE": str(RUNTIME_PACKAGE),
            "TEST_RUNTIME_PACKAGE_TARGET": str(self.runtime_package_target),
            "TEST_SERVICE_SOURCE": str(SERVICE),
            "TEST_SERVICE_TARGET": str(self.service_target),
            "TEST_TIMER_SOURCE": str(TIMER),
            "TEST_TIMER_TARGET": str(self.timer_target),
            "PYTHONDONTWRITEBYTECODE": "1",
        }

    def _write_executable(self, name: str, content: str) -> None:
        path = self.fake_bin / name
        path.write_text(content, encoding="utf-8")
        path.chmod(0o755)

    def _write_fake_commands(self) -> None:
        self._write_executable(
            "chezmoi",
            """#!/usr/bin/env bash
set -euo pipefail
printf 'chezmoi' >> "$TEST_CALL_LOG"
printf ' %s' "$@" >> "$TEST_CALL_LOG"
printf '\n' >> "$TEST_CALL_LOG"
case "${1:-}" in
  source-path)
    case "${2:-}" in
      */.codex/config.toml) printf '%s\n' "$TEST_CONFIG_TARGET" ;;
      */scripts/second_brain) printf '%s\n' "$TEST_RUNTIME_PACKAGE_SOURCE" ;;
      */scripts/second-brain) printf '%s\n' "$TEST_LAUNCHER_SOURCE" ;;
      *second-brain-checkpoint.service) printf '%s\n' "$TEST_SERVICE_SOURCE" ;;
      *second-brain-checkpoint.timer) printf '%s\n' "$TEST_TIMER_SOURCE" ;;
      *) exit 64 ;;
    esac
    ;;
  apply)
    case " $* " in
      *" --parent-dirs "*)
        chmod 0775 "${TEST_RUNTIME_PACKAGE_TARGET%/*}"
        if [ ! -d "$TEST_RUNTIME_PACKAGE_TARGET" ]; then
          mkdir -p "$TEST_RUNTIME_PACKAGE_TARGET"
        fi
        chmod 0775 "$TEST_RUNTIME_PACKAGE_TARGET"
        ;;
    esac
    if [ "${TEST_INSTALL_RUNTIME_PACKAGE:-0}" = "1" ]; then
      [ -d "$TEST_RUNTIME_PACKAGE_TARGET" ] || exit 92
      for source in "$TEST_RUNTIME_PACKAGE_SOURCE"/*.py; do
        case "$(basename "$source")" in remove_*) continue ;; esac
        target="$TEST_RUNTIME_PACKAGE_TARGET/$(basename "$source")"
        case " $* " in
          *" $target "*) cp "$source" "$target" ;;
        esac
      done
    fi
    case " $* " in
      *" $TEST_RUNTIME_PACKAGE_TARGET/state.py "*)
        rm -f "$TEST_RUNTIME_PACKAGE_TARGET/state.py"
        ;;
    esac
    if [ "${TEST_INSTALL_LAUNCHER:-0}" = "1" ]; then
      case " $* " in
        *" $TEST_LAUNCHER_TARGET "*)
          mkdir -p "$(dirname "$TEST_LAUNCHER_TARGET")"
          cp "$TEST_LAUNCHER_SOURCE" "$TEST_LAUNCHER_TARGET"
          chmod 0755 "$TEST_LAUNCHER_TARGET"
          ;;
      esac
    fi
    if [ "${TEST_INSTALL_UNITS:-0}" = "1" ]; then
      case " $* " in
        *" $TEST_SERVICE_TARGET "*)
          cp "$TEST_SERVICE_SOURCE" "$TEST_SERVICE_TARGET"
          ;;
      esac
      case " $* " in
        *" $TEST_TIMER_TARGET "*)
          cp "$TEST_TIMER_SOURCE" "$TEST_TIMER_TARGET"
          ;;
      esac
    fi
    ;;
  *)
    exit 64
    ;;
esac
""",
        )
        self._write_executable(
            "systemd-analyze",
            """#!/usr/bin/env bash
set -euo pipefail
printf 'systemd-analyze' >> "$TEST_CALL_LOG"
printf ' %s' "$@" >> "$TEST_CALL_LOG"
printf '\n' >> "$TEST_CALL_LOG"
if [ "${TEST_ANALYZE_FAIL:-0}" = "1" ]; then
  printf 'PRIVATE_NOTE_AND_CONFIG_CONTENT_MUST_NOT_LEAK\n' >&2
  exit 1
fi
""",
        )
        self._write_executable(
            "systemctl",
            """#!/usr/bin/env bash
set -euo pipefail
printf 'systemctl' >> "$TEST_CALL_LOG"
printf ' %s' "$@" >> "$TEST_CALL_LOG"
printf '\n' >> "$TEST_CALL_LOG"
if [ "${TEST_REQUIRE_RUNTIME_PACKAGE_AT_ENABLE:-0}" = "1" ] &&
   [ "${1:-}" = "--user" ] &&
   [ "${2:-}" = "enable" ] &&
   [ "${3:-}" = "--now" ]; then
  for source in "$TEST_RUNTIME_PACKAGE_SOURCE"/*.py; do
    case "$(basename "$source")" in remove_*) continue ;; esac
    target="$TEST_RUNTIME_PACKAGE_TARGET/$(basename "$source")"
    cmp -s "$source" "$target" || exit 91
  done
fi
""",
        )
        self._write_executable(
            "sudo",
            """#!/usr/bin/env bash
set -euo pipefail
printf 'sudo' >> "$TEST_CALL_LOG"
printf ' %s' "$@" >> "$TEST_CALL_LOG"
printf '\n' >> "$TEST_CALL_LOG"
exit 99
""",
        )

    def run_script(
        self,
        *arguments: str,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(SCRIPT), *arguments],
            cwd=self.root,
            env=self.env if env is None else env,
            text=True,
            capture_output=True,
            check=False,
        )

    def calls(self) -> list[str]:
        return self.call_log.read_text(encoding="utf-8").splitlines()

    def test_units_define_exact_local_1620_persistent_schedule(self) -> None:
        timer = TIMER.read_text(encoding="utf-8")
        self.assertIn("OnCalendar=*-*-* 16:20:00", timer)
        self.assertIn("Persistent=true", timer)
        self.assertIn("Unit=second-brain-checkpoint.service", timer)
        self.assertIn("WantedBy=timers.target", timer)
        self.assertNotIn("Timezone=", timer)
        self.assertNotIn("UTC", timer)

    def test_service_is_content_safe_user_level_direct_launcher(self) -> None:
        service = SERVICE.read_text(encoding="utf-8")
        self.assertIn("Type=oneshot", service)
        self.assertIn(
            "ExecStart=/usr/bin/env %h/scripts/second-brain checkpoint",
            service,
        )
        self.assertIn("StandardOutput=journal", service)
        self.assertIn("StandardError=journal", service)
        self.assertIn("SyslogIdentifier=second-brain-checkpoint", service)
        self.assertIn(
            'Environment="PATH=%h/.local/bin:/usr/local/bin:/usr/bin:/bin"',
            service,
        )
        self.assertIn("UMask=0077", service)
        for unsafe in ("sudo", "sh -c", "bash -c", "cat ", "config.toml"):
            self.assertNotIn(unsafe, service)

    def test_units_validate_before_home_launcher_is_installed(self) -> None:
        completed = subprocess.run(
            [
                "systemd-analyze",
                "--user",
                "verify",
                str(SERVICE),
                str(TIMER),
            ],
            cwd=self.root,
            env={**os.environ, "HOME": str(self.home)},
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_help_exposes_check_enable_disable_and_never_mentions_sudo(self) -> None:
        completed = self.run_script("--help")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        for option in ("--check", "--enable", "--disable"):
            self.assertIn(option, completed.stdout)
        self.assertNotIn("sudo", completed.stdout.casefold())
        self.assertEqual(self.calls(), [])

    def test_check_is_idempotent_uses_chezmoi_sources_and_xdg_lock(self) -> None:
        first = self.run_script("--check")
        second = self.run_script("--check")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout, "Second Brain timer units are valid.\n")
        self.assertEqual(second.stdout, first.stdout)

        service_target = self.unit_target_dir / SERVICE.name
        timer_target = self.unit_target_dir / TIMER.name
        expected_once = [
            f"chezmoi source-path {self.launcher_target}",
            f"chezmoi source-path {self.runtime_package_target}",
            f"chezmoi source-path {service_target}",
            f"chezmoi source-path {timer_target}",
            f"systemd-analyze --user verify {SERVICE} {TIMER}",
            "systemctl --user show-environment",
            (
                "systemd-analyze --user verify "
                f"{service_target} {timer_target}"
            ),
        ]
        self.assertEqual(self.calls(), expected_once * 2)
        self.assertFalse(any(" apply " in call for call in self.calls()))
        self.assertFalse(any("enable" in call for call in self.calls()))
        self.assertFalse(any(call.startswith("sudo") for call in self.calls()))

        lock_dir = self.state_home / "second-brain" / "locks"
        lock_file = lock_dir / "timer-setup.lock"
        self.assertEqual(stat.S_IMODE(lock_dir.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(lock_file.stat().st_mode), 0o600)

    def test_enable_applies_only_exact_chezmoi_targets_and_is_idempotent(self) -> None:
        first = self.run_script("--enable")
        second = self.run_script("--enable")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout, "Second Brain timer enabled.\n")
        self.assertEqual(second.stdout, first.stdout)

        service_target = self.unit_target_dir / SERVICE.name
        timer_target = self.unit_target_dir / TIMER.name
        module_targets = [
            self.runtime_package_target / name
            for name in RUNTIME_MODULE_NAMES
        ]
        expected_once = [
            f"chezmoi source-path {self.launcher_target}",
            f"chezmoi source-path {self.runtime_package_target}",
            f"chezmoi source-path {service_target}",
            f"chezmoi source-path {timer_target}",
            f"systemd-analyze --user verify {SERVICE} {TIMER}",
            "systemctl --user show-environment",
            "chezmoi apply "
            + " ".join(
                [
                    str(self.launcher_target),
                    *(str(path) for path in module_targets),
                    str(
                        self.runtime_package_target
                        / LEGACY_RUNTIME_TARGET_NAME
                    ),
                    str(service_target),
                    str(timer_target),
                ]
            ),
            (
                "systemd-analyze --user verify "
                f"{service_target} {timer_target}"
            ),
            "systemctl --user daemon-reload",
            "systemctl --user enable --now second-brain-checkpoint.timer",
        ]
        self.assertEqual(self.calls(), expected_once * 2)
        self.assertFalse(any(call.startswith("sudo") for call in self.calls()))

    def test_enable_installs_and_validates_launcher_with_units(self) -> None:
        self.launcher_target.unlink()
        env = {**self.env, "TEST_INSTALL_LAUNCHER": "1"}

        completed = self.run_script("--enable", env=env)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(self.launcher_target.is_file())
        self.assertTrue(os.access(self.launcher_target, os.X_OK))
        apply_calls = [call for call in self.calls() if " apply " in call]
        self.assertEqual(len(apply_calls), 1)
        self.assertIn(str(self.launcher_target), apply_calls[0])

    def test_check_rejects_missing_installed_launcher_without_mutation(self) -> None:
        self.launcher_target.unlink()

        completed = self.run_script("--check")

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "")
        self.assertIn(
            "installed Second Brain command is missing or not executable",
            completed.stderr,
        )
        self.assertFalse(any(" apply " in call for call in self.calls()))
        self.assertFalse(any("enable" in call for call in self.calls()))

    def test_check_rejects_stale_installed_launcher_without_mutation(self) -> None:
        self.launcher_target.write_text(
            "#!/usr/bin/env bash\nexit 0\n",
            encoding="utf-8",
        )
        self.launcher_target.chmod(0o755)

        completed = self.run_script("--check")

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "")
        self.assertIn(
            "installed Second Brain command is missing or not executable",
            completed.stderr,
        )
        self.assertFalse(any(" apply " in call for call in self.calls()))
        self.assertFalse(any("enable" in call for call in self.calls()))

    def test_enable_rejects_noop_apply_that_leaves_launcher_stale(self) -> None:
        self.launcher_target.write_text(
            "#!/usr/bin/env bash\nexit 0\n",
            encoding="utf-8",
        )
        self.launcher_target.chmod(0o755)

        completed = self.run_script("--enable")

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "")
        self.assertIn(
            "installed Second Brain command is missing or not executable",
            completed.stderr,
        )
        self.assertFalse(any("daemon-reload" in call for call in self.calls()))
        self.assertFalse(any("enable --now" in call for call in self.calls()))

    def test_enable_rejects_stale_runtime_package_before_activation(self) -> None:
        stale_module = self.runtime_package_target / "checkpoint.py"
        stale_module.write_text("# stale installed module\n", encoding="utf-8")

        completed = self.run_script("--enable")

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "")
        self.assertIn(
            "installed Second Brain runtime package is missing or stale",
            completed.stderr,
        )
        self.assertIn(
            f"chezmoi source-path {self.runtime_package_target}",
            self.calls(),
        )
        apply_call = next(call for call in self.calls() if " apply " in call)
        self.assertIn(str(self.runtime_package_target), apply_call)
        self.assertFalse(any("daemon-reload" in call for call in self.calls()))
        self.assertFalse(any("enable --now" in call for call in self.calls()))

    def test_enable_rejects_incomplete_runtime_source_before_apply(self) -> None:
        source = self.root / "incomplete-runtime-source" / "second_brain"
        shutil.copytree(
            RUNTIME_PACKAGE,
            source,
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        (source / "checkpoint_git.py").unlink()
        env = {**self.env, "TEST_RUNTIME_PACKAGE_SOURCE": str(source)}

        completed = self.run_script("--enable", env=env)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("runtime package source is incomplete", completed.stderr)
        self.assertFalse(any(" apply " in call for call in self.calls()))
        self.assertFalse(any("enable --now" in call for call in self.calls()))

    def test_enable_rejects_unexpected_runtime_source_before_apply(self) -> None:
        source = self.root / "unexpected-runtime-source" / "second_brain"
        shutil.copytree(
            RUNTIME_PACKAGE,
            source,
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        (source / "unexpected.py").write_text(
            "# Unreviewed runtime module\n",
            encoding="utf-8",
        )
        env = {**self.env, "TEST_RUNTIME_PACKAGE_SOURCE": str(source)}

        completed = self.run_script("--enable", env=env)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("runtime package source is incomplete", completed.stderr)
        self.assertFalse(any(" apply " in call for call in self.calls()))
        self.assertFalse(any("enable --now" in call for call in self.calls()))

    def test_enable_rejects_unexpected_installed_runtime_module(self) -> None:
        (self.runtime_package_target / "unexpected.py").write_text(
            "# Stale installed module\n",
            encoding="utf-8",
        )

        completed = self.run_script("--enable")

        self.assertEqual(completed.returncode, 2)
        self.assertIn(
            "installed Second Brain runtime package is missing or stale",
            completed.stderr,
        )
        self.assertFalse(any("daemon-reload" in call for call in self.calls()))
        self.assertFalse(any("enable --now" in call for call in self.calls()))

    def test_enable_rejects_installed_runtime_shadow_entries(self) -> None:
        for kind in ("extension", "package", "symlink"):
            with self.subTest(kind=kind):
                shadow = self.runtime_package_target / "checkpoint_git.so"
                if kind == "extension":
                    shadow.write_bytes(b"unreviewed native extension")
                elif kind == "package":
                    shadow = self.runtime_package_target / "checkpoint_git"
                    shadow.mkdir()
                    (shadow / "__init__.py").write_text(
                        "# Unreviewed package shadow.\n",
                        encoding="utf-8",
                    )
                else:
                    shadow.symlink_to(
                        self.runtime_package_target / "checkpoint_git.py"
                    )

                completed = self.run_script("--enable")
                calls = self.calls()
                if shadow.is_dir() and not shadow.is_symlink():
                    shutil.rmtree(shadow)
                else:
                    shadow.unlink()
                self.call_log.write_text("", encoding="utf-8")

                self.assertEqual(completed.returncode, 2)
                self.assertIn(
                    "installed Second Brain runtime package is missing or stale",
                    completed.stderr,
                )
                self.assertFalse(
                    any("daemon-reload" in call for call in calls)
                )
                self.assertFalse(
                    any("enable --now" in call for call in calls)
                )

    def test_enable_rejects_symlinked_runtime_bytecode_cache(self) -> None:
        external_cache = self.root / "external-cache"
        external_cache.mkdir()
        (self.runtime_package_target / "__pycache__").symlink_to(
            external_cache,
            target_is_directory=True,
        )

        completed = self.run_script("--enable")

        self.assertEqual(completed.returncode, 2)
        self.assertIn(
            "installed Second Brain runtime package is missing or stale",
            completed.stderr,
        )
        self.assertFalse(any("daemon-reload" in call for call in self.calls()))
        self.assertFalse(any("enable --now" in call for call in self.calls()))

    def test_enable_allows_real_runtime_bytecode_cache_directory(self) -> None:
        bytecode = self.runtime_package_target / "__pycache__"
        bytecode.mkdir()
        (bytecode / "checkpoint_git.cpython-312.pyc").write_bytes(
            b"generated bytecode fixture"
        )

        completed = self.run_script("--enable")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn(
            "systemctl --user enable --now second-brain-checkpoint.timer",
            self.calls(),
        )

    def test_enable_installs_exact_runtime_package_before_activation(self) -> None:
        self.launcher_target.parent.chmod(0o700)
        shutil.rmtree(self.runtime_package_target)
        env = {
            **self.env,
            "TEST_INSTALL_RUNTIME_PACKAGE": "1",
            "TEST_REQUIRE_RUNTIME_PACKAGE_AT_ENABLE": "1",
        }

        completed = self.run_script("--enable", env=env)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(
            stat.S_IMODE(self.launcher_target.parent.stat().st_mode),
            0o700,
        )
        self.assertEqual(
            stat.S_IMODE(self.runtime_package_target.stat().st_mode),
            0o755,
        )
        sources = [RUNTIME_PACKAGE / name for name in RUNTIME_MODULE_NAMES]
        self.assertEqual(
            [path.name for path in sorted(self.runtime_package_target.glob("*.py"))],
            [path.name for path in sources],
        )
        for source in sources:
            target = self.runtime_package_target / source.name
            self.assertEqual(target.read_bytes(), source.read_bytes())
        apply_call = next(call for call in self.calls() if " apply " in call)
        for source in sources:
            self.assertIn(
                str(self.runtime_package_target / source.name),
                apply_call,
            )
        self.assertIn(
            "systemctl --user enable --now second-brain-checkpoint.timer",
            self.calls(),
        )

    def test_enable_rejects_symlinked_runtime_package_before_apply(self) -> None:
        shutil.rmtree(self.runtime_package_target)
        outside = self.root / "outside-runtime"
        outside.mkdir()
        self.runtime_package_target.symlink_to(outside, target_is_directory=True)

        completed = self.run_script("--enable")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("timer install parent is unsafe", completed.stderr)
        self.assertFalse(any(" apply " in call for call in self.calls()))
        self.assertEqual(list(outside.iterdir()), [])

    def test_enable_rejects_symlinked_scripts_parent_before_apply(self) -> None:
        real_scripts = self.home / "real-scripts"
        self.launcher_target.parent.rename(real_scripts)
        self.launcher_target.parent.symlink_to(
            real_scripts,
            target_is_directory=True,
        )

        completed = self.run_script("--enable")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("timer install parent is unsafe", completed.stderr)
        self.assertFalse(any(" apply " in call for call in self.calls()))

    def test_enable_rejects_non_directory_runtime_parent_before_apply(self) -> None:
        shutil.rmtree(self.runtime_package_target)
        self.runtime_package_target.write_text(
            "not a directory\n",
            encoding="utf-8",
        )

        completed = self.run_script("--enable")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("timer install parent is unsafe", completed.stderr)
        self.assertFalse(any(" apply " in call for call in self.calls()))

    def test_enable_rolls_back_created_parents_when_later_parent_is_unsafe(
        self,
    ) -> None:
        shutil.rmtree(self.home / "scripts")
        shutil.rmtree(self.home / ".config")
        outside = self.root / "outside-config"
        outside.mkdir()
        (self.home / ".config").symlink_to(
            outside,
            target_is_directory=True,
        )

        completed = self.run_script("--enable")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("timer install parent is unsafe", completed.stderr)
        self.assertFalse((self.home / "scripts").exists())
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse(any(" apply " in call for call in self.calls()))
        self.assertFalse(any("enable --now" in call for call in self.calls()))

    def test_enable_creates_all_missing_install_parents(self) -> None:
        shutil.rmtree(self.home / "scripts")
        shutil.rmtree(self.home / ".config")
        env = {
            **self.env,
            "TEST_INSTALL_LAUNCHER": "1",
            "TEST_INSTALL_RUNTIME_PACKAGE": "1",
            "TEST_INSTALL_UNITS": "1",
            "TEST_REQUIRE_RUNTIME_PACKAGE_AT_ENABLE": "1",
        }

        completed = self.run_script("--enable", env=env)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        for directory in (
            self.home / "scripts",
            self.runtime_package_target,
            self.home / ".config",
            self.home / ".config/systemd",
            self.unit_target_dir,
        ):
            self.assertTrue(directory.is_dir())
            self.assertFalse(directory.is_symlink())
            self.assertEqual(stat.S_IMODE(directory.stat().st_mode), 0o755)
        self.assertTrue(self.launcher_target.is_file())
        self.assertTrue(self.service_target.is_file())
        self.assertTrue(self.timer_target.is_file())
        apply_call = next(call for call in self.calls() if " apply " in call)
        self.assertNotIn("--parent-dirs", apply_call)

    def test_check_rejects_missing_installed_unit_without_mutation(self) -> None:
        self.service_target.unlink()

        completed = self.run_script("--check")

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "")
        self.assertIn("installed systemd units are missing or stale", completed.stderr)
        self.assertFalse(any(" apply " in call for call in self.calls()))
        self.assertFalse(any("enable" in call for call in self.calls()))

    def test_enable_rejects_noop_apply_that_leaves_units_missing(self) -> None:
        self.service_target.unlink()
        self.timer_target.unlink()

        completed = self.run_script("--enable")

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "")
        self.assertIn("installed systemd units are missing or stale", completed.stderr)
        self.assertFalse(any("daemon-reload" in call for call in self.calls()))
        self.assertFalse(any("enable --now" in call for call in self.calls()))

    def test_enable_verifies_units_installed_by_chezmoi(self) -> None:
        self.service_target.unlink()
        self.timer_target.unlink()
        env = {**self.env, "TEST_INSTALL_UNITS": "1"}

        completed = self.run_script("--enable", env=env)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(self.service_target.read_bytes(), SERVICE.read_bytes())
        self.assertEqual(self.timer_target.read_bytes(), TIMER.read_bytes())
        self.assertIn(
            "systemd-analyze --user verify "
            f"{self.service_target} {self.timer_target}",
            self.calls(),
        )

    def test_disable_is_idempotent_and_does_not_require_chezmoi(self) -> None:
        first = self.run_script("--disable")
        second = self.run_script("--disable")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout, "Second Brain timer disabled.\n")
        self.assertEqual(second.stdout, first.stdout)
        self.assertEqual(
            self.calls(),
            [
                "systemctl --user show-environment",
                "systemctl --user disable --now second-brain-checkpoint.timer",
                "systemctl --user show-environment",
                "systemctl --user disable --now second-brain-checkpoint.timer",
            ],
        )
        self.assertFalse(any(call.startswith("sudo") for call in self.calls()))

    def test_installed_disable_works_without_source_repo_or_chezmoi(self) -> None:
        installed = self.home / "scripts" / "setup-second-brain-timer"
        installed.write_bytes(SCRIPT.read_bytes())
        installed.chmod(0o755)

        completed = subprocess.run(
            [str(installed), "--disable"],
            cwd=self.root,
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "Second Brain timer disabled.\n")
        self.assertEqual(
            self.calls(),
            [
                "systemctl --user show-environment",
                "systemctl --user disable --now second-brain-checkpoint.timer",
            ],
        )
        self.assertFalse(any(call.startswith("chezmoi") for call in self.calls()))

    def test_lock_contention_fails_without_system_actions(self) -> None:
        lock_dir = self.state_home / "second-brain" / "locks"
        lock_dir.mkdir(parents=True, mode=0o700)
        lock_dir.chmod(0o700)
        lock_path = lock_dir / "timer-setup.lock"
        with lock_path.open("w", encoding="utf-8") as stream:
            os.fchmod(stream.fileno(), 0o600)
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            completed = self.run_script("--check")

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "")
        self.assertIn(
            "another timer setup operation is already running",
            completed.stderr,
        )
        self.assertEqual(self.calls(), [])

    def test_state_overlap_rejected_without_chmod_or_write(self) -> None:
        fixture_repo = self.root / "fixture-repo"
        fixture_repo.mkdir()
        (fixture_repo / ".git").mkdir()
        vault = fixture_repo / "second-brain"
        vault.mkdir(mode=0o755)
        vault.chmod(0o755)
        front_door = vault / "README.md"
        front_door.write_text("# Protected fixture vault\n", encoding="utf-8")
        before_mode = stat.S_IMODE(vault.stat().st_mode)
        before_content = front_door.read_bytes()
        env = {
            **self.env,
            "SECOND_BRAIN_REPO_ROOT": str(fixture_repo),
            "XDG_STATE_HOME": str(fixture_repo),
        }

        for action in ("--check", "--disable"):
            with self.subTest(action=action):
                completed = self.run_script(action, env=env)

                self.assertEqual(completed.returncode, 2)
                self.assertEqual(completed.stdout, "")
                self.assertIn("timer setup state path is unsafe", completed.stderr)
                self.assertEqual(stat.S_IMODE(vault.stat().st_mode), before_mode)
                self.assertEqual(front_door.read_bytes(), before_content)
                self.assertFalse((vault / "locks").exists())
                self.assertEqual(self.calls(), [])

    def test_child_failure_is_actionable_without_leaking_child_output(self) -> None:
        env = {**self.env, "TEST_ANALYZE_FAIL": "1"}
        completed = self.run_script("--check", env=env)
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "")
        self.assertIn("systemd unit validation failed", completed.stderr)
        self.assertNotIn("PRIVATE_NOTE_AND_CONFIG_CONTENT", completed.stderr)
        self.assertFalse(any(call.startswith("sudo") for call in self.calls()))

    def test_checkpoint_service_output_omits_payload_and_config_contents(self) -> None:
        repo = self.root / "checkpoint-repo"
        remote = self.root / "checkpoint-remote.git"
        subprocess.run(
            ["git", "init", "--bare", str(remote)],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "init", "-b", "main", str(repo)],
            check=True,
            capture_output=True,
            text=True,
        )

        def git(*arguments: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                ["git", *arguments],
                cwd=repo,
                check=True,
                capture_output=True,
                text=True,
            )

        git("config", "user.name", "Timer Journal Test")
        git("config", "user.email", "timer@example.invalid")
        shutil.copytree(REPO_ROOT / "second-brain", repo / "second-brain")
        (repo / "dot_codex").mkdir()
        config_sentinel = "PRIVATE_CONFIG_SENTINEL_6d29f19a"
        (repo / "dot_codex/config.toml").write_text(
            f'model = "{config_sentinel}"\n',
            encoding="utf-8",
        )
        (repo / "README.md").write_text("# Timer fixture\n", encoding="utf-8")
        gate = repo / "scripts/executable_readme-recruiter-sync"
        gate.parent.mkdir()
        gate.write_text(
            "#!/usr/bin/env bash\nprintf 'pass_no_change\\n'\n",
            encoding="utf-8",
        )
        gate.chmod(0o755)
        git("add", ".")
        git("commit", "-m", "chore: initialize timer fixture")
        git("remote", "add", "origin", str(remote))
        git("push", "-u", "origin", "main")

        payload_sentinel = "PRIVATE_NOTE_SENTINEL_75fb56c1"
        note = repo / "second-brain/00 Context/Decisions.md"
        with note.open("a", encoding="utf-8") as stream:
            stream.write(f"\n- {payload_sentinel}\n")
        live_config = self.home / ".codex/config.toml"
        live_config.parent.mkdir()
        live_config.write_text(
            f'model = "fixture"\nmessage = "{config_sentinel}"\n',
            encoding="utf-8",
        )
        env = {
            **self.env,
            "SECOND_BRAIN_REPO_ROOT": str(repo),
            "SECOND_BRAIN_NOW": "2026-07-14T16:20:00-04:00",
            "TEST_CONFIG_TARGET": str(repo / "dot_codex/config.toml"),
        }

        completed = subprocess.run(
            [str(CHECKPOINT_LAUNCHER), "checkpoint", "--no-push"],
            cwd=self.root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

        visible_output = completed.stdout + completed.stderr
        self.assertEqual(completed.returncode, 0, visible_output)
        self.assertEqual(completed.stderr, "")
        report = json.loads(completed.stdout)
        self.assertEqual(report["result"], "committed")
        self.assertEqual(
            report["paths"],
            [
                "dot_codex/config.toml",
                "second-brain/00 Context/Decisions.md",
            ],
        )
        self.assertNotIn(payload_sentinel, visible_output)
        self.assertNotIn(config_sentinel, visible_output)


if __name__ == "__main__":
    unittest.main()
