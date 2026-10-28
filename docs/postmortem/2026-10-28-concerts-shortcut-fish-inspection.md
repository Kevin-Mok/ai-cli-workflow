# Concerts shortcut: Fish inspection sandbox failure

A configured Fish inspection ran startup hooks inside a read-only home sandbox. Use startup-free Fish for inspection and approved filesystem access for deployment.

- Symptom/evidence: `fish -c` printed fnm multishell, universal-variable and alias-generation read-only filesystem errors while inspecting functions; the outer process returned 0.
- Impact: inspection output was noisy; no successful deployment was established.
- Lookup: searched `fish inspection read-only filesystem`; reviewed the existing 2026-10-23 agent-policy Fish inspection incident. The same configured-shell startup side effects apply.
- Root cause: invoking configured Fish for a read-only function lookup runs writable startup hooks.
- Resolution/status: read the tracked function directly; use `fish --no-config` with explicitly sourced functions for subsequent inspection/deployment. Startup-free verification remains the next step.
- Learning: no new learning; existing environment-isolation guidance and the prior inspection incident cover this recurrence. Runtime shortcut deployment is verified separately in task output.

- Deployment follow-up: `chezmoi diff /home/kevin/aliases/key_dirs` returned 1 because the live alias file is migration-preserved/unmanaged. Full `refresh-config` then returned 1 at an unrelated `.config/mimeapps.list` conflict (private log `/tmp/refresh-config.7kVcimZ7.log`). Preserved that conflict and all existing live alias rows; added only the requested mapping to the live personal section, regenerated with installed `sync-shortcuts`, and sourced abbreviations using startup-free Fish. Fish syntax and `abbr --query cnc` passed (exit 0). Full refresh remains blocked by pre-existing local drift. No new learning: existing migration-preserved-target and refresh-conflict guidance applies.

- Commit follow-up: ordinary sandbox staging could not write Git objects or `.git/index.lock` (read-only filesystem). No candidate was staged. Git metadata is explicitly read-only in this workspace profile; retry staging/commit with approved repository-metadata access. This is a permissions limitation, not a shortcut defect.
