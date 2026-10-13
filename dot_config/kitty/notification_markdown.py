"""No-UI Kitty activation and native notification samples."""
from pathlib import Path
import runpy
from typing import TYPE_CHECKING

# Kitty APIs are embedded in its frozen Python runtime, not host site-packages.
from kittens.tui.handler import result_handler  # pyright: ignore[reportMissingImports]

if TYPE_CHECKING:
    from kitty.boss import Boss  # pyright: ignore[reportMissingImports]


def main(args: list[str]) -> None:
    pass


@result_handler(no_ui=True)
def handle_result(args: list[str], answer: object, target_window_id: int, boss: "Boss") -> str:
    case = args[1] if len(args) > 1 else "bold"
    samples = {
        "bold": ("Markdown **bold** test", "Normal text; **this should be bold**; normal again."),
        "literal": ("Markdown literal test", "**Bold** plus literal <span> & `**code**` and \\**escaped**."),
        "plain": ("Markdown plain test", "Plain notification text stays unchanged."),
    }
    if case not in (*samples, "activate"):
        raise ValueError("Use bold, literal, plain or activate.")
    from kitty.constants import config_dir  # pyright: ignore[reportMissingImports]
    callback = runpy.run_path(str(Path(config_dir) / "notifications.py"))["main"]
    manager = boss.notification_manager
    manager.filter_script = callback
    if case == "activate":
        return "Notification Markdown active."
    from kitty.notifications import OnlyWhen  # pyright: ignore[reportMissingImports, reportAttributeAccessIssue]
    command = manager.create_notification_cmd()
    command.title, command.body = samples[case]
    command.only_when = OnlyWhen.always
    command.application_name = "notification-markdown-test"
    command.sound_name = "silent"
    command.timeout = 15000
    command.identifier = "notification-markdown-" + case
    if manager.notify_with_command(command, target_window_id) is None:
        raise RuntimeError("The sample was filtered; check Kitty notification rules.")
    return case.capitalize() + " sample sent."
