# Notis used the bar default instead of the theme

The first label update inherited the bar default, which differed from the neighboring volume and calendar text. Use their shared wallpaper theme color and check click actions independently.

- Symptom: user screenshot shows blue Notis beside lavender volume/date.
- Impact: visual mismatch only; notification state still worked.
- Cause: the previous change removed inline coloring without checking that neighboring scripts override the global default with color7.
- Lookup: postmortem search “i3blocks color wal inherited” found local-terminal-color-test-environment; it concerns NO_COLOR/TERM tests and does not explain this mismatch. Direct source evidence identifies global #cbe4ff versus color7 #d0bce2.
- Status: resolved; helper uses wallpaper color7 with plain fallback. Left-click explicitly unpauses; right-click explicitly pauses.
- Verification: defining RED confirmed color and both click defects; refresh-config completed successfully, deployed/source bytes match, live output uses #d0bce2. Live right/right/left/left yielded true/true/false/false and restored the original state. Focused regression checks cover fallback and queued DND. Screenshot visual recheck remains manual.
