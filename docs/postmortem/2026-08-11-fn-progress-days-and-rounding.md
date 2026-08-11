# fn-progress Reported Fractional Ceiling Progress

## Symptom

`fn-progress` printed a fractional ceiling-style percentage such as
`89.9999%` and did not show how many season days had elapsed or remained.

## Impact

The helper's active-season summary was harder to scan and did not match the
requested whole-number progress display.

## Evidence

The deterministic Fish-level regression test froze progress at 89.9% and
failed against the old output, which printed `89.9999%` with no day line.

## Root Cause

The helper added `0.9999` after integer division in `bc`, intentionally
producing a decimal ceiling-like value, and never derived day counts.

## Resolution

The helper now calculates complete elapsed and remaining days from its
timestamps, prints one labeled day line, and adds half the duration before
integer division to round the percentage to the nearest whole number.

## Verification

- `bash tests/test_fn_progress.sh` exercises the real Fish function with a
