# Temporary Artifact Search Crossed Restricted Directories

This postmortem records a noisy temporary-file inventory command and the narrower search boundary used afterward.

## Symptom

A `find /tmp` query returned the intended task artifacts but also exited unsuccessfully after encountering unrelated system-managed temporary directories that deny traversal.

## Impact

No files changed and the relevant task artifacts were still listed. The command was broader than necessary and produced unrelated permission diagnostics.

## Evidence

- The successful output included the task-specific binary-review manifest and montages.
- All errors referred to unrelated system or daemon temporary directories outside the task prefix.

## Current status

Contained. Later inventories will target explicit `/tmp/ai-cli-dotfiles-public-*` paths rather than walking the whole temporary root.

## Root cause

The query used `/tmp` as its traversal root even though every task artifact has a known task-specific prefix.

## Resolution

Use explicit prefixed paths and shell expansion or a task-maintained manifest; do not traverse unrelated temporary directories.

## Verification

The intended manifest and two montage paths were returned before the permission errors, and subsequent checks use only those explicit paths.

## Follow-up

- Keep temporary artifacts under one task prefix or record each exact path as it is created.
- Avoid broad `/tmp` walks in shared system environments.
