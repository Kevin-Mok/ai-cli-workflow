# Skills Efficiency Implementation Plan

This plan reduces recurring agent context without losing skills or safeguards.
Measure first, change one technique at a time, verify and commit each pass, then
stop only after a measured review finds no further safe meaningful reduction.

> Agent execution: use executing-plans inline, with search/tests specialists and
> a final evidence-reviewer. User explicitly authorizes implementation now.

## Purpose And Observable Outcome
Deliver the benchmark/budget tooling, a lean discoverable policy, retained skill
entry points, lower loaded/on-demand costs, terse CLI output, per-pass evidence
and commits, and final totals at the top of `benchmarks/trim/PROGRESS.md`.

## Current Context And Scope
Start HEAD: `3e898a0f39172d7c30a6b0ae0258209cfe2c7f0c`.
Branch: `trim/skills-efficiency-20261022`; stay here. Initial status only untracked
`.trim-prompt.md` and `.trim-spec.md`; neither may be edited or committed.
Baseline was the first repository write: 59 canonical skills, 60 entries including
the duplicate `.agents` source; 37,619 loaded bytes, 403,458 body bytes.
Touch owned policy, owned skills, benchmark, tests and corresponding docs only.
Verify findings rather than treating the older audit as current policy.

## Assumptions
- No native Plan Mode switch or title tool is available. Planning precedes code
  in this document; do not claim an actual mode switch.
- Use stdlib Python and existing pytest/unittest tools; add no dependencies.
- Loaded estimate = root + canonical AGENTS + config developer instructions +
  canonical `dot_agents` descriptions; excludes runtime wrappers/names/paths and
  external installs. Measure all skill entries separately to expose duplicates.
- Meaningful = at least 1% of the relevant surface or 100 estimated tokens per
  candidate pass, with no lost trigger branch, rule, skill or required workflow.
  Body/output wins must not be reported as persistent wins.
- `.trim-spec.md` is an earlier audit, superseded by `.trim-prompt.md` where they
  conflict. Imported sources are protected except for the later explicitly approved
  named cull; its authorization includes playwright-interactive. No model/effort changes, pushes or config syncs.
- Existing unrelated test defects are recorded; relevant checks must pass for
  each commit. Do not silently weaken contract checks to match moved content.

## Ordered Implementation Checklist
- [x] Incorporate the updated `.trim-prompt.md`: trigger-eval baseline and
  log-mined failure evidence are required before the next trimming pass.
- [ ] Prepare a separate trigger-eval measurement milestone: 40–60 realistic
  prompts, expected sets/none, names+descriptions-only deterministic offline
  scorer, frozen baseline and regression gate. Run before description trimming;
  rerun every description pass, and revert any accuracy-lowering pass.
  Capture a current-source JSON report before each description edit; use that
  report as `--baseline PATH` for the after-edit `--check`, retaining the original
  baseline separately. This rejects declines after improvements, not just below
  the original 80% floor. Keep pass scores in PROGRESS.md and the same commit.
- [ ] Prepare log-mined evidence from ~60 days of native JSONL sessions. Screen
  private-context/helper sessions, stream read-only, publish only aggregate
  counts and generic paraphrases in `benchmarks/trim/failure-modes.md`.
- [ ] Use that evidence in a later distinct CASD-style rule pass: retain safety
  rules regardless of observed frequency; retain preventive rules for recurring
  observed failures; move unsupported conditional rules; add only frequent
  uncovered failure controls. Update lean-instructions in each matching commit.
- [x] Inspect status, prompts, canonical instructions and existing provenance.
- [x] Record BASELINE.json before other repository edits; metaprompt pass saved.
- [x] Add the requested `lean-instructions` skill and one-line AGENTS trigger;
  document each used technique's rule, rationale, measured before/after example,
  pitfalls and checklist in that skill in the same commit as every pass.
- [x] Pass 0: add `scripts/trim-benchmark`, inventory/budget regression tests and
  explicit exception allowlist; record pre-existing baseline failures and docs.
