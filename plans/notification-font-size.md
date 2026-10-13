# Enlarge and widen notifications

Increase desktop notification readability, apply supported sizing and verify real popup dimensions before sending samples.

## Purpose, context and final scope
Final Dunst font is Hack Nerd Font Mono 23.25pt (1.5x the preceding 15.5pt). Supported width=467 renders about 669px including frame on the current 135-DPI desktop, one third shorter than the preceding 1003px setting. Height follows text up to 600 logical pixels. Origin top-right, offset 30x20, notification_limit 5. User chose large text and growing height over a forced 16:9 crop.
The sample helper sends Codex/Discord with large text throughout, supports --app, --plain and explicit --compare old/new references, and avoids the codex-kitty audio rule.

## Assumptions and decisions
Configured dimensions are logical and scaled automatically; physical width is measured. Do not change font or scale to achieve width. Dunst 1.9.2 removed geometry/notification_height, so use supported keys and restart via existing activation helper.

## Ordered checklist
- [x] Capture initial status and preserve unrelated dirty work.
- [x] Observe original font/helper RED, implement and pass.
- [x] Revise default samples after screenshot; old baseline now opt-in.
- [x] Reproduce ignored legacy sizing (435px actual), consult local/official documentation and record incident.
- [x] Implement supported sizing; resolve render-readiness race and DPI scaling.
- [x] Measure 250px compact popup, then honor latest request for at least twice the width.
- [x] Observe updated width RED, implement 347 logical width and pass all five tests.
- [x] Refresh, activate and measure actual 501 x 134 Codex popup.
- [x] Reconcile README, smoke tests, incident, memory learning and this plan.

## Risks, protected state and rollback
README, smoke tests, memory ledger/references, lessons and many unrelated files were dirty before this task; add only related sections. Other sessions run concurrently. No commits requested. Restart clears history/queue. Rendering depends on DPI; final visual comfort remains user judgment. For preceding compact size restore supported width=169, refresh and restart; do not restore removed legacy settings.

## Verification and evidence
Automated: from /home/example/linux-config run `python3 -B tests/test_notification_font.py` (five passes after RED). Check task diff with git diff --check. Run targeted postmortem-memory check for docs/postmortem/2026-10-13-dunst-ignored-sizing.md.
Runtime: refresh-config reported REFRESH COMPLETE, exit 0. Activation and sample send succeeded, exit 0. Source/live config bytes match. Bounded xwininfo polling measured 501 x 134, compared with earlier 250 x 270. New daemon logs have no geometry/notification_height warnings. Unrelated startup/shortcut warnings remain outside scope.
Manual: `~/scripts/notification-font-test --app codex`; while visible, `xwininfo -name Dunst` should report width about 669 on this desktop. `~/scripts/notification-font-test --app discord --plain` should show large chat text and ASCII terminal output. Default sends both; --compare deliberately includes small old-size references. No sudo. Popups last 15 seconds.

## Progress and review notes
Earlier widths 500/700 edited ignored geometry keys; they were not runtime successes. Corrected under docs/postmortem/2026-10-13-dunst-ignored-sizing.md, with a verified runtime finding in tracked memory. Final change preserves large text and natural height, and meets latest at-least-double-width request. Keep config/helper/tests, related README/smoke entries, plan and incident/learning in one focused change. Commit-session is now authorized; previous implementation milestones below retain their historical delivery state. Suggested subject: `feat(notifications): enlarge text and size popups correctly`.

## Paste-ready Cursor prompt
Review plans/notification-font-size.md and relevant Dunst/helper/tests/docs changes, preserving unrelated dirty work. Run five focused tests and targeted sizing-postmortem memory check. Activate only after refresh, send a single installed sample and poll until rendered; verify about 669px width at current Xft.dpi=135 with supported width=467. Confirm large font and content-driven height. Keep docs and learning in the same change. Do not commit unless requested.

Final learning check: targeted postmortem-memory check passed with zero errors, exit 0 (reviewed hash 048c41904d06255c9a2237a08f190804172c7ea89c83cb94fbf7c095cd9f7117). Schema authoring correction recorded in incident. Final focused tests: five passes; scoped diff check passes.

## Latest font increase
User requests 1.5x larger font: 15.5 * 1.5 = 23.25pt. Keep supported width=347 (501px rendered) and natural height. Comparison helper should now show previous 15.5pt versus new 23.25pt, not the older original 8pt reference.
- [x] Observe RED, update font/helper/docs and pass focused checks.
- [x] Refresh, activate, confirm source/live, measure same-width taller popup and send samples.

1.5x font evidence: three expected RED failures then five GREEN passes; refresh completed and activation succeeded (exit 0). Installed config/helper match source. Render-ready Codex popup measured 501 x 239, compared with 501 x 134 at 15.5pt. Font now 23.25pt and --compare uses 15.5pt versus 23.25pt. README/smoke checks updated. No commit requested. To roll back only this increase, restore 15.5pt and helper comparison labels/sizes, refresh and activate.

## Latest width doubling
Double the current 501px physical width while retaining 23.25pt font and natural height. Set supported width=704 logical pixels (about 1003px including frame at 135 DPI); allow one-pixel rounding. Existing 2048px screen can accommodate it. Preserve unrelated dirty work.
- [x] Observe width RED, implement and pass tests.
- [x] Refresh, activate, measure rendered width and send samples.
Rollback for this step: restore width=347, refresh and activate.

Latest width verification: expected RED at 347, then five GREEN passes at 704. refresh-config reported REFRESH COMPLETE, activation/sample send exited 0, source/live match, actual popup 1003 x 187. Width is at least double previous 501px; 23.25pt font retained. README and smoke checks document new dimensions. No commit requested.

## Latest width reduction
Interpret user request "1/3 width shorter" as reducing width by one third: 1003 * 2/3 is about 669 physical pixels. Use supported width=467 logical pixels at current DPI; keep 23.25pt font and natural height. Preserve unrelated dirty work.
- [x] Observe RED, implement and verify tests.
- [x] Refresh, activate, measure width and send samples.
Rollback for this step: restore width=704, refresh and activate.

Reduction evidence: expected RED at 704, then five GREEN passes at 467. refresh-config completed, activation/sample send exited 0, source/live config match. Actual popup 669 x 239; width approximately two thirds of previous 1003. Font remains 23.25pt. README and smoke tests updated. No commit requested.

## Commit milestone: feat(notifications): enlarge text and correct popup sizing
Session ID: 01a13605-2f04-7db2-aaa9-1e3a40a6c13d. Scope helper reports unsafe because nested orchestration writes were not detected; use directly observed writes and captured pre-write baseline. Deliver 11 paths: Dunst config, helper, tests, this plan, two session incident reports, and only our hunks in README, smoke tests, lessons, memory reference and ledger. Leave all other pre-existing/concurrent changes unstaged.
Completed: 23.25pt font, about 669px rendered width, samples and documentation; fresh five-test pass, both targeted memory checks pass, README gate pass. README notification section moved before terminal License to preserve the contract. Rollback and review remain documented above. No blockers. Next: inspect and verify isolated staged content, commit once and push main to origin/main. Commit hash will be reported in Codex output; commit milestone recorded here by subject.

Commit preflight evidence: isolated staged snapshot passes five notification tests, both incident-learning checks and README gate; cached diff has no whitespace errors. Fresh installed comparison and ASCII Discord samples exit 0; render-ready xwininfo reports 669px width. Staged scope is exactly 11 intended paths, with only notification additions in five shared files. Unrelated UTF-8 serialization differences excluded from the staged ledger. Ready to create the single milestone commit and push origin/main.
