# Fish alias skill sandbox startup

The command sandbox failed before source reads ran. Approved scoped execution lets the authorized skill implementation proceed; host sandbox repair remains outside this task.

- Symptom: two initial reads, and an independent inspection read, failed with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`, exit 1.
- Impact: source inspection delayed; no command bodies or repository edits executed in the failed launches.
- Lookup: query `bwrap loopback Failed RTM_NEWADDR`; reviewed `local-sandbox-loopback-approved-route` in execution-environments.md. Applicable because startup failed before command output.
- Cause: Bubblewrap loopback namespace initialization denied; host policy cause remains uninvestigated.
- Resolution: approved require_escalated execution for the same bounded operations.
- Verification: source/prompt/status reads succeeded with exit 0. Status captured before writes.
- Status: verified workaround; default sandbox unresolved.
- Follow-up: continue authorized implementation through reviewed execution; do not alter host sandbox policy.
- Learning: no new learning beyond the existing approved-route finding; register this reviewed report and run targeted coverage check.