- [ ] Pass 1: progressive disclosure of conditional AGENTS procedures into owned
  skills/references; keep core <=150 lines/9KB, map old sections to new homes;
  update contract assertions to real new homes. Preserve compact root shims.
- [ ] Pass 2: scope alignment ceremony; retain assumption/safety rules, use
  relevant searches, task-sized planning, titles and substantive-failure records.
- [ ] Pass 3: strict cheap validation; commit skills block on failed checks;
  remove stale Claude permission entries without widening permissions.
- [ ] Pass 4: terse agent/non-TTY tooling; preserve interactive decoration,
  plain overrides and protocol output. Add defining output tests first.
- [ ] Pass 5: shorten owned skill descriptions while preserving trigger branches;
  compare each old/new description, keep imported descriptions unchanged.
- [ ] Pass 6: mechanical on-demand splits of owned long bodies, if eligible;
  list imported long skills, preserve their bytes and brand duplicate entries.
- [ ] Pass 7+: evaluate shared references/overlap and further owned opportunities;
  retain only meaningful safe wins and document rejected hypotheses.
- [ ] Complete independent audit; final summary/recommendations at PROGRESS top.

## Risks, Edge Cases, And Rollback
Natural-language triggering needs semantic review beyond size tests. Additional
skill routers cost description tokens; measure net loaded change. Preserve exact
safety wording when moving it. Imported sources and the `.agents` duplicate are
read-only. UTF-8 bytes, multiline frontmatter and additions must be counted.
Rollback uses a new reverting commit for the individual pass; never rewrite
history. Baseline is immutable. No refresh means live behavior stays unactivated.

