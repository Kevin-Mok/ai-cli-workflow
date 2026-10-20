# Redshift shortcut inspection constraints

Inspect the desktop through the approved host execution route and locate helpers before reading them.

- Symptom: sandboxed `i3-msg -t get_version` could not connect (Operation not permitted); an assumed `scripts/executable_refresh-config` path did not exist.
- Impact: initial inspection only; no desktop state changed.
- Evidence: i3 socket access denied; sed reported missing file.
- Lookup: postmortem-memory search `i3 IPC Operation not permitted` returned sandbox-route guidance. Applicable principle: use scoped approved host execution; loopback-specific cause is not established here.
- Root cause: restricted desktop IPC and an unverified helper path assumption.
- Status: task-local deployment and runtime verification complete; broad refresh remains blocked by unrelated MIME drift.
- Next steps: none for task-local deployment; unrelated MIME reconciliation remains separate.
- Learning: no new reusable finding; existing execution-environment guidance covers scoped escalation, and source discovery avoids assumed paths.

- Regression fixture: ubuntu-start test expected the old raw Redshift command; update its assertion to the new shared helper while preserving the 3000 K contract.
- Refresh attempt: fish refresh-config exited 1; apply stopped without adopting files. Private diagnostics retained under /tmp; inspect the conflict before scoped application.

- Scoped apply refused i3 as unmanaged: initially suspected GUI filtering; inspection confirmed gui=true and migrationPreservedTargets excludes i3. Initial refresh had already applied the fish wrapper before the MIME stop. Inspect template data and deploy explicitly rendered task files without altering unrelated host choices.

## Resolution and verification

Full refresh stopped because `.config/mimeapps.list` had local drift and no interactive input. Exact apply refused the i3 target because local migrationPreservedTargets excludes it. Used approved host execution, replaced only the live Redshift block, installed the helper, and regenerated shortcuts; unrelated settings remain intact.

Lookup `refresh-config conflict noninteractive` matched local-mime-drift-reconcile, local-refresh-snapshot-ownership and local-discover-paths-before-reads. Existing guidance applies to scoped deployment and discovering paths; no new reusable finding.

Fresh controller test (1 test), source binding check, ubuntu-start regression and fish syntax passed. Installed i3 validation exited 0 with pre-existing wheel-command deprecations; reload succeeded; live binding check passed. Real Redshift round trip produced 3000 → 3250 → 3000 K. Simulated Ctrl+Alt+Up/Down produced 3250 then 3000 K. Broad refresh remains incomplete; MIME reconciliation is outside this task.

## Commit privacy verification

The pre-commit gate blocked one home_path finding in the new ledger alias. Existing public privacy guidance applies: publish a neutral alias and retain the real alias only in local working state. A concurrent session staged unrelated files after the status check; use an isolated index so its candidate stays separate. No gate or hook bypass. Recheck the sanitized exact candidate before committing.
