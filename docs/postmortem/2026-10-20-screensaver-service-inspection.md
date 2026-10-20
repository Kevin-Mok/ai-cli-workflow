# Screensaver service inspection path

A read-only inspection guessed `scripts/executable_refresh-config`, which does not exist. No runtime state changed.

- Symptom/evidence: cat returned exit 1 for that path while screensaver source reads succeeded.
- Impact: inspection only; service work continues.
- Lookup: query `missing script path refresh-config` matched `local-discover-paths-before-reads`; applicable because refresh-config is a Fish function.
- Cause/resolution: guessed an executable path; use repository inventory from the search agent for the real Fish function.
- Verification: screensaver source and documentation were read successfully; no product failure occurred.
- Follow-up: discover paths before reads. No new learning beyond the existing path-discovery finding.

## User bus sandbox restriction

A read-only `systemctl --user is-system-running` failed with `Failed to connect to bus: Operation not permitted` (exit 1). DISPLAY=:1 and XAUTHORITY point to the live desktop. This is sandbox access, not evidence that systemd or the screensaver failed. Use scoped approved execution for live service operations; no service action was attempted by the failed probe.

## Additional environment evidence

- First Xvfb regression run: 30 passed, eight GUI cases could not open the sandboxed display. Scoped retry passed all 38; browser and desktop checks passed too.
- Legacy runtime status referenced PID 2546817, but `/proc/2546817` no longer existed. Reading its metadata returned FileNotFoundError; no PID was signalled. Treat status as stale and use systemd MainPID for recovery checks.
- Required `fish -c refresh-config` exited 1: chezmoi found a locally changed `.config/mimeapps.list`, prompted, then reached EOF. Preserved that unrelated file; explicit screensaver install succeeded, including live i3 service startup migration. Full refresh remains blocked by unrelated local drift.
- Scoped service activation succeeded: systemd reported active/running with MainPID 2681574. CLI confirmed the daemon running; automatic activation remains suppressed because the browser bridge is unavailable. This is existing fail-closed behavior.

Resolution: scoped live execution handles the sandbox; explicit installation handles screensaver deployment without overwriting unrelated local config. No additional reusable learning beyond existing path-discovery, stale-state and execution-environment guidance. Full refresh and browser bridge enablement remain operator acceptance items.

## Legacy-daemon migration

The first recovery signal returned `No main process to kill`: journal showed `Idle monitor is already running` and five-second restarts. The legacy daemon was alive outside the sandbox process namespace, so the earlier `/proc` absence did not prove a stale PID. Scoped inspection confirmed UID 1000 and exact command `python3 /home/example/scripts/media-screensaver daemon` for PID 2546817. After verifying UID and argv again, TERM stopped only that daemon. The service took ownership as PID 2683032 and reported the five-minute idle monitor running. No broader process kill or bypass of duplicate locking was used.

## Follow-up: Chrome bridge unavailable at 14:49

User reported continued unavailable-bridge messages and idle 0–1 seconds. Lookup query `screensaver browser bridge unavailable native host` returned no directly applicable bridge-install finding. Read-only scoped inspection confirmed native-host manifests and launcher exist, no bridge state files are published, and the expected extension ID is not registered in saved Chrome profile Preferences/Secure Preferences. No browsing content was printed. The separate source investigation confirmed the installer writes the host but Chrome requires the explicit Load unpacked step.

Root cause supported by observed metadata: browser extension setup is pending, rather than service startup failure. Clarified the guide and smoke check: complete Load unpacked in each profile and reload tabs; normal physical input explains idle 0–1 seconds. No service/gate code changed and no fail-closed check was bypassed. Status remains activation_pending until the user loads the extension and status confirms bridge coverage. No new general learning beyond the existing documented manual extension-install requirement.

## Immediate ss shortcut follow-up

The fish-alias helper previewed/applied `ss ~/scripts/media-screensaver preview` in the existing power options section, commenting its previous slideshow definition. A guessed sync-shortcuts Fish-function read failed; source mapping located the actual external script. The required refresh again stopped on the known unrelated mimeapps.list conflict. Targeted chezmoi diff then reported the live aliases file is not managed (its ignore policy excludes it). Rendering showed broad unrelated live/template differences, so no full alias replacement was performed. Instead, updated only the exact active ss line in the live aliases file, preserving the old mapping as a comment, and regenerated shortcuts using the installed sync-shortcuts. Fish syntax check exited 0. An attempted filtered `abbr --show ss` listed all abbreviations on this installed Fish; use output filtering rather than assuming this flag filters names. No supplied preview command was executed.

No new learning: existing path-discovery, local-drift and CLI-option-verification guidance applies. Documented the ss mapping in guide/README/smoke checks.

Shortcut verification correction: a regex filter used a literal Unicode escape unsupported by PCRE2. Replaced it with Fish glob matching. Fresh `fish --no-config` source plus `abbr --show | string match "abbr -a -- ss *"` exited 0 and printed only `abbr -a -- ss '~/scripts/media-screensaver preview'`. No runtime command executed.

## Commit privacy check

The pre-commit privacy gate blocked three home_path findings in this session's report, plan and ledger alias. Replaced machine-specific home paths with canonical example paths before restaging. No credential or runtime behavior change was required. Initial scope helper could not attribute wrapped tool writes; scoped hunks use direct conversation edit evidence. The final gate result is recorded in the plan.
