# CLI progress policy sandbox startup failure

The default shell runner failed before the requested instruction edit. Approved scoped execution allowed the update to proceed; host sandbox repair remains separate.

## Symptom and impact

Initial read-only inspection exited 1 with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. The command body did not run and changed no files. Approved repository status and instruction reads subsequently exited 0.

## Lookup and applicability

Read canonical postmortem-memory guidance and searched `bwrap loopback Failed RTM_NEWADDR`. The `local-sandbox-loopback-approved-route` verified workaround applies: identical pre-execution error, followed by successful approved scoped execution. No application failure was observed.

## Resolution and verification

Used approved `require_escalated` execution for bounded repository operations. Successful reads establish a verified workaround; the underlying sandbox initialization cause remains unverified and default execution remains unresolved.

## Learning and follow-up

No new reusable learning: this repeats existing sandbox-loopback guidance without expanding its remedy or authorization. Register the reviewed hash and run the targeted ledger check. Do not change host security settings.
