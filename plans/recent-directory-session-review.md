# Review recent directories and sessions

Show the five most recently worked-in directories, each with its three newest session recaps, and repair the source exclusions that hide recent conversations.

## Scope and decisions
Preserve all current dirty work (captured before edits). Work in this checkout. No Plan Mode capability is available; this plan records the accepted request. Default --limit counts directories (1–20); each directory has up to three eligible sessions. --all retains complete eligible history. Keep flat JSON session structure, grouped in directory recency order; details expand that selection. Infer selected recaps in global activity order, default budget min(directory limit × 3, 20), all default 20. Keep independent refresh-limit and scheduled refresh unchanged. Preserve privacy, physical source safety, dispositions and unchanged-summary reuse.

## Checklist
- [x] Capture baseline; inspect parser, discovery and existing contracts.
- [x] Diagnose absent recent sessions using metadata and record shapes, without disclosing transcript content.
- [x] Write failing native-record and directory grouping regressions.
- [x] Implement minimal parser correction and grouped review.
- [x] Update README, usage and reusable smoke checks.
- [x] Run focused and broader checks, review independently, install only verified runtime changes with rollback.
- [x] Exercise installed command against real metadata; record exact evidence and limits.

## Risks and rollback
Never relax privacy screening to include private content. Metadata caching must invalidate parser-version changes. Malformed input remains excluded. Five directories may require fifteen recaps; inference remains bounded and errors localized. Use rollback copies of changed installed modules and private state before activation; preserve explicit newer resolutions.

## Verification
Run python3 -B -m unittest discover -s tests -p 'test_second_brain_sessions*.py'; run python3 -B -m unittest discover -s tests -p 'test_second_brain*.py' (known unrelated vault-inventory failure). Run python3 -B tests/scripts/second_brain_sessions_review_check.py against source and installed CLI. Compare safe native latest-activity metadata with installed --refresh-limit 0 JSON selection. Run README gate and inspect scoped diffs.

## Investigation
User output shows only four old sessions. Native source inventory, parser reasons and cache freshness need investigation before fixes. Lookup query session review missing recent unsafe_source parser returns generic attribution/deployable-file/parser-contract guidance, no confirmed matching remedy. Independent read-only investigator assigned. Native title endpoint still has the known transport outage; no retry remedy attempted. Initial guessed tracked superpowers skill paths were absent; actual catalog paths under ~/.agents/skills were read successfully. No product change from the failed reads.

## Progress and evidence

Root cause: broad personal-context regex on arbitrary tool output excluded all nine latest real conversations examined (31 other latest sources were helpers). Public policy and skill output is not private retrieval and never enters inference. Screen actual call identity/arguments instead, protect private session/turn cwd and nested MCP invocation identity, handle native root agent dialogue, and distinguish public patch body literals from private destination paths. Parser-revision fingerprints force re-screening of old exclusions while preserving successful summary hashes and dispositions. Intentional RED cases covered grouping, global inference order, public policy/skill output, native agent dialogue, cache migration, nested MCP/turn cwd, and patch target provenance. All 91 session tests pass; source fixture verifies five directories with three recaps each and zero inference on repeat. README gate pass_no_change. Broader run: 340 of 341 tests pass; only known pre-existing vault inventory failure (July 22 Daily Note). A trailing blank-line diff check was corrected without behavior changes.

Independent reviewer confirms eight of nine latest real sources recover. One remains conservatively excluded because unknown exec-wrapped Python source-edit commands contain private-store path literals; distinguishing inert source from actual access would require unsupported dataflow analysis. This is an explicit remaining accuracy limit, not established private retrieval. Display warns that restricted sessions can make recent work incomplete. No parser safety relaxation is justified for that ambiguous case.

Installed fixture verification passes: default five directories, fifteen synthetic sessions, preserved dispositions and zero-inference repeat. Four runtime modules installed atomically after focused checks, with rollback and private-state backups in /tmp/recent-directory-review-rollback-_eky_r5s. Installed zero-inference real discovery selects five expected current directories and thirteen sessions (one directory has only one eligible session), all from native parsed activity. Actual recap generation is in progress. Latest focused result 92 tests passed; broader 342 of 343 passed, sole known vault-inventory failure.

Final independent review: all concrete findings resolved; reviewer independently ran 26 review acceptance tests and scoped diff check successfully. No blocker found. Unknown executable-input ambiguity remains documented.

