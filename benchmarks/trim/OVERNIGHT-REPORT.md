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

## Criterion 6: session context diff

[Full context diff](CONTEXT-DIFF.md) · [JSON twin](CONTEXT-DIFF.json). Both tables below use the same static catalog boundary and are copied verbatim from CONTEXT-DIFF.md. Skill “loaded” refers to descriptions, not bodies. See the linked measurement limits; on-demand totals are the complete inventory, not observed session usage.

## Session context totals

| Surface | Before bytes/4 tokens | After bytes/4 tokens | Difference | Change | Real tokenizer before → after |
| --- | ---: | ---: | ---: | ---: | ---: |
| AGENTS policy | 6,050.5 | 2,419.75 | -3,630.75 | -60.01% | 4,990 → 2,027 |
| Skill descriptions | 3,472.75 | 1,180 | -2,292.75 | -66.02% | 2,724 → 941 |
| Always-loaded: AGENTS + descriptions | 9,523.25 | 3,599.75 | -5,923.5 | -62.20% | 7,714 → 2,968 |
| Skill bodies: on-demand inventory | 109,142.5 | 53,435.75 | -55,706.75 | -51.04% | 97,588 → 47,085 |
| Config developer instructions (separate) | 179.25 | 0 | -179.25 | -100.00% | 135 → 0 |
| Existing collector total (includes developer) | 9,702.5 | 3,599.75 | -6,102.75 | -62.90% | 7,849 → 2,968 |

## Skill-by-skill context diff

