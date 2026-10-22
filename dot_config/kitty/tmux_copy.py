"""Select or copy Kitty text and foreground tmux pane history."""
import os

from kitty.boss import Boss
from kitty.fast_data_types import SCROLL_FULL
from kittens.tui.handler import result_handler


def main(args: list[str]) -> None:
    return None


@result_handler(no_ui=True)
def handle_result(args: list[str], answer: object, target_window_id: int, boss: Boss) -> None:
    window = boss.window_id_map.get(target_window_id)
    if window is None:
        return
    select_all = len(args) > 1 and args[1] == "select-all"
    if not select_all and window.text_for_selection():
        window.copy_to_clipboard()
        return
    # Query the terminal's foreground group directly: Kitty's cached process
    # list can be empty even while a tmux client owns the terminal.
    try:
        group = os.tcgetpgrp(window.child.child_fd)
        command = window.child.cmdline_of_pid(group)
    except (OSError, TypeError):
        command = window.child.foreground_cmdline
    # Noninteractive fish can lead the group while tmux is another member.
    commands = [command] + [process.get("cmdline") for process in window.child.foreground_processes]
    tmux_foreground = any(cmd and os.path.basename(cmd[0]).split(":", 1)[0] == "tmux" for cmd in commands)
    if select_all:
        window.screen.clear_selection()
        if tmux_foreground:
            window.write_to_child(b"\x01")
        else:
            # Kitty 0.49.2 stores each selection endpoint with its scroll offset.
            screen = window.screen
            screen.scroll(SCROLL_FULL, True)
            screen.start_selection(0, 0)
            screen.scroll(SCROLL_FULL, False)
            screen.update_selection(screen.columns - 1, screen.lines - 1, True)
    elif tmux_foreground:
        # Dedicated tmux User0; no global keyboard-protocol changes required.
        window.write_to_child(b"\x1b[99~")
    else:
        window.copy_to_clipboard()
