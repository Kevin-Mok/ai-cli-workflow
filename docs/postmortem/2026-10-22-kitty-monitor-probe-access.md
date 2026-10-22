# Kitty monitor probe access

Read-only desktop probes need scoped host access in this sandbox. Use installed
Kitty help and tagged primary source rather than guessing installed source paths.

- Symptom: xrandr could not open display :1; xrdb reported operation not permitted.
  Guessed Kitty source paths and a refresh-script glob were absent.
- Impact: initial diagnosis commands returned nonzero; no settings changed.
- Lookup: `X11 sandbox display` found existing sandbox/Kitty socket guidance;
  applicable to access, not evidence of a broken desktop.
- Root cause: sandbox access boundary and incorrect discovery assumptions.
- Resolution: scoped host xrandr/xrdb/i3/Kitty listing succeeded, confirming
  three monitors, DPI 135 and platform IDs. Use tagged primary API source.
- Verification: host probe exited 0 on 2026-10-22. No sandbox repair claimed.
- Status: verified workaround. Next: implement and verify sizing separately.
- Learning: no new reusable finding; existing scoped desktop-access guidance
  already describes this boundary. Register this report's reviewed hash.

## Isolated fixture follow-up

Real 12pt/19pt fixtures passed side scaling, repeated round trips, restart,
targeted zoom and restore. The final two-OS-window isolation assertion failed;
the initial wrapper suppressed assertion detail. All disposable processes were
cleaned up. No existing terminal was changed.

Lookup `Kitty targeted action font focus` returned adjacent terminal guidance,
but no fix for this exact dispatch issue. Detailed before/after metrics show
`action --match id:1 change_font_size current 17` left OS window1 at13.68 and
changed OS window2 from12 to17 on Kitty0.49.2. This disproves the proposed
action's unfocused-window safety in this runtime. The production adapter already
uses explicit OS-window IDs with `_change_font_size`, avoiding that path.
Change the acceptance check to exercise the delivered adapter, retain the
observed action limitation here, and verify exact OS-window isolation.
Status: adapter verification pending; source routing root cause not established.

The revised isolated adapter check passed (exit0), including two OS windows and
two independent instances. Production uses explicit OS-window IDs; it does not
depend on the failed action path. A unit test hit the same sandbox boundary on
socketpair.sendall; use a fragmented-byte fake for pure protocol tests while real
sockets remain covered by the isolated graphical smoke. A documentation patch
also rejected stale README context changed by concurrent work; reread current
context and preserve that work. No new sandbox remedy is implied.

## Activation follow-up

Required `fish -c refresh-config` stopped with exit1 and reported a private
conflict log. No force apply was attempted. Rendered repository i3 config differs
from live in unrelated preserved bindings and sanitized machine-local paths;
replacing the live file would lose user settings. Inspect the conflict and
deploy only this task's adapter, helper, unit and additive i3 startup entry.
Status: activation pending; retain unrelated live settings.

Targeted deployment passed; live service scaled all15 reachable windows and
reported zero unavailable sockets. Live service restart preserved every existing
metric. The first desktop-move fixture assumed Kitty's socket PID equalled its
launcher PID and timed out discovering it; discover the fixture's unique socket
prefix instead. Existing user windows were not moved and original focus was
restored in finally. Unit-file verification also requires scoped service-bus
access here. These are probe restrictions, not passing move evidence.

The corrected desktop fixture passed: both12pt and19pt unfocused windows moved
through DP-2, both sides and repeated returns with exact baseline retention.
Only fixture windows moved; both were closed and original focus restored.
Installed unit verification exited0, and service restart preserved all existing
font metrics. Activation is verified; global refresh remains blocked by unrelated
audio-mute divergence. Physical letter-height acceptance remains manual.

A whole-workspace fixture sent its first i3 move before i3 had registered the
new X11 window (Kitty's socket was ready first), so criteria returned no match.
Its finally block restored visible workspaces/focus and closed the fixture.
Wait for the XID in get_tree before issuing movement; production already retries
unmapped/new windows on its periodic reconciliation. This is a fixture readiness
race, not evidence of a watcher failure.

Waiting for the XID did not resolve the command rejection, disproving readiness
as the cause of that first move failure. The fixture also used a reserved
double-underscore workspace name. Retry with an ordinary unique name; retain
the readiness guard independently. The watcher itself never creates workspaces.

The ordinary-name fixture moved successfully but its next expected output check
timed out with the fixture still mapped to DVI-D-0. Current monitor sizing was
correct for that actual output. Workspace/focus cleanup ran. Investigate exact
i3 move semantics before another global workspace command; do not treat this as
watcher failure or continue moving potentially unrelated workspaces.

Primary i3 commands.c confirms XID criteria also apply to whole-workspace moves.
Use `[id=<fixture>] move workspace to output ...` rather than relying on desktop
focus. Another attempt stopped before creating fixtures because an unrelated
socket disappeared during status; the next scan had zero unavailable sockets,
and a direct connection inventory found no abandoned fixture sockets. Permit
partial status results in the fixture while still asserting its own metrics.

Final XID-targeted workspace fixture exited0: dedicated workspace moved through
both sides and returned to the main baseline, then fixture cleanup restored all
original visible workspaces and focus. The delivered isolated smoke passed
again, service remained active, and live status reported zero unavailable
sockets. Whole-workspace delivery is now verified; physical calibration alone
remains manual. No commit/push was requested or performed.

Final global diff validation encountered a concurrent unrelated EOF blank-line
warning in the already-dirty operational-drift.md reference. Preserve that work
and run a scoped diff check for this task instead; no production impact.
