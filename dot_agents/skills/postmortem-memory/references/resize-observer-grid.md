# ResizeObserver grid measurement

Use this finding when a responsive grid stacks despite a CSS reserve intended to fit multiple columns. Compare the measured box with the reserve, reproduce with a wide saved panel, then verify actual tile geometry.

## local-resize-observer-grid-content-box

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Four streams stack in one column when a capped wide chat leaves space for two columns.
- Applicability: Responsive grids measured with ResizeObserver contentRect inside padded viewports.
- Diagnostics: Compare contentRect to the CSS space reserve and minimum column width. Assert actual row/column geometry with the widest saved side-panel preference; absence of horizontal overflow also passes for a single column.
- Remedy: Use ResizeObserver content-box width and height directly; do not subtract padding a second time. Preserve minimum embed sizes and persistent iframe hosts.
- Verification: The wide-chat 2x2 geometry assertion failed before the measurement fix, then passed at 1280x900,1440x730,2048x973. No canvas overflow,390px controls and retained video/chat frames passed; typecheck/build/artifact inspection passed.
- Limitations: Controlled Chromium fixture only; no real Twitch playback/audio/login or physical-device verification. Full unit run had six concurrent unrelated quality-selection RED tests; full browser suite was not run by this task. Short or zoomed CSS viewports may still scroll to preserve minimum sizes.
- Source: [Four-stream grid falls back to one column](/home/kevin/coding/twitch-grid/docs/postmortem/2026-10-22-grid-content-box.md) (SHA-256 `6bcdd71fb8175538e2ca6a57e676f5ac5875b0c97ca5144379f5255b63aa1277`).
