# Overnight current-main refresh

Review what changed after main advanced, the measured results and the remaining
manual decisions. Read the evidence before considering merge or live activation.

## Result and delivery

Current main `8662fa3c30da549fbdb20b8477c80e015e7d5236` (58 commits/294 files after
410feaa) is merged with plain merge `a88eea7e` and pushed only to
review/skills-efficiency-20261023. Admission/evidence commit `f8e55fbf` is pushed and PR3 body is updated with the
current numbers; exact remote body comparison passed. The final documentation
receipt follows in this report-only pass. No main push,
force-push, rebase, other-PR/repo write, refresh-config or chezmoi apply.

| Measure | Current main | Candidate |
| --- | ---: | ---: |
| Recurring loaded bytes | 38,810 | 14,399 (−62.90%) |
| Estimated tokens (bytes/4) | 9,702.5 | 3,599.75 |
| Core policy lines / bytes | 361 / 23,512 | 147 / 8,989 |
| Canonical skill descriptions | 13,891B | 4,720B |
| On-demand skill bodies | 436,570B | 213,743B |
| Canonical skills | 61 | 29 |
| Same-label keeper proxy | 12/16 | 15/16 |
| Shared suite | 70 tests/17 subtests | 69 tests/11 subtests |

The prior trimmed endpoint also loaded 14,399 B; the original ceiling, core 9 KB,
150 instruction lines,400 description bytes and300 skill lines remain enforced.
New descriptions 417→183B; commit-dirty 354→159B offsets 195 B net intake/policy
growth. Body bytes are charged separately on invocation; no actual tokenizer,
billing, latency or live catalog savings are claimed.

## Merge conflicts and carry-overs

- dot_codex/AGENTS.md: keep trimmed core; put Chrome previews in core, preserve
  task-title checkpoints, carry design secondary-text/UX-DX-AX rules through
  mandatory system-design routing and stronger incident delivery in the
  mandatory postmortem reference. Repository-creation rule stays verbatim in
  delivery; model/effort source lines unchanged.
- dot_agents/skills/README.md: keep concise survivor catalog, add both new
  entries with explicit admission outcomes. No approved cull restored.
- night/SKILL.md: retain short explicit trigger and carry checkpoint-push,
  goal, blocker and restart procedures. Active request keeps its named branch.
- postmortem-memory/sources.json: newer main already contains the branch-only
  report; take newer main and register this task's incident. The initial naive
  union failed validation and was corrected without losing either branch.
- docs/smoke-tests.md: combine independent appended sections, then refresh
  stale comparison expectations to current main and the 54-case corpus.

Automatically merged relevant skill changes remain: commit-plan-push sanitizer
workflow, fish-alias immediate focused delivery, frontend-design secondary-label
guidance. Finite reviewed size ceilings cover main's imported legacy growth;
new authored files retain 20 KB defaults. Exact generated baseline/JSON outputs
are explicitly exempted. No wildcard safety bypass.

## Newly gated skills

| Skill | Verdict | Description before→after | Body | Reason |
| --- | --- | ---: | ---: | --- |
| ai-ux-deslop | DENY, retained | 165→86B | 6,257B/59 lines | Uniqueness 0; overlaps frontend-design/Impeccable. No-delete rule preserves it for Kevin. |
| hallmark | PASS, trimmed trigger | 252→97B | 17,907B/148 lines | Explicit deterministic theme/scaffold/lint workflow; value 2/uniqueness 2, category evidence only. |

Both bodies are unchanged from main; source notes retain true accepted/pinned
facts and Hallmark's MIT/runtime boundaries. No installer, paid API or external
asset generation/download was run. Nothing newly denied or uncertain was
deleted or silently disabled. Existing CULL.json remains unchanged.

## Verification and limits

- 259 focused tests/400 subtests PASS, exit0. New defining contracts observed
  RED then 43 tests/28 subtests GREEN; historical contract repairs 15/199 PASS.
  After the final metric correction, 26 data tests/17 subtests PASS.
- Expanded frozen 54:49/54 before and after; previous 46 remains 42/46, zero
  prior correct cases lost. Prompts/scorer/thresholds unchanged. Five misses:
  morning translation, three multi-label cases and a no-skill Python bug case.
  These are lexical proxies, not actual model routing.
- Inventory237 sources/0 drift. Doctor main 39 errors / 1 warning→candidate 35/1, no
  new keys; still not a clean audit. Missing public-vault paths and last30days
  provenance remain; brand duplicate warning is inherited.
- Full collection: same7 inherited SyntaxErrors on both main and candidate,
  exit2;1,464 main and1,546 candidate collected. Whole-suite green is not claimed.
- Merge staged privacy and README passed; admission exact staged gates
  PASS; final documentation gates repeat before the report commit.
- Disposable main content uses source Git metadata read-only; not isolation
  from the host environment or installed models. Native title/Plan Mode tools
  unavailable; written ExecPlan used.

See [machine evidence](pr-validation.json), [PR validation](PR-VALIDATION.md),
[comparison](COMPARISON.md), [plan](../../plans/skills-efficiency-pr.md),
[incident](../../docs/postmortem/2026-11-01-overnight-main-integration.md) and
[review](overnight/checks.md). Historical HTML comparison is superseded.
No push has been blocked and no placeholder was substituted, so no new
SANITIZED.md is needed.

## Manual follow-ups

1. Kevin decides whether to consolidate or remove the denied AI UX checklist.
   It remains discoverable on this unapplied source branch.
2. Review PR3 before main merge and separately authorize live activation or
   installed-only cleanup; this run leaves home configuration untouched.
3. Repair the7 inherited collection SyntaxErrors and remaining doctor debt in
   a separately scoped change; review last30days provenance without inventing
   origin facts.
4. Synchronize this task's learning into canonical external incident knowledge
   separately. Active hard rules forbid writing that other repository; this
   branch's ledger is registered and checked, installed copies untouched.

## Proposals for the next run

- Evaluate representative real model routing before further description cuts;
  keep lexical floors as cheap regression signals, not quality proof.
- Add unchanged adjacent-negative and multi-label cases for new skills, then
  investigate scorer limitations without rewriting existing gold labels.
- Revisit denied overlaps only with explicit consolidation authority and
  measured uncovered tasks; preserve provenance, licenses and cull history.
- Fix inherited test collection and doctor findings first so later comparisons
  can broaden their automated scope.

## Completion audit and marker

Independent review verified 16 claims with 0 incorrect; its three publication-only
items have separate root receipts. Final staged gates pass, admission commit
f8e55fbf is pushed, and PR3 body matches the prepared current-main table exactly
(SHA-256 23519a834b74b903b48096560dcaff39fb31de803b61193773e8b4661c555ffa).
Remote main remains `8662fa3c`; PR stays open/unmerged with no CI results reported.

All substantive done criteria are verified. After this report-only commit is
pushed, the final local audit writes the external completion marker at
~/.local/share/culling-night/DONE. That marker is deliberately outside the
public repository. It records final branch/head, baseline and verification;
its absence means completion has not yet been signaled.
