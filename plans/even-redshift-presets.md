# Even Redshift presets

Spread Super+1–0 and Alt+Super+1–0 evenly in kelvin from 1800 to 6500 K. The latest ten-key follow-up below supersedes the earlier nine-key evidence. This supersedes the reciprocal scale in the earlier curve plan.

## Decisions and scope

Use linear interpolation over eight intervals (587.5 K), rounded to the nearest 50 K with half steps rounded up: 1800, 2400, 3000, 3550, 4150, 4750, 5350, 5900, 6500 K. Update only presets, their existing checker and matching README/smoke documentation. Preserve reset, adjustment and workspace shortcuts. No controller changes, commit or push requested. Initial git status captured; all pre-existing dirty work is protected, including concurrent delivery work and prior plans. Live i3 config is intentionally unmanaged by chezmoi; preserve all other private/live bytes with a guarded scoped patch.

## Checklist

- [x] Read current source, checker, README, smoke docs and prior plan; capture status.
- [x] Observe RED with defining expectations changed first.
- [x] Update both modifier families and current usage documentation.
- [x] Run focused tests, refresh, validate/reload guarded live config.
- [x] Verify actual keys, restore starting temperature and record review.

## Verification and rollback

Run python3 scripts/smoke_redshift_keys.py before/after, python3 tests/test_redshift_control.py and git diff --check. Independently verify nearest-50 linear tuple. Run refresh-config, validate candidate via i3 -C, reload and check installed/live mappings. Actual Super+1/5/9 must select 1800/4150/6500 K; check Alt+Super alias and reset. Restore starting temperature after automated checks. Human smoke procedure lives in docs/smoke-tests.md. Roll back only preset values/comment in source and live config, validate/reload. Existing i3 wheel deprecations and subjective display comfort are outside this change.

## Evidence and review

Defining RED exited 1: the old reciprocal tuple differed from the new linear expectations. Updated both modifier families and matching docs afterward. No unexpected failures observed. Suggested commit: feat(i3): space Redshift presets evenly to 6500 K. Cursor continuation: follow this plan's latest evidence, verify both modifier families and preserve unrelated dirty work and private i3 settings.

Final evidence: source checker passed; all 6 controller tests passed; independent linear interpolation with Decimal ROUND_HALF_UP on value/50 then multiplication by50 matched the tuple. refresh-config completed with REFRESH COMPLETE. Live candidate checker and i3 -C exited0 (existing wheel deprecations only). Scoped patch preserved unrelated live bytes; i3-msg reload returned success:true; installed and --live checkers passed both shortcut families and workspace/reset/adjustment invariants. Actual Super+1/5/9 selected1800/4150/6500 K, Alt+Super+2 selected2400 K; starting temperature restored. Private rollback backup: /tmp/redshift-range-jk8pkjvf/config.before. git diff --check passed. README and smoke docs match current scale; no controller changes, commit or push performed. Verification-tool rounding assertion was corrected and recorded in the existing Redshift incident report; no runtime defect.

Independent review:4 verified claims,0 incorrect,0 unresolved for source/installed mappings, rounding math, README and smoke documentation. Main observed successful live IPC and actual keypress outcomes above; subjective display comfort remains untested.

## Follow-up: use all ten number-row keys

User requested 1–0. Redistribute the same1800–6500 K range over nine intervals, rounded to nearest50 K:1800,2300,2850,3350,3900,4400,4950,5450,6000,6500. Both modifiers share the mapping;0 becomes a6500 K preset, grave remains reset. Preserve adjustments/workspaces and all pre-existing dirty work captured before edits. Earlier evidence above is historical.

- [x] Inspect current state and update defining checker first.
- [x] Observe expected RED, then update source and matching docs.
- [x] Run checks, refresh, validate/reload guarded live preset changes.
- [x] Verify keys1/9/0/grave and alias, restore temperature, record review.

Rollback only this follow-up's preset changes; private live config remains protected. No commit/push requested.

Ten-key RED: updated checker exited1 against the previous nine presets, before source edits. Updated both modifier families and matching docs afterward.

Ten-key final evidence: source checker passed, all6 controller tests passed, independent Decimal nearest50 half-up interpolation over9 intervals matched all ten values; git diff --check passed. refresh-config completed successfully. Guarded private candidate checker and i3 -C exited0 with existing wheel deprecation diagnostics only. Scoped preset/comment patch preserved unrelated live bytes; reload returned success:true. Installed and live checkers passed both modifier families, grave reset, unchanged adjustments and workspace invariants. Actual X11 presses verified Super+1=1800, Super+9=6000, Super+0=6500, Alt+Super+5=3900 and Super+grave=6500 K. Starting temperature restored. Private backup: /tmp/redshift-ten-18ieia4c/config.before. Docs and current checker reflect the new0 preset/grave reset distinction. No unexpected failure or new incident. No commit/push performed. Subjective comfort remains manual. Suggested commit: feat(i3): use all ten Redshift preset keys. Cursor continuation: verify the latest ten-key follow-up and source/installed/live mappings, preserving unrelated dirty work and private config.

## Session delivery milestone

Commit subject: feat(i3): spread Redshift presets across ten keys. User requested commit-session; commit and push this session's attributable config/checker/README/smoke changes, all three related plans, incident report and only its memory registration. Scope helper returned unsafe because it detected no successful writes; captured pre-write status and successful writes in this conversation establish direct attribution for session01a15b5e-c683-7732-95be-7ebce252259a. Root README gate passed. Preserve unrelated memory reference edits, staged ledger changes and existing reports/prompts. Use an isolated index, explicit parent and guarded ref publication with active hooks and exact-tree privacy checks to avoid the known concurrent-HEAD race. Reconcile only scoped index entries while preserving the pre-existing staged ledger delta. Rollback is a later revert or restoration of scoped preset lines; no history rewrite. Current functionality is already live and verified; remaining work is exact-candidate checks, commit, one upstream push and final report. No implementation blockers. Public ledger registration uses a neutral example-home alias; local lookup aliases stay in the worktree.

Delivery readiness: fresh source/installed/live checks passed, all6 controller tests passed, root README gate pass_no_change, targeted incident-memory check passed, and exact isolated candidate/privacy preflight passed. Reviewed scope is9 files: config/checker, README/smoke docs, three related plans, session incident and only its public-safe memory entry. Unrelated staged ledger data and all other dirty paths are excluded. Milestone feat(i3): spread Redshift presets across ten keys is ready for guarded commit and one push to origin/main; no implementation blockers.
