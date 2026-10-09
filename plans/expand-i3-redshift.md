# Expand i3 Redshift shortcuts

Spread the temperatures previously on keys 2–4 evenly across keys 2–6, then apply and verify the running i3 configuration.

## Scope and decisions

User confirmed Alt+Super+2–6 = 1800, 2100, 2400, 2700, 3000 K. Preserve 1 = 1200 K, 7–9 = 4800, 5400, 6000 K and 0/grave resets. Update the existing smoke helper, i3 source, README and smoke documentation. User subsequently requested commit-session; ship only directly evidenced task changes. Pre-existing dirty files were captured with git status --short; preserve all existing hunks, including README, smoke docs and memory ledger.

## Checklist

- [x] Inspect bindings and confirm intended range with user.
- [x] Update defining smoke expectation before implementation.
- [x] Observe expected RED, update source and docs, then observe GREEN.
- [x] Run refresh-config, validate installed i3 config, reload and check live IPC.
- [x] Record verification and remaining limitations.

## Risks and rollback

The gap from key 6 to key 7 is intentional because keys outside 2–6 stay unchanged. Refresh snapshots live Codex/Git config and applies managed files; inspect resulting changes. Roll back only this task’s binding/doc changes, then refresh and reload. No subjective color check claimed without user observation.

## Verification and review

Run python3 scripts/smoke_redshift_keys.py before/after, then against ~/.config/i3/config and --live. Run i3 -C -c ~/.config/i3/config, i3-msg reload, and git diff --check. Manual: press Alt+Super+2 through 6; progressively less warm in 300 K steps; reset using 0 or grave. Handoff commit suggestion: fix(i3): spread Redshift presets across keys 2–6. Cursor continuation prompt: Verify the confirmed i3 Redshift mapping in plans/expand-i3-redshift.md, preserve unrelated dirty work, and rerun source, installed and live checks.

RED: smoke helper exited 1 showing old keys 3–6 against confirmed values. GREEN: same helper exited 0 after the four binding changes.

Final evidence: source, installed and --live smoke checks all exited 0. fish -ic 'refresh-config' exited 0 (REFRESH COMPLETE); it adopted the existing local Vesktop settings into tracked source as part of its normal conflict handling. That resulting file is left unstaged. i3 -C -c ~/.config/i3/config exited 0 with existing wheel_up_cmd/wheel_down_cmd deprecation diagnostics. i3-msg reload returned success:true. git diff --check exited 0. Implementation was completed before the later commit-session request. Visual warmth remains a user manual check. Required changes are four temperatures plus the explanatory comment; documentation and the existing smoke helper match. Existing unrelated work preserved.

## Delivery milestone

Commit subject: fix(i3): spread Redshift presets across keys 2–6. Completed: implementation, matching docs/check/plan, sandbox recurrence record and its scoped ledger entry. Fresh source/installed/live checks pass; README gate pass_no_change. No implementation blockers. Next step: commit this reviewed scope and push main to origin/main. The scope helper returned unsafe (no detected repo-writing actions); successful writes recorded in this conversation establish the fallback. Preserve baseline-dirty hunks, all other dirty files, and the unrelated local Vesktop settings captured by refresh. Session: 01a1228e-ed04-7712-83ef-d9f1ea81dfbf.
