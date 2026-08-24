# Postmortem: Non-Interactive Refresh Config Stopped at MIME Prompt

**Incident date:** 2026-08-19
**Severity:** Low — unrelated local desktop configuration prompt
**Status:** Resolved for the design-skill scope

## Symptom

The required `fish -ic 'refresh-config'` invocation stopped when chezmoi tried
to prompt about `~/.config/mimeapps.list` without a usable TTY.

## Impact

The full unrelated configuration apply did not finish. The design-skill helper,
timer units, external clones, and Codex skill links had already been applied
through exact target-scoped chezmoi commands; the daily timer remained enabled.

## Evidence

Chezmoi reported:

```
.config/mimeapps.list: could not open a new TTY: open /dev/tty: no such device
or address
```

## Resolution

Do not force a non-interactive answer to the unrelated MIME conflict. Verify the
design-skill targets directly and leave the existing MIME choice for an
interactive refresh-config run.

## Verification

- `setup-design-skills-timer --check` passed after the failed full refresh.
- `systemctl --user list-timers design-skills-sync.timer --no-pager` still
  shows the enabled 05:00 EDT timer.

## Follow-up

Run `refresh-config` interactively when the MIME association decision can be
reviewed. Keep future targeted deployments scoped to their owned paths before
calling a broad interactive refresh.

## Recurrence: 2026-08-24

The user explicitly requested the full `refresh-config` workflow after updating the canonical instruction. The workflow again reached `chezmoi apply` and stopped at the same noninteractive MIME prompt. The tracked and live `fn-progress` functions both contain the requested Chapter 7 Season 4 schedule output, so this change is applied despite the broader refresh remaining incomplete.

- Root cause: `chezmoi apply` requires an interactive decision for the existing MIME association conflict.
- Follow-up: Resolve the MIME choice in an interactive session before the next full refresh.

## Resolution Update: 2026-08-24

**Status:** Resolved.

### Confirmed Root Cause

The tracked FNLB association referenced the removed AppImage desktop entry, while
the installed association used `fnlb.desktop`. ChezMoi correctly detected that
drift and requested an overwrite choice that a noninteractive run could not give.

### Resolution

The tracked association is now `x-scheme-handler/fnlb=fnlb.desktop`, matching
the installed target. The broad `chezmoi apply` remains unforced, preserving
prompt protection for unrelated local configuration drift. A focused regression
test now guards the exact FNLB association.

### Verification

Completed: the focused regression passed, the target-scoped ChezMoi dry run did not prompt, and the full `refresh-config` workflow emitted `REFRESH COMPLETE`.

### Rollback

Restore only the previous `x-scheme-handler/fnlb` source line if the installed
FNLB desktop-file identifier changes again.

## Final Verification: 2026-08-24

- `bash tests/test_mimeapps_fnlb_handler.sh` passed after the source reconciliation.
- `chezmoi apply --dry-run ~/.config/mimeapps.list` completed without a TTY prompt.
- `fish -c 'source dot_config/fish/functions/refresh-config.fish; refresh-config'` completed and emitted `REFRESH COMPLETE`.
- `bash tests/test_refresh_config_function.sh` passed, preserving the existing refresh helper contract.
