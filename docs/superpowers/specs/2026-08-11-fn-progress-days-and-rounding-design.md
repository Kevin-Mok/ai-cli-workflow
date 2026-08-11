# fn-progress Days and Rounding Design

## Goal

Make the active C7S3 `fn-progress` output show both completed and remaining
whole days, and round its percentage to the nearest whole number.

## Decision

Keep the existing schedule and pre-season/ended branches unchanged. In the
active branch, derive elapsed and remaining days from the existing elapsed and
total seconds, then print one concise line in the form `⏱️ Days: 59 elapsed,
15 remaining`. Replace the current ceiling calculation with nearest-integer
rounding, so a calculated `89.9%` displays as `90%`.

## Alternatives Considered

- Separate elapsed and remaining lines would be more verbose without adding
  useful information.
- A compact `59/74 days` form would not explicitly identify the two counts.

The combined labeled line is the clearest minimal output change.

## Validation

Extend the existing Fish helper regression test to freeze an active season
timestamp and assert the rounded percentage plus both day counts. Retain the
existing schedule and active-branch assertions, and update the reusable smoke
test expectation to mention the new output.
