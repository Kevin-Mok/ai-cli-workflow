# Fish-alias immediate delivery

Make successful refresh flow directly through focused activation checks, commit and push. Prepare required documentation and README review before refresh so they cannot delay delivery afterward.

## Context and scope

Edit the existing fish-alias delivery section, its admission costs and the existing smoke expectation. Preserve mapping behavior, no-op/local-only handling, privacy hooks and unrelated dirty work (README, smoke tests, feedback, postmortem ledger/references, fish progress, Vesktop, approvals and Firstmate work).

## Decisions and checklist

- [x] Inspect current skill and capture dirty state.
- [x] RED: independent instruction review found no requirement to prepare README/docs before rf, or keep commit/push together before final handoff.
- [x] Admission PASS: retain value 3/uniqueness 2; compare readme-recruiter-sync and smoke-test-capture; update measured costs before editing. Trigger description unchanged; no new skill or private source.
- [x] Replace delivery paragraph and update existing smoke expectation.
- [x] GREEN: independent pressure review; admission tests, catalog check and README gate.
- [x] Prepare all delivery records, refresh and verify installed skill.
- [ ] Commit and push this verified milestone.

## Verification and review

Pressure cases: changed mapping with pending docs; repeated no-op; explicit local-only; failed activation; missing upstream/rejected push. Required sequence: preparation -> rf -> focused activation checks -> scoped staging/review -> commit -> push -> final handoff. Git/privacy hooks remain mandatory; post-commit status can be concise commentary while push proceeds.

Run python3 -m unittest discover -s tests -p test_skill_admissions.py and scripts/sync-vetted-skills --check. Run scripts/executable_readme-recruiter-sync. After refresh, read installed delivery text and compare it to tracked content. No shortcut command execution or unrelated helper refactor.

Rollback: restore only the edited delivery text, admission row and smoke expectation, then refresh. Documentation-only guidance cannot guarantee future agent compliance; no runtime helper change is intended.

Observed pre-refresh checks: admission suite 7 passed (exit 0); catalog 241 entries, 0 missing/stale (exit 0); README pass_no_change; independent pressure review passed all five cases. Description remains 132 B (33 estimated tokens), body 6455 -> 6679 B (1613.75 -> 1669.75 estimated tokens), weighted cost 199.975, score 4.0005; no recurring description growth.

Delivery milestone: docs(fish-alias): commit and push immediately after refresh. Refresh and installed-section comparison gate the commit; push targets origin/main immediately after commit, preserving unrelated work. No optional work follows refresh.

Refresh exited 0 and installed delivery section matches canonical source. Focused commit and origin/main push follow immediately; results reported in the final handoff.
