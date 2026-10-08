# Redshift binding inspection sandbox failure

The command runner could not start during i3 inspection. Use the approved scoped runner to complete the binding update; host sandbox repair remains separate.

## Symptom and impact

Two initial reads failed before shell execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. No files changed through those calls.

## Lookup and applicability

Read the canonical postmortem-memory skill and searched `bwrap loopback Failed RTM_NEWADDR`. Existing `local-sandbox-loopback-approved-route` and `ext-sandbox-loopback` guidance applies: startup failed before the requested command, and scoped escalated reads then exited 0.

## Resolution and verification

Scoped `require_escalated` inspection succeeded, exit 0. This is a verified workaround; the default runner remains unresolved. Continue only authorized task commands through this route.

## Learning

No new reusable learning: the symptom and successful workaround match existing guidance without expanding permissions or evidence scope. Register this report hash and run the targeted ledger check.
