# Discord direct messages skipped by speech

Trace sender-only notifications through Dunst routing and the speech parser, add app metadata recognition, then verify and deploy the existing local voice path.

## Symptom and impact

User hears no speech for Discord DMs displayed as sender plus message. Channel-format speech was previously installed and enabled; DMs were explicitly excluded from that matcher.

## Evidence, lookup and cause

Privacy-safe live Dunst history inspection found appname `vesktop`, nonblank title/body and no channel suffix. No sender or body content was printed or saved. Discord speech enabled, Ryan ready and Dunst unpaused. Source/live helper and dunstrc identical. Both coarse Dunst rule and Python classifier require the channel suffix, so DM callbacks never reach playback.

Postmortem-memory query `discord notification speech direct message` returned Codex provenance and unrelated Discord bot findings. local-notification-user-facing-completion applies to Codex, not this desktop DM classifier. Missing-clip lesson is inapplicable because the notification fails routing before audio. Fresh executable regressions will establish the fix. An optional source glob lookup scripts/*refresh* had no matches; the actual refresh function was located without changing runtime state.

## Resolution and verification

Added exact `vesktop` routing and nonblank visible sender/body fallback in the shared parser, preserving channel validation, independent switch, markup safety and speech-only playback. Added smoke discord-dm and updated guide/README/smoke checks.

- Expected RED: unit79 had two inherited no-play failures; private Dunst expected20 but saw19.
- GREEN: unit79/79; private Dunst1/1, verifying speech-only DM, app lookalikes, unknown apps and disabled state; basedpyright0 errors/warnings/notes. Diff whitespace check passed.
- refresh-config completed, log /tmp/refresh-config.jtU4Z4rB.log; helper applied and Dunst activated, exit0. Installed helper/config bytes equal source; switches enabled and Ryan ready.
- Installed synthetic DM: callback observed, one real WAV player, zero MP3 players, no new error-log bytes. Installed negative fixture: zero new players in three seconds.
- Status: verified runtime routing and synthesis/playback for synthetic fixtures. New real incoming DM and subjective listening remain pending. Vesktop non-message title/body notifications may also speak.

## Broader validation failures

Broader Codex discovery: 288 tests, 287 pass; existing test_directory_abbreviation_keeps_basename_and_full_preview expects /h/k but fixture /home/example abbreviates to /h/e. Postmortem suite:26 tests,25 pass; test_actual_ledger_reference_status_and_coverage references unavailable /home/example/coding and /home/example/linux-config roots and historical sources. These are path-dependent baseline issues, unrelated to notification routing. No broad fixture or historical-source migration attempted. Targeted source ledger check is the applicable validation for this report. Preserve the failures in handoff; follow up separately if those fixture paths need migration.
