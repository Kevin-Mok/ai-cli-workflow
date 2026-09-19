# Optional metadata inspection assumed a missing field

- Date: 2026-09-18.
- Symptom: An ad hoc jq inspection failed with `Cannot iterate over null`.
- Impact: No effect on download or integration validation; only optional progress inspection failed.
- Evidence/root cause: The `.info.json` sidecar omitted `requested_formats`, which the inspection attempted to iterate without a default.
- Resolution: Inspect only the required top-level ID, title, and duration fields. The integration checker does not use `requested_formats`.
- Status: Resolved by narrowing the diagnostic query.
- Verification: `jq '{id,title,duration}' /tmp/yt-dl-live-xurxudir/oLOzkH0zVZo.info.json`.
- Follow-up: Treat optional yt-dlp metadata fields as optional in diagnostics.
