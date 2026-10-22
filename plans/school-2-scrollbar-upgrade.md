# Prepare school-2 scrollbar upgrade

Prepare and verify a separate scrollbar-capable tmux while keeping the current server running.

## Scope and decisions

Live server/client are 3.4; school-2 has 13 windows and shares its server with five sessions. User explicitly requested preparation only. Do not restart, kill, migrate, replace /usr/bin/tmux, or redirect current launchers. Ubuntu package candidate is still 3.4. Prefer a versioned user-local binary and a separate preview socket.

## Checklist

- [x] Capture dirty state, inspect prior evidence and confirm live 3.4.
- [x] Resolve restart decision: preserve all current sessions.
- [x] Prepare newer upstream binary with an isolated configuration.
- [x] Verify version, scrollbar settings and history on separate socket; preserve production session IDs.
- [x] Record reproducible activation/rollback and reviewed incident evidence.

## Risks and protected state

README, smoke tests, sources.json, tasks/lessons.md and numerous unrelated files were dirty at entry. Preserve their existing changes. No commits or pushes requested. New binary must remain versioned so current clients retain protocol compatibility. Existing panes cannot migrate into a replacement server without ending their processes. Remove only versioned prepared artifacts to roll back.

## Verification

Baseline: live default server reports 3.4 and lacks native pane-scrollbars. New binary must report >=3.6; separate disposable server must expose pane-scrollbars on and retain numbered history. Compare production session IDs before/after. Physical mouse acceptance remains a separate preview check. Use read-only host access where sandbox prevents socket queries.

## Progress and review

2026-10-22: initial diagnosis confirmed; no behavior/config changes. Incident: docs/postmortem/2026-10-22-school-2-scrollbar-preparation.md.

## Prepared outcome and verification evidence

- Official upstream release 3.8 downloaded using gh-axi. Tarball SHA-256: e79c699c7e949dccd0a4a125e17b8d1261e311b16979dbc8eb34542f3966d82e. Built with downloaded/extracted Ubuntu headers and bison under /tmp/school-2-tmux-3.8-build; no package installation. Versioned install at ~/.local/opt/tmux-3.8/bin/tmux, matching man page alongside it. Dynamic dependencies resolve to existing host runtime libraries. Build output remains outside Git.
- Reused scripts/executable_tmux-scrollback-smoke: --scrollbar pins the prepared binary and sets pane-scrollbars on only on its unique disposable socket. Installed the exact helper at ~/scripts/tmux-scrollback-smoke. Default mode remains tmux 3.4. No tracked configuration changed, so no broad refresh was run against unrelated dirty configuration.
- RED: python3 -B tests/test_tmux_scrollbar_preview.py exited 1 with two argparse errors for absent --scrollbar. GREEN: both preview tests passed. Combined python3 -B -m unittest tests.test_tmux_scrollbar_preview tests.test_tmux_scrolling passed 24/24 on /usr/bin/tmux 3.4 (exit 0). With PATH selecting 3.8 it passed 20/24 (exit 1); stationary top-edge selection and bottom-edge movement failed in emacs and vi. This compatibility difference remains unresolved and blocks treating 3.8 as a drop-in production replacement.
- Real PTY scrollbar checks (temporary /tmp/school-2-tmux-3.8-build/check_scrollbar.py): shell history_size 3579, drag scroll_position 3578; mouse-aware app history_size 3581, drag scroll_position 3580. Both exited 0, entered history mode through actual scrollbar SGR mouse events, returned to live mode and accepted INPUT hello. Ordinary app wheel remained forwarded. These are real attached-client checks, not physical desktop acceptance.
- Production session ID/name/window-count snapshots before and after are identical (diff exit 0); school-2 remains PID 28315, version 3.4, session $2. All six original sessions preserved.
- Documentation: README, docs/smoke-tests.md prepared-preview section, this plan and the living incident. No commit or push requested/performed.

## Manual verification and activation boundary

Run ~/scripts/tmux-scrollback-smoke --scrollbar in a desktop terminal. Drag the right pane scrollbar to earlier records, return downward, press Escape, type hello and Enter, then Ctrl+D at empty input. Repeat with --app-mouse. Only the disposable preview closes. Physical desktop acceptance remains pending.

