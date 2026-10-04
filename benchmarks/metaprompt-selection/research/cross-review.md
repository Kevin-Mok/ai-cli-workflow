# Independent source cross-review — 2026-10-03

Read-only review of Group A evidence using primary `gh api`, current native
snapshots and independent SHA-256 calculations. No benchmark models were called.
No Group A file was edited.

## Findings

**No eligibility disagreement for either selected Group A package.**

- `wshobson/agents`: exact repository stars **40,179**, nonarchived, MIT;
  retrieved 2026-10-03T22:38:27.084621Z.
  [Aug15 maintenance](https://github.com/wshobson/agents/commit/56a28c6e4d575f1813f777ddfeb956e069aac07a)
  modifies the native package's `scripts/optimize-prompt.py` with a seven-line
  early stop when deterministic variations do not improve the current prompt.
  This changes executable behavior and prevents repeated evaluations, rather
  than only metadata or formatting. It is valid post-introduction package
  maintenance within both windows. The helper is optional for native authoring:
  its mock scores must not be presented as real downstream model evaluation.
- `alirezarezvani/claude-skills`: exact repository stars **27,473**, nonarchived,
  MIT; retrieved 2026-10-03T22:38:27.777741Z. Group A's 27,472 is an earlier
  timestamped observation, not an incorrect threshold finding.
  [June11 maintenance](https://github.com/alirezarezvani/claude-skills/commit/5acece10acd47513bbc7b0c91fe88f54df138adc)
  directly changes `engineering-team/skills/senior-prompt-engineer/SKILL.md`,
  its prompt-pattern reference, `prompt_optimizer.py` and `agent_orchestrator.py`.
  Baseline/eval-first requirements, structural and task-level no-regression
  gates, model-agnostic identifiers and user-supplied pricing are substantive
  runtime/helper changes. This is not a packaging move or introduction.

**One metadata correction is advisable:** Group A's senior record has
`author_is_linked_github_account=true`, which agrees with the current commit API
(`author.login=claude`). Its appended caveat that the author is *not linked* is
inconsistent. Say instead that the recorded linked author does not establish a
human maintainer's identity or ownership. Commit-author counts are not evidence
of an independent human maintenance team.

All **11 wshobson** and **8 senior** local package/license SHA-256 values matched
Group A's manifest. Each package's `SKILL.md` and root MIT license were also
independently fetched at its full pinned commit and matched local bytes.
The packages have distinct native layouts, helper implementations and contracts;
this review found no evidence that one finalist is a repackaged copy of another.
Repository popularity does not establish skill quality.

Workflow breadth is supported: wshobson explicitly covers creation, refinement,
variable-interpolated templates and code-generation templates. Senior combines
creation/meta-prompting, draft optimization, parameterized prompt patterns and
agent/tool prompt design. Its coding coverage is general-purpose agent/tool
prompting, rather than a specialized repository coding-instruction workflow.
Senior's baseline and real task-level eval gates must be supported or marked
unverified; static clarity/token metrics alone cannot satisfy those gates.
Neither package requires a separate paid API key for prompt authoring, although
optional provider examples and actual inner evaluations require available,
properly budgeted tooling.

## Sentry native completion checklist

Use the unmodified Sentry entrypoint as authority. Track artifact completion and
actual workflow evidence separately so an attractive wrapper cannot stand in
for executed evaluation:

1. Eight identifiable, nonempty sections: **Target**, **Success Criteria**,
   **External Context**, **Optimized Prompt**, **Adapter Notes**, **Eval Set**,
   **Optimization Log**, **Residual Risks**. Equivalent numbered labels are
   acceptable; the source does not mandate a particular heading syntax.
2. **Target** names the supplied model/family and relevant prompt surface;
   **Success Criteria** states objective, constraints and concrete failure or
   acceptance conditions. Do not invent provider features or snapshot facts.
3. **External Context** names exact supplied paths and their loaded/referenced/
   out-of-scope status, or explicitly says none applies. A loaded claim needs
   fixture tool-trace evidence.
4. **Optimized Prompt** supplies one explicitly selected usable prompt, or the
   requested reusable variable template. Extract this section deterministically.
   Do not require a code fence the native source never mandates or choose among
   unlabeled variants based on benchmark score.
5. **Adapter Notes** and **Residual Risks** contain task-relevant guidance or an
   explicit applicable-none statement; neither must manufacture concerns.
6. **Eval Set** contains concrete cases and acceptance/expected-output criteria.
   Sentry does **not** prescribe senior's 10–20-case minimum, so do not import it.
7. **Optimization Log** records actual comparisons, selected changes and stop
   reason. For refinement, check baseline and candidates used the same public
   cases; the native workflow asks for 2–4 candidate variants and holdout
   validation. Claims of execution must match budgeted eval traces/results.
   Honest “not executed” is distinct from completed native evaluation.
8. Existing-prompt work includes the native concise diff-style behavioral note.
9. Verify required context-selected reference reads: new/create/template/coding
   authoring uses `core-patterns.md`, `model-family-notes.md` and
   `transformed-examples.md`; existing-prompt refinement uses
   `meta-optimization-loop.md`, `core-patterns.md` and `model-family-notes.md`.
   Do not require every package file to be read on every task.

No native-completion criterion should demand fabricated metric improvements,
SDK execution, unavailable external inputs or an invented prompt wrapper.

## Pre-holdout runner review — 2026-10-03

Read-only inspection of `selection.py`, `selection_mcp.py`,
`selection_runtime.py`, `selection_eval.py` and the referenced core primitives.
This is a review of the pre-freeze development version; the parent may resolve
these findings before freezing. No inference was invoked.

**Findings requiring scoring clarification:**

- The inspected `native_observations` required senior's last ten-case public
  evaluation to pass every case. This is stricter than the native no-regression
  contract: a previously failing case may continue to fail without regressing.
  A local injected record with nine passes of ten was marked incomplete solely
  by `native_public_eval_has_failures`. Primary downstream success and native
  process completion should be reported separately.
- Two successful static helper invocations and a `baseline_path` argument do
  not prove senior's native structural gate. Parse the successful saved metric
  artifacts (helper stdout mixes prose/JSON), pair the earlier baseline artifact
  with the later comparison, and verify revision prompt bytes match the final
  extracted prompt. Require finite numeric `clarity_score >= baseline` and
  `token_count <= baseline * 1.10`.
- For the task-level native gate, pair completed baseline and final-revision
  evaluations with at least ten cases. Match their canonical actual case
  contents, including IDs, inputs and expected values; IDs alone are
  insufficient. Every baseline passing ID must also pass in the revision.
  Unobserved paired evaluation is “unverified”, not an invented perfect-score
  requirement or a downstream task failure.
- `request_usage` currently turns missing request usage into zero tokens and
  first-use averages inherit the zero. The local no-inference reproducer
  confirmed this behavior. Unknown usage must remain unknown; otherwise a
  missing observation can win the cost tie-break. Reconcile durable request
  reservations with observed request records, including interrupted inner evals.

**Checks that looked sound in the inspected version:**

- Every outer inference request obtains the durable `StageBudget` permit before
  forwarding. Compiler public evaluations use the same exact stage label and
  ledger, enforcing ten total compiler requests rather than ten per process;
  solver has a distinct ten-request stage ceiling. Global ledger reservations
  are locked and fsynced. Failed attempts are not refunded.
- Trial IDs are durably reserved before invocation. Interrupted placeholders
  remain terminal records and the ledger prevents automatic replay even if a
  placeholder is missing. Any additional development round needs a distinct
  declared trial ID and remains inside the global 100-trial reservation cap.
- Public evaluator requests contain only each case's ID and input: expected
  values remain local to its checker. Candidate-generated public cases are not
  hidden benchmark answer keys. Their results are recorded separately and their
  request evidence is included in compiler accounting.
- Model-facing filesystem access resolves only within scratch. Native helper
  execution uses the fixed supplied script, constrained arguments and no API
  environment. Coding execution has a pure-function AST/builtin boundary,
  resource limits and only public tests through its MCP action.
- Sentry's coding/new authoring use of transformed-examples is source-faithful:
  its native new-prompt route requires that reference. Sharpening uses the
  meta-optimization loop. No Sentry ten-case minimum or code fence should be
  added. Current section-name substring detection is merely an observable
  approximation; it cannot prove eight substantive nonempty report sections.
- Holdout schedule, source snapshots, checker inputs and runner files are
  hash-frozen before holdout; verification fails on changed frozen inputs.
  No protocol existed at review time, consistent with development still running.
  The report uses held-out rows for rate denominators and all rows for costs.

The initial read attempted the old benchmark root, then an incorrectly guessed
`selectionlib.py` path. Both read commands failed without writes or model calls;
inspection resumed using `rg --files` and the actual `selection_core.py` import.
No runtime or Group A files were changed by this review.
