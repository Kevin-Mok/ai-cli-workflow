# Workspace padding activation restrictions

The workspace-width change required a scoped live update because i3 is excluded from chezmoi. Refresh and reload succeeded with approved host permissions.

- Symptom: restricted refresh exited 1 opening chezmoistate.boltdb read-only; Fish startup also could not write runtime state. Restricted i3 IPC returned Operation not permitted.
- Impact: first activation attempt did not complete. Repository width edits were preserved.
- Evidence: /tmp/refresh-config.tROCCbnU.log; approved refresh /tmp/refresh-config.flQj3Ef1.log printed REFRESH COMPLETE. i3 reload returned success; live bars report widths 204, 155, 204.
- Lookup: searched refresh-config read-only sandbox; execution-environments guidance on scoped approved commands applies. Optional-path probes also found that refresh-config is a Fish function, not an executable script.
- Root cause: sandbox denies home/runtime writes and IPC; .chezmoiignore excludes .config/i3, so refresh alone cannot activate this file.
- Resolution: changed only workspace_min_width in the live config; ran refresh, i3 validation, one reload and read-only IPC verification with approved host permissions.
- Verification: validation exited 0 with existing wheel-command deprecation warnings. Workspace smoke check passed; 17 status-layout tests passed.
- Status: resolved activation; visual pixel spacing and physical clicks not inspected. Minimum widths use logical pixels and scale with DPI; long labels can exceed the minimum.
- Follow-up: none. Existing environment/path guidance covers this incident; no new reusable learning.
