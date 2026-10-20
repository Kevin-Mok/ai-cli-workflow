# tmux drag-to-edge selection and copying

Trace the active terminal, reproduce held-button edge scrolling and released-selection copying, then correct only a demonstrated defect. Verify clipboard contents independently of tmux buffers and preserve all existing sessions.

## Purpose and scope

Run prompts/tmux-drag-scroll-copy.md. Acceptance is one continuous left-button selection extending through multiple screens while held stationary at the pane top, followed by release and Ctrl+Shift+C into the system clipboard. Include wrapped lines, repeat copy after clipboard replacement, native Kitty copy, application mouse forwarding, Escape, emacs and vi. No upgrade, history clearing, session termination, commit or push requested.

## Context and assumptions

Initial status: only untracked prompts/tmux-drag-scroll-copy.md; preserve it. Read the canonical policy, prior plan/report, config/adapter/tests/fixture, applicable feedback and lessons. Current mode is fixed to Default; use this ExecPlan because a Plan Mode switch is unavailable. tmux 3.4 and Kitty 0.49.2. Read-only live process/client inspection establishes local Kitty -> fish -> tmux clients (config and school-2), not SSH nesting. Existing release/User0 bindings are active. Kitty config and adapter match deployed files; tmux differs outside the interaction block (investigate before refresh). Do not infer the user's exact problem window from hostname or these unrelated clients.

Postmortem lookup `tmux scroll copy clipboard drag` matched local-tmux-released-selection-copy-ux and local-tmux-history-mouse-ownership. They apply to ownership, foreground detection, fallback flags, clipboard reseeding and isolated GUI limits. Prior evidence covers wheel navigation and short selections, not held-edge multi-screen selection. Keep the existing bridge unless reproduction proves a defect.

## Checklist

- [x] Capture initial Git state and required context.
- [x] Inspect effective settings and nesting without modifying production sessions.
- [x] Reproduce copy failure with fish -c nesting; establish held-edge drag already works in PTY and isolated Kitty.
- [x] Add six-case routing regression, observe fish-owned group RED, apply minimum group-member correction and observe GREEN.
- [x] Identify tmux3.4 invalid release-event ordering; implement experimentally verified inward-cursor workaround after freezing selection, keeping exact selected bytes.
- [x] Verify multi-screen/wrapped/repeated copy, native/app behavior and emacs/vi regressions on isolated actual GUI.
- [x] Update exact smoke gestures, helper/docs; scoped refresh and guarded direct persistence/reload of machine-excluded tmux bindings verified.
- [x] Reconcile reviewed postmortem knowledge, final evidence and independent review; mark physical desktop acceptance pending.

## Risks and rollback

Preserve production clients, retained history, and user's clipboard on physical desktop; run pointer/clipboard experiments on a separate Xvfb display. Socket reads require approved execution outside the sandbox. Refresh may touch unrelated live config; inspect current helper and dry-run first. Undo only this task's diff if needed, then scoped reload without killing sessions. A passing PTY test does not prove shortcut dispatch or physical pointer routing. Never claim physical acceptance from XTest on Xvfb.

## Verification

Run python3 -B tests/test_tmux_scrolling.py on unique servers; add stationary top-edge multi-screen assertions plus wrapped exact-copy coverage if absent. Run an actual Kitty on Xvfb with repository config/adapter, drag to first pane row with XTest, hold, release, Ctrl+Shift+C and read X11 CLIPBOARD. Compare expected numbered history and wrapped logical lines; replace clipboard and copy again. Reuse scripts/executable_tmux-scrollback-smoke for physical follow-up. Run relevant terminal regressions, parser checks, git diff --check, reviewed-memory check and refresh activation checks if changing config.

## Progress and review notes

2026-10-19: initial unprivileged live socket query denied Operation not permitted; approved read-only query succeeded. This was an execution boundary, not terminal failure. Living incident records it. No production edits yet. Diagnostic subagents map existing paths, inspect official capability evidence and run disposable PTY reproduction.

Live no-UI Kitty inspection establishes fish -c leads the foreground group while tmux is another member. Both loaded copy maps/fallback flags and clipboard permissions are correct. One inspected window has a native selection (priority intentionally preserved). Actual direct-tmux GUI passes stationary edge/multi-screen/wrapped/repeat-copy/Escape. Actual matching fish-wrapped GUI fails copy after successful 60-row drag (expected RED). Six-case unit test independently fails fish-group case then passes after the adapter considers group members. No tmux bindings or new clipboard transport needed. First GUI GREEN attempt used installed old adapter despite source config: relative kitten lookup resolves via Kitty's config directory. Correct harness with explicit source adapter; verify installed adapter after refresh separately.

