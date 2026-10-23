---
name: lean-instructions
description: Use when adding to AGENTS.md or adding, editing, or removing a skill.
---

# Lean Instructions

Keep instructions discoverable while reducing recurring context. Before adding
to AGENTS.md or creating/editing/removing a skill, apply the techniques below and compare
the affected surface with `scripts/trim-benchmark`. Preserve safety and user
trigger phrases; inspect provenance before editing imported material.

For each technique used, maintain its rule, rationale, measured repo example,
mistakes and checklist here in the same commit as the pass. Keep descriptions
short and this body within the 300-line budget. Do not claim projected savings
as measured results. The pass log is `benchmarks/trim/PROGRESS.md`.

Before scoring an addition, search names, descriptions and jobs in
[vetted skills](references/vetted-skills.md) for overlap. If a live skill already
does the job, DENY with `duplicate of <skill>` or recommend a merge. Compare the
2–3 closest precedents and cite their IDs in the later admission verdict.
Additions/removals update that reference in the same commit. Preserve culled and
merged entries with date, real commit SHA, reason, evidence and survivor; use an
explicit pending SHA until a commit exists. Re-admission needs new evidence that
addresses the original reason. Run `scripts/sync-vetted-skills --check` to report
missing or stale entries, including configured sources and detectable built-ins.
Keep repo configuration and still-installed copies distinct until activation.

## Mandatory admission gate

After the duplicate search above, apply this gate before adding a skill or an
AGENTS.md rule. Duplicate jobs receive `DENY: duplicate of <skill>` or a merge
recommendation, before numerical scoring; re-admissions address the cull reason.

1. Score **value 0–5** from relevant repo/session evidence and **uniqueness 0–2**
   against the surviving jobs (0 = duplicate, 2 = uncovered). Cite the 2–3 closest
   vetted IDs with sanitized evidence and explain why no survivor substitutes.
2. Measure UTF-8 description and body bytes separately. Full token estimates are
   each bytes/4. **Weighted cost = description bytes/4 + body bytes/40** assumes
   a 10% body-load rate, not measured usage. **Score = (2 × value + uniqueness)
   / (weighted cost/100)**. Charge a standing rule's whole text as description.
3. Usually require **value ≥2, uniqueness ≥1, score ≥1**, trigger-first wording,
   current `BUDGETS.json` size limits, a frozen candidate trigger case, routing
   nonregression and source privacy/scope clearance. Use `scripts/trigger-eval
   --check`; the committed intake46 corpus covers every current local skill.
   This lexical proxy is not real model-trigger accuracy. Freeze new cases
   before evaluating future candidates and preserve earlier corpora and floors.
4. Before adding, record dated **PASS/DENY** in `docs/skill-admissions.md`: scores,
   both full token costs, weighted cost, evidence, closest precedents and why no
   survivor substitutes. PASS includes case IDs and size/privacy evidence; DENY
   includes the specific reason and what would change it. Label supplied costs
   as estimates; an approved proposal alone is not source or privacy clearance.
5. Add only on PASS; refresh measured costs when editing an admitted skill.
   Run `python3 -m unittest discover -s tests -p test_skill_admissions.py` and
   `scripts/sync-vetted-skills --check`. Additions/removals update calibration
   and preserve history. Commit the ledger, technique, plan and pass docs together.

Keep exceptions honest: `last30days` remains below cutoff under explicit user
KEEP authority. This gate/log and its standing router are explicitly required;
record their actual cost rather than inflating evidence or inventing savings.

## Admit evidence before spending context — admission pass

**Rule:** Require a recorded, tested PASS before adding context; reject duplicate
jobs first and retain rejected candidates as concrete precedents.

**Why:** Repeatedly priced admissions prevent catalog growth from undoing trims.

**Repo example:** The AGENTS pointer grows from 155 to 196 bytes: **10.25 recurring tokens
added, 0 saved**. This body grows from 10,307 to 13,913 bytes:
**901.5 on-demand tokens added**. Its 69-byte description remains
17.25 tokens. The unchanged intake46 lexical corpus scores 41/46 (89.13%) before
and after the gate; neither added enforcement nor moved references are savings.

