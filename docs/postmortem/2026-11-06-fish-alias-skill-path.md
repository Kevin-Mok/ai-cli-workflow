# Fish-alias skill source discovery

This records a diagnostic lookup failure during the delivery-order correction and the source used to complete it.

- Symptom: reading the writing-for-agents skill under engineering failed because the actual package is under productivity.
- Impact: one read failed; no user files were changed by that lookup.
- Lookup: prior reviewed ext-optional-path-discovery and local-discover-paths-before-reads guidance from this conversation applies to guessed skill paths. Used rg --files on the known plugin root before retrying.
- Root cause: assumed category instead of inventory.
- Resolution: read productivity/writing-for-agents/SKILL.md and its mechanics reference; updated canonical fish-alias delivery instructions.
- Status: resolved; admission tests 7 passed, catalog check found 0 missing/stale entries, and independent delivery scenario review passed. README gate pass_no_change.
- Learning: no new guidance; existing path discovery finding covers this repeat. Keep unrelated dirty ledger entries outside this commit.
- Next steps: deploy the revised delivery section, refresh, compare installed content, then commit and push.
