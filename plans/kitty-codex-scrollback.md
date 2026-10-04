# Configure Kitty for long Codex output

This plan records how to make Kitty's normal windows and Codex sessions use
the same draggable history as the verified fixture, then test and deploy it.

## Purpose and outcome

Make long Codex output easier to navigate using Kitty's native rounded,
draggable scrollbar, Shift+PageUp/PageDown, and a bounded 50,000-line history.
Preserve the existing 0.9 background opacity and pywal integration. Give the
user a reproducible smoke-test entrypoint and a direct documentation location.

## Context and scope

The completed read-only research found installed Kitty 0.49.2 already supports
the requested scrollbar. Its current configuration uses default hidden-until-
scrolled visibility and 2,000 lines of history. Codex 0.160.0 supports
`--no-alt-screen` for terminal-owned scrollback. The user now authorizes
configuration changes and smoke-test updates.

Update the Kitty configuration, the existing i3 Codex launch command if needed
to expose terminal history, focused README/smoke documentation, and a reusable
manual test helper. Record the
[inspection failures](../docs/postmortem/2026-10-04-kitty-scrollbar-inspection.md).
No terminal installation or Git worktree is requested. After verification,
the user explicitly requested `commit-session` to commit and push this work.

## Decisions and assumptions

- Use the settings already parser-validated in the research: 50,000 history
  lines; always-visible scrollbar when history exists; interactive thumb;
  width 0.6, hover width 1.2, radius 0.3, minimum height 2, hitbox expansion
  0.4, handle opacity 0.7, transparent track, hover-track opacity 0.1.
- Keep background opacity 0.9 and map Shift+PageUp/PageDown to page scrolling;
  Ctrl+Shift+End returns to the newest output.
- Use inline Codex for new sessions launched by the repository's i3 shortcut.
  The follow-up also makes inline mode the user-level Codex default so plain
  `codex` and `codex resume` launches receive the same behavior.
  A terminal scrollbar cannot expose tmux-owned pane history; document that
  limitation and test direct Codex separately from tmux.
- Use a runtime configuration probe and existing regression checks rather than
  adding tests that merely repeat these low-impact configuration literals.
- The reusable manual helper needs no sudo and must not launch paid inference,
  alter other terminal sessions, or change configuration.

## Ordered checklist

- [x] Capture initial status and inspect applicable instructions and research.
- [x] Read existing smoke checks, launcher tests, and the refresh implementation.
- [x] Run a pre-change executable probe showing the requested behavior is absent.
- [x] Apply the focused configuration and manual-test/documentation changes.
- [x] Run configuration parsing and relevant existing regression checks.
- [x] Run refresh-config and verify deployed Kitty settings and launcher.
- [x] Record evidence, limitations, rollback, and exact user test location.

## Protected state, risks, and rollback

The initial working tree already contains modified `aliases/key_dirs.tmpl`,
`docs/phone-ssh-public-ip.md`, and `docs/smoke-tests.md`, plus the terminal,
metaprompt, phone-SSH, and VPS prompt/plan/postmortem artifacts from earlier
work. Preserve all those changes. Only the terminal section of the dirty smoke
document is in scope; do not rewrite unrelated sections.

`refresh-config` snapshots live Codex and Git configuration before applying
chezmoi and rebuilding shortcuts. Inspect its behavior and dry-run scope before
execution so unrelated local edits are not accidentally overwritten. Any
unexpected refresh failure gets immediate evidence in the incident record.

Rollback restores only this task's Kitty and Codex-launcher settings and applies
those targets; preserve the user's original dirty changes. Close the standalone
manual test window to stop its fixture output. Larger scrollback allocates more
memory as it fills and does not recover output already discarded.

## Verification and handoff

Before editing, load the current Kitty file through its installed parser and
check the required scrollbar/history behavior; expect a deliberate failure.
After editing, parse the tracked and live files, confirm finalized paging
actions, and run the existing terminal workflow, wrapper, pywal, and Codex
launcher regressions that apply. Check Python syntax for the manual helper and
render/check the i3 configuration if its launcher changes.

The smoke documentation must contain the exact helper invocation plus grouped
Action/Expected checks for dragging early/middle/latest history, page keys,
return-to-bottom, stable viewing during streaming, wrapped text, selection,
resizing, transparency, and a fresh inline Codex session. Actual mouse/visual
acceptance remains user verification unless it can be observed directly.

Keep this plan and its exact evidence with related changes in any future commit.
Suggested subject: `feat: improve Kitty scrolling for Codex output`.

## Progress and review notes

- 2026-10-04: Status captured before the first write. The user explicitly
  authorized applying the researched settings and requested a test location.
