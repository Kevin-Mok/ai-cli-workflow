# Verify every wallpaper and generate readable palettes

Deliver a reusable read-only verifier for every background image and make the actual pywal application path produce vivid, distinct editing colors with measured contrast. Diagnose each failure precisely, preserve source images/live state during verification, and prove the full collection works.

Current comfort-policy correction: [comfortable terminal palette](pywal-comfortable-terminal-palette.md) supersedes the historical maximum-saturation/diversity decisions and measurements below. Historical 667-image results do not verify the replacement policy.

## Current scope and protected state

User expanded the original non-editing merge check to every background recursively, future additions, actionable diagnostics, fixes for all actual failures, and vivid/sharp/diverse colors for Vim and reading. Initial git status was captured before edits. Preserve all pre-existing dirty files and unrelated README/smoke/ledger/lessons hunks. No move/delete/merge mode. User subsequently invoked commit-session to authorize this scoped commit and upstream push. Previous fix commit08b8b66 remains the baseline.

Files: scripts/executable_verify-wallpaper-merge (new CLI), scripts/executable_pywal-readable (real extraction/application adapter), dot_vimrc.tmpl (keep validated six syntax lanes distinct), tests/test_verify_wallpaper_merge.py, tests/test_pywal_readable.py, tests/test_pywal_xcf.py, README.md, docs/smoke-tests.md, this plan, task-specific incidents/lessons/review ledger.

## Settled design

Verifier --root defaults to ~/Pictures/Backgrounds. Discover standard raster images/XCF/PPM plus image signatures and numbered suffixes anywhere under root; prune .git, reject symlinks/nonregular entries and traversal errors. Unknown files outside merge sources and incomplete .crdownload files are preserved metadata. Check bright/non-editing→bright/editing and dim/non-editing→dim/editing destination/ancestor collisions; unknown merge-source files block, exact shuffle.txt stays behind. Other directories are verified for palette quality but have no implied move destination. Missing merge categories/empty collections fail closed.

Every image runs real installed pywal with --saturate0.8 -n -s -e in unique temporary HOME/XDG/PYWAL_CACHE_DIR; never call the desktop-reloading wrapper. Check all18 text roles, actual Kitty/Xresources/Vim/shell/sequences exports, original background policy and exact idempotent restore. Hash source/metadata and effective live cache before/after. Subprocess progress every5s; bound180s; kill only owned child group. Default emojis, --plain ASCII, --details raw failure logs. --report writes JSON exclusively at a new path outside wallpaper/cache trees; default unique private temporary run directory. Never overwrite existing reports/files. Exit0 safe images-only merge;1 any verification/merge blocker;2 setup error.

JSON includes exact image path, named failed checks, per-slot color/background/ratio/required threshold, saturation and closest OKLab pair, before/after palettes when available, child argv/environment overrides/exit codes and captured stdout/stderr, software hashes, source/cache preservation and collision/metadata evidence. Re-scan on every run: no hard-coded filenames or stale skip cache.

Contrast model: rounded sRGB source-over at0.9 opacity, opaque and black/white underlay bounds. Body roles color7/foreground/cursor require7:1; other roles4.5:1. If white-composite headroom is below7:1, darken background by mixing withblack until>=7, preserving hue. Already sufficiently dark backgrounds stay unchanged. ANSI1–6 and9–14 are12distinct maximum-HLS-saturation highlights selected from72 five-degree hue candidates, wallpaper color1 anchor rounded5deg, candidate lightness increased only asnecessary (4.55 target provides rounding margin). Greedy farthest OKLab selection maximizes minimum pair spacing within this finite pool, not a mathematical global-optimum claim. Verifier requires saturation>=.98,12unique and minimum OKLab distance>=.04; dark screenshot test>=.08. Constants use author's public-domain reference https://bottosson.github.io/posts/oklab/ . Restores regenerate deterministically from quantized anchor.

Low/sparse quantization: reuse actual extracted colors for1–15color images; if upstream16–35color retries fail but256-color extraction succeeds, evenly sample16actual colors including endpoints. Preserve successful original extraction results. XCF ImageMagick decoder failure uses existing GIMP in isolated new headless instance to merge visible layers and cache a content-addressed PNG atomically; actual wallpaper setter receives that usable persistent PNG. No original edits or invented decoder-success colors. Missing GIMP yields actionable error only for XCFs needing fallback. Vim keeps original six distinct/readable syntax roles; legacy strongest-accent fallback remains for weak unvalidated palettes.

## Checklist

