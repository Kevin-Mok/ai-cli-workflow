# Trim task brief

Reduce persistent and on-demand agent context while retaining capabilities.
Follow the saved prompt, the original supplied inputs and the living ExecPlan.

Acceptance: pre-edit baseline; reproducible CLI and budget allowlist; one
technique/commit/benchmark row per pass; notes refine each next pass; skills and
triggers retained; imports untouched; all relevant checks green before commits;
final evidence-reviewer table and saturation evidence; final totals and
recommendations at the top of PROGRESS.md. No pushes, live config syncs, secrets,
model/effort edits or work outside this checkout.

Deliverables: `scripts/trim-benchmark`, `benchmarks/trim/`,
`plans/skills-efficiency.md`, owned source changes, tests and corresponding docs.
Resume: read PROGRESS.md and the plan, verify Git state, then take Next action.

Required technique skill: `dot_agents/skills/lean-instructions/SKILL.md`, short
trigger description, body <=300 lines and one AGENTS routing line. Every pass
updates its rule/rationale/real before-after token example/mistakes/checklist in
the same commit as that pass. Use it on AGENTS additions and skill additions/edits.

New required inputs: `trigger-cases.yaml` (40–60 cases with positive, multi-label
and none expectations), `scripts/trigger-eval`, frozen baseline accuracy and
no-regression reruns after every description pass. Also mine ~60 days of native
sessions read-only into `failure-modes.md` (counts and sanitized paraphrases),
then perform the separate CASD-style rule pass with safety rules retained.

Approved cull amendment: apply the private ranked audit as a separate cull pass.
Keep last30days/lean-instructions; merge the named handoff/commit pairs; narrow
frontend/README triggers and add the Playwright hint. Remove approved local
sources, disable external culls through repo install controls, preserve upstream
files and fix all active references/tests. Publish a neutral removal manifest
with reasons/bytes, keep-list routing comparison and manual follow-ups.

Ready private intake: only roster-approved #39/#33/#12/#46/#38/#55/#37 after
cull; audit each brought-in file, trim shadcn<=8KB and unused Impeccable resources,
merge specific README/source-ledger lines by hand. Do not mutate PRs or push.

Comparison: COMPARISON.md updated every pass commit, original ref3e898a0f to
actualHEAD, reproducible --ref metrics, real commit rows/chart/ranked savings.
Admission: exact mandatory one-line AGENTS gate, scored dated PASS/DENY ledger
in docs/skill-admissions.md, required PASS for each local skill, rejected PR
verdicts, explicit last30days exception, case/budget/privacy/trigger checks.

Latest calibration-sync requirement applies to cull and intake: inventory local,
configured external/install-script sources and detectable built-ins/installed
copies; fail missing/stale reference entries. Preserve dated Culled/MERGED-INTO
history with real SHA once available, reasons/evidence/survivor. Search precedent
names/descriptions/jobs before scoring; duplicate means DENY or merge.
Current instruction: finish and commit cull first; admission-only drafts are
backed up outside the active tree. Git metadata remains read-only; do not bypass.
