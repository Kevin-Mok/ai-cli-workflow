# LFS-Disabled Status Missed The Required Flag

This postmortem records a read-only status command that still invoked a failing required Git LFS filter and the complete override used for the final preflight.

## Symptom

A source `git status --short` command disabled the LFS process, clean, and smudge values but omitted `filter.lfs.required=false`. Git therefore still treated the absent filter process as fatal and exited nonzero on the retained image path.

## Impact

The command produced no usable source-status inventory. It was read-only, and no file, ref, remote, or object changed.

## Evidence

- Git reported that the LFS clean filter failed on the retained image path.
- The earlier successful inspection contract also disabled the filter's `required` setting.

## Current status

Resolved before transplant.

## Root cause

The retry copied three filter overrides from memory but omitted the boolean that permits Git to continue without the LFS filter process.

## Resolution

Use `filter.lfs.required=false` together with empty process and identity clean/smudge overrides for read-only source-status checks.

## Verification

The corrected command returned the complete 35-path source status without an LFS error and became an enforced transplant precondition.

## Follow-up

- Reuse the exact known-good LFS-disabled status command rather than reconstructing it piecemeal.
