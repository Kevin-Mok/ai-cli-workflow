# Backup recovery task shell sandbox startup failure

The normal shell runner failed before repository inspection. Use the approved scoped runner for this task, keep repository work separate from host sandbox repair, and verify actual command output and exit status.

- Symptom/evidence: first pwd/status/skill read returned `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` without executing the command body.
- Impact: no file or disk writes occurred; ordinary sandbox execution is unavailable.
- Lookup: searched `bwrap loopback Failed RTM_NEWADDR`; reviewed `local-sandbox-loopback-approved-route` in execution-environments.md. Applies because failure occurs before shell execution.
- Root cause: runner network namespace cannot initialize loopback; underlying host policy not diagnosed.
- Resolution/status: verified workaround, scoped require_escalated reads returned expected repository status and exit 0. No host security changes.
- Verification: pwd/git status and source/skill reads executed successfully through approved route; default sandbox remains unresolved.
- Follow-up: use scoped approved commands for this task, independently check resulting files; repair sandbox separately.
- Learning: same known workaround, no new reusable learning. Register this report against the existing finding and validate its reviewed hash.
