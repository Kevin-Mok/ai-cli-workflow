# Hevin shortcut activation and refresh

Apply the new i3 launcher while preserving unrelated local configuration. Inspect refresh failures, use a narrowly scoped binding insertion when full refresh encounters existing differences, and verify live i3 configuration.

## Symptom and impact

Initial sandboxed fish invocation loaded startup hooks that could not write fnm, fish variables or generated aliases outside the workspace. Refresh exited 1. The repository shortcut exists; live activation is pending.

## Evidence and current status

`fish -c 'source .../refresh-config.fish; refresh-config'` exited 1 with read-only filesystem errors and a private refresh log. No unrelated changes may be adopted. Next: consult reviewed memory, retry refresh with clean fish startup and desktop filesystem permission, then preserve local i3 settings when installing the single binding.

## Resolution and lookup

Lookup `refresh-config fish startup sandbox mimeapps` matched reviewed shell/sandbox guidance; read-only filesystem diagnostics confirm the boundary applies. Clean `fish --no-config` with explicit helper sourcing and approved home access completed refresh (exit 0, REFRESH COMPLETE). No MIME conflict occurred this time.

i3 validation exited 0 with pre-existing wheel command deprecation warnings, and reload returned success. The following inspection failed because `i3-msg get_config` defaults to formatted output rather than JSON; use `i3-msg -r -t get_config`. This is an inspection-format mistake, not an activation failure.

The refreshed live i3 file still lacked the binding; `chezmoi source-path` confirmed it is unmanaged. A scoped insertion preserved all existing content (rollback copy `/tmp/hevin-i3-rollback.config`). Validation exited 0, reload returned success, and raw IPC configuration confirmed exactly one release binding (exit 0). Existing wheel command deprecations are unrelated. The initial JSON schema inspection also assumed a nonexistent ledger `sources` key; inspecting actual keys showed the established `reports` schema before updating it.

No new learning: these outcomes repeat existing sandbox-boundary, source-ownership and observed-contract guidance. No screensaver logic changed. Physical-key visual acceptance remains manual.
