#!/usr/bin/env python3
"""Verify that the launcher uses a separate, stable Chrome data directory."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/executable_flavibot-browser"


class LauncherTest(unittest.TestCase):
    def test_launches_music_page_with_separate_persistent_data_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            chrome = base / "google-chrome"
            chrome.write_text("#!/usr/bin/env python3\nimport json, sys\nprint(json.dumps(sys.argv[1:]))\n")
            chrome.chmod(0o755)
            env = {**os.environ, "HOME": str(base / "home"),
                   "PATH": str(base) + os.pathsep + os.environ["PATH"]}
            for _ in range(2):
                result = subprocess.run(["bash", str(SCRIPT)], env=env,
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), [
                    "--user-data-dir=" + str(base / "home/.local/share/flavibot-chrome"),
                    "--no-first-run", "--no-default-browser-check", "--new-window",
                    "https://flavibot.xyz/music-player",
                ])


if __name__ == "__main__":
    unittest.main()
