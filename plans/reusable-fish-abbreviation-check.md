# Reusable local fish abbreviation check

Provide one command that tests real local interactive abbreviation expansion without executing the mapped command. Run it after each changed mapping is refreshed and before commit/push, and when shortcut generation changes; do not run it at shell startup or for unchanged no-op requests.

## Scope and decisions

Reuse the successful temporary PTY trial. Add scripts/executable_check-fish-abbr with a default disposable trial and optional NAME EXPECTED arguments to check an installed abbreviation. Load the installed catalog, validate fish syntax, capture Space expansion and clear it. Default trial explicitly erases its process-local abbreviation and checks absence. No dependencies, scheduled tasks or changes to existing mappings.

Protected initial state: pre-existing README/smoke/feedback/ledger/reference/fish-progress/Vesktop/approval/lessons/Firstmate changes and the prior temporary-trial incident are unrelated; preserve them. Stage only session hunks if delivering a commit.

## Checklist

- [x] Read existing trial and reserved-keyword PTY regression.
- [x] Write defining integration tests and observe RED before implementation.
- [x] Implement the smallest CLI with --plain/--details, actionable failure and bounded waiting.
- [x] Update skill, admission cost, README usage and existing smoke check with cadence.
- [x] Focused checker 4 tests, reserved-keyword regression 1, skill admissions 7 and catalog inventory passed. Local default, fm and --plain checks passed before final refresh.
- [x] Refresh and repeat local CLI activation before commit/push.
- [x] Prepare scoped commit/push workflow gated by local verification; outcomes reported in final handoff.

## Verification

Integration tests: default trial cleanup; installed abbreviation with shell metacharacters expands literally without running; wrong expectation and missing abbreviation fail. Use isolated HOME fixtures with installed catalog path. Run reserved-keyword regression and skill admission/catalog checks. Local checks: default temporary trial, fm expected cd ~/coding/firstmate, and command --plain mode.

## Risks and rollback

PTY verifies local fish expansion after sourcing the installed file; it cannot reload existing user terminals. Arbitrary installed source files are trusted configuration. No mapped command executes. Remove helper and its documentation/skill reference to roll back; existing abbreviations remain unchanged. Keep plan and verification evidence with implementation.

RED: 4 integration tests failed because CLI was absent. GREEN: all 4 pass, plus existing reserved-keyword PTY regression (1). Admission cost updated before skill edit, same scope/precedents and unchanged description. No new trigger or dependency. Checker stays runnable from the repository because rf excludes deployment of scripts.

Review: independent read-only review found no concrete defect in quoting, bounded waits, non-execution or child cleanup. Installed catalog is trusted sourced configuration. Broader test_fish_alias suite is blocked by pre-existing invalid test_example-user_home_directory_normalization in HEAD; recorded in docs/postmortem/2026-11-06-fish-alias-regression-identifier.md. Do not count it as passing. README gate pass_no_change. Helper remains directly runnable from checkout; no separate installation required.

Final activation: refresh exit 0; default disposable trial, installed fm check and ASCII trial all passed after refresh; temporary abbreviations removed. Installed delivery section matches canonical source. Delivery milestone: feat(fish): add reusable local abbreviation check. Stage only session-owned hunks and push origin/main immediately after verified commit. No scheduled run added.
