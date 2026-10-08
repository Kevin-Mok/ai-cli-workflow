# Compact sessions review

Make the explicit terminal review readable by showing project, title, goal, coverage gaps and outstanding checks in wrapped text. Keep full Markdown evidence behind `--details` and preserve stored digest and JSON contracts.

## Context and scope
The existing CLI calls the archival Markdown renderer directly. `--limit` bounds changed-source processing, not display. Source files sessions.py and associated tests are pre-existing untracked work; cli.py, README.md and docs/second-brain.md are already dirty. Preserve all their existing contents and changes; do not stage or commit.

## Decisions
Use plain text with no ANSI or Markdown syntax; width follows terminal with an 88-column maximum and a 40-column minimum. Group sessions by project, show goal and open checks, summarize unsummarized sessions as compact title/status rows. Do not display raw source paths, UUIDs, hashes or evidence paragraphs by default. Full details retain the existing render output. JSON remains complete and unchanged. Refresh remains metadata-only. Keep --limit semantics explicit in help and docs. No interactive selection or resolution behavior change.

## Checklist
- [x] Capture initial dirty state and locate root cause.
- [x] Write defining renderer/CLI tests and observe RED.
- [x] Implement compact renderer and --details integration.
- [x] Update README, usage docs and grouped smoke check.
- [x] Run focused and broader session regressions; inspect representative output.
- [x] Record final evidence and review.

## Risks and rollback
Long paths and check text must wrap; missing summaries and empty reports must be meaningful. Stale/partial coverage and refresh errors must remain visible. Stored private digest must keep full evidence and stable check IDs. Roll back only session-authored additions; extensive unrelated dirty state is protected.

## Verification
RED/GREEN: python3 -B tests/test_second_brain_sessions_render.py and python3 -B tests/test_second_brain_sessions_cli.py. Regression: python3 -B -m unittest discover -s tests -p 'test_second_brain_sessions*.py'. Manual: render representative long evidence with a 64-column width; inspect compact and detailed CLI help. No live inference needed for formatting validation.

## Progress and review
Root cause confirmed in sessions.render and cli.main. Sandbox startup failure has a dedicated reviewed postmortem; use approved scoped commands. Plan Mode is not available in the current harness; this living plan records the decisions.

## Handoff
Cursor prompt: Review plans/compact-sessions-review.md, preserve pre-existing dirty work, run the listed regressions and inspect default/--details/JSON rendering without live inference. Suggested commit: fix(second-brain): make session review compact. Keep this plan with matching implementation if committing later.

RED evidence: renderer tests failed 3 assertions because compact renderer was absent; CLI default emitted archival Markdown and --details was unrecognized. Intentional RED only.

## Final evidence and review
- Fresh session regression: python3 -B -m unittest discover -s tests -p 'test_second_brain_sessions*.py': 60 tests passed, exit 0. Renderer checks cover width 40/64, semantic content, archival noise omission, missing summaries/errors, retained open checks on skipped sessions, and resolved-check omission. CLI tests cover --details, complete JSON, refresh privacy and limit forwarding.
- Broader Second Brain run: 310 tests, one unrelated failure test_exact_sanitized_tree_exists_without_unapproved_files due to pre-existing 05 Daily Notes/2026-07-22.md. User vault preserved. Postmortem-memory run: 26 tests, one unrelated whole-corpus coverage failure; both task-specific targeted ledger checks pass.
- CLI help and synthetic 72-column compact output inspected; git diff --check exited 0. No live inference or private state changes needed.
- Independent reviewer confirmed archive/JSON compatibility and found skipped entries could retain checks. New RED test failed as expected; minimum inclusion fix passed.
- refresh-config was rejected by automatic approval review because this CLI/docs task did not clearly authorize broad home/Git writes. Safer alternative explicitly approved: confirmed installed cli.py and sessions.py match pre-change sources, saved rollback copies in /tmp/sessions-review-rollback-q3ad2j93, atomically installed only these two files. Installed CLI help and compact/details dispatch tested with a fixture, exit 0 and zero model calls. Broader refresh remains unexecuted; CLI activation is verified.
- No commits or staging performed. All prior dirty work retained; README and usage changes only extend the relevant session-review documentation. Rollback installed files from the two named backups, without touching private digest state.

