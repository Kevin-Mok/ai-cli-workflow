# VPS prompt delivery: documentation patch context mismatch

Date: 2026-10-04

## Symptom and impact

A patch updating the session-attribution incident and prompt-authoring plan
failed verification because its final plan hunk referenced text out of order.
The patch tool reported `Failed to find expected lines`. No commit or push
had occurred; delivery paused to inspect possible partial application.

## Evidence and root cause

The patch ended with an unnecessary context-only hunk for
`No model comparison, installation test, Terraform test, or cloud deployment`
after hunks targeting later sections of the same file. The ordered patch
search could not match that earlier text.

## Resolution and verification

Read-back inspection confirmed that neither target document had been partially
modified. The replacement patch removes the invalid context-only hunk and
orders the remaining changes as they occur in the source.

Read-back checks confirmed valid UTF-8, final newlines, no trailing whitespace,
and resolving local links across the six-path delivery scope. The prompt hash
still matches the approved text. `git diff --check` and the README gate both
passed, exit 0. Staged-scope inspection remains the normal pre-commit gate.
This record ships in the same commit as the corrected documentation.

## Follow-up

Avoid context-only patch hunks and keep multi-hunk edits in source order.
