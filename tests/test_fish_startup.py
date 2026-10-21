"""Exercise the real Fish login guard without starting a graphical server."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]


class FishStartupTests(unittest.TestCase):
    def test_startx_only_on_console_one_without_display(self):
        source = (REPO / "dot_config/fish/config.fish.tmpl").read_text()
        block = source.split("# login to X [[[ #", 1)[1].split(
            "# ]]] login to X #", 1
        )[0]
        block = "\n".join(
            line for line in block.splitlines()
            if not line.lstrip().startswith("{{")
            and not line.startswith("set -x GPG_TTY")
        )
        with tempfile.TemporaryDirectory() as directory:
            startx = Path(directory) / "startx"
            startx.write_text('#!/bin/sh\nprintf "startx:%s\\n" "$*"\n')
            startx.chmod(0o700)
            for login, display, vtnr, expected in (
                (True, ":1", None, "skipped\n"),
                (True, None, None, "skipped\n"),
                (True, None, "", "skipped\n"),
                (True, "", "1", "startx:-- -keeptty\n"),
                (True, None, "1", "startx:-- -keeptty\n"),
                (True, None, "2", "skipped\n"),
                (True, ":0", "1", "skipped\n"),
                (False, None, "1", "skipped\n"),
            ):
                with self.subTest(login=login, display=display, vtnr=vtnr):
                    env = os.environ.copy()
                    env.pop("DISPLAY", None)
                    env.pop("XDG_VTNR", None)
                    env["PATH"] = directory + os.pathsep + env["PATH"]
                    if display is not None:
                        env["DISPLAY"] = display
                    if vtnr is not None:
                        env["XDG_VTNR"] = vtnr
                    args = ["fish", "--no-config"]
                    if login:
                        args.append("--login")
                    result = subprocess.run(
                        args + ["-c", block + "\necho skipped"], env=env,
                        text=True, capture_output=True, timeout=10,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stderr, "")
                    self.assertEqual(result.stdout, expected)


if __name__ == "__main__":
    unittest.main()