## Follow-up: actionable default, 2026-10-08
User live output shows hundreds of empty/Guardian session rows. Root cause: terminal renderer includes every non-skipped entry, then prints archival goal/blocker context. Default must include only non-Guardian sessions with open checks; retain skipped sessions with open checks, state and detailed/JSON inventory. Count visible checks accurately, summarize omitted sessions once, and keep only status next to each title. Guardian detection uses the native title or inferred summary title, case-insensitively; no source parsing or state mutation. This supersedes the prior goal/blocker default.

- [x] RED tests for a large unsummarized/Guardian inventory, accurate visible count, and details preservation.
- [x] Filter default rows and omit goals/blocker paragraphs; align docs.
- [x] GREEN session regression, installed fixture verification and renderer smoke script.

Lookup: search `session review noise guardian` returned unrelated title/attribution/destination guidance; no matching filtering remedy. Fresh reproducer uses pasted-output structure. Extensive initial dirty state remains protected. No Plan Mode tool available; maintain this decision-complete plan.

Follow-up RED: tests/test_second_brain_sessions_render.py failed four assertions as expected: goal/blocker paragraphs remained, Guardian/empty rows remained, and visible count used total checks.

Follow-up GREEN: 61 session tests and 5 renderer tests pass (exit 0). Installed CLI fixture displays one check and one hidden count for 100 empty rows; details preserves the inventory. Independent review found no regressions. Only sessions.py installed, after comparing untouched source outside renderer; rollback /tmp/session-review-filter-rollback-x4vj4ifj/sessions.py. No broad refresh-config attempted: previous auto-review scope restriction remains; no configuration changed.

Follow-up broader verification: 312 Second Brain tests, 311 passed; unchanged unrelated vault-inventory failure due to pre-existing 05 Daily Notes/2026-07-22.md. Exit 1. No user vault files changed.

## Follow-up: five most recent work sessions, 2026-10-08

The accepted user plan supersedes both earlier terminal selection rules. Plain
review must select the newest five real work conversations across projects,
independent of open checks and the background refresh queue. Keep all prior
unrelated dirty work; initial snapshot and source copies are recorded in
`/tmp/recent-session-review-8elxxerz`. The subsequent commit-session request authorizes scoped delivery, including required pre-existing digest modules and prerequisite tests.

### Decisions and scope
- Implement in this checkout as requested; no worktree. Plan Mode is unavailable
  in this harness; this document is the execution ledger for the supplied plan.
- Separate safe discovery from inference in a cohesive review module. Screen all
  changed sources before displaying metadata; cache screened file fingerprints
  separately from hashes of successfully summarized dialogue. Migrate v1/v2
  state and retain check IDs/dispositions. No raw dialogue is persisted.
- Use native session origin (`source`, `thread_source`, parent metadata) to exclude
  spawned/Guardian helpers, with conservative legacy title fallback. Deduplicate
  by session ID, choose greatest parsed activity epoch, deterministic ties.
- `review` defaults to five; `--limit 1..20` limits display. `--refresh-limit 0..20`
  limits inference independently, defaulting to display size (20 for `--all`).
  `--all` selects all eligible historical work sessions, still respecting privacy
  and helper exclusions; it conflicts with an explicit display limit. Details
  and JSON expand the same selection. Background refresh retains its queue,
  seven-day initial window, refresh-budget limit, and metadata-only output.
- Recaps show numbered global recency, project, Toronto-local activity, two
  wrapped progress lines, and at most one next step from current remaining work
  or current unresolved summary checks. Retained historical checks remain in
  details/state only. Global diagnostics stay in details/JSON.
- Install only verified changed CLI modules with rollback copies. No configuration
  files change, so broad refresh-config is outside this scoped CLI install.

### Ordered checklist
- [x] Inspect sources, instructions, initial dirty state, prior incidents and native origin shapes.
- [x] Add selection/cache/privacy, renderer and CLI tests; record expected RED.
- [x] Implement discovery, state migration, selected refresh and compact recaps.
- [x] Update README, usage, and reusable smoke checks to the new contract.
- [x] Run session regressions and broader Second Brain checks; report known vault failure.
- [x] Independent final review; address meaningful findings with regressions.
- [x] Install verified CLI changes with rollback; exercise installed command.
- [x] Reconcile final evidence, remaining risks and handoff.

### Risks, verification and rollback
First discovery must screen previously unknown files, so cold-cache runtime scales
with source bytes. Unchanged runs should require neither reparsing nor inference.
Tests use isolated synthetic Codex/XDG homes and mock only model inference.
Run `python3 -B -m unittest discover -s tests -p 'test_second_brain_sessions*.py'`
and `python3 -B -m unittest discover -s tests -p 'test_second_brain*.py'`.
Exercise installed review with fixtures (default, limit, refresh budget, details,
JSON, all), then a requested real review; repeat unchanged-source verification.
Preserve real private state and back up installed modules before replacement.
Revert only this session's changes using captured baselines if needed.

