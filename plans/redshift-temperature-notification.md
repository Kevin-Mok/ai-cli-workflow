# Redshift temperature notification

Add a replaceable Dunst notification after successful manual temperature operations, keeping existing keys, state and stdout intact.

## Scope and decisions

The saved prompt `prompts/redshift-temperature-notification.md` authorizes implementation without commit/push. Extend `scripts/executable_redshift-control` at its locked success path; all existing i3, fish and login callers share it. Notify with applied/clamped kelvin using notify-send. The user's follow-up specifically prefers editing in place: capture the successful notification ID and use --replace-id for subsequent calls, retaining the stack tag as fallback. Notification failures must be best effort and bounded by a timeout. No monitor, dependencies or binding changes.

## Protected state and risks

Initial git status captured: pre-existing staged/unstaged postmortems, memory ledger, canonical instructions, MIME config, plans and untracked prompts remain untouched except additive ledger updates required for this task's incident. The original implementation request excluded commits; the subsequent `commit-session` request authorizes committing and pushing only this session's work. Keep prior Redshift plan unchanged. A daemon/external command may override the helper's saved state. Rollback this task's controller and docs hunks only.

## Checklist

- [x] Inspect controller, callers, tests, bindings, plan, feedback and lessons.
- [x] Add defining tests; observe RED for missing notification.
- [x] Add shared best-effort notification; observe GREEN and regression checks.
- [x] Update README and smoke checks; run refresh-config and verify installed controller.
- [x] Check real Dunst delivery without changing current temperature; record evidence and limits.

## Verification

Run `python3 -B tests/test_redshift_control.py`, binding checker (tracked/installed/live), fish syntax and Ubuntu startup regression. Tests cover set/adjust/reset/clamps, Redshift failure and missing/failing/timed-out notification. Live: reapply saved current value, inspect Dunst notification/history and unchanged state; verify repeated same-tag updates.

## Progress and review

Current design is the existing shared controller plus one best-effort subprocess call inside the lock after state persistence. Runtime deployment must preserve unrelated dirty work. Cursor prompt: Verify plans/redshift-temperature-notification.md and the shared controller's successful/failed notifications; preserve unrelated work. Commit suggestion: `feat(i3): notify Redshift temperature changes`.

## Evidence

- RED: `python3 -B tests/test_redshift_control.py` exited 1 with four expected failures: missing success notification and no notification attempt in the three notifier-error cases.
- GREEN: the same command exited 0 (4 tests); set/adjust/reset, both clamps, Redshift failure, missing notifier, nonzero notifier and timeout covered.
- Regression: `python3 -B scripts/smoke_redshift_keys.py`, installed and `--live` variants all exited 0. `bash tests/test_ubuntu_start.sh`, `fish -n dot_config/fish/functions/redshift-set.fish`, and `python3 -B tests/test_cli_emoji_python.py` (7 tests) exited 0. `git diff --check` exited 0.
- `fish -c refresh-config` exited 0 (REFRESH COMPLETE). Installed controller bytes equal source, including the new notification path.
- Runtime: installed helper `set 3000` twice exited 0, stdout remained `🌡️ Temperature: 3000 K`, saved temperature remained 3000. After expiration, Dunst history had one Redshift entry, id 105, title `🌡️ Redshift`, body `3000 K`, timeout 2000000 microseconds. This proves real delivery and replacement. Dunst was running and unpaused. Subjective popup appearance and physical keypresses were not observed; live binding checker passed. No deliberate live temperature change, reset or service shutdown was needed.
- Inspection-only missing-path incident documented in `docs/postmortem/2026-10-20-redshift-notification-inspection.md`; explicit no-new-learning ledger decision recorded and targeted check exited 0. Unrelated pre-existing dirty changes and index preserved. No commit or push requested or performed.

## In-place update clarification

The user's follow-up requested editing the same notification in place. An explicit identity probe showed stack-tag-only IDs 106/108, so earlier history evidence proved replacement only. Revised the implementation to persist the returned ID and pass --replace-id. Defining RED: missing --replace-id=123 (1 expected failure). GREEN: 5 controller tests and all previously listed regressions passed. Second refresh exited 0. Live installed set-current then adjust-0 reused ID 109/109 and kept 3000 K unchanged. Corrupt saved notification IDs fall back to a new notification. Expired notifications may receive new IDs. See the resolved notification-ID postmortem for evidence. Physical keypresses and subjective popup appearance remain unobserved.

Final review caught malformed UTF-8 and extremely long decimal IDs escaping the best-effort block. Both defining cases observed RED; catch ValueError makes final 6 controller tests pass. The same four related regression commands passed. Third refresh exited 0, installed source matches. A combined live assertion failed during active temperature changes (3900 K followed by 3150 K); immediate separate diagnostic freshly confirmed ID 109/109 with both adjust-0 calls at 3150 K. Do not restore any earlier temperature over current user changes. Final review issue resolved; no commit/push performed.

## Delivery milestone: feat(i3): update Redshift notifications in place

Completed: shared controller notification with returned-ID reuse, best-effort error handling, six controller tests, README/smoke docs, two task incidents and their isolated memory entries. Fresh commit-session verification: controller (6), CLI emoji (7), binding smoke, Ubuntu startup and fish syntax all passed; README gate `pass_no_change`. Runtime verification and rollback limits are recorded above. No implementation work remains. Subjective appearance was not checked.

The current session's scope helper returned unsafe because it detected no successful repo writes. Use directly observed patches and ledger writes from this conversation; exclude pre-existing untracked prompt and unrelated work. Use an isolated candidate index to preserve existing staged entries; include only task-specific sections/records of mixed memory files with public-safe aliases. Delivery sequence: privacy gate, one commit, one push to configured `origin/main`; report the resulting SHA and actual push status in the handoff. No known implementation blocker.