Existing school-2 cannot acquire this feature in-place on its 3.4 server. Future work must resolve the four edge-selection checks, obtain authorization for migration, and account for all six shared-server sessions. Do not replace /usr/bin/tmux, current client PATH or tmux-attach. A new server cannot inherit already-running pane processes automatically.

Rollback: remove only the separately prepared ~/.local/opt/tmux-3.8 installation if no preview is running, and revert only this task's --scrollbar helper additions. Do not touch default sockets, running sessions or existing config.

Atomic plan: diagnose -> versioned build -> isolated preview -> compatibility checks -> preserve production -> document limits. Suggested commit: feat(tmux): prepare isolated native scrollbar preview. Cursor follow-up prompt: Read plans/school-2-scrollbar-upgrade.md; investigate the four tmux 3.8 edge-selection compatibility failures using disposable servers, preserve all live sessions, and do not migrate without explicit authorization.

Final live read: prepared binary reports 3.8; production remains PID 28315 / tmux 3.4. The school-2 count is now 14 windows (initially 13); concurrent activity occurred after the identical before/after preparation snapshots. This task issued no production new/kill/respawn commands. Final deployment cmp and git diff --check passed. Targeted postmortem-memory check passed with no errors.

## Follow-up: Kitty launch compatibility

User reported real preview config parse failure for --allow-fallback under Kitty 0.32.2. Preserve the modern copy mapping and choose the existing user-local Kitty 0.49.2 in the helper. Scope: helper, defining test, smoke docs and this incident/plan; no production tmux or Kitty config edits.

- [x] Reproduce parser compatibility on installed old and modern Kitty.
- [x] Observe RED for legacy-PATH launcher selection, then prefer user-local Kitty.
- [x] Verify parser, helper launch, regression and deployed bytes; update reviewed knowledge.

Follow-up completed: helper prefers user-local Kitty and uses versioned tmux child PATH for plugins. Legacy parser reproduces the exact error; modern parser accepts full config. Two independent launcher RED assertions observed, then both tests GREEN. Real Xvfb launch with PATH=/usr/bin:/bin displays numbered history, scrollbar and exact INPUT hello without parse/TPM errors; exits 0. Installed helper bytes match source. Full tmux suites not repeated; original four edge-selection differences remain unresolved. Updated smoke guide, living postmortem, reviewed knowledge and tasks/lessons.md. No config change, refresh, commit or push. Suggested follow-up commit: fix(tmux): use compatible preview executables. Cursor prompt: Review the Kitty executable and child PATH regression coverage in tests/test_tmux_scrollbar_preview.py; preserve the existing session migration boundary.

## Delivery milestone 1: feat(tmux): add isolated native scrollbar preview

Commit-session authorized on 2026-10-22. Scope helper reported unsafe because it could not recognize successful tool writes; use directly observed session writes and the initial dirty baseline. Include the helper, defining tests, this plan, the incident, scoped README/smoke/lessons additions and exactly the two session findings plus one report in the shared ledger. Preserve all unrelated ledger changes and other dirty files. No binaries, extracted dependencies, screenshots or /tmp build outputs enter Git.

Fresh delivery checks: two preview tests pass, ASCII help passes, targeted postmortem-memory check has zero errors and root README gate reports pass_no_change. Earlier GUI verification proved clean modern-Kitty startup under system PATH and INPUT hello. Known tmux 3.8 edge-selection differences remain outside this preparation milestone. Review and rollback are documented above; no production migration is included. Next: scoped privacy gate, commit and push to origin/main.

Delivery review: concurrent audio-notification README/smoke hunks are excluded using an isolated candidate index. Shared ledger staging contains only the two session findings and report, with the public /home/example alias; all unrelated records and physical working aliases are preserved outside the candidate. Exact-candidate privacy retry passed, and the targeted live-knowledge check passed. Milestone scope is nine files; commit/push result will be reported with the resulting SHA in the handoff. Remaining work: physical acceptance and resolving the four 3.8 edge-selection differences before any separately authorized migration.