## Verification Evidence
Before each commit: relevant pytest suite, `scripts/trim-benchmark`, budget check,
README gate, staged diff review and privacy gate. Record exact results here or
in PROGRESS. Tests cover metric arithmetic, body/description separation,
frontmatter forms, additions/regressions and CLI plain/TTY semantics.
The requested technique skill is 60th in the canonical catalog; its description
plus one AGENTS route add 137 bytes (34.25 estimated recurring tokens). Initial
budgets include this requested addition; the original baseline is intact.
Before-edit AGENTS was 353 lines/22,750 bytes (the old audit's 341 is stale).
Baseline focused tests: 35 passed, 33 subtests passed, 3 failed (stale feedback
expectation, push-policy string drift, oversized root addendum). Full tests:
collection stopped with six pre-existing hyphenated Python identifiers. Raw
diagnostics remain in `/tmp/trim-baseline-tests-{focused,suite}.log`, uncommitted.
Manual review: compare description trigger branches, rule mapping and referenced
skill names; inspect output in PTY and redirected modes using controlled fixtures.
Review original requirements against HEAD and immutable baseline at completion.

## Progress
Pass 0 implementation ready, including the requested lean-instructions skill;
commit blocked by read-only shared Git metadata.
Intended commit: `test(trim): baseline instruction costs and budgets`.
RED: 5 expected failures because CLI absent; reviewer cases then caught missing
instruction comparisons and malformed snapshots. Latest GREEN: `python3 -m
pytest tests/test_trim_benchmark.py -q` — 8 passed, 9 passing subtests, exit 0.
`scripts/trim-benchmark --check --plain` — 37,756 loaded bytes, budgets PASS,
exit 0. Skill quick_validate passed. Final fresh focused check:
`python3 -m pytest tests/test_trim_benchmark.py tests/test_ai_workflow_doctor.py -q`
— 34 passed, 42 passing subtests, exit 0. `git diff --check` passed. README gate:
`./scripts/executable_readme-recruiter-sync` — pass_no_change, exit 0.
Native mode limitation and inherited unrelated tests remain recorded.
`git add` failed exit 128 creating the shared worktree index.lock; mount evidence
confirms `/home` is read-only. No staging or commit occurred. Next action: after
ordinary Git metadata writes are available, rerun checks, stage/review, privacy
gate and commit pass 0 before progressive disclosure. See the dated incident.

## Review Notes
New required measurement artifacts have independent commit boundaries when Git
metadata becomes writable. No optimization pass is complete without its commit.
Do not bundle trigger scoring or CASD rule changes into the original inventory
commit. Until access returns, preparatory read-only evidence and draft tooling
can advance, but the optimization commit sequence cannot.
Trigger routing is an offline lexical proxy, not a claim of actual model skill
selection. Freeze corpus and scorer before baseline scoring; do not tune to gold
answers. Use exact expected-set accuracy and report multi-label/none results.
Log mining: frequent means >=3 distinct eligible sessions across >=2 dates.
Regex candidate counts are observational evidence, not proof of root cause or
agent compliance; record exclusions, coverage and uncertainty. Never print/copy
raw transcripts, identifiers, private paths, projects, secrets or personal context.
F1 defaults confirmed high/xhigh; recommend trying a lower default on a measured
task set, without editing config. F6 Claude already imports the canonical body.
Playwright-interactive and screenshot were curated imports (install plan/history);
frontend bundle provenance unclear, so preserve it. Brand copies are identical,
but no verified ownership/removal contract authorizes deleting either.
Pass-0 evidence review: `benchmarks/trim/checks.md`. Initial five implementation
findings fixed; later huge-number traceback also reproduced RED and fixed GREEN.
Doctor snapshot before/after retains 38 existing errors/1 warning with unchanged
finding details; catalog advances 59/59 to 60/60. No whole-suite green claim.

## Approved Cull Amendment

Latest user authorization overrides the original no-drop constraint for the
specific ranked cull. Use the private `.skills-relevance.md` as input only; do
not publish its private repository/session examples. Keep last30days and the
new lean-instructions skill. Remove repo-local approved culls, merge
long-task-harness into context-handoff and commit-plan into commit-plan-push,
narrow frontend-design/readme triggers and add Playwright routing guidance.
For external skills change repo install configuration only; never delete global
upstream files. Preserve impeccable and built-in skills. Record each name,
reason and measured bytes saved plus manual follow-ups in PROGRESS.

- [x] Inventory exact local removals, external install controls and callers.
- [x] Record pre-cull trigger score and a frozen keep-list case slice.
- [x] Apply the cull/merges and reference/test repairs as one dedicated pass.
- [ ] Re-run keep-list routing, focused checks, benchmark and privacy gate.
- [ ] Commit this cull separately when normal Git metadata writes are possible.

The original 50-case corpus remains intact: removed-skill cases cannot score
unchanged against a deliberately smaller catalog. Define the keep-list subset
before removal and compare the same subset before/after; report coverage and
accuracy for it alongside the original pre-cull baseline, never retune labels.
Do not claim a committed pass while shared Git metadata remains read-only.

## Intake, Comparison And Admission Amendments

The final private PR roster is now available. Intake follows the cull and must
use only #39, #33, reviewed #12, trimmed #46 (SKILL<=8KB), trimmed #38 swap,
#55 hook and #37 feedback changes; reject #53/#54/#34/#36/#35/#25/#16. Keep
last30days. Do not mutate/comment/merge PRs. Add private as a read-only fetch
remote only when ordinary Git metadata writes permit; inspect each approved
file for personal/private content and run its exact-candidate privacy gate.
Merge README/sources ledger lines by hand, preserve current tests/contracts.

The first public-history audits (all objects and reachable refs) reported1,604
candidates:13 credential,1,462 email,4 home-path,4 provider-token,121 runtime-ID.
These are unadjudicated historical candidates, not a proven public disclosure.
The exact current index privacy gate passes; it excludes all untracked/unstaged
new work and cannot clear incoming files. The host subsequently fetched seven approved private branch refs and disabled
push on that remote. No PR file has been imported. The audits predate those
objects, no historical rewrite is authorized, and no audit is called clean.

- [x] Add trim-benchmark --ref and reproducible COMPARISON generator.
- [ ] Keep COMPARISON.md in every pass commit with actual commit rows, baseline
  metrics, largest skills, routing/tests, deltas, bar chart and ranked techniques.
  With no new commits, label all current changes as working draft.
- [ ] Admission pass: replace the old lean pointer with the exact mandatory
  PASS-only rule (still one line). Document scores/evidence/uniqueness/cost,
  trigger case and size gates in lean-instructions; write dated verdicts in
  docs/skill-admissions.md and test every local skill has PASS. Backfill retained
  candidates and explicit last30days exception; DENY rejected PR skills.
- [ ] Perform approved private intake only after the cull; audit each file,
  expand trigger cases without hiding older results, record net count/tokens.
- [ ] Rebuild final COMPARISON from actual START..HEAD commits after the series.

All amendments are separate pending commit boundaries. The shared metadata
read-only mount still prevents staging/commits; do not fabricate pass SHAs.

## Current Cull Checkpoint (latest instructions govern)

Finish and commit the cull before starting the next pass. The cull now also
includes calibration-sync maintenance, as required by the latest prompt section.
Do not include the frozen admission-scoring ledger/tests/cases or private PR
imports. Eight draft snapshots and their hashes are saved at
`/tmp/trim-post-cull-drafts-lr0ie7as/manifest.json`; calibration reference/tests
were restored for cull maintenance. Restore later shared-file changes as deltas.

- [x] Restore the cull-only AGENTS/lean body before applying the latest sync rule.
- [x] Repair remaining active README and smoke-test claims for retired installers.
- [x] Record the cull net row and all 39 names/reasons/byte savings in PROGRESS.
- [x] Inventory live/configured/built-in skills with sync-vetted-skills; retain
  dated Culled/MERGED-INTO history and explicit pending SHA until committed.
- [x] Pass fresh sync/reference checks, relevant tests, budgets and README gate.
- [ ] Stage only cull scope, inspect staged diff, run exact-candidate privacy gate,
  and commit the cull as its own pass. Shared Git metadata is still read-only.
- [ ] Resolve history entries' pending SHA to the real cull commit, without
  fabricating a self-referential hash or rewriting history.

Fresh pre-sync evidence: 72 tests / 34 subtests passed; Claude linker passed.
AI workflow contracts: 9 passed, 3 inherited failures. After required sync router
and description costs, loaded estimate is 29,632 bytes / 7,408 tokens; 22 local
skills. Keeper routing remains 15/17 against preceding 15/17 snapshot. The
original baseline remains unchanged. No push or live apply/refresh is authorized.

Commit subject: `refactor(skills): cull approved overlaps`. COMPARISON must stay
honest about HEAD remaining original until a real commit can be written. Later
admission scoring, private intake, CASD policy trimming and saturation remain open.

### Atomic cull handoff and resume prompt

Scope: the approved 39-source cull, two merge survivors, narrowed triggers,
external install controls, reference/caller/test/doc repairs and required
benchmark/trigger/calibration evidence. Exclude private input files and deferred
admission-scoring/PR-source changes. Rollback is a new reverting commit once
normal Git writes are available, with calibration state updated in that change.

Paste-ready Cursor prompt:

```text
Continue only the approved cull in plans/skills-efficiency.md. Read the latest
.trim-prompt.md and PROGRESS. Preserve private inputs and frozen admission drafts.
Verify Git metadata writes normally; do not bypass a read-only mount. Run the
focused cull tests, calibration sync check, benchmark, trigger-eval and README
gate. Inspect only the intended staged cull diff, run its exact privacy gate,
and commit refactor(skills): cull approved overlaps. Include matching plan,
technique record, calibration history and COMPARISON. Do not start intake or
another pass before this commit. Never push, refresh-config or apply chezmoi.
```

Automated validation: focused suites listed in pass-evidence.json plus the
calibration suites, bash tests/test_claude_skill_links.sh, trim-benchmark --check,
trigger-eval --check, sync-vetted-skills --check and readme-recruiter-sync.
Manual review: match all 39 removal reasons/bytes, planning-only no-write branch,
long-task acceptance/evidence handoff, narrowed keeper triggers and active doc
links; verify disabled config versus installed-only state. Live apply/timer
cleanup and real model routing are intentionally unverified.

Documentation: README, skill catalog, design guide, smoke checks, trim progress
and comparison, matching historical plan supersession notes and this ExecPlan.
Commit suggestion: refactor(skills): cull approved overlaps. No push authorized.

Fresh doctor review caught and repaired one cull-introduced provenance omission:
context-handoff/SOURCE.md now traces pinned harness bytes and the separately
hashed installed template. Rerun:35 errors/1 warning, zero new finding keys
against the saved baseline. This is not a clean doctor verdict.

Final cull implementation verification:82 tests/217 subtests passed, Claude
linker silent success, benchmark/budgets PASS, trigger15/17 vs previous15/17
PASS, sync plain/JSON228 sources/38 configured ACTIVE/190 installed-only/0drift,
README pass_no_change. Actual command and aggregate evidence:pass-evidence.json.
Read-only working-file privacy preflight:66 files,0 categories; protected inputs
excluded. This does not replace the blocked immutable staged-candidate gate.
Independent reviewer verified implementation/calibration and identified stale
old test counts; those counts and COMPARISON are now refreshed from final logs.
No new pass starts; normal staging/privacy/commit remain outstanding.

Final evidence-review outcome:11 verified/0 incorrect/1 unresolved, recorded in
benchmarks/trim/checks.md. The sole unresolved cull boundary is normal Git
staging, immutable candidate privacy validation and the dedicated commit.
The broader goal still includes later passes and saturation; not complete.

## Pass 1 resumed with writable Git metadata

User restarted with main .git writable access; normal git add succeeded. The
old mount report is not a reliable write probe in this sandbox. Fresh scoped
tests82/217 and budgets PASS. Both remaining routing misses were reconstructed
on original HEAD and are unchanged proxy limitations (compound request loses
second label; translation shares the word morning); rationale is in PROGRESS.
Commit pass1 now after exact staged privacy check; do not add scope.

## Pass 1 delivered; pass 2 intake

Pass1 `refactor(skills): cull approved overlaps` committed as
`bc0360c9a59610469526c45d83efefb82f296382` after82 tests/217 subtests,
unchanged/improved routing, staged scope review and exact privacy PASS.
Direct Git tool invocations work; do not use Python-spawned Git mutations in
this execution environment. No push or live config sync performed.

Pass2 imports only approved paths at the seven fetched refs. Source file privacy
audit104 files found only1home-path candidate; sanitized imports and local
provenance retain required runtime assets. Four imports and Impeccable pin add
5canonical dirs, now27 including required lean; no keeper removed locally.
The new46 frozen cases cover all27 names and score41/46 both before/after
local transforms; original keeper17 slice remains15/17.

- [x] Import and trim approved skills; shadcn entry6,727 bytes with on-demand refs.
- [x] Replace moving Impeccable install with pinned local web source.
- [x] Import size hook with preserved privacy chain, feedback consolidation and
  truthful public-contract fixes; keep feedback.log unchanged.
- [x] Merge README/catalog/routing lines and update calibration/history by hand.
- [ ] Freeze exact legacy size ceilings; run focused suites, budget/inventory,
  keeper/expanded routing, staged size/privacy gates and inspect staged scope.
- [ ] Commit `feat(skills): intake approved complementary workflows` as pass2.
- [ ] Regenerate actual-commit comparison; continue separate admission/CASD passes.

Rollback: revert the individual pass with matching config/calibration/docs; no
live hook/install state is changed. Current source metrics and exact commands
are recorded in pass-evidence and PROGRESS; do not claim full-suite collection
green while inherited sanitized syntax errors remain outside this scope.

Pass2 final focused evidence:192 tests/231 subtests PASS; both previously failing
budget assertions pass after the final freeze. Active routing41/46 (same proposal
floor), keeper15/17 unchanged; inventory233 sources/42ACTIVE/191installed-only/
0drift; trim budgets PASS. README gate pass_no_change. Legacy size ceilings
freeze to reviewed actual bytes; staged size/privacy gates precede commit.

Pass2 delivered as60c6e70f after192 tests/231subtests and exact staged
size/privacy PASS. No push/live apply. COMPARISON now includes actual pass2.
Pass3 scope: mandatory scored gate+27-skill ledger+7DENY records, duplicate and
precedent checks, measured-cost test enforcement, concise artifacts within
20KB authored-file limits. Preserve all current techniques and calibration.

## Pass 3 — admission gate ready

- [x] Require a recorded PASS before skill/rule additions; check duplicates first.
- [x] Backfill27localPASS,1rulePASS and7DENY with measured costs and2precedents.
- [x] Enforce missing/stale costs, score bounds, budget/case/precedent integrity.
- [x] Preserve93ranked calibrations and resolve intake retirement to its real SHA.
- [x] Document use/smoke review; keep ledger19,754B and lean237bodylines.
- [ ] Commit pass3 after selected tests and exact staged privacy/size review.

Loaded30,251→30,292B (+10.25tokens); this required quality gate saves0tokens.
Next pass: log-mined conditional AGENTS routing, with exact-retention map and
regression checks. Rollback: revert this commit with ledger/rule/docs together.

Fresh pass3 selected evidence:198tests/239subtests PASS, routing41/46 unchanged,
budgetPASS, inventory233/0drift, READMEpass_no_change. Commit subject identifies
this milestone; next progress update reports its resulting SHA.

## Pass 3 delivered; pass 4 CASD

Pass3 committed6e9934c7 after198tests/239subtests and exact staged privacy/size
PASS. Real comparison regenerated immediately. No push or live activation.
Pass4 moves conditional policy verbatim to mandatory routed homes, with a
paragraph/hash preservation map and defining RED/GREEN tests; retain safety and
observed completion/copy-paste controls. Original canonical23,147B/357lines;
loaded30,292B. No frequent uncovered complaint warrants a new standing rule.

- [ ] Define retention proof and observe expected RED.
- [ ] Move conditional procedures; keep routers mandatory and standing safety.
- [ ] Validate contract refs, routing, inventory, budgets and scoped suites.
- [ ] Update technique/ledger, actual comparison and exact staged gates; commit4.

Rollback is the individual pass commit; no original text deletion is accepted
without a retained home. Reference files stay below20KB each.

CASD implementation complete: defining2tests observed RED then GREEN;91blocks
retained exactlyonce,42moved,7refs. Canonical8,982B/145lines, staticloaded16,127B
(−3,541.25estimatedtokens from pass3). Checkpoint remains standing; details
conditional. Full active tests/routing/inventory and staged gates precede commit.
Known external publicfixture failure remains scoped; no safety rule deleted.

Fresh CASD selected200tests/330subtests PASS; frozen41/46routing unchanged,
233sources/0inventorydrift, budgetsPASS, READMEpass_no_change. Exact staged
size/privacy clearance precedes the dedicated pass4commit.

Independent review found and resolved2routercoveragegaps: docs/config now
required before commits/pushes; memory includes explicit personal-context and
project/session context. Added CASDassertions pass; finalcore8,982B/145lines.

## Pass 4 delivered; pass 5 body concision

Pass4 committedf0a1cbb0 after200tests/330subtests and staged privacy/sizePASS.
All91original blocks survive; both review-found router gaps fixed. Staticloaded
16,127B/4,031.75tokens; no runtime-load claim. COMPARISON regenerated.

Pass5 owns only lean-instructions body and matching costs/evidence/docs. Preserve
all8existing technique records and mandatory gate; add this technique's measured
example. Description69B unchanged. Body15,125B/256lines before; target<10KB.
- [ ] Compress repeated prose while preserving rule/why/example/mistakes/checklist.
- [ ] Refresh measured admission costs and run relevant checks on frozen source.
- [ ] Record on-demand-only savings and commit pass5; no recurring savings claim.

Pass5 implementation ready: leanbody15,125→10,897B (−1,057on-demandtokens),
177lines;9technique records with all5fields and completegate retained.
Description69B unchanged, recurring0saved. Rootreview confirms required fields
and decisions; measured admission cost refreshed. Focused tests/gates precede
commit. Four intakeprovenance schema findings remain separate follow-up.

Fresh pass5 selected200tests/330subtests PASS; budgetsPASS,41/46routing
unchanged, inventory233/0drift. Exact staged size/privacy gates before commit.

## Pass 5 delivered; pass 6 descriptions

Pass5 committed60f75a4a after200tests/330subtests and staged gatesPASS; lean
body−1,057on-demandtokens, no recurringchange. Actualcomparison regenerated.
Pass6baseline41/46 beforeedits saved description-before.json; selected8owned
descriptions remove1,011B/252.75recurringtokens. Allpreviouspositives retained;
42/46 now, keeper16/17. Rejected draft misfires, no gold/scorer edits.

- [x] Preserve invocationmetadata, triggerbranches and identical8skillbodies.
- [x] Update calibration descriptions/hashes, admissioncosts and technique.
- [x] Retire both descbudget exceptions; loadedceiling15,116B.
- [ ] Run focused tests/routing/inventory, stage privacy/size and commit6.

Next: CLIoutput pass, then structured-provenance findings and final saturation.

Fresh pass6 selected200tests/330subtests PASS; budgetsPASS,42/46routing
vs previous41/46, inventory233/0drift. Staged size/privacy gates before commit.

## Pass 6 delivered; pass 7 terse agent tooling

Pass6 committed5efb06a1 after200tests/330subtests and staged gatesPASS. Eight
owned descriptions save252.75recurringtokens; all prior positives retained,
now42/46. Actualcomparison regenerated.
Pass7 adapts existing README/doctor helpers and sync-vetted: nonTTY/agent
summary and no decoration, full JSON/explicit details, unchanged humanTTY and
protocol output. Defining PTY/pipe tests precede changes. Baseline synccheck
16,243B/235lines (4,060.75estimated outputtokens), not per-session savings.
- [ ] Exercise agent/human/pipe/plain/NO_COLOR, JSON/protocol and failures.
- [ ] Measure outputdelta; update docs/technique/costs and focused tests.
- [ ] Exact staged privacy/size and owncommit; no liveconfiguration activation.

Pass7ready: new4PTY/outputtests observed RED then GREEN; focused43tests/
243subtests PASS, bashsyntaxPASS. Same inventorycheck output−99.24%,4,029.75
estimatedtokens/invocation; staticloaded unchanged. FullJSON/details/errors/
protocol/exitcodes and humanTTY preserved. Roottechniquelog+admissioncost updated;
full focused suite and staged gates precede owncommit.

Fresh pass7 selected230tests/381subtests PASS; budgetsPASS,42/46routing
unchanged, inventory233/0drift, READMEpass_no_change. Staged gates beforecommit.

## Pass 7 delivered; pass 8 provenance normalization

Pass7 committedc24871f2 after230tests/381subtests and stagedgatesPASS. Inventory
check output−99.24%; recurringunchanged. Actualcomparison regenerated.
Pass8 fixes4new doctorSOURCEfield-format errors (39errors/1warning vs35inherited),
preserving source facts/credits/pins/licenses and public privacy boundaries.
Four source notes baseline12940B; source metadata is on demand,0recurring savings.
- [ ] Defining source-validator test RED, then normalize supported keys.
- [ ] Resolve accepted local intake Git blobs and retain true public upstream pins.
- [ ] Doctor0newkeys, scopedtests/routing/inventory; record actualbytes and commit8.

Pass8ready: new sourcevalidator test RED4→GREEN;14contracttests/4subtestsPASS.
FourSOURCErecords12,940→15,251B,0recurring savings; remote pins retained,local
accepted-source checkpoints resolve revision/path/blobhash. Doctor35errors/
1warning,0newkeys; inherited debt remains. Full focused tests and staged gates
precede commit. Next duplicate developerblock removal preserves model/effort.

Fresh pass8 selected231tests/385subtests PASS; budgetsPASS,42/46routing
unchanged, inventory233/0drift, READMEpass_no_change. Staged gates beforecommit.
