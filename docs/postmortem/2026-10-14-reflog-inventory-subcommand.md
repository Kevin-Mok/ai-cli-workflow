# Reflog Inventory Used An Invalid Subcommand

This postmortem records a failed verification command and the documented reflog enumeration used in its place.

## Symptom

`git reflog list` exited nonzero because this Git version does not provide `list` as a reflog subcommand.

## Impact

The earlier license, ref-count, remote/tag-ref, and replace-ref checks in the same read-only command completed. No repository state changed, but that command did not establish the reflog inventory.

## Evidence

- Git reported `list` as an ambiguous argument.
- `git reflog --help` and the installed command contract use `show --all` for enumeration.

## Current status

Contained. The verification is repeated with `git reflog show --all`.

## Root cause

The command confused ref-listing terminology with the reflog command's supported `show` operation.

## Resolution

Use `git reflog show --all` and count its output; retain `git for-each-ref` for ordinary ref inventory.

## Verification

The corrected `git reflog show --all` inventory produced zero entries. Remote/tag-ref and replace-ref inventories also remained empty.

## Follow-up

- Prefer installed help or a known-compatible command form when capturing final Git hygiene evidence.
