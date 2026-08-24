# Fix Refresh-Config MIME Apply Blocker

## Purpose and observable outcome

Make `refresh-config` complete without a ChezMoi prompt caused by the tracked
FNLB MIME handler differing from the installed handler.

## Current context, relevant files, and scope boundaries

- `dot_config/mimeapps.list` tracks `appimagekit_…-FNLB.desktop`.
- `~/.config/mimeapps.list` uses `fnlb.desktop`; ChezMoi reports the target as
  modified and a noninteractive apply cannot answer its overwrite prompt.
- Scope: reconcile only the FNLB handler, add a focused source regression test,
  and update the existing MIME incident postmortem.
- Protected dirty state: all files listed by `git status --short` before this
  work, including the existing config, README, and design-skills changes.

## Assumptions and decisions

- The installed `fnlb.desktop` handler is the intended current association.
- Do not broaden `chezmoi apply --force`; preserving unrelated conflict
  protection remains required.

## Implementation checklist

- [x] Capture current state and compare source with the installed MIME target.
- [x] Add and run a focused failing regression check for the expected handler.
- [x] Reconcile the tracked FNLB handler with the installed association.
- [x] Run the focused check, a ChezMoi dry run, and the live refresh workflow.
- [x] Update this plan and the incident postmortem with evidence and rollback.

## Risks, edge cases, rollback points, and protected dirty state

- This records a machine-local association in tracked source. Roll back by
  restoring only the previous `x-scheme-handler/fnlb` line if it proves wrong.
- No full-force ChezMoi apply is permitted; unrelated local config must retain
  its normal prompt protection.

## Exact automated and manual verification

- Run `tests/test_mimeapps_fnlb_handler.sh`; it must fail before the source fix
  and pass afterward.
- Run `chezmoi apply --dry-run ~/.config/mimeapps.list`; it must not request a
  TTY for the reconciled target.
- Run `fish -c 'source dot_config/fish/functions/refresh-config.fish; refresh-config'`;
  it must emit `REFRESH COMPLETE`.

## Progress, verification evidence, and review notes

- Root cause confirmed on 2026-08-24: source and target differ only at the
  FNLB handler (`appimagekit_…-FNLB.desktop` vs `fnlb.desktop`).
- Review: the simplest robust fix is source reconciliation, not changing the
  helper's established conflict-handling policy.

- RED evidence: `tests/test_mimeapps_fnlb_handler.sh` failed with the old tracked AppImage desktop entry.

- GREEN evidence: `bash tests/test_mimeapps_fnlb_handler.sh`, `chezmoi apply --dry-run ~/.config/mimeapps.list`, and `fish -c 'source dot_config/fish/functions/refresh-config.fish; refresh-config'` completed on 2026-08-24; the full workflow emitted `REFRESH COMPLETE`.
- Regression evidence: `bash tests/test_refresh_config_function.sh` passed.
- Rollback: restore only the prior FNLB handler source line if its desktop-file identifier changes.
