#!/usr/bin/env python3
"""Exercise real tmux mouse input on an isolated pseudoterminal/server."""
import fcntl
import os
from pathlib import Path
import pty
import re
import select
import struct
import subprocess
import tempfile
import termios
import threading
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = r'''
import os, sys, tty
for n in range(1, 3001):
    print(f"HISTORY {n:06d}" + (" | WRAPPED " + "word " * 35 + "END" if n % 10 == 0 else ""))
print("READY: a enables application mouse; z disables; type hello and Enter")
sys.stdout.flush()
tty.setraw(0)
line = b""
while True:
    b = os.read(0, 1)
    if b == b"a":
        os.write(1, b"\x1b[?1000h\x1b[?1006h")
    elif b == b"z":
        os.write(1, b"\x1b[?1000l\x1b[?1006l")
    elif b == b"\x1b":
        event = b
        while not event.endswith((b"M", b"m")):
            event += os.read(0, 1)
        os.write(1, b"\r\nAPP_MOUSE " + event.replace(b"\x1b", b"ESC") + b"\r\n")
    elif b in (b"\r", b"\n"):
        os.write(1, b"\r\nINPUT " + line + b"\r\n")
        line = b""
    else:
        line += b
'''


class MouseScrolling(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="tmux-mouse-")
        self.sock = str(Path(self.temp.name) / "socket")
        fixture = Path(self.temp.name) / "fixture.py"
        fixture.write_text(FIXTURE)
        env = dict(os.environ, TERM="xterm-256color")
        env.pop("TMUX", None)
        self.env = env
        self.tmux("-f", "/dev/null", "new-session", "-d", "-x", "80", "-y", "24", "-s", "fixture", "sleep 60")
        self.tmux("source-file", str(ROOT / "dot_tmux.conf"))
        self.tmux("new-window", "-n", "history", f"python3 {fixture}")
        self.master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 24, 80, 0, 0))
        self.client = subprocess.Popen(["tmux", "-S", self.sock, "attach", "-t", "fixture"], stdin=slave, stdout=slave, stderr=slave, env=env, start_new_session=True)
        os.close(slave)
        self.output = bytearray()
        self.stop = threading.Event()
        def drain():
            while not self.stop.is_set():
                if select.select([self.master], [], [], .05)[0]:
                    try:
                        self.output.extend(os.read(self.master, 65536))
                    except OSError:
                        break
        self.reader = threading.Thread(target=drain)
        self.reader.start()
        self.wait_for(lambda: "READY:" in self.tmux("capture-pane", "-p"))
        # Let the attached client establish its mouse mode before injecting events.
        self.wait_for(lambda: b"?1006h" in self.output)

    def tmux(self, *args):
        return subprocess.check_output(["tmux", "-S", self.sock, *args], env=self.env, stderr=subprocess.STDOUT, text=True).strip()

    def wait_for(self, predicate, timeout=3):
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            if predicate():
                return
            time.sleep(.03)
        self.fail("Timed out waiting for expected tmux state")

    def fmt(self, name):
        return self.tmux("display-message", "-p", "#{" + name + "}")

    def mouse(self, code, x=20, y=10, release=False):
        os.write(self.master, f"\x1b[<{code};{x};{y}{'m' if release else 'M'}".encode())
        time.sleep(.08)

    def tearDown(self):
        self.tmux("kill-server")  # Only our unique disposable server.
        self.client.wait(timeout=3)
        self.stop.set()
        self.reader.join(timeout=1)
        os.close(self.master)
        self.temp.cleanup()

    def test_wheel_history_selection_and_live_input(self):
        before = min(int(n) for n in re.findall(r"HISTORY (\d+)", self.tmux("capture-pane", "-p")))
        self.output.clear()
        self.mouse(64)
        self.mouse(64)
        self.assertEqual(self.fmt("pane_in_mode"), "1")
        self.assertGreater(int(self.fmt("scroll_position")), 0)
        # Real attached-client output must paint earlier history.
        self.tmux("refresh-client")
        self.wait_for(lambda: any(int(n) < before for n in re.findall(rb"HISTORY (\d+)", bytes(self.output))))
        for _ in range(8):
            self.mouse(65)
        self.assertEqual(self.fmt("pane_in_mode"), "0")
        os.write(self.master, b"hello\r")
        self.wait_for(lambda: "INPUT hello" in self.tmux("capture-pane", "-p"))

    def test_alt_wheel_overrides_app_mouse_without_breaking_plain_wheel(self):
        os.write(self.master, b"a")
        self.wait_for(lambda: self.fmt("mouse_any_flag") == "1")
        self.mouse(64)
        self.assertEqual(self.fmt("pane_in_mode"), "0")
        self.assertIn("APP_MOUSE ESC[<64;20;10M", self.tmux("capture-pane", "-p"))
        self.mouse(0)
        self.assertEqual(self.fmt("pane_in_mode"), "0")
        self.assertIn("APP_MOUSE ESC[<0;20;10M", self.tmux("capture-pane", "-p"))
        self.mouse(0, release=True)
        self.mouse(72)  # Alt + wheel up (SGR modifier bit 8).
        self.assertEqual(self.fmt("pane_in_mode"), "1", "Alt+wheel must enter tmux history even when the app owns mouse")
        self.assertGreater(int(self.fmt("scroll_position")), 0)
        for _ in range(8):
            self.mouse(73)
        self.assertEqual(self.fmt("pane_in_mode"), "0")
        os.write(self.master, b"hello\r")
        self.wait_for(lambda: "INPUT hello" in self.tmux("capture-pane", "-p"))

    def test_shift_wheel_browses_history_in_mouse_aware_app(self):
        os.write(self.master, b"a")
        self.wait_for(lambda: self.fmt("mouse_any_flag") == "1")
        self.mouse(68)
        self.assertEqual(self.fmt("pane_in_mode"), "1", "Shift+wheel must browse pane history")
        self.assertGreater(int(self.fmt("scroll_position")), 0)
        for _ in range(8):
            self.mouse(69)
        self.assertEqual(self.fmt("pane_in_mode"), "0")

    def test_drag_release_preserves_selection_then_escape_returns_live(self):
        self.mouse(64)
        self.mouse(64)
        self.mouse(0, 1, 8)
        self.mouse(32, 15, 8)
        self.mouse(0, 15, 8, release=True)
        self.assertEqual(self.fmt("pane_in_mode"), "1", "Releasing the mouse must keep history and highlight visible")
        self.assertEqual(self.fmt("selection_present"), "1")
        self.assertEqual(self.fmt("selection_active"), "0", "Selection must stop extending after release")
        os.write(self.master, b"\x1b")
        self.wait_for(lambda: self.fmt("pane_in_mode") == "0")
        os.write(self.master, b"hello\r")
        self.wait_for(lambda: "INPUT hello" in self.tmux("capture-pane", "-p"))

    def test_stationary_top_edge_drag_selects_multiple_screens_and_wrapped_lines(self):
        import base64
        self.mouse(0, 1, 8)
        self.mouse(32, 1, 7)
        self.mouse(32, 1, 1)  # First text row; no wheel events or repeated motion.
        self.wait_for(lambda: int(self.fmt("scroll_position") or 0) > 48, timeout=5)
        self.assertEqual(self.fmt("selection_active"), "1")
        self.mouse(0, 1, 1, release=True)
        self.assertEqual(self.fmt("selection_present"), "1")
        self.assertEqual(self.fmt("selection_active"), "0")
        position = self.fmt("scroll_position")
        time.sleep(.25)  # Several 50ms timer ticks must not scroll after release.
        self.assertEqual(self.fmt("scroll_position"), position)
        self.output.clear()
        os.write(self.master, b"\x1b[99~")
        self.wait_for(lambda: b"]52;" in self.output)
        match = re.search(rb"\x1b\]52;[^;]*;([^\x07\x1b]+)", bytes(self.output))
        copied = base64.b64decode(match.group(1)).decode()
        history = "\n".join(
            f"HISTORY {n:06d}" + (" | WRAPPED " + "word " * 35 + "END" if n % 10 == 0 else "")
            for n in range(1, 3001)
        )
        self.assertGreater(copied.count("\n"), 24)
        self.assertIn(" | WRAPPED " + "word " * 35 + "END", copied)
        self.assertIn(copied.rstrip("\n"), history, "Soft wraps must preserve the original logical text")
        self.assertEqual(self.fmt("scroll_position"), position)

    def test_bottom_edge_release_preserves_text_and_stops_scrolling(self):
        self.tmux("copy-mode")
        self.tmux("send-keys", "-X", "-N", "100", "scroll-up")
        self.mouse(0, 1, 8)
        self.mouse(32, 1, 9)
        self.mouse(32, 1, 23)
        self.wait_for(lambda: int(self.fmt("scroll_position")) < 80)
        self.assertEqual(self.fmt("selection_active"), "1")
        self.mouse(0, 1, 23, release=True)
        self.assertEqual(self.fmt("selection_active"), "0")
        position = self.fmt("scroll_position")
        self.tmux("send-keys", "-X", "copy-selection-no-clear")
        copied = self.tmux("show-buffer")
        time.sleep(.25)
        self.assertEqual(self.fmt("scroll_position"), position)
        self.tmux("send-keys", "-X", "copy-selection-no-clear")
        self.assertEqual(self.tmux("show-buffer"), copied)
        self.assertIn("HISTORY", copied)

    def test_tiny_pane_release_does_not_force_cursor_to_other_edge(self):
        self.tmux("set-window-option", "window-size", "manual")
        self.tmux("resize-window", "-x", "80", "-y", "2")
        self.assertEqual(self.fmt("pane_height"), "2")
        self.mouse(0, 1, 2)
        self.mouse(32, 1, 1)
        self.assertEqual(self.fmt("copy_cursor_y"), "0")
        self.mouse(0, 1, 1, release=True)
        self.assertEqual(self.fmt("selection_active"), "0")
        self.assertEqual(self.fmt("copy_cursor_y"), "0", "Tiny panes have no interior row for parking")

    def test_explicit_copy_sends_selected_text_to_terminal_clipboard_and_keeps_view(self):
        import base64
        self.mouse(64)
        self.mouse(64)
        self.mouse(0, 1, 8)
        self.mouse(32, 15, 8)
        self.tmux("send-keys", "-X", "stop-selection")
        position = self.fmt("scroll_position")
        self.output.clear()
        os.write(self.master, b"\x1b[99~")  # Kitty copy adapter's dedicated tmux user key.
        self.wait_for(lambda: b"]52;" in self.output)
        match = re.search(rb"\x1b\]52;[^;]*;([^\x07\x1b]+)", bytes(self.output))
        self.assertIsNotNone(match)
        copied = base64.b64decode(match.group(1)).decode()
        self.assertIn("HISTORY", copied)
        self.assertEqual(copied.strip(), self.tmux("show-buffer"))
        self.assertEqual(self.fmt("pane_in_mode"), "1")
        self.assertEqual(self.fmt("selection_present"), "1")
        self.assertEqual(self.fmt("scroll_position"), position)
        self.output.clear()
        os.write(self.master, b"\x1b[99~")
        self.wait_for(lambda: b"]52;" in self.output)
        second = re.search(rb"\x1b\]52;[^;]*;([^\x07\x1b]+)", bytes(self.output))
        self.assertEqual(base64.b64decode(second.group(1)).decode(), copied)
        self.assertEqual(self.fmt("selection_present"), "1")
        self.tmux("send-keys", "-X", "cancel")
        self.mouse(0, 15, 8, release=True)

    def test_copy_without_selection_does_not_write_clipboard_or_interrupt_input(self):
        self.output.clear()
        os.write(self.master, b"\x1b[99~")
        self.wait_for(lambda: b"Ctrl+Shift+C" in self.output)
        self.assertNotIn(b"]52;", self.output)
        self.assertEqual(self.fmt("pane_in_mode"), "0")
        os.write(self.master, b"hello\r")
        self.wait_for(lambda: "INPUT hello" in self.tmux("capture-pane", "-p"))

    def test_new_pane_retains_more_than_two_thousand_lines(self):
        self.assertTrue("HISTORY 000001" in self.tmux("capture-pane", "-p", "-S", "-"), "New pane history must retain early output beyond 2000 lines")


class ViMouseScrolling(MouseScrolling):
    def setUp(self):
        super().setUp()
        self.tmux("set-window-option", "mode-keys", "vi")


if __name__ == "__main__":
    unittest.main()