Plan revised on new evidence: stationary-edge regression finds selection_active0 after real release but viewport continuously advances (51->89); this was absent from earlier short-selection tests. Preserve failing assertion and inspect release/timer before considering a tmux binding change. Source timer rearms only at edge; stop-selection alone does not cancel it. Raw mouse forwarding candidates failed in disposable servers. Installed vi GUI passes exact original wrapped logical-text substring, reseeding, Escape/live input; app Shift-wheel entry and native raw Kitty GUI copy pass. Alt+C synthetic app entry initially raced; use documented Shift-wheel plus modifier release for acceptance. Native window readiness probe corrected to treat missing startup window as pending.

Scoped refresh-config exited0 (/tmp/refresh-config.67rYrZ4S.log), installed adapter/helper bytes match. Apply was constrained to these reviewed targets; broad status included unrelated MIME drift and home copies of repository artifacts. Actual refreshed helper runs reviewed apply and shortcut regeneration, not old live-to-source capture. Preserve all unrelated live settings.

Official source confirms release callback runs with m.valid0 and cmd_mouse_pane rejects it before timer cancellation. Workaround uses supported cursor commands after stop-selection; top/bottom runtime experiments preserve text and viewport in emacs/vi. Guarded bindings implemented; fresh pre-fix RED/current GREEN and final installed GUI pending. This does not repair upstream tmux, and requires an interior row (>2 text rows). Live fake-target routing checks show both original Kitty processes now detect tmux from their fish-owned groups without sending production input. Native raw Kitty GUI copy passes. No restart required for custom-file kitten handler invocation.

## Final verification and handoff

All four edge cases intentionally fail with pre-fix config (top51->56, bottom77/78->72). Current `python3 -m unittest tests.test_tmux_scrolling tests.test_kitty_tmux_copy -v` exits0:26 tests in23.320s (/tmp/tmux-final-tests.log). Two notification tests and both terminal shell regressions also exit0 (/tmp/tmux-broader-tests.log). Python AST parsing, helper --help/--plain emit and whitespace checks pass. Independent review caught tiny-pane cursor parking risk; two defining RED cases then >2-row guards pass, preserving existing behavior where no interior row exists.

Final installed GUI harness /tmp/tmux_gui_final_probe.py emacs and vi app both exit0: stationary drag60/65rows, release viewport stable0.6s and through clipboard reseeding/repeat copy; exact2,107/2,108byte clipboard is contiguous original wrapped logical text. App mouse forwarding, Escape/INPUT hello and native raw Kitty copy pass. This is isolated Xvfb evidence; physical shared-desktop acceptance stays pending. No production history loss or session termination.

Final refresh exit0 (/tmp/refresh-config.tazGZ8Mq.log). .tmux.conf is machine-excluded from chezmoi; an attempted targeted refresh rejected that unmanaged target. Preserve exclusion, refresh managed adapter/helper, then persist only owned release bindings plus comment directly. Exact inverse replacement equals original live bytes (backup /tmp/tmux-drag-live-backup-yez9lufe); scoped source-file reload and complete binding queries pass. Installed adapter/helper equal source. Existing windows need no restart. No commits/push requested. Raw final GUI evidence: /tmp/tmux-final-gui-emacs.log and /tmp/tmux-final-gui-vi-app.log (both exit0).

Atomic scope: adapter foreground-group detection + release-binding workaround + focused tests + README/helper/smoke docs + incident/reviewed learning + this plan. Suggested Conventional Commit: `fix: preserve tmux edge selections and copy from fish launchers`.

Manual plan (no sudo, any cwd): run ~/scripts/tmux-scrollback-smoke; hold left-drag at the first text row inside the pane for multiple screens, release and Ctrl+Shift+C; paste into an editor, including a WRAPPED..END line. Copy different text elsewhere then repeat Ctrl+Shift+C on retained selection; expect original full text and stable viewport. Escape and type hello, then Ctrl+D closes only fixture. Repeat --app-mouse after Shift-wheel entry and modifier release. Repeat with vi mode if used; raw Kitty/native Shift-drag copying stays available. Panes need at least three text rows. Three direct final commands are default fixture, app-mouse fixture and xclip clipboard read.

