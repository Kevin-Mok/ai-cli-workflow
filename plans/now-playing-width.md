# Music-style now-playing filter

## Purpose and current scope
User replaced compact universal formatting with displaying only Artist - Title
style media. Original helper constructs that form from separate metadata, so
matching the final constructed label alone may admit non-music video channels.
User chose leniency: accept any nonempty separate artist/title metadata, or raw
titles with nonempty sides around a hyphen/en dash/em dash (spaces optional).
Spotify remains eligible without an artist. Filter before player selection so
rejected browser sessions allow another eligible browser or Spotify fallback.
No length cap, truncation or title rewriting in the final scope.

## Initial state and protected work
Initial git status was clean. No pre-existing changes. Removed only this session's
superseded shortening edits/tests. Final filter deployed with refresh-config.

## Decisions and checklist
- [x] Inspect helper, tests, bar and previous plan.
- [x] Record user change of scope; retire unshipped truncation work.
- [x] Resolve match source and define failing tests.
- [x] Implement minimal format filter without changing safe click identity.
- [x] Update README and smoke checks; run focused media/layout regressions.
- [x] Run refresh-config and verify installed result; document any deployment limit.

## Risks and rollback
A text pattern recognizes a format, not whether content is music. YouTube channel metadata and hyphenated non-song titles qualify intentionally.
Songs without artist metadata or a title separator cannot be recognized.
Long qualifying labels can still overflow: user replaced the truncation request.
Preserve original metadata in click cache. Restore only new filter and reapply to
roll back. Do not disturb playback or queue during verification.

## Verification
Automated: python3 tests/test_i3blocks_now_playing_mpris.py;
bash tests/test_i3blocks_spotify_mpris.sh; bash tests/test_desktop_display_layout.sh;
git diff --check.
Manual: matching song visible, nonmatching Chrome media hidden, supported clicks
retain safe routing, selection/fallback follows documented policy.

## Progress and review
Original shortening RED reproduced unbounded strings. First GREEN had two suffix
fixture mismatches; user superseded the approach before further changes.
RED: 29 tests ran; 6 expected assertion failures showed missing filtering, fallback
and cache clearing. Existing format/selection checks passed. GREEN: 29 tests pass; Spotify and desktop layout shell regressions pass (exit 0).
Plan Mode unavailable; this document tracks decisions in available execution mode.

## Handoff
Suggested commit: fix(i3blocks): filter media by artist-title format.
Cursor prompt: Follow this plan's final matching decision, run automated tests and
manual checks from docs/smoke-tests.md, and preserve original playback identity.

## Final verification and review
- `fish -ic refresh-config`: exit 0, REFRESH COMPLETE; full log inspected.
  Codex snapshot already current; no unrelated tracked changes resulted.
- `cmp dot_config/i3blocks/scripts/executable_now_playing_mpris /home/example/.config/i3blocks/scripts/now_playing_mpris`: exit 0.
- Installed helper outputs `Logic - I'm Gone`, `I'm Gone`, `#c9b1c0` on three lines.
  Live metadata previously confirmed separate Logic / I'm Gone fields.
- `git diff --check`: exit 0. Independent review confirmed filtering before
  selection and click revalidation preserve original identity and fallback.
- README and smoke checks match the final lenient policy. No i3 restart is needed
  for a helper-only change; the existing five-second poll reads the installed file.
- Interactive playback-switch/click smoke checks were not performed; automated
  fixtures cover selection, hidden output, cache invalidation and existing controls.
- Rollback is the four-line read_player eligibility addition plus related tests/docs;
  reapply the helper.

## Delivery contract — 2026-09-19
User invoked commit-plan-push. All six dirty paths are one coherent change: helper,
regression tests, README, smoke checks, this plan and the matching postmortem.
Commit as `fix(i3blocks): filter media by artist-title format`, then push once to
`origin/feat/ai-workflow-optimization`. No unrelated or unsafe files found.
Fresh checks: 29 Python tests pass; Spotify and desktop layout shell regressions
exit 0; README gate returns `pass_no_change`; `git diff --check` exits 0.
Interactive playback/click checks remain documented manual validation.
