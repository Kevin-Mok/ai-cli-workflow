# Tcu shortcut inspection in a restricted shell

This report records inspection failures while adding a directory abbreviation and the checks used to complete deployment.

- Symptom: assumed script paths for refresh-config and sync-shortcuts did not exist; normal fish startup attempted writes to read-only fnm, universal-variable and alias locations.
- Impact: noisy inspection; shortcut preview and application succeeded independently.
- Evidence: missing-file exit 1; fish startup emitted read-only filesystem diagnostics despite overall exit 0.
- Cause: refresh-config is an autoload function, sync-shortcuts is an executable; normal fish startup has write side effects outside the workspace.
- Lookup: searched `fish startup read-only filesystem fnm`; broad environment findings did not establish an exact remedy for these startup writes.
- Resolution: authorized refresh-config via fish --no-config and explicit function path exited 0 (REFRESH COMPLETE). Host preservation rules excluded alias files from apply, so initial refresh left tcu absent. Explicitly rendered the reviewed directory template to ~/aliases/key_dirs and ran sync-shortcuts with authorized access. Generated key_abbr.fish passes fish -n; filtered abbr --show returns tcu mapped to cd ~/coding/track-codex-sessions and abbr --query tcu succeeds. Normal startup remains outside the restricted verification scope.
- Learning: no new reusable finding; this is an environment boundary and incorrect inspection-path assumption, not a shortcut logic defect.

- Commit phase: isolated-index staging hit the read-only Git object database (exit 128). No candidate commit was created; retry uses the authorized Git write route while preserving the unrelated main index.
