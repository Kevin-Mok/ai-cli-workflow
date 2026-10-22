# Dirty worktree delivery

Review the current dirty worktree, commit safe changes in three coherent groups, then push the complete series to origin/main. Keep machine-local substitutions and session metadata outside the public commits.

## Context and boundaries

Initial branch main tracks origin/main at 98a57d2; staged changes were empty. The user explicitly invoked commit-plan-push for the entire dirty worktree. Preserve unrelated local bytes, existing hooks and history. Public candidates use neutral /home/example paths and redacted local executor IDs; the local evidence ledger keeps its physical aliases. No files exceed the Git LFS size threshold.

## Ordered series

- [x] docs(memory): record reviewed troubleshooting evidence — generalized external findings, report registrations, saved Discord implementation prompt and handoff incident.
- [x] fix(i3): apply repeat defaults without fish exports — startup code/test, matching plan/incident, README/smoke/lesson and memory additions.
- [ ] fix(notifications): read Discord once and add speech volume control — isolate parsing, one Dunst callback, bot exclusions, persisted 75% volume, tests, matching plan/incident and documentation.
- [ ] Recheck residuals and push the verified series once to origin/main.

## Safety, residuals and rollback

Leave :memory:.ses as session metadata. Existing path-only substitutions and revealed local executor IDs are machine-local residuals. Inspect exact staged bytes, run the unchanged privacy gate immediately before each commit and retain hook enforcement. Do not rewrite history or weaken privacy rules. Rollback would use new revert commits after review; no reset/rebase/amend is authorized.

## Verification

README gate: pass_no_change. Fresh focused notification85 and basedpyright0 pass. UBS startup, keyboard-remap, dictation-binding and pywal checks plus Bash syntax pass. Targeted memory checks for all three new local incidents pass. Private Dunst1 and installed speech/bot/volume probes passed during implementation; user confirmed75 by listening. Earlier broader290 run retained unrelated socket restrictions and a placeholder-path fixture failure; no blanket green-suite claim.

Review candidate JSON semantically to avoid committing incidental key/list reordering. Recompute source hashes when public report bytes are sanitized, and preserve reciprocal finding links. Exact privacy gate results and commit milestones follow below.

## Delivery milestones

Milestone 1 — docs(memory): record reviewed troubleshooting evidence. Candidate evidence was reviewed against source reports; all20 new source hashes match. Removed one unsupported historical test-count assertion while retaining its supported pass/limit statement. Public paths and executor IDs are neutralized without modifying local evidence bytes. README and focused checks pass; privacy check is the final commit gate. Remaining: startup and notification commits, then one push. No blockers beyond any privacy findings.

Next step: commit the reviewed evidence candidate. No push has been performed yet.

Milestone1 committed as0028565; privacy gate and active hook passed. No push yet. Milestone2 — fix(i3): apply repeat defaults without fish exports — includes the startup correction, focused regression, matching plan/incident, README/manual checks, lesson and reviewed memory. All four shell regressions, syntax and targeted memory checks pass. Next: notification commit and one upstream push; no implementation blockers.

Milestone2 committed as82fc01c; all focused shell checks, exact candidate privacy gate and active hook passed. Milestone3 — fix(notifications): read Discord once and add speech volume control — is the final prepared implementation group. Fresh85 tests and zero-error type check pass; private Dunst, actual installed once-only/bot-silence probes and user-confirmed75 playback are recorded in its implementation plan. README gate passes; privacy gate is required immediately before commit. No content group remains omitted after this candidate; deliberate private aliases, path-only substitutions, local executor IDs and session metadata remain outside publication. Next step: one normal push of the complete series to origin/main; actual push result will be reported in Codex output.

Concurrent publication: d5fe03c (tcu shortcut) was added after milestone2. Preserve its files/report registration; rebuild from current HEAD and merge shared ledger additions. Candidate review caught the missing new record before commit. Use explicit-parent/CAS publication with active hooks and exact-tree privacy checks so a later HEAD change is blocked safely. One live-ledger read failed during concurrent work; subsequent reads were valid, so stable-snapshot/atomic-update guards preserve its current data without claiming a product repair.
