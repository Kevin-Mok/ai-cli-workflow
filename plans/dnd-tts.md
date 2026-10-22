# Honor DND for automatic notification speech

Make automatic Codex, Discord and Grok audio honor the existing Dunst pause used by the i3blocks DND indicator. Reproduce silence with a fake player, add a bounded pause query at playback boundaries, then deploy and verify.

## Scope and decisions
- Shared player: `scripts/executable_codex-notification-sound`; regression tests, notification docs and smoke checks.
- Explicit previews bypass DND. Automatic audio suppressed during DND is discarded, not replayed. An already playing clip/phrase may finish; later playback stages recheck pause.
- Missing/unreachable Dunst preserves previous audio behavior, with a one-second query timeout.
- Preserve all initial dirty files/hunks (captured git status); commit-session now authorized. Installed player is byte-identical despite newer mtime.

## Checklist
- [x] Trace i3blocks pause and event-hook bypass; consult incident memory.
- [x] Add failing behavioral test for automatic audio under DND, normal audio, explicit preview, queued playback and between-stage pause.
- [x] Add minimum shared playback gate; update documentation.
- [x] Run focused regression/type checks; refresh config; compare installed bytes and run isolated installed checks.

## Evidence and review
Memory query `dnd tts notification sound`: overlapping Dunst callback finding applies to delivery architecture, but does not cover direct event playback. Do not add a second script rule.
Protected state includes README, smoke tests, memory ledger/reference changes and many unrelated files; edits must append or patch only relevant text.
Rollback: remove the new automatic-playback gate and its call arguments. No settings/schema change or daemon restart needed.
Manual: right-click DND, trigger a real completion/question (silent), then left-click and trigger another (audible); preview remains audible while paused.

## Final evidence
- RED: 5 isolated DND tests, 3 expected failures (paused automatic, queued, between-stage).
- GREEN: `python3 -B tests/test_notification_dnd.py` 6/6; `python3 -B tests/test_codex_notification_sound.py` 89/89; `python3 -B tests/test_codex_question_notification.py` 12/12; basedpyright helper 0 errors.
- `xvfb-run -a dbus-run-session -- python3 -B tests/scripts/codex_notification_daemon_check.py`: 1/1 passes outside socket-restricted sandbox, covering Codex/Grok/Discord display, queue, history and suppression.
- `refresh-config` attempted and stopped on unrelated local Kitty drift. Targeted `chezmoi apply ~/scripts/codex-notification-sound` succeeded. No Dunst restart needed.
- Installed helper exercised against live Dunst with silent fake player: paused automatic0, explicit preview1, resumed automatic1; original pause=false restored; installed/source bytes match.
- Manual listening/new natural incoming completion remains unobserved. Full repository suite skipped: focused audio paths and daemon regression are proportional to this change.
- Review: one shared gate, no new settings/dependencies; timeout/missing Dunst preserves audio. A currently playing phrase can finish. Commit/push authorized by follow-up commit-session.

## Handoff
Atomic plan: reproduce → shared gate → regressions → targeted deployment (complete).
Cursor prompt: “Review plans/dnd-tts.md and the shared player diff. Preserve unrelated dirty work; verify automatic DND silence, preview bypass, queued suppression and resume with the listed tests.”
Suggested commit: `fix(notifications): honor DND for automatic TTS`.
Docs updated: notification usage, README DND behavior, shared smoke checklist and living incident. Rollback removes only this gate and corresponding tests/docs, then targeted apply. Manual acceptance: pause via right-click, feed a normal completion/question, explicitly preview, resume via left-click and trigger a new completion. Already playing audio may finish.

Memory learning: reviewed report SHA-256 `a27fdfaa542914bea4809093711845565d038dfde8b0f7b6d22ec839cc0b48e4`, finding `local-dnd-direct-event-audio`, runtime scope; targeted memory check exit0 with no errors. Added tracked reference/ledger entry preserving pre-existing edits. Final diff whitespace check exit0.

## Delivery milestone — fix(notifications): honor DND for automatic TTS
Session `01a16556-d09f-7cd2-a6a6-435743a7e8e9` uses direct-write attribution: the scope helper returned unsafe/no detected writes for this tool runtime. Only observed DND edits are eligible; split README, smoke-checklist and ledger from baseline dirties. README recruiter gate passed. Fresh focused checks are recorded in the delivery response. Implementation, targeted installation and automated/runtime verification are complete; remaining acceptance is subjective listening/new natural events. Full refresh remains blocked by unrelated Kitty drift. Next step after committing is one push to origin/main; preserve unrelated dirties.

Fresh commit-session checks: DND6/sound89/question12 and typecheck0 pass. Git staging needs authorized execution because .git is read-only in the sandbox; initial attempt made no index changes.

Staging splitter now anchors the top-level ledger arrays to exclude nested finding lists; staged candidate review includes only eleven DND paths.

Privacy gate initially rejected two home paths; public candidate uses tilde/public placeholder alias, preserving the local working ledger alias. Only session-attributed paths/hunks are staged.
