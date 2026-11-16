# Comfortable wallpaper-derived terminal colors

This policy makes terminal and editor text calmer without lowering the readability floor. The adapter extracts the wallpaper, assigns restrained semantic colors, checks contrast before exporting, and uses the same correction for future wallpapers and restores.

## Why the old palette was uncomfortable

The supplied terminal and Vim screenshots show pure red, magenta, cyan and yellow competing across ordinary syntax. The old generator deliberately used HLS saturation 1 and maximized distance among twelve accents. It also retained cyan ordinary text. High contrast can make text distinguishable without establishing a useful hierarchy or comfortable sustained reading. The visible browser/background detail remains possible at opacity 0.9; opacity and fonts are unchanged here.

[WCAG's contrast guidance](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum/) supports a legibility floor; it does not score subjective comfort. [Visual Presentation](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html) also emphasizes user-adjustable presentation. [Nord's design guidelines](https://www.nordtheme.com/docs/colors-and-palettes/) describe dimmed pastel colors, semantic grouping and uncluttered highlighting. [Kanagawa's actual source palette](https://raw.githubusercontent.com/rebelot/kanagawa.nvim/master/lua/kanagawa/colors.lua) provides concrete restrained Dragon colors alongside brighter diagnostic colors. [OKLab's author](https://bottosson.github.io/posts/oklab/) explains separating perceived lightness, chroma and hue. These are references, not a claim that a named theme guarantees comfort.

Measured with the adapter's OKLab transform:

| Reference sample | Chroma range | Lightness range |
| --- | --- | --- |
| Nord Aurora: BF616A, A3BE8C, EBCB8B, B48EAD | .062–.121 | .606–.855 |
| Kanagawa Dragon: C4746E, 87A987, C4B28A, 8992A7 | .033–.102 | .645–.769 |
| Proposed current normal accents | .085–.086 | .749–.751 |

These comparisons motivate, rather than scientifically prescribe, a chroma target of .085. We use a higher lightness than some reference colors to meet the existing translucent-terminal contrast requirement.

## Generator and verifier contract

- ANSI 1–6 keep muted red, green, yellow, blue, magenta and cyan families at OKLCH hue 25/140/85/255/310/200°. The normalized wallpaper-background hue shifts them by at most 8°, preserving semantic roles. This modest influence intentionally reduces wallpaper-to-wallpaper variation.
- ANSI 9–14 are the same families, .035 higher in lightness. There are six color families, not twelve unrelated attention colors.
- Normal lightness starts at .75 and increases only until 4.55:1 contrast is reached; the small margin covers RGB rounding. Gamut mapping reduces chroma rather than clipping channels. Verification requires chroma .055–.105, lightness at most .86, twelve unique RGB values and pair distance at least .02. Brights must be lighter and remain within .07 OKLab of their normal partner.
- Ordinary body/cursor/color7 text uses neutral #D8DADF, adjusted upward only if needed for 7:1 contrast. ANSI gray roles are also neutral. This removes the old cyan wash.
- Every text slot remains at least 4.5:1 over the dark background and its 0.9-opacity black/white sRGB composites. Body roles remain at least 7:1. Already-supported dark backgrounds are preserved; other backgrounds darken by a black mix until the white-composite headroom is 10:1. That leaves room for subdued text instead of forcing near-white accents. The current #050412 background stays unchanged.
- Fresh extraction, cached extraction, -R and legacy -r restore all run through the shared pre-export boundary. Kitty, Xresources, Vim, shell exports and terminal sequences receive the repaired colors. Background-specific export roles, sparse extraction and GIMP XCF decoding remain intact.

These limits are design judgments. They do not guarantee medical eye-strain relief, color-vision equivalence, arbitrary selection backgrounds, lower opacity or application-owned truecolor.

## Reproduction, activation and rollback

Use `~/scripts/apply-pywal-theme -R -n` to restore the current theme through the policy. Wallpaper shortcuts use the same installed adapter. Run `python3 scripts/executable_verify-wallpaper-merge --report /tmp/pywal-comfort-new-report.json` from the checkout for a fresh recursive library check; the report path must not already exist. It preserves source files, source metadata and the active cache, and retains exact paths, extraction palettes, repaired palettes, per-role measurements and raw subprocess diagnostics in its JSON report.

Inspect real fish command highlighting and `lsd -F --group-dirs first --size short`, then a Python buffer in Vim/Neovim with folds opened. Compare strings, types, comments, functions and keywords, and check neutral body text. Also check a fresh Kitty window. Visual judgment remains part of acceptance; the numerical checks alone are insufficient.

Current task evidence, activation status and rollback paths are recorded in [the execution plan](../plans/pywal-comfortable-terminal-palette.md). Full refresh can stop at an unrelated duplicate MIME target; scoped pywal installation must be reported separately from a successful full refresh. Restoring only a cached old palette through the new adapter re-applies the new policy; an actual old-policy rollback requires the backed-up old adapter and cache together.
