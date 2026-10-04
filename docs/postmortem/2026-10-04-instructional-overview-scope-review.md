# Instructional overview scope review

This records an automatic approval rejection during the documentation sweep.
Clarify which source files are maintained guides, preserve pinned evidence,
then apply only the authorized editorial changes.

## Symptom and impact

Automatic approval review rejected a batch of overview edits because it
included `dot_agents/skills/metaprompt/SOURCE.md`. The earlier scope statement
excluded provenance records, so review treated this path as excluded.
The rejected command did not run and none of its files changed. A second,
separated attempt was also rejected: review required explicit user permission
for edits to source records. No further retry was attempted.

## Evidence and cause

The file combines provenance with the maintained reviewed-update and rollback
procedure. It explicitly states that the local provenance document is outside
the eight native files recorded in `UPSTREAM.json`. The blanket provenance
exclusion failed to distinguish this how-to from immutable source evidence.

## Resolution and current status

The task scope now explicitly includes this maintained procedure and five
source records whose import wording needs to acknowledge new local overviews.
Original source URLs, revisions, import dates, native content and hashes stay
intact. Unaffected guide edits continue separately. A proposed six-file patch was
prepared outside the repository for review. The user explicitly approved all
six edits, after which `git apply --check` and `git apply` completed with exit
0. The five import notes and maintenance-guide overview are now applied.

## Verification

All eight SHA-256 digests in `metaprompt/UPSTREAM.json` still match. Snapshot
comparison confirms preserved source URLs, revisions, import dates, YAML and
fenced examples. The documentation refresh completed successfully. No
unresolved approval block remains.

## Follow-up

Classify mixed-purpose files by their contents before assigning blanket path
exclusions. Keep mutable maintenance guidance distinct from pinned upstream
bytes in the coverage record.
