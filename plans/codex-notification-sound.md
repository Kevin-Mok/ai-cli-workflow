# Codex notification sound

Add optional local MP3 playback to every displayed Codex popup, including completion and approval notifications, by tagging the existing Kitty notification and letting Dunst invoke an isolated helper. The selected clip is now stored at `scripts/can-i-ask-you-a-question.mp3` by explicit user request; installation still leaves sound disabled until a local path is configured.

## Context and scope

- Codex config already uses `tui.notifications = true` and `notification_method = "osc9"`; do not change it or add a completion-only notify hook.
- Kitty 0.49.2 loads `notifications.py:main(command)`. A false return preserves the existing notification, and its visibility gate runs before the callback. Channel IDs identify windows, not the active terminal.
- Dunst 1.9.2 and mpv are installed. Inspect its exact script execution contract before choosing rule options.
- Change only new callback/helper/tests/docs/prompt and the narrow Dunst rule. Root README and smoke tests contain pre-existing edits; append only this task's content.
- Initial status captured before writes: many unrelated backup, session-search, aliases, lessons and postmortem-memory edits/untracked files. Preserve all; no staging, commit, push or worktree. `dot_codex/config.toml` has skip-worktree set; refresh snapshots must be compared with its current bytes.

## Assumptions and decisions

- Confirm Codex via originating window's foreground process and `/proc/PID/exe` basename `codex`; avoid arbitrary text, active-window fallback and subprocess lookups inside Kitty.
- Tag only `application_name = "codex-kitty"`; return false and preserve content, timing, focus actions and suppression.
- Helper uses a machine-local JSON setting under XDG config; the selected clip is included under scripts with an exact Git LFS attribute (user override of the original no-bundled-clip scope). Use argv without a shell and mpv's `--` path delimiter.
- Dunst runs the playback helper in a separate process. Errors are logged and never replace or break notifications.
- Ruling: execute the supplied approved design directly in the existing checkout using this ExecPlan as the ledger. User forbids commits and worktrees; those override generic skill setup/finish flows.

## Ordered checklist

- [x] Capture dirty state, inspect config, installed APIs and required instructions.
- [x] Write defining fake-window/process and player tests; observe intentional RED.
- [x] Implement origin tagging and playback/configure/preview/disable/status/manual helper.
- [x] Verify installed API loading, isolated chezmoi deployment and relevant regression tests.
- [x] Update README, smoke checks, usage/rollback documentation and reusable handoff prompt.
- [x] Run refresh-config after preflight; verify deployed bytes and restart Dunst.
- [x] Review complete task diff, record final evidence and pending live MP3 checks.

## Risks and rollback

Foreground process inspection can race with process exit; fail open to ordinary Kitty notifications. Remote SSH/tmux Codex is not locally identifiable and stays untagged. Binary-name origin detection is local application classification, not a security boundary. MP3/player/config failures must be diagnostic-only. Dunst script duplicate/replay timing requires exact-version verification. Callback reload may require a fresh Kitty instance.

Disable sound immediately with `~/scripts/codex-notification-sound disable`. Full rollback removes only this task's Dunst rule and new callback/helper, then refreshes config and starts fresh Kitty; preserve unrelated dirty files. No `git reset`/`checkout` rollback.

## Automated and manual verification

Run `python3 -B tests/test_codex_notification_sound.py` for completion/approval identity, channel isolation, unrelated processes/text, disappeared process, safe paths, invalid/missing configuration/player, player failure, exact one spawn, and installed executable layout. Record RED and GREEN output.

Run focused existing terminal/refresh tests after reading their commands. Validate with installed Kitty Python and isolated Dunst on private DBus where available. Use a mocked player for live daemon rule timing and dedup tests without playing audio. Run `fish -ic 'refresh-config'` only after snapshot/dirty preflight, then compare installed callback, helper and Dunst config byte-for-byte.

User manual commands: configure a clip with spaces, preview, tagged/unrelated smoke notifications, genuine Codex completion and approval while unfocused, focused suppression, click-to-focus and disable. These are pending until the user chooses an MP3.

## Progress and evidence

Initial default exec failed before execution (`bwrap` loopback); scoped escalation works. Living incident and reviewed no-new-learning record: [environment postmortem](../docs/postmortem/2026-10-07-codex-notification-sound-environment.md). Targeted memory check exit 0. Read-only API agent independently verified installed callback order/signature and channel mapping.

## Review notes

Implementation and focused automated verification complete; real MP3/Codex TUI acceptance remains manual. Keep one popup, no copied text-based origin heuristics, and no automatic/default sound selection. Record refresh side effects separately from session-owned changes.

### Dunst ruling

Ruling: preserve native duplicate stacking rather than add persistent ID/text deduplication. Actual 1.9.2 replaces a coalesced duplicate with an unsounded object: no immediate second playback, but its later history recall may sound once. Normal already-sounded history remains silent. The initial universal history-silence assertion was an inspection assumption beyond the user spec; the test now distinguishes both native paths without weakening completion, approval, unrelated, queued or suppressed behavior. No new popup or replay is manufactured by this hook.

### Verification so far

