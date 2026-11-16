# Comfortable wallpaper palettes

Replace neon terminal accents with restrained semantic colors, verify actual exports and every wallpaper, then activate with rollback evidence.

## Outcome, context and boundaries

Execute prompts/pywal-comfortable-terminal-palette.md once. Preserve opacity 0.9, fonts, images, decoder/sparse fallbacks and unrelated dirty work (snapshot /tmp/pywal-comfort-evidence/initial-status.txt). Generator, verifier, their tests, README and smoke documentation are in scope. No commit/push requested.

## Decisions and assumptions

Use six conventional ANSI hue families, muted OKLab chroma, paired normal/bright shades and neutral body text. Modest hue adjustment comes from the normalized wallpaper background so restore is deterministic. Contrast remains 4.5 text / 7 body over the 0.9 composite envelope. Normalize only unsupported backgrounds to allow subdued text. Numerical chroma/lightness limits are design judgments informed by Nord and Kanagawa, not medical comfort scores. User already authorized implementation in the saved specification; no additional design gate is required.

## Ordered checks

- [x] Capture dirty state, inspect screenshots, generator, consumer path and prior incidents.
- [x] Research primary sources and settle policy.
- [x] Define and observe failing comfort/semantic/idempotence regressions.
- [x] Implement generator/verifier policy and run focused regressions.
- [x] Fresh complete wallpaper discovery and isolated four-worker verification.
- [x] Attempt full refresh; preserve rollback, activate scoped pywal scripts and inspect real terminal/editor.
- [x] Align docs and review final evidence.

## Risks and rollback

Subjective comfort requires user feedback; metrics only constrain legibility/chroma. Colored selection surfaces and application-owned truecolor remain outside coverage. Keep live cache backup before activation; never overwrite local-newer source. Existing duplicate MIME chezmoi targets may block refresh; retain unrelated files. No source image changes. Prior complete 667-image runs are historical only.

## Evidence and review

Postmortem lookup: `pywal vivid harsh saturation palette` returned an unrelated PDF color measurement finding, inapplicable to terminal palettes. Prior wallpaper reports confirm decoder/isolation capabilities to retain. Screenshot evidence directly shows pure red/magenta/cyan, competing syntax salience and cyan ordinary text. One exploratory read used a nonexistent personal-context helper filename; discover the actual helper before use, no remedy inferred.

Sources: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum ; https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html ; https://www.nordtheme.com/docs/colors-and-palettes/ ; https://raw.githubusercontent.com/rebelot/kanagawa.nvim/master/lua/kanagawa/colors.lua ; https://bottosson.github.io/posts/oklab/ .

Exact automated checks: unittest discovery for test_pywal_readable.py, test_verify_wallpaper_merge.py, test_pywal_xcf.py and i3 palette tests; full verifier `python3 scripts/executable_verify-wallpaper-merge --report /tmp/pywal-comfort-evidence/full-library.json`. Manual: comparable fish/lsd and Python Vim content in real Kitty at unchanged opacity; compare saved before/after cache and screenshots. Cursor continuation: Read this plan and saved prompt, preserve dirty work, finish unchecked items using retained raw evidence. Suggested commit: fix(pywal): soften terminal accents and neutralize body text.

RED logs: red-readable.log rejects neon chroma .3225 and tinted body .073; red-verifier.log lacks maximum_chroma. GREEN final: readable 11, verifier 19, real XCF 1, i3 1 all pass (logs under /tmp/pywal-comfort-evidence). First GREEN exposed three inherited vivid-distance fixture thresholds, corrected to the settled .02 paired-shade spec. Research rationale and exact numerical reference comparisons: docs/pywal-comfortable-palette.md. Full refresh exit1: /tmp/refresh-config.e8Z1ufFt.log reports duplicate MIME targets; preserve both. First fresh library run interrupted143 after396 began; no final report, rerun in progress with continuous monitoring.

Fresh complete report: /tmp/pywal-comfort-evidence/full-library-final.json; process64970 exit0. 667/667 pass, zero failures/collisions, exact fresh scan coverage, 15 metadata files untouched, source/cache hashes unchanged. Minimum text4.5000616806, minimum reading7.1529518891, maximum chroma.0865180103, minimum accent distance.0322270627. Thirteen unsupported backgrounds normalized. Current adapter/verifier SHA-256 match report. Independent review found no material defect; reviewer also stress-checked1000seeded backgrounds with contrast, comfort, background and idempotence checks.

