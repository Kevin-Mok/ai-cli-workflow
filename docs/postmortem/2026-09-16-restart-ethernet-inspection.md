# Postmortem: Restart Ethernet inspection blocked by sandbox

Date: 2026-09-16

## Symptom

The initial read-only repository inspection command failed before returning
output with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.

## Impact

Repository instructions, worktree status, and existing script conventions were
not available from that inspection attempt.

## Evidence

The command was run from `/home/example/linux-config` and exited during sandbox
setup before producing command output.

## Status and next steps

Investigating with narrower read-only commands. If the issue is isolated to the
shell sandbox, continue using available repository tools and verify all changes
normally.

## Resolution

The inspection continued through the elevated read-only path; no repository files were changed by the diagnostic failure.

## Verification

The restart helper and its command-sequence test were reviewed and `bash -n scripts/executable_restart-ethernet` passed.
