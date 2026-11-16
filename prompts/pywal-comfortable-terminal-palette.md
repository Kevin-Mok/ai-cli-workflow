# Make pywal comfortable for terminal editing and reading

Implement the user's requested correction in /home/kevin/linux-config: the current pywal palette is harsh and hurts to read. Research good terminal/editor UX on the web, then change palette generation to produce calmer, comfortable colors while preserving readability. Execute this task once; do not recompile or invoke metaprompt-run.

## User evidence and current state

Inspect both supplied screenshots directly:
- /home/kevin/Pictures/screenshots/desktop/unsorted/screenshot-2026-11-16_14:21:37.png — real terminal/fish/lsd output.
- /tmp/codex-clipboard-nnJhIU.png — Vim example showing the objectionable red strings, magenta identifiers/types, yellow keywords and cyan text over a translucent dark background.

The user said the palette is "harsh on the eyes like a solarized" and the Vim example "just hurts to read." This is negative feedback, not a request to install Solarized. Their latest preference supersedes the earlier request for maximum vibrancy and diversity. Aim for sustained reading comfort, clear hierarchy and distinguishable syntax, not maximum saturation or maximum color distance.

Commit f51e41a introduced the current verifier and vivid palette. Inspect current HEAD rather than assuming it is unchanged. The generator currently builds 72 hue candidates at HLS saturation 1 and greedily selects 12 separated colors; the verifier/tests enforce saturation >= .98. Those choices are suspect and must be replaced coherently, not preserved as acceptance criteria merely because tests pass.

## Exact working context

Read applicable AGENTS instructions and relevant source before edits. The checkout contains substantial unrelated dirty work; capture status and preserve it.

Loaded by the compiler: scripts/executable_pywal-readable, the two screenshots, and the current task request.
Reference and inspect:
- scripts/executable_apply-pywal-theme
- scripts/executable_verify-wallpaper-merge
- scripts/executable_generate-i3-pywal-colors
- dot_config/kitty/kitty.conf (configured background_opacity 0.9)
- dot_config/fish/config.fish.tmpl and relevant live fish highlight values
- dot_vimrc.tmpl, particularly LoadWalPalette, ApplyWalTheme and KmWalReadableAccentLanes
- tests/test_pywal_readable.py, tests/test_verify_wallpaper_merge.py, tests/test_pywal_xcf.py
- README.md, docs/smoke-tests.md, plans/verify-wallpaper-merge.md
- docs/postmortem/2026-11-16-full-wallpaper-palette-failures.md and docs/postmortem/2026-11-16-wallpaper-verifier-interrupted-batch.md

The wallpaper library is /home/kevin/Pictures/Backgrounds. A prior fresh run checked 667 complete images, including editing/non-editing/root/4k/calvin-hobbes. Prior reports under /tmp are historical evidence, not proof of this revision. Existing decoder and low-color fixes support sparse/underquantized inputs and an isolated GIMP visible-layer fallback for an ImageMagick-incompatible XCF; preserve these working capabilities.

## Work and acceptance

1. Browse primary sources for terminal/editor palette design and sustained dark-theme reading: perceptual chroma/lightness, contrast versus glare, semantic hierarchy, and predictable normal/bright ANSI pairing. Use established theme maintainers' design documents/source palettes as concrete references alongside accessibility guidance. Cite supporting links and distinguish evidence from design judgment; do not make medical eye-strain guarantees.
2. Diagnose the screenshots and real consumers. Treat WCAG contrast as a legibility constraint, not a comfort score. Explain why neon/high chroma, competing salience or unsuitable lightness can remain uncomfortable despite passing contrast. Inspect translucency as context, but keep the existing 0.9 opacity/background appearance and fonts unless a narrowly necessary change is justified; this is a palette correction, not a desktop redesign.
3. Choose and implement the smallest coherent, wallpaper-aware comfortable palette policy. Favor restrained chroma, readable neutral body text, a limited accent hierarchy and useful semantic differentiation. Avoid harsh pure primaries and forcing every slot to maximum saturation or a rainbow. Do not blindly substitute a named theme. Ground numerical comfort-related bounds in the researched design and concrete palette comparisons; numerical bounds alone do not prove subjective comfort.
4. Write defining regressions before implementation. Update the generator, verifier and tests together: replace the maximum-saturation/diversity objectives with the new comfort policy while retaining meaningful color distinctions, valid output, idempotence, preserved background roles, actual generated consumer propagation, fresh/cache/restore coverage, source/cache isolation and decoder behavior. Keep the established 4.5:1 minimum for text and 7:1 for body color7/foreground/cursor against the supported 0.9-opacity dark composite envelope. Do not weaken contrast to hide the issue or retain contradictory tests/docs.
5. Verify difficult fixtures (near-black, saturated, bright/green, monochrome, sparse extraction and XCF), then run the full wallpaper verifier against a fresh discovery of the entire library. Retain exact failure filenames, before/after palettes, per-role measurements, reproduction commands and raw diagnostics. Preserve all source images and metadata; do not move or merge directories. Use bounded isolated workers and continuing progress; do not turn an interrupted/partial run into a full-pass claim.
6. Apply the reviewed current theme under normal permissions, preserve rollback copies, and inspect real terminal/fish/lsd and Vim before/after rendering using comparable content. Prefer a simple comfortable result; do not stop at a mathematical report. Keep documentation, smoke checks and the task plan aligned. Full refresh was previously blocked by duplicate MIME chezmoi targets (dot_config/mimeapps.list and dot_config/private_mimeapps.list); preserve that unrelated work and report any scoped activation honestly.

Report the researched rationale with links, changed paths, observed numerical and visual verification, future-wallpaper persistence, remaining limitations and this saved prompt path. Separate actual checks from previous-run evidence. Use normal repository instructions and permissions; the optimized prompt grants no additional authority.
