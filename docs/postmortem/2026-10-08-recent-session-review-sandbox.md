# Recent session review sandbox startup failure

Continue the authorized session-review implementation through scoped approved commands. The normal shell sandbox cannot initialize loopback; host repair is outside this task.

## Symptom and impact
The first read-only shell command failed before execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` (exit 1). No repository command or write ran.

## Lookup and evidence
Query `bwrap loopback Failed RTM_NEWADDR` matched `local-sandbox-loopback-approved-route` and `ext-sandbox-loopback` in execution-environments.md. Their startup-only scope applies. Approved repository reads and `git status --short` succeeded (exit 0). Initial dirty state was captured before changes.

## Resolution and verification
Verified workaround: use the approved require_escalated route for the same bounded operations. Normal sandbox startup remains unresolved. No new reusable learning beyond the existing finding. Do not change host networking or security settings.
