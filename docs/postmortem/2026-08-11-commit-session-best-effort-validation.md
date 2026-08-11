# Commit-Session Best-Effort Validation Repair

## Symptom

`commit-session` abandoned an otherwise safe, session-scoped commit when a
focused validation or the README recruiter gate reported a non-safety issue.

## Impact

Users could not ship safely attributed work even after the workflow had
established ownership and could truthfully repair README coverage.

## Evidence

The documentation-contract regression initially failed because the skill did
not instruct the workflow to record failed validation as a warning, repair
truthful README findings, and continue to staging.

## Root Cause

The workflow treated all validation and README-gate failures as hard stops,
rather than separating non-safety outcomes from unsafe scope or an unstageable
README repair.

## Resolution

The skill now preserves hard ownership and scope stops, records best-effort
validation failures as warnings, repairs truthful README findings inside the
safe scope, and continues after a remaining non-safety gate result.

## Verification

- The contract test asserts the warning and README-repair policy.
- The full commit-session test suite and README recruiter gate are rerun before
  this repair is committed.

## Follow-up

Keep the smoke checklist aligned whenever commit-session changes its user
visible validation or README-gate behavior.
