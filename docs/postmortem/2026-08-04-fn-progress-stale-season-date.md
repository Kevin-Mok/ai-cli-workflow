# fn-progress Stale Season Date

## Symptom

On August 4, `fn-progress` reported C7S2 as 90.9999% complete and used stale
June 10 and August 10 schedule timestamps.

## Impact

The helper would have declared the current season ended nine days too early,
understated elapsed progress, and displayed the wrong chapter-season label.

## Evidence

The function hard-coded `C7S2`, `2026-06-10 00:00:00`, and
`2026-08-10 00:00:00`; a deterministic Fish test reproduces the schedule
output with an August 4 current time.

## Root Cause

The schedule constants were not updated when the active season changed.

## Resolution

The helper now labels the schedule C7S3 and uses `2026-06-06 00:00:00` through
`2026-08-19 00:00:00`; its progress calculation remains unchanged.

## Verification

`bash tests/test_fn_progress.sh` runs the helper against fixed timestamps and
confirms it prints active C7S3 progress through August 18.

## Follow-Up

- Update the two schedule literals together when a season changes.
- Use the Fish Helpers entry in [the smoke checklist](../smoke-tests.md).
