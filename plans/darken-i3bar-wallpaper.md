# Darken wallpaper behind i3bar

Give every bottom bar an 80% black backdrop, preserving original wallpapers and pywal colors. Update the shared i3 alpha, refresh config, deploy the same narrow change to the migration-preserved live config, then validate and reload once.

## Scope and decisions

Use native i3bar ARGB: `$black$bar_trans`, alpha `cc` (204/255). All three bars share it. Alt+R is Mod1+r and already invokes apply-pywal-theme, which reloads i3. No wallpaper processing or gradient beyond the bar. Protect all initial dirty files (README and smoke-tests included); edit only related paragraphs. User subsequently requested commit-session; commit only directly evidenced session hunks.

## Checklist

- [x] Inspect bindings, shared alpha and initial dirty state.
- [x] Change shared alpha and document it.
- [x] Run refresh-config, preserve live additions and deploy alpha only.
- [x] Validate deployed config, reload once, inspect live bar colors.

## Verification and risks

Run i3 -C on deployed config; query all live bar configs for #000000cc. Manually inspect bright/dim wallpaper after Alt+R; desktop appearance requires user visual acceptance. Restore alpha 00 to undo. No new logic or automated test for a one-value configuration change. Related existing pywal regression passed. See incident report for sandbox probes.

## Handoff

Atomic plan: one shared opacity setting plus docs and live activation. Cursor prompt: Verify plans/darken-i3bar-wallpaper.md against live i3 bar configs and inspect Alt+R with bright and dim wallpapers; preserve unrelated edits. Suggested commit: fix(i3): darken wallpaper behind status bars.

## Evidence and review

refresh-config completed (exit 0). Live alpha-only edit preserved other additions. i3 -C -c ~/.config/i3/config exited 0 with pre-existing wheel command deprecation warnings; i3-msg reload returned success. All three live get_bar_config responses reported #000000cc. bash tests/test_apply_pywal_theme.sh exited 0 (silent), run by tests agent this turn. No whole-repo suite for this configuration-only change. Visual bright/dim Alt+R inspection remains user acceptance; no wallpaper was switched during validation. Live config is explicitly migration-preserved; do not replace it from the template.

## Delivery milestone: fix(i3): darken wallpaper behind status bars

Implementation and activation complete. Commit-turn checks: pywal regression exit 0; README gate pass_no_change. Scope helper returned unsafe because it did not recognize nested tool-wrapped writes (session 01a19454-41b8-7570-9f3e-5a7aacd014ea); direct observed edits establish eligibility. Commit includes config, this plan, incident report, and only session README/smoke/ledger additions. All backup, Vesktop, unrelated incident and knowledge changes stay dirty. Privacy gate and staged review required immediately before commit. Push once to origin/main after commit; no implementation blockers. Remaining acceptance: visually inspect Alt+R on bright/dim wallpapers. Rollback: set alpha to 00 and reload.
