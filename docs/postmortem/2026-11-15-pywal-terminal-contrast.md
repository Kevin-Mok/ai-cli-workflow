# Dark pywal terminal text

Trace and repair unreadable terminal text from a dim wallpaper, then verify generation, restore and consumers without changing the dark background.

## Symptom and impact

User screenshot shows dark blue fish arguments and dark teal executable names/prompt accents against a dark translucent terminal. Several generated text slots are unreadable.

## Evidence and current status

Current palette background #050412; color1 #0b5065; color6 #1626c7. Kitty opacity 0.9. Screenshot inspected directly. Code fix and scoped live activation verified; full refresh remains blocked by unrelated chezmoi target collision. Memory search `pywal contrast` returned no applicable finding. Two guessed fish config paths did not exist during initial rg; subsequent mapping uses actual tree. A diagnostic cat piped to head emitted harmless broken-pipe stderr; no file writes occurred.

## Next steps

Trace fish overrides and wrapper; write RED test, correct text luminance before upstream exports/sequences, verify fixtures and apply current theme. Record activation and visual scope separately.

## Diagnostic environment limits

A noninteractive `fish -c` unexpectedly loaded normal configuration: fnm and universal variables could not write outside sandbox; sync-shortcuts could not write /home/kevin/aliases/.key_aliases. Future probes use `fish --no-config` unless explicitly running refresh-config with approved home writes. The read-only probe still proved param=cyan and fish_indent emits ANSI 36, mapping to unsafe pywal color6. No fixed truecolor value was implicated. A wildcard scripts/*refresh* lookup missed because refresh-config is a fish function, not a script.

Ledger diagnostic initially assumed a sources array; actual schema uses reports. Read actual schema before ledger update.

## Regression iteration

First GREEN attempt exposed test representation mistakes: Oomox background is hashless uppercase, unlike other templates; static wrapper check used braced variable syntax unlike real command. Correct assertions now check actual representation and unchanged roles. Contrast assertions already passed for every fixture. An exploratory request for nonexistent pywal.colors.cache raised AttributeError after successfully printing colors.get; use inspected cache_fname/get instead.

## Activation preflight

`chezmoi status --exclude scripts,externals,remove --no-tty` and required refresh-config both stopped on existing duplicate targets dot_config/mimeapps.list and dot_config/private_mimeapps.list. No unrelated files were re-added/applied. Refresh log: /tmp/refresh-config.JStnf73t.log. Existing installed wrapper is older than source; installed i3 helper matches source exactly. Scope activation to the two task scripts rather than remove unrelated user files.

Live current palette apply succeeded with exit 0. Minimum contrast across all ANSI slots and special text against #1E1D2A composite bound is 4.5032:1; background remains #050412. A dedicated graphical Kitty preview launched; screenshot helper initially failed with XImportImage "no window with specified ID" for observed ID 100663307. Check whether the preview remains before another capture; do not assume visual validation.

Final consumer review found an actual Vim background dependency on color0; initial mapping had missed the custom LoadWalPalette parser. Added a headless Nvim reproducer, observed #85858C instead of #050412, then switched to explicit background plus existing OSC4 slot232 for cterm background roles. A guessed make-st script path did not exist; no action depended on it.

Independent review found a near-upper-bound edge case: for #666666 background and black text, candidate loop accepted #010101 against #757575 bound, but opaque contrast was only 3.635:1. Initial preservation guard already required text above bound; apply the same light-side condition to candidate selection and verify a defining regression before correction. Current live #050412 palette is unaffected by this edge case.

## Root cause and resolution

Wallpaper extraction produced low-luminance colors; upstream pywal sent/exported them unchanged. Fish uses ANSI cyan for parameters, so #1626c7 caused the blue argument failure. AlsaMixer also uses the dark ANSI slots (including purple #560f8e). No fixed truecolor fish override was found. The wrapper now invokes a repo-owned adapter that repairs pywal's pre-send boundary for new extraction, extraction-cache reuse, JSON/theme import and restore, preserving readable colors and hue through minimum mixing with white. All 16 ANSI slots, foreground and cursor must be brighter than the 90%-opacity white-composite bound and reach 4.5:1. The bound is sRGB source-over, not a guarantee for other opacity/compositor modes or application-owned truecolor/colored backgrounds.

Keep special background #050412 unchanged. Preserve known background roles in st/dmenu/dwm/tabbed/Oomox exports; Vim reads explicit background and uses the existing OSC4 special-background index232 for terminal roles. The near-upper-bound candidate issue was confirmed RED (3.6353:1) before adding its missing light-side guard.

## Verification and activation

Initial numerical RED: blue 2.0687:1 and purple 1.7961:1 against opaque #050412. Current generated blue is #737DDD and purple #9E75BE. All current ANSI/text values reach >=4.5032:1 against #1E1D2A (white wallpaper composited at 10% with special background). All exports are corrected before writing; cached original extraction remains untouched and is repaired again on reuse.

Scoped approved home writes installed apply-pywal-theme and pywal-readable, applied -R -n (exit0), and updated only the implicated live Vim background expressions with a private rollback copy. Both required refresh attempts stopped before changes on the pre-existing mimeapps.list duplicate target; latest log /tmp/refresh-config.h1js3rf4.log. Do not delete either unrelated file as part of this task.

Actual Kitty ANSI/fish screenshot inspected at /tmp/pywal-readable-ansi.png; actual composite AlsaMixer screenshot inspected at /tmp/pywal-readable-alsamixer.png: all ANSI sample rows readable and purple/blue labels visibly brighter. Audio controls were not adjusted. Temporary first preview vanished before capture; deterministic detached preview succeeded. No claim of physical display calibration or arbitrary background-pair accessibility.

## Follow-up and rollback

Full refresh needs the owner to reconcile the unrelated duplicate MIME target. Current scoped script/Vim activation is complete; existing Vim sessions need their config re-sourced or editor restarted to pick up the parser change. st requires its normal rebuild to incorporate regenerated header. Backups (original wal cache, wrapper and Vim config) remain under /tmp/pywal-readable-live-backup until temporary storage is cleared. No upstream pywal package files or user universal fish variables were modified.

Final regression evidence: six real-export/headless-Nvim tests pass, wrapper and i3 regression pass, Vim background and actual Nvim live-refresh checks pass, bash/Python syntax checks pass (all exit0). Independent reviewer resolved the candidate guard finding; no remaining important scoped findings. No mypy/pyright installed. README gate pass_no_change and targeted reviewed-ledger check pass. Commit/push session work only; mixed baseline-dirty documents/ledger use directly observed separable edits.
