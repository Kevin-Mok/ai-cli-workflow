#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
UNIT_DIR = REPO_ROOT / "dot_config" / "systemd" / "user"
SERVICE = UNIT_DIR / "superpowers-release-sync.service"
TIMER = UNIT_DIR / "superpowers-release-sync.timer"


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


if __name__ == "__main__":
    unittest.main()
