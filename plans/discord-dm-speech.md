# Discord DM speech

Restore local Ryan speech for sender-only Vesktop notifications by identifying their app metadata, verifying the real Dunst route, then deploying the existing helper and configuration.

## Context, scope and decisions

Live Dunst history contains appname `vesktop`, a nonblank sender-only title (no channel suffix), and nonblank body. Text was deliberately not printed or saved. Current speech and Discord switches are enabled, Ryan ready, Dunst unpaused. Source/live helper and dunstrc are byte identical despite newer live timestamps. Preserve all initial dirty files and unrelated edits to README, smoke tests, lessons and memory ledger. Initial implementation requested no commit; commit-session now authorizes a scoped commit and push. Default mode exposes no Plan-mode switch; execute this record inline.

Keep existing channel-format matching; accept nonblank sender/body for exact observed app `vesktop`. Do not infer identity from arbitrary sender names. No bot, token, message logging, new audio engine or history replay. Reuse markup sanitation, switch and speech-only lock. Other clients require their own observed metadata.

## Ordered checklist

- [x] Capture dirty baseline, inspect caller/parser/rules/tests/docs and privacy-safe live metadata.
- [x] Add unit and real-Dunst DM regressions and observe expected RED.
- [x] Extend existing parser/callback, app rule and synthetic smoke fixture minimally.
- [x] Verify GREEN, type checks and broader relevant notification regressions.
- [x] Update usage, README, smoke checks and incident learning.
- [x] Run refresh-config, activate Dunst and verify installed synthetic speech path.

## Verification

Automated: python3 -B tests/test_codex_notification_sound.py; xvfb-run -a dbus-run-session -- python3 -B tests/scripts/codex_notification_daemon_check.py; basedpyright --level error scripts/executable_codex-notification-sound; notification-focused broader tests. Unit negatives include unknown app sender-only, blank title/body, malformed channel suffix, disabled switch, markup/shell data and app lookalikes. Integration app vesktop must synthesize exactly one WAV and no clip. Installed smoke discord-dm must launch local WAV; discord-unrelated must remain silent. No real message sending. Subjective listening requires user observation.

## Risks and rollback

Vesktop non-message notifications with nonblank title/body will also speak. Appname is a desktop routing hint, not an authentication guarantee. Restarting Dunst loses notification history, so inspect history before restart. Disable via ~/scripts/codex-notification-sound discord-speech disable; prior tracked helper/rule can be reapplied if needed, preserving unrelated work.

## Evidence and review

Root cause: both Dunst coarse title filter and Python parser exclude sender-only DMs. Existing local-notification-user-facing-completion guidance concerns Codex provenance, not Vesktop detection; fresh metadata and reproduction required. Existing missing-clip lesson is inapplicable: voice is ready, setting enabled and the callback is never routed. Initial optional glob lookup scripts/*refresh* had no match; actual refresh function located in dot_config/fish/functions/refresh-config.fish; no remedial runtime action resulted.

RED: unit79, two expected no-play failures (inherited test); private Dunst1 fails expected20 vs19. Minimum shared-parser/callback/app rule implemented with synthetic discord-dm smoke mode.

Handoff: atomic change is parser/callback + Vesktop rule + DM fixture + regression coverage and docs. Suggested commit: fix(notifications): read Vesktop direct messages aloud. Cursor prompt: Read plans/discord-dm-speech.md; preserve unrelated dirty work, review Vesktop metadata recognition and execute the listed unit/private-daemon checks; report any live incoming-DM listening acceptance still pending. Commit-session now authorizes the scoped commit and push.

Final verification: unit79/79, private Dunst1/1, basedpyright0, git diff --check exit0. Broader Codex288:287 pass,1 existing path-abbreviation fixture fail (/h/k expected for /home/example). Postmortem26:25 pass,1 historical roots/source coverage failure (/home/example paths absent); targeted report coverage checked separately. No unrelated path migrations.

Deployment verified: refresh-config log /tmp/refresh-config.jtU4Z4rB.log completed; helper applied, Dunst restarted, byte equality confirmed. Enabled switches and Ryan ready. Installed synthetic DM callback ->one WAV,zero MP3,no error-log growth; unrelated fixture->zero new players. Live incoming DM listening acceptance remains pending. Implementation was deployed before the commit request. Docs, incident and memory guidance reflect this scope.

## Delivery milestone: fix(notifications): read Vesktop direct messages aloud

Completed scope: shared parser/callback, exact observed app rule, DM smoke fixture, regressions, guide/README/smoke checks, incident and reviewed learning. This session's writes were observed directly; scope helper reports unsafe because it cannot detect nested exec writes. Use the captured initial status plus direct writes as fallback. Include only this session's separable hunks in already-dirty README, smoke checks, lessons and memory. Keep historical memory changes, keyboard-repeat work, handoff prompts/reports and all other pre-existing work unstaged. Public ledger candidate uses the existing /home/example placeholder convention; local runtime aliases remain private worktree differences.

Verified focused unit79/private Dunst1/type0, installed synthetic one-WAV/no-MP3 playback and unrelated silence. Broader path-dependent failures remain as recorded above. README gate pass_no_change. No implementation blockers. Next: review exact candidate, pass privacy gate, commit this milestone and push main to origin/main once. Report actual hash and push result in Codex. No history rewrite. Subjective incoming-DM listening remains manual.
