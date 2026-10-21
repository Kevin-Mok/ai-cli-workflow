#!/usr/bin/env python3
"""Behavior checks for the DND i3blocks click target and text color."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "dot_config/i3blocks/scripts/executable_dnd"


class DndBlockTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.bin = self.home / "bin"
        self.bin.mkdir()
        self.state = self.home / "paused"
        self.state.write_text("false")
        colors = self.home / ".cache/wal/colors.sh"
        colors.parent.mkdir(parents=True)
        colors.write_text("color7='#d0bce2'\n")
        dunstctl = self.bin / "dunstctl"
        dunstctl.write_text("""#!/bin/sh
case "$1" in
  is-paused) cat "$DND_STATE" ;;
  set-paused)
    if [ "$2" = toggle ]; then
      [ "$(cat "$DND_STATE")" = true ] && value=false || value=true
      printf '%s' "$value" > "$DND_STATE"
    else
      printf '%s' "$2" > "$DND_STATE"
    fi ;;
  count) echo 2 ;;
esac
""")
        dunstctl.chmod(0o755)
        self.env = {**os.environ, "HOME": str(self.home), "PATH": f"{self.bin}:{os.environ['PATH']}", "DND_STATE": str(self.state)}
        self.env.pop("color7", None)
        self.colors = colors

    def run_block(self, button=None):
        env = self.env.copy()
        if button is not None:
            env["BLOCK_BUTTON"] = str(button)
        else:
            env.pop("BLOCK_BUTTON", None)
        return subprocess.check_output(["bash", str(SCRIPT)], env=env, text=True).strip()

    def test_unpaused_uses_wal_color7(self):
        self.assertEqual(self.run_block(), '<span color="#d0bce2">Notis</span>')

    def test_unpaused_falls_back_to_plain_text_without_color7(self):
        for setup in ("missing", "without-color7"):
            with self.subTest(setup=setup):
                if setup == "missing":
                    self.colors.unlink()
                else:
                    self.colors.write_text("color8='#ffffff'\n")
                self.assertEqual(self.run_block(), "Notis")
                if setup == "missing":
                    self.colors.write_text("color7='#d0bce2'\n")

    def test_left_click_disables_pause_from_either_state(self):
        for initial in ("false", "true"):
            with self.subTest(initial=initial):
                self.state.write_text(initial)
                self.run_block(1)
                self.assertEqual(self.state.read_text(), "false")

    def test_right_click_enables_pause_from_either_state(self):
        for initial in ("false", "true"):
            with self.subTest(initial=initial):
                self.state.write_text(initial)
                self.run_block(3)
                self.assertEqual(self.state.read_text(), "true")

    def test_no_click_and_middle_click_leave_state_unchanged(self):
        for button in (None, 2):
            with self.subTest(button=button):
                self.state.write_text("false")
                self.run_block(button)
                self.assertEqual(self.state.read_text(), "false")

    def test_paused_queue_remains_red(self):
        self.state.write_text("true")
        self.assertEqual(self.run_block(), "<span color='#ff6b6b'>DND (2)</span>")


if __name__ == "__main__":
    unittest.main()
