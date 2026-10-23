# Monitor-aware Kitty font sizing

Keep the preferred font size on the main 4K display and shrink each terminal on
the side displays. The i3 watcher follows window and workspace moves, preserves
each terminal's baseline and manual zoom, and restores that size on return.

## Behavior

New terminals default to19pt on the main 4K display,14.12pt on the left and
11.31pt on the right, matching the readable reference terminal. Ctrl+Return
uses the same19pt baseline. tmux windows/panes inherit the containing terminal
font. Existing windows retain their zoom; opening a new tmux window alone does
not change its containing terminal’s size.

| Output | Multiplier | 12pt baseline | 19pt baseline |
| --- | ---: | ---: | ---: |
| DP-2, main | 1 | 12pt | 19pt |
| DVI-D-0, left | 0.743322 | 8.92pt | 14.12pt |
| HDMI-0, right | 0.595238 | 7.14pt | 11.31pt |

Global Xft.dpi remains135. Ratios use vertical pixels per reported physical
millimetre, relative to DP-2; visual calibration remains necessary. Kitty rounds
sizes to supported precision. Side targets have a 4pt floor.

The watcher subscribes to i3 workspace/window/output/shutdown events and checks
every two seconds for zoom and delayed sockets. A no-UI kitten maps X11 IDs to
Kitty OS-window IDs, reads actual font metrics and keeps baseline/last-applied
state inside each Kitty process. There are no baseline files or stale PID keys.
Watcher/i3 restarts cannot double-scale windows. New terminals capture their
actual font size, including launch overrides, even on side monitors. Panes and
tabs in one OS window share a font size. No titles or shell content are saved.

Existing Ctrl+Alt+Up/Down still change all OS windows within that Kitty instance.
The next scan interprets changed metrics as manual zoom on the last observed
output. Separate Kitty instances stay independent. Simultaneous zoom and move
is attributed to that previous output. Unknown outputs, scratchpad windows and
unreachable sockets are skipped and retried. Remote control remains socket-only;
the watcher explicitly addresses owned `/tmp/kitty` and `/tmp/kitty-*` sockets.

## Operation

Normal `refresh-config` deploys managed helper, adapter and service targets.
Migration-preserved live i3 configs require merging only the new autostart line;
never replace their unrelated settings with the public template. On this machine
refresh stopped on unrelated audio-mute divergence; this task used scoped
deployment and an additive live i3 merge. Reload the user service manager before
initially reloading i3. The i3 autostart entry imports
DISPLAY/XAUTHORITY/I3SOCK and restarts `kitty-monitor-font.service` on login/reload.
It runs `~/scripts/kitty-monitor-font watch` with minute-by-minute heartbeats.
No new dependency or Kitty configuration reload is needed.

Working directory: `/home/kevin/linux-config`; no sudo. Read-only live metrics:

python3 scripts/executable_kitty-monitor-font status

Modes: `status` reads metrics, `once` reconciles once, `watch` follows i3, and
`restore` stops the service, restores known baselines and clears tracking.
`--plain` gives ASCII messages; `--json` emits one-shot machine-readable results.
Unavailable sockets are counted and make one-shot commands return nonzero.

Run the disposable runtime check without changing existing terminals:

python3 scripts/executable_kitty-monitor-font-smoke --plain

It uses installed Kitty/Xvfb on an isolated display to check both baselines,
side ratios, repeated returns, restart, zoom, restore and unfocused isolation.
Output assignments are simulated through the actual adapter; this does not prove
physical appearance or live i3 move delivery. `--details` shows raw diagnostics.
Child processes are cleaned up even on failure. Rerun this after Kitty upgrades:
the adapter uses version-sensitive internal APIs.

## Acceptance and rollback

Follow [the grouped smoke checks](smoke-tests.md#kitty-monitor-font-sizing).
Move 12pt/19pt windows and whole workspaces to both sides and back repeatedly;
confirm physical height, exact main-size recovery and independent instances.
Zoom on a side, return to main, launch new side terminals and restart the service
while scaled. Inspect live metrics after each action.

Rollback: remove the i3 autostart entry and refresh/reload i3, then restore while
Kitty processes remain alive:

python3 scripts/executable_kitty-monitor-font restore

This stops the service. Leave it stopped until scaling is wanted again. No DPI,
launcher or remote-control-policy rollback is necessary.

## Maintenance handoff

Atomic plan and verification: [kitty-monitor-font-sizing.md](../plans/kitty-monitor-font-sizing.md).
Automated: `python3 -B tests/test_kitty_monitor_font.py`; regressions:
`python3 -B tests/test_kitty_tmux_copy.py` and `bash tests/test_desktop_display_layout.sh`.
Suggested commit: `feat(kitty): scale terminal fonts by i3 output`.

Paste-ready Cursor prompt:

```text
Read plans/kitty-monitor-font-sizing.md and docs/kitty-monitor-font-sizing.md.
Maintain actual per-OS-window baselines; never infer sizes from focus or12pt.
Run defining tests and isolated runtime smoke. Verify real i3 moves separately
from simulated assignments. Preserve DPI135, launcher19pt, socket-only control
and unrelated working-tree edits. Keep matching docs and plan in the same commit.
```

Primary evidence: [font implementation](https://github.com/kovidgoyal/kitty/blob/v0.49.2/kitty/boss.py#L1572),
[no-UI kitten responses](https://github.com/kovidgoyal/kitty/blob/v0.49.2/kitty/rc/kitten.py),
[global X11 DPI](https://github.com/kovidgoyal/kitty/blob/v0.49.2/glfw/x11_init.c#L516).
The proposed matched action changed a different OS window in an isolated fixture;
the adapter instead supplies explicit OS-window IDs to `_change_font_size`.
See [the runtime report](postmortem/2026-10-22-kitty-monitor-probe-access.md).
