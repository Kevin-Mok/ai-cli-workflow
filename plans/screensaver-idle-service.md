# Screensaver idle service

Keep the existing 300-second idle monitor running under a systemd user service. Install the unit, launch it from i3 with the current X11 environment, and retain browser/lock gates.

## Context and scope

The daemon already handles five-minute raw-input inactivity, locking, preview cleanup and duplicate prevention. Change only installation/startup, service asset, CLI tests and matching README/guide/smoke checks. Preserve all initial dirty files listed by the initial git status, including pre-existing postmortem ledger edits. Commit/push now authorized by `$commit-session` (initial implementation was uncommitted).

## Decisions

Use a service with Restart=always and five-second retry; no timer. i3 invokes a `service` command importing DISPLAY, XAUTHORITY and XDG_SESSION_ID before starting the unit. Do not enable at default.target before X11 is available. Installation writes/reloads the unit; service startup is explicit and at each i3 login. Stop/restart using systemctl. Existing foreground daemon remains available.

## Checklist

- [x] Inspect scope and initial status.
- [x] Add defining service installation/start tests and observe RED.
- [x] Implement unit, CLI service activation and i3 migration preserving unrelated lines.
- [x] Update README, guide and smoke checklist.
- [x] Run regression tests, refresh-config, install/start live service and inspect status/journal.
- [x] Record evidence and review.

## Verification

Automated: screensaver Python suite under Xvfb, browser Node suite and desktop layout regression. Unit syntax via systemd-analyze verify. Live: install, service, systemctl show/status, CLI status; restart recovery by terminating only the service MainPID. Uninterrupted five-minute idle and full lock/suspend acceptance remain separate desktop observations.

## Risks and rollback

Browser coverage still intentionally suppresses activation. A legacy daemon must be stopped by verified owned PID before service takes over. No unrelated players or listeners may be killed. Rollback: stop media-screensaver.service and restore the prior i3 daemon line. Service PartOf=graphical-session.target permits normal desktop teardown. Home writes/system bus access may need scoped sandbox escalation.

## Progress and review

Source map confirms IDLE_SECONDS=300 and existing threshold test. Inspection guessed a nonexistent refresh script and sandbox blocks the user bus; tracked in the service inspection postmortem. Initial inspection preceded implementation; final evidence is below.

RED: CLI suite exited 1: four passed, missing service action errored and absent i3 service startup failed. Unit installation is file-only; `service` performs daemon-reload before importing environment and starting.

## Final evidence and outstanding acceptance

- Python: `xvfb-run -a python3 -B -m unittest discover -s tests -p 'test_media_screensaver*.py' -v`: 38/38 passed with scoped display access. Initial sandbox-only run had eight X11 errors; tracked in incident.
- `node tests/test_media_screensaver_browser.cjs` and `bash tests/test_desktop_display_layout.sh`: passed, exit 0.
- `systemd-analyze --user verify scripts/media_screensaver/media-screensaver.service`: exit 0, sandbox bus warnings only.
- Explicit installer exit 0; live i3 config contains exactly `exec --no-startup-id /home/example/scripts/media-screensaver service`.
- `fish -c refresh-config`: attempted, exit 1 on unrelated live mimeapps.list drift; preserved it. Explicit installer installed screensaver files and startup without requiring global refresh success.
- Live service initially encountered legacy daemon lock contention. Scoped UID/argv verification permitted stopping only legacy PID 2546817; service then ran as PID 2683032.
- Live recovery: `systemctl --user kill --signal=TERM --kill-whom=main media-screensaver.service` exited 0; journal shows graceful cleanup at 14:32:53 and restart at 14:32:58, new PID 2683510, active/running and Restart=always.
- CLI status confirms running idle monitor; bridge unavailable intentionally suppresses automatic activation. Operator must enable unpacked extension in every Chrome profile and reload tabs before five-minute playback can be accepted. No full uninterrupted idle wait or suspend/resume performed.
- Self-review: unit and installer/package paths agree; i3 migration removes only owned legacy line; foreground daemon, gate behavior and 300-second threshold retained. No new dependency. Commit/push now authorized by `$commit-session` (initial implementation was uncommitted). Concurrent unrelated README/smoke/postmortem/lesson changes remain untouched.

## Handoff

Atomic plan: install service asset and `service` CLI → migrate i3 startup → verify existing 300-second boundary and recovery → enable browser bridge and perform five-minute smoke acceptance. Implementation is installed; bridge acceptance remains outstanding.

Cursor prompt: “Read plans/screensaver-idle-service.md and docs/media-screensaver.md. Preserve unrelated work. Verify media-screensaver.service is active, enable the unpacked extension in all Chrome profiles, reload tabs, then run the five-minute idle/activity/lock smoke checks. Keep fail-closed browser checks. Resolve refresh-config mimeapps.list conflict only with an explicit decision about the local file.”

Suggested commit: `feat(screensaver): supervise five-minute idle daemon`

Docs updated: README usage, media-screensaver installation/service lifecycle/rollback, smoke checklist service recovery and idle acceptance. Remaining risk: unavailable browser bridge blocks auto playback by design; full chezmoi refresh was not completed.

Follow-up 14:49 log: scoped metadata inspection finds native host manifests/executable present, expected extension absent from saved Chrome profile registrations and no bridge state files. Browser setup remains pending. Guide/smoke entries now explicitly distinguish native-host installation from Chrome Load unpacked and explain idle 0–1s during input. No runtime changes; no further automated regressions needed for this documentation clarification.

Immediate command follow-up: `ss` now expands to `~/scripts/media-screensaver preview` in power options; legacy command commented. Required refresh attempted but blocked by local mimeapps drift. Preserved broad live alias differences by patching only ss, then regenerated shortcuts. Fish syntax and isolated abbreviation inspection passed. Preview intentionally not executed per fish-alias skill. Docs updated with mapping/loading instructions.

## Delivery milestone: feat(screensaver): supervise five-minute idle daemon

Completed: service lifecycle, i3 startup migration, immediate ss abbreviation and matching setup/smoke documentation. Fresh pre-commit Python suite passed 38/38; browser and display regressions and fish syntax passed; README recruiter gate returned pass_no_change. Prior live service restart recovery remains verified. Remaining: extension setup/five-minute acceptance and unrelated global refresh conflict.

Scoping session: 01a15a92-db1d-7203-92ec-ed73e3be82ad. Scope helper returned unsafe because its parser detected no successful wrapped writes; direct conversation write evidence is the fallback. Include only observed screensaver files/hunks and this report's ledger record. Preserve all unrelated work, including pre-existing ledger and reference edits, UBS mount changes and untracked prompts. Reviewed rollback remains service stop and restoration of prior startup/mapping. Next: privacy check, focused commit, then push origin/main.

Privacy review: initial candidate blocked three home_path findings; canonical example paths replace machine-specific paths in public artifacts. Ledger staging is limited to the new report, preserving unrelated byte formatting and dirty records.

Ledger privacy boundary: public report aliases use the repository's canonical `/home/example` path convention. The targeted checker requires exact actual paths, so its successful local check uses an additional machine-local alias that is excluded from the public staged ledger. Unrelated ledger records remain untouched in the commit.

Final candidate review: README/smoke/index ledger hunks contain only session changes; unrelated formatting hunks removed. Privacy gate passed after canonical-path repair. All 11 staged files are under 3 MB. Delivery milestone will be identified by its subject above; resulting hash and actual push outcome are reported in Codex output.
