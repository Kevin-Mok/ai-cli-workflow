# fn-progress C7S3 Season Date

## Purpose And Observable Outcome

Correct the `fn-progress` Fish helper so that, on August 4, 2026, it reports
Chapter 7 Season 3 as active with its June 6 start and August 19 end date.

## Current Context, Relevant Files, And Scope Boundaries

- `dot_config/fish/functions/fn-progress.fish` contains the stale C7S2 label
  and an August 10 end timestamp.
- `tests/test_fn_progress.sh` will provide a deterministic Fish-level
  regression test using a mocked `date` executable.
- `docs/postmortem/` records the incident; `docs/smoke-tests.md` records the
  real helper verification.
- Pre-existing dirty files are protected, including `README.md`, Fish
  configuration, Second Brain sources, docs, and existing plans. This change
  must not stage or edit them.

## Assumptions And Decisions

- The user confirmed that this schedule is C7S3, launched June 6, 2026, and
  ends August 19, 2026.
- The existing date-only convention represents local midnight:
  `2026-08-19 00:00:00`.
- Keep the current progress calculation and output structure unchanged.
- Out of scope: dynamic online schedule discovery, changes to other Fortnite
  helpers, and unrelated cleanup.

## Implementation Checklist

- [x] Capture initial Git status and identify the stale literal root cause.
- [x] Confirm with the user that the schedule should be labeled C7S3.
- [x] Add a deterministic failing Fish regression test for the active C7S3
  date range.
- [x] Run the test and record its clean RED result.
- [x] Update the function's label and end timestamp only.
- [x] Correct the C7S3 start timestamp and extend the regression test.
- [x] Run the focused test and syntax check; record GREEN evidence.
- [x] Add the smoke-test entry and linked incident postmortem.
- [x] Run changed-file, diff, and runtime verification; record results.

## Risks, Edge Cases, And Rollback

- A date-only end remains subject to future schedule changes; the single
  literal is the rollback point.
- The regression test mocks timestamps so it is deterministic and does not
  depend on the host clock or network.
- Rollback is limited to restoring the prior label/date line; no external
  state changes are required.

## Verification

- RED: `bash tests/test_fn_progress.sh` must fail against a function that
  still contains the June 10 start because its expected June 6 output is
  absent.
- GREEN: the same command must pass after the minimal update.
- Syntax: `fish -n dot_config/fish/functions/fn-progress.fish` must exit 0.
- Manual runtime: source the function with a deterministic mocked `date` and
  confirm it prints C7S3, August 19, and a progress line rather than `ended`.

## Progress, Verification Evidence, And Review Notes

- Root cause: the helper hard-codes `SEASON_END` as August 10 and labels the
  output `C7S2`; the user confirmed the intended C7S3 August 19 schedule.
- Initial RED fixture correction: the mock initially omitted Fish's `date +%s`
  current-time invocation. The fixture now returns a deterministic timestamp
  (`150`) between the mocked start (`100`) and intended end (`200`); the helper
  remains unchanged.
- The fixture also handles the zero-argument display-time call without reading
  an unset positional parameter.
- It maps the stale August 10 value to `140`, before the mocked current time,
  so RED demonstrates the premature ended branch cleanly.
- RED evidence: `bash tests/test_fn_progress.sh` exited 1 and printed
  `Fortnite C7S2 has ended! (Ended on 2026-08-10 00:00:00)` for mocked August
  4 time, proving the stale schedule reached the premature ended branch.
- Implementation update: `fn-progress` now uses the confirmed C7S3 label and
  `2026-08-19 00:00:00` end timestamp; the calculation is untouched.
- GREEN evidence: `bash tests/test_fn_progress.sh` exited 0 after the update.
  `fish -n dot_config/fish/functions/fn-progress.fish` exited 0. The real
  `fish -c "source dot_config/fish/functions/fn-progress.fish; fn-progress"`
  output on August 4 showed C7S3, an August 19 end, and 79.9999% progress.
- Final review: `git diff --check` exited 0. `docs/smoke-tests.md` includes
  pre-existing unrelated Second Brain and rsync additions; only the C7S3 Fish
  Helpers entry is part of this work.
- Deployment evidence: `chezmoi diff ~/.config/fish/functions/fn-progress.fish`
  showed only the C7S3 label/date changes before deployment. Targeted
  `chezmoi apply ~/.config/fish/functions/fn-progress.fish` completed, then
  the installed function printed C7S3, August 19, and active 79.9999% progress;
  the subsequent target diff was empty.
- Review target: the diff must be limited to the helper, its focused test, this
  plan, and incident/manual-verification documentation.
- Follow-up root cause: the first correction retained the stale June 10 start
  literal. The user supplied the authoritative C7S3 June 6 launch date; the
  test now requires that date before the function is updated.
- RED evidence for the follow-up: `bash tests/test_fn_progress.sh` exited 1
  and showed `Season Start: 2026-06-10 00:00:00`, omitting the required June 6
  start. The implementation now sets `SEASON_START` to `2026-06-06 00:00:00`.
- GREEN and deployment evidence for the follow-up:
  `bash tests/test_fn_progress.sh`, `fish -n dot_config/fish/functions/fn-progress.fish`,
  and `git diff --check` all exited 0. A targeted `chezmoi apply
  ~/.config/fish/functions/fn-progress.fish` completed; the installed function
  then printed the June 6–August 19 C7S3 schedule and 80.9999% progress on
  August 4. The target diff was empty after deployment.