## Reproducible handoff
Atomic scope: parser provenance, revisioned metadata cache, grouped selection/rendering, CLI help, focused tests and fixture smoke, README/usage/smoke docs, this plan and matching incident learning. Suggested Conventional Commit: fix(second-brain): review recent directories and restore work sessions. Cursor prompt: Read plans/recent-directory-session-review.md and current AGENTS; preserve unrelated dirty work. Re-run the listed regressions and installed fixture, inspect five directories and three newest eligible recaps per directory, confirm actual private retrieval/malformed sources stay excluded and dispositions survive parser revision. Keep this plan and matching docs with the implementation commit if delivery is authorized. Manual check: second-brain sessions review; second-brain sessions review --limit 1 --refresh-limit 0 --plain. No sudo is needed. Roll back the four runtime modules from the named local backup, preserving newer explicit check dispositions before restoring private state.

Installed live default acceptance: 305 seconds, 12 model calls, five directories, thirteen selected sessions and thirteen valid recaps, error null. Two conversations changed during inference and received localized changed_source warnings; a final bounded two-call refresh is in progress. Scheduled algorithm/configuration was not changed or activated.

## Final acceptance
Live generation exited 0 with all thirteen selected sessions recapped across five directories; twelve missing recaps were generated. Final bounded refresh made one model call and exited 0; one still-active conversation changed again and remains explicitly stale. This is a reported concurrency limit, not hidden refresh failure. Installed CLI JSON/ASCII runtime checks verify five directories, up to three sessions each, unique IDs, directory and within-directory native activity order, zero-budget operation and full recaps. No configuration or timer changes were made; four source/installed runtime files match. README gate and scoped diff check pass. No commits or staging were performed for this follow-up; unrelated dirty work is preserved.

## Follow-up: bat paging and emoji hierarchy

User explicitly requests bat as a less-style reader and prettier emoji output. Preserve the five-directory/three-session contract. Interactive text review uses bat (batcat alias supported) with forced less paging and no source-style line-number/grid clutter. Use direct less fallback when bat is absent; print directly when no pager exists. JSON, redirected output, --plain and explicit --no-pager do not invoke a pager. NO_COLOR disables bat coloring. No shell evaluation of pager settings. Add folder, session, activity, recap and next-step emoji cues with spacing between sessions; retain ASCII output and wrapped recap limits.

- [x] Observe RED for interactive pager dispatch and emoji hierarchy.
- [x] Implement minimal pager helper and rendering cues.
- [x] Cover quitting/fallback, non-TTY/plain/JSON bypass and NO_COLOR.
- [x] Update README, guide and reusable smoke check; run focused and broader checks.
- [x] Install verified changed modules with rollback; exercise real bat/less in a PTY and zero-inference live review.

Verification: session regression suite, source/installed fixture smoke, real PTY bat/less quit with q, source diff check and README gate. Preserve private digest and all unrelated dirty work. No configuration or scheduling changes; install only CLI and renderer modules. Rollback copies will be recorded before installation.

Pager follow-up verification: missing pager dispatch/flag and absent emoji cues failed RED; periodic-progress helper also failed RED before implementation. Emoji-prefix terminal-cell width reproducer failed before wrap-width correction. Now 100 session tests pass. Both source and installed smoke --pager-check pass against real bat/less in a disposable PTY, including Space scroll and q exit. Independent pager reviewer found no blocker. Broader 350/351 pass, sole known Daily Note inventory failure. README gate pass_no_change and scoped diff check pass. Two changed modules installed with verified hashes and rollback copies in /tmp/session-review-pager-rollback-nvj24pe0. Ongoing five-second elapsed progress uses stderr and stops before the pager starts; no percentage/ETA is invented. No configuration or timer changes and no Git staging/commits. Real installed zero-budget PTY review opened bat/less with emoji hierarchy and current directory selection; Space advanced to the next page and q exited 0. Newer live sessions appeared correctly with explicit not-generated labels because this check disabled inference.

Smoke handoff (repo cwd /home/example/linux-config; no sudo): review --refresh-limit 0 for bat/less scrolling; add --no-pager for direct emoji output; add --plain for ASCII/no pager; use --limit 1 for one directory; --format json for machine output; use --details for full evidence; run python3 -B tests/scripts/second_brain_sessions_review_check.py --pager-check for disposable real viewer verification. Suggested combined follow-up commit remains fix(second-brain): review recent directories and restore work sessions, including pager/progress/docs/plan.

