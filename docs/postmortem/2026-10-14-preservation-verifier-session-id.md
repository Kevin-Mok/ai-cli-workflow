# Preservation Verifier Session ID Was Not Retained

This postmortem records why the first independent metadata/topology verification
run produced no readable result.

## Symptom

On 2026-10-14, the verifier exceeded the command runner's 30-second yield. The
wrapper printed only the absent output/exit fields instead of the returned
session identifier. By the next process check, the verifier had exited, so its
result could not be retrieved.

## Impact

No preservation claim could be made from that run. The verifier was read-only;
the repository, refs, files, and remotes were unchanged.

## Evidence

- The command waited just over 30 seconds and returned no exit status.
- A subsequent process inventory showed no verifier or child Git process.
- The wrapper had not serialized the complete command result, so the session
  identifier was unavailable for polling.

## Resolution

Every subsequent run used an early yield, serialized the complete command
result, and retained the session identifier for polling.

## Verification

The final verifier completed with status `pass`: 688 retained historical commits
matched original author/committer dates and approved message transformations,
with zero topology mismatches.

## Current Status

Resolved.

## Next Steps

No code follow-up remains. The postmortem-memory ledger update is intentionally
deferred because that canonical ledger is outside the user-authorized folder.