- Unit RED: `python3 -B tests/test_codex_notification_sound.py` exited 1 with 13 defining missing-implementation assertions. GREEN: same command exited 0, 13 tests, including empty-home chezmoi installation and explicit failure-path diagnostics.
- Daemon RED after correcting nonactivating DBus readiness: `xvfb-run -a dbus-run-session -- python3 -B tests/scripts/codex_notification_daemon_check.py` exited 1 because no production sound rule existed. GREEN after rule and native-history distinction: exit 0, 1 real-daemon integration test with four fake-player calls across scenarios.
- `basedpyright --level error scripts/executable_codex-notification-sound`: exit 0; 0 errors/warnings.
- Snapshot dry-run passed. Codex source is skip-worktree and differs from HEAD; live/source differ in model. User explicitly approved full refresh and live-over-tracked replacement on 2026-10-07. Preserve all other pre-existing work. Docs explain daemon restart and fresh Kitty activation; no live MP3 selected.

### Review and activation follow-up

Fresh review found no callback/player/rule runtime defect. Fixed an overbroad Dunst comment and added a reusable activation command (no sudo) that restarts the verified current-session Dunst bus owner, optionally starts fresh Kitty, and preserves sound settings/existing terminals. Activation defining RED exited 1 at the missing-helper assertion; GREEN integration now restarts its private daemon, verifies a new PID and empty history, then verifies the same sound rule still works (five total fake-player calls).

Existing terminal workflow/wrapper and refresh-function regressions exited 0. Real downloader installed-layout unittest: exit 0, one test. Broader `tests/test_postmortem_memory.py`: 25/26 passed; `WorkflowTest.test_actual_ledger_reference_status_and_coverage` failed on unrelated whole-corpus unregistered historical aliases/new reports. Preserve their ownership; task-targeted memory checks establish current incident registration. User-approved refresh finished with `REFRESH COMPLETE` and exit 0; deployed callback/player/Dunst bytes matched, helper executable, local sound disabled, live/tracked Codex bytes identical. Source skip-worktree remains protected. A concurrent task also changed postmortem artifact-verification guidance; do not revert it.

### Final implementation state

- Second full refresh exited 0 with REFRESH COMPLETE; includes activation helper and corrected Dunst comment.
- Installed Kitty callback probe passed against real NotificationCommand with its required weak-cache/log dependencies. Only application_name changed; existing focus actions/timeout were retained. The initial incorrect constructor probe is documented in the living environment incident and was not credited as evidence.
- `~/scripts/codex-notification-activate` exited 0 on the live desktop: verified current-session Dunst owner restarted, existing Kitty sessions retained; `dunstctl count displayed` and `waiting` both 0. This activation resets Dunst history/queue. No fresh Kitty was opened automatically; run the helper with --open-kitty for the new callback process.
- `~/scripts/codex-notification-sound status`: disabled; no setting/clip was written into the repo or live config.
- Whole-corpus coverage summary: five unrelated new reports and 204 unregistered aliases, zero changed hashes/missing_sources. Task incident schema/hash checks are separate from that historical-corpus gap. Preserve all concurrent/pre-existing work.
- Code review's only concerns were corrected: native history caveat in the config comment and an executable activation procedure. Activation defining RED→GREEN and final daemon suite cover the correction; no review issue remains deferred.

### Final acceptance boundaries and delivery

Automated verification covers channel origin classification, error isolation/argv, actual Dunst delivery/stacking/history/queue suppression, real empty-home executable installation, actual installed Kitty object loading and live disabled-state deployment. User-selected MP3 audio, genuine completion/approval, upstream focused suppression and click-to-focus still require the linked smoke checks in a fresh Kitty process. The callback does not change those native fields or emission settings.

Atomic scope: callback, sound/activation helpers, narrow Dunst rule, defining tests, guide/README/smoke updates, this ExecPlan, handoff prompt, living incidents and directly reviewed learning. No commits, staging or pushes. Suggested future subject: feat(notifications): add optional Codex popup sound. Rollback and exact automated/manual commands are in docs/codex-notification-sound.md; paste-ready continuation prompt is prompts/codex-notification-sound.md.

### Fresh final verification receipt

Final full refresh: `fish -ic 'refresh-config'` exited 0, printed REFRESH COMPLETE. Final independent test batches both exited 0:

- `python3 -B tests/test_codex_notification_sound.py`: 13/13 passed; expected failure-path diagnostics only.
- `xvfb-run -a dbus-run-session -- python3 -B tests/scripts/codex_notification_daemon_check.py`: 1/1 passed, including scoped daemon restart and post-restart sound delivery.
- `basedpyright --level error scripts/executable_codex-notification-sound scripts/executable_codex-notification-activate`: 0 errors, 0 warnings.
- `bash tests/test_st_terminal_workflow.sh`, `bash tests/test_st_terminal_wrapper.sh`, `bash tests/test_refresh_config_function.sh`: all exit 0.
- `python3 -B -m unittest discover -s tests -p test_yt_dl_chezmoi.py`: 1/1 passed.
- Scoped `git diff --check`: exit 0. Installed callback, Dunst config and both executable helpers match their sources; approved Codex snapshot matches live. Status remains disabled.
- Both `postmortem_memory.py check --postmortem` task reports: exit 0, no errors/new hashes/unregistered aliases. Earlier full-corpus coverage failure remains explicitly reported.

