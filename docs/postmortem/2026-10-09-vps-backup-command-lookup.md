# VPS backup command lookup: shell sandbox startup failure

This report records a shell runner failure while checking existing VPS backup shortcuts. Scoped read-only escalation allowed the lookup to finish.

- Symptom: both initial read-only commands failed before execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Impact: initial skill read and shortcut search did not run; no backup was attempted.
- Lookup: searched `bwrap loopback Failed RTM_NEWADDR`; `ext-sandbox-loopback` applies because failure occurred in runner initialization, before repository commands.
- Evidence: scoped escalated `pwd`, skill reads and repository searches completed successfully. A later search returned exit 2 because optional search paths did not exist; searching known existing paths completed successfully.
- Status: verified workaround; default sandbox remains unverified and unrepaired.
- Resolution: use approved scoped escalation for required repository reads. No server or backup state changed.
- Learning: no new reusable finding; existing sandbox guidance covers this failure. Avoid guessing directory names in explicit search operands.
- Next steps: host sandbox repair is outside this command-lookup task.

## Follow-up project lookup

The user directed the lookup to `/home/example/coding/example-client-app`. Two read-only commands included incorrect optional operands: a mistyped extra `ls` path and a guessed `recovery.py` filename. They returned exit 2; no files changed. Reading the actual entry point and recovery guide, then checking the documented helper with `Path.is_file()` and running `vps.sh recovery --help`, succeeded. The prepared capture helper and policy exist. No remote access or backup was performed. This adds no reusable learning beyond checking actual paths before searching them.

## USB completion check

Read-only metadata inspection found one published capture with `verified: true`, its encrypted archive, wrapped identity and matching checksum record. One `.partial` capture has no receipt. Initial traversal stopped on `PermissionError` for a protected extraction directory; scoped enumeration then reported both protected extraction/VM directories without changing permissions. A guessed optional controller source filename was absent; reading the actual `vps-recovery.py` confirmed receipt publication follows archive verification. No backup was modified, no full archive rehash/decryption was attempted, and extraction/guest completion remains unconfirmed. No new reusable finding; permission-aware scoped reads and actual entry-point lookup cover this inspection.
