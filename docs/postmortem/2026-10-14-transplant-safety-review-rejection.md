# Transplant Safety Review Rejected Destructive Reset

This postmortem records why the first attempt to run the final source-repository transplant was rejected before execution and how the transplant preflight was strengthened.

## Symptom

The elevated transplant request was rejected because the proposed hard reset would replace a source checkout containing pre-existing media paths before the script itself proved that their bytes were recoverably backed up.

## Impact

The first transplant did not start. No source ref, worktree file, remote, reflog, Git object, or LFS payload changed during the rejected attempt.

## Evidence

- The command runner rejected the process before creation.
- The original source still reported its original ref graph and private remote afterward.
- A protected-media directory already held byte-for-byte copies, but the rejected script did not validate them as part of its own preflight.

## Current status

Resolved. The revised preflight and transplant completed without a push.

## Root cause

The first transplant relied on evidence collected earlier in the session rather than making protected working-tree verification an atomic precondition of the destructive reset.

## Resolution

The revised script required the exact 35-path source status set, byte-matched all four media paths to protected backups, copied every current changed path to a separate recovery overlay, and verified the original private bundle before any fetch or reset. It then installed the sanitized refs, removed the private remote, expired reflogs, pruned Git objects, and pruned LFS payloads.

## Verification

- The transplant installed 18 local heads and a 689-commit all-ref graph at the expected public tip.
- The source remote inventory, LFS path inventory, LFS object-file inventory, reflog inventory, replace-ref inventory, and unreachable-object inventory are empty.
- The final source privacy audit passed across 689 commits and 5,175 blobs with zero findings.

## Follow-up

- Put preservation assertions inside destructive delivery scripts instead of relying only on conversational evidence.
- Keep recovery material only until the final report and verification are complete, then remove it with the other sensitive temporary artifacts.
