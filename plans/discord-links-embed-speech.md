# Short Discord tweet and link announcements

Announce only the sender and kind for Discord links and SaucyBot notifications. Update the shared parser, checks and documentation, then deploy the reviewed helper and verify local Ryan playback.

## Outcome, context and scope

The latest user correction supersedes the original request to read SaucyBot tweet contents: say exactly `SENDER sends tweet` or `SENDER sends link`, without contents or URLs. SaucyBot nonblank notifications announce tweet. Other notifications with an X/Twitter status URL announce tweet; other scheme/www links announce link, including URL-only bodies and markup link targets. Ordinary text keeps `SENDER says MESSAGE`. Twitter Cap Bot remains muted. Nothing is fetched. Source is scripts/executable_codex-notification-sound; callers are the existing single Dunst callback and CLI smoke modes.

Initial status captured on both turns before edits. Protect baseline dirty plans, prompts, postmortems and learning ledger/references, plus untracked memory. Preserve first-turn scoped changes. No commit/push requested. Default mode has no Plan-mode switch; execute this bounded decision-complete plan inline. Docs: README, docs/codex-notification-sound.md and docs/smoke-tests.md.

## Decisions and risks

Classify links from raw body to include hidden href destinations, but normalize sender and validate the same existing title/body structure. Recognize X/Twitter status URLs by explicit domain and status path; profile URLs and lookalike domains remain generic links. SaucyBot identity is a notification label, not authentication. Preserve independent enable switch, volume, local voice, suppression, locking, Unicode normalization and one callback. Sender-only DMs still require exact vesktop identity. No image OCR or embed fetching.

## Checklist

- [x] Capture baseline and inspect parser/callers/docs/prior incidents.
- [x] Observe first-turn RED89/22 failing subcases, implement URL omission and unmute SaucyBot.
- [x] Verify first-turn focused89/broader111/type0/private Dunst1 and installed WAV1/1/0.
- [x] Apply latest correction; observe RED89/54 failing subcases before implementation.
- [x] Replace body-reading/sanitization with sender-and-kind announcements; update docs and private checks.
- [x] Run final focused/broader/type/private daemon checks.
- [x] Run required refresh, deploy exact owned helper and verify installed callback.
- [x] Reconcile incident learning, diff and final evidence.

## Verification

Automated commands: `python3 -B tests/test_codex_notification_sound.py`; `python3 -B -m unittest discover -s tests -p 'test_codex_notification*.py'`; `basedpyright --level error scripts/executable_codex-notification-sound`; `xvfb-run -a dbus-run-session -- python3 -B tests/scripts/codex_notification_daemon_check.py`. Tests agent runs these; inspect reports and runtime evidence. Private socket access requires escalation. Updated daemon assertions cover SaucyBot tweet, descriptive Markdown link, URL-only human and SaucyBot, plus existing mute/suppression/duplicate paths.

Manual, no sudo, any directory: `~/scripts/codex-notification-sound smoke discord-links` says Alex sends link; `smoke discord-saucybot` says SaucyBot sends tweet; `smoke discord-link-only` says Alex sends link. Normal popups remain. Installed callback probe checks source/live equality, exact parser text and real Piper/mpv WAV counts. Subjective listening and next real incoming message remain separate acceptance.

## Evidence and review notes

Prior lookup: local-discord-direction-isolates applies to restricted D-Bus access and normalization; local-dunst-overlapping-audio-rules applies to one callback, with old SaucyBot exclusion superseded. First-turn shape probes established tweet words in a SaucyBot body without printing private message contents; no need to read history again. Living incident docs/postmortem/2026-10-22-discord-embed-history-access.md records access restriction, fixture display capacity and refresh conflict. Draining earlier private fixture popups repaired the test while preserving production notification_limit5 and suppression.

First required refresh stopped safely on unrelated scripts/audio-mute mode0755 live/0775 source. Unforced exact helper apply succeeded; no unrelated permission edits. Latest correction requires another refresh attempt and exact deployment if the same protected conflict persists. Earlier installed volume74 was preserved. Rollback: existing discord-speech disable; no changes to other notification audio settings.

Suggested commit: `fix(notifications): announce Discord tweet and link senders`.
Cursor prompt: Review plans/discord-links-embed-speech.md and its scoped diff; preserve unrelated dirty work, verify exact sender sends tweet/link wording and ordinary text behavior through the installed callback, then report unobserved real-message/listening acceptance.

Final correction evidence: focused89/broader111/type0/private Dunst1 all pass. Exact helper apply exited0 after full refresh stopped on the same unrelated audio-mute mode conflict. Installed source/live equality and exact wording passed for all three public callbacks; each produced one WAV, zero MP3, exit0 and no stderr. No subjective listening or new real incoming notification observed. Latest private daemon verifies URL-only notifications announce kind. Full refresh remains incomplete; scoped deployment is active. Targeted incident-learning check and whitespace check pass. No commit/push performed.

## Authorized session commit milestone

User invoked commit-session. Ship `fix(notifications): announce Discord tweet and link senders` as one commit with this plan, helper/tests, README/usage/smoke updates, living incident and only matching reviewed learning. Session01a1649c-7180-7a11-9d58-ef169999d6fc scope helper returned unsafe because orchestration writes were not detected; use captured pre-write status and observed successful writes as fallback. Split shared baseline-dirty operational guidance and ledger from HEAD, retaining only this session's finding/report and obsolete mute-advice removal. Exclude all other baseline/concurrent changes. Candidate-only public aliases use /home/example; preserve local ledger aliases. README gate pass_no_change. Prior final verification89/111/type0/private1 plus real installed WAV1/1/1 remain valid; fresh pre-commit focused89/type0 passed, exit0. Remaining issue: full refresh stopped on unrelated mode drift; exact helper deployed. Next: privacy-gate the exact candidate, commit once and push origin/main. Keep all unrelated work and existing index state intact. No history rewrite.
