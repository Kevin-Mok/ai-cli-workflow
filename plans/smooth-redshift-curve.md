# Smooth Redshift preset curve

Make Super+1–9 progress smoothly from 1800 to 6000 K with reciprocal-temperature spacing, updating both modifier families and activating the scoped live presets.

## Context and decisions

Latest confirmed range: rounded reciprocal-temperature spacing of 1800, 1950, 2200, 2450, 2750, 3200, 3800, 4650, 6000 K over keys 1–9. Earlier evidence below records the preceding 3–9 range. User explicitly requested both Super and Alt+Super modifiers. Preserve reset and adjustment values. Move workspace 11 to Super+F11 and remove conflicting Godot binding as in existing source. No controller changes or commit requested. Preserve pre-existing edits in README, smoke docs, config and checker, plus all unrelated dirty files captured in initial git status. i3 is intentionally unmanaged by chezmoi; preserve private live config and change only preset lines after refresh.

## Checklist

- [x] Inspect current presets, docs, prior plan and protected dirty state.
- [x] Update defining checker and observe RED before config changes.
- [x] Update presets, README and existing smoke expectations.
- [x] Run focused regression checks and refresh-config.
- [x] Resolve live modifier mismatch, validate and reload scoped live config.
- [x] Record evidence and remaining limitations.

## Risks and rollback

Perceived smoothness varies by display and needs a human check. Restore only the old preset values to roll back. Preserve unrelated source and installed settings. No temporal fade is introduced.

## Verification

Run python3 scripts/smoke_redshift_keys.py before/after; python3 -m unittest discover -s tests -p test_redshift_control.py; validate installed config via i3 -C -c ~/.config/i3/config and run checker against installed and running i3. Manual: press Super+3 through Super+9; observe notifications and warmth. Confirm reset, workspace and adjustment keys using docs/smoke-tests.md. Run git diff --check.

## Evidence and review

RED: python3 scripts/smoke_redshift_keys.py exited 1 as expected with old values at keys 4/6/7/8. Prior activation report establishes unmanaged i3 config and sandbox desktop limits; use scoped desktop access when needed. No visual-comfort claim until human inspection.

GREEN: source checker passed; python3 -m unittest discover -s tests -p test_redshift_control.py passed all 6 tests; git diff --check passed. fish -c refresh-config exited 0 with REFRESH COMPLETE. Live bindings are still Alt+Super, while source is Super-only. Asked user which modifier to activate; no live config mutation until clarified. Inspection-path postmortem registered with explicit existing-learning decision; targeted memory check passed with no errors.

Modifier decision resolved: user requested both. Second intentional RED exited 1 for missing Alt+Super+1. Added equivalent Alt+Super preset/reset aliases.

## Final evidence and handoff

Both modifier families are active. Final source checker and all 6 controller tests passed; diff check passed. Second refresh-config exited 0 with REFRESH COMPLETE. Installed config changed to Super-only during refresh; first scoped activation guard stopped before any write. Re-inspected current config, then added both binding families. Candidate i3 -C exited 0 with existing wheel_up_cmd/wheel_down_cmd deprecation diagnostics. i3-msg reload returned success; live checker passed both modifier families and unchanged adjustments/workspaces. Backup: /tmp/redshift-curve-backup-g0tl727v/config. No commit or push requested.

Manual test: press Super+3–9, repeat with Alt+Super+3–9, verify 2100/2350/2700/3100/3700/4600/6000 K notifications and subjective smoothness; use either modifier with 0/grave to reset. Automated: python3 scripts/smoke_redshift_keys.py; python3 -m unittest discover -s tests -p test_redshift_control.py. README and existing smoke checklist updated. Subjective display comfort remains untested.

Cursor handoff prompt: Verify the two Redshift modifier families in source, installed and live i3 against plans/smooth-redshift-curve.md; preserve all unrelated dirty changes and do not commit unless requested.

Suggested commit: feat(i3): smooth Redshift presets across both shortcuts

## Session delivery milestone

Commit subject: feat(i3): smooth Redshift presets across both shortcuts. User requested commit-session after runtime verification. Scope helper could not detect writes or baseline; use the explicit initial status and successful writes recorded in this conversation. Both modifier families and their required collision removal/workspace relocation were explicitly authorized in this session. Include only this session’s curve, aliases, tests/docs, plan and inspection report registration. Preserve the newer all-nine-key follow-up and unrelated existing staged/unstaged work using an isolated index. README recruiter gate passed. No pending implementation blockers; next step is scoped commit and one upstream push to origin/main after exact-candidate checks.

Exact candidate verification: isolated source checker passed; controller regression re-run from repository root passed all 6 tests. Root README gate passed. Privacy check is required immediately before commit; preserve all hooks. Candidate contains only this session’s original 2100–6000 K range; newer follow-up remains uncommitted.

## Follow-up: spread 1800–6000 K across all nine keys

Latest user request supersedes the earlier 3–9 range. Use reciprocal-temperature spacing between 1800 and 6000 K over eight intervals, rounding to the nearest 50 K: 1800, 1950, 2200, 2450, 2750, 3200, 3800, 4650, 6000 K. Preserve both modifier families, reset, adjustments and workspaces. Initial dirty status captured; preserve all previous task work. Update existing checker first, then source/docs; refresh and apply only preset values to intentionally unmanaged live config.

- [x] Inspect current source, docs, helper and prior evidence.
- [x] Observe defining checker RED with new expectations.
- [x] Update all nine presets and matching README/smoke checks.
- [x] Run regressions, refresh, validate and activate live presets.
- [x] Verify actual endpoint/midpoint keys, restore starting temperature, and record review.

Rollback: restore only previous preset values in both modifier families. Existing private live paths and unrelated settings must remain byte-for-byte unchanged. No commit/push requested. Physical comfort remains manual.

Follow-up RED: source checker exited 1 with the previous preset tuple versus all-nine-key expectations. Updated both modifier families and matching docs afterward.

Follow-up GREEN and activation: source smoke exited 0; all 6 tests/test_redshift_control.py tests passed; nearest-50 reciprocal interpolation assertion produced the exact selected tuple. refresh-config exited 0 with REFRESH COMPLETE. Private candidate passed checker and i3 -C (exit 0; existing wheel deprecations only). Scoped patch changed only the preset values/comment, preserving unrelated live bytes. Reload returned success:true. Installed and running checkers passed both modifiers, reset/adjustments and workspace invariants. Actual X11 key injection: Super+1=1800, Super+5=2750, Super+9=6000, Alt+Super+2=1950 K; restored starting temperature. Private backup: /tmp/redshift-range-pwe9_k1i/config.before. git diff --check passed. No unexpected failure in this follow-up; intentional RED is exempt from incident recording.

Current manual checks: Super+1/5/9 display 1800/2750/6000 K; repeat with Alt+Super; 0/grave reset. Docs updated in README and docs/smoke-tests.md, including Super+3=2200 followed by adjustments 2450/2200 K. Subjective smoothness remains a human check. No commit or push performed; suggested commit: feat(i3): spread Redshift curve across nine presets. Cursor continuation: verify the latest all-nine-key section of this plan and source/installed/live mappings; preserve unrelated dirty work and private i3 settings.

Independent review confirmed both modifier families, reciprocal math, collision checks and README/smoke consistency. Reviewer found stale active values in the earlier shortcut plan; corrected its keys 1/3 to 1800/2200 K and linked this current range follow-up.

Historical curve milestones above are superseded by the current ten-key mapping and delivery milestone in plans/even-redshift-presets.md.