- [x] Capture baseline, map source/application paths and define CLI/tests.
- [x] Observe RED before verifier: missing feature, full-root/future coverage, missing diagnostics/metrics, poisoned cache override, unreadable traversal and FIFO hangs.
- [x] Implement isolated verifier, report protections and exhaustive scanning with regression coverage.
- [x] Run121non-editing images:121/121 pass, no collisions or source/cache changes.
- [x] Run original full667:662passed/5failed; diagnose exact causes and keep living incidents.
- [x] Add REDs and fix light-background normalization, underquantization and XCF decoder incompatibility.
- [x] Add vivid/reading/perceptual-separation REDs (72anchors), implement and retain distinct Vim lanes.
- [x] Target all five original failed images with final fixes:5/5 pass.
- [x] Finish final full667 run and reconcile coverage/source/software fingerprints/quality metrics.
- [x] Attempt required refresh, activate reviewed helper/Vim changes narrowly if unrelated refresh blocker remains; inspect real terminal/Vim.
- [x] Final docs/review/ledger check and handoff.

## Exact verification and evidence

Fresh focused checks: python3 -m unittest discover -s tests -p test_pywal_readable.py (11tests including72anchors); python3 -m unittest discover -s tests -p test_verify_wallpaper_merge.py (19tests); python3 -m unittest discover -s tests -p test_pywal_xcf.py (1actual GIMP/XCF integration, portable skip if local asset/GIMP absent); bash tests/test_apply_pywal_theme.sh; python3 -m unittest discover -s tests/scripts -p test_executable_generate_i3_pywal_colors.py; bash tests/test_vim_pywal_background.sh; bash tests/test_vim_wal_live_refresh.sh; Python compile; git diff --check; README gate.

Initial real report /tmp/wallpaper-all-backgrounds-2026-11-16.json:662/667, all source/live hashes unchanged. Failed light backgrounds #11820f/#078504/#079F08 cannot support original contrast envelope. ji77X.jpeg quantizes to9/11/46colors when requesting16/35/256; original retry limit cannot supply16. ImageMagick cannot read XCF, but independent GIMP loaded and exported visible1920x1080 composite with192209colors; not source corruption. First vivid batch exposed remaining underquantization branch; extension changes only failed-generator branch, retains prior successes. Final five-case report /tmp/pywal-fixed-cases-2026-11-16.json passes5/5. Final complete current-software report: /tmp/wallpaper-all-final-parallel-2026-11-16.json (fresh exit0, matching log). The earlier sequential final attempt was interrupted and produced no JSON. Do not replace failures in an old report to claim full current-software success.

Focused metric GREEN: readable10 before last underquantization regression, verifier19, XCF1 and all adjacent checks pass. Subsequent readable11 and verifier19 pass. Logs /tmp/pywal-lowcolor-readable.log and /tmp/pywal-lowcolor-verifier.log; prior /tmp/pywal-check-*.log. Final reviewer approved palette selection, cache isolation, source/report guards and GIMP cache writes; repeat targeted review if new behavioral changes arise. No mypy/pyright installed; no unrelated entire-repo suite.

## Risks, rollback and delivery

Guarantee is numerical contrast under documented opacity/compositing, not subjective comfort, physical monitor calibration, color blindness or arbitrary app truecolor/colored selections. All current complete images must pass; incomplete downloads/scripts/archives remain metadata and must not be merged. Re-run immediately before moving because reports are point-in-time. Verification has no user-state rollback; palette activation must keep private backups and preserve unrelated local edits. Known refresh blocker: unrelated duplicate MIME chezmoi targets; do not remove either file. Authorized atomic milestone: feat(pywal): verify and diversify wallpaper palettes; commit and push only this session scope after checks.

## Paste-ready Cursor handoff

Read plans/verify-wallpaper-merge.md and preserve unrelated dirty work. Run the focused checks listed above and the actual executable_verify-wallpaper-merge over ~/Pictures/Backgrounds with a fresh report path. Require every image to pass all contrast, colorfulness, restore/export, background and collision checks. Inspect exact failed-entry diagnostics before fixes, add RED first, never silently exclude bad images. Preserve sources/cache and never move folders. Check live Kitty/fish/Vim after reviewed activation; report 667/full-root counts based on fresh discovery, software hashes and actual output.

## Execution environment and visual evidence

Sequential finalbatch exited143 at354thimage (353completed); no report existed and no completionclaimwasmade. Exact terminationcauseunknown, recorded in docs/postmortem/2026-11-16-wallpaper-verifier-interrupted-batch.md. Bounded4-worker independent image checks now run with uniqueprofiles/caches and orderedresultreporting; existingactualmulti-imageCLItestpassed afterchange. Final fresh report /tmp/wallpaper-all-final-parallel-2026-11-16.json completed exit0, logsamebasename. This current-software batch supersedes earlierpartial/failedreports.

