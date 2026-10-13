"""Copy native Kitty selections or a released tmux selection with one shortcut."""
import os

from kitty.boss import Boss
from kittens.tui.handler import result_handler


def main(args: list[str]) -> None:
    return None


@result_handler(no_ui=True)
def handle_result(args: list[str], answer: object, target_window_id: int, boss: Boss) -> None:
    window = boss.window_id_map.get(target_window_id)
    if window is None:
        return
    if window.text_for_selection():
        window.copy_to_clipboard()
        return
    # Query the terminal's foreground group directly: Kitty's cached process
    # list can be empty even while a tmux client owns the terminal.
    try:
        group = os.tcgetpgrp(window.child.child_fd)
        command = window.child.cmdline_of_pid(group)
    except (OSError, TypeError):
        command = window.child.foreground_cmdline
    tmux_foreground = bool(command and os.path.basename(command[0]).split(":", 1)[0] == "tmux")
    if tmux_foreground:
        # Dedicated tmux User0; no global keyboard-protocol changes required.
        window.write_to_child(b"\x1b[99~")
    else:
        window.copy_to_clipboard()
