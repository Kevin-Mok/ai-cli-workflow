# Refresh stopped on local MIME settings

Refresh must preserve local managed changes before applying source changes.

Symptom: refresh-config stopped; private log reported .config/mimeapps.list changed since last write and EOF. Impact: tv activation pending. Cause: helper only applied, without importing local modifications. Lookup: refresh-config conflict returned broad historical matches, no verified remedy for this exact helper. Resolution in progress: use native re-add (preserves templates and ignores unmanaged targets), retry drift only, stop persistent/fatal failures. Verification pending.

Resolution: import only status entries whose first column is M/A before apply. Broad re-add experimentally reverted pending source changes and created an identical private_mimeapps duplicate; restored session-caused changes and removed identical duplicate. Live corrected refresh exited 0 with REFRESH COMPLETE. Templates remain protected by native re-add. Persistent identical/fatal errors stop.
