"""No-UI adapter: retain actual per-OS-window baselines inside Kitty."""
import json
import math

from kittens.tui.handler import result_handler
from kitty.fast_data_types import os_window_font_size

RATIOS = {"DP-2": 1.0, "DVI-D-0": (1152 / 287) / (2160 / 400),
          "HDMI-0": (1080 / 336) / (2160 / 400)}


def main(args):
    pass


@result_handler(no_ui=True)
def handle_result(args, answer, target_window_id, boss):
    mode = args[1]
    outputs = json.loads(args[2])
    if mode not in ("apply", "status", "restore") or not isinstance(outputs, dict):
        raise ValueError("Expected apply, status or restore and an output map")
    windows = list(boss.list_os_windows())
    state = getattr(boss, "_monitor_font_state", {})
    live = {w["id"] for w in windows}
    state = {wid: entry for wid, entry in state.items() if wid in live}
    changes, rows, pending = {}, [], {}
    for window in windows:
        wid = window["id"]
        current = os_window_font_size(wid)
        if not current or not math.isfinite(current) or current <= 0:
            continue
        output = outputs.get(str(window["platform_window_id"]))
        ratio = RATIOS.get(output)
        previous = state.get(wid)
        baseline = current if previous is None else previous["baseline"]
        if previous is not None and abs(current - previous["actual"]) > 0.001:
            # A user zoom belongs to the monitor on which it was last observed.
            baseline = current / previous["ratio"]
        target = baseline if mode == "restore" else baseline * ratio if ratio else current
        target = max(4., target) if ratio and ratio != 1 and mode != "restore" else target
        known = ratio is not None or (mode == "restore" and previous is not None)
        if known and mode != "status":
            if abs(current - target) > 0.001:
                changes[wid] = target
            pending[wid] = {"baseline": baseline, "ratio": 1. if mode == "restore" else ratio}
        rows.append({"os_window_id": wid, "platform_window_id": window["platform_window_id"],
                     "output": output, "current": current, "baseline": baseline,
                     "target": target, "tracked": previous is not None})
    if changes:
        # Kitty 0.49.2's targeted font action ends here; this never uses focus.
        boss._change_font_size(changes)
    if mode != "status":
        for wid, entry in pending.items():
            entry["actual"] = os_window_font_size(wid)
            state[wid] = entry
        boss._monitor_font_state = {} if mode == "restore" else state
    return json.dumps(rows)
