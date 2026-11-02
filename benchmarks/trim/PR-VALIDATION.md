# Refreshed skills review against current main

Review current-main costs, frozen routing and isolated tests before considering
PR3. The previous `410feaa` comparison and visual artifact are historical.

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

## Executed scope

Plain merge `a88eea7e` incorporates main `8662fa3c`,58 commits/294changed files after
410feaa. Five conflicts were resolved explicitly; trimmed core/catalog survive,
relevant upstream changes are carried, repository-creation rule stays verbatim
in mandatory delivery, model/effort settings and CULL.json remain unchanged.

- Merge checkpoint:93 tests/5 subtests PASS.
- New contracts:43 tests/28 subtests PASS, after defining RED. Final focused suite259 tests/400 subtests PASS
  is recorded in pr-validation.json; no whole-suite green claim.
- Shared main 70 tests/17 subtests and candidate 69/11 PASS. Test files evolved;
  counts do not imply identical cases. Main content snapshot uses read-only
  source Git metadata, not OS/home/model isolation.
- Full collection: main 1,464 and candidate 1,546collected, same7 SyntaxErrors,
  exit2. Error paths and log hashes are in JSON; unrelated failures not repaired.
- Doctor: main 39 errors / 1 warning, candidate 35/1, zero new keys; diagnostics are
  not a passing audit. Source notes for both new skills use pinned actual facts.
- Original budget14,399B retained. Strict core 9 KB/150 lines, descriptions400B,
  skills300 lines all pass. Hallmark body17,907B/148 lines; ai-ux6,257B/59 lines.

## Newly gated skills

Hallmark PASS: explicit deterministic theme/scaffold/lint workflow; value 2 and
uniqueness 2 with category-level demand only. No measured usage invented.
AI UX de-slop DENY: duplicate of frontend-design/Impeccable (uniqueness 0).
Retained under the overnight no-delete rule for Kevin's decision; remains in
the catalog and routing cases. No uninstall, disable or re-admission claimed.
[Measured decisions](../../docs/skill-admissions-current-main.json) cite
2–3precedents, costs and change conditions.

## Routing and reproduction

Expanded 54 remains49/54 (90.74%); original 46 remains 42/46 (91.30%), with no
previous correct case lost. Common16keepers12/16→15/16. Prompt labels, original
corpora and scorer are preserved. These lexical results do not prove semantic
routing or real model behavior.

Use scripts/trim-benchmark --ref origin/main --plain and
scripts/trim-benchmark --check --plain from the review branch. Use
scripts/trigger-eval --check --plain for expanded 54; the separate previous46
report enforces the immediately preceding accepted floor. Read
[COMPARISON](COMPARISON.md), [overnight report](OVERNIGHT-REPORT.md) and
[plan](../../plans/skills-efficiency-pr.md) for conflict/rollback/delivery details.

No live configuration or installed catalog activation, provider trials, tokenizer
usage, latency or billing evidence. Revert with a new commit if needed; no rebase,
force-push, main push or other-PR/repo change.
