# Live Guardian recap titles

Replace generic Guardian review labels with AI recap headlines as recaps arrive,
then verify filtering, selection and exact resume in the real terminal picker.

## Scope and decisions

Only an exact Guardian review title (case-insensitive, surrounding whitespace
ignored) uses a nonblank string recap headline. Ready, stale and generating
cached recaps may supply it. Meaningful native titles remain unchanged; preview
retains Original title and status. Do not rename saved conversations or change
generation policy. Without a headline, keep the native title until one arrives.

Publish the current headline on every recap update. Preserve the query and
highlighted input index while the session still matches. A query matching only
the old generic title re-filters normally; clearing it reveals the new title.
Enter with zero matches resumes nothing. Keep original UUID/directory identity.
No external GET/query then POST gate, hidden search aliases or fzf upgrade.

Default mode has no mode-switch tool; this plan records the required decisions.
Initial Git status was captured and extensive unrelated work remains protected.

## Context and revised decision

The earlier implementation froze titles with row_titles.setdefault. Static
rendering passed, but the user's repeated screenshot rejected that policy.
Read-only actual cache and active-picker inspection found ready/stale headlines
beside rows still labelled Guardian review; installed/source bytes matched.
The fixed-opening policy and its earlier verification are superseded.

Postmortem lookup used Guardian/fzf/headline/query symptoms. Existing
local-fzf-ui-stream-and-resume-fixture applies to real UI and safe UUID checks,
but does not establish headline propagation. fzf 0.44 searches transformed
--with-nth text; independent review confirmed normal re-filtering is required.

## Atomic work

- [x] Diagnose actual cache/active rows and record living incident.
- [x] Observe live terminal RED: Guardian row stayed generic after the AI headline arrived (exit 1).
- [x] Remove frozen title state and publish current recap titles.
- [x] Verify cached/live updates, stable-directory selection and old-title re-filter to zero matches.
- [x] Update README, operator guide, smoke checks and the corrected local lesson.
- [x] Activate only the picker module and verify installed real-terminal behavior.
- [x] Independently review final code/tests and register incident learning.
- [x] Complete targeted learning-ledger check and final whitespace review.

## Evidence and review

- python3 tests/scripts/codex_recent_live_check.py: exit 0; query, selection,
  Ctrl-G, cancellation and worker cleanup passed. No provider calls.
- python3 -m unittest discover -s tests -p 'test_codex_search*.py':
  93 tests passed in 24.708s, exit 0.
- chezmoi apply --force -- /home/example/scripts/codex_search_recent.py: exit 0;
  installed bytes match source. The full real-terminal synthetic fixture also
  passed after importing /home/example/scripts/codex_search_recent.py, exit 0.
- Independent final review found no blocking resume/selection issues. Historical
  seen_rows validates a displayed row if Enter races reload; UUID stays trusted.
- Commit verification superseded the cached-mode scheduling assumption: synthetic
  startup overwrote ready state. The fixture now preserves cached state and
  asserts cached titles/exact resume with zero workers. The real terminal check
  and all 98 search tests pass in 38.034s, exit 0. See the related living report
  and the delivery milestone in plans/codex-title-progress.md.

- Targeted postmortem-memory check: exit 0, no errors, current hash/alias covered
  by local-picker-live-headline-integration; git diff --check: exit 0.

## Manual check and limits

Close any picker opened before installation, then run crg once to load the code.
Use a directory query, select a missing-recap Guardian row and request Ctrl-G.
Its headline should replace the generic label live with the same UUID selected.
Repeat with only Guardian as the query: the completed row may disappear; clear
that query to see its new title. Enter with no matches resumes nothing.

A missing/failed recap cannot provide a title. Old processes retain their loaded
code until reopened. No real inference was started by development verification;
actual model generation policy is unchanged. No configuration changed, broad
refresh, saved-conversation rename, commit or push was performed.

## Handoff and rollback

Automated: run the two commands above from /home/example/linux-config; no sudo.
Docs: README.md, docs/codex-session-search.md and docs/smoke-tests.md reflect live
updates. Incident: docs/postmortem/2026-10-08-guardian-titles-frozen-after-recap.md.
Rollback only these task hunks, then reapply the exact picker module.

Cursor prompt: Review plans/guardian-recap-titles.md and the live Guardian title
changes, preserve unrelated work, run both regression commands, and verify exact
UUID resume plus safe zero-match Enter before any requested commit.
Suggested commit: fix(codex): update Guardian recap titles live.

## Follow-up: exact 13:44 row

- [x] Capture current Git status and inspect the exact reported UUID safely.
- [x] Compare actual authenticated fzf state with current recap metadata.
- [x] Explain generation timing in the operator guide and manual smoke check.
- [x] Register the report's reviewed hash and final targeted check.

The picker opened at Toronto 13:44:06.647; the reported row's recap cache was
written at 13:44:34.641, approximately 28 seconds later. Actual fzf GET state
shows its descriptive AI headline in title field four and ready/partial status.
Installed/source bytes match. No extra inference, selection mutation or code
change was required. Screenshot capture time is unknown, so the state at capture
cannot be reconstructed exactly; current display confirms this row updated.
Other rows can still be queued, outside the newest-20 batch, disabled or failed.
Independent SummaryManager review confirms those limits; preserve generation
policy and the verified live-update implementation.

Reviewed incident: docs/postmortem/2026-10-08-guardian-title-generation-delay.md.
Lookup Guardian recap live title matched local-picker-live-headline-integration;
its runtime guidance applies directly. No broad regression rerun is needed for
this documentation clarification; the exact live display is fresh evidence.

Targeted report check and git diff --check both exited 0; no coverage errors.
