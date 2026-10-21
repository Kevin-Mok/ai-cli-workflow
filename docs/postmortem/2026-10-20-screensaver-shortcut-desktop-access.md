# Screensaver shortcut desktop access

Record the restricted desktop probe and its scoped recovery while adding Alt+Shift+S. Inspect live mappings, update only the shortcut, refresh configuration and reload i3.

- Symptom: restricted xmodmap could not open DISPLAY=:1; i3 IPC returned Operation not permitted. No configuration had changed.
- Impact: live mapping and activation checks require scoped approved execution.
- Lookup: searched `xmodmap unable open display X11 sandbox`; reviewed the keycode-108 X11 incident and local-i3-probe-ipc-unicode. The execution-context workaround applies; Unicode workspace restoration is unnecessary because this task changes no workspaces.
- Evidence: the same probes under scoped approved execution exited 0; keycode64 is Alt_L in Mod1; i3 is4.23.
- Status: verified access workaround; default sandbox unchanged. No new learning beyond the existing scoped-access incident.
- Shortcut scope: preserve Super+Shift+S; add Mod1+Shift+S on release. Live i3 is unmanaged by chezmoi, so patch only that line without importing private machine configuration into public source.
- Verification: defining assertion failed because the Alt binding was absent before implementation. Live configuration validation exited0 (existing wheel command deprecations), refresh completed, and i3 reload returned success. Runtime verification passed: a real Alt+Shift+S event launched the expected command, the screensaver window appeared, and Escape dismissed it (exit0).

## Probe assertion correction

The first live shortcut probe received the correct launcher event with `event_state_mask=[shift, Mod1]`, but its assertion expected capitalized Shift and exited1. This is a diagnostic casing error, not a shortcut failure. Existing local-i3-probe-ipc-unicode guidance supports checking actual event evidence. Normalize modifier names in the probe, cover preview dismissal in cleanup and repeat. No new reusable learning is needed beyond consuming the actual IPC payload.

Final verification: focused independent checks4/4passed for both release bindings, no conflict and matching docs. No broad media regression suite was needed for the one-line declarative addition. Physical keyboard acceptance remains manual; the injected X11 chord is verified. No commit or push requested. Rollback removes the new Alt binding from tracked and live i3 configuration and reloads i3.

Ledger registration probe initially supplied a file to scan --root, which requires a directory; no data changed. Corrected to the postmortem directory and selected this report from its scan results. This is a local invocation correction with no additional generalized learning.

## Commit-session Git permission boundary

The first staging attempt could not write a Git object: unable to create temporary file, Read-only file system (exit128). No index changes were made; the environment explicitly mounts .git read-only. This matches the known execution-context permission boundary rather than a repository content defect. Use scoped approved execution for Git object/index writes and commit/push; preserve all unrelated hunks. Learning remains no-new-learning because this is an explicit sandbox boundary.

## Public candidate privacy review

The required pre-commit privacy gate blocked one home_path finding in the new ledger alias; no commit was created. Existing public ledger aliases use a placeholder home directory. Sanitize only this candidate alias to that established public form, preserving the real local alias in the working ledger for targeted local checks. Update the candidate report hash and rerun the exact staged gate. This is privacy minimization, not a scanner bypass; no private path is published.
