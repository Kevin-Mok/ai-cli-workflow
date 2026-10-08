# Notification speech sandbox startup failure

The notification speech implementation uses approved scoped commands because the default runner cannot initialize its network namespace.

- Symptom/evidence: two independent read-only commands failed before execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Impact: initial instructions/status reads blocked; no files changed.
- Lookup: searched `bwrap loopback Failed RTM_NEWADDR`; reviewed `ext-sandbox-loopback` in execution-environments.md. Applicable because both failures precede shell execution.
- Root cause: sandbox network namespace initialization denied by host (confirmed startup symptom; host cause not repaired).
- Resolution/status: verified workaround; approved require_escalated reads successfully captured status and source context (exit 0). Continue with scoped approved commands.
- Verification: repository status/source reads succeeded through approved route; default sandbox remains unavailable.
- Follow-up: host sandbox repair is outside this task. No new learning beyond the existing approved-route finding.
