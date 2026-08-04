#!/usr/bin/env python3

import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "executable_setup-second-brain-state"


class SecondBrainStateSetupTest(unittest.TestCase):
    def test_default_state_root_uses_standard_xdg_location(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary) / "home"
            home.mkdir()
            completed = subprocess.run(
                ["bash", str(SCRIPT)],
                env={**os.environ, "HOME": str(home)},
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            root = home / ".local" / "state" / "second-brain"
            for path in (root, root / "raw", root / "migrations", root / "locks"):
                self.assertTrue(path.is_dir(), path)
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o700)
            self.assertFalse((home / "second-brain").exists())
            self.assertIn(f"{home}/.local/state", completed.stdout)


if __name__ == "__main__":
    unittest.main()
