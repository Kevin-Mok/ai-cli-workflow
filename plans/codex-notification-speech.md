# Speak exact Codex titles after the MP3

Implement offline title-only speech after the existing clip, using exact Codex identity and preserving desktop popup behavior. Install the optional voice, deploy the completion callback, then explicitly enable machine-local speech. Current policy speaks user-facing completed answers with nonblank final text only; permissions, spawned helpers and unknown origins remain silent after user feedback.

## Context and scope

Existing helper: scripts/executable_codex-notification-sound; existing unit suite: 13 tests. Add an event bridge, Piper setup helper, user hooks.json and notify callback. Update docs/codex-notification-sound.md, README command entries and docs/smoke-tests.md. Preserve all baseline dirty work, particularly README, smoke checklist, canonical instructions and postmortem sources. No worktree or commit requested.

## Settled decisions

- User supplied plan is the specification; inline execution with independent setup-helper delegation.
- Speech disabled by default; preserve MP3 configuration. Speech activation suppresses Dunst audio only.
- Completion uses thread-id and metadata. Runtime permission callbacks are silent; historical permission identity resolution tests remain separate from event eligibility. Never use parent session_id or visible terminal title for completion speech.
- Validate transcript under configured CODEX_HOME; permit separate rollout UUID. Exclude all spawned/internal threads and unknown or ambiguous provenance; require nonblank event-local final text. Missing/inconsistent title for a verified user-facing answer means MP3 only. See [the eligibility follow-up](fix-unnecessary-question-audio.md). Capture title before queueing.
- Piper 1.8.0, en_US-lessac-medium, isolated XDG data venv; synthesis stdin and 30-second timeout, each mpv playback 60 seconds, per-user lock over the sequence.
- Ruling: use current workspace and maintain this plan as ledger; user forbids unsolicited worktrees and requested implementation, so skill worktree prerequisite does not apply. Current mode cannot switch itself to Plan mode; execute the supplied decision-complete plan.

## Checklist

- [x] Capture git status, read source/instructions and prior sandbox incident guidance.
- [x] Write defining identity, playback, setup and configuration tests; observe RED.
- [x] Implement bridge, serialized MP3/title playback and machine-local switches.
- [x] Implement and verify isolated voice installer/check.
- [x] Deploy callbacks/hooks, update guide, README and shared smoke checks.
- [x] Run unit/private Dunst checks, type checks, offline synthesis and refresh-config after snapshot preflight.
- [x] Review final diff and record activation/manual limits.

## Risks and rollback

Transcript format may drift: unknown provenance fails silently; unavailable title for a verified user-facing answer retains MP3 fallback. No permission hook trust is required for completion speech. Enable after active sessions load the completion callback; legacy permission calls stay silent through runtime gating. Speech disable immediately restores Dunst MP3 delivery. No permanent service. Preserve user-selected clip and unrelated changes. Per-user lock serializes playback but queue ordering depends on scheduler.

## Verification

Run python3 -B tests/test_codex_notification_sound.py; python3 -B tests/test_codex_notification_speech_setup.py; xvfb-run -a dbus-run-session -- python3 -B tests/scripts/codex_notification_daemon_check.py; type-check changed Python helpers. Cover shared terminals, focused/background events, renamed and Unicode titles, spawned/internal agents, copied metadata, mismatched IDs, malformed settings, timeout/failure fallback, safe stdin and concurrent non-overlap. Manual: trust /hooks, restart/resume sessions, focused/background completions, approval including auto-review, unchanged popup actions, offline preview and disable rollback.

## Progress and review notes

Initial sandbox startup failed; approved reads work. Incident recorded with no-new-learning decision and targeted ledger check. Setup helper independently implemented and reviewed. Defining suite RED: 32 tests, 7 failures/3 argparse errors from missing bridge/config/interfaces; setup RED: six missing-helper failures. GREEN: 33 notification tests, six setup tests; concurrency uses real subprocess fake synthesis/player and verifies no overlap. Private Dunst regression passes (1 test). All changed helpers pass basedpyright --level error with 0 errors/warnings. Real Piper install succeeds, offline --check creates valid WAV, and MP3/title preview exits 0. Live exact-ID lookup returns this task title in 1.27 seconds.

