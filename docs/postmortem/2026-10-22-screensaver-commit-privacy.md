# Screensaver commit blocked by machine-specific ledger paths

Remove machine-specific source aliases from the public commit candidate while preserving local incident lookup metadata, then repeat the required privacy gate before delivery.

## Symptom and evidence

The mandatory staged privacy check exited 1 with one `home_path` finding. No commit or push was attempted. The scoped incident ledger additions retained absolute local home aliases, while existing public ledger records use placeholder home paths.

## Lookup and resolution

Read the tracked postmortem-memory procedure and searched `privacy gate home_path public alias`. Public-history and source-path guidance applies: review staged bytes and retain machine-specific metadata outside the public candidate; do not weaken or bypass the gate.

Use the existing `/home/example/linux-config` placeholder for the new staged source aliases. Leave current machine aliases in the local working ledger. This changes source-location metadata only, not incident hashes or findings. Preserve unrelated ledger edits and source records. Verify the exact staged diff and rerun the privacy gate with hooks enabled.

## Status and verification

Privacy repair verified: the exact staged candidate passed the mandatory privacy gate, exit 0. Hooks remain enabled; a final gate will run immediately before commit. No new reusable learning beyond existing public-path sanitation and exact candidate verification. Record this report in the ledger with placeholder public aliases and private local aliases retained only in the working file.