Paste-ready Cursor prompt: Read plans/tmux-drag-scroll-copy.md and docs/smoke-tests.md tmux section. Complete physical desktop acceptance using the existing disposable fixture; verify stationary held-edge multi-screen drag, release, actual clipboard paste with wrapped lines, replacement/repeated copying, native/app gestures and Escape. Preserve all production sessions/history and unrelated work. Run the26 focused tests if implementation changes, update this plan/incident/reviewed memory, and apply only reviewed targets. Do not replace the bridge, upgrade tmux or commit/push without authorization.

Independent review: no remaining important code findings after tiny-pane guard. Reviewer directly read final source/API, raw26 focused and2 notification results, installed GUI harness/logs, live binding guards and source/installed adapter/helper bytes. Silent shell exit0 is observed by executor, not independently recoverable from its silent logs. Physical desktop acceptance remains the only interaction acceptance gap.

Reviewed learning: report hash43c89ef5553cf9396553b3430993099a6cf10cd3e7725cfdd563e01554417949; findings local-tmux-foreground-group-members (verified_fix/runtime) and local-tmux-edge-release-timer (verified_workaround/runtime). Updated tracked sources.json, artifact-verification.md and repo lesson. Targeted check exits0, errors/missing/new/changed/unregistered aliases all empty. No installed knowledge copy edited. Preserve the initial untracked prompt; no unrelated staging, commit or push.

## Session delivery milestone

2026-10-20: user invoked commit-session, authorizing one scoped commit and origin/main push. Milestone subject: `fix: preserve tmux edge selections and fish launcher copying`. Completed: foreground-group detection, guarded edge-release workaround, fixture, tests, README/smoke instructions, incident and reviewed learning. Physical-desktop acceptance remains pending; isolated runtime verification is complete. Next delivery action: verify candidate privacy, commit and push once; no history rewrite.

Scope helper for session01a154dd-7577-78e2-b965-c8f59a41edb7 returns unsafe because it cannot detect writes/baseline inside orchestrated calls. Direct-write fallback uses the captured initial state (only the pre-existing untracked prompt) and successful edits in this conversation. Include all directly authored tmux implementation/tests/docs, this plan, incident, related lesson and the two tmux finding/report additions. Exclude the initial prompt, unrelated state-security finding, unrelated ledger additions and JSON formatting changes from another session. Publish a neutral `/home/example` report alias in the candidate ledger; preserve the machine-local physical alias in the worktree. No secrets, caches or local runtime logs enter the candidate.

README gate returns pass_no_change. Fresh focused regression and final privacy checks are recorded before commit; previous verified evidence includes26 focused tests, two notification checks, two terminal shell regressions, installed GUI clipboard checks and independent review. Rollback is a forward revert of the focused commit and scoped config reload; retain all sessions/history. Delivery warnings do not waive the privacy gate or active hooks.

Fresh pre-commit verification exits0:26 focused tests in43.485s, two notifications in0.831s and both terminal shell regressions (explicit per-command statuses in /tmp/tmux-commit-tests.log). Targeted reviewed-memory check exits0 with no hash/alias/schema errors; whitespace check passes. Implementation has no blocking issue; physical acceptance remains pending. Eligible milestone is ready for exact staged-diff/privacy review, then the authorized commit and upstream push. Preserve the unrelated ledger/reference work and original prompt.

Exact staged review confirms12 owned paths and only two tmux finding/one report additions in the mixed ledger. Public candidate uses a neutral report alias; unrelated working bytes remain untouched. Shared privacy gate exits0 with exact-candidate PASS; active hooks are preserved for commit. Milestone is complete and verified for isolated terminal interaction, with no implementation blocker. Next delivery step is the authorized commit and origin/main push; physical acceptance remains the documented follow-up.

Milestone1 committed35e9363, subject `fix: preserve tmux edge selections and fish launcher copying`; active privacy hook passed. Exact committed tree and parent match the reviewed candidate, all12 intended paths match, and the index is clean. A broad preservation assertion then stopped before push because unrelated state-security/ledger bytes changed concurrently; this session never edited that reference. Preserve newer bytes, do not restore stale snapshots. Existing reviewed stale-preservation guidance applies; matching short delivery report records no new reusable learning.

Milestone2 subject: `docs: record tmux delivery concurrency check`. Scope: this plan, delivery incident and only its reviewed ledger record. Implementation/tests remain verified and unchanged. No implementation blocker; next action is the final scoped documentation commit, then one normal origin/main push of both session commits. Keep unrelated reference/ledger changes, local aliases and the pre-existing prompt out of scope. Physical desktop acceptance remains pending.
