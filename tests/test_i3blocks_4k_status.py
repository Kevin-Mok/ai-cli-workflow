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
    scale = 0.7 if markup.startswith('<span size="70%">') else 1
    return round(len(html.unescape(re.sub(r"<[^>]+>", "", markup))) * 10 * scale)


class SongLayout(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), "4K adaptive status filter is missing")
        self.module = runpy.run_path(str(SCRIPT))

    def blocks(self, song="A very long artist - " + "Long song " * 20):
        return [
            {"name": "volume", "full_text": "VOL 33%", "short_text": "VOL 33%", "separator_block_width": 25},
            {"name": "redshift", "full_text": "🌡️ 4500 K", "separator_block_width": 25},
            {"name": "spotify", "full_text": song, "short_text": "<span></span>", "separator_block_width": 25},
            {"name": "calendar", "full_text": "Thu 10/22 13:35", "short_text": "13:35"},
        ]

    def test_long_song_uses_space_up_to_workspace_buttons(self):
        blocks = self.module["layout_blocks"](self.blocks(), 2000, 400, measure)
        self.assertTrue(blocks[2]["full_text"].endswith("…</span>"))
        self.assertEqual(blocks[0]["full_text"], "VOL 33%")
        width = sum(max(measure(b["full_text"]), b.get("min_width", 0)) for b in blocks) + 75
        self.assertLessEqual(width, 2000 - 400 - 8)
        self.assertGreaterEqual(width, 2000 - 400 - 8 - 14)
        self.assertEqual(blocks[3]["full_text"], "Thu 10/22 13:35")

    def test_short_song_uses_smaller_font_without_spacer(self):
        blocks = self.module["layout_blocks"](self.blocks("Short song"), 2000, 400, measure)
        self.assertEqual(blocks[2]["full_text"], '<span size="70%">Short song</span>')
        self.assertLessEqual(blocks[2].get("min_width", 0), measure(blocks[2]["full_text"]))
        self.assertEqual(blocks[1]["full_text"], "🌡️ 4500 K")
        self.assertEqual(blocks[3]["full_text"], "Thu 10/22 13:35")

    def test_smaller_song_fits_more_text_without_changing_other_blocks(self):
        source = self.blocks("Olivia Rodrigo - the cure")
        blocks = self.module["layout_blocks"](source, 2000, 1420, measure)
        self.assertEqual(blocks[2]["full_text"], '<span size="70%">Olivia Rodrigo - the cure</span>')
        for index in (0, 1, 3):
            self.assertEqual(blocks[index]["full_text"], source[index]["full_text"])

    def test_padding_preserves_click_identity_and_text(self):
        source = [{"name": "volume", "instance": "sink", "full_text": "🔉38%"}]
        padded = self.module["pad_blocks"](source, 18)
        self.assertEqual(html.unescape(re.sub(r"<[^>]+>", "", padded[0]["full_text"])), "🔉 38%")
        self.assertEqual(padded[0]["instance"], "sink")
        self.assertEqual(padded[0]["border_right"], 18)
        self.assertEqual(padded[0]["border_left"], 0)
        self.assertNotIn("border_right", source[0])

    def test_icon_padding_reaches_compact_text_and_playback_buttons(self):
        gap = '<span size="1" letter_spacing="20480"> </span>'
        blocks = [{"name": "calendar", "full_text": "📅Thu", "short_text": "🕒18:34"},
                  {"name": "spotify", "full_text": '🎵<span size="x-small">⏸️</span>Song'}]
        padded = self.module["pad_blocks"](blocks)
        self.assertEqual(padded[0]["full_text"], "📅" + gap + "Thu")
        self.assertEqual(padded[0]["short_text"], "🕒" + gap + "18:34")
        self.assertEqual(padded[1]["full_text"], '🎵' + gap + '<span size="x-small">⏸️</span>' + gap + 'Song')

    def test_right_padding_counts_toward_available_width(self):
        blocks = self.blocks()
        for block in blocks:
            block.update(border_left=0, border_right=25)
        result = self.module["layout_blocks"](blocks, 2000, 1580, measure)
        visible = [b for b in result if b.get("full_text")]
        width = sum(max(measure(b["full_text"]) + b["border_left"] + b["border_right"],
                        b.get("min_width", 0)) for b in visible)
        width += sum(b.get("separator_block_width", 9) for b in result[:-1] if b.get("full_text"))
        self.assertLessEqual(width, 2000 - 1580 - 8)

    def test_workspace_minimum_width_reserves_padding_without_clipping_wide_names(self):
        width = self.module["workspace_button_width"]
        self.assertEqual(width("1💻", measure, 135, 144), 202)
        self.assertEqual(width("11💻", lambda text: 240, 135, 144), 253)
        self.assertEqual(width("1💻", measure, 96, 0), 29)

    def test_workspace_markup_and_hidden_number_match_rendered_width(self):
        seen = []
        def measure_markup(text):
            seen.append(text)
            return 100
        name = "6:<span size='1' letter_spacing='18432'> </span>6💬"
        width = self.module["workspace_button_width"](name, measure_markup, 135, 0, True)
        self.assertEqual(width, 113)
        self.assertEqual(seen, [name.split(":", 1)[1]])

    def test_workspace_pressure_shortens_song_before_volume(self):
        blocks = self.module["layout_blocks"](self.blocks(), 2000, 1550, measure)
        self.assertTrue(blocks[2]["full_text"].endswith("…</span>"))
        self.assertLess(measure(blocks[2]["full_text"]), 200)
        self.assertEqual(blocks[0]["full_text"], "VOL 33%")

    def test_extreme_pressure_drops_calendar_and_song_first(self):
        blocks = self.module["layout_blocks"](self.blocks(), 2000, 1920, measure)
        self.assertEqual(blocks[0]["full_text"], "VOL 33%")
        self.assertEqual(blocks[1]["full_text"], "🌡️ 4500 K")
        self.assertEqual(blocks[2]["full_text"], "")
        self.assertEqual(blocks[3]["full_text"], "")

    def test_calendar_fallbacks_reserve_redshift_and_all_separators(self):
        for workspace, calendar in ((1580, "Thu 10/22 13:35"), (1670, "13:35"), (1780, "")):
            with self.subTest(workspace=workspace):
                blocks = self.module["layout_blocks"](self.blocks(), 2000, workspace, measure)
                visible = [b for b in blocks if b.get("full_text")]
                width = sum(max(measure(b["full_text"]), b.get("min_width", 0)) for b in visible)
                width += sum(b.get("separator_block_width", 9) for b in visible[:-1])
                self.assertLessEqual(width, 2000 - workspace - 8)
                self.assertEqual(blocks[0]["full_text"], "VOL 33%")
                self.assertEqual(blocks[1]["full_text"], "🌡️ 4500 K")
                self.assertEqual(blocks[3]["full_text"], calendar)

    def test_unicode_markup_is_valid_and_state_prefix_is_preserved(self):
        prefix = ' <span size="x-small" rise="8192">▶</span> '
        fitted = self.module["fit_song"](prefix + "A&amp;B - 東京" * 30, 250, measure)
        self.assertTrue(fitted.startswith(prefix))
        self.assertTrue(fitted.endswith("…"))
        self.assertLessEqual(measure(fitted), 250)
        self.assertNotIn("&am…", fitted)

    def test_calendar_compacts_before_music_emoji_is_lost(self):
        prefix = '🎵<span size="x-small" rise="8192">▶️</span>'
        for workspace, calendar in ((1560, "Thu 10/22 13:35"), (1670, "13:35"), (1720, "")):
            with self.subTest(workspace=workspace):
                blocks = self.module["layout_blocks"](self.blocks(prefix + "Artist - " + "Song " * 20),
                                                       2000, workspace, measure)
                self.assertTrue(blocks[2]["full_text"].startswith('<span size="70%">' + prefix), blocks[2])
                self.assertEqual(blocks[3]["full_text"], calendar)

    def test_headers_click_identity_and_empty_song_are_preserved(self):
        transform = self.module["transform_line"]
        self.assertEqual(transform('{"version":1,"click_events":true}\n', lambda b: b),
                         '{"version":1,"click_events":true}\n')
        self.assertEqual(transform('[[]\n', lambda b: b), '[[]\n')
        blocks = self.blocks("")
        blocks[2]["instance"] = "click-target"
        result = self.module["layout_blocks"](blocks, 2000, 400, measure)
        self.assertEqual(result[2]["full_text"], "")
        self.assertEqual(result[2].get("min_width", 0), 0)
        self.assertEqual(result[2]["instance"], "click-target")

    def test_compact_song_keeps_artist_then_title(self):
        fitted = self.module["fit_song"]("Very long artist name - Stitches", 160, measure)
        self.assertEqual(fitted, "Very long artis…")
        self.assertTrue(fitted.endswith("…"))

    def test_no_song_still_reserves_volume_under_pressure(self):
        result = self.module["layout_blocks"](self.blocks(""), 2000, 1920, measure)
        self.assertEqual(result[0]["full_text"], "VOL 33%")
        self.assertEqual(result[3]["full_text"], "")

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

    def test_rapid_redshift_clicks_survive_busy_scheduler(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scripts = root / ".config/i3blocks/scripts"
            scripts.mkdir(parents=True)
            # A slow block reproduces scheduler drops; each event must run once.
            block = scripts / "redshift"
            block.write_text("#!/bin/sh\nif [ \"$BLOCK_BUTTON\" = 4 ]; then sleep .08; echo x >> \"$TEST_EVENTS\"; echo '🌡️ ERR'; else echo '🌡️ 3000 K'; fi\n")
            block.chmod(0o755)
            xrdb = root / "xrdb"
            xrdb.write_text("#!/bin/sh\nexit 1\n")
            xrdb.chmod(0o755)
            (root / ".config/i3blocks/i3blocks-4k.conf").write_text(
                "[redshift]\ncommand=~/.config/i3blocks/scripts/redshift\ninterval=1\nsignal=2\n")
            clicks = "[\n" + "\n".join(
                ("," if i else "") + json.dumps({"name": "redshift", "button": 4})
                for i in range(8)) + "\n"
            process = subprocess.Popen(["/usr/bin/python3", str(SCRIPT)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                env={**os.environ, "HOME": directory, "PATH": directory + ":/usr/bin:/bin",
                     "TEST_EVENTS": str(root / "events")}, text=True)
            try:
                process.stdin.write(clicks)
                process.stdin.flush()
                import time
                time.sleep(1.8)
                process.terminate()
                output, errors = process.communicate(timeout=4)
            finally:
                if process.poll() is None:
                    process.kill()
                    process.communicate()
            events = (root / "events").read_text().splitlines() if (root / "events").exists() else []
            self.assertEqual(len(events), 8, errors)
            self.assertIn(json.dumps('🌡️<span size="1" letter_spacing="20480"> </span> ERR',
                                     ensure_ascii=False), output)

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
                "i3blocks": 'printf \'%s\\n\' \'{"version":1,"click_events":true}\' \'[[]\' \',[{"name":"volume","full_text":"33%"},{"name":"redshift","full_text":"🌡️ 4500 K"},{"name":"spotify","full_text":"Song"},{"name":"calendar","full_text":"13:35"}]\'\n',
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
            status = json.loads(result.stdout.splitlines()[-1].lstrip(","))
            song = next(block for block in status if block.get("name") == "spotify")
            self.assertIn('<span size="70%">', song["full_text"])


if __name__ == "__main__":
    unittest.main()