## Follow-up: full prettified default report

The latest request supersedes compact recap truncation and raw archival Markdown under `--details`. Default text and `--details` will use the same full terminal report: clear emoji sections, complete goal/intentions/accomplishments/remaining/blockers/verification, all check dispositions and IDs (retained checks clearly separate), readable session metadata and resume command, and a coverage footer. Keep archival `digest.md`, JSON schema, screening, directory selection and refresh budgets unchanged. Bat/less remains the interactive reader. Preserve all pre-existing dirty work; this follow-up is not a new commit request.

- [x] Observe RED for full default/details parity, complete evidence, check history and cell-aware wrapping.
- [x] Implement full terminal sections and aligned metadata without truncating content.
- [x] Update README, guide and existing smoke assertions/checks.
- [x] Verify focused/broader tests, fixture PTY, README gate and scoped diff.
- [x] Install only verified changed CLI files with rollback copies; test installed default/details equivalence and pager.

Verification uses the existing session suites and disposable smoke script. All content remains screened before rendering and controls/secrets remain cleaned. Session/check cache hashes stay in JSON; full meaningful user information is displayed. Known unrelated vault inventory failure remains separately reported.

Full-report progress: RED demonstrated truncated goal/evidence, missing checks/metadata, raw details Markdown and changed-space commands. Independent review passed renderer/CLI tests and identified VS16 width and combined stale/partial limits; both received RED regressions and fixes. Now 105 session regressions pass. Source and installed disposable smoke with --pager-check pass, confirming full default/details parity, five directories/three sessions, complete check dispositions, JSON/ASCII and real Space/q paging. Fixture assertion incidents were recorded in docs/postmortem/2026-10-08-full-review-smoke-fixture.md; targeted reviewed-hash check exits 0 with explicit no-new-learning decision. README gate pass_no_change and scoped diff check exit 0.

Only cli.py and session_review.py were installed atomically after verification, with byte equality and rollback manifest in /tmp/full-session-review-rollback-ifm3jqji. Real installed command checks exit 0: --limit 1 --refresh-limit 0 default/details each show full prettified report, three sessions in one directory, ASCII works and JSON reports zero model calls. No config/timer changes, no staging or commits for this follow-up.

### Full-report handoff

Atomic plan: define complete report tests → implement the shared width-aware terminal renderer → align usage/README/smoke checks → run regressions and review → install verified CLI files with rollback → exercise native command and PTY. Automated checks: `python3 -B -m unittest discover -s tests -p 'test_second_brain_sessions*.py'`; broader same discovery with `test_second_brain*.py`; `python3 -B tests/scripts/second_brain_sessions_review_check.py --runtime-dir scripts --pager-check`; installed equivalent without --runtime-dir; README gate and scoped diff check. Manual checks: default review, --limit 1, --details, --no-pager, --plain and --format json, all with --refresh-limit 0 for no inference; Space and q navigate the interactive reader. No sudo required.

Docs updated: README session command and operating description, docs/second-brain.md usage contract, docs/smoke-tests.md Action/Expected checks, and this plan. Suggested future commit: `fix(second-brain): prettify full session reviews` (include matching plan/docs/test and incident learning updates, preserve unrelated dirty work).

Paste-ready Cursor prompt:

```text
Read AGENTS.md and plans/recent-directory-session-review.md. Preserve unrelated dirty work. Verify Second Brain review defaults to the full prettified report across five newest directories with three sessions each, and --details uses the same renderer. Keep JSON, privacy screening, refresh budgets, check dispositions and the archival Markdown unchanged. Run the exact automated/manual checks in the plan, report the known unrelated vault-inventory failure separately, and preserve the scoped install rollback. If authorized to commit, include the matching plan/docs/tests and incident learning in the same focused Conventional Commit.
```

Final full-report evidence: fresh session suite 105/105 passed, exit 0. Fresh broader Second Brain suite 355/356 passed, exit 1 solely for test_exact_sanitized_tree_exists_without_unapproved_files and the existing 05 Daily Notes/2026-07-22.md. Source and installed disposable PTY smoke exit 0. The exact installed `second-brain sessions review --limit 1 --refresh-limit 0 --details` opens the prettified report in bat/less; Space navigation and q exit 0 were verified in a real PTY. Both changed installed files match current source bytes. No remaining feature work or blockers; existing privacy exclusions/concurrent-source freshness warnings still apply. Rollback uses the two files and manifest at the recorded backup path. The native title endpoint retains its previously documented transport outage; the known conversation subject remains this review improvement.

