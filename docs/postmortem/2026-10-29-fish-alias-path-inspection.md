# Fish shortcut source inspection

This report records harmless inspection errors while adding a directory shortcut and the verified source locations used instead.

- Symptom: rg reported missing guessed scripts/executable_refresh-config and dot_config/fish/config.fish paths; ls reported missing ~/.config/fish/key_dirs. A later optional AGENTS inventory returned no matches.
- Impact: read-only inspection noise; no user files changed by those probes.
- Lookup: searched postmortem-memory for "missing source path inspection". Finding local-discover-paths-before-reads applies: refresh-config is a Fish function and source paths must be inventoried.
- Evidence: read dot_config/fish/functions/refresh-config.fish and scripts/executable_sync-shortcuts successfully. The generator reads ~/aliases/key_dirs, not ~/.config/fish/key_dirs.
- Root cause: guessed locations instead of inventory-first discovery.
- Resolution/status: verified workaround; use the observed source paths. Shortcut deployment verification is tracked in the task response.
- Follow-up: no new learning beyond the existing path-discovery finding; avoid speculative optional-file reads.

## Deployment follow-up

- Default refresh failed with read-only home/runtime writes. An approved elevated refresh reached chezmoi but stopped on unrelated .config/mimeapps.list drift (EOF at overwrite prompt).
- Impact: full refresh incomplete; unrelated local file retained.
- Lookup: searched "fish startup read-only sandbox refresh" and "refresh conflict local file"; sandbox finding has limited applicability (different syscall); use approved execution and a scoped target to preserve unrelated drift.
- Next: deploy only ~/aliases/key_dirs and regenerate shortcuts with the existing helper; validate generated Fish syntax and exact abbreviation.

- Scoped apply reported key_dirs is not managed despite target-path resolving it; the deployment excludes this live file. Additional inspection repeated missing optional-path errors. Render the tracked template and compare against the live file before copying; retain chezmoi exclusions.

- Verification: rendered/live diff contained only the requested or directory mapping; copied reviewed rendering with approved access and ran the existing sync-shortcuts helper. Generated fish -n passed (exit 0). Full refresh remains blocked by unrelated mimeapps.list drift; scoped installation succeeded. No supplied command was executed.
