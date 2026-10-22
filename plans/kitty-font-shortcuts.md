# Kitty font shortcuts

Add convenient one-point font zoom keys, preserve existing monitor sizing, and
apply the configuration after checking the shortcuts in a disposable terminal.

## Scope and decisions

Use Kitty's native `change_font_size current` action for Ctrl+Shift+Up/Down,
Ctrl+Plus (including Ctrl+=) and Ctrl+Minus. Existing Ctrl+Alt keys retain their
all-window semantics. No font defaults, monitor ratios or dependencies change.
The live/source i3 Ctrl+Shift+Plus gaps binding intercepts Ctrl+Plus; the user
approved moving it to Ctrl+Super+Plus. Source/live Kitty contents initially
match despite the newer deployed timestamp.

Relevant files: Kitty config; i3 gaps binding only if approved; README and smoke
checklist. Initial status has extensive unrelated dirty work, including untracked
monitor-font implementation/docs and dirty i3/README/smoke files. Preserve it.

## Checklist

- [x] Inspect bindings, live/source state, preferences and relevant lessons.
- [x] Resolve gaps conflict and add only native zoom mappings.
- [x] Run required refresh, deploy scoped changes if an unrelated conflict blocks it.
- [x] Verify actual key delivery/font metrics and reload affected running apps.
- [x] Update docs, evidence and final review.

## Verification and risks

Trivial declarative mappings need no new unit tests. Use disposable Kitty/Xvfb
with actual xdotool keypresses and font metrics for up/down, plus/minus and equals;
confirm another OS window is unchanged. Validate/reload live i3 if its binding
changes; preserve unrelated live contents. Keep existing all-window zoom bindings.
Manual: focus Kitty, press each increase/decrease pair and observe one-point
changes; allow the monitor watcher to reconcile, then verify zoom persists.
Rollback: remove the new mappings, restore the old gaps binding if moved,
refresh and reload Kitty/i3. Commit/push is now authorized by `commit-session`.

## Progress and handoff

Native mappings added; user-approved gaps relocation added. Suggested commit:
`feat(kitty): add convenient font zoom shortcuts`.
Cursor prompt: Read this plan and the affected config/docs; keep zoom scoped to
the current OS window, preserve monitor baselines and unrelated dirty edits,
verify real keypresses, and refresh/reload the deployed configuration.

Final evidence: `python3 /tmp/kitty-font-verify.py` exited0 after fixture repairs;
Kitty parsed with `bad_lines=[]`. Real Ctrl+Shift+Up/Down, Ctrl+=, Ctrl+Shift+=
and Ctrl+- changed focused size by exactly1pt; another OS window stayed12pt.
Owned Xvfb/Kitty processes terminated. Installed/source Kitty config bytes match.
Scoped `chezmoi apply ... ~/.config/kitty/kitty.conf` exited0. All16 owned live
Kitty instances reloaded with current font sizes preserved. i3 config validation
exited0 (pre-existing wheel-command warnings), reload returned success, and raw
IPC confirmed the live replacement binding and absence of the old grab.
Real Ctrl+Super+Shift+Plus and Ctrl+Super+Shift+= both emitted the correct i3
binding event, command `gaps inner all set 20;gaps outer all set 0`; Ctrl+Shift+0
restored the original zero gaps. A workspace-only gap-value assertion was not a
reliable observation of the action; event evidence verifies the modifier routing.

Required normal `fish -c refresh-config` was attempted after both config changes,
but exited1 on unrelated live `.config/kitty/monitor_font.py` divergence (private
log `/tmp/refresh-config.wrOgtkKi.log`). Preserve that helper. Live i3 is
migration-preserved, so only its approved gaps line was merged; no full overwrite.
Inspection/fixture failures and their corrections are recorded in
`docs/postmortem/2026-10-22-kitty-shortcut-inspection.md`. README and grouped smoke
checks document the final keys. Initial implementation did not commit/push; manual physical
font sizing and monitor moves remain the existing monitor task's acceptance.

## Delivery milestone: convenient font zoom shortcuts

Commit subject: `feat(kitty): add convenient font zoom shortcuts`.
Scope attribution uses observed writes and the captured pre-write dirty baseline;
the helper could not see wrapped tool calls (`unsafe`: no detected writes).
Include only this task's Kitty mappings, i3 gaps relocation, README text,
standalone smoke section, plan, inspection report and that report's ledger entry.
Leave pre-existing monitor-font work and every other task's edits unstaged.

Fresh pre-commit evidence: isolated Xvfb/Kitty key fixture again passed5/5 with
`bad_lines=[]`, unchanged second window and cleanup, exit0. README gate returned
`pass_no_change`. Avoid further active-desktop probes/reloads per current durable
feedback. Existing full-refresh conflict is unchanged and does not block the
already applied shortcuts. This milestone's delivery sequence checks the exact
candidate with the privacy gate, commits it, and pushes configured `origin/main`;
the observed commit hash and push result are reported in Codex output. No source
configuration changes were needed during this commit workflow.
