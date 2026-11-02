# Make commit-plan-push execute by default

Explicit skill invocation should plan, commit and push; explicit plan-only requests remain read-only.

## Scope and decisions

Update the existing skill, catalog, README, smoke checks and defining contract test. Refresh admission costs without adding a skill. Picker metadata already requests execution. This request changes the skill; it does not ship the pre-existing dirty worktree. Initial status:27 dirty paths, no staged changes; preserve all unrelated hunks.

## Checklist

- [x] Inspect source, callers, existing tests and initial status.
- [x] Observe defining test RED; update mode routing and documentation.
- [x] Run focused tests, admission/calibration checks and refresh-config.
- [x] Record evidence and limitations.

## Risks and rollback

Keep explicit planning-only and privacy/hook safeguards. Undo only this session's hunks to restore the old default. Full refresh may encounter protected local drift; report exact limits rather than overwrite user work.

## Verification

Run unittest discovery for test_commit_plan_push_skill.py and test_skill_admissions.py; scripts/sync-vetted-skills --check; fish -c refresh-config. Manual: in a disposable repository invoke the skill alone, then request plan only; expect delivery in the first case and zero Git writes in the second. Live model delivery is not automatically exercised against this dirty worktree.

## Evidence and review

Defining invocation contract first failed (1/5), then passed5/5 after routing changes. Admission regression initially exceeded20000bytes; session-added bookkeeping shortened to19764bytes, fresh7/7passed. sync-vetted-skills --check:241entries/0stale. trigger-eval --check:46/51, gatePASS (lexical routing proxy, not model behavior). README gate:pass_no_change. Incident helper check:0errors/0missing sources. fish -c refresh-config exited0 with REFRESH COMPLETE; cmp confirms installed skill equals tracked source. Reviewer found no conflicting default/planning-only instructions.

No commit/push requested for this skill-edit task. No end-to-end agent delivery in a disposable repository or actual wrapped terminal-copy verification performed. Pre-existing dirty changes remain protected. To check manually, use the skill alone in a disposable repo with upstream; repeat with explicit plan only and confirm zero Git writes.
