---
name: lean-instructions
description: Use when adding to AGENTS.md or adding, editing, or removing a skill.
---

# Lean Instructions

Before AGENTS or skill edits, apply this gate and the techniques below; compare
`scripts/trim-benchmark` results. Preserve safety, triggers and provenance.
Keep each technique's five fields here, descriptions short and body≤300lines.
Commit ledger, technique, PROGRESS, COMPARISON and plan together; stop if commit
is blocked. Estimates are not billing; projections are not measured savings.

## Mandatory admission gate

1. **Duplicate search first:** search names/descriptions/jobs in
   [vetted skills](references/vetted-skills.md). Live overlap gets DENY with
   `duplicate of <skill>` or a merge recommendation. Compare/cite2–3 closest IDs;
   re-admission needs new evidence addressing the cull reason.
2. Score **value0–5** from repo/session evidence, **uniqueness0–2** against
   survivors (0=duplicate,2=uncovered); sanitize evidence and explain no substitute.
   Measure UTF-8 description/body bytes: each full token cost=bytes/4.
   **Weighted cost=description bytes/4+body bytes/40** assumes **unmeasured10% loading**.
   **Score=(2×value+uniqueness)/(weighted cost/100)**. Rule text pays description cost.
3. Usually require **value≥2,uniqueness≥1,score≥1**, trigger-first wording, current
   `BUDGETS.json`, frozen candidate cases, routing nonregression and source
   privacy/scope clearance. Freeze new cases before scoring; retain original
   corpora and previous accepted floors. `scripts/trigger-eval --check` uses
   intake46 covering current locals; lexical routing is not model accuracy.
4. Record dated PASS/DENY in `docs/skill-admissions.md` **before adding**: scores,
   both full token costs, weighted cost, evidence, precedents, no-substitute reason.
   PASS cites cases and size/privacy checks; DENY gives reason/change condition.
   Label supplied costs estimates; proposal approval does not clear source/privacy.
5. Add only on PASS; refresh admission costs on edits. Run `python3 -m unittest
   discover -s tests -p test_skill_admissions.py` and `scripts/sync-vetted-skills --check`.
   Add/remove updates calibration in the same commit. Preserve cull/merge date,
   real SHA (explicit pending until committed), reason/evidence/survivor.
   Distinguish configured sources from still-installed host copies.

`last30days` has explicit user KEEP below cutoff; this gate/log/router are
user-required. Disclose actual costs; keep scores honest and exceptions named.

## Admit evidence before spending context — admission pass

**Rule:** Record/test PASS before additions; reject duplicates first.
**Why:** Priced admissions prevent growth undoing trims.
**Repo example:** Pointer155→196B adds10.25recurring tokens (saves0); body
10,307→13,913B adds901.5on-demand tokens. Description69B=17.25tokens and
intake41/46 (89.13%) unchanged. Enforcement/reference moves are not savings.
**Mistakes:** Renamed duplicates, inflated scores, assumed loads called measured,
uninspected sources, relabelled cases, stale costs or vague DENYs.
**Checklist**
- [ ] Cite2–3 precedents; price full/weighted loads and exceptions.
- [ ] Check cases/privacy/scope/size/nonregression; record verdict first.
- [ ] Test all local admissions; update costs/calibration and preserve evidence.

## Measure the actual loading boundary — pass0

**Rule:** Compare identical per-file bytes/lines/bytes÷4 before/after; descriptions
recur, bodies load on invocation. Separate CLI costs; ratchet explicit budgets.
**Why:** Correct boundaries prevent misleading savings.
**Repo example:** Baseline37,619B=9,404.75tokens; measurement saves0.
`scripts/trim-benchmark --plain` reproduces it. Bodies403,458B=100,864.5tokens
are separate. Required lean/router adds34.25tokens:37,619→37,756B (9,439tokens).
**Mistakes:** Billing claims, moved capabilities called deleted, baseline
replacement, whole-suite claims from focused tests, incomparable snapshots.
**Checklist**
- [ ] Preserve pre-edit inventory/original baseline; include router growth.
- [ ] Compare each item/category, paths/triggers and snapshot/error cases.
- [ ] Test/budget; log gains, next hypothesis and same-commit pass artifacts.

## Guard trigger quality — trigger baseline

