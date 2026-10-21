# DND inspection path lookup

Two read-only inspection commands included guessed filenames that do not exist.
No configuration changed during those commands.

- Symptom/evidence: rg reported missing scripts/executable_refresh-config; sed reported missing tests/test_i3blocks_volume.sh.
- Impact: inspection noise only; existing files in each batch were still read.
- Lookup: searched postmortem memory for “missing file guessed path”; local-discover-paths-before-reads applies.
- Cause: filenames were inferred instead of discovered.
- Resolution: located refresh-config at dot_config/fish/functions/refresh-config.fish; use the search agent’s report for DND scope.
- Verification: read the actual refresh function and compared deployed/source DND scripts successfully.
- Status: resolved; no product defect or new reusable learning beyond the existing discovery guidance.
- Next steps: complete the requested label change and deployment checks.

## Configuration activation restriction

- Symptom: fish startup could not write fnm links/universal variables/shortcut files; refresh-config could not open chezmoi state due to the read-only home sandbox.
- Evidence: /tmp/refresh-config.eUnz8EFj.log reports chezmoistate.boltdb read-only.
- Impact: first refresh did not apply the label.
- Lookup: searched “refresh-config read-only filesystem”; sandbox write restrictions apply, independently of the label edit.
- Status: resolved. Authorized refresh exited 0 with REFRESH COMPLETE; installed/source DND files match and the live read-only invocation prints Notis.
