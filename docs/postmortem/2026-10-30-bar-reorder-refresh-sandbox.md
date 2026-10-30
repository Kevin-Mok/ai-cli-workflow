# Bar reorder refresh sandbox restriction

The bar reorder required applying managed home configuration. This report records the initial sandbox restriction and successful activation.

- Symptom: `fish -ic refresh-config` exited 1 with read-only filesystem errors for Fish, fnm, shortcuts and managed home configuration.
- Impact: Initial refresh could not activate the bar reorder; source changes were preserved.
- Evidence: `/tmp/refresh-config.a75JXWa5.log`; retry `/tmp/refresh-config.MGIGzJvj.log` completed with REFRESH COMPLETE and exit 0.
- Lookup: `refresh-config read-only filesystem` returned general path discovery and environment guidance; restriction evidence identifies sandbox writes as the relevant boundary.
- Root cause: Workspace-only writes exclude managed home configuration and runtime paths.
- Resolution: Approved elevated refresh succeeded, followed by successful i3 configuration validation and one reload. Existing wheel command deprecation warnings remain unrelated.
- Verification: Source and deployed configuration order are redshift, volume, spotify, calendar. Renderer checks initially asserted against incomplete asynchronous startup frames (`[None]`, then `[None, calendar]`); verification must wait for populated blocks. An empty unnamed protocol block persists; excluding it, the populated renderer verified redshift → volume → spotify → calendar. The earlier assertion incorrectly treated that block as a status control.
- Status: Resolved. No helper changes required; no new learning beyond existing sandbox boundary guidance.
- Follow-up: Use appropriate home-write access for live configuration application. Visual placement and click interaction remain manual checks.

- Commit validation: the scheduler regression initially failed because it still expected volume before Redshift. Updated its order and corresponding content indices to the requested order; no scheduler logic changed. Focused suites are rerun before commit.

- Delivery boundary: initial Git object creation was blocked by the read-only `.git` sandbox. Retry requires approved repository-metadata write access. Focused rerun passed 21 status tests and 1 scheduler test.
