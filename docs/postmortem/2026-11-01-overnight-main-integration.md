# Overnight main integration guard failures

Track merge-time validation failures, preserve imported behavior, and verify
bounded corrections before publishing the checkpoint.

## Symptoms and impact

The staged size guard rejected 23 growing legacy files imported by the plain
merge. The first JSON ledger union also produced duplicate finding IDs and an
alias registered under multiple hashes; the read-only lookup exited 2. A search
agent initially used an unsupported multi-ref rev-parse shape, corrected to
individual refs without changing files. None of these commands changed live
configuration or remote branches.

## Evidence and lookup

2026-11-01: file_size_guard.py exited 1 with exact staged growth diagnostics.
Lookup: postmortem_memory.py search 'file-size merge upstream inherited' failed
ledger validation before retrieval; no prior remedy is claimed applicable.
The merged sizes are reviewed inherited main changes, not new feature growth.
The old exact ceilings predate current main. No wildcard exemption is added.

## Current status and next steps

Resolve ledger entities by stable IDs and hashes with alias movement; preserve
both branches' reviewed additions. Set finite, exact-path size ceilings only for
reviewed imported legacy files and this task's bounded evidence growth. Re-run
size, privacy, README and ledger checks before the merge commit.

## Learning ownership

Active hard rules forbid writing other repos. Canonical external knowledge is
therefore not modified. Register this report in this branch's tracked ledger;
canonical learning synchronization remains a manual follow-up.

## Resolution

The ledger now matches current main exactly: its newer records already contain
the branch's sole report addition. Stable-entity comparison avoids the erroneous
union; targeted existing-report coverage passes with 286 findings and no errors.
Finite exact-path ceilings now cover the imported oversized legacy files.
Privacy check passed for the staged merge; focused regression run is in progress.
Canonical external learning remains unmodified under the explicit scope rule.