- The initial search used the wrong refresh-helper path; the incident record
  documents the failure and the correct fish-function location.
- The pre-change native-parser probe deliberately returned 1 for shallow
  history, a scrollbar hidden until scrolling, and missing Shift+Page mappings.
  The same behavior probe now returns 0, including preserved 0.9 opacity.
- Corrected a pre-existing test expectation for st's `-A1` flag on Kitty's
  launcher. An exact-line assertion now checks the existing intended launcher;
  the launcher itself was not changed to satisfy this obsolete test.
- Passed (exit 0): `bash tests/test_st_terminal_workflow.sh`,
  `bash tests/test_st_terminal_wrapper.sh`, `bash tests/test_apply_pywal_theme.sh`,
  `./scripts/executable_readme-recruiter-sync` (`pass_no_change`), and
  `git diff --check`.
- Parsed the Python fixture, exercised `--help`, and emitted three history plus
  two stream records with `--interval 0`. Confirmed order, absence of terminal
  screen-control escapes, and rejection of invalid counts/nonfinite intervals.
- Rendered i3 with `chezmoi execute-template` and checked with `i3 -C -c`:
  exit 0 with existing wheel-command deprecation warnings. The scoped
  chezmoi dry-run for Kitty, i3, and the fixture also returned 0.
- Independent refresh audit confirmed no hook collisions, no source/live Git
  difference, and a valid Codex snapshot. The refresh will capture existing
  live changes to `model`, `model_reasoning_effort`, and
  `plan_mode_reasoning_effort`; it also deploys pending documentation.
  Backups are in `/tmp/kitty-scrollback-baseline-kceztcrf`.
- `refresh-config` completed with exit 0. Full log:
  `/tmp/refresh-config-20261004-161355-543609.log`. Installed Kitty, i3,
  and fixture files matched their source/rendered candidate. Unrelated alias,
  phone-SSH, Git config, and smoke-document sections matched baseline bytes.
  The Codex snapshot changed only the three audited keys and matched live.
- `i3-msg reload` returned success; `kitty @ --to unix:/tmp/kitty-PID
  --use-password never load-config` returned 0 for all 12 active, owned Kitty
  instances. Existing process-specific overrides were retained.
- Independent review found one fixture edge case: at fewer than 40 columns,
  wrapping 10,000 records can exhaust 50,000 rows. The helper now prompts for
  a wider window before generating history, and smoke documentation records
  the width requirement. No other implementation issue was reported.
- An isolated pseudoterminal reproduced the pre-guard helper emitting at 24
  columns. The revised helper paused, resumed after resizing to 80 columns,
  emitted history and streaming records in order, and closed cleanly (exit 0).
- Corrected the existing README refresh description to include its local-
  conflict adoption/retry behavior; the function itself was not changed.
- Final refresh after the width safeguard returned 0; log:
  `/tmp/refresh-config-20261004-161651-548381.log`. The deployed helper,
  Kitty configuration, and smoke guide match source. The live parser printed
  `50000 always True 0.9`; the installed helper's help and short fixture,
  all three terminal regressions, README gate, and diff check returned 0.
  No commit or push was performed.

## Follow-up: normal Codex sessions

