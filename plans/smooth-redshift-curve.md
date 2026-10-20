# Smooth Redshift preset curve

Make Super+3–9 progress smoothly from 2100 to 6000 K by changing existing presets and applying the scoped live bindings.

## Context and decisions

Use rounded reciprocal-temperature spacing: 2100, 2350, 2700, 3100, 3700, 4600, 6000 K. User explicitly requested both Super and Alt+Super modifiers. Keep keys 1/2, reset and adjustment values. Move workspace 11 to Super+F11 and remove conflicting Godot binding as in existing source. No controller changes or commit requested. Preserve pre-existing edits in README, smoke docs, config and checker, plus all unrelated dirty files captured in initial git status. i3 is intentionally unmanaged by chezmoi; preserve private live config and change only preset lines after refresh.

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
