# Fish alias prompt sandbox startup

The command wrapper prevented initial skill reads. Approved scoped execution allowed prompt preparation; the default sandbox remains unresolved.

- Date: 2026-10-08.
- Symptom: bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted; initial command exited 1 before its body ran.
- Impact: Initial skill reads delayed; no files changed by the failed command.
- Lookup: Query bwrap loopback Failed RTM_NEWADDR matched local-sandbox-loopback-approved-route, a verified workaround. Identical error and absent command output establish applicability. Skill reads through the approved route were prerequisites to retrieval.
- Root cause: Wrapper loopback initialization failed; underlying host policy remains uninvestigated.
- Resolution and verification: Approved scoped reads returned exit 0 and captured Git status before writes. Prompt saving and exact read-back succeeded through the same route.
- Status: Verified workaround for prompt preparation; no claim of host repair or implemented alias skill.
- Follow-up: Execute the compiled task in the requested fresh conversation; keep sandbox repair outside this task.
- Learning: No new reusable learning beyond the existing local-sandbox-loopback-approved-route finding; register this report with an explicit no-new-learning decision.
