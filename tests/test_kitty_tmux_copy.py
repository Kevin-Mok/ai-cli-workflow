#!/usr/bin/env python3
"""Check Kitty copy routing without importing its frozen GUI runtime."""
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]


class CopyRouting(unittest.TestCase):
    def setUp(self):
        boss_module = ModuleType("kitty.boss")
        boss_module.Boss = object
        screen_module = ModuleType("kitty.fast_data_types")
        screen_module.SCROLL_FULL = -999997
        handler_module = ModuleType("kittens.tui.handler")
        handler_module.result_handler = lambda **kwargs: lambda function: function
        spec = importlib.util.spec_from_file_location("tmux_copy", ROOT / "dot_config/kitty/tmux_copy.py")
        self.adapter = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {"kitty.boss": boss_module, "kitty.fast_data_types": screen_module, "kittens.tui.handler": handler_module}):
            spec.loader.exec_module(self.adapter)
        self.window = Mock()
        self.window.screen.columns = 80
        self.window.screen.lines = 24
        self.window.text_for_selection.return_value = ""
        self.window.child.cmdline_of_pid.return_value = ["tmux", "attach"]
        self.window.child.foreground_processes = []
        self.boss = SimpleNamespace(window_id_map={1: self.window})

    def copy(self):
        with patch.object(self.adapter.os, "tcgetpgrp", return_value=42):
            self.adapter.handle_result([], None, 1, self.boss)

    def test_direct_tmux_with_empty_cached_process_list(self):
        self.copy()
        self.window.write_to_child.assert_called_once_with(b"\x1b[99~")
        self.window.copy_to_clipboard.assert_not_called()

    def test_fish_wrapper_group_includes_tmux(self):
        self.window.child.cmdline_of_pid.return_value = ["fish", "-c", "tmux-attach config"]
        self.window.child.foreground_processes = [
            {"pid": 42, "cmdline": ["fish", "-c", "tmux-attach config"]},
            {"pid": 43, "cmdline": ["/usr/bin/tmux", "attach", "-t", "config"]},
        ]
        self.copy()
        self.window.write_to_child.assert_called_once_with(b"\x1b[99~")
        self.window.copy_to_clipboard.assert_not_called()

    def test_native_selection_takes_priority(self):
        self.window.text_for_selection.return_value = "native text"
        self.copy()
        self.window.copy_to_clipboard.assert_called_once_with()
        self.window.write_to_child.assert_not_called()

    def test_non_tmux_group_does_not_receive_private_key(self):
        self.window.child.cmdline_of_pid.return_value = ["fish"]
        self.window.child.foreground_processes = [{"cmdline": []}, {"cmdline": ["ssh", "host"]}]
        self.copy()
        self.window.copy_to_clipboard.assert_called_once_with()
        self.window.write_to_child.assert_not_called()

    def test_tty_lookup_error_retains_supported_fallback(self):
        self.window.child.foreground_cmdline = ["tmux: client"]
        with patch.object(self.adapter.os, "tcgetpgrp", side_effect=OSError):
            self.adapter.handle_result([], None, 1, self.boss)
        self.window.write_to_child.assert_called_once_with(b"\x1b[99~")

    def select_all(self):
        with patch.object(self.adapter.os, "tcgetpgrp", return_value=42):
            self.adapter.handle_result(["tmux_copy.py", "select-all"], None, 1, self.boss)

    def test_select_all_routes_to_tmux_even_with_old_native_selection(self):
        self.window.text_for_selection.return_value = "old selection"
        self.select_all()
        self.window.screen.clear_selection.assert_called_once_with()
        self.window.write_to_child.assert_called_once_with(b"\x01")
        self.window.copy_to_clipboard.assert_not_called()

    def test_select_all_native_uses_entire_retained_history(self):
        self.window.child.cmdline_of_pid.return_value = ["fish"]
        self.select_all()
        screen = self.window.screen
        screen.scroll.assert_any_call(-999997, True)
        screen.start_selection.assert_called_once_with(0, 0)
        screen.scroll.assert_any_call(-999997, False)
        screen.update_selection.assert_called_once_with(screen.columns - 1, screen.lines - 1, True)
        self.window.write_to_child.assert_not_called()
        self.window.copy_to_clipboard.assert_not_called()

    def test_closed_window_is_ignored(self):
        self.adapter.handle_result([], None, 99, self.boss)
        self.window.write_to_child.assert_not_called()
        self.window.copy_to_clipboard.assert_not_called()


if __name__ == "__main__":
    unittest.main()
