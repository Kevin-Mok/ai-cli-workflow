# Readable pywal terminal colors

Repair generated terminal text while retaining the dark background. Trace generation and fish highlighting, establish a failing reproducer, then repair and verify the shared export/application path.

## Scope and protected state

Execute `prompts/pywal-readable-terminal-colors.md` once. Initial git status captured before edits; README, smoke tests, lessons, postmortem ledger and many unrelated files were already dirty. Preserve all prior hunks; user later invoked `$commit-session`, authorizing scoped commit and upstream push. Screenshot directly inspected: fish options are saturated dark blue, executable filenames/prompt accents dark teal. No unrelated UI redesign.

## Decisions and assumptions

Use WCAG sRGB relative luminance and a minimum 4.5:1 text contrast. Kitty is configured at opacity 0.9. Bound supported background by compositing the existing dark background with white at 10% in sRGB; this bounds any wallpaper pixel at this opacity. Also consider opaque background. Preserve special background; ANSI color0 must be safe as text, so templates must use special background for intentional background roles. Preserve already readable text and hue when feasible. Raw upstream wal remains outside the repo wrapper guarantee.

## Ordered work

- [x] Capture dirty state, inspect screenshot, read instructions and lookup incident memory.
- [x] Trace actual palette and fish consumer paths and record root cause.
- [x] Add executable regression; observe expected RED before implementation.
- [x] Repair shared generation/restore/export path; named ANSI fish highlighting requires no truecolor override.
- [x] Verify fixtures, idempotence, background roles, real consumer exports and wrapper integration.
- [x] Update README/smoke checks, apply current theme, run refresh-config and inspect runtime where permitted.
- [x] Record final evidence, review and limits.

## Verification

Run focused unittest regression via a tests agent. Use real installed pywal export templates in an isolated HOME; exercise fresh generation, cached generation and restore with a deterministic fixture. Numerically check all 16 ANSI slots and special foreground/cursor against opaque/composited backgrounds. Inspect fish param/option configuration and generated Kitty/Xresources/Vim/shell/sequences. Run syntax checks and adjacent pywal/i3 tests. Apply corrected current colors through wrapper restore without changing wallpaper, then read actual generated files and fish highlight output. Inspect a real terminal if display tooling permits; report numerical and visual evidence separately.

## Risks and rollback

Brightened ANSI black also changes applications using it as background; preserve explicit special background roles and document ANSI ambiguity. Arbitrary lower opacity/bright themes/custom truecolor are outside supported envelope. Refresh may encounter unrelated dirty/local divergence; do not overwrite it. Roll back only this session’s helper/wrapper/fish edits and restore previous cached palette from private /tmp backup if required.

## Evidence and review

Memory lookup `pywal contrast`: no match. Broader query returned unrelated fish transport and Kitty clipboard findings; none establishes a contrast remedy. Initial diagnostics guessed nonexistent fish config paths; resolve from actual tracked tree instead. No remediation based on guesses.

RED: `python3 -m unittest discover -s tests -p test_pywal_readable.py`: five expected assertion failures (1 test with fixture subtests), blue 2.0687:1 and purple 1.7961:1 against #050412. Fish parameter uses ANSI36 (color6); no fixed truecolor implicated. Hook upstream sequences.send before exports; normalize deprecated -r to -R. Preserve known color0 background roles in built-in exports (st, dmenu, dwm, tabbed, oomox).

Review found Vim LoadWalPalette parses color0 as background and uses ctermbg=0. Expanded scope to dot_vimrc.tmpl and its static regression: parse explicit background and use pywal's OSC4 special-background slot 232 for terminal background/invisible text roles. Defining headless Nvim RED: actual #85858C versus expected #050412, exactly one failure of five. No fish override change is needed because all relevant values are named ANSI colors.

## Final verification and delivery

Fresh final checks (all exit0): `python3 -m unittest discover -s tests -p test_pywal_readable.py` (6 tests); `bash tests/test_apply_pywal_theme.sh`; `python3 -m unittest discover -s tests/scripts -p test_executable_generate_i3_pywal_colors.py` (1 test); `bash tests/test_vim_pywal_background.sh`; `bash tests/test_vim_wal_live_refresh.sh` (actual Nvim); `bash -n scripts/executable_apply-pywal-theme`; `python3 -m py_compile scripts/executable_pywal-readable`. Logs /tmp/pywal-final-*.log. No mypy/pyright installed; no unrelated whole-repo suite run. README gate pass_no_change; targeted postmortem ledger check has no errors. Independent reviewer found the upper-background light-side issue; exact RED preceded fix, final reviewer resolved it with no remaining important findings.

Live current palette restore -R -n exited0. Preserved background #050412; composite bound #1E1D2A. ANSI minimum4.5032:1, blue #1626c7 -> #737DDD, purple #560f8e -> #9E75BE. Real Kitty ANSI/fish screenshot /tmp/pywal-readable-ansi.png and composited AlsaMixer screenshot /tmp/pywal-readable-alsamixer.png inspected: readable text/labels, no audio changes. Both required refresh-config attempts stopped on pre-existing duplicate mimeapps.list targets before applying. Scoped approved installation of two theme scripts and implicated Vim background expressions completed; original cache/wrapper/Vim private backups in /tmp/pywal-readable-live-backup. Existing Vim needs config reload/restart; st needs normal header rebuild. No arbitrary opacity/compositor/truecolor/colored-background guarantee.

### Atomic commit milestone

`fix(pywal): brighten unsafe terminal text colors`: helper + wrapper + Vim reader, executable regression coverage, usage/smoke docs and this plan. Scope helper returned unsafe because nested execution writes were not recognized; use the directly observed edit record and initial dirty baseline. Mixed README, smoke tests, lessons and source ledger require only this session's separable changes. The pre-existing untracked compiled prompt is a reviewed required specification prerequisite; include it without other parent-session work. Preserve all unrelated dirty files. Commit and push origin/main once after checks. Pending push status is reported in the final handoff, not assumed here.

### Reproducible manual check

In Kitty with normal 0.9 opacity, run `~/scripts/apply-pywal-theme -R -n`, type `lsd -F --group-dirs first` in fish, then open `alsamixer` and inspect purple/blue labels; Escape exits without changing volume. Repeat after a normal wallpaper change and in a new Kitty. Verify Vim remains dark after reloading its config; regenerate/rebuild st normally if used. Three final handoff commands exercise restore, fish highlighter and actual mixer.

### Paste-ready Cursor prompt

Review `plans/pywal-readable-terminal-colors.md` and `prompts/pywal-readable-terminal-colors.md`. Preserve unrelated dirty work. Run the six focused checks listed above, inspect the installed helper/wrapper bytes and current palette contrast, and verify fish/AlsaMixer labels in Kitty at 0.9 opacity. Do not invoke metaprompt-run or alter audio settings. Report numerical versus visual evidence separately; full refresh is blocked by unrelated duplicate MIME targets.