The final receipt only updates this plan document; no configuration changed after the final refresh. Live MP3 and genuine Codex UI acceptance remain pending as specified above.

### Activation-frequency clarification

User asked whether activation is required for every Kitty launch. Updated the guide and shared smoke prerequisites: activation is needed once after installation or callback/rule changes; fresh Kitty processes load it automatically, local clip selection persists, and `set` takes effect without restart. Existing pre-install Kitty processes still need a fresh process once. Documentation-only clarification; runtime/config unchanged, so no refresh or repeated runtime tests required. Scoped diff formatting check passed.

### User-selected clip stored in the repository

User explicitly requested `/home/example/linux-config/scripts/can-i-ask-you-a-question.mp3`, superseding the earlier instruction to keep audio outside Git. The MP3 already existed at that exact path and the machine-local setting already selected it. Preserve its bytes rather than recopy or overwrite it. Initial follow-up status captured before writes; no staging/commit/push is authorized.

File verification: 27,046 bytes; SHA-256 `73d0efe60961e22853cb0db0ee6720778c1fbe2baf1542184310ca535f02fc89`. `file` identifies MP3/MPEG layer III, mono, 44.1 kHz, 128 kbps. Add an exact LFS attribute for this one asset, update guide/README/smoke checks/continuation prompt, and retain machine-local JSON plus disabled defaults. `refresh-config` will deploy the same clip to ~/scripts on GUI hosts. Remaining actual Codex UI/audio checks are not inferred from storage/format validation.

Rollback for this follow-up: remove only the new exact `.gitattributes` line and revert the corresponding prose if requested; the MP3 pre-existed this turn and must not be deleted as assistant-created work. Local sound-path JSON remains untouched.

Clip follow-up verification: ffprobe exited 0 and identified a 1.410612-second MP3 audio stream at 44.1 kHz, mono (plus embedded PNG artwork). `git check-attr filter diff merge text -- scripts/can-i-ask-you-a-question.mp3` reports lfs/lfs/lfs/-text. Required refresh exited 0 with REFRESH COMPLETE. Repo bytes retain the original SHA-256, installed ~/scripts copy matches byte-for-byte, and current local setting still points to the requested repo path. Scoped diff formatting check passed. No audio playback, staging or commit was performed; no callback/player behavior changed, so runtime tests were not repeated for this asset/documentation follow-up.

### Authorized session delivery

The user's `$commit-session` request supersedes the earlier no-commit restriction for this conversation's eligible work, including the explicitly requested MP3 and funny-clip research prompt. Branch `main` tracks `origin/main`. Scope helper returned unsafe because nested writes were not recognized; use captured baseline and directly observed edits, with independent read-only hunk review.

Stage full task-owned new files and narrow Dunst/LFS changes. Stage only our README rows, notification smoke section, lesson, two memory findings/references and two reports. Reconstruct mixed staged files from HEAD plus those exact additions; preserve unrelated working bytes. Codex config remains skip-worktree and has additional concurrent/pre-existing settings beyond the approved refresh snapshot; leave it uncommitted. HEAD already enables the required notifications.

The shared smoke checklist was unexpectedly truncated during review. Preserve its current worktree; stage only our independently recovered notification section over HEAD. The living environment incident records the unresolved cause, lookup and scoped workaround. Do not commit the unrelated deletions.

- [x] Review task ownership, scope-helper fallback and companion plan/docs.
- [x] Run fresh focused checks, README gate and scoped incident checks.
- [x] Inspect exact staged diff and LFS pointer; prepare authorized commit.
- [x] Confirm configured upstream and remaining dirty state; ready for commit/push delivery.

Fresh delivery checks: unit suite 13/13 passed; private Dunst suite 1/1 passed (five mocked player calls); basedpyright 0 errors/warnings; README gate pass_no_change. Reconstructed HEAD-plus-session ledger checks passed for both reports with 139 findings, zero changed/unregistered hashes and no errors. Environment report hash refreshed to `9bc612a634334486ba2affd56e7c1eda1e377a2acc3109113d4e1c1f541cb1fd`. The earlier unrelated whole-corpus coverage warning remains outside scope. No live audio or genuine Codex UI acceptance is claimed.

Exact staged scope: 20 files, including only two README rows and our 47-line smoke section, two learning sections/records, the selected 27,046-byte LFS asset, helpers, tests, guide, prompts and this plan. `git diff --cached --check` passed. Pointer OID matches the original MP3 SHA-256; an LFS listing diagnostic used an unsupported positional path and was corrected after installed help inspection. Branch/upstream are `main`/`origin/main` at user@example.invalid:example-user/ai-cli-dotfiles.git`. All unrelated files/hunks and skip-worktree Codex config remain outside the snapshot. Commit/push are the next authorized delivery operations; live audio/Codex smoke checks and unrelated corpus/document issues remain explicitly outside automated acceptance.
