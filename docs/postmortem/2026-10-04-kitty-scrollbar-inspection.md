# Kitty scrollbar inspection failures

- Date: 2026-10-04.
- Symptom: During read-only research, a diagnostic executed through
  `kitty +runpy` failed with `NameError: name 'representation' is not defined`.
  At implementation startup, a search also named the nonexistent
  `scripts/executable_refresh-config` path and reported an `rg` file error.
- Impact: Two inspection steps needed correction. Neither failure changed
  terminal settings, repository contents, or running sessions.
- Evidence: Replacing the diagnostic generator expression with an explicit
  loop exited 0 and showed the finalized Shift+PageUp/PageDown and
  Ctrl+Shift+End actions. Repository references identify the actual refresh
  helper as `dot_config/fish/functions/refresh-config.fish`.
- Root cause: The diagnostic assumed ordinary top-level Python scope inside
  Kitty's embedded execution context. The search assumed the refresh helper
  was a script instead of locating the documented fish function first.
- Resolution: Use the corrected explicit-loop probe and inspect the actual
  fish function before refreshing configuration.
- Current status: Resolved. Research and configuration deployment are complete.
  These were diagnostic failures and a stale regression, not Kitty runtime
  defects.
- Verification: The corrected keymap probe and new settings parse exited 0.
  Refresh-function inspection and target dry-run passed. The required refresh
  returned 0, deployed targets matched source, i3 reloaded successfully, and
  all 12 active Kitty instances accepted their configuration reload.
- Baseline regression finding: Before any terminal implementation edit,
  `bash tests/test_st_terminal_workflow.sh` exited 1 because it expects
  `bindsym Control+Shift+Return exec $term -A1`, while the existing Kitty
  launcher has no `-A1` flag. The terminal-wrapper and pywal checks both passed.
  History traces the stale expectation to the earlier default-terminal switch.
  Corrected it to require the exact existing Kitty command without st-only
  flags. All three terminal checks now return 0. The deliberate scrolling-
  behavior RED probe is expected and is not an incident.
- Next steps: Complete the documented manual visual/drag checks in a fresh
  fixture window and a fresh Codex session; automated checks do not establish
  visual acceptance.
- Patch-context failure: The first combined implementation patch was rejected
  because its README context used a different example placeholder than the
  existing command table. No implementation files changed. Re-read the exact
  line and split the source and documentation patches; both then applied.
- Follow-up: Use known repository paths for workflow helpers. Keep this note
  with the related [implementation plan](../../plans/kitty-codex-scrollback.md)
  and changes in any future commit.
- Follow-up inspection, 2026-10-04: A broad read-only `rg --files /tmp` search
  encountered permission-denied messages for service-private directories.
  It made no changes. Limit subsequent source searches to the installed Codex
  package and explicitly known task directories; use official documentation
  when that package does not ship its configuration schema.
- Config-probe failure, 2026-10-04: The npm Codex binary rejected the existing
  `model_reasoning_effort = "max"` before reaching the intentional invalid
  scrolling-setting probe. The diagnostic assertion therefore failed for an
  unrelated reason. No model setting was changed. An isolated minimal
  CODEX_HOME probe then correctly rejected an invalid alternate-screen enum
  and accepted `never`. The normal fish PATH selects Codex 0.160.0, while the
  i3 launcher used an old 0.114.0 installation. The normal runtime accepts the
  full existing config plus the scrolling override (exit 0). The shortcut now
  uses that verified runtime. After apply/refresh, the actual Node/CLI pair
  parses the deployed config without any scrolling override (exit 0), and i3
  reload reports success. Root cause: fnm's default alias and the interactive
  shell selected different Codex installations. Resolution preserved all
  existing model settings and changed only the shortcut's runtime path.
- Commit verification, 2026-10-04: A probe assumed the clean-looking
  `dot_codex/config.toml` status meant its scrollback setting was already in
  HEAD. Parsing HEAD instead found no `tui.alternate_screen` and raised a
  KeyError. The terminal, fixture, and README checks passed. No staging or
  commit occurred. Inspection found the file's skip-worktree bit set: source
  and live contain `never`, but HEAD/index do not. Its other local fields are
  unrelated to this task. Stage only this session's TUI addition against HEAD
  and preserve the flag and local bytes. Cleanliness alone is not evidence
  that a setting was committed.
- Staging verification, 2026-10-04: The exact session patch and reviewed files
  staged successfully, then an overly broad source/live byte-equality assertion
  failed. Both files are actively used by other sessions, so inspect only the
  requested TUI value and exact staged candidate for shipping; retain unrelated
  local/runtime differences. Follow-up parsing found identical semantic
  contents and `never` in both files; only serialization differed. The staged
  Codex blob exactly matched HEAD plus the authorized setting/comment, with
  skip-worktree preserved. No commit or push had occurred at that point.
