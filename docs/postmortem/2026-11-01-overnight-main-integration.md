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

## Measurement preparation

A one-off historical catalog reader did not strip quoted YAML skill names, so
trigger-eval correctly refused its missing playwright label before any result
was published. Use the collector's existing frontmatter normalization; frozen
case files remain intact. Missing optional ai-ux-deslop SOURCE.md and a guessed
test filename were read-only lookup misses; use tracked inventory first.

## GitHub wrapper contract

The ergonomic wrapper rejects native gh --json on pr view (exit2); read its
subcommand help before retrying. No PR mutation occurred. Read-only explicit
body/head fields will be verified through supported wrapper output or native gh
as a capability fallback, never by assuming wrapper flag compatibility.

## Regression and fixture follow-up

The first broad run had257passing tests and399passing subtests with3stale
contract failures: unranked verdicts did not recognize retained denial, a
historical717B dedup check assumed no later skills, and exact conditional-body
comparison omitted main's additive sanitizer paragraph. Preserve the original
assertions on pinned historical endpoints and explicitly test the supported
current-main additions. Doctor found two source notes missing required field
labels; normalize them using real pinned facts, never fabricate provenance.

Disposable archive tests initially lacked Git history; attach the allowed
read-only gitfile with explicit source cwd. A premature read of an agent's
incomplete JSON output failed decoding; consume results only after its live
handle is terminal. Broad /tmp inventory hit protected system temp directories;
subsequent reads use exact task artifact paths. None changed source or live state.

## Final regression evidence

Fresh broad259tests/400subtests PASS; targeted historical contracts15/199PASS.
Source metadata normalized: candidate doctor35errors/1warning and zero new
keys vs current main39/1. Same7SyntaxErrors remain in both full collections.
The merge/fixture/lookup failures above are resolved for this task; inherited
full-suite and external-learning limitations remain explicit.

## Evidence review correction

Independent review recomputed the inherited description bytes with the actual
collector: ai-ux165B and Hallmark252B, not the earlier subagent estimates187/376.
Corrected417→183B/58.5estimated tokens in every current report and technique log;
refreshed lean admission costs and body total213,743B. Overall loaded14,399B
and62.90% reduction were unchanged. No incorrect per-skill figures were pushed.

Final wrapper field-selection probe rejected native field names; supported
head/base filters without extra fields verified PR3. Exact body comparison
passed after edit. No further wrapper retries or external mutations needed.