**Mistakes:** Scoring renamed duplicates; inflating a borderline keeper's score;
calling assumed body loads measured usage; approving uninspected private files;
relabelling cases to hide routing losses; recording stale costs or vague DENYs.

**Checklist**
- [ ] Search live jobs first; compare and cite 2–3 vetted precedent IDs.
- [ ] Price both full loads and assumed weighted cost; preserve honest exceptions.
- [ ] Check frozen cases, nonregression, privacy/scope and current size budgets.
- [ ] Record dated PASS/DENY before adding; refresh costs and calibration together.
- [ ] Test every local admission and preserve all earlier pass evidence.

## Measure the actual loading boundary — pass 0

**Rule:** Record UTF-8 bytes, lines and bytes/4 estimates before editing. Compare
the same files and categories afterward; count descriptions in recurring context
and bodies only when invoked. Ratchet explicit existing budget exceptions.

**Why:** Separating recurring and on-demand costs prevents misleading savings;
a reproducible CLI and budgets expose growth without guessing from line counts.

**Repo example:** Baseline manual loaded sum: 37,619 bytes (9,404.75 tokens).
`scripts/trim-benchmark --plain` reproduces 37,619 bytes before the required lean
skill addition. Before/after savings from measurement itself: **0 tokens**.
The separate 403,458 body bytes (100,864.5 tokens) are not recurring savings.
The required skill description and AGENTS pointer change loaded cost to 37,756
bytes (9,439 tokens): **34.25 tokens added**, not saved. Record both costs.

**Mistakes:** Treating bytes/4 as tokenizer billing; counting moved bodies as
deleted capabilities; silently replacing the baseline; claiming whole-suite
green from focused tests; recording malformed or incomparable snapshots.

**Checklist**
- [ ] Save the pre-edit inventory and preserve its original baseline.
- [ ] Separate loaded, body and CLI-output metrics; include new router costs.
- [ ] Compare lines, bytes and estimates per item; test snapshot/error paths.
- [ ] Preserve skill paths and trigger branches, not just the aggregate count.
- [ ] Run relevant tests and budgets; record gains, costs and next hypothesis.
- [ ] Update this skill, pass row and plan with the same commit; do not advance
      to another pass when the current commit is blocked.

## Guard trigger quality — trigger baseline

**Rule:** Freeze realistic positive, multi-skill and no-skill cases before
shortening descriptions. Save a before-edit JSON report with `scripts/trigger-eval`;
after editing, rerun with `--baseline` set to that report and `--check`. Reject
any decline from the previous accepted score; retain the original baseline too.

**Why:** Shorter descriptions are useful only while user requests still route.
A fixed corpus and scorer prevent changing the exam to hide a regression.

**Repo example:** The 58-byte lean-instructions description is unchanged before
and after this guard (14.5 estimated tokens, **0 tokens saved**). The initial
50-case lexical baseline is 40/50 (80%). This is measurement infrastructure;
actual description passes must report their own token reduction and score.

**Mistakes:** Comparing only to the original floor after an improvement;
tuning gold labels after scoring; calling lexical accuracy model-trigger quality;
assuming the 38 tested skill names prove preservation of all 60 skills.

**Checklist**
- [ ] Save the current-source score before editing; preserve original cases.
- [ ] Rerun the same cases against the before-edit snapshot; reject any decline.
- [ ] Review uncovered trigger branches semantically; never score skill bodies.
- [ ] Log token change and exact-set accuracy; update this skill with the pass.

## Mine failure evidence before changing rules — measurement input

**Rule:** Screen the recent session window read-only, excluding helpers and
private context before retaining counts. Keep safety rules regardless of matches;
use recurring observed problems to retain controls and move conditional detail.
Add a new control only for a frequent uncovered failure.

**Why:** Evidence reduces speculative standing policy without treating absent
regex matches as proof that a safeguard is useless.

**Repo example:** The 205-byte completion-evidence paragraph remains unchanged
(51.25 estimated tokens before/after, **0 tokens saved**). In 416 eligible
sessions, the scan found 2 unsupported-completion complaint candidates; it
supports retaining the rule. No complaint class met the predeclared frequency
threshold, so no extra standing rule was added by this measurement step.

**Mistakes:** Publishing raw logs; equating failed tool completions with
unexpected incidents; treating intentional RED as a defect; deleting safety
controls because privacy exclusions or regex wording produced zero matches.

