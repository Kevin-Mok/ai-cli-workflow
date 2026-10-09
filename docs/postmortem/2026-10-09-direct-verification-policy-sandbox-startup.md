# Direct-verification policy edit: sandbox startup failure

The command sandbox failed before repository reads could run. Approved scoped
execution allowed this documentation task to continue; host repair is outside scope.

- Symptom: initial read-only command exited 1 before shell startup with
  `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Impact: initial reads did not execute and no repository files changed.
- Lookup: searched `bwrap loopback Failed RTM_NEWADDR`; matching finding
  `ext-sandbox-loopback` and the 2026-10-08 smoke-output startup report apply
  because the startup error is identical.
- Cause: loopback initialization is denied; underlying host cause was not investigated.
- Resolution and evidence: approved scoped status/instruction reads exited 0.
  This verifies the existing workaround, not repair of the default sandbox.
- Status: verified workaround; continue through approved scoped execution.
  Default sandbox startup remains unresolved and needs separate host investigation.
- Learning: no new reusable learning; identical symptom and workaround are already
  covered by `ext-sandbox-loopback`. Register this reviewed report and run the
  targeted memory check.
