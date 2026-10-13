# Notification font command environment

Inspect Dunst configuration through the approved runner, then apply and verify the font change.

## Symptom and impact
The first read-only command failed before shell startup: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. No files changed. A later inspection also assumed a nonexistent snapshot Fish function; the actual helper is `scripts/executable_snapshot-codex-config`.

## Lookup and evidence
Query: `bwrap loopback Failed RTM_NEWADDR`. Matched `ext-sandbox-loopback`, verified workaround; applicable because the failure preceded shell execution. Approved scoped execution then returned repository status and source contents, exit 0. Snapshot helper located from repository file inventory.

## Resolution and verification
Use approved scoped execution for this task. Repository inspection succeeds, exit 0; default runner sandbox remains unrepaired. Missing-path inspection corrected by reading the actual tracked Python helper, exit 0. No new learning beyond existing runner workaround and locating files before assuming paths.

## Next steps
Continue notification configuration work using scoped approved commands; preserve unrelated dirty files. Host sandbox repair is outside this task.

## Documentation edit correction
A documentation insertion assumed a single-line README table row; lookup raised StopIteration. Font/helper writes completed before the exception; tests passed. Inspected README structure and used an additive subsection instead. No new reusable learning beyond grounding edits in actual source structure.
