# Skill import sandbox startup failure

The default command runner failed before reading skill instructions. Approved execution allows the requested skill import to continue; host sandbox repair remains outside this task.

## Symptom and impact

On 2026-10-12, the first read returned exit 1 with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. The command body never ran and no repository files changed.

## Lookup and evidence

Queried `bwrap loopback Failed RTM_NEWADDR` using the tracked postmortem-memory helper. Finding `local-sandbox-loopback-approved-route` applies: failure occurred before shell startup, and approved execution read instructions and captured Git status with exit 0. Its reference explicitly limits the remedy to a workaround.

## Status and resolution

Verified workaround: use approved scoped execution for this task. The underlying host namespace restriction is unresolved; no host security settings were changed. Read-only repository inspection succeeded with exit 0 through this route.

## Follow-up and learning

Continue importing the two installed skills and verify managed deployment. No new reusable learning: this is the existing sandbox-startup signature and already documented approved-route remedy.
