# Redshift notification inspection path miss

The initial read assumed refresh-config lived under scripts. Locate its actual fish function before running the configuration refresh.

## Symptom, impact and evidence

During notification implementation, `cat scripts/executable_refresh-config` reported “No such file or directory”. No configuration was modified by that read. Other batched reads succeeded.

## Status and next steps

Resolved: read `dot_config/fish/functions/refresh-config.fish` after the search agent located it. `fish -c refresh-config` exited 0 and printed REFRESH COMPLETE. No product defect established. A test agent also queried a nonexistent Makefile while inspecting runners; enumerating existing files resolved that read-only lookup without affecting tests.

## Memory lookup

Query: `No such file refresh-config script path`. Existing finding `local-discover-paths-before-reads` directly applies: refresh-config is a Fish function, and inspection should inventory paths before reads. The returned guidance was read before retry. No new learning beyond this existing finding; record an explicit no-new-learning ledger decision. Verification scope: read-only inspection plus successful refresh; root cause confirmed as an assumed path.
