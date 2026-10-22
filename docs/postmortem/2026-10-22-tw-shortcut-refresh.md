# Scoped refresh for the tw directory shortcut

This report records the refresh failure after replacing the `tw` directory
mapping and its recovery. Check managed targets, preserve local-only mappings,
then deploy the reviewed shortcut and scope refresh to the aliases directory.

- Symptom: scoped `refresh-config` exited 1 during chezmoi apply and reported
  that apply stopped before shortcut regeneration.
- Impact: the first refresh stopped before shortcut regeneration.
- Evidence: `the private failure log` is the private diagnostic log.
  The invocation used a temporary fish wrapper to add only
  `~/aliases/key_dirs` to the existing chezmoi apply command.
- Diagnostic: the private log contains only
  `chezmoi: ~/aliases/key_dirs: not managed`.
- Lookup: searched memory for `refresh-config chezmoi apply scoped target
  conflict`; the returned MIME/capture/mode findings apply only to managed
  targets and do not establish a remedy for this unmanaged path. Existing
  path-discovery guidance applies to checking the actual deployment layout.
- Report update error: an inline Python edit exited 1 with an unterminated
  string literal before any write. A memory lookup for `unterminated string
  literal multiline edit` preceded recovery using a structured patch.
- Disposable verification error: the test agent initially supplied a missing
  temporary commands-source path; the corrected fixture passed. Its failed
  attempt wrote only under `/tmp` and did not affect configuration.
- Installed verification error: the test agent also tried an assumed
  `~/.local/share/chezmoi/aliases/key_dirs` source path (exit 2), then compared
  against the confirmed live `~/aliases/key_dirs` successfully. Its broad
  abbreviation listing was filtered to the intended effective names.
- Root cause: this host's private chezmoi data lists all three alias inputs in
  `migrationPreservedTargets`; `.chezmoiignore` intentionally excludes them.
  Only their parent `~/aliases` directory is managed. Appending the
  ignored file target to chezmoi apply therefore fails even when the template
  exists in the source repository.
- Resolution: confirmed the live regular file still matched the captured
  pre-change rendering, rendered only the reviewed directory template to it,
  then invoked the existing `refresh-config` through a temporary fish wrapper
  that limited chezmoi apply to the managed aliases directory. Its prior
  verbose dry run exited 0 without proposed changes. Private migration policy
  and unrelated destination files were preserved.
- Verification: the recovery exited 0; apply, shortcut synchronization, and
  sourcing all ran and printed `REFRESH COMPLETE`. Recovery private log:
  `the private recovery log`. Source previews for absolute and normalized
  requests were no-ops; disposable and installed generated fish passed `fish -n`.
  A fresh fish process showed `tw` as `cd ~/coding/triway-nextjs` and retained
  `ntw` as `$EDITOR ~/linux-config/dot_taskrc`; source and live directory
  mappings compared byte-for-byte equal.
- Status: resolved. This was a scoped refresh; no broad apply was performed.
- Learning: no new general rule beyond the existing reviewed path-discovery,
  local-state preservation, and nested-language literal guidance. The ignored
  targets are host-specific policy; this workaround does not change the default
  refresh implementation. Register this report's current reviewed hash and alias.
- Follow-up: check both `chezmoi managed` and `chezmoi ignored` before assuming
  a source template has an applicable destination; use structured patches for
  multiline report edits.
