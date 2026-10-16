# Notification speech blocked by a missing clip

Restore silent notification audio by checking the selected clip first, choosing an existing local copy, then verifying both offline synthesis and desktop playback.

## Symptom and impact

The user could see notifications but heard neither the question clip nor spoken text. Repeated live error-log entries reported a missing configured checkout MP3. Popup delivery continued normally.

## Lookup and evidence

- Query: `notification silent speech audio voice playback` using the tracked postmortem-memory helper.
- Reviewed `local-audio-sink-mute` and `local-notification-user-facing-completion`: applicable diagnostic boundaries, but no evidence for their remedies here. Desktop output was unmuted at volume 0.60; errors instead named an absent configured MP3.
- Installed `codex-notification-sound status --details` reproduced the failure (exit 1). `sound.json` selected the checkout clip, which is absent; the matching installed clip exists in `~/scripts` (27,046 bytes). Speech remains enabled and Ryan voice/runtime files exist.
- `play()` calls `configured_clip()` before synthesis or playback, so validation failure blocks both stages. Dunst remains silent in speech mode because the event bridge owns audio.
- Initial sandboxed pactl/wpctl diagnostics could not access desktop sockets. Repeating read-only diagnostics with approved desktop access succeeded; this was a diagnostic restriction rather than the audio cause.

## Root cause and resolution

The machine-local selection referred to a checkout asset that is no longer present. The existing installed clip was retained, so `codex-notification-sound set "$HOME/scripts/can-i-ask-you-a-question.mp3"` repaired the path. No player, voice, service, hook or event-policy change was necessary. The exact operation that removed the checkout asset was not established.

Recovery is verified. Keep selected audio outside the checkout and check clip existence before investigating speech or hook wiring when both stages are silent. Preserve unrelated workspace changes.

## Verification

- Installed `status --details`: exit 0, sound and speech enabled, Ryan ready, installed clip selected. Historical missing-path errors remain in the log; no log was erased.
- Installed `setup-codex-notification-speech --check`: exit 0, offline Piper 1.8.0 synthesis ready.
- Installed `preview --title "Notification audio is restored" --details`: exit 0. The user explicitly confirmed hearing both the clip and spoken sentence.
- Installed notification CLI probe: 14/14 cases passed, exit 0. Installed question probe: 6/6 passed, exit 0. The parent independently repeated the accepted-question case: two silent playback calls and exact expected question text, exit 0. These fixtures check routing, ordering and exclusions rather than physical output.
- The defining reproducer was installed status failing on the absent configured clip before the local setting repair, then succeeding afterward. Existing behavior was sufficient; no source-code change or new test was needed.

## Documentation and follow-up

Corrected stale bundled-clip claims in the notification guide and shared smoke checklist; added the missing-path recovery note to README. Record this failure mode in tracked postmortem memory and local lessons. No tracked runtime configuration changed, so refresh-config deployment is unnecessary. The subsequent `commit-session` request authorizes a scoped documentation commit and upstream push.

## Limits and rollback

Audible preview is user-confirmed; a subsequent naturally occurring completion or question remains a separate end-to-end acceptance check. To silence configured audio, use the existing `disable` command; to restore popup-only clip behavior, use `speech disable`. Both preserve the MP3. Do not reselect the absent checkout path.

## Commit validation follow-up

The focused `python3 -B tests/test_postmortem_memory.py` run completed 26 tests: 25 passed, one failed. `WorkflowTest.test_actual_ledger_reference_status_and_coverage` expects the sanitized default roots `/home/example/coding` and `/home/example/linux-config` to exist and resolves historical public aliases as physical machine paths. Those roots are absent here; this coverage check is a pre-existing environment/alias limitation, separate from notification playback. Do not rewrite historical reports, weaken the test, or bundle unrelated fixes into this session commit. The focused current-report check passed before the shipping review. Public ledger aliases and plan examples must use neutral home paths; machine-local alias translation belongs in temporary private validation data.
