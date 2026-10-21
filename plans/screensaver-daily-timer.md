# Daily screensaver timer

Install a systemd user timer for 10:00 AM local time using a reusable script. Keep the existing five-minute idle service unchanged and provide a safe scheduled entrypoint.

## Scope and decisions

Add scripts/executable_setup-screensaver-timer, a scheduled command in scripts/media_screensaver/main.py, focused tests, and usage/smoke/README documentation. Use a separate daily service, Persistent=false (no inactive/poweroff catch-up; suspend may launch on resume), one-second timer accuracy. Require an installed screensaver and X11 desktop for installation; import its display/session environment. Scheduled playback preserves lock/browser gates and renderer dismissal. No sudo, cron or dependency installation. The later commit-session request authorizes a scoped commit and upstream push. Plan Mode is unavailable; execution is recorded here.

## Checklist

- [x] Capture git status and inspect launcher/install/service/tests and feedback.
- [x] RED: installer creates correct units/enables timer; scheduled skips locked sessions.
- [x] GREEN: implement installer and scheduled entrypoint.
- [x] Update guide, README and grouped smoke checks, preserving existing dirty hunks.
- [x] Focused/regression tests and real systemd calendar verification; inspect final diff.

## Risks and rollback

Initial dirty files include README, smoke tests, lessons, ubuntu-start, orientation and unrelated plans/prompts/postmortem memory. Preserve all. User must be logged into X11; no wake-from-suspend. A timer due during suspend may launch on resume. Existing idle daemon can also launch playback; a new shared preview lock prevents simultaneous renderers. Disable with systemctl --user disable --now media-screensaver-daily.timer; stop daily service separately for immediate playback cleanup. Installation writes only its two named units, not media or unrelated config. Script installation into live home is deferred to the user's desktop invocation unless authorized execution is available.

## Verification and review

Automated: Python unittest discover for test_screensaver_timer.py and existing screensaver CLI tests. Tests use temporary HOME and strict systemctl boundary double; actual unit parser/calendar checked with systemd-analyze. Manual: run installer from desktop, inspect list-timers, start daily service on unlocked desktop, dismiss with input; test lock/browser suppression. Confirm no inactive-timer catch-up and repeat installation. Cursor prompt: Review plans/screensaver-daily-timer.md, run focused tests, inspect generated units and verify next local 10:00 plus dismissal on desktop; preserve unrelated work. Suggested commit: feat(screensaver): add daily 10am timer installer.

## Evidence

RED observed missing installer and argparse rejection of scheduled command. Initial GREEN: 2 timer tests and 6 existing CLI tests passed. A defining duplicate-playback test then failed because the second preview began scanning; added shared nonblocking flock around preview. Installer now also rejects an outdated launcher before any writes. Unit files parsed by systemd-analyze --user verify (exit 0); sandbox emits unavailable bus/socket diagnostics, so this proves parser acceptance, not live installation. systemd-analyze calendar confirmed next 10:00 EDT is 2026-10-22 10:00, UTC 14:00. No live home/systemd files changed. No tracked managed config changed, so refresh-config does not apply; package deployment uses the explicit existing installer.

Read-only inspection path miss recorded in docs/postmortem/2026-10-21-screensaver-timer-inspection.md; existing local-discover-paths-before-reads applies. No new reusable learning. Added reviewed report hash to the existing dirty ledger, preserving its entries; targeted check passed (0 errors).

Final automated verification: timer suite 4/4, focused CLI 6/6, complete Xvfb screensaver suite 57/57, browser CJS passed. Initial sandbox restrictions on runtime lock and X11 are recorded in the same postmortem; scoped test reruns passed. Xvfb emitted DRI2/deprecation/resource diagnostics. git diff --check passed. Manual desktop timer enable/start/dismiss/lock acceptance remains for the user's installation. No live timer was enabled and no commit/push performed. Updated docs: README, screensaver guide and grouped smoke tests. Direct handoff sequence: update launcher → run setup-screensaver-timer → inspect list-timers.

Independent review caught systemd suspend semantics: Persistent=false skips inactive/poweroff catch-up but calendar timers may fire on resume. Corrected installer message, README, guide and smoke check; no unsupported promise of skipping suspended events remains.

## Delivery milestone — feat(screensaver): add daily 10am timer installer

Implementation and documentation are complete. Reviewed the 10:00 calendar, lock/browser suppression and shared playback ownership; existing regression evidence is above. README gate returned pass_no_change. Session helper reported unsafe because orchestration writes were not recognized; direct conversation write evidence establishes scope for this task. Stage only the daily timer additions from baseline-dirty README/smoke/ledger files; preserve all unrelated work. Commit contains this plan and incident report. The exact physical ledger alias/hash update remains local because the public privacy gate rejected its home path; no privacy policy was relaxed. Live activation remains pending on the desktop; no installation is claimed. Next step after commit: push the complete single-commit session to origin/main.

Commit-session fresh check: timer suite 4/4 (exit 0); staged whitespace check passed. Public privacy gate initially blocked one machine home path in the ledger; removed only this ledger entry from staging and retained local learning coverage. Other pre-existing ledger edits remain untouched.

Narrowed privacy candidate passed (exit 0); eight intended task files remain staged, with README/smoke hunks separated from unrelated work. Final commit repeats the unchanged privacy gate. No implementation blockers remain; live desktop installation and acceptance are the remaining manual steps.
