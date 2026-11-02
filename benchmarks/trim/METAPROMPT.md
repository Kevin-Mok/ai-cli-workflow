# Trim metaprompt pass

This records the task contract and the comparisons used to sharpen the supplied
prompt before implementation. The executable work follows the saved prompt and
ExecPlan; size measurements do not prove model behavior.

## Target
Refine an agent user-task prompt; portable wording, executing in Codex.
Expert gap: separate persistent, on-demand and output costs and ratchet budgets.
Raw material: `.trim-prompt.md`, `.trim-spec.md`, HEAD sources and import history.
Methods: UTF-8 inventory, fixed comparison cases, mechanical moves, regression tests.
Outside judge: reproducible benchmark, policy/link checks and evidence-reviewer.

## Success Criteria
Retain required capabilities and keeper triggers, apply only approved culls,
lower measured costs, preserve provenance and
safety, green relevant checks before each local commit, honest saturation audit.

## External Context
Loaded: supplied prompt/spec, root routing files, `dot_codex/AGENTS.md`,
`.agent/PLANS.md`. Referenced: `dot_agents/skills/README.md`, provenance/install
plans, `tests/test_ai_workflow_contract.py`, `scripts/executable_ai-workflow-doctor`.
Out of scope: live installed skills/config, private stores, notification hooks.

## Optimized Prompt
```prompt
Optimize this worktree's agent context while preserving required capabilities and safety.

Latest additions in `.trim-prompt.md` govern earlier wording. Finish the approved
cull as its own verified commit before starting another pass. Use the private
ranking as input only; never publish its private examples. Cull approved local
sources, merge the named pairs and disable repo-managed external exposures
without deleting upstream files. Preserve last30days. Run the pre-cull trigger
baseline and compare unchanged keeper cases after the cull. Keep per-name
reasons/bytes and net metrics in PROGRESS, not just gross deletion totals.

Keep `lean-instructions/references/vetted-skills.md` aligned with configured and
detectable installed/built-in skills using `scripts/sync-vetted-skills`. Preserve
dated removal/merge history, reason, evidence and survivor; label unknown commit
SHAs pending. Search precedent names/descriptions/jobs for duplicates before
scoring additions. Update the reference in the same pass commit.

After the cull commit, perform only the approved private PR intake using fetched
`private/<branch>` refs. Audit every candidate file first; hand-merge README and
sources.json. Never modify PRs or push. The scored admission gate/ledger is its
own pass; maintain COMPARISON from original ref 3e898a0f39172d7c30a6b0ae0258209cfe2c7f0c
to actual HEAD, separating drafts from committed rows.

Read `.trim-prompt.md`, verify `.trim-spec.md` findings against HEAD, and follow
`plans/skills-efficiency.md`. Record a pre-edit baseline in
`benchmarks/trim/BASELINE.json`: UTF-8 lines, bytes and bytes/4 estimates for
instruction files, each skill description and body, and the repo's always-loaded
surface. Keep session-loaded costs separate from on-demand bodies and CLI output.

Maintain `dot_agents/skills/lean-instructions/SKILL.md` in the same commit as
every pass. For every technique used, record its rule, rationale, a measured repo
before/after example with token savings or added cost, mistakes and a checklist.
Use it when adding to AGENTS.md or adding/editing a skill; keep its description
short, its body in budget and exactly one routing line in AGENTS.md.

Before the next trimming pass, create 40–60 realistic trigger cases in
`benchmarks/trim/trigger-cases.yaml`, including expected skill sets and none.
Add `scripts/trigger-eval` using skill names/descriptions only; a frozen
deterministic offline baseline is acceptable. Record baseline accuracy and rerun
after every description pass; revert any pass that lowers accuracy.

Read native session JSONL from the last ~60 days without modifying or exporting
logs. Publish aggregate recurring failure/correction counts and sanitized generic
examples in `benchmarks/trim/failure-modes.md`. Use a separate CASD-style pass to
retain rules backed by observed failures, move unsupported conditional rules,
and add only frequent uncovered controls. Always retain safety rules. Record
the technique in lean-instructions. Exclude private-context/helper sessions,
never expose identifiers or secrets, and disclose sampling/coverage limitations.

Implement `scripts/trim-benchmark` and a ratcheted size-budget test with explicit
existing exceptions. Iterate one technique per pass and one local Conventional
Commit per pass. Run relevant tests and the benchmark before each commit. Record
old/new values, percent change, skill count, evidence, what worked and the next
hypothesis in `benchmarks/trim/PROGRESS.md`; commit matching plan updates.

Prioritize concise trigger-preserving descriptions, conditional AGENTS procedures
moved to discoverable skills/references, mechanical splits of owned long skills,
shared references for overlapping owned skills, and terse agent-run CLI output.
Verify provenance first: leave imported, external and vendored skills unchanged
and list them, except for the explicitly approved named cull and intake paths.
Preserve other skill names unless a documented merge preserves their capability. Check routed references and representative trigger phrases.

Use deterministic measurements and executable regression checks as independent
judges. Compare at least a minimal edit and a structural candidate against the
same constraints. Define meaningful savings before optimization; continue until
the remaining eligible techniques produce no meaningful reduction without losing
requirements. Record rejected candidates and remaining opportunities honestly.
At that point put final totals and prompt-efficiency recommendations at the top
of PROGRESS.md and obtain an evidence-reviewer audit of the original requirements.

Work only in the existing worktree and branch. Preserve pre-existing dirty work,
especially the supplied `.trim-*` files. Never push, apply chezmoi, run
refresh-config, touch secrets, edit unapproved imported skills, or change model/effort lines
in `dot_codex/config.toml`. Report unavailable native Plan Mode and baseline test
failures accurately; do not claim unexecuted behavioral model evaluations.
```
Saved: `prompts/trim-skill-context.md` (prompt only).
Execution is separately authorized by the user's explicit implement instruction.

## Adapter Notes
Use direct constraints and file references. No model-specific performance claim.
Native Plan Mode/title tool absent from the available catalog; preserve the
planning-before-implementation sequence with a written ExecPlan in Default mode.

## Eval Set
Fixed cases: description keeps a user trigger; moved safety rule remains reachable;
imported long skill is untouched; non-TTY output is plain; oversized new body is
rejected; pre-existing dirty input remains uncommitted. Holdout: multiline YAML,
UTF-8 metrics and interactive output with agent environment variables.
These are repository checks and prepared cases, not paid model-output comparisons.

## Optimization Log
Minimal candidate: add explicit metric and stop criteria to the original prompt.
Structural candidate (selected): separate measurement, iteration and protected
state; reference stable files and distinguish loaded from on-demand savings.
Both were manually compared against the same fixed constraints; structural form
makes accounting and provenance boundaries explicit. No empirical model winner.
Depth tweaks accepted: byte accounting, ownership checks, saturation evidence,
and independent checks. Rejected growth: external installs and model retuning.
Diff: clarified accounting/stop condition; preserved authorized scope and commits.

## Residual Risks
Bytes/4 is approximate. External installed catalogs differ from the repo inventory.
Mechanical checks cannot prove natural-language triggering or agent compliance.
