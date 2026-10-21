# Refresh stopped on screensaver launcher permissions

Track the reviewed-target conflict that stopped refresh, compare content and
permissions, and reconcile only the supported ownership boundary.

- Status: recovery verified; explicit reinstall can recreate mode drift.
- Symptom: `refresh-config` exits 1 after the apply phase.
- Impact: shortcut regeneration/reload never runs; full refresh is incomplete.
- Evidence: the private log identifies `scripts/media-screensaver` as changed
  since chezmoi last wrote it, followed by prompt EOF. Source, installed and
  rendered launcher contents have identical SHA-256
  `423eddcc8da46ae97b02b4b9f540a0fa894bde0216771cd3e6cf5b2fe4830276`.
  `chezmoi diff` shows only `old mode 100755`, `new mode 100775`.
- Root cause: the explicit installer sets launcher mode 0755; the current
  chezmoi target expects 0775. The helper has stdin closed, so its overwrite
  protection refuses the changed target instead of accepting a choice.
- Lookup: `refresh-config apply stopped local differences` found
  `local-mime-drift-reconcile`, `local-hidden-prompt-lock` and
  `local-refresh-snapshot-ownership`. Drift reconciliation/protection applies;
  MIME-specific content and the historical keep-going remedy do not justify
  overwriting unrelated current targets.
- Protected state: preserve all initial dirty Fish, smoke, lessons, prompt,
  plan and incident-knowledge files; no commits/push requested.
- Next steps: inspect actual managed target/ignore rules and permissions
  contract; define a failing reproducer; reconcile this exact conflict;
  verify no content changes and exercise the real refresh safely.

## Verification and remaining limits

Read-only launcher comparison and target diff passed (exit 0). No new refresh
attempt or permission change has been made yet.

The current chezmoi umask is002. Actual managed-target inspection shows Fish
config is deliberately unmanaged, despite the differing raw public template;
the earlier assumption that refresh would overwrite that file was too broad.
`chezmoi status` lists only the launcher as both source/live modified. A direct
diff request for the unmanaged Fish config exits1 as expected, confirming the
scope boundary; no retry or modification is appropriate for that file.

Decision: exact-target apply may reconcile the reviewed permission delta;
normal broad refresh remains unforced. Preserve installed contents and verify
hashes. An explicit reinstall can recreate the mode conflict; installer policy
changes are outside this narrow repair.

## Reconciliation progress

The defining `chezmoi verify` returned1 for the exact target. A guarded
exact-target apply then changed only0755 to0775; the content hash stayed equal,
and target verification returned0. No other both-modified target remained.

The first refresh verification launcher used `fish --no-config`, which does
not load this machine's function setup; it returned127 (`refresh-config:
command not found`) before calling chezmoi. This is a verification setup error;
no broad apply ran. Use the normal configured Fish invocation after consulting
the existing function-discovery guidance.

## Resolution and verification

The existing function-discovery finding applies to the setup error. Normal
`fish -c 'refresh-config'` completed all apply/sync/source phases, emitted
`REFRESH COMPLETE`, and exited0. The new private refresh log is recorded by the
helper; the exact launcher now passes `chezmoi verify` at mode0775 with its
original contents. No installer or broad-force policy was changed.

- Installed `media-screensaver status --plain`: exit0; three monitors and idle
  monitor running. Browser-bridge suppression remains accurately reported.
- Installed Fish login with VT absent and DISPLAY set: exit0, success marker,
  zero stderr bytes; original startup repair remains active.
- `bash tests/test_refresh_config_function.sh`: exit0; isolation, conflict
  refusal and actual chezmoi exclusion contracts pass.
- `python3 -B tests/test_fish_startup.py`: exit0; all eight guard cases pass.

The effective boundary matters: `--exclude scripts` excludes chezmoi run hooks,
not managed executable files in the destination's scripts directory. README and
smoke checks now clarify this. Future explicit screensaver installation still
sets0755; under the current chezmoi umask002, that can recreate this mode-only
conflict. The verified workaround reconciles the exact reviewed target; changing
installer permissions is intentionally outside this recovery. No commit/push.
