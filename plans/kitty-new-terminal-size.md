# Readable new terminal size

Make new Kitty terminals use the same 19pt main-display baseline as the user's
left reference terminal. Keep existing monitor ratios and zoom behavior; validate
on an isolated display and deploy without reloading i3 or moving user windows.

## Context, scope and decisions

User supplied screenshots of small new tmux terminals and two readable targets.
Read-only live metrics identify the earlier “Fix consumption hour totals” reference
as baseline19pt/current14.123pt on DVI-D-0. The current conversation terminal has
the same metrics. Default launches use12pt; Ctrl+Return already overrides19pt.
Set the Kitty default to19pt: DP-2=19, left=14.123, right=11.310. tmux inherits
the containing OS window's font; no tmux or i3 change is needed.

Protected initial state: extensive existing dirty work including Kitty shortcut
mappings, i3 config, monitor-font helper/adapter/tests/docs, README, smoke tests,
plans and postmortem knowledge. Preserve every unrelated hunk. No commit requested.

## Checklist

- [x] Inspect launch chain, live metrics, references, lessons and durable feedback.
- [x] Reproduce the12pt default using real Kitty on an isolated display.
- [x] Change only default font_size; update current docs and smoke checks.
- [x] Run required refresh; preserve conflicts and deploy scoped config if needed.
- [x] Verify isolated launch and monitor scaling, source/live identity and review.

## Verification

Use an isolated Xvfb/Kitty fixture with the real config and actual font metrics.
Before change expect19pt and observe12pt (intentional RED). After change expect
19pt, then apply existing adapter mappings and observe14.123/11.310/19pt. Close
only fixtures. Run existing monitor-font regression and isolated runtime smoke.
No desktop moves, i3 reloads or unsolicited size changes to existing windows.

## Risks and rollback

New windows show fewer columns/rows. Physical preference needs user acceptance.
Kitty reload must preserve current sizes; avoid broadcasting a font reset. Restore
font_size12 and apply only Kitty config to roll back new-terminal behavior.

## Progress and review

Lookup `terminal font size tmux monitor 4k` found existing explicit OS-window API
runtime guidance; applicable adapter already in use, no new adapter fix needed.
Atomic implementation: default19, verify actual launch/scaling, scoped deploy.
Suggested commit: `fix(kitty): use readable font size for new terminals`.
Cursor prompt: Read this plan; preserve existing monitor ratios, zoom mappings,
and unrelated dirty changes. Verify new19pt launches on isolated Xvfb, then
14.123pt left/11.310pt right and19pt return. Never move desktop windows or reload i3.


## Final evidence

`python3 /tmp/kitty-default-font-check.py`: intentional RED observed12pt against
19pt expectation (exit1); after change GREEN observed19,14.12311266,11.30952381,
19pt across default/left/right/main (exit0). All fixtures terminated.
`python3 -B tests/test_kitty_monitor_font.py`:10 tests pass;
`python3 -B tests/test_kitty_tmux_copy.py`:8 tests pass.
`python3 scripts/executable_kitty-monitor-font-smoke --plain`: isolated runtime
PASS for12/19pt, zoom, restore and cross-window/instance isolation (exit0).
Required refresh exited1 on the pre-existing monitor_font.py conflict; Kitty
config was applied before that stop. Scoped chezmoi apply and byte comparison
exited0. No current terminal size reset, i3 reload or workspace move occurred.
Docs: README, monitor-font usage and grouped smoke checks updated. New tmux
windows inside an old Kitty keep that OS window's current font; zoom that window
or open a new terminal to use the new default. Physical acceptance remains
manual. No commit/push requested or performed. Rollback remains font_size12.

Direct verification (any working directory, no sudo): launch `kitty`, inspect
`~/scripts/kitty-monitor-font status`, and run
`~/scripts/kitty-monitor-font-smoke --plain`. New-terminal baseline should be19;
check current output target visually without moving existing workspaces.
