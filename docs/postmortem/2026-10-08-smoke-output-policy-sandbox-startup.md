# Smoke-output policy edit: sandbox startup failure

The command sandbox failed before repository reads could run. Approved scoped
execution allowed the documentation task to continue; host sandbox repair remains
outside this task.

- Symptom and evidence: two independent read-only commands exited 1 with
  `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` before shell startup.
- Impact: initial status and instruction reads did not execute; no files changed.
- Lookup: searched `bwrap loopback Failed RTM_NEWADDR`; reviewed
  `references/execution-environments.md#ext-sandbox-loopback`. The identical
  startup errors and successful approved status read match its applicability.
- Cause: restricted runner loopback initialization is denied; the underlying
  host permission cause was not investigated.
- Resolution and verification: approved `require_escalated` status and source
  reads exited 0; initial Git status was clean. This verifies a workaround only.
- Status and next steps: documentation work can proceed through scoped approved
  execution. Default sandbox startup remains unresolved and requires separate
  host-level investigation.
- Learning: no new reusable finding; this repeats reviewed
  `ext-sandbox-loopback` guidance without changing its scope or remedy. Register
  this report's reviewed hash and run the targeted memory check.
