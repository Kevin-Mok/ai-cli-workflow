# Codex picker Toronto timestamps

Show recent-session activity in America/Toronto in both the picker row and preview.

## Context and decisions

The raw UTC timestamp is currently printed by scripts/codex_search_recent.py.
Use zoneinfo, preserve seconds and fractional precision, and display offset plus
EDT/EST. Preserve stored timestamps, chronological sorting, UUIDs and resume behavior.
Invalid or missing values retain the existing escaped fallback. Only picker display
is in scope. Existing dirty files and untracked implementation are protected.
Postmortem lookup: timestamp timezone UTC Toronto returned unrelated quota and
spreadsheet findings; none applies to this rendering defect. Intentional RED is exempt from incident recording. A later broad /tmp lookup
hit private-directory permissions; exact-path inspection succeeded. Diagnostic
ledger inspection assumed the wrong key, corrected before ledger mutation. Both
are recorded in docs/postmortem/2026-10-08-codex-picker-tmp-lookup.md.

## Checklist

- [x] Capture git status and inspect renderer and existing tests.
- [x] Observe RED for exact supplied timestamp, winter offset and day rollover.
- [x] Add minimal display conversion and document picker timezone.
- [x] Run focused and Codex-search regressions, install module and verify live bytes.

## Risks and rollback

Requires the system America/Toronto timezone database. Revert only this task's
renderer/test/docs hunks and reinstall that module; preserve pre-existing work.
No commit or push requested. This plan belongs with these hunks in any later commit.

## Verification and review

RED: the defining unittest failed all three cases with raw UTC output, exit 1.
Minimal conversion now applies only to recent picker rows/previews. Manual: run crg; activity row and preview should agree on Toronto time,
including EDT or EST; Enter must still resume the selected session.

## Handoff

Cursor prompt: Finish plans/codex-picker-toronto-time.md, preserve unrelated work,
run python3 -m unittest discover -s tests -p 'test_codex_search*.py', then check crg
row/preview timezone and resume. Suggested commit: fix(codex): display picker activity in Toronto time.

GREEN: python3 -m unittest discover -s tests -p 'test_codex_search*.py'
ran 90 tests in 16.437s, exit 0. Includes actual fzf/resume regression fixtures.
chezmoi apply --force -- /home/example/scripts/codex_search_recent.py: exit 0.
Fresh installed-module byte comparison and real render_session row/preview
assertions passed for supplied timestamp, exit 0. No tracked configuration
changed, so activation applies only this module; no broad refresh needed.
Documentation describes the verified picker scope; ordinary search output
retains its existing timestamp format. Interactive personal-history inspection
was not run; synthetic picker integration and installed rendering are verified.

## Compact timestamp follow-up

User requested the shortest human-readable timestamp after viewing picker rows.
Use `Oct 8 12:24` (Toronto, 24-hour clock) in rows; retain full year, precision
and offset in the preview for disambiguation of historical sessions.
- [x] Observe updated row regression RED (three expected long-versus-short failures, exit 1).
- [x] Implement compact row and update docs.
- [x] Run regression suite and activate installed module.

Compact follow-up GREEN: 90 Codex-search tests passed in 14.907s, exit 0;
git diff --check passed. Exact-target chezmoi apply exited 0 and installed bytes
match source. Installed screenshot fixture displays `Oct 8 12:24` in the row
and preserves full Toronto timestamp in preview; assertions passed, exit 0.
No configuration changes, commit or push. Reopen crg for updated rows.

## Authorized delivery

On 2026-10-08 the user invoked commit-session and explicitly approved including
the pre-existing recent-picker implementation and required modules/tests. The
scope helper returned unsafe because it could not observe function-wrapped
writes; direct conversation write evidence plus that approval establishes scope.
Session: 01a11c3a-cb20-7082-94dc-2750703a5978. Preserve all unrelated hunks in
README, aliases, smoke tests, learning ledger and lessons. Include associated
plans, specification and nine reviewed incident reports with this implementation.

Fresh working-tree validation: 91 Codex tests passed in 17.356s, shell launcher
regression passed. README recruiter-sync: pass_no_change. Required scoped
refresh-config: REFRESH COMPLETE, exit 0; log
/tmp/refresh-config-20261008-123924-1658082.log. Exact picker modules applied,
live Codex/Git snapshots retained and shortcuts reloaded. Index scope audited
against explicit manifest, excluding unrelated features/configuration.
Commit subject: feat(codex): browse recent sessions with compact previews.
Push destination: origin/main. Local rollback is a normal future revert; no
history rewrite. No external model smoke request repeated during delivery.

Exact staged-code snapshot verification: 91 tests passed in 18.498s, exit 0.
All nine related postmortem learning checks passed. Shared-file staged hunks
were independently checked to exclude Second Brain, directory-size, backup and
unrelated alias changes. Final staged whitespace check passed.
