"""Tag local Codex popups; Kitty retains delivery, suppression and focus actions."""
import os
from typing import Protocol


class Notification(Protocol):
    channel_id: int
    application_name: str


def main(notification: Notification) -> bool:
    # Kitty invokes this after its normal permission/visibility checks. Never
    # launch a player here: Dunst runs the optional sound in a separate process.
    try:
        from kitty.fast_data_types import get_boss

        if not notification.channel_id:
            return False
        window = get_boss().window_id_map.get(notification.channel_id)
        if window is None:
            return False
        for process in window.child.foreground_processes:
            pid = process.get('pid')
            if not isinstance(pid, int) or pid <= 0:
                continue
            try:
                executable = os.path.basename(os.readlink(f'/proc/{pid}/exe'))
            except OSError:
                # One process may exit while others in its foreground group live.
                continue
            if executable == 'codex':
                notification.application_name = 'codex-kitty'
                break
    except Exception:
        # API changes or process races must not swallow the original popup.
        return False
    return False
