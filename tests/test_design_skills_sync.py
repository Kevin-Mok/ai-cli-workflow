#!/usr/bin/env python3

from __future__ import annotations

import os
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

UPSTREAMS = {
    "impeccable": "https://github.com/pbakaus/impeccable.git",
    "21st": "https://github.com/21st-dev/skill.git",
    "review-animations": "https://github.com/emilkowalski/skills.git",
    "scroll-world": "https://github.com/oso95/scroll-world.git",
}
SYMLINKS = {
    "impeccable": "upstreams/impeccable/.github/skills/impeccable",
    "21st-cli-use": "upstreams/21st/skills/21st-cli-use",
    "21st-ai": "upstreams/21st/skills/21st-ai",
    "21st-design-sync": "upstreams/21st/skills/21st-design-sync",
    "21st-registry": "upstreams/21st/skills/21st-registry",
    "review-animations": "upstreams/review-animations/skills/review-animations",
    "scroll-world": "upstreams/scroll-world/skills/scroll-world",
}


class DesignSkillSourcesTest(unittest.TestCase):
    def test_externals_refresh_daily_and_symlinks_expose_each_skill(self) -> None:
        externals = EXTERNALS.read_text(encoding="utf-8")

        for slug, url in UPSTREAMS.items():
            target = f'[".codex/skills/upstreams/{slug}"]'
            self.assertIn(target, externals)
            start = externals.index(target)
            block = externals[start : externals.find("\n[", start + len(target))]
            self.assertIn('type = "git-repo"', block)
            self.assertIn(f'url = "{url}"', block)
            self.assertIn('refreshPeriod = "24h"', block)
            self.assertIn('args = ["--ff-only"]', block)

        plugin = '[".codex/plugins/higgsfield"]'
        self.assertIn(plugin, externals)
        plugin_block = externals[externals.index(plugin) :]
        self.assertIn('type = "git-repo"', plugin_block)
        self.assertIn('url = "https://github.com/higgsfield-ai/skills.git"', plugin_block)
        self.assertIn('refreshPeriod = "24h"', plugin_block)

        for slug, target in SYMLINKS.items():
            link = REPO_ROOT / "dot_codex" / "skills" / f"symlink_{slug}.tmpl"
            self.assertEqual(link.read_text(encoding="utf-8").strip(), target)


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

    def test_dry_run_refreshes_externals_without_updating_uiux_pro_max(self) -> None:
        completed = self.run_helper("--dry-run")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Design skill refresh preview complete.", completed.stdout)
        self.assertEqual(len(self.calls()), 1)
        self.assertIn("chezmoi -S", self.calls()[0])
        self.assertIn("apply --refresh-externals -v -n", self.calls()[0])
        self.assertNotIn("npx", self.calls()[0])

    def test_bootstrap_installs_uiux_bundle_when_missing(self) -> None:
        completed = self.run_helper("--bootstrap")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Design skills bootstrap complete.", completed.stdout)
        self.assertEqual(len(self.calls()), 1)
        self.assertIn("npx --yes ui-ux-pro-max-cli init --ai codex --global", self.calls()[0])

    def test_normal_refresh_updates_existing_uiux_bundle_after_externals(self) -> None:
        (self.home / ".agents" / "skills" / "ui-ux-pro-max").mkdir(parents=True)

        completed = self.run_helper()

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Design skills refreshed.", completed.stdout)
        self.assertEqual(len(self.calls()), 2)
        self.assertIn("chezmoi -S", self.calls()[0])
        self.assertIn("apply --refresh-externals -v", self.calls()[0])
        self.assertIn("npx --yes ui-ux-pro-max-cli update --ai codex --global", self.calls()[1])


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
