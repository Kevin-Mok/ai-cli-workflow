# Restore Super+1 workspace switching

Restore Windows+1 to workspace 11 and retain Alt+Windows+1 at 1800 K.

## Scope and decisions

Change the i3 binding, existing checker and matching README/smoke instructions. All other presets and Super+F11 remain. Initial git status captured; pre-existing dirty files and unrelated hunks are protected. Installed i3 is intentionally unmanaged and has private differences; apply only an exact guarded shortcut replacement there. No commit requested.

## Checklist

- [x] Inspect bindings, prior plans and live/source differences.
- [x] Observe updated checker RED, then minimally update source.
- [x] Verify source, refresh configuration, activate scoped live change and verify installed/running config.

## Verification and review

Run the existing checker against tracked, installed and running configuration; validate rendered i3 syntax and Redshift unit tests. Manually press Super+1 then Alt+Super+1: workspace 11 then 1800 K. Physical keyboard acceptance remains manual. Rollback replaces only the single changed binding. Memory lookup: redshift/Super/workspace found diagnostic IPC guidance, which applies only if testing actual keys. No prior remedy is assumed.

## Final evidence and handoff

Checker RED observed against old preset, GREEN after change. Source, installed and running checker pass (exit 0); i3 candidate syntax exit 0, reload success true; controller 6 tests and emoji checks 7 tests pass. Existing wheel deprecations remain. Required refresh-config attempted but stopped on an unrelated modified media-screensaver target; preserve it. Live activation used a guarded single-line replacement; no other installed bytes changed. No commit or push requested/performed.

Docs: README and smoke checklist now describe Super+1 workspace 11 and Alt+Super+1 1800 K. Rollback: revert this binding and checker/documentation expectations together. No abstraction or new dependency needed.

Cursor prompt: Review only the Super+1 workspace restoration in config.tmpl, smoke_redshift_keys.py and matching docs; preserve all unrelated dirty changes and the installed private configuration. Verify Alt+Super+1 still sets 1800 K and Super+1 only switches workspace 11.

Automated checks: python3 scripts/smoke_redshift_keys.py; python3 tests/test_redshift_control.py; python3 tests/test_cli_emoji_python.py. Runtime checks: run the checker against ~/.config/i3/config and --live. Manual: press Windows+1, expect workspace 11 without temperature change; press Alt+Windows+1, expect 1800 K without changing workspace; press Windows+F11, expect workspace 11. Physical input remains manual.

Suggested commit: fix(i3): restore Super+1 workspace shortcut

Final refreshed runtime evidence: the strengthened checker passed installed and running configuration after requiring Alt+Super+1 explicitly and rejecting duplicate Super+1 actions. Targeted postmortem ledger check and git diff --check both exited 0.

## Commit-session milestone

Authorized shipping after implementation: fix(i3): restore Super+1 workspace shortcut. Scope helper for session 01a15f88-6adf-7bf3-a588-2244abf3857f returned unsafe because wrapper writes were not detected. Direct-write evidence and the captured initial status establish the seven eligible files. Stage entire originally clean config/checker and new plan/report; stage only shortcut README/smoke hunks and this report ledger entry. Preserve all other baseline-dirty work. README recruiter gate: pass_no_change. Prior source/installed/live checks passed; 13 focused tests and two negative fixtures passed. No implementation work remains; physical key acceptance and full refresh conflict remain as documented. Target: main to origin/main; one normal push after commit and privacy gate. Rollback is a new inverse commit, without history rewriting.

Privacy gate initially blocked the real home alias in the report ledger. Sanitize that committed alias to the established example home; preserve real alias only in local dirty state. Fresh tests: 6 controller and 7 CLI checks passed. Two negative fixtures rejected missing Alt+Super+1 and duplicate Super+1.
