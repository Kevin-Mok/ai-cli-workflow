# Open the saved CTO chat directly

> Superseded on 2026-11-11: Kevin chose native Firstmate with Codex. The wrapper,
> custom prompts and wrapper tests have been retired. This plan retains historical
> evidence, not current launch or recovery instructions. See
> [native usage](../docs/firstmate.md) and [retirement plan](retire-firstmate-cto.md).

Give the operator one command to reopen the saved CTO conversation when attaching
only shows fish and Fleet. Preserve existing windows, workers and conversation history.

## Context and decisions

Live metadata on 2026-11-11 shows cto-master ($5) has fish and fleet, no cto.
The launcher only attaches; start refuses a missing cto window. Codex resume help
confirms its default picker filters by working directory. Use that supported picker
in the private control directory; never guess a thread or resend the startup brief.
Explicit chat opens the picker; --no-attach prepares it without changing client focus.
Existing cto windows are selected, never overwritten. No hook approval changes.

## Scope and protected work

Modify the launcher, its existing tests, guide and smoke check. All these source
artifacts and the original setup plan already have uncommitted work; preserve it.
Initial git status captured before writes. No commits or pushes requested.

## Checklist

- [x] Inspect launcher, docs, saved incident evidence and live pane metadata.
- [x] Observe RED for chat recovery, repeat invocation, attachment and ownership.
- [x] Implement chat using Codex resume picker, preserving existing shell and Fleet.
- [x] Run focused suite and isolated real tmux check; update operator documentation.
- [x] Attempt required refresh; activate only reviewed launcher and verify live picker.

## Risks and rollback

Picker selection remains an operator action. An existing cto window is preserved;
its name alone does not establish a running supervisor. No workers or goals are
resumed automatically. Roll back only this session's additions; preserve older work.

## Verification and review

Pending RED/GREEN and runtime checks. Manual: chat opens a picker in control cwd;
choose the saved CTO with Enter, type at Codex input; repeat chat selects that window.
Fleet continues. Suggested commit: fix(firstmate): reopen saved CTO chat directly.
Cursor handoff: Read this plan and docs/firstmate-cto.md; verify recovery without
resending prompts or altering worker supervision. Run tests/test_firstmate_cto.py.

RED: 3 targeted tests, 2 expected invalid-choice failures, exit 1. Foreign refusal
test strengthened to require ownership error, not just exit 2.

GREEN: FIRSTMATE_CTO_REAL_TMUX_TEST=1 python3 -B tests/test_firstmate_cto.py,
26 passed, exit 0 (11.527s); includes real isolated missing-window recovery twice.
Live installed chat --no-attach and repeat exited 0; capture showed one cwd-filtered
saved conversation, Drawing-night approval blocked. Windows: 0 fish, 1 fleet, 2 cto.
Installed bytes match source. git diff --check passed. Help exposes chat/--no-attach.
Full refresh attempted, blocked by existing duplicate MIME source mapping; exact
reviewed launcher installed after comparing older target and saving /tmp backup.
The operator still selects the conversation with Enter; input, hook trust and
active supervision after selection are unverified. No goal resumed or worker touched.
README, guide and smoke checks updated. No commit/push. Automated checks are scoped
to this launcher, not the repository's unrelated tools. Actual Codex TUI wrapped-copy
and syntax-color rendering were not tested; no renderer setting changed.

## Native-role clarification follow-up

User asked how to instill the CTO concept and use native Firstmate. Read the
installed README, AGENTS startup contract, configuration preference schema and
Codex supervision protocol; a focused read-only mapper independently confirmed
these. The primary already owns cross-project coordination. Guide and smoke
checks now distinguish native primary CTO preferences from optional outer chat.
No live setup, preference changes, worker dispatch or run resume performed.
Manual adoption check: primary confirms its actual home and saved role without
starting work. Documentation checks only; earlier 26 runtime tests are from the
chat-recovery turn, not newly rerun for this prose clarification.
