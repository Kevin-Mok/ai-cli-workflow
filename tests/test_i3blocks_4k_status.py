#!/usr/bin/env python3
"""Check adaptive song fitting without changing the user's workspaces."""
import html
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "dot_config/i3blocks/scripts/executable_4k_status"


def measure(markup):
    return len(html.unescape(re.sub(r"<[^>]+>", "", markup))) * 10


class SongLayout(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), "4K adaptive status filter is missing")
        self.module = runpy.run_path(str(SCRIPT))

    def blocks(self, song="A very long artist - " + "Long song " * 20):
        return [
            {"name": "volume", "full_text": "VOL 33%", "short_text": "VOL 33%", "separator_block_width": 25},
            {"name": "spotify", "full_text": song, "short_text": "<span></span>", "separator_block_width": 25},
            {"name": "calendar", "full_text": "Thu 10/22 13:35", "short_text": "13:35"},
        ]

    def test_long_song_ellipsizes_and_volume_is_centered(self):
        blocks = self.module["layout_blocks"](self.blocks(), 2000, 400, measure)
        self.assertTrue(blocks[1]["full_text"].endswith("…"))
        self.assertEqual(blocks[0]["full_text"], "VOL 33%")
        width = sum(max(measure(b["full_text"]), b.get("min_width", 0)) for b in blocks) + 50
        self.assertLessEqual(abs((2000 - width + 35) - 1000), 2)

    def test_short_song_keeps_volume_at_center(self):
        blocks = self.module["layout_blocks"](self.blocks("Short song"), 2000, 400, measure)
        self.assertEqual(blocks[1]["full_text"], "Short song")
        self.assertGreater(blocks[1]["min_width"], measure("Short song"))

    def test_workspace_pressure_shortens_song_before_volume(self):
        blocks = self.module["layout_blocks"](self.blocks(), 2000, 1650, measure)
        self.assertTrue(blocks[1]["full_text"].endswith("…"))
        self.assertLess(measure(blocks[1]["full_text"]), 200)
        self.assertEqual(blocks[0]["full_text"], "VOL 33%")

    def test_extreme_pressure_drops_calendar_and_song_first(self):
        blocks = self.module["layout_blocks"](self.blocks(), 2000, 1920, measure)
        self.assertEqual(blocks[0]["full_text"], "VOL 33%")
        self.assertEqual(blocks[1]["full_text"], "")
        self.assertEqual(blocks[2]["full_text"], "")

    def test_unicode_markup_is_valid_and_state_prefix_is_preserved(self):
        prefix = ' <span size="x-small" rise="8192">▶</span> '
        fitted = self.module["fit_song"](prefix + "A&amp;B - 東京" * 30, 250, measure)
        self.assertTrue(fitted.startswith(prefix))
        self.assertTrue(fitted.endswith("…"))
        self.assertLessEqual(measure(fitted), 250)
        self.assertNotIn("&am…", fitted)

    def test_headers_click_identity_and_empty_song_are_preserved(self):
        transform = self.module["transform_line"]
        self.assertEqual(transform('{"version":1,"click_events":true}\n', lambda b: b),
                         '{"version":1,"click_events":true}\n')
        self.assertEqual(transform('[[]\n', lambda b: b), '[[]\n')
        blocks = self.blocks("")
        blocks[1]["instance"] = "click-target"
        result = self.module["layout_blocks"](blocks, 2000, 400, measure)
        self.assertEqual(result[1]["full_text"], "<span></span>")
        self.assertGreater(result[1]["min_width"], 0)
        self.assertEqual(result[1]["instance"], "click-target")

    def test_compact_song_prioritizes_title_over_long_artist(self):
        fitted = self.module["fit_song"]("Very long artist name - Stitches", 160, measure)
        self.assertTrue(fitted.startswith("Stitches"))
        self.assertTrue(fitted.endswith("…"))

    def test_no_song_still_reserves_volume_under_pressure(self):
        result = self.module["layout_blocks"](self.blocks(""), 2000, 1920, measure)
        self.assertEqual(result[0]["full_text"], "VOL 33%")
        self.assertEqual(result[2]["full_text"], "")

    def test_startup_failure_preserves_stream_and_forwards_clicks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, body in {
                "xrdb": "exit 1\n",
                "i3blocks": 'cat > "$TEST_CLICK_DATA"\nprintf \'%s\\n\' \'{"version":1,"click_events":true}\' \'[[]\' \',[{"name":"volume","full_text":"33%"}]\'\n',
            }.items():
                command = root / name
                command.write_text("#!/bin/sh\n" + body)
                command.chmod(0o755)
            clicks = '[{"name":"volume","button":1}]\n'
            result = subprocess.run(
                ["/usr/bin/python3", str(SCRIPT)], input=clicks,
                env={**os.environ, "PATH": directory + ":/usr/bin:/bin",
                     "TEST_CLICK_DATA": str(root / "clicks")},
                capture_output=True, text=True, timeout=5,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            status = json.loads(result.stdout.splitlines()[-1].lstrip(","))
            self.assertEqual(status[0]["full_text"], "33%")
            self.assertEqual((root / "clicks").read_text(), clicks)
            self.assertIn("layout unavailable", result.stderr)

    def test_transient_startup_failure_recovers_layout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            commands = {
                "xrdb": 'if [ ! -e "$TEST_READY" ]; then touch "$TEST_READY"; exit 1; fi\nprintf "Xft.dpi: 96\\n"\n',
                "i3-msg": '''case "$2:$3" in
get_bar_config:) echo '["bar-2"]';;
get_bar_config:bar-2) echo '{"outputs":["DP-2"],"font":"pango:monospace 10"}';;
get_outputs:) echo '[{"name":"DP-2","rect":{"width":2000}}]';;
get_workspaces:) echo '[]';;
esac
''',
                "i3blocks": 'printf \'%s\\n\' \'{"version":1,"click_events":true}\' \'[[]\' \',[{"name":"volume","full_text":"33%"},{"name":"spotify","full_text":"Song"},{"name":"calendar","full_text":"13:35"}]\'\n',
            }
            for name, body in commands.items():
                command = root / name
                command.write_text("#!/bin/sh\n" + body)
                command.chmod(0o755)
            result = subprocess.run(
                ["/usr/bin/python3", str(SCRIPT)], input="",
                env={**os.environ, "PATH": directory + ":/usr/bin:/bin",
                     "TEST_READY": str(root / "ready")},
                capture_output=True, text=True, timeout=5,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('"min_width"', result.stdout)


if __name__ == "__main__":
    unittest.main()
