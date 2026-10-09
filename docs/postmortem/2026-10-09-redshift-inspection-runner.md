# Redshift inspection runner failure

Use the approved scoped runner to inspect and update Redshift shortcuts after
the default sandbox cannot start. Host sandbox repair remains separate.

## Symptom, impact and evidence

Two initial reads failed before shell execution with `bwrap: loopback: Failed
RTM_NEWADDR: Operation not permitted`; no requested command body ran. A later
inspection assumed a scripts/executable_refresh-config path that does not
exist; the actual helper is dot_config/fish/functions/refresh-config.fish.
No configuration change resulted from those failures.

## Lookup and applicability

Read canonical postmortem-memory and searched `bwrap loopback Failed RTM_NEWADDR`.
Reviewed local-sandbox-loopback-approved-route: same pre-shell symptom,
matching approved read workaround. Scoped require_escalated reads exited 0.
The refresh helper was located by repository search and read successfully.

## Resolution, status and follow-up

Verified workaround for runner startup; default sandbox remains unresolved.
Use the scoped approved runner for authorized operations. Avoid assuming a
script location when repository search identifies a fish function.

## Learning

No new reusable learning: existing sandbox and inspect-before-use guidance
covers both symptoms. Register reviewed hash with explicit no-new-learning
and run the targeted check. Deliberate mapping RED checks are exempt.
