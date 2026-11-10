# Manual README sync validation and activation limits

This report records checks that could not complete while making README sync manual-only. Preserve unrelated source ownership and separate code verification from live activation.

## Symptom and impact
Full cull suite has an existing commit-plan-push wording mismatch. Journal fixtures lack second-brain/00 Context/Decisions.md. Hook isolation fixtures are refused by privacy validation. No attempt made to weaken privacy checks. Admission costs initially stale after edits; refreshed them, then shortened the description to meet the 20,000-byte catalog budget.

Refresh in sandbox failed on home/runtime writes. Authorized elevated refresh also failed: chezmoi reports duplicate .config/mimeapps.list owners, dot_config/mimeapps.list and dot_config/private_mimeapps.list. Installed policy activation remains blocked; no unrelated MIME source was deleted.

## Evidence and lookup
Logs: /tmp/refresh-config.nmacNBiO.log and /tmp/refresh-config.ioW7qpuB.log. Lookup: chezmoi inconsistent state; existing local-hidden-prompt-lock and same-day night-refresh-preflight cover partial refresh and conflicting MIME ownership. Those references do not justify overwriting unrelated sources.

## Verification and status
Manual-only assertion passes. Checkpoint 24/24, security 6/6 and commit failure 1/1 pass. Journal and hook-isolation suites remain unverified for the reasons above. No commits or pushes requested.

## Next steps
Resolve MIME source ownership in its owning task, then rerun refresh-config. Repair missing journal/private-policy fixtures separately. No new reusable learning beyond existing source-ownership and fixture-contract guidance.
