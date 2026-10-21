# Match Notis color and mouse actions

Make the notification indicator match the volume/date theme color, then give each mouse button a fixed notification state.

## Context and scope

The DND helper currently inherits #cbe4ff, while volume and calendar use wallpaper `color7` (#d0bce2 currently). Change only the helper, its focused test, README and existing smoke check. Preserve all pre-existing dirty work captured with git status --short, including previous-turn DND edits.

## Decisions

Use the existing ~/.cache/wal/colors.sh color7 like neighboring blocks, with the bar default as fallback if unavailable. Left button sets paused false; right button sets paused true. Keep paused red/queue count and other buttons unchanged.

## Implementation

- [x] Confirm surrounding block colors and requested click semantics.
- [x] Observe defining test RED, update helper and documentation, then verify GREEN.
- [x] Run refresh-config, verify deployed helper and record final evidence.

## Risks and rollback

Missing wallpaper colors must not hide the indicator. Repeated clicks must be idempotent. Preserve live pause state during verification. Rollback only task hunks, never unrelated work. Commit/push authorized by commit-session.

## Verification

Run python3 tests/test_i3blocks_dnd.py and bash -n dot_config/i3blocks/scripts/executable_dnd. Run fish -c refresh-config with required home access, compare deployed/source bytes, and inspect live read-only output. Manual: right-click shows red DND, repeat stays DND; left-click shows Notis matching volume/date, repeat stays enabled.

## Evidence and review

RED caught the expected color and left/right click mismatches. Refresh exited 0, deployed/source bytes match; installed output uses #d0bce2. Live right/right/left/left returned true/true/false/false; original pause state restored. Focused GREEN results recorded below. Visual evidence: user screenshot shows the blue Notis label beside lavender volume/date; neighboring scripts explicitly select color7.

Final checks: bash -n passed; python3 -m unittest tests/test_i3blocks_dnd.py passed 6 tests including both palette fallback cases. git diff --check passed. README and smoke checks updated. Manual screenshot comparison remains outstanding.

## Delivery milestone

Commit subject: `fix(i3blocks): match Notis theme and mouse actions`. Implementation and deployment verified; focused tests, Bash syntax and README gate pass. Session-only hunks will be committed together with this plan; unrelated dirty files remain excluded. Next step: privacy gate, commit and push origin/main. No blockers. Scope helper could not detect nested tool writes; use directly observed session writes and the captured initial dirty baseline.

Privacy review caught machine-specific report aliases; replaced only the two session aliases with the established /home/example public placeholder before retrying the gate.

## Queue smoke-check milestone

The implementation milestone was committed as 1e9e4c9 and pushed to origin/main.
Follow-up live verification queued two distinct notifications: dunstctl reported
2 waiting and the installed helper emitted red DND (2). DND remained enabled for
the user to exercise recovery; delivery of both popups was not observed by the
agent. Added the repeatable queue/resume check to docs/smoke-tests.md.

Commit subject: `docs(i3blocks): capture two-notification queue check`.
Scope is only this smoke-check entry and matching plan update, using directly
observed writes because the scope helper cannot detect nested tool writes.
README gate passes; no executable behavior changed. Other dirty work remains
excluded. Next step: inspect staged docs, run privacy gate, commit and push.
