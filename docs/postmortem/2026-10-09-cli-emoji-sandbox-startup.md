# CLI emoji inventory sandbox startup failure

The default shell runner could not start the output inventory. Approved scoped host execution allowed inspection to continue; the default sandbox remains unresolved.

## Symptom and impact

Two initial read-only commands exited 1 with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. Neither command body ran. Repository status was captured through approved execution before this report was written; pre-existing dirty files remain protected.

## Lookup and applicability

Read the canonical postmortem-memory skill and searched `bwrap loopback Failed RTM_NEWADDR`. Reviewed `references/execution-environments.md#local-sandbox-loopback-approved-route`: the identical pre-execution failure and subsequent successful approved reads establish applicability. The initial skill retrieval used the permitted prerequisite host route because default retrieval itself failed.

## Resolution and verification

Approved `require_escalated` execution returned repository status, required skills and the output inventory with exit 0. This verifies the existing workaround, not a repair of Bubblewrap or its underlying host policy. No host security settings were changed.

## Learning and follow-up

No new reusable learning: this repeats the reviewed loopback-startup workaround without expanding its authorization or verification scope. Register this report hash with that explicit decision and run the targeted coverage check. Continue only task-scoped approved operations; host sandbox repair remains separate.
