#!/usr/bin/env python3
"""Defining checks for cadence, discovery and input dismissal; synthetic paths only."""
import importlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
try:
    core = importlib.import_module("media_screensaver.core")
except ModuleNotFoundError:
    core = None

class ConveyorTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(core, "media conveyor core has not been implemented")

    def test_item_identity_survives_ten_second_steps_and_exits_after_slide(self):
        c = core.Conveyor([Path("a.mp4"), Path("b.jpg")], start=100)
        first = c.entries[0]
        self.assertEqual(first.slot, 0)
        c.tick(109.999)
        self.assertEqual(first.slot, 0)
        c.tick(110)
        self.assertEqual(first.slot, 1)
        self.assertEqual(c.progress(110.375), 0.5)
        c.tick(120)
        self.assertEqual(first.slot, 2)
        c.tick(130)
        self.assertEqual(first.slot, 3)
        self.assertIn(first, c.entries)
        c.tick(130.75)
        self.assertNotIn(first, c.entries)

    def test_delayed_frames_do_not_shift_cadence(self):
        c = core.Conveyor([Path("a.jpg")], start=0)
        c.tick(10.4)
        self.assertEqual(c.next_advance, 20)
        c.tick(30.1)
        self.assertEqual(c.next_advance, 40)
        self.assertEqual(len(c.entries), 4)
        c.tick(30.8)
        self.assertEqual(len(c.entries), 3)

    def test_random_selection_avoids_adjacent_duplicates_when_possible(self):
        c = core.Conveyor([Path("a.jpg"), Path("b.jpg"), Path("c.mp4")], start=0)
        last = c.entries[-1].path
        for i in range(1, 100):
            c.tick(i * 10 + 1)
            current = c.entries[-1].path
            self.assertNotEqual(last, current)
            last = current

    def test_rejecting_corrupt_item_does_not_stop_other_items(self):
        c = core.Conveyor([Path("bad.mp4"), Path("good.jpg")], start=0)
        c.reject(Path("bad.mp4"))
        for i in range(1, 5):
            c.tick(i * 10 + 1)
            self.assertEqual(c.entries[-1].path, Path("good.jpg"))
        c.reject(Path("good.jpg"))
        c.tick(60)
        self.assertFalse(c.paths)

    def test_discovery_is_recursive_case_insensitive_and_read_only(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "nested").mkdir()
            for name in ("JPG", "jpeg", "PNG", "webp", "heic", "MP4", "mov", "mkv", "txt"):
                (root / "nested" / ("item." + name)).write_bytes(b"synthetic")
            (root / "link.jpg").symlink_to(root / "nested" / "item.JPG")
            paths = core.discover(root)
            self.assertEqual(len(paths), 8)
            self.assertNotIn(root / "link.jpg", paths)
            self.assertTrue(all(p.read_bytes() == b"synthetic" for p in paths))
            with self.assertRaisesRegex(ValueError, "unavailable"):
                core.discover(root / "missing")

    def test_live_monitor_parser_retains_unequal_vertical_offsets(self):
        monitors = core.parse_monitors("""Monitors: 3
 0: +*DP-2 3840/700x2160/400+2048+0 DP-2
 1: +DVI-D-0 2048/510x1152/287+0+504 DVI-D-0
 2: +HDMI-0 1920/598x1080/336+5888+540 HDMI-0
""")
        self.assertEqual([m["name"] for m in monitors], ["DVI-D-0", "DP-2", "HDMI-0"])
        self.assertEqual(monitors[0]["y"], 504)
        self.assertEqual(core.placement(monitors, 1, 0.5), {"x": 1024, "y": 252, "width": 2944, "height": 1656})
        self.assertEqual(core.placement(monitors, 0, 0)["x"], -2048)
        self.assertEqual(core.placement(monitors, 3, 1)["x"], 7808)
        with self.assertRaisesRegex(ValueError, "three"):
            core.parse_monitors("Monitors: 0")


if __name__ == "__main__":
    unittest.main()
