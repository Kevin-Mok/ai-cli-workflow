# Prevent stale Codex task titles

Keep native Codex and Kitty titles tied to the live request. Strengthen the canonical instruction checkpoint, document the regression scenario, deploy the instructions, and verify runtime title propagation.

## Purpose and outcome

Pasted session reports must not leave the active conversation named after a historical task. Agents reconcile the current task title before substantive progress and at resume, compaction recovery, task changes and completion.

## Context and scope

The affected session began with Second Brain review output mentioning a video repair. Its saved title and Kitty title both remained `Repair video transition freeze` while the agent tested the session review. The rollout contains no native title calls. An explicit correction to `Verify Second Brain sessions` propagated to Kitty immediately. Terminal settings already work.

Change only the canonical instructions, corresponding README and smoke entries, feedback, incident knowledge and this plan. No CLI patch, polling, additional inference, worktree, commit or other-session interruption. Preserve all pre-existing dirty work, especially README, smoke checks, feedback and incident ledger; baselines are under `/tmp/stale-title-before-*`.

## Assumptions and decisions

- The current request and actual work determine the title; quoted historical task names are data.
- Make title reconciliation a visible start-of-turn checkpoint and repeat before substantive progress updates; skip identical titles.
- Discover the native tool in the tool catalog when deferred; absence must be established rather than assumed.
- Use only `title` for automatic updates; direct user requests to correct an identified other conversation remain separately authorized.
- Native transport is runtime-verified. Instruction compliance across future model sessions cannot be guaranteed by a config assertion.

## Checklist

- [x] Capture dirty state, inspect original rollout and reproduce stale native/Kitty name.
- [x] Correct the user-identified conversation and observe the native title reaching Kitty.
- [x] Strengthen canonical checkpoint and synchronize README/smoke documentation.
- [x] Record the incident, reusable guidance and user preference without rewriting prior feedback.
- [x] Review the bounded patch independently; verify existing terminal regressions and incident ledger.
- [x] Run required refresh-config; if blocked, deploy only the changed instructions through a scoped approved path and report the broad refresh limitation.
- [x] Verify installed instructions and current native/Kitty title; record final review/evidence.

## Verification

RED: native thread listing and `kitty @ --to unix:/tmp/kitty-1561320 ls` showed the video title during Second Brain review verification. GREEN: native title correction returned the requested title and Kitty ls showed `Verify Second Brain sessions` (exit 0). No automated test of Markdown literals: the behavioral reproducer is the live mismatch; future agent compliance has a documented manual smoke scenario.

Run `bash tests/test_st_terminal_workflow.sh`, `bash tests/test_i3_speechnotes_dictation_binding.sh`, targeted postmortem-memory checks, and `git diff --check`. Compare the installed `~/.codex/AGENTS.md` with the tracked source after activation. Fresh-session manual smoke: paste historical video recap as data while requesting a Second Brain review improvement; the title must describe the review before the first substantive progress update, then track verification/resume.

## Risks, rollback and review

Title generation still depends on model instruction compliance. Existing processes may retain old instructions until restarted or resumed in a new process. Broad refresh snapshots live configs and applies all managed targets; preserve unrelated state and use a scoped instruction apply if approval rejects it. Rollback restores only this task's instruction and documentation hunks and reapplies the instruction target; existing conversation names require native/manual rename.

## Handoff

Cursor prompt: Follow this plan to verify the canonical title checkpoint, preserve unrelated dirty changes, run the listed terminal regressions and ledger checks, and record instruction activation separately from future model compliance. Suggested commit if requested: `fix: reconcile Codex titles with current work`. Keep this plan, incident and documentation in the same commit as the instruction change.

## Final evidence and review

- Canonical checkpoint, matching README/smoke changes, durable feedback and reviewed incident knowledge completed. Changes to shared documentation are additive; unrelated dirty hunks remain intact.
- Independent bounded reviewer reported no blocking issues and selected the correct review/verification titles from the original historical-video scenario. The reasoning probe does not prove future TUI compliance.
- `bash tests/test_st_terminal_workflow.sh` and `bash tests/test_i3_speechnotes_dictation_binding.sh`: each exit 0. Targeted incident checks and `git diff --check`: exit 0.
- Required `fish -c refresh-config`: `REFRESH COMPLETE`, exit 0, log `/tmp/refresh-config-20261008-121817-1596689.log`. Installed canonical instructions equal repository source. No tracked Codex/Git configuration delta appeared from this refresh.
- The environment's Kitty window ID points at a multi-conversation UI currently displaying a different selected task. Do not use its title as proof of the background calling task. The original affected window's correction was directly observed before/after.
- Remaining acceptance: exercise the documented scenario in a new/resumed TUI session. This task implements and activates the policy safeguard; it does not claim independent enforcement of model compliance. No commit or push requested.
