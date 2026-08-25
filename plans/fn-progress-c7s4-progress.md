# fn-progress C7S4 Progress

## Purpose And Observable Outcome

Report active Chapter 7 Season 4 progress for the August 20 through November
1, 2026 schedule, with labeled whole days and a nearest-whole percentage.

## Current Context, Relevant Files, And Scope Boundaries

- `dot_config/fish/functions/fn-progress.fish` and its deterministic shell
  test contain the C7S4 implementation.
- `docs/smoke-tests.md` now has the matching C7S4 manual expectation.
- Completed C7S3 plans remain historical; no schedule lookup is in scope.

## Assumptions And Decisions

- The fixed C7S4 dates in the current source are authoritative for this change.
- The two August 24 incident records remain with the implementation commit.

## Implementation Checklist

- [x] Capture the dirty worktree before documentation changes.
- [x] Update the C7S4 helper, regression, incident records, and smoke check.
- [x] Run final focused verification and refresh tracked configuration.

## Risks, Verification Evidence, And Review Notes

- Rollback restores the prior helper and matching regression; no external state changes.
- Automated: `bash tests/test_fn_progress.sh`, `fish -n`, and `git diff --check`.
- Manual: source the installed helper during C7S4 and inspect dates, days, and percentage.
- Evidence: `refresh-config` printed `REFRESH COMPLETE` with exit 0.
- Evidence: `bash tests/test_fn_progress.sh`, `fish -n`, and `git diff --check`
  exited 0 on 2026-08-25.
- Manual evidence: the installed helper reported C7S4, August 20 through
  November 1, `5 elapsed, 67 remaining`, and `8%` on 2026-08-25.
