# fn-progress Level Pace Plan

## Purpose and observable outcome

Extend the `fnpr`/`fn-progress` Fish helper so an optional current-level argument reports the number of whole days ahead of or behind the pace required to reach level 200 by the active season end.

## Current context and scope

- `dot_config/fish/functions/fn-progress.fish` owns the active-season output.
- `dot_config/fish/config.fish.tmpl` already maps `fnpr` to `fn-progress` and needs no change.
- `tests/test_fn_progress.sh` supplies a deterministic active-season timestamp.
- `docs/smoke-tests.md` contains the reusable manual check.
- Protected pre-existing state: `dot_agents/skills/feedback-memory/feedback.log` was modified before this session and is out of scope.

## Assumptions and decisions

- A supplied level is compared proportionally against the 200-level target over the full season duration.
- The helper reports a whole-day pace difference and says `ahead` for non-negative results and `behind` for negative results.
- Calling `fn-progress` without an argument preserves its existing output.

## Implementation checklist

- [x] Record initial protected dirty state and define scope.
- [x] Add a deterministic failing regression assertion for `fn-progress 75`.
- [x] Run the focused test and confirm the assertion fails because the pace line is absent.
- [x] Add optional level-argument pace calculation and output in `fn-progress.fish`.
- [x] Re-run focused regression and Fish syntax checks.
- [x] Update the Fish helper smoke-test expectation.
- [x] Update the incident record with cause, resolution, and verification.
- [x] Run `refresh-config` and capture its result.
- [x] Review the final diff and record evidence.

## Risks, edge cases, and rollback

- Invalid or out-of-range levels are outside this narrowly requested change; existing no-argument behavior remains unchanged.
- Negative pace values must use `behind` instead of producing an incorrect `ahead` message.
- Roll back by reverting this plan, the helper, test, smoke-test entry, and incident record together.

## Verification

- RED: `bash tests/test_fn_progress.sh` must fail because the expected pace output does not yet exist.
- GREEN: the same test must pass after implementation.
- Regression: `fish --no-execute dot_config/fish/functions/fn-progress.fish` must pass.
- Manual: `fnpr 75` during C7S4 prints the normal season details plus its level-200 pace difference.

## Progress, evidence, and review notes

- 2026-08-30: Initial inspection identified the `fnpr` abbreviation and `fn-progress` implementation. The first sandboxed inspection failed before producing repository output due to `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; the elevated retry succeeded. The required incident record is included in this change.
- 2026-08-30 RED evidence: `bash tests/test_fn_progress.sh` exited 1 with the expected missing level-pace line.
- 2026-08-30 GREEN evidence: `bash tests/test_fn_progress.sh && fish --no-execute dot_config/fish/functions/fn-progress.fish` exited 0.
- 2026-08-30 refresh evidence: `fish -c 'refresh-config'` exited 0 and printed `REFRESH COMPLETE`; no additional repository files changed.
- 2026-08-30 review: `git diff --check` exited 0. The no-argument manual invocation retained the existing output and emitted no level-pace line.
