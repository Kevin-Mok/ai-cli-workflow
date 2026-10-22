# Monitor-aware Kitty font sizing

Preserve each terminal's preferred main-monitor size while automatically scaling
its text on the two lower-density monitors. Implement a small i3 watcher, verify
baseline recovery, and activate it without changing global DPI or launchers.

## Context and decisions

- Kitty 0.49.2, socket-only remote control, 12pt default and 19pt launcher.
- Live scoped checks confirm DP-2 2160/400mm, DVI-D-0 1152/287mm,
  HDMI-0 1080/336mm and global Xft.dpi 135.
- Ratios: DP-2 1; DVI-D-0 (1152/287)/(2160/400); HDMI-0
  (1080/336)/(2160/400). Dimensions remain estimates pending visual acceptance.
- `ls` exposes platform IDs but no live font size. Use a no-UI custom kitten
  to read `os_window_font_size` and apply absolute OS-window sizes via Kitty's
  own `_change_font_size` implementation. This is a version-sensitive internal
  API, also used by the proposed targeted action, and avoids focus changes.
- Baseline/last-applied state lives on the Kitty boss, keyed by OS window ID;
  it survives watcher restart without disk state or stale PID reuse. New windows
  capture their actual current size, including launch overrides. Manual zoom is
  interpreted relative to the last applied multiplier. Existing all-window zoom
  keys remain unchanged, including their broadcast semantics within an instance.
- No new dependencies. A user systemd service supervises the watcher; i3 starts
  it on login/reload. Subscribe to i3 events and reconcile periodically for zoom,
  delayed sockets and reconnects. Unknown outputs are skipped conservatively.

## Scope and protected work

New watcher, Kitty adapter, systemd unit, defining regression/runtime checks,
i3 autostart entry, README addition and grouped smoke checks. No global DPI,
display placement, launcher-size or remote-control-policy changes.
Initial git status contained unrelated README/smoke docs, notification code/tests,
postmortem knowledge, plans and prompts. Preserve all pre-existing edits; no
commit requested. Use this existing checkout.

## Checklist

- [x] Read relevant sources, preferences, lessons and live geometry.
- [x] Write defining tests; observe RED before implementation.
- [x] Implement adapter and watcher; verify GREEN and regression checks.
- [x] Document usage, acceptance, limitations, rollback and Cursor handoff.
- [x] Attempt refresh; deploy owned targets, validate/reload i3 and inspect status.
- [x] Independent final review; record final evidence and outstanding checks.

## Verification

Automated: `python3 -B tests/test_kitty_monitor_font.py`; existing desktop-layout
and Kitty-copy checks. Cover mixed baselines, both sides, repeated round trips,
zoom, restarts, unknown outputs, closed windows, missing sockets and unfocused
targets. Runtime: no-UI adapter in disposable Kitty instances; inspect actual
font metrics and targeted action support. Live status before/after activation;
do not move or close existing user terminals for testing.
Physical acceptance: manually move 12pt and 19pt terminals/workspaces to each
side and back repeatedly; inspect equal physical letter height and preserve
manual zoom. This requires the user's visual judgment.

## Risks and rollback

Internal Kitty API may change with upgrades; fail visibly rather than guess a
baseline. A zoom exactly concurrent with a move is interpreted on the previously
observed monitor. State dies with Kitty (correct for new processes); disabling
requires stopping the service then restoring baselines while Kitty remains alive.
Rollback: stop/disable the user service, run the helper's restore command, remove
i3 startup entry and refresh/reload. Unknown output windows retain their current
size until moved to a recognized output. No monitor calibration is user-accepted.

## Evidence and review

Initial sandbox xrandr/xrdb probes failed to access X11; scoped host probes passed.
Postmortem lookup `X11 sandbox display` matched existing sandbox access guidance;
applicable restriction, not a display configuration defect. Guessed installed
source paths were absent; primary tagged Kitty source supplies API evidence.
RED: `python3 -B tests/test_kitty_monitor_font.py` exited1 before adapter existed.
GREEN: defining suite10/10; Kitty-copy regression8/8; desktop-layout shell check
exit0. Unit IPC uses fragmented fake bytes after sandbox socketpair restriction.

Runtime: `python3 scripts/executable_kitty-monitor-font-smoke --plain` exited0:
real12/19pt Kitty metrics through both ratios, three round trips, restart,
targeted zoom, restore, unfocused OS-window and cross-instance independence.
The proposed matched action changed the other OS window in a multi-window
fixture; explicit OS-window sizing avoids that verified failure. No focus-based
font action is used by production.

Activation: required `fish -c refresh-config` exited1 on unrelated live
`scripts/audio-mute` divergence. i3 config is migration-preserved and contains
unrelated live bindings and local paths; do not force apply/adopt it. Deployed
only new helper/smoke/adapter/unit and merged one autostart line into live i3.
`i3 -C -c ~/.config/i3/config` exited0 (existing wheel-command deprecations),
`i3-msg reload` returned success, installed systemd unit verification exited0.
Service active; live status showed15 reachable windows, zero unavailable
sockets, baselines12/19 and expected side metrics8.920/14.123 and7.143/11.310pt.
Actual service restart preserved every existing metric.

Live move fixture `/tmp/kitty-monitor-live-check.py` exited0 after correcting
socket discovery to use its unique prefix rather than launcher PID. Temporary
unfocused12pt and19pt windows followed both side outputs and repeated DP-2
returns with exact baselines. Only fixture windows moved; cleanup restored focus.
Whole-workspace moves also passed in `/tmp/kitty-monitor-workspace-check.py`:
dedicated fixture workspace followed XID-matched moves through both sides and
back to main; all original visible workspaces and focus were restored. Fixture
corrections included a non-reserved workspace name, XID readiness, explicit
criteria rather than desktop focus, and partial status tolerance for unrelated
closing sockets. Physical letter-height acceptance remains manual.

Final review: independent agent found no important bugs. Deferred minors:
runtime creation of a second OS window while its parent is scaled (source shows
adapter leaves global font baseline unchanged); cosmetic number spacing in docs.
The plan-evidence update requested by review is complete. No commit/push was
requested or performed. Rollback restores baseline while Kitty remains running.
Ruling: use explicit OS-window API instead of proposed matched action because
the latter failed isolation; cost is version-sensitive Kitty API maintenance.
Ruling: scoped deployment instead of forcing refresh; cost is the unrelated
audio-mute conflict remaining unresolved.

Final installed smoke command exited0 again; service status showed active
(running), and live helper status reported zero unavailable sockets. README
gate returned `pass_no_change`; `git diff --check` passed. Postmortem learning
was updated in tracked knowledge and its targeted hash/contract check passed.
The final global diff check later saw a concurrent blank-line-at-EOF warning in
the pre-existing dirty operational-drift.md reference. Leave that unrelated edit
intact; scoped whitespace verification covers this task's files.

## User-reported desktop disruption

The user found live validation disorienting and reported a missing middle bar.
Do not repeat active-desktop window/workspace tests or reload i3 to investigate.
Watcher runtime never reloads i3; manual activation/test steps were disruptive.
Read-only follow-up reports three dock-mode bar windows; screenshot root cause
is unresolved. See the [incident](../docs/postmortem/2026-10-22-i3-disruptive-validation.md).
