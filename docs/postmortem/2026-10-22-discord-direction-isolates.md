# Discord channel metadata spoken aloud

Normalize invisible direction isolates before recognizing Discord channel titles, then verify the shared parser and deployed notification route.

## Symptom, impact and evidence

Vesktop channel notifications speak channel/server metadata instead of just sender says message. Live Dunst metadata contains U+2068/U+2069 around all title fields. The literal ` (#` delimiter is absent, so the existing Vesktop DM fallback uses the whole title. Use public synthetic names in fixtures; do not retain private messages.

## Lookup and current status

Postmortem query `discord notification speech` returned local-vesktop-dm-notification-identity. Its observed Vesktop identity remains applicable, but its sender-only fallback omitted isolated channel titles. Fresh regression required before remedy.

The sandbox history probe returned `Dunst is not running` and its JSON consumer failed on empty output. Elevated Dunst history succeeded; this was a sandbox D-Bus access limitation, not daemon downtime. No daemon was restarted for diagnosis.

## Resolution and verification

Removed U+2066–U+2069 before visible-text normalization and suffix parsing. Widened the coarse Dunst glob for isolates before #; full parser validation remains. Added a reusable discord-isolates probe and guide/smoke documentation.

Expected RED: 81 unit tests with eight isolate subtest failures; private Dunst expected playback 12 but observed 11. The private daemon probe also needed elevated D-Bus access, consistent with the recorded sandbox limitation.

Unforced refresh-config succeeded (log /tmp/refresh-config.GyMNzuDk.log), helper applied and Dunst activation succeeded. Source/live helper and dunstrc match byte-for-byte. Discord speech remains enabled, Ryan ready and original Codex settings unchanged. Installed parser produced exactly Alex says hello. Installed synthetic channel and DM probes each launched one WAV and zero MP3 players; unrelated Voice probe launched zero players. Runtime observer /tmp/discord-isolate-runtime.py exited 0.

Focused notification tests passed (81/81); basedpyright reported 0 errors/warnings/notes. Automatic approval review rejected the elevated private Dunst GREEN run as outside the image request scope; the user then explicitly approved it and the isolated GREEN rerun passed (one test, exit 0). Broader discovery ran 290 tests: four failures, one error, one skip. Three failures could not bind localhost: test_actual_cli_guardian_update_preserves_query_uuid_and_cached_generation_cap, test_async_recap_preserves_query_and_uuid_and_ctrl_g_requests_selected, test_all_provider_free_actual_cli_startup_scenarios. test_directory_abbreviation_keeps_basename_and_full_preview expected /h/k but fixture /home/example produces /h/e (known baseline). test_visible_and_hidden_panes_forward_wrapped_osc9 errored on tmux new-session (socket access). These tests do not exercise Discord parsing; no unrelated fixes attempted. Explicit user approval allowed the isolated private daemon GREEN rerun: one test passed, exit 0.

Status: verified runtime fix for synthetic fixtures; private Dunst GREEN passed after explicit approval. Subjective listening and a new real message remain separate checks. No messages were sent to others.

## Learning

New finding local-discord-direction-isolates records the boundary normalization and coarse route regression. Runtime evidence covers installed synthetic playback; private daemon GREEN passed after approval; subjective real-message acceptance remains unverified. The reviewed source hash and reciprocal finding are recorded in tracked memory; targeted ledger check passed.

## Duplicate playback follow-up

User reported the same message read twice after deployment. Hypothesis: isolated Vesktop channel titles now match both format and Vesktop script rules. Existing installed positive probe used FormatProbe, missing this overlap. Investigate daemon script accumulation and add an exact Vesktop channel regression before remedy. Lookup dunst multiple scripts duplicate rules returned local-dunst-stacked-script-state; that concerns history replacements rather than simultaneous callbacks, so it is not an established remedy. User also requested silent SaucyBot and Twitter Cap Bot senders; apply this only to speech, preserving popups.

Confirmed duplicate cause: installed Dunst1.9.2 scripting docs specify a script runs for every matching rule. New private-daemon RED observed22 playbacks instead of21 for one Vesktop channel message. The isolate fix exposed the existing format/Vesktop overlap; FormatProbe-only acceptance did not cover it.

Final resolution: consolidate four overlapping script rules into one notification_audio callback. Existing Python dispatch still classifies Codex/Grok/Discord and ignores unrelated notifications. Do not deduplicate message text: identical messages can be legitimate separate deliveries. Normalize the parsed sender and skip exact case-insensitive SaucyBot/Twitter Cap Bot names for channel and Vesktop DM speech; preserve popups and similarly named human senders.

