# Recent title filter snapshot-helper lookup

A read-only search included a guessed Fish helper path that does not exist. Use the repository file inventory to find the real snapshot implementation before preparing the protected refresh.

- Date: 2026-10-07.
- Symptom: rg reported `dot_config/fish/functions/snapshot-codex-config.fish: No such file or directory`.
- Impact: No configuration or session mutation; the executable snapshot helper was found in the same read.
- Cause: An unverified alternate helper path was included in the source lookup.
- Status: Verified workaround; inventory located `scripts/executable_snapshot-codex-config`, whose successful read identified `second_brain.config_snapshot` as the implementation.
- Next steps: Consult reviewed path-discovery guidance, read the actual source, register the report and verify its learning check.

Lookup `nonexistent guessed helper path source inventory` matched `local-discover-paths-before-reads`; its path-ownership reference explicitly states that refresh-config is a Fish function and snapshot-codex-config is an external Python executable. This directly applies. The inventory and executable read exited 0. No new reusable learning: that existing finding already covers this exact path-discovery error and remedy. Register this reviewed hash and run the targeted check.
