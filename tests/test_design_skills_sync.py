#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTERNALS = REPO_ROOT / ".chezmoiexternal.toml.tmpl"
HELPER = REPO_ROOT / "scripts" / "executable_sync-design-skills"
SERVICE = REPO_ROOT / "dot_config" / "systemd" / "user" / "design-skills-sync.service"
TIMER = REPO_ROOT / "dot_config" / "systemd" / "user" / "design-skills-sync.timer"
SETUP = REPO_ROOT / "scripts" / "executable_setup-design-skills-timer"
IMPECCABLE = REPO_ROOT / "dot_agents" / "skills" / "impeccable"
OMITTED = {
    "reference/ios.md", "reference/android.md",
    "reference/adapt.native.md", "reference/audit.native.md",
    "agents/impeccable_asset_producer.toml", "agents/impeccable_documenter.toml",
    "agents/impeccable_finish_reviewer.toml", "agents/impeccable_manual_edit_applier.toml",
}


class DesignSkillSourcesTest(unittest.TestCase):
    def test_only_higgsfield_remains_an_external_design_source(self) -> None:
        externals = EXTERNALS.read_text(encoding="utf-8")
        self.assertNotIn("impeccable", externals)
        self.assertFalse((REPO_ROOT / "dot_codex/skills/symlink_impeccable.tmpl").exists())

        plugin = '[".codex/plugins/higgsfield"]'
        self.assertIn(plugin, externals)
        plugin_block = externals[externals.index(plugin) :]
        self.assertIn('type = "git-repo"', plugin_block)
        self.assertIn('url = "https://github.com/higgsfield-ai/skills.git"', plugin_block)
        self.assertIn('refreshPeriod = "24h"', plugin_block)
        self.assertIn('args = ["--ff-only"]', plugin_block)

    def test_pinned_shared_impeccable_keeps_explicit_invocation_and_runtime_boundary(self) -> None:
        skill = (IMPECCABLE / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("version: 4.5.2", skill)
        self.assertIn("disable-model-invocation: true", skill)
        description = re.search(r'^description: "(.+)"$', skill, re.MULTILINE)
        self.assertIsNotNone(description)
        self.assertLessEqual(len(description.group(1).encode()), 140)
        for required in ("$impeccable", "/impeccable", "IMPECCABLE_NO_TELEMETRY=1", "Launcher unavailable"):
            self.assertIn(required, skill)
        self.assertIn("allow_implicit_invocation: false", (IMPECCABLE / "agents/openai.yaml").read_text())
        self.assertEqual((IMPECCABLE / "scripts/VERSION").read_text().strip(), "0.1.14")
        source = (IMPECCABLE / "SOURCE.md").read_text()
        self.assertIn("9d9fcf5cf7a47728959e0c92ae0ab274571b16e3", source)
        self.assertIn("omitted", source.lower())
        for required in ("LICENSE", "NOTICE.md", "licenses/modern-screenshot.txt", "licenses/platform-design-skills.txt"):
            self.assertTrue((IMPECCABLE / required).is_file(), required)
        for omitted in OMITTED:
            self.assertFalse((IMPECCABLE / omitted).exists(), omitted)
        for role in ("asset-producer", "documenter", "finish-reviewer", "manual-edit-applier"):
            self.assertTrue((IMPECCABLE / f"reference/degraded/{role}.md").is_file(), role)

    def test_impeccable_remaining_links_and_web_runtime_assets_are_intact(self) -> None:
        manifest = json.loads((IMPECCABLE / "UPSTREAM_SHA256.json").read_text())
        modified = {
            "SKILL.md", "agents/openai.yaml", "reference/adapt.md", "reference/animate.md",
            "reference/audit.md", "reference/doctor.md", "reference/init.md", "reference/layout.md",
            "reference/new-work.md", "reference/typeset.md",
        }
        for name, expected in manifest.items():
            if name in OMITTED | modified:
                continue
            installed_name = "scripts/executable_impeccable" if name == "scripts/impeccable" else name
            path = IMPECCABLE / installed_name
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected, name)
        missing = []
        for path in IMPECCABLE.rglob("*.md"):
            for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                target = link.split("#", 1)[0]
                if target and not re.match(r"\w+:|^/", target):
                    if not (path.parent / target).exists():
                        missing.append(f"{path.relative_to(IMPECCABLE)}: {target}")
        self.assertEqual(missing, [])

    def test_culled_externals_and_exposure_templates_are_not_managed(self) -> None:
        externals = EXTERNALS.read_text(encoding="utf-8")
        for source in ("21st", "review-animations", "scroll-world"):
            self.assertNotIn(f'".codex/skills/upstreams/{source}"', externals)
        for slug in (
            "21st-ai", "21st-cli-use", "21st-design-sync", "21st-registry",
            "review-animations", "scroll-world",
        ):
            self.assertFalse((REPO_ROOT / "dot_codex" / "skills" / f"symlink_{slug}.tmpl").exists())


class DesignSkillRefreshHelperTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.home = self.root / "home"
        self.source = self.home / "linux-config"
        self.home.mkdir()
        self.source.mkdir()
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.log = self.root / "calls.log"
        self.log.touch()
        self._write_fake("chezmoi")
        self._write_fake("npx")
        self.env = {
            **os.environ,
            "HOME": str(self.home),
            "LINUX_CONFIG_SOURCE": str(self.source),
            "PATH": str(self.bin) + os.pathsep + os.environ["PATH"],
            "TEST_CALL_LOG": str(self.log),
        }

    def _write_fake(self, name: str) -> None:
        path = self.bin / name
        path.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "{ printf '%s' \"$0\"; printf ' %s' \"$@\"; printf '\\n'; } >> \"$TEST_CALL_LOG\"\n",
            encoding="utf-8",
        )
        path.chmod(0o755)

    def run_helper(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(HELPER), *arguments],
            cwd=self.root,
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )

    def calls(self) -> list[str]:
        return self.log.read_text(encoding="utf-8").splitlines()

    def test_dry_run_refreshes_only_retained_sources(self) -> None:
        completed = self.run_helper("--dry-run")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Design skill refresh preview complete.", completed.stdout)
        self.assertEqual(len(self.calls()), 1)
        self.assertIn("chezmoi -S", self.calls()[0])
        self.assertIn("apply --refresh-externals -v -n", self.calls()[0])
        self.assertTrue(self.calls()[0].endswith(
            f"{self.home}/.codex/plugins/higgsfield"
        ))
        self.assertNotIn("impeccable", self.calls()[0])
        self.assertNotIn("npx", self.calls()[0])

    def test_legacy_bootstrap_is_a_noop_without_network(self) -> None:
        completed = self.run_helper("--bootstrap")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("no separate bootstrap is needed", completed.stdout)
        self.assertNotIn("UI/UX Pro Max", completed.stdout)
        self.assertEqual(self.calls(), [])

    def test_normal_refresh_leaves_unmanaged_installed_copies_untouched(self) -> None:
        skill = self.home / ".agents" / "skills" / "ui-ux-pro-max"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("explicit-only marker")
        upstream = self.home / ".codex/skills/upstreams/impeccable"
        upstream.mkdir(parents=True)
        (upstream / "marker").write_text("legacy upstream")

        completed = self.run_helper()

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Design skills refreshed.", completed.stdout)
        self.assertEqual(len(self.calls()), 1)
        self.assertIn("chezmoi -S", self.calls()[0])
        self.assertIn("apply --refresh-externals -v", self.calls()[0])
        self.assertNotIn("npx", "\n".join(self.calls()))
        self.assertNotIn("impeccable", "\n".join(self.calls()))
        self.assertEqual((skill / "SKILL.md").read_text(), "explicit-only marker")
        self.assertEqual((upstream / "marker").read_text(), "legacy upstream")

    def test_pinned_launcher_uses_explicit_engine_without_download(self) -> None:
        engine = self.bin / "test-engine"
        engine.write_text(
            "#!/usr/bin/env bash\n"
            "printf '%s\\n' \"$IMPECCABLE_SKILL_DIR\" \"$IMPECCABLE_NO_TELEMETRY\" \"$@\"\n"
        )
        engine.chmod(0o755)
        completed = subprocess.run(
            ["sh", str(IMPECCABLE / "scripts/executable_impeccable"), "context", "--target", "src/app"],
            env={**self.env, "IMPECCABLE_BIN": str(engine), "IMPECCABLE_NO_TELEMETRY": "1"},
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.splitlines(), [str(IMPECCABLE), "1", "context", "--target", "src/app"])
        self.assertEqual(self.calls(), [])


class DesignSkillsTimerTest(unittest.TestCase):
    def test_daily_service_and_timer_are_valid(self) -> None:
        service = SERVICE.read_text(encoding="utf-8")
        timer = TIMER.read_text(encoding="utf-8")

        self.assertIn("ExecStart=%h/scripts/sync-design-skills", service)
        self.assertIn("Environment=LINUX_CONFIG_SOURCE=%h/linux-config", service)
        self.assertIn("UMask=0077", service)
        self.assertIn("OnCalendar=*-*-* 05:00:00", timer)
        self.assertIn("Persistent=true", timer)
        self.assertIn("Unit=design-skills-sync.service", timer)

        completed = subprocess.run(
            ["systemd-analyze", "verify", str(SERVICE), str(TIMER)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)


class DesignSkillsTimerSetupTest(unittest.TestCase):
    def test_setup_command_exposes_check_enable_and_disable(self) -> None:
        completed = subprocess.run(
            [str(SETUP), "--help"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("usage: setup-design-skills-timer", completed.stdout)
        self.assertIn("--check", completed.stdout)
        self.assertIn("--enable", completed.stdout)
        self.assertIn("--disable", completed.stdout)


if __name__ == "__main__":
    unittest.main()
