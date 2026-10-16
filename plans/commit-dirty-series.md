# Ship reviewed dirty work

Review all current dirty changes, repair concrete delivery blockers, split the
safe work into focused commits, and push main to its configured origin once after
the complete series. No history rewrite, live migration, provider call, installer,
storage move, or destructive cleanup is part of this task.

## Context and scope

Initial branch main, upstream origin/main, public SSH remote. Baseline captured
before edits: 52 modified tracked files, 38 expanded untracked paths, no staged
changes. User explicitly authorized the full safe dirty scope with commit-plan-push;
pre-existing work is included only after review. Ignored traces, private rules,
live settings, recovery material and generated state remain excluded.

## Decisions and ordered checklist

- [x] Capture dirty baseline and independently review terminal, workflow and
  migration groups. Prior dirty-byte scan found only a test-expression false positive.
- [x] Correct that test's source spelling without changing generated JSON; retain
  privacy assertions and rerun regression checks.
- [x] Fix destination symlink containment with observed RED/GREEN; mark completed
  migration guidance historical and repair stale notification documentation.
- [x] Run focused validation, README gate and full dirty-byte review.
- [ ] Run the staged gate separately for each actual commit candidate.
- [x] Commit configuration privacy/refresh prerequisites with matching docs.
- [x] Commit migration helper, guard, plans/prompt/incident and matching docs.
- [x] Commit portable storage offload tool and docs.
- [x] Commit notification source outlines, speech updates, Dunst indicator and docs.
- [ ] Commit the clipboard startup improvement and checks.
- [ ] Commit pinned Context Mode tooling and docs.
- [ ] Commit metaprompt depth and existing-thread navigation with docs.
- [ ] Commit Markdown-aware workflow audit parsing and graph smoke checks.
- [ ] Commit privacy gate, commit policy, tests, plan and troubleshooting memory.
- [ ] Inspect all staged diffs, audit outgoing commit bytes/metadata, push once,
  verify remote outcome and report any residual paths.

## Shared surfaces and commit boundaries

README, smoke checklist, metaprompt guide, lessons and troubleshooting ledger have
multiple groups. Build cumulative index versions from reviewed sections while
leaving the complete working file intact; inspect each staged diff. Include this
living delivery plan with every implementation milestone. Never bypass hooks.
Every candidate is scanned immediately before the normal Git commit.

## Verification and risks

Tests agent runs relevant privacy/checkpoint, migration, notification, refresh,
metaprompt, workflow parser, installer-fixture, storage-fixture and editor suites.
Known pre-existing checkpoint-journal fixture can fail before tested behavior;
report exact results and continue independent safe work. Public postmortem aliases
use neutral paths and retain their known local alias-check portability warning.
No claim of full live desktop/provider/storage/migration QA or perfect secret
recognition. Exact-content fixture approvals require fresh review after edits.
Rollback: preserve working bytes and commits; no reset/rebase/amend/force-push.
A rejected push leaves safe local commits intact.

## Progress and review notes

Implementation review found a migration destination-ancestor symlink escape and
stale completed-migration/voice documentation. A worker owns only migration
script/tests; root owns documentation and commit orchestration. Other reviewers
found no confirmed privacy leak. Final evidence and commit milestones follow.

Ruling: group the Dunst status helper with notifications and the graph smoke helper
with workflow audits; both are small companion user/verification surfaces. Keep
Context Mode, storage, metaprompt and clipboard changes independently reviewable.


### Validation evidence before staging

Migration guard RED showed a disposable outside sentinel overwrite; minimum
containment guard plus 45 migration tests passed. Privacy gate/checkpoint/history
suites passed 45+1+14+24. Workflow doctor 26, Context Mode 6, storage 11,
config-snapshot discovery 19, Fish 9, notification/voice/editor and refresh shell
checks passed. Tmux notification2/scrolling14 passed under scoped socket permission.
Metaprompt138/139 passes; the unchanged baseline host-envelope expectation fails
closed. Timer33/34 and journal0/1 have known missing-note setup failures. These
three results remain warnings and are not described as green.

The full current dirty-byte audit exited0: 93 paths, zero findings/errors,
index unchanged. README gate reports pass_no_change. Native title service remains
unavailable; existing title retained. No real commit or push has occurred yet.
The configured upstream was fetched successfully without tags or worktree edits.


### Resumed after coordinated wait

User requested waiting for the active notification documentation session. It
completed and pushed69a53b9; ls-remote confirms that exact remote main tip. Its
working changes and original index were preserved. This shipping series starts
from69a53b9. The first scope assertion refused before any staging while that
session was active. Full shared-file snapshots were rebuilt against the new HEAD.

Real local snapshot validation returns2 in both modes; no configuration content
was printed or copied. Disposable contract tests19/19 remain green; local settings
were left untouched. Context Mode real local index/search/empty demos exited0
using disposable data and unchanged client config. Storage preview refused the
unmounted /tmp destination with exit1, intentionally, without moving anything.


### Milestone 1 — fix(config): keep live settings out of public source

Scope: read-only Codex validation, conflict-stopping refresh, matching canonical
instructions, command documentation and fixture expectations. Included current
shipping-validation incident/memory and this delivery plan. Verification:
snapshot19/19, Fish9/9 and refresh shell pass; README gate pass_no_change. Real
snapshot validation remains a reported local refusal without writes. Safe refresh
completed successfully. Remaining: migration, storage, notifications, clipboard,
Context Mode, metaprompt, workflow auditing and privacy-gate groups; no safety
blocker for this candidate. Three known baseline fixture failures remain recorded.


### Milestone 2 — feat(migration): add guarded private checkout cutover

Milestone1 committed as a230322. This milestone includes the migration helper,
46-test suite, completed historical prompt/plans, private-template controls,
matching README/smoke/lessons and incident-memory records. Destination symlink
escape reproduced RED before the minimal containment guard; all45 migration
checks passed. No live apply or rollback ran. Remaining: storage, notifications,
clipboard, Context Mode, metaprompt, workflow audit and privacy gate. No safety
blocker for this candidate; previously recorded runtime/fixture warnings remain.


Milestone2 hold: the safe read-only preview found an HTTPS-only remote comparison
rejecting the authorized canonical SSH origin. No migration writes occurred.
Worker adds a defining regression and finite canonical URL acceptance before the
migration candidate is restaged; no commit is attempted with the stale snapshot.

Milestone2 hold resolved: canonical URL RED/GREEN complete, all46 checks pass.
Frozen candidate refreshed; recorded HEAD/journal guards remain intact.

### Milestone 3 — feat(storage): add guarded home offload preview

Milestone2 committed as bbe1202. Storage helper,11 passing fixture tests,
README and smoke documentation are reviewed. Real /tmp preview refuses an
unmounted destination with no moves. No apply ran. Six groups remain after this
commit; known fixture/live-validation warnings remain unchanged.

### Milestone 4 — feat(notifications): outline sources and expose DND state

Milestone3 committed as 6ef819f. Notification source/speech/Dunst/tmux changes,
matching runtime smoke helpers and corrected public docs are reviewed. Focused
notification suites passed; isolated completion/question smoke scenarios freshly
passed, including zero playback for workers, empty and secret questions. No live
audio/provider request ran. Five groups remain after this candidate.

### Milestone 5 — fix(nvim): avoid blocking X11 clipboard detection

Milestone4 committed as eb903a2. Minimal clipboard provider selection preserves
explicit providers, Wayland and legacy behavior; all6 disposable startup checks
pass. README/smoke entries match the implementation. Four groups remain after
this candidate. No new blocker; previously recorded warnings remain.
