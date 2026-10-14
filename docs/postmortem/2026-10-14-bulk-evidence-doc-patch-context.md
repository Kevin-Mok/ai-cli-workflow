# Bulk Evidence Documentation Patch Context Failure

This postmortem records why one combined documentation update did not apply.

## Symptom

On 2026-10-14, a single patch spanning the smoke checklist, lessons, ExecPlan,
and harness progress failed because one ExecPlan context line did not match.

## Impact

The atomic patch made no changes. The underlying evidence and implementation
were unaffected, and nothing was committed or pushed.

## Evidence

- The patch tool identified the unmatched line in the ExecPlan progress list.
- The requested updates covered four independent locations with different
  surrounding context.

## Root Cause

The combined patch assumed one long-lived context block across four documents.
The ExecPlan progress wording had diverged enough that the patch tool correctly
rejected the atomic operation.

## Resolution

The smoke checklist, lessons, ExecPlan, and harness progress were patched
separately using freshly read context.

## Verification

Each document now contains its intended task-specific section or updated
checklist/evidence entries, and the earlier atomic failure left no partial edit.

## Current Status

Resolved.

## Next Steps

No code follow-up remains. The postmortem-memory ledger update is intentionally
deferred because that canonical ledger is outside the user-authorized folder.
