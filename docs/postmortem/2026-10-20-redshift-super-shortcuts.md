# Redshift Super shortcut validation and activation

Record validation failures and live activation evidence while simplifying Redshift shortcuts. Preserve unrelated local config and existing dirty work.

## Symptoms and impact

A first skill read used the wrong installed path and a later config probe assumed a nonexistent .chezmoi.toml.tmpl; both reads failed without mutations. The catalog path resolved the skill. The initial X11 keycode probe could not open display :1 inside the sandbox. The source checker subsequently found Super+5 already bound to Godot, disproving the earlier mapping report that only Super+1 conflicted. Rendered i3 validation exited 139 because the sandbox could not create the runtime error log. No reload has occurred yet.

## Lookup and diagnosis

Read the tracked postmortem-memory skill and searched X11 display sandbox refresh-config. Existing execution-environment guidance and the reviewed screensaver X11 report support scoped escalation for desktop checks. Missing guessed files require using mapped/catalog paths, not changing production behavior. The Godot conflict is a real active bind found by the defining checker; the user explicitly chose to remove the Godot shortcut.

## Initial diagnosis

Source binding changes and docs exist; intentional initial RED showed missing Super-only presets. Removed the real Godot duplicate as requested. refresh-config exited 0 with REFRESH COMPLETE but the installed i3 config retained old bindings. chezmoi status reports i3 is not managed; migrationPreservedTargets intentionally keeps local machine settings outside public source. Use a scoped binding patch instead of removing that protection; preserve unrelated live changes and private paths. With runtime access, i3 -C reached validation and exited 1 for the real duplicate plus existing wheel deprecation diagnostics. Repeat after conflict removal, then reload and inspect live config. The live read-only xmodmap probe succeeded: 64 is Alt_L and 133 is Super_L. Running and installed configurations matched before activation. No visible temperature/comfort verification is claimed.

## Learning decision

No new reusable finding: existing scoped desktop-access and config-preservation guidance covers the environment; checking all active bindings and using the collision checker covers the mapping omission. Keep this report registered with its current reviewed hash when finalized.

## Concurrent temperature-scale edit

Scoped activation prepared a private candidate and ran the checker before touching the live file. It failed: the checker had concurrently changed its expected keys 4/6/7/8 to 2350/3100/3700/4600 K, while the template and installed config still contained 2400/3000/4800/5400 K. The checker modification time followed the last successful GREEN run. The live config was not changed and no reload occurred. Preserve the concurrent edit and ask which scale should be authoritative before activation. The prepared candidate is a rollback-safe private temporary file; do not bypass the failing check.

## Resolution and final evidence

The user confirmed the new temperature scale. Updated source and docs to match the concurrent checker edit. Scoped candidate validation then passed; installed only reviewed binding changes and four temperature values, preserving other live bytes. i3 validation exited 0 with existing wheel deprecations; reload returned success:true. Source, installed and running shortcut checks exited 0, and all 6 Redshift helper tests passed. refresh-config completed successfully; its lack of i3 changes is intentional machine-config preservation, not refresh failure. Live key injection proved Super+4=2350 K, Super+0=6500 K, Super+F11=workspace 11 and Alt+1=workspace 1. Starting temperature and workspace were restored. Reviewer sandbox IPC failure adds no new finding; scoped main IPC succeeded. No pending activation blocker; subjective warmth and ergonomics remain manual.

## Parallel compatibility-alias update

Final recheck observed another concurrent checker change: it now requires Alt+Super aliases in addition to Super shortcuts. Read-only task context identified the separate smoother-curve task adding both modifier families; source then passed the combined checker. Installed/live checks still lacked aliases while that task prepared activation. Do not undo its source/checker changes or duplicate live writes; wait for its activation before final verification. The previously verified Super-only behavior remains loaded.

Parallel activation completed: the combined installed and running checkers both passed with Super and Alt+Super presets/reset aliases. Requested single-modifier behavior is active and the source/live mappings agree. No activation work remains.

## Linear-range follow-up verification tool

During the later user-requested linear1800–6500 K change, the test agent's first independent Decimal assertion used quantize(Decimal(50)), which rounds decimal places instead of multiples of50. It failed with unrounded intermediate kelvin values; the preset checker and all6 controller tests already passed. Corrected the independent calculation to divide by50, quantize to an integer using ROUND_HALF_UP, then multiply by50. It exactly matched1800/2400/3000/3550/4150/4750/5350/5900/6500 K. This was a verification-tool error with no config effect. Lookup Decimal quantize rounding multiples assertion returned no applicable exact finding. No new reusable learning: use exact unit-aware independent calculations, already covered by verification discipline. Required live candidate validation, reload, installed/live checkers and actual endpoint/midpoint keys all passed; starting temperature restored.
