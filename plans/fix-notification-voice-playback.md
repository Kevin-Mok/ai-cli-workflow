# Restore notification voice playback

Restore the existing clip and spoken notification sequence by correcting its machine-local clip path, then verify playback and document recovery.

## Outcome and scope

Notifications display but neither the configured clip nor speech plays. The installed helper reports a missing checkout MP3. Repair only the local selection and related recovery documentation; preserve existing audio behavior, voice, hooks, and unrelated dirty work. No implementation change is needed. The subsequent `commit-session` request authorizes committing and pushing only this session’s documentation/learning changes.

## Context and decisions

- Initial `git status --short` captured before writes: many unrelated modifications, including notification scripts/tests/docs, README, lessons and postmortem memory. Preserve these edits.
- `~/scripts/codex-notification-sound status --details` exits 1: configured checkout `scripts/can-i-ask-you-a-question.mp3` does not exist.
- The installed `~/scripts/can-i-ask-you-a-question.mp3` exists (27,046 bytes); speech is enabled and Ryan model/runtime files exist.
- `configured_clip()` validates the clip before either MP3 or speech starts; a stale setting explains both silent stages. Reuse existing `set`; no fallback or new code is needed.
- Unsandboxed `wpctl get-volume @DEFAULT_AUDIO_SINK@` reports 0.60 without MUTED. Desktop sockets require unsandboxed access; initial sandbox diagnostics were denied.
- Assumption: retain the currently selected question clip and Ryan voice. Completion speech continues to announce the task title; question hooks announce the actual question.

## Checklist

- [x] Capture dirty state, map callers, read docs and relevant incident knowledge.
- [x] Reproduce missing clip via installed status (RED, exit 1).
- [x] Select existing installed clip with the existing CLI.
- [x] Verify status, speech synthesis and clip-then-speech playback against desktop audio.
- [x] Run installed silent completion/question probes, including excluded worker cases.
- [x] Correct stale clip documentation and shared smoke check; record incident and reviewed memory.
- [x] Record final evidence, risks and handoff.

## Verification

- RED: `python3 ~/scripts/codex-notification-sound status --details` → missing configured clip, exit 1.
- GREEN: installed `status --details` → existing clip, speech enabled, Ryan ready.
- Runtime: installed `preview --title 'Notification audio is restored' --details` → clip then synthesized sentence, exit 0. The user confirmed hearing both stages.
- Synthesis: installed `setup-codex-notification-speech --check` → pinned runtime and successful offline WAV generation.
- Event routing: `python3 -B scripts/smoke_codex_notification_events.py --installed --plain` → all cases pass; `python3 -B scripts/smoke_codex_question_events.py --installed --plain` → valid questions two playback calls and worker/empty/secret cases zero.
- Memory: targeted `postmortem_memory.py check --postmortem` → current report hash registered and references valid.

## Risks and rollback

Local settings require writing outside the workspace through the normal approval mechanism. The previous JSON selected the absent checkout clip, as recorded in the incident. Selecting that missing path is not a useful rollback; use `speech disable` for popup MP3 behavior or `disable` for silence. No service restart or hook trust change is needed. The user confirmed subjective speaker audibility for the real preview; genuine later notification acceptance remains separate from silent fixture probes.

## Progress and review

Completed local path repair using the existing CLI; no implementation change, dependency, hook rewrite, service restart, commit or push during the initial repair. Related prior knowledge covers muted sinks and event eligibility; neither remedy applied because the output was unmuted and the configured file was absent. All initial dirty files remain protected.

### Final evidence

- `python3 ~/scripts/codex-notification-sound set ~/scripts/can-i-ask-you-a-question.mp3`: exit 0; selected existing installed clip.
- Installed `status --details`: exit 0, sound/speech enabled, Ryan ready, installed clip selected. Old timestamped errors retained.
- Installed `setup-codex-notification-speech --check`: exit 0, Piper 1.8.0 ready.
- Installed `preview --title 'Notification audio is restored' --details`: exit 0; user answered **Yes, both played**.
- Test agent ran installed notification probe (14/14) and question probe (6/6), both exit 0; parent repeated accepted-question direct probe, two playback calls with exact expected text, exit 0.
- Installed resolver recognizes the calling live thread as eligible with title `Fix notification voice playback`; no synthetic player action was launched by this lookup.
- Updated README missing-clip recovery sentence, notification guide, shared smoke checklist, local lesson and living incident; retained unrelated content. README gate returned `pass_no_change`, exit 0.
- Memory scan exit 0; reviewed incident SHA-256 `046b3b7c29548b6f4fae359a3e35a4b9667b4e4ecb73d43930cf3ec4644aaa42`, finding `local-notification-missing-clip` with runtime scope. Targeted check exit 0 with no errors/new/changed/missing sources.
- No tracked runtime configuration changed, so no refresh-config deployment is needed. Existing status/preview reproducer provides RED/GREEN without a source-code test change.

### Review and remaining scope

The simplest fix was selecting the retained asset outside the checkout. The incident does not establish which earlier operation removed the checkout asset. A subsequent natural notification remains a final event-delivery acceptance check; real audio preview and installed handler routing are separately verified. Full application suite omitted because executable source did not change. The shipping review ran 26 postmortem-memory tests: 25 passed, one historical coverage test failed because sanitized default `/home/example` roots are absent. This is a warning; the notification repair remains verified. Suggested documentation commit, if requested later: `docs: document missing notification clip recovery`; keep this plan and matching incident/memory/docs together.


## Session commit milestone

- [x] Reconfirm branch `main`, upstream `origin/main`, initial staged set empty.
- [x] Run scope helper: `unsafe` because wrapped tool writes were not detected; use directly observed edits from this conversation, with the captured initial dirty status as the boundary.
- [x] Stage only the eight session-attributable files/hunks using a private alternate index; preserve pre-existing changes in the working tree and original index.
- [x] Run README gate, current-report memory validation, exact-candidate privacy check and staged-diff review. All passed; current-report checking used a temporary private mapping from its neutral public alias to the candidate artifact.
- [x] Prepare the verified milestone `docs: document missing notification clip recovery` for commit on `main` and one push to `origin/main`. Record the resulting SHA and remote receipt in the commit-session handoff.

Eligible scope: README missing-clip sentence; notification guide clip/recovery paragraphs; notification smoke checklist; this plan; missing-clip incident; corresponding lesson; the new memory reference section and its single finding/report ledger entries. Other voice, refresh, privacy-gate, migration and tool changes remain excluded. The local sound selection and MP3 are machine-local and will not be committed.

Milestone overview: the local audio repair and its eight-file recovery/learning record are complete. Runtime preview was user-confirmed audible; 20 routing cases passed. Candidate README gate, scoped memory validation, privacy gate and whitespace review passed. One historical full-ledger coverage test remains an out-of-scope warning (25/26 tests passed). No remaining implementation work or safety blocker. Next workflow action is commit followed by the single upstream push, preserving all unrelated work. Public ledger paths are neutral; exact machine aliases remain outside the committed candidate.
