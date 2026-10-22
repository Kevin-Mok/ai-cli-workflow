# Fish alias inspection failures

This report records inspection failures while adding the `va` directory shortcut
and the checks used to finish without overwriting unrelated configuration.

- Symptom and evidence: a combined `cat` exited 1 because
  `dot_config/fish/functions/sync-shortcuts.fish` does not exist. A subsequent
  normal Fish startup exited 0 but emitted read-only filesystem errors from fnm,
  universal variables, and shortcut generation.
- Impact: inspection noise and delay; neither failure changed tracked sources.
- Cause: assuming an executable was an autoload function and using normal shell
  startup for a read-only inspection under a restricted filesystem.
- Lookup: query `cat no such file sync-shortcuts function path` matched
  `local-discover-paths-before-reads` in `references/paths-ownership.md`;
  the inventoried executable is `scripts/executable_sync-shortcuts`, deployed as
  `~/scripts/sync-shortcuts`. The existing path-discovery guidance applies.
- Additional failure: scoped refresh exited 1; its private log reports
  `chezmoi: ~/aliases/key_dirs: not managed` (home path normalized). No apply completed.
  Query `chezmoi apply permission conflict key_dirs` returned attribute, parent
  creation, and MIME findings, none explaining this unmanaged alias target.
- Diagnosis: the existing catalog is currently unmanaged by chezmoi. Historical
  state and `target-path` output do not establish current management. Reviewed
  `local-chezmoi-preserved-target-activation` applies: merge the authorized small
  change into the preserved live file and regenerate its derived outputs.
- Broad dry-run exited 1 at an unrelated Kitty managed-file conflict; do not
  overwrite that file. An isolated source containing only the rendered directory
  catalog also stopped at a historical state conflict for `aliases/key_dirs`.
  The installed catalog still matches the pre-change rendered source byte for
  byte, so forcing only that exact reviewed target is safe for this change.
- Status: resolved for the requested shortcut; unrelated broad-refresh conflict
  remains outside this task.
- Resolution: inspected inventoried paths, used `fish --no-config`, and ran
  refresh-config with a temporary chezmoi wrapper selecting an isolated rendered
  source and forcing only the previously compared directory catalog. No tracked
  refresh code or unrelated configuration was changed.
- Verification: scoped refresh exited 0 and its private log was empty; installed
  Fish inspection returned `abbr -a -- va 'cd ~/coding/twitch-grid'`; Bash alias
  inspection returned the corresponding directory alias. The repeated absolute
  request reports `changed: false`, `conflicts: 0`. Generated Fish syntax and
  `git diff --check` passed, exit 0. No mapped command executed.
- Follow-up: broad refresh still requires separate review of the existing Kitty
  conflict. No new reusable learning: existing path-discovery, sandbox-startup,
  and preserved-target activation guidance cover this incident. Register this
  report with that explicit decision; do not duplicate existing findings.