Temporary actualKitty/Nvim preview uses productionthemefunctions and currentwallpaperpalette transformedinmemory only; no realcachewrite. Final screenshot /tmp/pywal-vivid-editor.png inspected: vivid orange strings, magenta identifiers/functions/types, green/cyan/yellow accents with readable pale-cyan body. Initial temporaryfixtures omitted walcolors_name/airlinehelper and showedswap/default-themeissues; correctedfixtureverifiedheadless exit0, disabledswapsandcapturedactualproductionhighlightsbefore screenshot. Thosefirstcaptureswerenotaccepted as paletteevidence.

## Final observed results and activation

Current-software four-worker run completed exit0:667/667 images passed,0collisions,0failures,15metadata/non-image files preserved. A fresh scan has exactly the same image/metadata path sets; current repo and installed verifier/helper hashes equal the report. All source/metadata and effective active-cache hashes were unchanged during verification. Minimum alltext contrast4.500065767572464:1; minimumreading7.001850442641139:1; minimumHLSsaturation1.0; minimumOKLab separation0.054415877408915105. Six backgrounds normalized; every generation/restore returned0 and all exports/idempotencechecks passed. No source images were moved or edited. This supersedes all older partial/failedbatch evidence.

Required refresh-config stopped before modifying files on the existing duplicate dot_config/mimeapps.list vs private_mimeapps.list target; log /tmp/refresh-config.3yHQ4Knk.log. Reviewed installed helper and live Vim accent function matched their committed baselines before narrow activation. Copied new helper/verifier to ~/scripts and replaced only the implicated live Vim function; private original cache/wrapper/helper/Vim backup /tmp/pywal-vivid-live-backup-rnxe97oe. Current theme restored without changing wallpaper, exit0. Explicit repeat restore record /tmp/pywal-vivid-live-apply-result.json proves exit0 and byte-identical live cache on repetition. Installed verifier actual smoke /tmp/pywal-installed-verifier-ot1nmkaa/report.json passed two copied original problem inputs with sources/cache unchanged. Installed bytes match current source. New Vim sessions use updated function; existing sessions need config reload/restart.

Fresh final check metadata /tmp/pywal-final-check-results.json stores exact argv, stdout/stderr and exitcode0 for all ten checks:11palette+19verifier+1actualXCF+1i3 tests (32Python tests), wrapper, Vim background, actual Nvim live refresh, compilation, whitespace and READMEgate. This retains explicit exit evidence for otherwise silent checks. No mypy/pyright available; no unrelated whole-repo suite. Evidence reviewer independently revalidated all667 palettes/pathsets/softwarehashes and observed preview; no claim of visually checking every wallpaper. Earlier reviewer notes about missing exit metadata/stale plan are resolved here and by the explicit records.

Three living postmortems finalized and their reviewed hashes registered in tracked source ledger; targeted checks all exited0 with no errors. Existing generic isolation/artifact/completeness findings apply; specific lessons added once to tasks/lessons.md. Full refresh collision remains outside task; scoped activation succeeds. Directory merge was not performed. Commit-session now authorizes shipping this implementation with its related plan/docs; no unrelated hunks enter scope.

Usage: ~/scripts/verify-wallpaper-merge --details checks all current/future images, prints a fresh report path and exits nonzero with exact failures. --plain omits glyphs, --root selects another structured collection, --report must name a new external path. On this exact checked collection, images-only merging is verified; preserve shuffle.txt and all other metadata. Re-run just before an actual move. ~/scripts/apply-pywal-theme -R -n reapplies current vivid palette idempotently. Rollback backups are temporary and private, not Git artifacts.

## Authorized commit-session milestone

Subject: feat(pywal): verify and diversify wallpaper palettes. CODEX_THREAD_ID 01a1e1fb-feeb-7b10-a242-88d432d9cb26. Scope helper reports unsafe because nested functions.exec writes are not recognized; direct observed writes plus pre-write git status establish ownership. Include source/helper/Vim/test changes, all three living incidents and their reviewed ledger records, sampling and implementation plans, and only pywal-related README/smoke/lesson hunks. All other dirty work remains excluded.

This-turn fresh pre-commit checks /tmp/pywal-commit-checks.json:32 Python tests and wrapper/Vim/syntax checks all exit0. Prior complete667-image report remains valid against current helper/verifier hashes; no source behavior changed since that run, so extraction is not repeated. README accuracy repaired for conditional XCF fallback and regenerated accents; rerun README gate before staging. Record actual commit hash/upstream push outcome in handoff. No history rewriting.
