# fn-progress C7S3 Season Date Design

## Goal

Make the Fish helper describe the user-confirmed C7S3 schedule from June 6
through August 19, 2026 without changing its calculation or presentation
structure.

## Decision

Use the existing local timestamp convention and update the three stale
literals: the season label becomes `C7S3`, the start timestamp becomes
`2026-06-06 00:00:00`, and the end timestamp becomes `2026-08-19 00:00:00`.
A focused test freezes the effective current time between the timestamps,
verifying the active-progress path.

## Alternatives Considered

- A remote schedule lookup would reduce manual updates but adds network
  reliability and parsing risk to a simple local shell helper.
- Updating only the end date would leave a misleading C7S2 label.

The literal update is the smallest correct choice for the confirmed schedule.
