# Session review displayed non-actionable inventory

Default review should show outstanding actions without hundreds of empty or Guardian review rows. Filter terminal output while retaining the complete private digest and detailed/JSON records.

## Symptom and impact
User output from `second-brain sessions review --limit 1` showed many Untitled/Guardian sessions, goals and historical blocker narratives. The prior wrapping change reduced line length but did not reduce irrelevant inventory.

## Lookup and cause
Search `session review noise guardian` found no matching filtering remedy. The renderer included every non-skipped session and printed goal/blocker context. The refresh limit bounds processing, not display. A synthetic inventory reproduced the clutter; four defining RED assertions failed for expected reasons.

## Resolution and verification
Filter default rows to sessions with open checks, excluding normalized Guardian review titles. Count displayed checks accurately and summarize omitted sessions once. Remove goal/blocker paragraphs; retain state, full Markdown details and JSON. Skipped sessions with retained checks remain actionable. Session suite passed 61 tests (exit 0); renderer smoke script passed 5 tests. Independent review found no new issues. Installed renderer tested through CLI with 100 hidden rows and one visible check, zero model calls or state changes. Rollback copy: /tmp/session-review-filter-rollback-x4vj4ifj/sessions.py.

## Status and follow-up
Verified runtime activation using controlled installed-CLI fixtures. Broader Second Brain suite ran 312 tests: 311 passed, with the same unrelated test_exact_sanitized_tree_exists_without_unapproved_files failure caused by pre-existing 05 Daily Notes/2026-07-22.md (exit 1). No vault files were changed. Keep full inventory accessible through --details; do not remove stored checks or alter inference to fix terminal clutter.
