# Colorful workspace icons

Replace workspace glyphs with color emoji inspired by their existing meanings; preserve keyboard shortcuts, windows, outputs and focus.

## Scope and assumptions

Change only active `$ws1`–`$ws13` definitions in `dot_config/i3/config.tmpl`; keep numeric prefixes, `$wsN` references, bindings, assignments, fonts and workspaces 14/15. Use 💻 for terminals, 🌐 browser, 🧰 misc, 🎥 video, 💬 chat, 📤 upload, 📚 journal, 📝 editing, 🎵 music, 🖥️ server and 🎮 games. Noto Color Emoji is already installed. Installed config is unmanaged and private; only guarded exact label substitutions there are authorized. Use compact labels and native minimum widths; rename live workspaces before reloading their new assignment rules. Commit/push authorization is recorded below.

## Protected state and risks

Initial git status captured: many unrelated dirty files, including README/smoke docs and i3blocks changes. Preserve all existing hunks. Source i3 config initially clean. Installed config is newer and differs privately; keep all non-label bytes, do not import private config. Emoji width can reduce status space; existing renderer measures actual workspace labels. Rollback only new label substitutions and rename back using private `/tmp/workspace-icons` baseline. No window/focus changes for validation on active desktop.

## Checklist

- [x] Map labels/callers and capture initial source, installed, runtime/workspace/tree state.
- [x] Add defining emoji/shortcut smoke check, observe expected RED.
- [x] Substitute labels, update README/smoke docs and verify GREEN.
- [x] Exercise real keys on isolated Xvfb display; run focused existing regression checks.
- [x] Run refresh-config, validate guarded installed candidate, activate once and verify workspace/window/focus identity.
- [x] Review final diff and record evidence/limits.

## Verification and review

Run `python3 scripts/smoke_workspace_icons.py`, installed-path and `--live` modes. Existing Redshift checker verifies overlapping shortcuts. An isolated Xvfb i3 instance exercises Alt digits, Ctrl+Alt digits and Alt+Shift digits using actual config bindings. Compare application XIDs by workspace number separately from restarted dock windows; compare workspace IDs/output/visibility/focus around final activation. Capture bar-only screenshot to verify native emoji. Physical keyboard firmware remains manual.

Plan Mode is unavailable in current active mode; use this ExecPlan. Cursor prompt: Follow this plan, preserve pre-existing dirty work, change only workspace labels, retain every keyboard binding, and complete isolated/runtime checks. Suggested commit: `style(i3): use colorful workspace emoji`.

## Compact refinement

User requested narrower workspace buttons after viewing the live laptop emoji. Remove spaces between number/icon and trailing padding from all 13 named workspaces; retain numeric prefix and all binding text. Defining compact checker observed RED for all old padded labels. Rename live names before reloading so loaded old output-assignment names cannot match new names and relocate workspaces. The first activation used reverse order and the output assertion caught relocation; review output restoration before final handoff.

## Final padding refinement

User requested about 15px padding around the icon. All narrow Unicode spaces measure as a full 56px cell in the current mono font, so retain compact names and set native per-bar `workspace_min_width` (144 logical px at 50pt, 95 at 30pt). At current 135 DPI, one-digit text widths are 173/104px; minimum widths are 202/134px, approximately 15px per side around the number/icon group. Wider names grow naturally. Teach the existing 4K width calculation to respect the native minimum, with defining RED test (missing width calculation helper) and GREEN regression. Preserve unrelated concurrent 4K edits.

## Final evidence and delivery

RED: workspace checker rejected all 13 monochrome labels; compact refinement rejected padded labels; minimum-width regression failed before its helper existed. GREEN: final workspace checker and Redshift checker passed source/installed/running configs. Isolated Xvfb exercised 27 actual Alt digit, Super+1/F11 and Ctrl+Alt/Alt+Shift move combinations, exit 0. Fresh layout suite 16/16 and scheduler 1/1 passed; voice binding check passed. All installed binding lines remained byte-identical. Native padding is 144/95 logical pixels; final large-bar screenshot is 202px wide for a 173px one-digit label, about 15px each side. Config refresh and syntax check exit 0; legacy wheel warnings remain. Final padding reload preserved workspace IDs, monitors, visibility and focus; deployed layout helper equals source. git diff --check exit 0.

Unexpected diagnostic/runtime boundaries and the stale desktop-label test are recorded in `docs/postmortem/2026-10-29-workspace-icons-activation.md`. The strict window-set comparison included restarted i3bars: follow-up retained all 32 original application windows on their original numbered workspaces. Earlier output reassignment was restored with an isolated-tested criterion move, retaining the then-visible workspaces/focus. Other concurrent edits to i3 status commands/layout source are preserved and outside this task.

Manual acceptance: inspect each monitor's colored icons and compact side padding; physically press normal workspace/select/move keys with a disposable window. Physical firmware and whole-repo tests are unverified. Current padding scales with font/DPI and native minimum width applies to the number/icon group; wider labels expand naturally. Rollback only this task's icon/min-width/measurement hunks, then refresh and rename before reload. No commit or push performed.

## Session shipping milestone

User authorized `commit-session`. Scope session: `01a189c3-ab57-7382-97b4-8c5f923cc820`; helper returned unsafe because wrapped writes were not detected. The initial git status and directly observed edits establish the safe fallback: only this session's label/minimum-width hunks, workspace width helper/regression, new workspace smoke checker, matching README/smoke additions, this plan, and activation report with its exact ledger/reference additions. Exclude concurrent status-command changes, prior icon/media/Redshift work, and all other dirty files. Build the commit candidate from HEAD plus those exact hunks; test that candidate separately so uncommitted prerequisites cannot conceal a dependency. README gate passed `pass_no_change` on the working README.

Milestone subject: `style(i3): add compact colorful workspace icons`. Target: `main` to `origin/main`, one normal push after privacy gate and commit. Completed: workspace visuals/padding and unchanged shortcuts, matching docs/plan and incident learning. Remaining: candidate-specific checks, commit and push verification. Physical-key acceptance remains manual; no implementation blockers. Preserve all unrelated worktree bytes and index entries. Rollback is an inverse follow-up commit, never history rewriting.

Candidate-specific verification completed: HEAD plus only session hunks passed 13 layout tests, one scheduler test, workspace-label checker and Redshift shortcut checker, all exit 0. Both working README and isolated-candidate README gates returned `pass_no_change`. The candidate excludes prior i3blocks/CLI changes and simultaneous status-command changes. No implementation remains; the only delivery steps are exact staged review, privacy-gated commit and normal push. Prior live checks remain the runtime evidence; no disruptive desktop retest is needed for staging-only work.