The user confirmed the fixture works and requested the same behavior in actual
Kitty use. The helper passes no config overrides: tracked and live Kitty files
already match its working settings. The missing route is ordinary Codex launch,
whose `tui.alternate_screen` is unset. Official [TUI configuration guidance](https://learn.chatgpt.com/docs/config-file/config-advanced#tui-options)
documents `never` as the persistent native-scrollback setting.

The i3 shortcut also points to fnm's stale default installation (Codex 0.114.0),
which rejects the existing `model_reasoning_effort = "max"`. The normal fish
PATH selects the v22.15.0 installation with Codex 0.160.0, which accepts the
current config plus the `never` override. Use that verified absolute Node and
Codex entrypoint pair for Super+C without changing model preferences.

- [x] Capture current status; verify the fixture has no Kitty overrides and
  confirm the missing normal-launch default.
- [x] Verify the persistent setting with official docs and the installed CLI;
  isolate and explain the old-launcher validation failure.
- [x] Set the existing Codex TUI table's alternate-screen default to never,
  correct the i3 runtime path, and clarify README/manual smoke checks.
- [x] Deploy the exact Codex target before refresh-config so its live-to-source
  snapshot preserves this authorized source edit; run refresh and reload i3.
- [x] Verify unchanged Kitty settings, deployed Codex TUI value, actual launcher
  config parsing, existing regressions, and the final diff.

Both Codex files were byte-identical before this follow-up; exact backups are
in `/tmp/kitty-codex-default-_d0o3ql5`. Before the targeted apply, compare live
against that backup again to detect concurrent edits. Preserve all existing
dirty files, including the newly edited canonical instructions and feedback log.
Rollback removes only the newly added TUI setting and reverses this follow-up's
launcher path correction, then reapplies those targets. Running Codex sessions
must restart or resume to read the new default; discarded output is not restored.

Before deployment, TOML comparison proved that only `tui.alternate_screen` was
added and the live config still matched its backup. The exact Node/CLI pair
from the corrected shortcut reported 0.160.0 and parsed the full current config
with `--no-alt-screen -c 'tui.alternate_screen="never"' features list` (exit 0).
The rendered i3 config, three terminal regressions, README gate, and diff check
also returned 0. No model inference was requested.

The targeted apply and required refresh completed with exit 0; full log:
`/tmp/refresh-config-20261004-162924-569540.log`. Source/live Codex and Kitty
files match, and the rendered i3 file matches its validated candidate. i3
reload returned success. The corrected Node/CLI pair ran `features list`
without any scrolling override and returned 0 with the deployed config.
The native Kitty probe still reports `50000 always True 0.9`. The user-accepted
fixture appearance was not changed; restart/resume is required for old Codex
processes. The revised manual procedure covers both shell and Super+C routes.

## Session delivery scope

The session-scope helper reported `unsafe` because it did not recognize the
successful orchestrated writes in thread
`01a10863-b8f2-77c1-a9ff-5855cce6a85a`. Use direct-write evidence: the Kitty/i3
changes, fixture, focused test correction, terminal README/smoke hunks, lessons,
this plan and inspection postmortem, plus the two terminal prompts and their
authoring plan/postmortem. Successful patches in the same session log establish
the earlier prompt artifacts; their current bytes match the replayed patches.

The Codex file has Git's skip-worktree bit set. Its live/source scrolling
setting is present, while HEAD lacks it. Stage only the added alternate-screen
setting/comment against HEAD and retain the skip-worktree flag and unrelated
local Codex contents. Do not mistake hidden changes for committed changes.

Keep unrelated README introduction/instruction wording, smoke-document
overview/phone-SSH/procedural checks, alias/phone files, standing-instruction
and feedback changes, other documentation/skills, and other prompts/plans out
of this commit. Stage only the inspected terminal hunks in mixed files. Fresh
terminal regressions, fixture emission, README gate, and whitespace checks
passed before staging. The commit uses the configured `main` → `origin/main`
upstream and includes its matching plans and records.

The implementation was committed as `c1326da`. Automatic review initially
blocked the push pending destination trust evidence. Read-only GitHub API
checks establish that authenticated `example-user` owns the private
`example-user/ai-cli-dotfiles` repository with admin/push permission. Record the
[push review](../docs/postmortem/2026-10-04-kitty-session-push-review.md) in the
follow-up documentation commit before the normal push of the verified series.

## User test location and follow-up handoff

Run `/home/example/scripts/kitty-scrollback-smoke` from any terminal; no sudo is
needed. Follow [Kitty and Codex scrolling](../docs/smoke-tests.md#kitty-and-codex-scrolling).
The helper uses the deployed configuration in a fresh Kitty window, and the
user has confirmed it works. Actual Codex acceptance starts a fresh session
from the shell or Super+C; live Codex scrolling still needs that separate check.

For a repeatable native configuration inspection after deployment:

```sh
kitty +runpy 'from kitty.config import load_config; o = load_config("/home/example/.config/kitty/kitty.conf"); print(o.scrollback_lines, o.scrollbar, o.scrollbar_interactive, o.background_opacity)'
/home/example/scripts/kitty-scrollback-smoke --help
bash tests/test_st_terminal_workflow.sh
bash tests/test_st_terminal_wrapper.sh
bash tests/test_apply_pywal_theme.sh
./scripts/executable_readme-recruiter-sync
git diff --check
```

Expected config output: `50000 always True 0.9`; each command exits 0.
The full manual sequence covers dragging, modified page keys, return to live
output, selection, resize, transparency, and streaming; it is not replaced by
the parser probe. Earlier discarded lines and tmux-owned history remain
outside this terminal-history change.

Paste-ready Cursor follow-up if manual acceptance finds a problem:

> Read `plans/kitty-codex-scrollback.md` and the Kitty/Codex section of
> `docs/smoke-tests.md`. Reproduce the reported scrolling problem with
> `scripts/executable_kitty-scrollback-smoke` in a fresh Kitty window, then with
> a fresh inline Codex session when relevant. Preserve unrelated dirty work and
> opacity 0.9; change only the failing behavior. Run the listed checks, update
> this plan and smoke procedure, and run the required refresh-config. Do not
> create a worktree, commit, or push without an explicit request.
