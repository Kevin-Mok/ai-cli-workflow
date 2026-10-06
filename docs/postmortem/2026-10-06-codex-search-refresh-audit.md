# Codex search final refresh hash audit

The final scoped refresh succeeded but the protected-file comparison detected concurrent source drift. Preserve those updates, inspect refresh scope and session additions, then distinguish concurrent activity from deployment writes.

## Symptom and impact

The final refresh-config returned REFRESH COMPLETE, but the following hash audit failed because four source paths changed after capture: dot_agents/skills/postmortem-memory/sources.json, tasks/lessons.md, docs/postmortem/2026-10-06-backup-recovery-reference-lookups.md and docs/postmortem/2026-10-06-live-backup-swap-alias.md. No automatic rollback or overwrite was performed. The first protected refresh had verified all 38 hashes unchanged.

## Lookup and evidence

Read tracked postmortem-memory and searched `concurrent refresh protected hashes` before retry. Inspect matching reviewed guidance and the current files. The temporary fish shim only permits broad apply on ~/scripts/codex-search and ~/aliases/key_aliases; snapshot/exact config apply remain normal. The four source paths are outside that application and are part of concurrently active backup incident work already present in Git status. Hash equality alone cannot attribute their edits.

## Status and next steps

Verified preservation workaround; original writer attribution remains unconfirmed; preserve all drift. Verify installed bytes, unchanged task-owned source content, survival of session learning records and current target checks. Save byte snapshots before a repeated bounded audit so any further drift can be explained without overwriting shared work. No private corpus output enters this report.

## Resolution, verification, and learning

Reviewed local-stale-preservation-baseline: its guidance applies to long-running shared-work preservation checks and explicitly cautions against attributing writer identity from hashes. Preserve current contents and refresh the byte baseline immediately before the bounded mutation. Our installed executable and all session-specific ledger/lesson additions survived the drift. The repeated actual scoped refresh returned 0/REFRESH COMPLETE, log /tmp/refresh-config-20261006-130510-167971.log, and all 44 fresh byte snapshots (including Codex/Git configs) matched afterward. Installed executable matched source. No stale snapshot was restored. This verifies preservation for the latest bounded refresh, not who wrote the original four paths.

No new learning: local-stale-preservation-baseline already documents this exact attribution boundary and verified workaround. Register the current report hash with that explicit decision and run the targeted check. Current unrelated backup incident edits remain preserved.

## Follow-up dependency-install refresh

The missing-fzf follow-up installed checksum-verified Ubuntu fzf 0.44.1 in ~/.local/bin without sudo. Normal-PATH picker display/selection and all 22 tests succeeded. Its documentation refresh returned REFRESH COMPLETE, but the protected hash audit detected dot_codex/config.toml changed. Source exactly matched live at the first inspection; all other captured source hashes and installed search bytes matched. The helper explicitly snapshots live config, so preserve that source state rather than restore stale content.

A diagnostic then incorrectly asserted that comparing to Git HEAD would isolate the current model change. HEAD is not a valid current-workspace preservation baseline (the file can have historical local changes), so that assertion failed without modifying any source. Replace it with a byte snapshot whose hash is verified against the immediate pre-refresh baseline. Do not attribute the writer or changed keys from HEAD. Existing local-refresh-snapshot-ownership and local-stale-preservation-baseline guidance applies; no new reusable learning.

Retained byte snapshot matches the immediate pre-refresh hash; parsed top-level keys changed from that baseline: model, model_reasoning_effort. This confirms the scoped difference without printing config values. Source/live equality was verified at the first inspection. Subsequent live settings changed again; preserve both current files rather than repeatedly snapshot a moving baseline.

Final boundary: live/source config differences at the last inspection are top-level keys model_reasoning_effort. These current CLI setting changes are unrelated to fzf; no more config remediation or restoration is part of this dependency task. fzf is installed and verified.

## Help/documentation refresh audit

The help follow-up's scoped refresh returned 0/REFRESH COMPLETE and installed
source bytes matched. Its immediate before/after guard compared 46 source
files; only unrelated tests/test_backup_pc.py changed during the interval,
so the aggregate guard exited 1. Log: /tmp/codex-search-help-refresh-27n2hiku.log.
No backup file was written or restored by this task. The shim's broad apply
targets remain the search executable and aliases; the log confirms ordinary
Codex/Git snapshots and shortcut generation. Preserve the current backup test.

Lookup: `concurrent refresh protected hashes` and the reviewed
local-stale-preservation-baseline guidance apply: changed hashes cannot identify
the writer. Do not rerun deployment merely to obtain equality while shared work
is active. Verify the installed help and task-owned source independently.
Refresh itself succeeded; this is an attribution limit in the preservation
audit, not a search/help failure. No new reusable learning; retain the existing
stale-baseline/snapshot-ownership decisions and update this report's reviewed
hash. Remaining limitation: exact backup-test writer is unconfirmed.

## Session commit staging guard

The session-only commit snapshot passed its focused checks, but a broad
working-copy hash guard stopped staging because sources.json changed during
review. The assertion ran before git add/update-index, so the index was not
modified. Preserve the current shared ledger and verify only the attributed
search records against the reviewed candidate; unrelated concurrent additions
must neither enter this commit nor be restored away. The known
local-stale-preservation-baseline guidance applies to this same attribution
boundary. Refresh the candidate's own report hash after this audit update,
then stage its reviewed blobs without requiring unrelated ledger content to
freeze. Writer attribution remains unconfirmed; this is not a search failure.
