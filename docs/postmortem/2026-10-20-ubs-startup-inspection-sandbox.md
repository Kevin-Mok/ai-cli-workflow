# UBS startup inspection sandbox limits

Startup inspection encountered restricted home writes and the user bus. This records the diagnostic limits while the startup configuration is inspected without shell initialization.

- Symptom: `fish -c` initialization attempted fnm symlinks, universal variables and generated aliases outside the writable workspace; `systemctl --user show-environment` could not connect to the bus.
- Impact: initial shortcut inspection was noisy and incomplete; no intentional configuration edits occurred.
- Evidence: read-only filesystem diagnostics and `Failed to connect to bus: Operation not permitted`; command exit 1.
- Lookup: searched `fish read-only systemctl bus sandbox`; `ext-sandbox-loopback` offers only a related restricted-runner pattern, not evidence that loopback caused this failure.
- Cause: normal Fish initialization has write side effects and the restricted runner cannot access the session bus.
- Status: inspection recovered with approved read-only live i3/process access. Both installed and tracked i3 config already launch `ubuntu-start`; this initial inspection did not establish successful wallpaper setup. The subsequent user report and investigation are in [UBS wallpaper startup](2026-10-20-ubs-wallpaper-startup.md).
- Verification: live i3 4.23 reports the installed config path; picom, imwheel and dunst are running. A reboot was not performed. Initial `get_config` parsing expected JSON without requesting raw output; use `i3-msg -r` for JSON pipelines. The pipeline parser error did not alter session state.
- Learning: no new reusable finding; existing permission-boundary guidance applies, with no application defect established.
