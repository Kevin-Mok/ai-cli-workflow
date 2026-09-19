# Now-playing title eligibility — 2026-09-19

## Symptom and impact
Long Chrome/YouTube titles crowded the i3 bar. The user ultimately requested
a lenient Artist - Title filter instead of truncation.

## Evidence and root cause
The helper accepted any Chrome title and emitted it in full. Live song metadata
was separate `Logic` / `I'm Gone`; requiring a dash in the raw title would hide it.

## Resolution
Browser media now qualifies with artist metadata or a title matching
`\S.*[-–—].*\S`. Spotify remains eligible without artist metadata. Filtering at
metadata read precedes selection and click validation; original metadata is retained.
Nonmatching Chrome allows another eligible player; no player clears text/cache.
No truncation is retained. Non-songs may qualify, and songs without artist metadata
or a separator cannot be identified. Qualifying long labels can still overflow.

## Investigation interruptions
Sandbox startup failed before execution with `bwrap: loopback: Failed RTM_NEWADDR:
Operation not permitted`; approved elevated execution restored access. Discovery
reads guessed config paths without `.tmpl` and one nonexistent optional doc; file
inventory resolved the source. No modifications resulted from failed reads.
The superseded shortening attempt had two suffix-budget fixture mismatches in
its first GREEN run. Its code/tests were removed after the user's scope change,
before deployment; they are not part of the final implementation.

## Verification and current status
Resolved and deployed. RED: 6 expected assertions across 29 tests exposed missing
filtering, fallback and cache clearing. GREEN: all 29 tests pass; existing Spotify
and desktop layout shell regressions pass. `git diff --check` passes.
`fish -ic refresh-config` returned REFRESH COMPLETE, exit 0; log inspected and no
unrelated tracked changes resulted. Installed helper matches source byte-for-byte
and emits Logic - I'm Gone / I'm Gone / #c9b1c0. Independent review confirmed
selection and click identity safety. Playback/queue were not modified.

## Follow-up
Use the [desktop smoke checks](../smoke-tests.md) for interactive media transitions
and controls. Matching format is deliberately permissive, not music classification.
See the [implementation plan](../../plans/now-playing-width.md) for scope and rollback.
