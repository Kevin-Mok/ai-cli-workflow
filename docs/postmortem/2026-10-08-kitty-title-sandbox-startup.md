# Kitty title investigation sandbox startup failure

The default command runner failed before repository inspection. Use the approved scoped runner to inspect the reported stale title; host sandbox repair is separate.

## Symptom and impact

The initial read-only command returned `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` before running. No repository changes occurred. Subsequent scoped escalated status and instruction reads exited 0.

## Lookup and evidence

Read the canonical postmortem-memory skill. Query: `bwrap loopback Failed RTM_NEWADDR`. Matching guidance: `local-sandbox-loopback-approved-route` and `ext-sandbox-loopback`, verified workarounds. Applicable because the failure occurred before shell execution and approved reads then succeeded. The default sandbox remains unresolved.

## Resolution and verification

Approved `require_escalated` repository reads succeeded with exit 0. This is a verified workaround, not a host repair. Continue necessary scoped commands using this route.

## Learning and follow-up

No new reusable learning: this recurrence matches the existing sandbox-loopback findings without expanding their evidence or permission scope. Register this report hash and run the targeted ledger check. No host security changes are authorized.