| Skill | Loaded before | Loaded after | Mark / gate | Description bytes before → after | Description tokens (bytes/4) before → after |
| --- | --- | --- | --- | ---: | ---: |
| adapt | yes | no | removed by cull | 143 → 0 | 35.75 → 0 |
| ai-ux-deslop | yes | yes | added-then-denied; retained, new on main | 165 → 86 | 41.25 → 21.5 |
| ai-workflow-doctor | yes | yes | kept | 200 → 158 | 50 → 39.5 |
| animate | yes | no | removed by cull | 134 → 0 | 33.5 → 0 |
| arrange | yes | no | removed by cull | 151 → 0 | 37.75 → 0 |
| audit | yes | no | removed by cull | 194 → 0 | 48.5 → 0 |
| bolder | yes | no | removed by cull | 132 → 0 | 33 → 0 |
| brand-system-designer | yes | yes | kept | 383 → 383 | 95.75 → 95.75 |
| clarify | yes | no | removed by cull | 124 → 0 | 31 → 0 |
| colorize | yes | no | removed by cull | 130 → 0 | 32.5 → 0 |
| commit-dirty | yes | yes | kept | 354 → 159 | 88.5 → 39.75 |
| commit-plan | yes | no | merged into commit-plan-push | 343 → 0 | 85.75 → 0 |
| commit-plan-push | yes | yes | kept | 394 → 155 | 98.5 → 38.75 |
| commit-session | yes | yes | kept | 434 → 245 | 108.5 → 61.25 |
| context-handoff | no | yes | added on trim branch | 0 → 173 | 0 → 43.25 |
| critique | yes | no | removed by cull | 179 → 0 | 44.75 → 0 |
| delight | yes | no | removed by cull | 143 → 0 | 35.75 → 0 |
| design-taste-frontend | yes | no | removed by cull | 202 → 0 | 50.5 → 0 |
| distill | yes | no | removed by cull | 111 → 0 | 27.75 → 0 |
| extract | yes | no | removed by cull | 180 → 0 | 45 → 0 |
| feedback-memory | yes | yes | kept | 338 → 166 | 84.5 → 41.5 |
| find-skills | yes | no | removed by cull | 303 → 0 | 75.75 → 0 |
| fish-alias | yes | yes | kept | 166 → 132 | 41.5 → 33 |
| frontend-design | yes | yes | kept | 254 → 106 | 63.5 → 26.5 |
| full-output-enforcement | yes | no | removed by cull | 203 → 0 | 50.75 → 0 |
| gh-fix-ci | yes | no | removed by cull | 313 → 0 | 78.25 → 0 |
| grok-cli-handoff | no | yes | added on trim branch | 0 → 123 | 0 → 30.75 |
| hallmark | yes | yes | added (new on main, kept); PASS | 252 → 97 | 63 → 24.25 |
| harden | yes | no | removed by cull | 169 → 0 | 42.25 → 0 |
| high-end-visual-design | yes | no | removed by cull | 234 → 0 | 58.5 → 0 |
| imagegen | yes | no | removed by cull | 328 → 0 | 82 → 0 |
| impeccable | no | yes | added on trim branch | 0 → 92 | 0 → 23 |
| last30days | yes | yes | kept | 246 → 246 | 61.5 → 61.5 |
| lean-instructions | no | yes | added on trim branch | 0 → 69 | 0 → 17.25 |
| leetcode-init | yes | no | removed by cull | 216 → 0 | 54 → 0 |
| long-task-harness | yes | no | merged into context-handoff | 365 → 0 | 91.25 → 0 |
| metaprompt | yes | yes | kept | 222 → 130 | 55.5 → 32.5 |
| metaprompt-alxve | yes | no | removed by cull | 488 → 0 | 122 → 0 |
| metaprompt-run | yes | yes | kept | 221 → 221 | 55.25 → 55.25 |
| minimalist-ui | yes | no | removed by cull | 145 → 0 | 36.25 → 0 |
| morning | yes | yes | kept | 257 → 257 | 64.25 → 64.25 |
| next-tasks | yes | yes | kept | 423 → 127 | 105.75 → 31.75 |
| night | yes | yes | kept | 300 → 148 | 75 → 37 |
| normalize | yes | no | removed by cull | 67 → 0 | 16.75 → 0 |
| onboard | yes | no | removed by cull | 149 → 0 | 37.25 → 0 |
| open-pr | yes | no | removed by cull | 286 → 0 | 71.5 → 0 |
| openai-docs | yes | no | removed by cull | 372 → 0 | 93 → 0 |
| optimize | yes | no | removed by cull | 138 → 0 | 34.5 → 0 |
| overdrive | yes | no | removed by cull | 228 → 0 | 57 → 0 |
| pdf | yes | no | removed by cull | 248 → 0 | 62 → 0 |
| personal-context | yes | yes | kept | 358 → 261 | 89.5 → 65.25 |
| playwright | yes | yes | kept | 209 → 209 | 52.25 → 52.25 |
| playwright-interactive | yes | no | removed by cull | 94 → 0 | 23.5 → 0 |
| polish | yes | no | removed by cull | 123 → 0 | 30.75 → 0 |
| postmortem-memory | yes | yes | kept | 160 → 124 | 40 → 31 |
| quieter | yes | no | removed by cull | 116 → 0 | 29 → 0 |
| readme-recruiter-sync | yes | yes | kept | 236 → 98 | 59 → 24.5 |
| redesign-existing-projects | yes | no | removed by cull | 225 → 0 | 56.25 → 0 |
| screenshot | yes | no | removed by cull | 220 → 0 | 55 → 0 |
| second-brain-session | yes | yes | kept | 278 → 278 | 69.5 → 69.5 |
| shadcn | no | yes | added on trim branch | 0 → 98 | 0 → 24.5 |
| skill-eval | no | yes | added on trim branch | 0 → 107 | 0 → 26.75 |
| smoke-test-capture | yes | yes | kept | 194 → 194 | 48.5 → 48.5 |
| teach-impeccable | yes | no | merged into frontend-design | 148 → 0 | 37 → 0 |
| transcribe | yes | no | removed by cull | 216 → 0 | 54 → 0 |
| typeset | yes | no | removed by cull | 140 → 0 | 35 → 0 |
| ui-ux-pro-max | yes | no | removed by cull | 147 → 0 | 36.75 → 0 |
| vercel-react-best-practices | no | yes | added on trim branch | 0 → 78 | 0 → 19.5 |
