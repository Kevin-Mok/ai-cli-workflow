# Notification Fish inspection triggered sandbox startup writes

An inspection of the notification configuration started normal Fish initialization,
which attempted writes outside the workspace. Use a clean Fish process for scoped
inspection, and request the normal approved route for configuration deployment.

## Symptom and impact

During the three-mode notification task, `fish -c 'functions -q refresh-config;
and functions refresh-config'` printed the requested function and returned zero,
but startup emitted read-only-filesystem errors. No notification implementation
failure was established; the diagnostic output made the inspection noisy.

## Evidence and cause

- Startup could not create fnm multishell links under
  `/run/user/1000/fnm_multishells/`.
- Fish reported inability to open its universal-variable file at `/`.
- Shortcut initialization raised `OSError: [Errno 30] Read-only file system`
  when writing `/home/kevin/aliases/.key_aliases`.
- The task sandbox permits repository and temporary writes, while these startup
  destinations lie outside that scope. Normal Fish initialization ran incidental
  setup even though the requested command only inspected a function.
- A combined source lookup also found no
  `dot_config/fish/functions/sync-shortcuts.fish`; the actual helper is
  `/home/kevin/scripts/sync-shortcuts`, tracked as
  `scripts/executable_sync-shortcuts`. This was a lookup miss, not a helper failure.

## Lookup and applicability

Searched the tracked postmortem helper for `fish startup fnm read-only sandbox
universal variables` and then `fish fnm read-only`. The
`ext-sandbox-loopback` finding in `references/execution-environments.md` supports
distinguishing execution restrictions from application failures and using scoped
approved commands when necessary. Its loopback failure is a different mechanism;
it does not prove this Fish command would recover through escalation.

## Resolution and verification

The clean-shell inspection
`fish --no-config -c 'source dot_config/fish/functions/cli-message.fish;
cli-message 🔔 "Clean Fish ready"'` returned zero without startup errors.
This verifies the inspection workaround only. The underlying sandbox remains
restricted. An approved escalation of
`fish --no-config -c 'source dot_config/fish/functions/cli-message.fish;
source dot_config/fish/functions/refresh-config.fish; refresh-config'` returned
zero and completed every refresh step with `REFRESH COMPLETE`; its private log
is `/tmp/refresh-config.R7vPFrpM.log`. Installed block and audio-player files
byte-match their sources. No shell startup or sandbox policy was changed.

An approved live Dunst probe returned DND with one queued notification for
button 3, Silent for button 2, and Notis for button 1. State queries matched
each mode, and the original state was restored: Dunst unpaused, mute marker
absent. This validates control/state behavior, not physical sound or visual
desktop appearance; neither was directly inspected.

## Status and next steps

Status: verified workaround for clean-shell inspection and successful approved
configuration refresh. Continue with `fish --no-config` and explicit dependencies
for scoped inspection; preserve the approved command route for outside-workspace
writes. Physical audio/visual acceptance remains manual. Do not treat a zero
command exit as proof that startup diagnostics were harmless.

Learning decision: no new general remedy beyond existing execution-boundary
guidance. Record the narrow clean-Fish workaround without promoting it to a fix
for sandbox permissions or live deployment.
