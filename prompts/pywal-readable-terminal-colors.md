# Fix pywal text contrast in dark transparent terminals

Implement the user's requested pywal readability fix in /home/kevin/linux-config. Inspect the actual palette-generation and application paths before choosing the smallest complete change. Execute this task once; do not invoke metaprompt-run again.

## Reported failure and evidence

The current wallpaper-derived palette can assign text colors so dark that they blend into the dark semitransparent terminal and underlying wallpaper. In the supplied screenshot, fish arguments/options in `lsd -F --group-dirs first` are dark blue and nearly unreadable. The screenshot is available at /home/kevin/Pictures/screenshots/desktop/unsorted/screenshot-2026-11-15_20:23:33.png. Inspect it directly. The user's goal is that every generated color used for terminal text remains readable, regardless of a dim wallpaper's extracted palette. Automatically brighten any unsafe text color while retaining its hue where feasible.

## Context and scope

Read AGENTS.md, dot_codex/AGENTS.md and applicable nested instructions; follow normal runtime permissions. Inspect relevant existing pywal wrappers/hooks/templates, terminal opacity/background configuration, fish highlighting and ANSI/truecolor consumers to trace why the screenshot's argument color is dark. The checkout contains unrelated dirty work; preserve it and capture fresh git status before edits. Do not assume pywal alone owns every visible color.

## Implementation and verification

1. Reproduce the unsafe palette/highlighting with a failing executable regression before implementation. Use the actual screenshot palette/config when available and deterministic dark/saturated fixtures.
2. Define a measurable text-contrast floor, using relative luminance and contrast ratio rather than RGB brightness alone; use at least 4.5:1 for normal text against the supported dark backgrounds. Account for the configured opacity and underlying wallpaper's composited dark background, and explain the tested envelope. A universal guarantee for arbitrary wallpaper pixels/transparency is impossible: do not claim one. Keep the configured dark background appearance; repair foreground/text roles, preserving intentional background roles and readable foregrounds.
3. Fix the shared palette/application path so every generated text slot, including normal/bright ANSI and fish argument/option highlighting, is checked and unsafe colors are brightened. Verify any fixed truecolor override implicated in the failure. Ensure regeneration, cached-palette reuse and reload cannot bypass the correction. Reuse existing helpers and avoid dependencies or unrelated redesigns.
4. Verify all text colors numerically across dark, near-black, saturated-blue and already-readable fixtures; check idempotence, valid color output, preserved background roles and propagation into actual generated consumer configs. Run focused regression and relevant broader checks.
5. Apply the corrected current theme under normal permissions and inspect the real terminal rendering where available, including the reported fish command and an ANSI color sample on the dim wallpaper. Follow repository refresh-config requirements for tracked configuration changes. Distinguish numerical checks from visual checks and explicitly report any live validation blocked by permissions or tooling.
6. Keep the required plan and relevant usage/smoke-test documentation accurate. Report the changed paths, contrast floor, observed before/after evidence, automated/manual verification, persistence on future wallpaper changes and remaining limitations. Do not add unrelated features or alter existing user work.
