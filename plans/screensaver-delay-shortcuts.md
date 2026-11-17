# Screensaver delay shortcuts

Keep immediate `ss` playback and let `sofs HOURS` turn displays off until one scheduled launch. Extend the existing timer installer, verify it with isolated tests, then refresh and deliver only this task's changes.

## Scope and decisions

- `ss` already maps to `~/scripts/media-screensaver preview`; preserve it.
- Replace `sofs` with the installer plus `--delay-hours`; retain `sofss` for daily 10 AM.
- Reuse the existing daily service/timer. A delay replaces the daily schedule with a non-enabled one-shot; reboot cancels it. Repeating the command restarts the full delay. Default installer/`sofss` restores daily scheduling.
- Accept positive finite fractional hours. Input may wake displays early; suspend may delay playback. Do not run either supplied display-changing shortcut during verification.
- Protected dirty state captured before changes: numerous unrelated files, including aliases, README and smoke tests. Preserve baseline copies in `/tmp/screensaver-shortcuts-baseline`; stage only this task's deltas.

## Checklist

- [x] Inspect mappings, timer implementation, callers, docs and existing tests.
- [x] Add failing delay, invalid-input, repeat/reset and failure-safety tests.
- [x] Add minimal delay option and preview/apply abbreviation through fish-alias helper.
- [x] Update README, screensaver guide and smoke checks; run focused regression and README gate.
- [x] Run shortcut-scoped refresh and verify installed expansion without execution.
- [x] Prepare scoped delivery; explicit commit-session now authorizes session commit/push.

## Verification and rollback

Automated: `python3 -B -m unittest discover -s tests -p test_screensaver_timer.py`; installed `executable_check-fish-abbr` for `ss` and `sofs`; Python compilation/diff checks. Unit tests isolate HOME and systemctl/xset, so displays never turn off.
Manual: type `ss` + Space and cancel; type `sofs 0.01` + Space and cancel to inspect expansion. User-run end-to-end check: dismiss any preview, run `sofs 0.01`, leave input untouched and observe displays off then playback after 36 seconds; rerun to verify replacement. Run `sofss` to restore 10 AM or installer `--disable` to cancel.
Rollback: restore previous `sofs` mapping and remove delay option, refresh; restore daily timer through installer. Cursor follow-up prompt: Verify sofs HOURS safely with isolated HOME and fake systemctl/xset, preserve unrelated work, and check installed abbreviation expansion without executing playback.

## Evidence and review

Initial inspection: immediate shortcut exists, delay option absent. No playback or power-off commands executed. Delivery subject: `feat(screensaver): add hours-delayed blackout shortcut`.

RED: ten tests ran with two expected missing-option errors. GREEN: ten timer tests passed. Related media suite: 49 cases, one failure and twelve errors from restricted X11/runtime access, documented in the validation incident. README gate: `pass_no_change`. Alias helper preview/apply: one prior sofs mapping preserved as a comment in power options. Activation will use the established shortcut-scoped refresh because live catalogs are migration-preserved and broad apply risks unrelated work.

Pre-delivery checks: Python AST parsing passed; postmortem ledger targeted check passed. No supplied shortcut executed. Broad refresh deliberately scoped to shortcut generation after merging only the requested row into the migration-preserved live catalog; no unrelated chezmoi targets applied. Physical wake and wrapped terminal clipboard paste remain untested.

Review caught scientific notation rejected by systemd; switched to decimal duration formatting and extended delay coverage to 0.00001 and 1000000 hours. Installed `systemd-analyze timespan 0.00001h 1000000h` accepts both (exit 0). Also stop the old timer before rewriting/reloading so rearming uses a fresh activation; ordering assertion observed RED before implementation. Independent review confirmed ordinary delay, failure safety and daily restore.

Final verification: ten focused timer tests passed (exit 0), including decimal edges and stop-before-reload. Shortcut-scoped refresh exited 0; installed `sofs` and unchanged `ss` both passed real interactive Space-expansion checks without execution. README gate `pass_no_change`; targeted incident ledger check passed. Pending: focused commit and origin/main push; no implementation blocker. Revert only this task’s commit and regenerate shortcuts to roll back.

Final diff review also covered fresh installation: stopping an unknown unit before writing it would fail. Added an executable regression (observed RED), then guard stop by existing timer-file presence; replacement tests seed the prior timer. Re-run focused tests and installed expansion after this necessary correction before commit.

Fresh-install correction verified: final focused suite ran ten tests, all passed (exit 0). No new runtime uncertainty beyond the already documented X11/sandbox limits. Delivery remains the one focused Conventional Commit above, then origin/main push; actual hash and push outcome are reported in the conversation.

Delivery blocker: automatic approval review rejected the exact focused commit/push to origin/main as consequential default-branch mutation and possible external disclosure without explicit authorization of this workflow. User-supplied fish-alias skill authorizes immediate commit/push, but review still rejected execution. No commit or push occurred; nine focused files/hunks remain staged and live shortcut activation is verified. Ask for explicit commit/push approval; do not bypass the rejection.

Sessiondelivery: later explicitcommit-session resolves the earlier authorizationblock; include this plan and shortcut changes with related finalmotion/blanking implementation. One focusedsessioncommit andorigin/mainpush; finalhash/result reportedinconversation. Priorblock entries remainhistoricalevidence.
