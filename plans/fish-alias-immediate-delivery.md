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
- [x] Commit and push this verified milestone: 8b8ecd1 pushed to origin/main.

## Verification and review

Pressure cases: changed mapping with pending docs; repeated no-op; explicit local-only; failed activation; missing upstream/rejected push. Required sequence: preparation -> rf -> focused activation checks -> scoped staging/review -> commit -> push -> final handoff. Git/privacy hooks remain mandatory; post-commit status can be concise commentary while push proceeds.

Run python3 -m unittest discover -s tests -p test_skill_admissions.py and scripts/sync-vetted-skills --check. Run scripts/executable_readme-recruiter-sync. After refresh, read installed delivery text and compare it to tracked content. No shortcut command execution or unrelated helper refactor.

Rollback: restore only the edited delivery text, admission row and smoke expectation, then refresh. Documentation-only guidance cannot guarantee future agent compliance; no runtime helper change is intended.

Observed pre-refresh checks: admission suite 7 passed (exit 0); catalog 241 entries, 0 missing/stale (exit 0); README pass_no_change; independent pressure review passed all five cases. Description remains 132 B (33 estimated tokens), body 6455 -> 6679 B (1613.75 -> 1669.75 estimated tokens), weighted cost 199.975, score 4.0005; no recurring description growth.

Delivery milestone: docs(fish-alias): commit and push immediately after refresh. Refresh and installed-section comparison gate the commit; push targets origin/main immediately after commit, preserving unrelated work. No optional work follows refresh.

Refresh exited 0 and installed delivery section matches canonical source. Focused commit and origin/main push follow immediately; results reported in the final handoff.

## Follow-up: require local expansion before delivery

- [x] RED review: previous wording required registration/syntax but did not require interactive expansion on this PC.
- [x] Admission PASS: same shortcut scope and precedents; updated body costs before edit; description unchanged.
- [x] Require fresh interactive local fish, installed abbreviations, Space expansion capture and cancellation without execution; retain fish -n and immediate delivery. Existing PTY regression supplies the pattern.
- [x] Admission/catalog checks, local fm expansion, refresh, installed skill comparison and repeated local expansion all passed.
- [x] Commit and push follow-up milestone: 22b374c pushed to origin/main.

Manual equivalent: source the installed abbreviation file in local fish, type fm plus Space, inspect cd ~/coding/firstmate and cancel without Enter. No supplied command executes. Scope adds no runtime helper or dependency; preserve unrelated smoke edits.

Observed follow-up evidence before refresh: local installed fm PTY expansion exactly cd ~/coding/firstmate plus trailing Space, cleared without execution; target directory exists; fish -n exit 0. Admission suite 7 passed; inventory 241 entries with 0 missing/stale; README pass_no_change. Updated description/body costs: 132/7041 B, 33/1760.25 estimated tokens, weighted 209.025, score 3.827293. Required final activation check is rerun after refresh before commit/push.

Final pre-commit activation: refresh exit 0; repeated local interactive fm Space expansion passed without execution; installed fish syntax passed; installed delivery section matches canonical source. Delivery subject: docs(fish-alias): verify local expansion before delivery. Push configured origin/main immediately after commit.
