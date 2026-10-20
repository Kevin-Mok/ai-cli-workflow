# Enable keycode 108 for Alt workspace switching

Verify the active X11 key and i3 shortcuts, make the smallest persistent mapping
change if needed, and check switching through the running desktop.

## Outcome, context, and scope

Keycode 108 should work as Alt when held with the existing workspace keys.
The tracked i3 config uses `Mod1` and Alt+1–0 for workspaces 1–10. The active
X11 map currently reports `108 = Alt_R Meta_R Alt_R Meta_R` and includes
`Alt_R (0x6c)` in Mod1. Establish actual switching before choosing a change.
Relevant files are `dot_Xmodmap`, the startup callers in `dot_xinitrc.tmpl` and
`scripts/executable_ubuntu-start`, and the workspace bindings in
`dot_config/i3/config.tmpl`. Keep existing bindings and other keyboard mappings.

## Assumptions and decisions

- “Like Alt” means holding keycode 108 with the same workspace keys as left Alt.
- This is a mechanical keyboard task; no private personal context is needed.
- Do not add duplicate i3 shortcuts or a single-key workspace action.
- If the existing live mapping passes, avoid an unnecessary config rewrite.
- Default mode is active; use this written plan without changing collaboration mode.

## Checklist

- [x] Capture initial status and inspect relevant instructions and keyboard paths.
- [x] Inspect live key/modifier state through scoped approved desktop access.
- [x] Reproduce workspace switching with raw keycode 108 and compare left Alt.
- [x] Determine correction need: existing live mapping passes; no config change required.
- [x] Update the shared smoke check and relevant public documentation.
- [x] Record runtime evidence and limitations; reviewed incident learning updated.
- [x] Run final targeted ledger coverage and diff checks (both exit 0).

## Risks and protected state

Initial dirty files include README, smoke tests, i3 config, postmortem-memory
guidance/ledger, Redshift plan/script and untracked reports/plans/prompts.
Preserve all prior hunks. The follow-up commit request covers only this session. Live switching must
restore previously visible workspaces and focus and release every synthetic
modifier in a finally block. Do not move windows, stop apps, or replace AltGr
behavior without establishing the need. A mapping change can be rolled back
by removing only this task's added lines, refreshing config, and reapplying
the original map. Any tracked config change requires `refresh-config`.

## Verification

- Inspect `xmodmap -pm` and keycodes 64/108 before any change.
- Use XTest raw key events for 108 plus the number-row key, compare i3's focused
  workspace to the configured destination, and restore original focus.
- Compare left Alt with right Alt; physical key use remains a manual check.
- Add an Action/Expected pair in `docs/smoke-tests.md` for physical right-Alt
  switching using the ordinary number row.
- No new unit tests for a trivial mapping; use actual X11/i3 behavior.

## Evidence and review

- Initial `git status --short` captured before the first edit.
- Restricted X11 inspection failed; approved reads exit 0 and expose the live
  mapping. See `docs/postmortem/2026-10-20-keycode-108-x11-access.md`.
- Live i3 is in default binding mode. Workspace 3 was initially focused.
- Final `python3 /tmp/keycode-108-workspace-check.py` exited 0: both keycodes
  64 and 108 plus 1/2/0 emitted Mod1 bindings and focused workspaces 1/2/10.
  Visible workspaces 10/3/1 and focus 3 were restored. No keyboard config changed,
  so `refresh-config` is not needed for a keyboard deployment.
- README now identifies Right Alt/keycode 108 and its existing 1–0 shortcuts;
  smoke tests document physical-key verification. README scope review:
  `update_in_same_change`, with the shortcut clarification included; existing
  recruiter-first hierarchy was preserved.
- Probe API/Unicode failures were corrected and recorded in the postmortem,
  tracked memory and local engineering lessons. Physical keypress/firmware
  acceptance and a fresh-login check remain manual; no restart was performed.
- Follow-up `$commit-session` authorizes one scoped commit and push to
  `origin/main`. Scope helper reports unsafe because it detects no writing
  actions in this tool transport; use the directly observed seven-file scope.
  Preserve unrelated reference sections and ledger entries, including the
  pre-existing staged ledger changes, using an isolated candidate index.
- Commit milestone: `docs(i3): clarify right Alt workspace shortcuts`.
  Completed: live six-case probe, README/smoke documentation and reviewed
  incident learning. Verified: exact live binding/focus events and restored
  layout; README gate, targeted ledger check, candidate ledger/schema/hash
  validation, staged diff review and exact-candidate privacy check pass.
  Remaining: scoped commit and upstream push. No task blocker identified.
  Physical keyboard/firmware and fresh-login checks remain manual.
- Public commit uses the existing `/home/example` placeholder for the new report
  alias. The actual machine lookup alias remains in local unstaged ledger data;
  exact physical-path lookup is local, while the public record retains the same
  verified report hash and reciprocal finding link. No private policy exception
  or hook bypass is used.

## Reusable verification and handoff

From any directory in the active X11 desktop, without sudo:
`xmodmap -pm` shows Alt_R (0x6c) in mod1; `xev -event keyboard` reports keycode
108/Alt_R when the physical Right Alt key is pressed; after Right Alt+2,
`i3-msg -t get_workspaces` shows workspace 2 focused. The physical smoke check
also compares Left Alt and Right Alt with number-row 1/2/0 and restores focus.

Cursor handoff prompt: “Read plans/keycode-108-workspaces.md. The live X11/i3
probe passed for keycode 108 and Left Alt with 1/2/0; no remap is required.
Preserve concurrent dirty work. If physical behavior differs, capture xev events
from that keyboard before changing dot_Xmodmap. Use literal UTF-8 workspace
names for i3 command text and restore the visible layout.”

Final checks: targeted postmortem coverage reports zero errors/missing sources/unregistered aliases; `git diff --check` exits 0. No live shortcuts were re-run after the successful six-case probe.
