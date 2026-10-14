# Reused Binary Path Enumeration Gap

This report records a large binary that remained after an exact-path history
filter because the same blob was reachable at more than one path.

## Symptom

On 2026-10-14, the post-filter binary inventory contained 259 PNG blobs instead
of the expected 258 generic small images. The all-object text scan itself passed
with zero findings.

## Impact

One visually reviewed large image remained reachable under a second path. No
source-repository refs had yet been replaced, and the rewritten clone remained
isolated.

## Evidence

- The first inventory contained 264 images: six large and 258 small.
- Seven exact paths (six large-image representatives and one audio path) were
  removed across history.
- The second inventory contained no audio but still contained 259 PNG blobs.
- `git rev-list --objects` supplies a representative path for each object; it is
  not a complete object-to-all-paths mapping.

## Root Cause

The temporary manifest was built from `git rev-list --objects --all`, so a blob
reused at multiple paths contributed only one path to the drop set.

## Resolution

Enumerate every unique commit tree with `git ls-tree -r`, collect every path for
each rejected blob ID, extend the private path rules, and rerun the path filter.

## Verification

Every unique tree was enumerated and all paths for rejected objects were
removed. The final historical inventory contains 258 small PNG UI/icon assets,
zero large images, and zero audio objects. The all-object audit passes with zero
findings.

## Follow-up

Use full tree enumeration whenever history sanitation needs an exhaustive
object-to-path relation. The external canonical postmortem-memory ledger remains
untouched because it is outside the authorized folder.
