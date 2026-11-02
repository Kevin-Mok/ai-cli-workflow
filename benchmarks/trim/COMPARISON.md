# Current-main trim comparison

Compare the fetched current main with the refreshed review branch. Use the same
collector and unchanged common routing prompts, then inspect test scope and limits.

| Measure | Current main `8662fa3c` | Trimmed candidate |
| --- | ---: | ---: |
| Recurring loaded bytes | 38,810 | 14,399 (−62.90%) |
| Estimated tokens (bytes/4) | 9,702.5 | 3,599.75 |
| Core AGENTS lines / bytes | 361 / 23,512 | 147 / 8,989 |
| Description bytes | 13,891 | 4,720 |
| On-demand skill body bytes | 436,570 | 213,743 |
| Canonical skills | 61 | 29 |
| Same-label keeper proxy matches | 12/16 | 15/16 |
| Shared test files | 70 tests / 17 subtests | 69 tests / 11 subtests |

Main is pinned at `8662fa3c30da549fbdb20b8477c80e015e7d5236`, 58 commits/294 files
after `410feaa`. It is an ancestor through plain merge `a88eea7e`. The original
experiment is preserved in BASELINE-original.json and COMPARISON-original.md;
it is not the current PR baseline.

Candidate recurring cost stays 14,399 B, equal to the preceding trimmed endpoint
and unchanged loaded ceiling. Core grows 7 B; description total falls 7 B. New
main descriptions 417→183B save 58.5 estimated tokens against inherited growth;
commit-dirty 354→159B saves 48.75 more. Night's checkpoint-push wording adds 5 B.
These changes offset 195 B of net new policy/skill load. Bodies are on-demand;
no host catalog cleanup or actual model savings are claimed.

## Routing

Expanded 54 frozen before description edits:49/54 before and 49/54 after, with
zero lost correct cases. Original intake 46 remains 42/46; common-label keeper
slice 12/16 main→15/16 candidate. The only excluded original keeper prompt
expects lean-instructions, absent on main. Lexical proxy, not model routing.
Five expanded misses remain: morning/translation, three multi-label prompts,
and a no-skill Python bug prompt. No gold labels/scorer thresholds were changed.

## Reproduction and limits

From repo root, use scripts/trim-benchmark --ref origin/main --plain, then
scripts/trim-benchmark --check --plain. BASELINE.json contains the exact pinned
main collector output. Use scripts/trigger-eval --check --plain for active54
and --cases benchmarks/trim/intake-cases.yaml --baseline
benchmarks/trim/overnight-previous46.json --check for the unchanged prior slice.

[PR validation](PR-VALIDATION.md) and [JSON evidence](pr-validation.json) record
executed commands/results. Full collection has the same7 SyntaxErrors on both
trees. Doctor 35 errors / 1 warning vs main 39/1, no new keys; it is not a clean audit.
Static UTF-8 bytes/4 excludes external installs, wrappers, names/paths, caches and
triggered references. No tokenizer, billing, latency, provider or live activation
measurements. No refresh-config, chezmoi apply, main push or history rewrite.
