"""Render terminal bold text and tag Codex; Kitty retains native delivery/actions."""
import os
import re
from html import escape
from typing import Protocol, SupportsIndex
from operator import index


class Notification(Protocol):
    channel_id: int
    application_name: str
    title: str
    body: str


_PROTECTED = re.compile(r"\\.|(?<!`)(`+)[\s\S]*?\1(?!`)")
_BOLD = re.compile(r"(?<!\*)\*\*(?!\*)(?=\S)(.+?)(?<=\S)\*\*(?!\*)", re.DOTALL)


class PangoMarkup(str):
    """Only generated, escaped markup bypasses Kitty's plain-body neutralizer."""
    def replace(self, old: str, new: str, count: SupportsIndex = -1) -> str:
        # Verified against Kitty 0.49.2 FreeDesktopIntegration.notify. Preserve
        # ordinary string operations and never disable escaping globally.
        count_value = index(count)
        if count_value == -1 and (old, new) in (("<", "<\u200c"), ("&", "&\u200c")):
            return self
        return super().replace(old, new, count_value)


def markdown_bold(text: str) -> str | None:
    """Render balanced **strong** spans; leave code and escapes literal."""
    pieces: list[str] = []
    changed = False
    position = 0

    def convert(segment: str) -> str:
        nonlocal changed
        def bold(match: re.Match[str]) -> str:
            nonlocal changed
            changed = True
            return "<b>" + match.group(1) + "</b>"
        return _BOLD.sub(bold, escape(segment))

    for match in _PROTECTED.finditer(text):
        pieces.append(convert(text[position:match.start()]))
        pieces.append(escape(match.group()))
        position = match.end()
    pieces.append(convert(text[position:]))
    return "".join(pieces) if changed else None


def format_notification(notification: Notification, boss: object) -> None:
    manager = getattr(boss, "notification_manager", None)
    integration = getattr(manager, "desktop_integration", None)
    if not getattr(integration, "supports_body_markup", False):
        return
    for field in ("title", "body"):
        text = getattr(notification, field, "")
        if isinstance(text, PangoMarkup):
            continue
        if rendered := markdown_bold(text):
            setattr(notification, field, PangoMarkup(rendered))


def main(notification: Notification) -> bool:
    # Kitty invokes this after its normal permission/visibility checks. Never
    # launch a player here: Dunst runs the optional sound in a separate process.
    try:
        from kitty.fast_data_types import get_boss  # pyright: ignore[reportMissingImports]

        boss = get_boss()
        format_notification(notification, boss)
        if not notification.channel_id:
            return False
        window = boss.window_id_map.get(notification.channel_id)
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
