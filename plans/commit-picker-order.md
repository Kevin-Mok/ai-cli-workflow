# Commit picker order

Make `$comm` show Session, Plan & Push, Dirty, then Plan by numbering their display names. Keep skill slugs and workflows unchanged, apply only these four metadata targets, and verify source/live parity.

## Scope and decisions

Change four `agents/openai.yaml` display names, the existing metadata contract, README, and smoke check. Upstream `skill_popup.rs` sorts equal fuzzy matches by display name; use `Commit 1 Session`, `Commit 2 Plan & Push`, `Commit 3 Dirty`, `Commit 4 Plan`. No unsupported priority fields. The current mode has no Plan Mode switch; this document records the small mechanical change.

## Checklist

- [x] Capture initial dirty state; preserve all pre-existing changes.
- [x] Inspect metadata, local installation, upstream picker comparator, and live/source parity.
- [x] Update display names and documentation.
- [x] Run focused contracts; deploy metadata and verify parity.

## Risks and rollback

Numbers are visible in the picker; full-name searches remain host-ranked. Revert only these four titles to roll back. Existing unrelated dirty files and pending chezmoi targets are excluded. Live metadata matches tracked source before editing. A new Codex session may be needed to reload cached metadata.

## Verification and evidence

Run `python3 tests/test_commit_plan_push_skill.py -v` and `python3 tests/test_ai_workflow_contract.py -v`. Run refresh-config with a temporary process-local chezmoi wrapper restricting apply to the four metadata targets, preserving unrelated pending managed files. Compare all four live/source metadata files. Manual: open a fresh Codex picker and type `$comm`, `$commit`, and `$commit-session`; verify the four numbered entries and original skill insertion.

## Review notes

Display metadata only; no commit workflow or canonical slug changes. README needs a short presentation note. Initial implementation had no commit request; the follow-up `$commit-session` authorizes shipping this session. Upstream evidence: https://github.com/openai/codex/blob/main/codex-rs/tui/src/bottom_pane/skill_popup.rs (filtered comparator).

RED: the focused metadata contract ran four tests: two passed, two failed for the old metadata and smoke-check titles, as expected before editing.

GREEN: focused metadata suite 4/4 passed; broader workflow suite 9/12 passed, with three unrelated baseline instruction-policy assertions recorded in docs/postmortem/2026-10-22-commit-picker-validation.md. Scoped diff whitespace check passed. Scoped refresh-config exited 0 (REFRESH COMPLETE); all four installed YAML files byte-match source and print the requested numbered labels. Manual picker interaction remains unchecked; reopen Codex for cached metadata. No workflow behavior changed.

## Delivery milestone: fix(skills): order commit picker labels

Complete: four metadata labels deployed, matching README/smoke checks and focused contract updated. README gate: pass_no_change. Session helper could not detect wrapped writes; direct observed-write fallback scopes the seven previously clean changed files, this plan, the validation report, and only the new report record in the mixed sources.json ledger. All unrelated dirty files and prior ledger edits remain excluded. Commit this milestone with its implementation, then push once to origin/main. Remaining: live picker acceptance and separate baseline-policy repairs; no blocker to scoped delivery.

Delivery privacy review rejected the new local home alias; sanitized it to the existing public `/home/example` convention. Local targeted ledger check had passed before sanitization; public alias resolution is a known local-check limitation. Recheck the final staged candidate with the privacy gate.

Final delivery checks: README gate passed; focused tests 4/4 passed; installed metadata parity confirmed. Privacy gate passed after alias sanitization. Targeted memory recheck reports only the expected unregistered real local alias; public report/hash registration is retained. Broad policy failures and local alias resolution remain warnings, not picker regressions.
