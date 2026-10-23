# Redshift temperature notifications in i3

Implement this request in /home/kevin/linux-config: “when using redshift in i3 i want a noti that shows what temp its at like in dunst”.

Make the existing i3 Redshift controls show a Dunst desktop notification with the resulting color temperature in kelvin after a successful operation. Assume notifications are wanted for manual i3 adjustments, presets and reset; do not add a background monitor or periodic notifications.

Start from these repository sources and inspect their current contents:
- dot_codex/AGENTS.md: canonical repository instructions.
- scripts/executable_redshift-control: existing shared set/adjust/reset controller; currently persists the last successful value and prints it to stdout.
- dot_config/i3/config.tmpl: existing Redshift key bindings call that controller.
- dot_config/fish/functions/redshift-set.fish: existing wrapper also calls the controller.
- tests/test_redshift_control.py and scripts/smoke_redshift_keys.py: existing verification surfaces.
- plans/i3-redshift-arrows.md and docs/smoke-tests.md: existing behavior and manual checks.

Inspect existing Dunst/notify-send patterns and use the smallest compatible integration, preferably at the existing shared success path. Preserve current keys, limits, persistence, terminal behavior and fish callers. Use the applied successful temperature rather than an unapplied requested value; never display a success notification when Redshift fails. Repeated adjustments should replace the same notification instead of building a queue. A missing or failed notification service must not turn a successful temperature change into a failure.

The working tree already contains staged and unstaged work, including the controller and related config/tests/docs. Capture current status and preserve it; extend the current implementation without reverting or committing unrelated changes. This request does not ask for a commit or push.

Follow applicable instructions for test-first implementation, focused regression checks, documentation and configuration refresh. Cover successful set/adjust/reset, clamped temperatures, Redshift failure, and notification failure with focused tests. Verify a real Dunst notification in the live i3 session when available, without unnecessarily changing the user's temperature; report runtime limitations accurately.

Report what changed, the notification text and triggering controls, verification results and remaining limitations. Include this saved prompt's path in the final handoff. Do not invoke metaprompt-run or recompile this task.
