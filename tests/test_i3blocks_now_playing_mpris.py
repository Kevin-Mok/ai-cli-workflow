#!/usr/bin/env python3
"""Exercise the real block executable with a strict, structured D-Bus boundary."""

import json
import os
import runpy
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "dot_config/i3blocks/scripts/executable_now_playing_mpris"
CHROME = "org.mpris.MediaPlayer2.chromium.instance4159"
SPOTIFY = "org.mpris.MediaPlayer2.spotify"


def variant(kind, data):
    return {"type": kind, "data": data}


def player(title, artist, status="Playing", **capabilities):
    props = {
        "PlaybackStatus": variant("s", status),
        "Metadata": variant("a{sv}", {
            "xesam:title": variant("s", title),
            "xesam:artist": variant("as", [artist] if artist else []),
            "mpris:trackid": variant("o", "/track/1"),
        }),
    }
    props.update({key: variant("b", capabilities.get(key, True)) for key in
                  ("CanControl", "CanPause", "CanPlay", "CanGoPrevious", "CanGoNext")})
    return props


FAKE_BUSCTL = r'''#!/usr/bin/env python3
import json, os, sys, time
from pathlib import Path
args = sys.argv[1:]
with open(os.environ["TEST_CALLS"], "a") as log:
    log.write(json.dumps(args) + "\n")
assert args[:3] == ["--user", "--json=short", "--timeout=1"], args
args = args[3:]
data = json.loads(Path(os.environ["TEST_BUS"]).read_text())
if data.get("timeout"):
    time.sleep(3)
if data.get("invalid_json"):
    print("invalid JSON")
    sys.exit(0)
if args == ["list", "--no-pager"]:
    print(json.dumps([{"name": name, "connection": owner}
                      for name, owner in data["names"].items()]))
else:
    assert args[0] == "call", args
    assert args[2] == "/org/mpris/MediaPlayer2", args
    owner = args[1]
    if owner not in data["players"] or data["players"][owner] is None:
        sys.exit(1)
    if data["players"][owner] == "timeout":
        time.sleep(3)
    if args[3:] == ["org.freedesktop.DBus.Properties", "GetAll", "s",
                   "org.mpris.MediaPlayer2.Player"]:
        print(json.dumps({"type": "a{sv}", "data": [data["players"][owner]]}))
    else:
        assert args[3] == "org.mpris.MediaPlayer2.Player", args
        assert args[4:] in (["PlayPause"], ["Previous"], ["Next"]), args
'''


class NowPlayingTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), "browser-aware now-playing helper is missing")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        fake = self.path / "busctl"
        fake.write_text(FAKE_BUSCTL)
        fake.chmod(0o755)
        self.fixture = self.path / "bus.json"
        self.calls = self.path / "calls.jsonl"
        self.colors = self.path / "colors.sh"
        self.colors.write_text("color7='#112233'\nexit 99\n")
        self.cache = self.path / "cache/i3blocks/now-playing.json"
        self.env = {**os.environ, "PATH": f"{self.path}:{os.environ['PATH']}",
                    "TEST_BUS": str(self.fixture), "TEST_CALLS": str(self.calls),
                    "XDG_CACHE_HOME": str(self.path / "cache"),
                    "NOW_PLAYING_COLORS_FILE": str(self.colors)}
        self.env.pop("BLOCK_BUTTON", None)
        self.data = {"names": {CHROME: ":1.50", SPOTIFY: ":1.649"}, "players": {
            ":1.50": player("Soul Food", "Logic"),
            ":1.649": player("Janice STFU", "Drake"),
        }}

    def run_block(self, button=None):
        self.fixture.write_text(json.dumps(self.data))
        env = dict(self.env)
        if button:
            env["BLOCK_BUTTON"] = button
        result = subprocess.run([sys.executable, str(SCRIPT)], env=env,
                                capture_output=True, text=True, timeout=8)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(len(result.stdout.splitlines()), 3, result.stdout)
        return result.stdout.splitlines()

    def actions(self):
        return [args[4:] for args in map(json.loads, self.calls.read_text().splitlines())
                if len(args) > 6 and args[6] == "org.mpris.MediaPlayer2.Player"]

    def test_playing_chrome_wins_over_spotify(self):
        self.assertEqual(self.run_block(), ["Logic - Soul Food", "Soul Food", "#112233"])

    def test_browser_accepts_separate_artist_metadata_without_title_separator(self):
        self.data["players"][":1.50"] = player("I'm Gone", "Logic")
        self.assertEqual(self.run_block()[0], "Logic - I'm Gone")

    def test_browser_accepts_lenient_artist_title_separators(self):
        for title in ("Logic - I'm Gone", "Logic–I'm Gone", "Logic — I'm Gone",
                      "Logic-I'm Gone", "宇多田ヒカル - 光"):
            with self.subTest(title=title):
                self.data["players"][":1.50"] = player(title, "")
                self.assertEqual(self.run_block()[0], title)

    def test_unstructured_browser_title_falls_back_to_spotify(self):
        self.data["players"][":1.50"] = player("Live Set In KC / Endless Summer Tour #logic", "")
        self.assertEqual(self.run_block()[0], "Drake - Janice STFU")

    def test_unstructured_browser_title_hides_and_clears_click_state(self):
        self.data["names"] = {CHROME: ":1.50"}
        self.run_block()
        for title in ("A long video title with no artist", "- Missing artist", "Missing title -"):
            with self.subTest(title=title):
                self.data["players"][":1.50"] = player(title, "")
                self.assertEqual(self.run_block(), ["", "", "#112233"])
                self.assertFalse(self.cache.exists())
        self.run_block("1")
        self.assertEqual(self.actions(), [])

    def test_filtered_browser_does_not_mask_matching_browser(self):
        self.data["players"][":1.50"] = player("Unstructured video", "")
        self.data["names"][CHROME + "2"] = ":1.51"
        self.data["players"][":1.51"] = player("Logic - I'm Gone", "")
        self.assertEqual(self.run_block()[0], "Logic - I'm Gone")

    def test_playing_spotify_wins_over_paused_chrome(self):
        self.data["players"][":1.50"]["PlaybackStatus"] = variant("s", "Paused")
        self.assertEqual(self.run_block()[0], "Drake - Janice STFU")

    def test_both_paused_prefers_chrome(self):
        for props in self.data["players"].values():
            props["PlaybackStatus"] = variant("s", "Paused")
        self.assertEqual(self.run_block()[0], "Logic - Soul Food")

    def test_track_transition_is_read_fresh(self):
        self.run_block()
        self.data["players"][":1.50"] = player("Soul Food II", "Logic")
        self.assertEqual(self.run_block()[0], "Logic - Soul Food II")

    def test_closed_browser_falls_back_without_cached_track(self):
        self.run_block()
        del self.data["names"][CHROME]
        del self.data["players"][":1.50"]
        self.assertEqual(self.run_block()[0], "Drake - Janice STFU")

    def test_bad_or_stopped_browser_falls_back(self):
        for props in (None, {}, player("", "Logic"), player("x", "Logic", "Stopped"),
                      player(["bad type"], "Logic"), player("x", "Logic", "unknown")):
            with self.subTest(props=props):
                self.data["players"][":1.50"] = props
                self.assertEqual(self.run_block()[0], "Drake - Janice STFU")

    def test_other_players_are_ignored(self):
        self.data["names"] = {"org.mpris.MediaPlayer2.vlc": ":1.50"}
        self.assertEqual(self.run_block(), ["", "", "#112233"])

    def test_no_players_clears_text_and_click_state(self):
        self.run_block()
        self.data["names"] = {}
        self.assertEqual(self.run_block(), ["", "", "#112233"])
        self.assertFalse(self.cache.exists())

    def test_invalid_json_clears_text(self):
        self.data["invalid_json"] = True
        self.assertEqual(self.run_block()[0], "")

    def test_timeout_is_bounded_and_clears_text(self):
        self.data["timeout"] = True
        start = time.monotonic()
        self.assertEqual(self.run_block()[0], "")
        self.assertLess(time.monotonic() - start, 2.8)

    def test_markup_quotes_unicode_and_newlines(self):
        props = player('L’été <II> & "one"\nnext\\end', "")
        props["Metadata"]["data"]["xesam:artist"] = variant("as", ["A&B", "C<D>"])
        self.data["players"][":1.50"] = props
        self.assertEqual(self.run_block()[0],
                         'A&amp;B, C&lt;D&gt; - L’été &lt;II&gt; &amp; "one" next\\end')

    def test_pango_invalid_controls_are_removed(self):
        self.data["players"][":1.50"] = player("Song\x01name", "Logic")
        self.assertEqual(self.run_block()[0], "Logic - Songname")

    def test_hung_browser_does_not_hide_healthy_spotify(self):
        self.data["names"][CHROME + "2"] = ":1.51"
        self.data["names"][CHROME + "3"] = ":1.52"
        self.data["names"] = {name: owner for name, owner in self.data["names"].items() if name != SPOTIFY}
        self.data["names"][SPOTIFY] = ":1.649"
        for owner in (":1.50", ":1.51", ":1.52"):
            self.data["players"][owner] = "timeout"
        self.assertEqual(self.run_block()[0], "Drake - Janice STFU")

    def test_multiple_playing_browsers_have_deterministic_priority(self):
        self.data["names"] = {CHROME + "2": ":1.51", **self.data["names"]}
        self.data["players"][":1.51"] = player("Second browser", "Other")
        self.assertEqual(self.run_block()[0], "Logic - Soul Food")

    def test_failed_cache_write_invalidates_old_click_target(self):
        self.run_block()
        helper = runpy.run_path(str(SCRIPT))
        selected = helper["Player"](SPOTIFY, ":1.649", "Other", "Artist", "", "Playing", frozenset())
        with mock.patch.object(helper["tempfile"], "NamedTemporaryFile", side_effect=OSError("disk full")):
            helper["remember"](self.cache, selected)
        self.assertFalse(self.cache.exists())

    def test_unremovable_cache_disables_clicks(self):
        self.run_block()
        helper = runpy.run_path(str(SCRIPT))
        bus = mock.Mock()
        with mock.patch.object(Path, "unlink", side_effect=PermissionError("read only")):
            helper["click"](bus, self.cache, "1")
        bus.properties.assert_not_called()

    def test_missing_artist_and_color_fallback(self):
        self.colors.write_text("color7='invalid'\n")
        self.data["names"] = {SPOTIFY: ":1.649"}
        self.data["players"][":1.649"] = player("Solo", "")
        self.assertEqual(self.run_block(), ["Solo", "Solo", "#cbe4ff"])

    def test_click_uses_previously_displayed_owner(self):
        self.run_block()
        self.data["players"][":1.50"]["PlaybackStatus"] = variant("s", "Paused")
        self.assertEqual(self.run_block("1")[0], "Drake - Janice STFU")
        self.assertEqual(self.actions(), [[":1.50", "/org/mpris/MediaPlayer2",
                                         "org.mpris.MediaPlayer2.Player", "PlayPause"]])

    def test_previous_and_next_route_to_displayed_spotify(self):
        del self.data["names"][CHROME]
        self.run_block()
        self.run_block("2")
        self.run_block("3")
        self.assertEqual([a[-1] for a in self.actions()], ["Previous", "Next"])
        self.assertTrue(all(a[0] == ":1.649" for a in self.actions()))

    def test_no_cache_click_does_not_control_any_player(self):
        self.run_block("1")
        self.assertEqual(self.actions(), [])

    def test_vanished_displayed_player_click_never_controls_fallback(self):
        self.run_block()
        self.data["players"][":1.50"] = None
        self.run_block("3")
        self.assertEqual(self.actions(), [])

    def test_changed_track_click_is_ignored(self):
        self.run_block()
        self.data["players"][":1.50"] = player("New song", "Someone else")
        self.run_block("1")
        self.assertEqual(self.actions(), [])

    def test_capabilities_are_respected(self):
        for button, capability, status in (("1", "CanPause", "Playing"),
                                           ("1", "CanPlay", "Paused"),
                                           ("2", "CanGoPrevious", "Playing"),
                                           ("3", "CanGoNext", "Playing"),
                                           ("1", "CanControl", "Playing")):
            with self.subTest(button=button, capability=capability):
                self.data["names"] = {CHROME: ":1.50"}
                self.data["players"][":1.50"] = player("Soul Food", "Logic", status,
                                                       **{capability: False})
                self.run_block()
                self.run_block(button)
                self.assertEqual(self.actions(), [])

    def test_expired_or_corrupt_cache_disables_clicks(self):
        self.run_block()
        state = json.loads(self.cache.read_text())
        self.assertEqual(self.cache.stat().st_mode & 0o777, 0o600)
        state["time"] = time.time() - 60
        self.cache.write_text(json.dumps(state))
        self.run_block("1")
        self.cache.write_text("broken")
        self.run_block("1")
        self.assertEqual(self.actions(), [])


if __name__ == "__main__":
    unittest.main()
