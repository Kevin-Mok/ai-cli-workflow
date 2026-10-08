# Guardian titles remained generic after recap generation

The recent picker should replace Guardian review labels when AI recaps become
available. Compare active rows with recap metadata, reproduce the missed update,
and verify live propagation in addition to static rendering.

## Symptom and impact

After the previous title fix, the user still saw Guardian review in the list.
Actual cache and active sessions.json contained descriptive ready/stale headlines,
but active row title fields remained Guardian review. The source and installed
module matched. Ready cache entries matched the activity times in the screenshot.
Diagnosis read metadata and headlines without starting real model requests.

## Root cause and applicability

row_titles.setdefault froze the initial fallback before generation completed.
Static render_session tests passed but did not establish live row propagation.
The fixed-opening policy preserved filtering but failed the requested behavior.
The failing real-terminal regression reported Guardian row stayed generic after
the AI headline arrived, exit 1, before the production fix.

Prior lookup used Guardian/fzf/headline/query symptoms and matched the existing
local-fzf-ui-stream-and-resume-fixture guidance. It applies to real UI and safe
resume checks, but not to this frozen display state. fzf 0.44 searches transformed
visible fields, so dynamic titles must re-filter normally. UUID remains identity.

## Resolution

Removed the frozen title map and renderer override. Each status publication
renders the current AI headline. Query text stays entered and the highlighted
session stays selected while matching; an old-title-only query can lose that row.
Enter with zero matches safely returns no selection. Meaningful native titles
and generation policy remain unchanged. Preview retains the original title.

Updated the README, operator guide, smoke checks, active plan and local lesson.
Installed only the corrected picker module with exact-target chezmoi apply.

## Verification and status

Verified fix with real-terminal synthetic runtime evidence: live Guardian and
cached Guardian scenarios retain ID2 under a directory query; a review-only query
loses each completed row, keeps its query, and Enter with no matches returns None.
Ctrl-G, cancellation, worker reaping and private temporary cleanup also pass.
python3 tests/scripts/codex_recent_live_check.py exited 0. The complete Codex search
suite passed 93 tests in 24.708s, exit 0. Installed bytes match source; the same
terminal fixture passed importing the installed module, exit 0. Independent
read-only review found no blocking selection or resume issue.

## Limits and follow-up

Synthetic workers exercise the actual fzf update path without provider calls.
Existing caches supplied diagnostic evidence; real generation was not retested.
Already-open picker processes must be closed and reopened once to load new code;
subsequent recaps update their row titles live. Missing recaps retain the native
title. Subsequent commit verification exposed a cached-fixture startup race:
its synthetic manager overwrote ready state before the initial assertion. The
corrected fixture preserves cached state and verifies opening titles/exact
resume with zero workers; all 98 search tests pass in 38.034s, exit 0. See
2026-10-08-title-progress-cached-fixture-race.md for the superseding evidence.

Register this reviewed report with local-picker-live-headline-integration in the
tracked postmortem-memory ledger and topic guidance; run the targeted check.
No commit or push was requested for this follow-up.