Clarification follow-up: the zero-budget smoke examples intentionally leave missing recaps pending. Updated usage and existing smoke expectations to explain removing --refresh-limit 0 for generation and rerunning after q because the pager is a snapshot. Verified the default budget expression in session_review.review (three per directory, capped at twenty); scoped documentation diff check passes. No runtime changes or additional inference were needed.

## Follow-up: press r to refresh

Add a pager-local r binding that closes the old snapshot, re-runs the same directory/session selection, updates missing/stale recaps, and reopens the full report. q exits normally; Space/search remain less controls. Explicit positive refresh budgets persist, but r intentionally replaces zero-preview budget with the normal bounded generation budget. Unchanged recaps never incur inference; --all remains capped at twenty refresh attempts per cycle. JSON/plain/no-pager/redirected output do not become interactive. Keep progress flowing during refresh and release state locks before viewing. Use a private temporary less keymap and explicit refresh signal, never interpolate report content into shell commands or modify the user's global less configuration. Preserve baseline dirty work; install verified changed files only with rollback.

- [x] Observe RED for repeated refresh cycles, selection/budget preservation, failure recovery and q exit.
- [x] Implement private key binding and report refresh loop with progress.
- [x] Extend disposable real bat/less PTY smoke to change a fixture source while open, press r and observe the new output.
- [x] Update README, guide, smoke checks and verification evidence; run regression and broader checks.
- [x] Install verified CLI changes with rollback and test installed interactive refresh.

Refresh-key investigation: independent disposable PTY probes confirm less590 supports `r quit R` (exit82) but installed bat/batcat discard pager status. A private Python wrapper reports all less exit statuses through a temporary control file; report content is only passed on stdin. Both direct less and bat refresh signals are handled. q, normal paging/search, interruptions and readable fallback remain. Startup native title tool still returns the documented transport outage; requested title Add session review refresh could not be applied. No new title retry mechanism added.

RED: CLI loop tests failed for absent repeated review, zero-budget override and quota recovery; real PTY fixture failed because r did not discover a newly added work session. Inner pager failure regression also failed before adding status propagation. GREEN evidence and activation follow below.

Refresh-key verification: 109 session regressions pass; broader Second Brain359/360 pass with only the known existing July22 Daily Note inventory failure. Source and installed smoke --pager-check exit0, now also asserting the visible controls prompt and verifying r rediscovery plus recap generation on new fixture work after zero preview. Independent review's colon-prompt defect received a failing PTY assertion and grammar-safe correction; tracked incident learning/ledger check is recorded with the fix. Only cli.py was installed, hash verified; rollback /tmp/refresh-key-review-rollback-klom5bng. No configuration/timer changes, new package module, staging or commit. Old open processes must be reopened once to load the new key binding.

Refresh-key handoff: atomic plan is tests → private less binding/status bridge → review loop → docs/runtime verification → scoped activation. Exact automated checks are the session regression and broader Second Brain commands already listed, plus source/installed `python3 -B tests/scripts/second_brain_sessions_review_check.py [--runtime-dir scripts] --pager-check`; README gate and scoped diff check. Manual checks: reopen review, press r after --refresh-limit0 to enable recaps, press r with positive budget to retain it, use Space/search and q, and verify JSON/plain/no-pager remain noninteractive. Updated README, usage guide and Action/Expected smoke entries. Suggested future commit `feat(second-brain): refresh session reviews with r` must include this matching plan, docs/tests and incident learning. Cursor prompt: Read this plan and AGENTS; preserve unrelated dirty work. Re-run the exact source/installed PTY and regression checks; verify r reloads selected directories and recaps, zero preview enables normal generation only after r, explicit positive budgets persist, unchanged recaps are reused, and q/JSON/plain/fallback remain safe. Include matching docs/plan and incident learning with any authorized scoped commit.

Installed native command verification: real `second-brain sessions review --limit 1 --refresh-limit 0` shows the full report and visible `r refresh recaps` help in bat/less; q exits0. Live inference stayed disabled for this native metadata check; installed disposable PTY independently verified actual r discovery/generation. Final source/live cli.py bytes match, README gate passes and scoped diff check exits0. All refresh-key checklist items complete; no feature blockers remain. No commit was requested for this follow-up.
