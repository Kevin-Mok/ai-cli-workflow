# Codex voice auditions and playback latency

Audition ten local Piper voices with numbered names and upbeat shared samples, replay selected voices with custom text, and reduce the delay after the question clip in actual notification playback.

## Context and scope

Existing Piper 1.8.0 environment and Lessac medium voice live under XDG data. Actual notification speech is completion-only; permission requests remain silent. Add scripts/executable_codex-voice-auditions and focused tests; optimize scripts/executable_codex-notification-sound and its regression tests. Update notification guide, README and smoke checks. Initial audition phase requested no commit or voice selection. User subsequently selected Voice Contributor (6) using celebrate and authorized commit-session with push. No worktree or cloud service; activation switches remain unchanged.

## Decisions and assumptions

- User wants ten numbered, named local-only voices, natural and upbeat delivery, custom replay text and the existing question clip before every audible test.
- Verified upstream catalog: Amy, Bryce, HFC Female, HFC Male, Contact A, Voice Contributor (US), Alan, Alba, Cori, Jenny Dioco (UK). All single-speaker; Voice Contributor and Cori high quality, others medium.
- Start synthesis while clip plays, then play speech strictly afterward. Remaining gap measures process handoff, not physical speaker onset. Do not persist title caches.
- Download selected missing models only; offline mode prohibits downloads. Reuse installed pinned runtime; setup helper remains prerequisite. Audition does not write notification settings.
- Use a slightly brisk audition pace (length scale 0.95); subjective expressiveness needs listening. Runtime default voice/pace remains unchanged until selection.
- Current mode cannot be changed by available tools; this decision-complete ExecPlan records the non-trivial authorized work.

## Checklist

- [x] Capture initial dirty state, read source/policy/docs and verify catalog/CLI.
- [x] Define audition tests and observe expected missing-helper RED.
- [x] Implement numbered listing, sample lines, selection/custom replay, overlap, WAV export, offline/error handling and ongoing progress.
- [x] Define runtime overlap/cleanup RED and implement latency optimization (focused agent).
- [x] Update README, guide and grouped smoke checks, preserving pre-existing edits.
- [x] Run focused/broader/type checks, real synthesis and sample exports.
- [x] Run refresh-config after changes; verify installed behavior and record limitations.
- [x] Review final diff and handoff commands.

## Risks and rollback

Protect baseline changes: README.md, docs/commit-status-overviews.md, docs/smoke-tests.md, feedback.log, sources.json, dot_codex/AGENTS.md and existing untracked incidents/reference. Only additive intended documentation hunks. Model downloads require internet/storage; never add models/audio output to Git. Piper naturalness is voice-dependent and cannot be established by tests. MP3 must play once even on synthesis failure; failed clip playback must reap synthesis. Existing lock preserves sequence isolation. Roll back scoped source changes, or disable speech using the existing helper; preserve local clip/config.

## Verification

Automated: python3 -B tests/test_codex_voice_auditions.py; python3 -B tests/test_codex_notification_sound.py; python3 -B -m unittest discover -s tests -p 'test_codex*.py'; basedpyright --level error scripts/executable_codex-voice-auditions scripts/executable_codex-notification-sound. Targeted postmortem ledger check; git diff --check. Real: list, samples, dry-run custom replay; render ten WAVs and inspect nonempty frames, rate and manifest. Manual: play all ten, replay 1 and 6 with custom lines, compare gap, offline cached playback and pace adjustment. No sudo needed.

## Progress and review notes

Initial command-runner loopback startup failed; approved scoped runner works. Incident recorded and ledger check passes; host repair remains outside scope. Optional nonexistent checkout .codex discovery operand also documented. Independent catalog investigation verified upstream voice IDs and installed Piper CLI. User clarified clip-before-sample, real latency reduction, energetic natural local-only voices and numbered replay. Runtime optimization delegated with isolated source/test ownership.

## Handoff

Cursor prompt: Follow this plan; preserve completion-only gating and existing dirty work. Verify numbered ten-voice local auditions, custom replay, synthesis/clip overlap and owned-child cleanup. Update docs with evidence, run refresh-config and avoid changing selected voice until user decides.
Suggested commit: feat(notifications): audition voices and reduce speech delay

## Verification evidence so far

Audition RED: six missing-helper failures before implementation. GREEN initially six, now ten tests including clip-failure child cleanup, incomplete downloads/WAV rejection and watchdog-start failure. Review regressions intentionally RED, then GREEN; final focused ten pass (0.141s). Runtime RED proved serial synthesis and wrong deadline; GREEN 42 tests with real fake-child overlap, owned cleanup, hard deadline, exact stdin and fallback. Independent review found truncated-WAV and watchdog-start cleanup gaps; both fixed with defining regressions. Both helpers type-check with 0 errors/warnings. README gate pass_no_change. Targeted annotation-incident ledger check passes.

