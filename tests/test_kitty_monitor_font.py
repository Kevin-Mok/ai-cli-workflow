"""Defining monitor/baseline tests, with Kitty APIs replaced by a tiny fake."""
import importlib.util
from importlib.machinery import SourceFileLoader
import json
from pathlib import Path
import sys
from types import ModuleType
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sizes = {}
handler = ModuleType("kittens.tui.handler")
handler.result_handler = lambda **kw: lambda fn: fn
fast = ModuleType("kitty.fast_data_types")
fast.os_window_font_size = lambda wid: sizes[wid]


def load(name, path):
    spec = importlib.util.spec_from_loader(name, SourceFileLoader(name, str(ROOT / path)))
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, {handler.__name__: handler, fast.__name__: fast}):
        spec.loader.exec_module(module)
    return module


adapter = load("monitor_font", "dot_config/kitty/monitor_font.py")
watcher = load("watcher", "scripts/executable_kitty-monitor-font")


class Boss:
    def __init__(self):
        self.windows = [{"id": i, "platform_window_id": 100 + i} for i in sizes]
        self.changes = []

    def list_os_windows(self):
        return iter(self.windows)

    def _change_font_size(self, changes):
        self.changes.append(changes.copy())
        sizes.update(changes)


class Scaling(unittest.TestCase):
    def setUp(self):
        sizes.clear()
        sizes.update({1: 12., 2: 19.})
        self.boss = Boss()

    def call(self, outputs, mode="apply"):
        return json.loads(adapter.handle_result(
            ["monitor_font.py", mode, json.dumps(outputs)], None, 1, self.boss))

    def test_mixed_baselines_roundtrips_and_restart(self):
        for _ in range(5):
            self.call({"101": "DVI-D-0", "102": "HDMI-0"})
            self.assertAlmostEqual(sizes[1], 12 * adapter.RATIOS["DVI-D-0"], places=3)
            self.assertAlmostEqual(sizes[2], 19 * adapter.RATIOS["HDMI-0"], places=3)
            # Re-import simulates watcher/kitten module restart, retaining Kitty boss.
            restarted = load("restart", "dot_config/kitty/monitor_font.py")
            restarted.handle_result(["monitor_font.py", "apply", '{"101":"DVI-D-0","102":"HDMI-0"}'], None, 2, self.boss)
            self.call({"101": "DP-2", "102": "DP-2"})
            self.assertEqual(sizes, {1: 12., 2: 19.})

    def test_zoom_preserved_even_when_move_precedes_poll(self):
        self.call({"101": "HDMI-0"})
        sizes[1] += 1
        expected = sizes[1] / adapter.RATIOS["HDMI-0"]
        self.call({"101": "DP-2"})
        self.assertAlmostEqual(sizes[1], expected, places=3)
        self.assertEqual(sizes[2], 19.)

    def test_unknown_missing_status_and_restore(self):
        self.call({"101": "unknown", "102": "DP-2"})
        self.assertEqual(self.boss.changes, [])
        self.call({"101": "HDMI-0"}, "status")
        self.assertEqual(sizes[1], 12.)
        self.call({"101": "HDMI-0"})
        self.call({}, "restore")
        self.assertEqual(sizes, {1: 12., 2: 19.})

    def test_new_side_window_and_closed_cleanup(self):
        self.call({"101": "HDMI-0"})
        self.boss.windows = self.boss.windows[1:]
        self.call({"102": "DVI-D-0"})
        self.assertAlmostEqual(sizes[2], 19 * adapter.RATIOS["DVI-D-0"], places=3)
        self.assertNotIn(1, self.boss._monitor_font_state)

    def test_invalid_request_does_not_mutate(self):
        with self.assertRaises(ValueError):
            self.call({"101": "HDMI-0"}, "invalid")
        self.assertEqual(sizes, {1: 12., 2: 19.})

    def test_unfocused_window_only_and_main_noop(self):
        self.call({"101": "DP-2", "102": "HDMI-0"})
        self.assertEqual(sizes[1], 12.)
        self.assertEqual(set(self.boss.changes[0]), {2})

    def test_independent_instances(self):
        first = self.boss
        second = Boss()
        self.call({"101": "DVI-D-0"})
        self.assertFalse(hasattr(second, "_monitor_font_state"))
        self.boss = first
        self.call({"101": "DP-2"})
        self.assertEqual(sizes[1], 12.)


class Watcher(unittest.TestCase):
    def test_nested_workspaces_and_floating_windows(self):
        tree = {"nodes": [{"type": "output", "name": "HDMI-0", "nodes": [
            {"type": "workspace", "nodes": [{"window": 11}],
             "floating_nodes": [{"window": 12}]}]}]}
        self.assertEqual(watcher.placements(tree), {"11": "HDMI-0", "12": "HDMI-0"})

    def test_fragmented_ipc_and_disconnect(self):
        import struct
        message = b'{"success":true}'
        packet = struct.pack("=6sII", b"i3-ipc", len(message), 2) + message
        class FragmentedSocket:
            def __init__(self):
                self.chunks = iter(bytes([byte]) for byte in packet)

            def recv(self, count):
                return next(self.chunks, b"")
        sock = FragmentedSocket()
        self.assertEqual(watcher.receive(sock), (2, {"success": True}))
        with self.assertRaises(ConnectionError):
            watcher.receive(sock)

    def test_missing_socket_is_counted_and_never_falls_back_to_focus(self):
        import stat
        metadata = type("Metadata", (), {"st_mode": stat.S_IFSOCK, "st_uid": watcher.os.getuid()})()
        with patch.object(watcher.glob, "glob", side_effect=[["/tmp/kitty-1"], []]), \
             patch.object(watcher.os, "lstat", return_value=metadata), \
             patch.object(watcher, "run", side_effect=['{"nodes":[]}', OSError("closed")]) as run:
            self.assertEqual(watcher.reconcile("status", "kitty", "adapter"),
                             {"windows": [], "unavailable_sockets": 1})
            command = run.call_args.args[0]
            self.assertIn("unix:/tmp/kitty-1", command)
            self.assertIn("--match", command)
            self.assertNotIn("action", command)


if __name__ == "__main__":
    unittest.main()
