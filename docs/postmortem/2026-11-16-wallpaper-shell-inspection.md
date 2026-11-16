# Wallpaper shell inspection restrictions

A wallpaper configuration inspection invoked Fish startup inside the restricted sandbox. Use configuration-free Fish for read-only inspection and approved access for live deployment.

- Symptom: Fish startup emitted read-only errors for fnm multishells, universal variables and aliases; a speculative search also named a nonexistent script glob.
- Impact: inspection was noisy; no wallpaper deployment had occurred.
- Evidence: `fish -c 'functions refresh-config'` returned the function but startup attempted writes outside the workspace. The tracked and live ubuntu-start scripts compared equal before editing.
- Lookup: searched `fish sandbox read-only fnm`; reviewed ext-sandbox-loopback in execution-environments.md. Applicable permission-boundary principle; this incident occurs during shell startup, not loopback setup.
- Cause: configured Fish startup has side effects even for a function inspection.
- Resolution: use bash source reads for inspection; request scoped approved execution for home deployment and refresh.
- Additional deployment blocker: chezmoi dry-run reports inconsistent state because both dot_config/mimeapps.list and dot_config/private_mimeapps.list map to .config/mimeapps.list. These are pre-existing unrelated files; neither was removed or overwritten. Required refresh is being attempted; wallpaper script deployment uses a direct scoped install.
- Learning: no new general learning beyond the existing scoped sandbox escalation guidance. Do not infer deployment success from a shell inspection exit code.
- Verification: startup regression and bash syntax checks pass. Live startup script equals tracked source. apply-pywal-theme reports wallpaper set, and ~/.cache/wal/colors.json names fn-jonesy-cool.jpeg. Required refresh-config exits 1 on the pre-existing duplicate MIME destination; scoped install succeeded. Fresh graphical login remains untested.