Real model downloads and ten rendered samples succeeded, exit 0. All ten WAVs have 22,050 Hz audio and nonzero PCM, about 4.53–6.87 seconds for the initial celebrate line; output /tmp/codex-voice-auditions stays outside Git. The final celebrate line uses natural wording "Take a look at what I built!". Real installed two-voice clip/speech playback and final broader checks are in progress.

refresh-config completed, exit 0, after preflight confirmed tracked/live Codex and Git configs matched. It snapshots live Codex/Git, applies chezmoi, regenerates shortcuts and reloads fish. Audition and runtime helpers deployed. Initial broader regression (before four added review checks): 156 tests pass in 36.971s, exit 0. Fresh final run pending below. No selected-voice/config switch changed.

## Final evidence and handoff

- Fresh final broader regression: 160 tests pass in 36.827s. Complete log inspected: /tmp/codex-voice-final-tests.log. Both helper type checks report 0 errors/warnings, exit 0. Deployed chezmoi verify and git diff --check exit 0. Number/name/ID list and custom Voice Contributor dry-run work through the installed command.
- Real installed Amy/Voice Contributor celebrate auditions exit 0, playing the original clip then sample, with observed process-handoff gaps 1.126s and 1.901s respectively. These are not hardware speaker-onset measurements and do not promise zero wait. Downloads are now cached for all ten voices. /tmp/codex-voice-playback contains the final celebrate wording and per-voice timing manifest.
- Actual installed notification preview --title 'All done! The tests passed.' --plain exits 0. Existing selected voice is still Lessac medium; existing speech/sound switches remain enabled and ready. Permission requests remain silent.
- Review confirmed complete PCM validation and guarded watchdog startup/owned-child cleanup. The original hard deadline and serialized audio lock remain. No new permanent service/cache for conversation titles. Naturalness and favorite choice remain subjective listening decisions.
- Updated README command table, notification guide and grouped smoke checklist. No commit/push requested. Suggested commit remains feat(notifications): audition voices and reduce speech delay; include this plan and matching docs/incidents with implementation.
- Automated reproducible commands are in Verification; manual plan: default all voices, --voice 1 6 --sample celebrate --offline, custom --text replay, pace 0.9 comparison and render-only export. Cursor prompt is in Handoff. Remaining work: user selects favorite number; setting the actual voice is a separate authorized follow-up once chosen. No task blocker.

## Voice Contributor selection and session shipping

User selected number 6 Voice Contributor using celebrate and invoked commit-session. Use en_US-Voice Contributor-high at celebrate audition pace0.95; actual completions retain exact title speech. Installer/check now target Voice Contributor high and matching pace. Status exposes selected model and pace. Existing runtime/image models stay machine-local and uncommitted.

- [x] Capture new-turn state/upstream main -> origin/main and run session scope helper.
- [x] Observe defining RED for default Voice Contributor, pace0.95 and selected-model status (three failures); installer RED seven tests/four failures.
- [x] Verify Voice Contributor selection GREEN, install/preview/check and refresh-config.
- [x] Run README gate; construct reviewed index with only session-owned hunks and three session-owned report entries.
- [x] Prepare the verified feat(notifications): audition voices and select Voice Contributor commit milestone and configured origin/main push; report resulting hash/push in Codex.

Scope helper returned unsafe (no successful writing actions detected in tool-wrapped log), session ID01a12157-1d89-7251-850f-b7edde62c4c0. Direct successful writes and initial gitstatus captured in this conversation establish fallback. Include sound/installer/audition sources, their three test files, clean-baseline guide/lesson, active plan and two created incidents. Mixed README/smoke changes: only notification/audition rows/sections. Mixed sources.json: only this session's two reviewed report records, preserving HEAD's other records. Exclude baseline-only policy/feedback/status/reference incidents. Keep index changes focused and worktree content intact.

### Shipping verification and milestone

Selected Voice Contributor model/pace tests GREEN, installer7 and audition10 pass. Full Codex regression163 passes in38.337s, exit0; all three helper type checks report0 errors/warnings. Initial concurrency fixture mismatch was recorded, fixed without weakening assertions, reviewed in sources.json and targeted check included. Real installed Voice Contributor --check, status, celebrate audition and actual preview all exit0. Celebrate audition remaining gap1.712s; no zero-latency claim. README gate pass_no_change; installed chezmoi verify succeeds.

User additionally requested the Voice Contributor MP3 be committed. Created scripts/Voice Contributor-celebrate.mp3 from the selected Voice Contributor high WAV (celebrate text, pace0.95); MP3 full decode and ffprobe checks pass. Track it via explicit .gitattributes Git LFS rule consistent with the existing question MP3. No voice models or general audio cache are committed. Add static MP3 replay smoke check and reference links.

Milestone subject: feat(notifications): audition voices and select Voice Contributor. Completed implementation, Voice Contributor selection, generated MP3, docs and checks. Remaining at commit time: push to configured origin/main. No blockers. Related plan and three session incidents/report entries travel in the same commit. Protected unrelated work remains dirty. Next step after push: use selected Voice Contributor notifications and numbered replay as desired.
