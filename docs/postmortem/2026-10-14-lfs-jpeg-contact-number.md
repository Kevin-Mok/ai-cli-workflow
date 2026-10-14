# LFS JPEG Contact Number Escaped Text Audit

This postmortem records why a personal contact number embedded in an image was not caught by the initial history audit, how the evidence review found it, and how the public-history rewrite removes both the Git pointer and the corresponding LFS payload.

## Symptom

The evidence reviewer visually inspected the only retained Git LFS image and found a readable personal contact number on an object in the photograph. The automated history audit had reported zero findings because Git history contained only the LFS pointer text, not the image pixels.

## Impact

The candidate public history was not safe to publish. Publishing it with LFS content would have exposed personal contact information even though the Git-object scan was clean.

## Evidence

- `git lfs ls-files` identified one retained LFS path.
- The reviewer inspected the resolved LFS payload and identified a readable contact number without reproducing it in logs or reports.
- The path appears in one original commit lineage and has a single LFS object identifier.

## Current status

Resolved in the isolated candidate. Source-repository transplant verification remains part of the final delivery gate.

## Root cause

The first binary review treated a successful LFS integrity check as evidence that the payload was safe. The content scanner examined Git blobs, where the file is represented by a small pointer, and the manual binary montage excluded LFS-resolved content. No explicit review gate required visual inspection of every retained LFS payload.

## Resolution

The image path was removed from every retained commit with empty-commit pruning enabled. Original rewrite refs and reflogs were deleted, Git objects were pruned, and the sole candidate LFS payload was pruned. The stale current-tree LFS attribute was also removed.

## Verification

- The sanitized graph still contains 688 retained historical commits.
- The removed path has no result in the all-ref object inventory.
- `git lfs ls-files` reports no paths, and `git lfs prune --force` reported one deleted local object with none retained.
- `git fsck --full --unreachable --no-reflogs` reports no unreachable objects.
- A fresh private-rule audit passed across 688 commits and 5,128 unique blobs with zero findings.

## Follow-up

- Require visual or format-aware inspection of every retained LFS payload in public-history rewrites.
- Treat a clean Git-blob scan as incomplete whenever `git lfs ls-files` is non-empty.
- Keep final reports explicit about binary and LFS review coverage.
