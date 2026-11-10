# Manual README sync

Make README recruiter sync an explicit user action by removing automatic delivery triggers and the checkpoint call. Preserve unrelated dirty files and existing privacy checks.

## Scope and decisions
Keep the skill and CLI; disable implicit invocation. Update commit skills, canonical policy, catalog, README and smoke checks. No commits or pushes requested. Existing README, smoke tests and feedback edits are protected.

## Checklist
- [x] Capture initial status and map triggers.
- [x] Observe RED for manual-only skill assertion.
- [x] Remove automatic triggers and checkpoint call; document manual use.
- [x] Run focused checks and refresh-config; record results.

## Verification evidence
RED: test_skill_cull_contract.py fails the new explicitly-triggered assertion. Checkpoint journal tests cannot reach execution: existing fixture lacks 00 Context/Decisions.md. Broader cull suite also has an unrelated commit-plan-push assertion failure.

## Risks and rollback
Instruction-based behavior requires a fresh session after refresh. Restore only this session’s hunks to roll back. Do not revert pre-existing dirty work.

## Review notes
Keep manual README quality checking available; no privacy gates removed.

GREEN: manual-only test passes; checkpoint 24, security 6, commit failure 1 pass. Journal missing fixture and hook-isolation privacy refusal remain. refresh-config attempted sandboxed and elevated; duplicate MIME source ownership blocks activation. See docs/postmortem/2026-11-10-manual-readme-sync-validation.md. Admission costs/calibration refreshed. No commit/push performed.

Final checks: manual-only 1/1 and admissions 7/7 pass; git diff --check passes; targeted postmortem memory check has no errors. Catalog check reports two existing missing installed no-mistakes calibration entries (agents and claude). Left outside this request.

## Delivery milestone — chore(skills): make README sync manual-only
User invoked commit-session. Scope helper could not detect nested tool writes; direct observed edits and the original status baseline establish scope. Mixed README, smoke checks, feedback and incident ledger are staged from HEAD with only session hunks. Fresh checks: manual-only 1/1, admissions 7/7, checkpoint 24/24, security 6/6, commit-failure 1/1 passed. Existing broader fixture/catalog warnings and MIME activation blocker remain. Commit and origin/main push pending. Git index writes require sandbox escalation; working files preserved.
