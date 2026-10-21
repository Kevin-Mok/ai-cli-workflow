# Repair Chrome updater verification

Repair the existing Ubuntu updater so it reports activity, reads the candidate from refreshed APT metadata, and accepts an installed version equal to or newer than the candidate. Keep the implementation, regression checks, documentation and reviewed incident learning in one focused commit.

## Scope and decisions

- Script: scripts/executable_update-chrome.sh; regression: tests/test_update_chrome_script.sh.
- Docs: Chrome command reference in README, Chrome smoke check, this plan and the living Chrome incident.
- Learning: only the Chrome lessons and reviewed-memory report/finding links.
- No dependency, browser restart, repository signing-key repair or system-package mutation by the agent. --check remains read-only and explicitly uses cached metadata.
- Normal mode refreshes metadata even when cached versions match, then skips installation when installed >= candidate according to dpkg ordering. Verification reads the candidate again after installation.

## Checklist

- [x] Capture initial Git status and inspect existing helper, callers, documentation and reviewed incident guidance.
- [x] Reproduce silent large-policy failure and missing query diagnostics before implementing full-output drain and explicit errors.
- [x] Reproduce stale-candidate verification and installed-newer false failure before changing candidate timing and comparisons.
- [x] Verify all eleven scenarios, syntax and read-only live CLI checks; update docs, lessons and reviewed incident memory.
- [x] Review only current-session files/hunks, pass README check, neutralize privacy findings and preserve unrelated dirty work.
- [x] Prepare delivery milestone: fix(chrome): verify against refreshed apt candidate; verification and scope review complete, with one origin/main push authorized after the mandatory privacy check.

## Evidence and review

- RED: large mock policy output produced silent status1. Full drain repaired it, then the failed-query diagnostic assertion failed as expected.
- RED follow-up: metadata advancing to156 caused comparison against the saved146 candidate; after fresh candidate reads, the newer-installed fixture still attempted installation.
- GREEN: bash tests/test_update_chrome_script.sh exits0 for eleven scenarios; bash -n scripts/executable_update-chrome.sh tests/test_update_chrome_script.sh exits0, including after neutral fixture changes. Scenarios cover existing behavior, large output, query errors, metadata advancement, equal cached versions, newer installed versions and incomplete upgrade rejection.
- Live --check and binary --version exit0: installed/candidate both156.0.8078.47-1; Google Chrome156.0.8078.47. The user's sudo transcript confirms successful installation. No second privileged update or browser relaunch by the agent.
- README gate: pass_no_change. Scoped staged diff check: exit0. Targeted staged-memory check: exit0, one reviewed report, no errors, using only an ephemeral neutral-to-local alias substitution.
- Initial staging hit the read-only .git sandbox boundary; reviewed staging succeeded with repository-write escalation. Privacy gate initially blocked home paths and IP-shaped version fixtures; task-owned paths and fake versions were neutralized without exemptions. Keep hooks active and recheck immediately before committing.

## Session scope and delivery

Session 01a15bd2-7168-76b0-af68-93f86231529b: scope helper reported unsafe because it did not detect wrapped tool writes. The recorded pre-write status and directly observed edits establish eligibility. Full Chrome script, test, incident and plan are eligible; shared files include only Chrome hunks. Ten files total. Prior unrelated commits remain intact.

Exclude unrelated changes in docs/postmortem/2026-10-20-description-handoff-runtime.md, docs/postmortem/2026-10-20-redshift-handoff-byte-check.md, memory api-contracts-fixtures.md and state-security.md, non-Chrome operational-drift.md and sources.json hunks, plans/github-recruiter-descriptions.md, plans/screensaver-video-orientation.md, and the monitor-media-screensaver, recruiter-github-descriptions, redshift-temperature-notification and tmux-drag-scroll-copy prompts. Preserve any additional concurrent dirties; inspect final status after push.

## Manual verification, risks and rollback

From the repository root, run ./scripts/executable_update-chrome.sh --check and google-chrome-stable --version without sudo. Both should report156.0.8078.47 (the APT package includes -1). Run sudo ./scripts/executable_update-chrome.sh to refresh configured repository metadata and update if needed, then relaunch Chrome and inspect chrome://settings/help. Version values are examples, not permanent pins.

Repository availability and pinning determine the APT candidate; this is not an independent check of Google's newest published release. Existing unrelated repository warnings remain out of scope. Rollback is an ordinary follow-up revert of this focused commit; do not rewrite history or revert unrelated work. No tracked configuration files were changed, so no configuration refresh is needed.

## Handoff

Atomic change: drain policy output and surface errors, refresh before candidate display/decision, re-read after installation and compare with dpkg ge; include tests/docs/learning together. Commit subject: fix(chrome): verify against refreshed apt candidate.

Cursor prompt: “Read plans/chrome-updater-silent-exit.md and the linked Chrome incident. Review refreshed candidate selection and Debian version ordering, then rerun the focused Bash test and syntax check. Preserve unrelated dirty work; verify the loaded browser version only after a human relaunch.”
