# Fix unnecessary question audio

Only announce a completed user-facing Codex answer that contains nonblank final text. Reproduce the false triggers first, change event eligibility, update documentation, then deploy and verify the installed bridge without audible test playback.

## Context and scope

Sources: scripts/executable_codex-notification-event and tests/test_codex_notification_sound.py. Live speech/sound enabled; installed sources match. Ordinary spawned helpers and unknown identities currently trigger MP3 playback. Live worker spawn metadata includes inherited completion events while root work continues. Include guide, shared smoke checklist, README, reusable event probe, incident learning and lessons as needed. No worktree, commit or push requested. Current mode cannot be switched by a tool; maintain this decision-complete ExecPlan in Default mode.

## Assumptions and decisions

Current user report overrides earlier ordinary spawned-agent audio eligibility: those results are collected by the parent and require no user attention. Automatic audio requires known user-facing provenance and event-local nonblank last-assistant-message. Never infer readiness from historical/copied transcript finals or a title. Known user-facing completions may keep clip-only fallback when a saved title is unavailable; unknown/ambiguous provenance stays silent. Manual previews, selected clip, voice and desktop popup behavior remain available.

## Checklist

- [x] Capture initial status, instructions, relevant preference/lessons and live metadata; independently review trigger classification.
- [x] Write and observe defining RED tests for worker, missing/blank response, unknown and ambiguous provenance.
- [x] Implement minimal eligibility guard and reusable CLI event probe; update guide, README and grouped smoke entries.
- [x] Run focused/broader Codex regression, type checker, isolated Dunst and artifact probes; preflight and run refresh-config.
- [x] Verify deployed handlers and silent-event probes, update incident/hash/guidance, review final diff and handoff.

## Protected work, risks and rollback

Initial dirty tracked files: README.md, docs/commit-status-overviews.md, docs/smoke-tests.md, dot_agents/skills/feedback-memory/feedback.log, dot_agents/skills/postmortem-memory/sources.json, dot_codex/AGENTS.md. Initial untracked reports: 2026-10-08-smoke-output-policy-sandbox-startup, 2026-10-09-direct-verification-policy-sandbox-startup, 2026-10-09-vps-backup-command-lookup; untracked session-insights.md. Other conversations are actively writing; reread before edits and preserve their hunks. Newer dirty work is protected too. Do not stage anything. Event schema/provenance may drift; prefer silence when eligibility cannot be verified. Existing detached workers can outlive deployment; inspect and clean only revalidated same-user event-play process groups if present. refresh-config snapshots live Codex/Git before applying and can adopt local conflicts; review source/live snapshot diffs first. Rollback restores prior handler and refreshes; no local audio settings are changed.

## Exact verification

RED/GREEN: python3 -B tests/test_codex_notification_sound.py EventBridgeTests (and focused new cases). Regression: python3 -B -m unittest discover -s tests -p 'test_codex*.py'; basedpyright --level error on changed Python handlers; xvfb-run -a dbus-run-session -- python3 -B tests/scripts/codex_notification_daemon_check.py. Direct CLI probes: user-facing completion launches one sequence; helper, empty/missing answer, unknown provenance and legacy permission produce no playback. Installed status preserves enabled sound/speech and Voice Contributor voice. Run fish -c refresh-config, then chezmoi verify on affected targets and installed CLI probes. No sudo required. Actual future completion audibility/desktop focus remains a manual smoke check.

## Progress and evidence

Live evidence and applicable reviewed guidance are in docs/postmortem/2026-10-09-empty-attention-notification-audio.md. Initial sandbox launch failed; scoped approved reads succeed. Root-cause scope: verified eligibility defects; exact historical offending audio event is unlogged. RED/GREEN, regression, deployment and final review pending.

## Review notes and handoff

Keep changes limited to automatic audio eligibility. No need to alter desktop notification matching, voice synthesis, media assets or production Codex. Suggested Conventional Commit: fix(notifications): silence completions without user-facing answers. Cursor prompt: Follow this plan, preserve dirty work, prove silent false events and retained exact-title root audio before deploying. Automated and manual checks are listed above; record actual evidence before completion.

Focused GREEN: 16 event/probe tests pass (7.839s). RED: initial 15 event tests had 16 failed assertions; complete key-worker/unknown/ambiguity RED rerun had 3 failures; missing probe RED had 1 failure. Type check: zero errors/warnings. Private Dunst: 1 test passes in 3.375s. Broader191: five unrelated in-progress picker/priority failures; no notification failures. README gate pass_no_change. Exact owned event-play queue inventory empty; no process termination. refresh preflight reviewed live xhigh/default vs tracked low/fast; preserve live snapshot.

Final evidence: notification/speech67 PASS (15.300s); installed all-eight probe PASS, completion1 and seven false triggers0; real installed user resolver eligible/exact title and helper silent; chezmoi verify PASS; live sound/speech enabled, ready Voice Contributor high and clip unchanged; refresh-config exit0, log /tmp/refresh-config-20261009-144606-879580.log. Independent review found no issues and reran focused16 PASS. Broader rerun193 in45.189s: one unrelated test_async_recap_preserves_query_and_uuid_and_ctrl_g_requests_selected failure, installed fzf rejects transform action; no audio failures. Prior five-failure result superseded. No further edits to concurrent picker work. Learning finding local-notification-user-facing-completion linked to final report hash 6c3e5daec804556c6d1ec941073c8e718c7a719aeb5280790ece76f65dc9a6a0. Final targeted ledger check and post-learning refresh pending.

Atomic result: eligibility guard plus RED/GREEN cases, silent CLI probe, synchronized public documentation and incident learning. Paste-ready Cursor prompt: "Review plans/fix-unnecessary-question-audio.md and the scoped notification changes. Preserve all concurrent work. Verify cli/vscode nonblank answers announce once; spawned, empty/missing, unknown/ambiguous, parent-linked and permission events stay silent. Run the exact focused/type/Dunst and installed-probe checks listed above. Do not fix unrelated picker failures or commit/push unless requested." Suggested commit: fix(notifications): silence completions without user-facing answers. Manual acceptance: allow a normal focused/background user answer to finish and hear one clip plus its saved title; spawn helpers while root works and hear no helper ping. These subjective live actions remain unperformed.

Targeted ledger check completed: exit0, one reviewed report, no changed/new/unregistered aliases or errors; reviewed hash 6c3e5daec804556c6d1ec941073c8e718c7a719aeb5280790ece76f65dc9a6a0. Final post-learning refresh and installed probe outcomes are reported in the handoff. Changes remain uncommitted; no delivery blocker for the audio fix, with one named unrelated broad-suite failure and subjective hardware acceptance remaining.

Final completion evidence: post-learning fish -c refresh-config exit0 and REFRESH COMPLETE (/tmp/refresh-config-20261009-144846-885845.log); fresh installed eight-case probe exit0 with completion1 and all seven false triggers0; final chezmoi verify, README gate pass_no_change and git diff --check all exit0. No remaining audio implementation/deployment work.