Broader python3 -B -m unittest discover -s tests -p 'test_codex*.py': final 135 tests pass in 19.368s (exit 0). Focused final suite: 35 tests pass, including actual detached permission bridge under held playback lock, saved title capture before rename, empty approval stdout and Unicode stdin delivery. Voice remains disabled. Snapshot preflight: Git source equals live; Codex differs in notify plus model/effort (live gpt-6.1-sol/medium vs tracked gpt-6-astra/xhigh). User chose live defaults. Added only notify to live config before refresh; refresh-config completed three times (exit 0), deployed callback/hooks/helpers, snapshotted live Codex/Git and regenerated shortcuts. First refresh adopted pre-existing live scripts/second_brain/sessions.py conflict using normal helper behavior; later refreshes needed no adoption. Final live check shows gpt-6.1-sol/high, reflecting a concurrent live setting change; this task never writes reasoning effort and preserves live settings. Missing-source read probes (snapshot function assumed wrong path, .chezmoi.toml.tmpl absent) were resolved by rg --files; no writes from those probes. Documentation updated while waiting. Independent review completed and fixes verified: internal provenance wins over ambiguous duplicate metadata; explicit nested subagent.other is recognized while ordinary nicknames are ignored. Two initial review tests RED, then nested discriminator RED, all final GREEN. Canonical incident guidance/hash checks pass. Final private Dunst check passes with speech-enable suppression and speech-disable restoring MP3. Real installed --check succeeds; preview exits 0. chezmoi verify for Codex config/hooks and all three helpers exits 0. README gate pass_no_change; git diff --check exits 0.

Manual activation limits: /hooks trust must be reviewed in Codex, then all affected conversations restarted/resumed before speech enable. Speech remains disabled as specified. Focused/background real Codex turns, real auto-reviewed permission popup actions and subjective voice acceptance are documented in shared smoke checks but not claimed as exercised. No commit or push requested. Rollback verified with private Dunst and unit switches; user-selected clip remains configured.

## Handoff

Cursor prompt: Implement this plan with defining tests first. Resolve exact conversation IDs and saved names, preserve existing work, verify single MP3-plus-speech delivery, and document activation and rollback.
Suggested commit: feat(notifications): speak exact Codex task titles. Include this plan and matching documentation with implementation.

## Final CLI-output instruction update

- [x] Reconcile replacement AGENTS CLI rule with current notification work.
- [x] Defining status/setup tests RED (36 notification tests: 1 failure; 7 setup tests: 1 failure) then GREEN.
- [x] Implement aligned/icon status, width-aware output, --plain ASCII, --details paths/diagnostics, concise warnings and quiet install defaults. Preserve no-ANSI/NO_COLOR behavior and exact five-argument Dunst callback classification.
- [x] Update guide, README and shared smoke expectations for output flags.
- [x] Run final updated focused/broader/type/Dunst checks and refresh-config.

Prior final regression counts (35/135 and six setup tests) precede this additive CLI polish. Latest focused counts are 36 notification and seven setup tests; all helper type checks pass. Speech remains disabled awaiting manual trust/resume activation.

Final CLI evidence: broader Codex suite 137 tests in 22.028s, exit 0; basedpyright 0 errors/warnings, exit 0; private Dunst 1 test passes including suppression/rollback; README gate pass_no_change; diff check clean. Final refresh completes, and deployed plain/default status and offline check succeed; chezmoi verify exits 0. Speech disabled, MP3 selected, voice ready.

## User correction: completion-only audio

User reported repeated task-title speech during work. Active exact-title user tasks had no completion events, but frequent escalation requests; seven queued owned audio workers confirmed backlog. The original permission-audio scope is superseded by this correction.

- [x] Capture turn status; inspect live hook/switch/transcript event counts and worker backlog.
- [x] Define and observe RED: permission requests never launch speech, completions still snapshot exact queued titles.
- [x] Silence permission events in bridge, remove configured permission hook and clear owned audio queue without touching Codex.
- [x] Update guide, README, smoke checks, durable preference and incident learning.
- [x] Run focused/broader/private-Dunst/type checks, refresh-config, restore prior speech activation and verify no permission workers spawn.

Keep the clip and popup behavior. No cooldown is needed after correcting event eligibility. Existing sessions retain loaded hooks; the bridge must therefore refuse permission audio even after source hook removal. Preserve pre-existing work. Rollback: speech disable restores MP3-on-popup behavior. Manual completion acceptance remains documented; do not synthesize fake completion audio to the desktop.

Correction evidence: defining suite RED (37 tests, one expected failure), then GREEN (37 pass). Removed configured PermissionRequest handler; bridge also rejects legacy permission calls so active sessions need no hook reload for silence. Temporarily disabled speech, stopped five still-queued owned detached audio groups, preserving Codex. Restore the prior enabled state after deployment.

Completion-only final evidence: 37 focused and 138 broader tests pass; changed helper type checks and private Dunst pass; README gate/diff clean; refresh and chezmoi verification pass. Restored original enabled speech; ten real deployed permission calls exit 0 silently, zero audio workers. Queue cancellation stopped five still-queued owned detached groups. Updated incident learning and durable feedback in canonical tracked sources.
