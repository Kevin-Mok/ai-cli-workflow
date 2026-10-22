# Discord speech with direction isolates

Normalize Discord's invisible Unicode direction isolates before extracting the sender and message, then deploy the shared callback. Keep visible sender parentheses, DMs, Codex/Grok routing and local speech unchanged.

## Context, scope and decisions

Live Dunst metadata confirms Vesktop channel titles wrap sender, channel and server in U+2068/U+2069. The existing literal ` (#` check fails and the Vesktop DM fallback speaks the whole title. Normalize only U+2066–U+2069; retain visible Unicode. Widen the coarse Dunst glob to route isolated channel titles from browser clients too; the Python parser remains authoritative. Add unit and private daemon regressions plus a synthetic CLI probe.

Initial git status captured. Protect all pre-existing dirty files, especially README, smoke tests, lessons and postmortem ledger; append only scoped changes. No commit/push requested. Default mode offers no Plan-mode switch; execute this bounded plan inline.

## Checklist

- [x] Inspect parser, callback, live metadata and prior DM incident.
- [x] Observe failing isolate regression before implementation.
- [x] Normalize isolates, route channel probes, update docs and incident learning.
- [x] Run focused checks; refresh and verify installed callback.
- [x] Private daemon GREEN after explicit user approval (one test, exit0).

## Verification, risks and rollback

Run `python3 -B tests/test_codex_notification_sound.py`, basedpyright on the helper, and private Dunst integration under Xvfb/D-Bus. Verify an installed synthetic isolate notification. Real incoming notification/listening remains separate. Roll back with `codex-notification-sound discord-speech disable`; preserve unrelated audio settings. Same-format apps can still match by existing design. No messages sent to others.

## Evidence and review

Postmortem lookup `discord notification speech`: local-vesktop-dm-notification-identity applies to routing but omitted invisible isolates. Live metadata establishes the parser boundary failure. Sandbox `dunstctl history` incorrectly reported no daemon; elevated access succeeded, proving access restriction rather than daemon downtime. See docs/postmortem/2026-10-22-discord-direction-isolates.md.

Suggested commit: `fix(notifications): normalize Discord direction isolates`.
Cursor prompt: Review plans/discord-isolate-speech.md and the scoped diff; preserve baseline dirty work, verify isolate normalization and private daemon routing, then check a new real Discord notification for sender-only speech.

RED evidence: unit81 with eight expected isolate failures; private daemon one test failed at expected playback12 versus actual11. GREEN focused exit0; basedpyright0 errors/warnings/notes. Broader290: four failures, one error, one skip; three localhost-bind restrictions, one known /h/k versus /h/e fixture, one tmux new-session error. Exact IDs are in the linked incident; no notification regression failed. Private daemon GREEN initially rejected by automatic approval review as outside image request scope. User explicitly approved the isolated test; rerun passed one test, exit0. No bypass attempted.

Deployment: refresh-config exit0 (/tmp/refresh-config.GyMNzuDk.log), explicit helper apply exit0, activation exit0. Source/live bytes identical; Discord enabled and Ryan ready. Installed observer /tmp/discord-isolate-runtime.py exit0: isolated channel and DM each WAV1/MP3 0, unrelated Voice WAV0/MP3 0. Installed parser returns exactly Alex says hello. Subjective listening/new real Discord receipt remain unverified. No commit/push. Documentation updated in README, notification guide, smoke checklist and incident learning. Concurrent staging in unrelated files was observed and left untouched.

Final review: scoped diff checked; no whitespace errors. All defining unit81/private Dunst1/type checks pass; broader environmental/baseline failures remain documented. Rollback is the existing independent Discord switch. No new dependencies or changes to visible sender names. Postmortem-memory targeted check passed.

## Live follow-up scope

- [x] Reproduce duplicate speech for a Vesktop channel title and fix shared routing.
- [x] Test-first silence normalized sender names SaucyBot and Twitter Cap Bot in channel/DM speech; preserve popups.
- [x] Repeat focused/private daemon checks, refresh/activate and installed probes with real Vesktop identity.

Follow-up evidence: daemon RED actual22 versus expected21 establishes overlapping script execution. Bot RED unit83/16 failures. Final GREEN unit83/private Dunst1/type0. Consolidated four script rules into one callback, retaining parser classification and suppression. No text-based deduplication/cache added. Refresh succeeded (/tmp/refresh-config.DsZxpBG4.log); installed acceptance passed: Vesktop channel WAV1, each ignored bot WAV0; MP3 0 throughout. Source/live bytes match. Suggested final commit: `fix(notifications): read Discord messages once and mute bots`.

## Volume follow-up

- [x] Compare application/output signal and Ryan TTS; exact Vole player slider unavailable.
- [x] Add defining attenuation/persistence/validation tests, observe RED, lower speech only.
- [x] Refresh, verify actual playback gain and document measured limits.

## Persistent volume control

User requests a command to set TTS volume. Add speech-volume [0..100] to the existing helper, persist it atomically in private speech-volume.json, report it in status and use it only for WAV speech. Missing/invalid settings default50. Empirical mpv PCM render: source at100=-16.08LUFS, at50=-34.13LUFS; 12 falls below meter gate. Native mpv curve is cubic, so the provisional12 setting was too quiet and is superseded by50. Current stream output sample=-31.26LUFS. Tests cover persistence, invalid input/schema, playback application and unchanged clip gain. No auto-ducking, browser changes or new dependencies.

Final volume choice: user heard replay at75 and explicitly requested default75. This supersedes provisional12 and measured-comparison50 settings. The persistent command accepts0..100 (including mute0), rejects invalid input without changing the previous setting, and falls back to75 for missing/malformed persisted data. The CLI applies to future notification speech across existing routes, with clips unchanged. Command/help/status/docs now agree. User already confirmed subjective playback75; exact Twitch slider unavailable, and fixed gain cannot follow future stream loudness changes.

Final command suggestion: `fix(notifications): read Discord once and add speech volume control`.
Cursor prompt: Review plans/discord-isolate-speech.md and the scoped diff; preserve unrelated dirty work, run85 focused notification tests/type check, verify speech-volume set/query/validation and a single synthetic Vesktop announcement, and retain bot exclusions and75 default.

Final verification:85 focused tests passed; basedpyright0 errors/warnings/notes. Private daemon1 passed the same implementation before the default-only change. Refresh exit0 (/tmp/refresh-config.tOQ2Nvsi.log); saved and fresh installed volume queries both75%; source/live bytes match. User confirmed playback75. All authorized implementation work complete; no commit/push requested or performed. Broader baseline/socket failures remain documented, and live fixed gain does not track stream loudness automatically.

## Authorized commit delivery

The user invoked commit-plan-push after the implementation summary. Include this plan, notification source/tests, README/smoke guide, incident and reciprocal reviewed learning in fix(notifications): read Discord once and add speech volume control. Fresh85 focused tests and basedpyright0 pass; earlier private Dunst1 and installed runtime/listening evidence remain recorded above. Code and installed helper match. Preceding series commits0028565 and82fc01c cover independent evidence/startup work. Next: exact candidate privacy check, final commit and one push to origin/main. See plans/discord-volume-delivery.md; no history rewrite is authorized.