**Rule:** Freeze positive/multi/no-skill cases before trims. Save current-source
`scripts/trigger-eval --json`; replay with `--baseline <pre-edit-report> --check`.
Reject any decline even above the original floor; preserve original cases/baseline.
**Why:** A fixed corpus/scorer exposes losses without changing the exam.
**Repo example:** Description58→58B (14.5tokens) saves0; baseline40/50 (80%).
Only38names tested, not all60; actual trims report their own savings.
**Mistakes:** Original-floor-only checks, tuned gold labels, lexical results
called model accuracy or full-catalog preservation.
**Checklist**
- [ ] Save before score; replay unchanged cases/scorer against previous acceptance.
- [ ] Review uncovered branches semantically; score names/descriptions, not bodies.
- [ ] Log token/exact-set deltas; reject regressions and update technique.

## Mine failure evidence before changing rules — measurement input

**Rule:** Screen recent logs read-only; exclude helpers/private context before
counts. Keep safety regardless; add only frequent uncovered controls and use
evidence to retain controls or relocate conditional detail.
**Why:** Absent regex matches do not invalidate safeguards.
**Repo example:** Completion rule205→205B (51.25tokens) saves0. In416sessions,
2unsupported-completion candidates; no class met3sessions/2dates, so no new rule.
**Mistakes:** Raw exports, tool failures called unexpected incidents, intentional
RED called defective, safety removed after zero/private-excluded matches.
**Checklist**
- [ ] Freeze window/codebook; stream bounded stable files without exports.
- [ ] Report exclusions/counts/uncertainty safely; map controls, measure moves separately.

## Cull by relevance and preserve useful overlap — approved cull

**Rule:** Cull approved names after freezing keeper routing; merge unique
behavior/planning-only branches, repair callers, disable external exposure in
repo config and preserve upstream files.
**Why:** Rare overlaps spend recurring context and cause misfires.
**Repo example:**39sources remove7,847description B (1,961.75tokens gross) and
280,523body B. Keep last30days; merge long-task-harness→context-handoff and
commit-plan→commit-plan-push. Before calibration-sync growth,37,756→29,543B
saves2,053.25tokens (21.75%); unchanged keep routing13/17→15/17. External savings
remain potential until activation/cleanup; no live upstream deletion.
**Mistakes:** Gross called net, removed labels called keeper regressions, lost
planning behavior, global/private-input deletion, private-study publication.
**Checklist**
- [ ] Record authority/names/reasons/bytes/pre-metrics; freeze unchanged keeper slice.
- [ ] Preserve merges/gold; repair references and test survivors.
- [ ] Log net count/cost/routing, per-name costs, manual cleanup and commit status.

## Keep calibration aligned with configuration — cull maintenance

**Rule:** Inventory configured/detectable installed skills and built-ins; fail
missing/stale entries. Search jobs before scoring; retain cull/merge history
and require new evidence addressing cull reasons for re-admission.
**Why:** Stale precedents approve duplicates and forget earlier losses.
**Repo example:**39removed sources retain measured reasons in the on-demand
reference; integrity checking saves0tokens. Router growth is charged to culling;
reference bytes are excluded from recurring context.
**Mistakes:** Deleted history, invented SHAs, disabled installer called host
cleanup, renamed duplicates, unmeasured built-ins called scored candidates.
**Checklist**
- [ ] Inventory local/configured/installed sources and detectable built-ins.
- [ ] Cite precedents; retain date/SHA/reason/evidence/survivor and cull rationale.
- [ ] Run drift tests/sync; commit reference and config changes together.

## Admit complementary sources and disclose load costs — intake pass

**Rule:** Import approved paths after semantic privacy review and exact-candidate
gate. Retain triggers, pinned provenance/licenses and required runtime assets;
move detailed workflows to on-demand references.
**Why:** Complementary jobs earn bounded entry costs without losing capability.
**Repo example:** Four descriptions498→406B avoid23recurring tokens of intake
growth. shadcn20,669→6,727B saves3,485.5on-demand entry tokens; workflows stay
linked. PROGRESS charges net additions; required web assets remain, unused
native resources removed. These are not existing-catalog/external savings.
**Mistakes:** Whole-branch/private-note imports, moved text called deleted,
required assets dropped for size, external costs counted locally.
**Checklist**
- [ ] Pin allowed paths; screen private text semantically/exactly; preserve licenses.
- [ ] Freeze original-proposal-description cases before scoring; retain old gold.
- [ ] Check keeper/expanded floors, catalog/history/budgets/net costs and staged gates.
- [ ] Commit intake separately; approval grants no broader import authority.

