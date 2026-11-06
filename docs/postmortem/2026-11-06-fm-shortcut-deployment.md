# Firstmate shortcut deployment probes

This report records diagnostic path and sandbox restrictions encountered while adding the fm directory abbreviation, and the checks used to finish deployment.

- Symptom: an assumed fish function path for sync-shortcuts did not exist; ordinary fish startup and refresh attempted writes outside the workspace and failed on a read-only filesystem.
- Impact: initial refresh did not deploy the shortcut. No user command was executed.
- Evidence: sync-shortcuts exists at scripts/executable_sync-shortcuts; fish startup reported read-only fnm and universal-variable writes; refresh log /tmp/refresh-config.vI6dJSto.log.
- Lookup: query `missing file path discovery` matched ext-optional-path-discovery; applicable because executable placement was assumed. Query `refresh-config read-only sandbox` checked prior permission guidance before retry.
- Root cause: diagnostic path assumption and execution inside the restricted filesystem.
- Status: resolved. Authorized refresh outside the sandbox succeeded using fish --no-config. The installed catalog was migration-preserved; added only fm there and refreshed again.
- Resolution: source contains fm in cdn; installed catalog preserves unrelated entries. A diagnostic ledger read incorrectly selected sources rather than reports (KeyError); inspected schema and corrected it without modifying data.
- Verification: refresh exited 0; isolated fish registered fm as cd ~/coding/firstmate; fish -n exited 0; README gate pass_no_change. No navigation command was executed.
- Learning: no new reusable guidance; existing path-discovery, schema inspection, sandbox escalation and preserved-catalog activation guidance apply. Interactive typing remains untested.
- Next steps: focused commit and upstream push.