Scoped activation: process94711 exit0. Local installed scripts matched HEAD before replacement, no local drift overwritten. Backed up both old scripts and full wal cache under /tmp/pywal-comfort-evidence/rollback; executable restore.sh provides rollback. Installed adapter/verifier and restored current theme; actual live JSON exactly matches reviewed proposed palette. Updated15running Kitty sockets. Full refresh remains blocked by duplicate MIME targets; this is scoped activation only.

Actual visual verification: retained vim-before.png/vim-after.png, terminal-before.png/terminal-after.png and fresh-window-after.png under /tmp/pywal-comfort-evidence. Inspected screenshots show neutral body text and quieter semantic highlighting. Actual Vim query: Normal#D8DADF/String#99BA82/Type#CCA86F/Function#82B3E2/Keyword#B8A1DB/Comment#A4A6AB on#050412. Fresh standalone Kitty get-colors matches live background/foreground/cursor; opacity0.899999976 remains0.9. Source and live scripts match; rollback script shell syntax checked without executing it.

Documentation: README, docs/smoke-tests.md, docs/pywal-comfortable-palette.md and prior verify-wallpaper-merge plan now identify current policy versus historical evidence. Postmortem ledger targeted check passed with no errors/new/changed/unregistered aliases; local contrast-versus-comfort lesson appended. No commit or push requested/performed. No new dependencies, fonts or opacity changes. Subjective comfort, physical display calibration, colored selection surfaces and application truecolor remain outside proof. Actual Codex wrapped-selection/paste interaction is unavailable to shell automation; no TUI rendering settings changed.

## Reproducible handoff

Automated checks run this turn (all exit0):

```text
python3 -m unittest discover -s tests -p test_pywal_readable.py
python3 -m unittest discover -s tests -p test_verify_wallpaper_merge.py
python3 -m unittest discover -s tests -p test_pywal_xcf.py
python3 -m unittest discover -s tests/scripts -p test_executable_generate_i3_pywal_colors.py
python3 scripts/executable_verify-wallpaper-merge --report /tmp/pywal-comfort-evidence/full-library-final.json
python3 dot_agents/skills/postmortem-memory/scripts/postmortem_memory.py check --postmortem /home/kevin/linux-config/docs/postmortem/2026-11-16-harsh-terminal-palette.md
git diff --check
```

The completed report path already exists; choose a new report path on rerun. Manual checks performed: restore current theme, compare fish syntax/lsd and unfolded Python Vim content in the same Kitty, query actual Vim highlights, compare opacity, start fresh standalone Kitty and compare its colors with exports. No source images moved, deleted or merged. Full-refresh conflict was preserved, not bypassed as a success claim.

Paste-ready Cursor prompt: Review the completed pywal comfort change using plans/pywal-comfortable-terminal-palette.md and docs/pywal-comfortable-palette.md. Preserve all pre-existing dirty work. Validate any follow-up against the recorded tests and real terminal/editor views; keep contrast floors and decoder fallbacks. No commit or push is authorized by this continuation prompt.

Atomic plan completed: define RED → replace shared policy and verifier → focused GREEN → fresh entire-library pass → backup/scoped activation → real consumer inspection → documentation/incident learning/review. All requested implementation steps are done; full-refresh conflict and subjective/truecolor limits remain disclosed.

Final evidence reviewer verified all remaining claims against the completed report, current source/installed hashes, live palette and real screenshots. Raw terminal-after.png includes an incidental concatenated command typo before successful output; fresh-window-after.png is the clean standalone lsd rendering. The postmortem records this automation artifact. Rollback not executed (would undo activation). Disposable verification terminals closed and original focus restored.

Follow-up: the duplicate MIME full-refresh blocker was subsequently resolved and actual refresh completed0. See [identical MIME recovery](refresh-config-identical-duplicates.md) for implementation, backup and verification. Earlier scoped-activation evidence remains accurate for its original run.