## Route conditional policy without losing safeguards — CASD pass

**Rule:** Retain failure-backed/safety controls; relocate procedures verbatim
behind mandatory conditional routers. Sparse evidence never deletes safety.
**Why:** Unrelated tasks avoid detail; triggered tasks reach original policy.
**Repo example:** AGENTS23,147→8,982B; loaded30,292→16,127B saves3,541.25recurring
estimated tokens. All91blocks survive once;42move to7refs. Triggered loads cost
separately: static-boundary savings, not measured runtime usage. No complaint
met3sessions/2dates; no speculative rule added.
**Mistakes:** Moved called deleted, always-read reference called conditional,
weakened safety, heading-only preservation checks.
**Checklist**
- [ ] Map failures to controls; retain safety at zero matches.
- [ ] Verify original hashes/one home/routers/source contracts; budget router and triggered costs.

## Compress repeated technique prose — body concision pass

**Rule:** Compress repetition; retain every technique's five fields here and all
gate decisions/safeguards. Required techniques stay in this body.
**Why:** Less on-demand context preserves actionable decisions.
**Repo example:** f0a1cbb0 body15,125→10,897 B saves1057.00
estimated on-demand tokens; description69→69B saves0recurring tokens.
No required technique moved; frozen routing/cases remain unchanged.
**Mistakes:** Dropped actions/safeguards, hidden techniques, on-demand savings
called recurring or billing measurements.
**Checklist**
- [ ] Compare all old technique steps, gate arithmetic and safeguards.
- [ ] Preserve frontmatter/triggers; measure bytes, five fields and relevant gates.
- [ ] Commit measured on-demand delta with0recurring savings and pass artifacts.

## Shorten triggers without adding misfires — description pass

**Rule:** Keep user trigger words and invocation metadata; trim procedure from
descriptions after freezing a current-source routing report.
**Why:** Descriptions recur every session; bodies retain execution detail.
**Repo example:** Eight owned descriptions save1,011B/252.75recurring tokens;
loaded16,127→15,116B. Frozen routing41/46→42/46 and keepers15/17→16/17; no
previously correct case lost. Unchanged bodies preserve behavior.
**Mistakes:** Shortening explicit-only skills into generic false positives;
editing imported sources, changing gold/scorer, or comparing only an old floor.
**Checklist**
- [ ] Save current cases/report; retain trigger branches and invocation controls.
- [ ] Reject losses; review misfires and preserve prior positives.
- [ ] Refresh admission costs/current calibration; record net bytes and score.

## Summarize agent-run checks — CLI output pass

**Rule:** Use undecorated summaries for pipes/agents; retain human TTY output,
all failure signals, JSON/protocol data and explicit full diagnostics.
**Why:** Repeated tool responses spend context without improving decisions.
**Repo example:** sync-vetted check16,243→124B/235→3lines saves4,029.75
estimated output tokens per invocation; recurring instructions save0tokens.
Doctor/README suppress decoration for nonTTY or CODEX_*/CLAUDECODE.
**Mistakes:** Truncated errors/JSON, lost exit status, testing TTY inside a shell
command substitution, or claiming output savings as per-session instruction savings.
**Checklist**
- [ ] Exercise real TTY, agent variables, pipes, plain and NO_COLOR.
- [ ] Preserve full JSON/protocol/errors; expose --details and document it.
- [ ] Measure the same invocation; test actual output and record its boundary.

## Close provenance audit findings with exact source facts — follow-up

**Rule:** Record machine-readable source fields from pinned evidence; preserve
credits, licenses and private-source boundaries while fixing audit findings.
**Why:** A concise entry still needs reproducible lineage when reviewed.
**Repo example:** Four SOURCE notes12,940→15,251B; audit4newerrors→0.
This adds 577.75 on-demand estimated tokens, saves0recurring tokens;
staticloaded15,116B unchanged. Prior35errors/1warning remain outside this pass.
**Mistakes:** Invented upstream origin, private repo locations, punctuated dates,
weakened validators or a whole-audit-clean claim from fixing four findings.
**Checklist**
- [ ] Prove full revision/path/hash; label local accepted snapshots honestly.
- [ ] Preserve source history/notices and validate supported metadata fields.
- [ ] Recompare exact finding keys; test scoped fixes and report inherited debt.
