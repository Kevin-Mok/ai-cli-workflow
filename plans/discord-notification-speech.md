# Discord notification speech

Recognize complete channel notification titles and speak sender says message with local Ryan, through the existing shared playback lock. Implement the approved saved prompt once, verify in isolation, then deploy and enable.

## Context and scope

Sources: scripts/executable_codex-notification-sound, dot_config/dunst/dunstrc; unit and private Dunst suites; existing notification guide, README and smoke checks. No commit/push requested. Preserve baseline dirty README, smoke tests, lessons, postmortem ledger/guidance and unrelated tasks. Saved prompt: prompts/discord-notification-speech.md. Current Default mode does not expose a Plan-mode switch; execute this approved decision-complete plan inline.

## Decisions and assumptions

Match whole normalized title SENDER (#CHANNEL, SERVER), retaining sender parentheses and Unicode. Strip only actual supported notification markup before entity decoding so escaped literal markup stays visible. Nonblank components required. Unknown apps may match; sender-only DMs excluded. Existing Codex/Grok dispatch has precedence. Independent discord-speech.json switch defaults off; explicitly enable after verification. Dunst coarse glob precedes existing rules, uses existing callback, retains always_run_script=false. No cloud, bot, account access or extra sound clip.

## Checklist

- [x] Capture dirty baseline and read source, instructions, related lessons.
- [x] Define matcher, control and callback tests; observe RED.
- [x] Implement minimum parser/control and Dunst rule.
- [x] Extend private Dunst coverage and run unit/broader/type checks.
- [x] Update guide, README and Action/Expected smoke checks.
- [x] Reconcile live managed files, refresh, install helper, activate and enable.
- [x] Exercise installed synthetic fixtures; record actual evidence and remaining limits.

## Risks and rollback

Same-format unrelated apps are accepted. Dunst duplicate stacks can produce one first-display sound upon recall, as already documented. Speech cannot cover notifications Discord suppresses upstream. Rollback: codex-notification-sound discord-speech disable; preserves global speech and clip. Never log message text. Real incoming Discord and subjective listening require observed acceptance, otherwise pending.

## Verification

Unit RED/GREEN: python3 -B tests/test_codex_notification_sound.py. Broader: python3 -B -m unittest discover -s tests -p 'test_codex*.py'. Type: basedpyright --level error scripts/executable_codex-notification-sound. Private runtime: xvfb-run -a dbus-run-session -- python3 -B tests/scripts/codex_notification_daemon_check.py. Installed synthetic smoke modes will send public fixture notifications with real local playback, plus Voice negative fixture; verify setting/rule bytes, voice synthesis and player outcomes separately from subjective listening.

## Progress and review notes

Initial mapping includes a diagnostic rg probe for optional absent paths (exit 2); discovered actual refresh function via mapper. No runtime failure or source modification from probe. Relevant prior knowledge: local-discover-paths-before-reads; use inventoried paths. Existing shared lock, timeout, subprocess argv and temporary-file cleanup will be reused.

## Handoff

Suggested commit: feat(notifications): speak format-matched Discord messages.
Cursor prompt: Review plans/discord-notification-speech.md and the matching diff; preserve existing dirty work, verify format parsing, independent activation and shared Ryan playback, then complete any explicitly pending real Discord/listening acceptance.

RED observed: 75 unit tests, 26 expected missing-parser/CLI errors, exit 1 (test inheritance repeats cases). Private D-Bus initially blocked before tests by socket permission; elevated isolated rerun requested.

Private Dunst expected RED reached after approved socket escalation: 1 test, expected 11 calls observed 10 (exit 1), proving new route is absent. Pre-deploy live helper and dunstrc byte-identical to source; global speech enabled, sire.mp3 selected, Ryan ready.

Independent review found three gaps: quoted > markup attributes, malformed final suffix backtracking, and CLI-command app names. Added defining cases; waiting RED before correcting. Focused initial GREEN 75/75; basedpyright 0 errors/warnings/notes; private Dunst 1/1. Broader restricted suite encountered socket and baseline path-fixture issues (living report docs/postmortem/2026-10-21-discord-broader-check.md).

Refresh preflight: source/live helper and Dunst already equal after concurrent managed refresh. chezmoi status shows an unrelated MM media-screensaver target. Render/live bytes exactly match; diff is solely mode0755 to0775. Reviewed existing plans/refresh-config-screensaver-conflict.md and local-screensaver-launcher-mode-drift; guarded exact-target apply may reconcile mode without content changes before unforced refresh. Preserve all other unrelated source content. No force apply or adoption.

Final review regressions: new cases first failed (4 parser failures/2 app-name errors), then passed after HTMLParser, final-suffix rpartition and callback urgency classification. A second reviewer caught preview titles LOW/NORMAL/CRITICAL misclassified by urgency; defining test RED (77 tests, two failures), then guard excludes CLI option forms. Reviewer confirmed all findings resolved. Final focused77/private Dunst1/type0 all GREEN. Notification subset97 and question12 passed before final guard refinement; final focused includes the changed dispatch and private daemon covers every route. Elevated broad284 has one pre-existing unchanged search fixture failure (/h/k expected vs actual /h/e for /home/example). No unrelated search fix.

Deployment: guarded mode-only reconciliation preserved media-screensaver SHA-256; unforced refresh completed twice. Latest /tmp/refresh-config.PgxO93I6.log, exit0. Installed helper/dunstrc chezmoi verify exit0. Ryan offline check exit0 (Piper1.8.0). Activation restart succeeded; Discord enabled; global speech enabled and sire.mp3 selected unchanged; Dunst pause=false. Both installed matching fixtures displayed and each launched one real WAV player, zero MP3. Negative fixture first overlapped concurrent MP3; living incident records inconclusive observer and attributed repeat. No worker was stopped. Final acceptance pending the repeat result, real Discord and subjective listening.

Final installed negative repeat: /tmp/discord-negative-probe.py exited0, fixture_players0, other_observed_players[], no new audio diagnostics. Synthetic public fixtures now all verified through actual installed desktop path: two popups/one WAV each and Voice popup/no audio. Subjective listening and a real incoming Discord notification are explicitly pending, not completion claims. No messages sent to anyone. No commit/push performed. Final handoff carries three direct CLI checks; rollback discord-speech disable leaves Codex state unchanged. All scoped implementation/docs/checklist work complete; accepted limitation remains same-format unrelated apps and sender-only DM exclusion.

## Session delivery milestone

Authorized commit-session: feat(notifications): speak format-matched Discord messages. Implementation, plan, guide, five task incident reports and their reviewed ledger additions ship together. Scope helper returned unsafe (no writes detected through this tool interface); successful edits recorded in this conversation establish direct-write attribution. README includes only the Discord row, smoke checks only the Discord section, ledger only five current-task report records. Baseline dirty files and the pre-existing saved prompt remain excluded. Public candidate replaces machine-specific ledger aliases with /home/example; working ledger retains locally valid aliases and unrelated pre-existing work.

Fresh pre-commit checks: notification unit77, private Dunst1, basedpyright0 errors/warnings/notes; README gate pass_no_change. Previous broader check284 retains one unchanged placeholder-path assertion failure. Implementation and synthetic installed checks complete; real Discord and subjective listening pending. Rollback remains discord-speech disable. After candidate review and privacy gate, commit once and push origin/main. No history rewrite. Remaining blockers: none for eligible safe scope; public privacy gate must pass before commit. Next step: create the verified commit and push, then report hash and actual push status.