### Progress and evidence
Sandbox startup failed before execution; reviewed incident is
`docs/postmortem/2026-10-08-recent-session-review-sandbox.md`. Lookup matched
`local-sandbox-loopback-approved-route`; approved scoped commands succeed. Its
new hash/alias has an explicit no-new-learning entry; targeted check exits 0.
Pre-flight interfaces: discovery supplies screened entries and content hashes;
selected inference consumes those hashes and updates successful-summary hashes;
CLI uses one selected report for compact, details and JSON. No interface conflict.

Defining RED: 10 review tests yielded four assertion failures (inventory selection,
deduplication, helper exclusion, historical discovery) and three missing-argument
errors. Five renderer tests and two CLI cases failed on the removed check-only
contract and absent options. After implementation these three suites passed:
10 review, 5 rendering, 11 CLI tests, all exit 0. Adapted the existing bounded
privacy-queue test to explicitly exercise background `refresh`; immediate review
screening is now covered independently. Updated the v1 fixture to omit all later
cache fields, and captured atomic-write rollback state after review's legitimate
metadata migration. Existing assertions about background behavior remain intact.

Independent review found four concrete gaps. Five new regression tests reproduced
privacy appends during inference, ambiguous v2 stale-summary hashes, two background
history enrollment cases, and archive moves reopening a dismissed check. All five
failed before the fix; afterward 77 session tests passed. Review discovery now
revalidates after inference, keeps an independent background refresh timestamp,
never enrolls historical sources into the background queue, conservatively
migrates only proven ready/partial hashes, and preserves identity/check IDs when
a source moves to the archive. The scheduled algorithm retains its original
queue/window policy. No reviewer findings were deferred.

Latest AGENTS guidance adds helpful emoji and ASCII mode to CLI output. The new
renderer test observed RED on the missing visual cue; the implementation adds a
compact header icon, local warning icon and `--plain` with ASCII escapes. JSON
remains unchanged; no ANSI colors are emitted, including under NO_COLOR.

Source drift was detected before installation and recorded in
`2026-10-08-session-review-verification-drift.md`. Only the baseline-identical
sessions.py was restored with this task's patches. The next broader run ran
328 tests, 327 passed, with only the known pre-existing vault file inventory
failure; the guarded source hash was unchanged. The native title endpoint is
unavailable, so the last successful title remains in place.

Installation evidence: `/tmp/recent-session-review-rollback-1j1h03__` contains
installed-before copies, baseline-v2 source copies, private pre-migration state,
and verified source hashes. Three files required replacement (cli.py, sessions.py,
session_review.py); parser and installer already matched the verified sources.
All five installed files were compared by hash. The fixture smoke command
`python3 -B tests/scripts/second_brain_sessions_review_check.py` passes against
`/home/example/scripts`: default five, recency, helper exclusions, all/limits,
refresh budget, preserved dismissal and zero-inference repeat. Installed help
lists `--limit`, `--all`, `--refresh-limit`, `--plain`, and `--details`.

README gate: `./scripts/executable_readme-recruiter-sync` returned
`pass_no_change`, exit 0, after the in-scope updates. Existing unrelated README
and smoke-check edits made concurrently remain untouched. No tracked configuration
was changed by this task; no broad refresh-config or timer activation was run.
The first default real-session review is in progress; only safely screened
selected recaps may invoke the existing isolated inference runtime.

### Updated handoff
Atomic scope: recent-review module, its parser/persistence/CLI integration,
installer manifest, session tests, fixture smoke script, relevant docs and this
plan; include matching incident/learning records when committing later. Do not
stage the extensive unrelated pre-existing or concurrent changes.

Cursor prompt: Read the newest follow-up in plans/compact-sessions-review.md and
the current AGENTS instructions. Preserve all unrelated dirty work. Verify the
newest-five selection, independent recap budget, origin/privacy exclusions,
archive dispositions, v1/v2 migration and --plain mode with
`python3 -B -m unittest discover -s tests -p 'test_second_brain_sessions*.py'`.
Run `python3 -B tests/scripts/second_brain_sessions_review_check.py` against the
installed CLI, then the broader Second Brain suite; report the known unrelated
vault-inventory test separately. Inspect only the session-authored diff and
keep this plan and documentation with any authorized commit.

