# Restore confirmation stdin is consumed by launcher

Record a restore-readiness blocker found while reviewing the dated-bundle runbook. No real restore was attempted and no disk was changed.

## Symptom, impact and evidence

scripts/executable_backup-pc executes Python using `exec python3 - "$@"` with a heredoc on stdin. restore() then calls input() for the ERASE confirmation. Python has consumed stdin as its program, so input reaches EOF and the caught EOFError cancels before destructive operations. The example bundle contains the same launcher. Restore dry-run returns before input and is unaffected. Backup does not require this input prompt.

An independent documentation reviewer reproduced the EOF using an isolated heredoc. Root verification and resolution are recorded below. Successful backup publication and archive validation do not test the real interactive launcher.

## Lookup

Postmortem-memory query `heredoc stdin EOFError` was retrieved before any remedy. Compare matching entries against this launcher; generic shell-transport guidance is not evidence of a fixed backup helper.

## Status and next steps

Unresolved. This task documents the blocker, preserves the original bundle and does not alter its checksummed files. Fix and test the interactive launcher/confirmation in a separate implementation change, then validate the full restore in a disposable VM before claiming boot recovery. Do not bypass confirmation or modify the bundled script in place, which would invalidate SHA256SUMS.

## Verification and applicability

Root independently ran an isolated Python heredoc that calls input(), catches EOFError and prints a confirmation marker: exit 0 with `confirmed: heredoc stdin is exhausted before confirmation`. This intentionally exercises the failure and is not a real restore attempt. Source inspection confirms the same pattern in both scripts/executable_backup-pc and the dated bundle helper. ext-stdin-consumed-by-child is related transport evidence but its /dev/null remedy is inappropriate for an interactive prompt and was not applied. Recovery guides now warn explicitly. No backup bytes or runtime scripts were changed.

## Learning record

local-backup-restore-stdin-confirmation remains unresolved with confirmed mechanism and code verification scope. Track this report hash and guidance in postmortem-memory and run its targeted check. No actual erase or boot was attempted.
