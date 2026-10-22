#!/usr/bin/env python3
"""Exercise the 4K config through the installed i3blocks scheduler."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class FourKOverflow(unittest.TestCase):
    def test_volume_precedes_song_and_song_can_disappear(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            scripts = home / ".config/i3blocks/scripts"
            scripts.mkdir(parents=True)
            for name, output in {
                "volume": "VOL 75%\nVOL 75%\n#ffffff\n",
                "now_playing_mpris": "Artist - Long song\nArtist - Long song\n#abcdef\n",
                "calendar": "12:34\n12:34\n#ffffff\n",
            }.items():
                script = scripts / name
                script.write_text("#!/bin/sh\ncat <<'EOF'\n" + output + "EOF\n")
                script.chmod(0o755)
            process = subprocess.Popen(
                ["i3blocks", "-c", str(ROOT / "dot_config/i3blocks/i3blocks-4k.conf.tmpl")],
                env={**os.environ, "HOME": directory}, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            try:
                output, errors = process.communicate(timeout=1)
            except subprocess.TimeoutExpired:
                process.terminate()
                output, errors = process.communicate(timeout=3)
            self.assertEqual(errors, "")
            updates = [json.loads(line.lstrip(",")) for line in output.splitlines()
                       if line.lstrip(",").startswith("[{")]
            blocks = [block for block in updates[-1] if block.get("name")]
            self.assertEqual([block["name"] for block in blocks],
                             ["volume", "spotify", "calendar"])
            self.assertEqual(blocks[0]["full_text"], "VOL 75%")
            self.assertEqual(blocks[0]["short_text"], "VOL 75%")
            self.assertIn("Artist - Long song", blocks[1]["full_text"])
            self.assertEqual(blocks[1]["short_text"], "<span></span>")
            self.assertEqual(blocks[1]["color"], "#abcdef")


if __name__ == "__main__":
    unittest.main()
