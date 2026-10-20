# Simplify Redshift shortcuts

Use Left Super (normally keycode 133, Mod4) plus number-row keys for existing Redshift presets. Move workspace 11 to Super+F11 and preserve Alt+digits.

## Context and decisions

Implement the approved conversation plan in the existing checkout. Scope: i3 bindings, existing shortcut checker, README, smoke checklist and this plan. Notifications and Ctrl+Alt adjustments remain unchanged. User subsequently selected the concurrent new temperature scale: 1200, 1800, 2100, 2350, 2700, 3100, 3700, 4600, 6000 K. No commit or push requested. The checker found an additional Godot conflict on Super+5; the user explicitly chose to remove that shortcut. Initial git status captured; all pre-existing dirty memory files, reports, plans and prompts are protected.

## Checklist

- [x] Inspect source, docs, helper and installed config; capture baseline status.
- [x] Observe RED using updated defining checker before implementation.
- [x] Change bindings and matching README/smoke documentation.
- [x] Validate rendered config, complete required refresh, and activate scoped desktop bindings.
- [x] Record final evidence and review.

## Risks and rollback

Installed config is newer and differs in unrelated local bindings, voice toggle, service placement and private machine paths. Do not overwrite it wholesale with the public template. Preserve its unrelated bytes. Refresh may stop on existing managed-file conflicts; diagnose before retry. Restore only the changed bindings to roll back. Live X11/IPC may require scoped escalation. Physical key comfort and visible warmth require a human check.

## Verification

Run python3 scripts/smoke_redshift_keys.py before and after the binding edit; then render with chezmoi execute-template and validate via i3 -C -c. After safe activation, check installed and live configs with the same helper. Manual: Super+1/3/9 select 1800/2850/6000 K; Super+0 selects 6500 K; Super+grave resets; Alt+digits still switch workspaces; Super+F11 selects workspace 11. Reuse docs/smoke-tests.md. Run git diff --check.

## Progress and review

RED observed: updated checker exited 1, finding no Super-only presets before implementation. Bindings and matching docs updated. Prior display probe could not connect to :1 inside sandbox; existing screensaver postmortem establishes scoped escalation as a workaround, not a repaired display. Lookup: X11 display sandbox refresh-config; applicable execution-environment guidance only. Existing repo config uses sanitized example paths; retain private live paths outside tracked files.

### Validation and concurrency checkpoint

Source checker and rendering passed after user-authorized Godot shortcut removal; rendered i3 validation exited 0 with existing wheel_up_cmd/wheel_down_cmd deprecation diagnostics. refresh-config exited 0 but i3 is intentionally unmanaged via local migration preservation. Read-only live probes confirmed keycode 133=Super_L and running/installed config equality. Scoped candidate validation then stopped before installation: another edit changed only the checker's expected temperature scale (keys 4/6/7/8) during this task. User confirmed the new scale; preserve and integrate that edit. This checkpoint was resolved by the subsequent user confirmation and scoped activation below.

## Final verification and handoff

- Source smoke: exit 0 for confirmed new scale and preserved workspace shortcuts.
- python3 tests/test_redshift_control.py: 6 tests passed, exit 0.
- Rendered i3 validation and private live candidate validation: exit 0 with pre-existing wheel_up_cmd/wheel_down_cmd deprecation diagnostics.
- refresh-config completed successfully; i3 remains intentionally excluded from chezmoi management. Final refresh also completed successfully.
- Scoped live patch preserved all unrelated local config bytes, changing only approved bindings, comment and four confirmed temperature values. i3-msg reload returned success:true. Installed and --live checker: exit 0.
- Actual X11 injected keypresses: Super+4 saved 2350 K without changing workspace; Super+0 saved 6500 K; Super+F11 focused workspace 11; Alt+1 focused workspace 1. Starting temperature/workspace restored. Each assertion passed.
- git diff --check: exit 0. Independent review found no correctness issue; reviewer IPC is sandbox-limited, while main live checks passed with scoped access.

No commit or push requested or performed. Suggested commit: feat(i3): simplify Redshift preset shortcuts. Rollback: restore only the scoped bindings and four temperature values in source/live config, validate and reload; private pre-activation backup exists in /tmp for this session. Subjective warmth/ergonomics remain a user check. Existing wheel deprecations are outside scope.

Cursor continuation prompt: Read plans/simplify-redshift-shortcuts.md, preserve unrelated dirty work and intentionally unmanaged private i3 settings, verify the confirmed Super preset scale and source/installed/live checkers, and make no extra shortcut changes without user direction.

### Compatibility coordination

A separate active smoother-curve task added Alt+Super aliases and corresponding shared checker requirements after this task's successful scoped activation. Preserve those changes; the new Super shortcuts remain the requested primary bindings. Combined source checker passes. Wait for that task's live activation, then rerun the combined installed/live checks. No additional live write is needed from this task.

Coordination resolved: the parallel task activated the compatibility aliases. Fresh combined installed and running checkers passed after its reload. Both modifier families now share the confirmed curve; single-modifier Super+digits, relocated workspace 11 and removed Godot shortcut are verified. No remaining implementation blocker.

Latest range follow-up supersedes historical temperature values above: see plans/smooth-redshift-curve.md for current 1800–6000 K over all nine keys. Active manual verification values are updated; earlier recorded runtime outcomes remain historical evidence.

Current delivery and final ten-key preset scope are recorded in plans/even-redshift-presets.md; earlier temperatures above are historical.