Suggested commit: `feat(second-brain): recap five recent work sessions`.

Final automated checks after ASCII-mode steering: 79/79 session tests pass,
fixture smoke passes against installed CLI, README gate returns pass_no_change,
and git diff --check exits 0. Broader command
`python3 -B -m unittest discover -s tests -p 'test_second_brain*.py'` ran 330 tests:
329 passed; only test_exact_sanitized_tree_exists_without_unapproved_files fails
because of pre-existing `second-brain/05 Daily Notes/2026-07-22.md`. The vault is
untouched. No repository type-checker configuration is present for this Python
CLI; all changed modules import and execute through the regression and runtime
checks. No deferred code-review findings remain.

Live default selected five sessions correctly and displayed four recaps, with a
localized invalid_summary on one generated recap. Recorded in
`docs/postmortem/2026-10-08-recent-session-review-live-check.md`; a one-call retry is
in progress without regenerating the successful summaries.

Live verification exposed a provider/local schema mismatch: generated check keys
were unconstrained even though the validator requires short lowercase kebab-case.
An inference-boundary test accepted invalid `UI Check` before the fix (RED). Added
the existing check-key/text constraints to the provider schema and made the
prompt rule explicit, preserving strict validation. All 80 session tests now
pass. The sixth verified runtime file is session_digest_runtime.py; its baseline
copy is in the same rollback folder. A guarded install detected it already
matched the verified source, so no overwrite was needed. Default live review
is being rerun with this corrected runtime.

### Final acceptance evidence
The installed plain default command exited 0 and showed five eligible real work
sessions with five useful recaps. A subsequent installed JSON review independently
checked five unique IDs in descending parsed activity order and reported
`model_calls: 0`; `--limit 1 --refresh-limit 0 --plain` exited 0 with ASCII output.
Final source/installed verification covers six matching runtime files.

Final automated result is **80 session tests passed**, and **330 of 331 broader
Second Brain tests passed**. The sole broader failure is the known unrelated
vault inventory assertion for the pre-existing Daily Note. The independent
review's four findings were reproduced and fixed; the live-discovered provider
schema mismatch was also tested RED/GREEN and verified live. README, usage,
smoke checks and this plan describe the current options and behavior. Targeted
checks cover all task-created incident hashes and learning records.

Remaining limits: cold discovery screens all uncached sources and costs time;
recap generation depends on the existing model service, with bounded per-recap
failure handling. Active conversations can change while review runs; final
privacy screening may replace a selection with an unsummarized newer session
when the inference budget is exhausted. The observed source reversion and native
title transport outage have no established underlying fix; installed/source
hashes remained equal at final verification. No unrelated dirty changes were
reverted, and no staging, commits, worktrees or timer/config activation occurred.

Rollback copies are in `/tmp/recent-session-review-rollback-1j1h03__`.
`baseline-v2/` contains coherent pre-task CLI sources, `installed-before/` records
what was present before replacements, and `private-state/` contains the private
pre-migration snapshot. Restore matching code and schema-version state together
if rolling back; preserve any newer explicit check resolutions before replacing
state. This is a local temporary rollback location, not a tracked artifact.

## Scoped delivery

The user authorized committing the prerequisite digest modules and tests. The scope helper returned unsafe because it detected no successful repo-writing actions; direct-write evidence and captured baselines establish the scoped feature changes. Shared README, usage, smoke checks, lessons and postmortem learning ledger are split against HEAD. Unrelated changes and timer setup are excluded. A temporary index preserves concurrent staging. Fresh checks: 80 session tests pass, installed fixture smoke passes, README gate pass_no_change. Broader verification remains 330/331 with the unrelated vault inventory failure. Commit and upstream push follow scoped-tree verification.

Scoped-tree verification: 69 included session tests pass, fixture smoke passes against the staged runtime, and the staged README gate returns pass_no_change. Prior full-workspace verification includes 80 session tests; unrelated timer/unsafe-source test files remain outside this session commit.

Final delivery checks: normal-checkout broader suite ran 331 tests, 330 passed; only the documented pre-existing Daily Note inventory failure remains. The optional extracted-tree broader run exposed protected-path/Git-metadata fixture assumptions, recorded with a no-new-learning ledger entry. Source/staged/installed runtime hashes match; installed smoke and README gate pass. Rollback remains the verified private local backup described above. Reviewed scope is ready for a single Conventional Commit and origin/main push.
