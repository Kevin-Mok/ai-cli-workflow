# Private digest integration validation

Integration checks caught package import and timer fixture assumptions before activation. Fix the dependency boundary and rerun the regressions.

- Symptom: isolated Second Brain command fixtures failed while importing codex_search_index, which exists beside the repository package but was not copied into the fixture. Timer validation fixture also rejected duplicate valid Environment directives and a shared runtime checkpoint module.
- Impact: ordinary CLI commands would depend on optional recap helpers at import time. No timer activated.
- Evidence: integration agent observed 34 command tests with 41 failed assertions caused by package import. Timer agent saw fixture errors; timer exact-target test requires sorted module whitelist.
- Lookup: existing paths/ownership and fixture guidance applies: inspect deployed package boundaries and fixture intent before changing behavior.
- Root cause: eager external recap imports and fixture assumptions about shared runtime deployment. A diagnostic rg glob also exited 2 because executable_refresh-config does not exist; actual refresh-config is a fish function.
- Resolution/status: move optional helper imports into parse/infer; metadata and all ordinary CLI operations stay self-contained. Sort whitelist and correct timer fixtures. Verification pending.
- Next steps: rerun package command, timer and digest regressions; verify installed runtime before activation.
- Learning: no new learning; existing dependency-boundary and fixture-contract guidance applies.

## Broader regression evidence

Second Brain suite ran 291 tests: 290 passed; existing vault fixture expected an exact file tree without the committed `05 Daily Notes/2026-07-22.md`. The implementation did not change the vault or that fixture. Codex search suite passed 89 tests. A prerequisite lookup also found no ~/.local/bin/codex (ls diagnostic); the active Codex is installed in a fnm version directory omitted from the new service PATH. The fnm default alias points to another version, so timer setup must use the actual current executable bin path rather than guessing that alias. Timer runtime-path verification is in progress. Reviewed code fixes cover all MCP tool events, normalized-text check identity, anchored regular-file sources and state rollback on Markdown export failure.

A mistakenly narrowed test discovery pattern matched no file (0 tests, exit 5); it supplied no validation evidence. The full sessions pattern is authoritative. refresh-config exited 0; live Codex config and tracked snapshot hashes matched before it and remained unchanged. Hash comparison detected concurrent .gitattributes/README/smoke edits, which are preserved as unrelated work.

Type-checking the new modules caught seven annotation/import-boundary diagnostics (including top-level sibling imports under the installed scripts entrypoint and optional cwd). Fix with explicit dynamic imports for the deployment boundary, precise generic return and narrowing; rerun before final activation verification. New timer enable exited 0, pending bounded inference/next-trigger checks.

## Metadata-first live correction

The first bounded live attempt completed successfully (1 inference attempt, 2 open checks, 375 pending sources, 237 conservative exclusions), but discovery parsed 6 GB of old history before limiting inference. The intended stop raced with successful completion; kill reported no such process. No state was lost. Revising discovery to metadata-first fingerprints and applying the invocation limit to privacy screening as well as inference. A new defining test observed 25 parsed files for --limit 1 before implementation. The first revised GREEN run exposed an empty-string boolean aggregate in stale counts; existing fixture/type boundary guidance applies. Normalize the aggregate to bool and rerun. State version 2 migrates validated version 1 private state without losing summaries or dispositions.

## Final resolution and verification

The metadata-first correction is live: one bounded refresh completed in 15.24 seconds with 1 inference attempt, private state migrated to version 2, 3 open checks, 613 queued sources, 237 conservative exclusions, and 1 partial summary. Native activity enforces the fixed initial seven-day window after candidate screening; later new/changed old sources remain eligible. Native title changes wait for changed-source screening. Previously screened safe summaries stay explicitly stale until refreshed; actual detected private use withdraws them.

Final focused digest/timer tests: 54 passed. Type check: 0 errors/warnings. Codex search regression: 89 passed. Broader Second Brain regression: 304/305 passed; the unchanged committed daily-note versus exact-tree fixture mismatch remains out of scope. Real unchanged native source check: 1 eligible summarized source, 0 inference calls, no live state modification or raw transcript copies. State directory is 0700; state, Markdown and lock are 0600. Timer enabled/active; next trigger October 7 at 16:00 EDT. Existing checkpoint remains enabled/active and deferred remains disabled/inactive. refresh-config completed successfully and live/tracked Codex config hashes remained equal and unchanged. No commit/push performed by this task.

Status: verified implementation/runtime workaround; original sandbox restriction and unrelated vault fixture remain. No new reusable learning: existing environment, fixture and dependency/path guidance applies; scaling correction is recorded in the implementation plan and operator guide. Rollback disables only the sessions timer through its helper, retaining private digest state.
