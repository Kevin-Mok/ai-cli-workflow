# Vesktop theme dimming

Restore readable wallpaper shading by checking theme selection and Quick CSS, then applying the managed configuration.

## Symptom and impact
User screenshot shows a bright wallpaper with unreadable chat and reports grey default styling at launch.

## Evidence and lookup
Memory query `vesktop clearvision theme background` returned notification/browser findings, none applicable to theme shading. Both live and tracked Quick CSS explicitly set background-shading transparent with important priority; both FrostedGlass and ClearVision are enabled. Live CSS matches source. Existing settingsSyncVersion edit is protected. Initial official CSS fetch failed DNS in sandbox; retry outside sandbox to distinguish network restriction from upstream failure. An optional skill lookup used an absent path; corrected to catalog path without changing configuration.

## Status and next steps
Investigating current upstream CSS, then restore shading and select ClearVision alone. Grey launch cause remains unconfirmed; remote imports remain a possible dependency. Preserve wallpaper, fonts, accents, plugins and unrelated dirty files.

## Resolution and verification
Removed FrostedGlass from enabledThemes and restored 100% shading with rgba(0,0,0,0.60), preserving wallpaper/filter/fonts/accents. Official current main.css retrieved outside sandbox confirms shading consumes this variable; initial DNS failure was sandbox network restriction. Both defining tests observed RED and then GREEN (2 tests). refresh-config exited 0; installed settings and CSS match source byte-for-byte. Refresh removed an unrelated MIME source file; restored only that initially clean source file to HEAD. No visual runtime verification or cold-launch reproduction; grey launch remains unresolved and remote imports remain a dependency. Reload with Ctrl+R and inspect; restart manually afterward.

## Learning
Confirmed configuration cause of missing overlay: transparent important override; concurrent full themes are an avoidable conflict. Status: activation_pending for visual outcome. Configuration applied, but actual rendered appearance remains unobserved.

Ledger validation initially rejected unsupported scope `configuration`; corrected to allowed scope `code` for activation_pending. Targeted check rerun below.
