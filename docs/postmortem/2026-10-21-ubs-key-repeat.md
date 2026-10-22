# UBS keyboard repeat at i3 startup

Trace the reported slow repeat rate through the startup launcher, reproduce the lost setting, and verify the smallest correction.

- Symptom: the user reports that `ubs` at i3 startup does not apply the faster keyboard repeat setting.
- Impact: keyboard repeat remains slower than intended after desktop initialization.
- Lookup: `i3 ubs keyboard repeat xset` and `ubuntu-start` found `local-ubs-unattended-wallpaper-mount`. Its noninteractive startup boundary is relevant context, but its disk-mount remedy does not establish a keyboard fix.
- Diagnostic evidence: the first live `xset q` exited 1 with `unable to open display ":1"` inside the sandbox. This is an inspection access failure, not evidence that the user's X server is broken.
- Cause: `ubuntu-start` guarded `xset` behind both `XSET_*` exports, which are initialized in Fish rather than i3. The controlled startup test exited 1 with `expected startup repeat command "r rate 200 90", got ""` before the fix.
- Resolution: independently default absent/empty delay and rate to 200/90. Preserve nonempty overrides and optional-command skipping. Installed only this correction into the older live script through a task-scoped temporary chezmoi source and the existing `refresh-config`; it reported `REFRESH COMPLETE` and preserved unrelated live script differences. This host's non-GUI source configuration otherwise ignores desktop scripts.
- Verification so far: startup, keyboard-remap, i3 startup and pywal regression scripts passed. Bash syntax passed after the test runner initially guessed a nonexistent startup-file path (diagnostic command error only; corrected to the actual script). Live default, empty-variable and delay-override checks passed.
- Runtime probe correction: requesting rate 60 produced a server-reported 62, so the temporary probe's exact 60 assertion failed despite correct `xset` arguments. Its finally block restored defaults. Use a representable rate of 50 for the live override check; retain the command-boundary regression at 60 to verify exact argument forwarding.
- Final runtime verification: the corrected probe executed the actual installed script with a temporary HOME and PATH containing only real `xset`, avoiding desktop service side effects. Missing and empty variables produced 200/90; delay-only override produced 300/90; rate-only override produced 200/50; both overrides produced 300/50. All five live assertions passed, exit 0; finally restored 200/90. The command-boundary test also covers a missing optional `xset`.
- Status: verified_fix for the missing-environment startup behavior, runtime scope. No i3 process is running on this host, so an actual fresh-login/physical-typing check remains unverified.
- Next: at the next i3 login, confirm fast repeat before opening Fish. No restart was forced and no commit or push was requested.
- Learning: reviewed as `local-ubs-repeat-without-shell-exports`; keep command argument verification separate from the rates actually reported by the X server. Initial sandbox access failure was resolved by permitted host execution, not by changing X11 authentication.
