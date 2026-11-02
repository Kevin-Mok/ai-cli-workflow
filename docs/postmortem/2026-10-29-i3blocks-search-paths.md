# i3blocks lookup used nonexistent paths

Record a read-only discovery failure and use repository inventory before opening guessed script or test paths.

## Symptom and impact

Two batched rg calls reported missing paths: `scripts/executable_refresh-config*`, `tests/test_now_playing_mpris.py`, and `tests/test_dnd_block.py`. Existing files still returned results. No application state or user data changed.

## Evidence and status

Observed rg exit status 2 for missing operands. Root cause: guessed names instead of using the existing search-agent inventory. Status: resolved with a discovery workaround; no product defect. The search agent identified `test_i3blocks_now_playing_mpris.py`, `test_i3blocks_dnd.py`, and `dot_config/fish/functions/refresh-config.fish`. Reads of those inventoried paths completed with exit status 0.

## Next steps

Lookup query: `rg missing file guessed test path`. Applicable finding: `local-discover-paths-before-reads` in `references/paths-ownership.md`; confirmed by missing operands and successful reads of the inventoried paths. Existing guidance already covers this exact pattern; no new reusable learning. Register this reviewed report with that explicit decision and run the targeted coverage check. Future reads must use the discovered inventory.
