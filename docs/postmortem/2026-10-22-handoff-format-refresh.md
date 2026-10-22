# Handoff format refresh conflict

This report tracks activation of the requested command-first handoff format. Save the canonical policy, inspect refresh failures without exposing private configuration, and activate only the owned handoff rules when broad apply is blocked.

## Symptom and impact

`fish -ic 'refresh-config'` exited 1 after starting the reviewed chezmoi apply. It reported a stopped apply and private log `/tmp/refresh-config.iQEp4n3M.log`. The canonical AGENTS format, README, smoke checks and append-only feedback were saved; broad activation was not established. No force apply or unrelated reconciliation was attempted.

## Lookup and evidence

Read the canonical postmortem-memory instructions. Searched `refresh-config chezmoi apply local changes conflict`. Applicable guidance: `local-refresh-snapshot-ownership` preserves unrelated ownership and permits exact owned activation; `local-chezmoi-preserved-target-activation` permits a small scoped live merge only after confirming ignore/preserved status. Generic MIME drift guidance is not applicable without a matching MIME error. Canonical source mtime was newer than the installed AGENTS before this task, so no newer-live-source adoption was required.

## Status and next steps

The refresh blocker was an existing local change to `.config/kitty/monitor_font.py`. Chezmoi requested diff/overwrite/skip/quit and reached EOF under non-TTY execution. No unrelated Kitty file was reconciled or forced.

`chezmoi ignored` lists `.codex/AGENTS.md`; `chezmoi source-path ~/.codex/AGENTS.md` reports not managed. Applied the existing preserved-target guidance: copied only the canonical Handoff Format block into the installed instruction file and updated its handoff references. Retained personalized paths and other live policy sections; did not copy the whole sanitized source file.

## Verification and limits

Canonical and installed Handoff Format blocks match exactly. Both specify three visible command/expected-output pairs followed by Verified, Use and Implemented. Source/README/smoke documentation and append-only feedback are aligned. Required broad refresh was attempted and remains blocked by the unrelated Kitty conflict; no full-refresh success is claimed. Activation of this scoped instruction section is verified by reading the installed file; fresh-model compliance remains a documented manual smoke check.

Canonical incident learning/check registration is tracked separately; this report is finalized for hashing.


## Commit privacy preflight

The first authorized commit attempt was rejected by the pre-commit privacy gate with one `home_path` finding. No commit or push occurred. The candidate ledger record used the physical local home alias, unlike the existing published ledger's `/home/example/` convention. Preserve the physical alias in the local working ledger for exact-source checks, but publish only the placeholder alias in the scoped candidate. Do not disable or bypass the hook.

Lookup: searched `privacy gate home_path canonical incident ledger public placeholder` before remediation. Check the actual gate rule and staged record before retrying; record verification after a safe candidate passes.


Publication verification: confirmed the scanner rejects real home usernames and permits the existing neutral placeholder. Replaced only the public candidate alias with `/home/example/`, retaining the physical local alias outside the published candidate. The unmodified privacy gate's exact staged-candidate check exited 0 with PASS. No approval exemption or hook bypass was added. Commit/push will proceed only through the normal hook.
