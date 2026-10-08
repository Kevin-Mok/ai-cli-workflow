# Backup fix tooling failures

Record command-runner failures and inspection mistakes during the vanished-file fix, separate from backup behavior.

## Symptom, impact and evidence

Initial read commands failed before execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. Approved scoped escalation reads succeeded. Lookup `bwrap loopback Failed RTM_NEWADDR` matched execution-environments guidance; the identical startup diagnostic applies. Normal sandbox startup remains unresolved.

A read-only rg included a nonexistent scripts/executable_refresh-config path; the actual helper is dot_config/fish/functions/refresh-config.fish. A ledger inspection assumed a sources key and raised KeyError; actual top-level key is reports, as the workflow contract states. Neither changed application state.

## Resolution and verification

Use approved scoped commands and inspect actual paths/schema before access. Repository status and implementation reads completed. These repeat existing environment and API-contract lessons; no new generalized finding is needed. Host sandbox repair is outside this task.