Bot-filter RED: unit83 with16 expected subtest failures. Final GREEN: unit83 pass, private Dunst1 pass (single Vesktop channel announcement plus both bots silent in channels and DMs), basedpyright0 errors/warnings/notes. Earlier broad socket/path failures remain unrelated and unchanged. Refresh-config succeeded again, log /tmp/refresh-config.DsZxpBG4.log; helper applied and Dunst activated. Final installed observer exited0: Vesktop isolated channel WAV1/MP3 0, SaucyBot WAV0/MP3 0, Twitter Cap Bot WAV0/MP3 0. Source/live helper and dunstrc match byte-for-byte; diff whitespace check passes. Subjective listening and a new incoming message remain manual.

## Requested volume calibration

User reports TTS louder than Twitch and requests it slightly quieter. Sandbox pactl sink/input inspection failed with Operation not permitted/Connection refused, consistent with the established desktop socket boundary. No volume changed. Query actual desktop audio with normal escalation before choosing attenuation; compare browser volume and live signal levels.

Volume evidence: PulseAudio Chrome input100%, output45%; browser automation exposes a directory tab rather than the actual stream player. User confirms stream playing in Chrome. Per-input parec monitoring returned silence twice, even on the matching sink; do not infer Twitch is silent from that capture. Direct output-monitor measurement is in progress. Ryan sample approximately -15.5 LUFS and +0.1 dBTP before gain. No audio recording retained.

### Volume calibration resolution and command

Direct sink-monitor sample measured -31.26LUFS. Raw Ryan measured about -15.5LUFS. Crucially, actual mpv PCM rendering showed its nonlinear scale: volume100=-16.08LUFS, volume50=-34.13LUFS, volume12 below the integrated-loudness gate. The provisional12 assumption treated percentages as linear amplitude and was corrected before final acceptance. Use measured playback, not slider arithmetic. The actual Vole Chrome profile has no available debugging connection here; browser-volume attribution is limited, while speaker-monitor and TTS render measurements are established. No browser settings changed or captured audio retained.

Added speech-volume [0..100] to the shared helper, with private atomic speech-volume.json persistence, query-only mode, status output, validated integer range and safe missing/malformed fallback. WAV speech uses the saved software gain; intro clips/browser/system levels remain unchanged. One extracted atomic writer preserves existing enable/disable semantics.

Volume command RED: missing CLI and old gain; GREEN85 unit/private daemon1/type0 at initial50 default. Installed command set/query50 succeeded; real player observed exactly one WAV with --volume=50, no MP3. User then selected75, requested another test, and explicitly confirmed default75 after hearing it. Installed set75 and synthetic replay succeeded. Default-change RED: two failures expected75 versus50. Final source default/help75, docs updated; final85 focused tests pass and basedpyright reports0 errors/warnings/notes. Unforced refresh completed (log /tmp/refresh-config.tOQ2Nvsi.log); installed saved and fresh-config queries both report75%, and source/live helper bytes match. Earlier broad290 failures remain documented above.

## Delivery plan filename collision

While preparing commit-plan-push, Add File reused plans/dirty-worktree-delivery.md without checking tracked existence, temporarily replacing its earlier delivery milestones. Candidate diff review exposed the replacement before commit. Lookup plan path overwrite existing file returned ext-optional-path-discovery; inventory-before-write applies. Read the existing HEAD plan, restored its exact bytes (it was clean at task start), and exclusively created plans/discord-volume-delivery.md. No earlier milestone or user edit was lost. Existing path-discovery/ownership guidance covers this recurrence; no new general finding is required. Private candidate plan paths were updated before staging again.

## Concurrent ledger parse failure during delivery

The final candidate merge preserved the new TCU report, then parsing the live working sources.json failed with Invalid escape at line42/column34. No final commit was attempted. The isolated candidate JSON remains parseable; inspect the live malformed escape and preserve concurrent ledger edits before retrying. Existing JSON-boundary and shared-worktree lessons apply; record the exact remedy and fresh targeted checks after diagnosis.

Follow-up diagnosis: the live ledger parsed successfully on the next read and contained all228 findings; no persistent malformed value was established. Treat the single failed parse as a transient shared-file read during concurrent work, not a repaired product bug. Take a stable byte snapshot, guard it against subsequent modification, and publish only a merged candidate retaining the concurrent TCU record. This report and both local/public source hashes are updated together; final targeted validation follows.
