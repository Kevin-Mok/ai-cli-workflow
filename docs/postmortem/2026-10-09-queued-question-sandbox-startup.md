# Queued-question notification: sandbox startup failure

The default runner failed before inspecting the queued-question audio path. Use the scoped approved execution workaround to continue the authorized change; host sandbox repair is outside this task.

## Symptom and impact

Initial pwd and skill-reading commands exited 1 before their bodies ran: bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted. No files changed. Approved source reads and git status subsequently exited 0. Existing dirty changes are protected.

## Lookup, applicability, and evidence

Searched bwrap loopback Failed RTM_NEWADDR with the tracked postmortem-memory helper. Reviewed ext-sandbox-loopback and local-sandbox-loopback-approved-route: verified_workaround, scope workaround. Identical errors across independent harmless launches establish the startup boundary. The approved require_escalated route executes the same scoped commands successfully; no security settings changed.

## Status, cause, resolution, and next steps

Scoped alternate execution verified. Default Bubblewrap loopback initialization remains unresolved; the underlying host policy was not investigated. Continue the queued-question task using reviewed scoped commands. No new reusable learning: the two existing findings cover this symptom and workaround. Register this report with an explicit no-new-learning decision and run the targeted check.

## Helper-path inspection failures

A source read assumed scripts/executable_refresh-config; sed reported no such file. A compact private-context lookup assumed personal_context.py; Python exited 2 for a missing file. No files changed from either failed lookup. Before correcting paths, search missing helper assumed path matched ext-optional-path-discovery and local-discover-paths-before-reads. Read their applicability and used rg --files to discover actual paths: dot_config/fish/functions/refresh-config.fish and the installed context_store.py helper. These are inspection assumptions, not notification defects. No new reusable learning; existing discover-before-read guidance applies.

Independent read-only investigation assumed generated schemas under a v2 subdirectory; rg exited 2 for missing paths. No files changed. Existing discover-before-read guidance applies; schema inventory identified the actual root-level files before further inspection.

## Existing synthesis-timing regression failure

The focused notification/speech suite ran 67 tests in 20.905s, exited 1, with one failure in test_synthesis_overlaps_clip_but_title_plays_after_once: synthesis end index 3 was not greater than clip end index 4. The unchanged sound implementation and this task's untouched existing test assert a timing relationship between independent fake subprocesses. New question tests (10), existing bridge tests (15), and changed-script type checking passed. Inspect the fixture and reviewed timing guidance before rerunning; do not weaken playback-order coverage. Full regression remains unverified pending investigation.

## Fixture root cause, resolution, and verification

Confirmed fixture race: fake mpv touched clip-ended before appending its clip-end event. Piper could observe the marker and log synthesis end first. Deliberately adding a 50ms scheduling gap between marker and event reproduced the original failure. Move the event log before publishing the marker, preserving every assertion and all pre-existing test changes. The same scheduling-gap reproducer now passes. Fresh focused notification/speech suite: 67 tests, 20.126s, exit 0; intentional audio-failure fixtures emit expected diagnostic warnings. New question suite: 11 tests, exit 0. Changed bridge/probe type checker: zero errors/warnings. Private Dunst: one test, exit 0. The unchanged audio implementation was not the cause.

Learning: local-audio-fixture-marker-ordering records this verified code-scope fixture correction and its deterministic reproducer. Existing sandbox and discover-before-read findings remain applicable workarounds; default sandbox repair remains outside scope. Native blocking/async fake-provider probes confirmed actual hook delivery. Installation/trust and live-session acceptance are recorded in the active question plan. No commit or push requested.

## Concurrent whitespace warning at final handoff

Final full-repository git diff --check exited 2 for a new blank line at EOF in dot_agents/skills/postmortem-memory/references/editing-shell-transport.md:232. This task did not edit that file; its content changed concurrently while working. Preserve it. Lookup concurrent dirty whitespace diff check matched local-authored-markdown-whitespace; its repair applies to authored task files, not this unowned change. Also reviewed local-stale-preservation-baseline, which requires preserving current concurrent content and separately verifying scope. Run the diff check restricted to this task's files; report the repository-wide warning without claiming all-repository whitespace cleanliness. No new reusable learning beyond those findings.

## Session commit companion type-check failure

Commit-session extraction moved the question probe into a new session-owned file to exclude the pre-existing untracked completion probe. Twelve runtime question tests passed, but basedpyright reported event possibly unbound at smoke_codex_question_events.py:82:50 because assignment was conditional on known case membership. The CLI choices establish valid runtime inputs, but the function accepts arbitrary strings. Initialize the event dictionary before the branch and rerun type and runtime checks. Lookup possibly unbound event conditional initialization found no specific reusable remedy beyond existing Python integration guidance. No new reusable learning: a local conditional-initialization oversight, not a native hook defect. No commit occurred before correction.

The first rerun of the temporary commit-version preparer stopped at an assertion because its earlier resolver replacement was already applied. No preparer writes executed during that rerun, and the probe type error remained. Current source proves the replacement is present; make that temporary preparation step accept the already-applied state, then rerun. This is a scoped authoring-helper idempotence oversight; no new reusable learning or product defect.

A prospective ledger check mistakenly treated the partial session overlay as a complete knowledge directory. It exited 2 because untouched reference files were absent from the fixture. This does not establish a repository knowledge defect. Verify using a complete HEAD archive with the session overlay, not the partial overlay alone. Lookup missing reference partial fixture was reviewed; this is fixture assembly only, with no new reusable learning. The companion initialization correction now type-checks with zero errors/warnings and all twelve runtime question tests pass.
