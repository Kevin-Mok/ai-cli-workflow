# Sessions review inspection sandbox startup failure

Repository inspection could not start in the normal command sandbox. Use the approved scoped command route to continue the output repair; host sandbox repair remains separate.

## Symptom and impact
Three initial read-only commands and the independent reviewer failed before shell execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. No application command ran or modified files.

## Evidence and lookup
The query `bwrap loopback Failed RTM_NEWADDR` matched `ext-sandbox-loopback` in execution-environments.md. Independent harmless reads failed identically; approved require_escalated reads and git status succeeded. This matches the existing namespace-startup incident, not a sessions renderer failure.

## Status, cause and resolution
Verified workaround: scoped approved commands bypass the unavailable sandbox. The normal runner remains unavailable. Existing reviewed guidance applies; no new reusable learning.

## Verification and follow-up
Approved repository reads exited 0 and captured pre-existing dirty files. Continue focused scoped commands for this task; host sandbox repair is outside scope.
