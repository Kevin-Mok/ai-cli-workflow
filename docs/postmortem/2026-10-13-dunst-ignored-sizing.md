# Dunst ignored notification sizing

Replace removed Dunst settings with supported options, then measure a live notification rather than treating deployed source bytes as runtime evidence.

## Symptom and impact
Width changes to legacy geometry were deployed and reported as working, but Dunst 1.9.2 ignored them. User screenshots continued to show the same width. The daemon log states `Setting geometry in section global doesn't exist` and the same for notification_height. Font changes worked; width completion claims were unsupported.

## Lookup and applicability
Searched reviewed memory for `dunst geometry notification_height ignored width`: no applicable sizing remedy; returned stacking guidance applies to audio/history only. Local Dunst 1.9.2 manual declares geometry removed and width supported. Official v1.9.2 draw.c uses width bounds and a maximum height. A real popup executable RED measured 435 x 134 pixels while expecting about 250px width.

## Root cause and current status
Confirmed: editing removed keys and verifying only source/live equality. Replace geometry with width, origin, offset and notification_limit; remove ignored notification_height. User chose large text with natural growing height over a fixed 16:9 crop. Use a generous explicit maximum height, not a fictitious minimum. Fixed and activated; live dimensions verified.

## Next steps
Keep supported settings and verify render-ready window dimensions after future size changes. Unrelated legacy startup/shortcut warnings remain outside scope.

## Runtime measurement readiness
First post-restart measurement ran before Dunst drew its popup and saw its placeholder 2048 x 1 window; assertion failed. Activation and sending succeeded. Retry with a bounded render-readiness poll instead of assuming send completion means the window has resized.

A render-ready popup measured 364 x 167 with width=250: desktop scaling also affects window dimensions, so configured width is logical pixels. Determine the scale before claiming a physical 250px width.

## Resolution and final verification
At Xft.dpi=135, Dunst automatically scales dimensions by 135/96. Supported width=169 rendered a 250 x 270 popup. User then requested at least twice that width; final width=347 renders 501 x 134 for the same Codex sample. Font remains 15.5pt, height grows with content up to 600 logical pixels, origin top-right, offset 30x20 and notification_limit 5. No forced aspect ratio, per user preference.

Final refresh reported REFRESH COMPLETE, activation succeeded, source/live bytes match, render-ready xwininfo measured 501 x 134 and new startup logs contain neither removed sizing warning. Five focused tests pass after observed RED. Earlier claims about legacy geometry widths were incorrect; source deployment alone did not prove runtime sizing.

## Learning and follow-up
Use supported settings for the installed daemon version; observe startup warnings and actual rendered dimensions. Account for DPI scaling and frame pixels, and poll render readiness rather than measuring the initial placeholder window. Register this verified runtime fix in tracked postmortem memory. Preserve unrelated daemon warnings for a separate task.

## Learning validation
First targeted memory check rejected the new finding because symptoms was authored as a string instead of the required list. Converted it to a nonempty list; rerun targeted validation. This authoring correction does not affect the verified runtime sizing fix.