**Checklist**
- [ ] Freeze the window/codebook; stream stable bounded files without exports.
- [ ] Report exclusions, candidate counts and uncertainty; paraphrase safely.
- [ ] Map observed failures to retained rules; measure any later move separately.

## Cull by relevance and preserve useful overlap — approved cull

**Rule:** Cull only explicitly approved names after freezing a keep-list routing
slice. Merge unique behavior into survivors, fix callers, and disable external
exposures through repo configuration while preserving upstream files.

**Why:** Rare overlapping catalogs cost every session and increase misfires;
retaining useful contracts avoids losing capabilities with the discarded entry.

**Repo example:** Removing 39 approved local sources eliminates 7,847 description
bytes (1,961.75 estimated recurring tokens gross) and 280,523 body bytes.
Retain last30days, add the context-handoff merge survivor, and measure net costs
with trim-benchmark: before the new calibration-sync requirement, loaded context
moved from 37,756 to 29,543 bytes (**2,053.25 tokens saved**, 21.75%). Keep-list
routing moved from 13/17 to 15/17 on unchanged
cases. External removal estimates are potential configuration savings until
installation cleanup; no live upstream file was deleted.

**Mistakes:** Treating gross bytes as net savings; scoring removed labels as
keeper regressions; silently discarding planning-only behavior; deleting global
installs or private inputs; quoting a private study in public artifacts.

**Checklist**
- [ ] Record explicit authorization, per-name reasons and pre-cull metrics.
- [ ] Freeze the retained-case slice before edits; preserve original gold data.
- [ ] Preserve merge behavior, repair active references and run focused tests.
- [ ] Report per-name bytes, net metrics, routing, manual cleanup and commit state.

## Keep calibration aligned with configuration — cull maintenance

**Rule:** Inventory configured and detectable installed skills, retain removal
history, and fail drift checks when live entries are missing or active entries
are stale. Search jobs and descriptions for duplicates before scoring additions.

**Why:** A gate trained on stale keepers approves duplicates and forgets why an
earlier candidate lost. Persistent culled entries make re-admission reviewable.

**Repo example:** The 39 removed source directories retain their measured cull
reasons in the on-demand reference instead of disappearing. This integrity
check saves **0 tokens** itself; its description/router growth is charged in the
cull benchmark, and the long reference is excluded from recurring context.

**Mistakes:** Deleting cull history; inventing a pending commit's SHA; treating a
disabled repo installer as proof the old host copy is gone; bypassing duplicates
by changing names; treating unmeasured built-ins as scored study candidates.

**Checklist**
- [ ] Inventory local/configured sources and detectable built-ins/installed copies.
- [ ] Search names, descriptions and jobs; cite the closest precedents.
- [ ] Keep dated cull/merge history, reasons, evidence and survivor.
- [ ] Run drift tests and sync check; commit reference and config changes together.

## Admit complementary sources and disclose load costs — intake pass

**Rule:** Import only approved paths after a privacy screen; keep meaningful
triggers, move detailed workflows to references and retain licenses/provenance.
Audit private-source text semantically as well as with the exact-candidate gate.

**Why:** A complementary job earns a bounded recurring cost; pinned on-demand
resources preserve capability without putting all detail in the entry point.

**Repo example:** Four approved skill descriptions total498→406 bytes:23
estimated recurring tokens of avoided intake growth, not existing-catalog
savings. shadcn entry20,669→6,727 bytes saves3,485.5 on-demand entry tokens;
detailed workflows remain linked. Net added descriptions are charged separately
in PROGRESS. Required web runtime assets remain; unused native files are removed.

**Mistakes:** Importing a whole private branch; copying private evaluation notes;
claiming a moved reference disappeared; dropping runtime assets to meet a byte
target; including installed external descriptions in repo-only savings.

**Checklist**
- [ ] Pin allowed paths, screen content and preserve provenance/licenses.
- [ ] Freeze cases using original proposal descriptions before evaluating trims.
- [ ] Keep old cases unchanged; check both keeper and expanded-corpus floors.
- [ ] Update catalog, calibration/history, budgets and measured net costs.
- [ ] Run staged privacy/size checks; commit this intake as its own pass.
