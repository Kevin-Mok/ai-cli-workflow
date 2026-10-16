# Metaprompt selection: completed handoff

This historical handoff records the completed selection and its limits. Raw run
records were subsequently removed from public history and retained privately;
offline replay requires their private restoration. Current source verification
has the known [pin mismatch](postmortem/2026-10-16-benchmark-source-pins.md).

**Subsequent installation:** on October 4 the user explicitly requested the
chosen skill replace `$metaprompt`. That separate
[replacement](../plans/replace-metaprompt-with-sentry.md) is now deployed and
verified as Sentry. The benchmark history and earlier no-install boundary below
describe the completed experiment; they do not describe the current installed
default. The frozen experiment is retained privately; public aggregate findings remain.

**Completed on 2026-10-04 after the user resumed. No benchmark work remains.**
The final [report](metaprompt-selection.md) recommends **Sentry prompt-optimizer**
at 14/16, versus Wshobson 13/16 and Senior 11/16. Raw and minimal both score
15/16 at lower cost. The run is closed at **100 attempts and 754 requests**.
Do not restart inference, recover failures, install a skill or change defaults.

This file was originally written for a lower-reasoning continuation after an
Astra/max session, at **2026-10-04 00:09:45 UTC** (October 3 in Toronto).
The appendices preserve that historical 75/80 checkpoint, decisions and traps.
Their pending-action language and archived continuation prompt are superseded
by this completion update. All five remaining flatten trials subsequently passed.

## Goal and Done Criteria

Goal: recommend a specific maintained native metaprompt skill from a popular
GitHub repository, supported by real source receipts, balanced trials, costs,
and candid limitations. The user found the earlier pilot unhelpful and wants
an actual choice, not another inconclusive table.

- DC1: pinned eligible candidates and substantive maintenance receipts.
- DC2: all 80 held-out outcomes, within 100 attempts and 2,000 requests overall.
- DC3: reconciled requests, costs, paired comparisons and declared sensitivities.
- DC4: concrete recommendation, finished report, guide/README/smoke/plan updates.
- DC5: relevant automated checks and truthful broader-test attribution.
- DC6: cleanly paused execution and reproducible continuation, now completed.

## Constraints

- **Do not edit any of the 54 frozen inputs.** Preserve the earlier pilot too.
- All 754 benchmark requests used **gpt-6.1-sol / medium**, regardless of the
  orchestrating assistant's reasoning setting.
- No installs, default changes, worktrees, commits, pushes, retries or refunds.
- Preserve unrelated dirty work. Capture `git status --short` before edits.
- The user resumed the pause; the remaining work finished within its caps.
  There are no unreserved trial attempts left in this run.

## Decisions

- Three eligible skills plus raw/minimal controls; four workflows weighted 25%.
- 20 development attempts + 80 held-out; 10 compiler and 10 solver requests
  maximum per attempt, including nested public evaluations.
- Frozen primary results stay intact. An explicitly post-hoc diagnostic omits
  one ambiguous template case equally from all arms.
- Rank eligible skills by success, then maintenance recency, known mean first-use
  input tokens, then stars. Explain the implementation's eligibility caveat.

## Current State

- Repository `/home/example/linux-config`, branch `main`, HEAD
  `8cc477da2d5f2bb1b80e4ff6648b55e39be31e15`.
- **Complete: 80/80 held-out outcomes; 100/100 attempts; 754/2,000 requests.**
- All 100 records are terminal. No active runner or interrupted outcome remains.
- Development used 169 requests; held-out work used 585. The continuation used
  the final five attempts and 52 additional requests without rerunning anything.
- Sentry is the frozen-rule choice. Its 190 held-out first-use requests compare
  with raw's 32; the run establishes no optimizer benefit over the controls.
- Primary and derivative aggregates agree, with no integrity errors. The
  current installed `$metaprompt` remains Majkey; no installation occurred.

## Evidence and Failed Attempts

- DC1 — **met** — pin/hash audit → 3 finalists, 27 package files; all 54 frozen
  files match → [manifest](../benchmarks/metaprompt-selection/sources.json).
- DC2 — **met** — schedule/records → 80 held-out outcomes, 100 total attempts →
  private run records (not included in the public checkout).
- DC3 — **met** — final reconciliation → 754 observed = 754 charged; all
  requested/served gpt-6.1-sol/medium, HTTP 200, complete usage, no orphan labels,
  every stage at most ten requests →
  private analysis (not included in the public checkout).
- DC4 — **met** — recommendation, costs, sensitivities, source receipts and
  optional installation/rollback published; README/guide/smoke/plan updated →
  [report](metaprompt-selection.md), [plan](../plans/select-maintained-metaprompt-skill.md).
- DC5 — **met** — focused suite → 62 passed; broader suite → 548/550 with two
  unchanged unrelated failures → [validation log](postmortem/2026-10-03-metaprompt-selection-validation.md).
  Final README gate → `pass_no_change`; scoped diff and 39 local-link checks
  passed; both 54/82-file frozen inventories and all 102 analysis evidence hashes
  match.
- DC6 — **met** — parent-only SIGINT originally drained its batch; resumed
  scheduler executed exactly five new trials and exited 0. Both frozen
  inventories still match; no original record was recovered or retried.
- Failures: 6 compiler limits; 4 unrecognized final handoffs; 2 control failures
  on one ambiguous bound template. These are preserved, not retried.

## Artifacts

- [ExecPlan](../plans/select-maintained-metaprompt-skill.md): scope and history.
- [Saved specification](../prompts/select-maintained-metaprompt-skill.md).
- [Analyzer](../scripts/metaprompt-selection-analysis.py): unfrozen derivative.
- [Report](metaprompt-selection.md): final choice, measurements and limitations.
- Primary summary: private `summary.json`; absent from the public checkout.
- Detailed analysis: private `analysis.json`; absent from the public checkout.
- [Postmortem](postmortem/2026-10-03-metaprompt-selection-validation.md): defects and attribution.

## Blockers

None for this task. Two unrelated pre-existing broader test failures remain
documented; no benchmark failure was hidden or repaired after freeze.

## Future work boundary

No experiment implementation step remains. A later audit may regenerate the
report and analysis offline only after restoring the frozen records privately
and reviewing the known source-pin mismatch. Synthetic tests need no raw records.
Installation, default replacement,
new trials, parser repairs in a new harness version, or delivery commits require
a new applicable request. Preserve the frozen artifacts and unrelated dirty work.

Final interpretation traps: Sentry's native section check reads 3/16 because
twelve final headings have rejected suffixes and one compiler exhausted its cap;
Wshobson's native flag is vacuous; Senior's native check reads 9/16. Four handoff
failures have unmeasured downstream quality. Omitting the ambiguous template
equally gives controls 100%, Sentry 85.42%, Wshobson 81.25%, Senior 66.67%, with
unchanged primary scores and charges. All held-out hard-label counts are zero.

---

## Appendix A: authorization and user intent

The original request was to execute `prompts/benchmark-metaprompt-skills.md`.
The user chose Codex subscription quota, initially capped at 50 model calls,
and explicitly requested **6.1 sol medium for testing**. That old pilot exhausted
its allocation and failed to support a useful coding-quality choice.

The user then requested concrete evidence for highly starred GitHub repositories
with shown maintenance, invoked `$metaprompt`, approved the replacement plan,
and said **“Implement the plan.”** The approved replacement allocation is
100 complete trial attempts / 2,000 inference requests, including development
and failures. It supersedes the exhausted pilot for this separate run. Do not
reinterpret the old 50-request pilot cap as the new run's cap, and do not treat
the unused request ceiling as permission to exceed 100 trial attempts.

Latest steering: the current conversation uses Astra/max to use remaining weekly
quota; the work will resume tomorrow with lower reasoning; create a Markdown
file with as much useful context as possible. This handoff fulfills that new
request while leaving the benchmark task unfinished and safely paused.

The user dislikes repeated permission questions. Once they resume, existing
authorization covers the five remaining trials and the planned analysis/docs.
Do not ask again which model, budget, workflows or candidates to use. Do not
install anything or commit/push unless newly authorized.

The context-handoff skill normally requests a brief eight-section artifact.
The user's explicit request for detailed useful context takes precedence over
its 600-word cap; the appendix provides the deeper continuation material.

## Appendix B: exact checkpoint and safe resumption

Working directory for every command below:

```bash
cd /home/example/linux-config
```

Run root:

```text
benchmarks/metaprompt-selection/runs/selection-2026-10-03
```

At the checked pause:

| Item | Observed value |
| --- | ---: |
| Development records | 20 |
| Held-out records | 75 |
| Total trial reservations | 95 |
| Development requests | 169 |
| Held-out requests | 533 |
| Total reserved/observed requests | 702 / 702 |
| Largest compiler/solver label count | 10 |
| Request/record accounting mismatches | 0 |
| Orphan request labels | 0 |
| Requests missing the usage object | 0 |
| Held-out hard-failure labels | 0 |
| Interrupted or active trial records | 0 |

All 702 saved request records specify `gpt-6.1-sol`, reasoning `medium`, and
report served model `gpt-6.1-sol`. The inference requests include nested public
evals; the count is not the number of Codex CLI sessions.

The exact remaining schedule, in order, is:

```text
selection-coding-flatten--sentry-prompt-optimizer
selection-coding-flatten--wshobson-patterns
selection-coding-flatten--minimal
selection-coding-flatten--alireza-senior
selection-coding-flatten--raw
```

All are workflow/family `coding`, case `selection-coding-flatten`, split
`holdout`. None had a trial reservation at the checkpoint.

The old running command was `python3 scripts/metaprompt-selection.py run --jobs 3`,
parent PID **2863595**, unified exec session **16517**. Those identifiers are
historical, not handles to reuse tomorrow. A single **SIGINT to the parent PID
only** interrupted its scheduler. `ThreadPoolExecutor.__exit__` waited for the
already submitted batch to complete. The last Sentry chunks result persisted;
the process then exited **130 / KeyboardInterrupt**, intentionally. No child
process group was killed, no active record was abandoned, and no next batch
was submitted. The parent process was confirmed absent afterward.

Do not treat that intentional exit as an infrastructure failure or reset any
record. Do not use Ctrl-C/process-group termination to reproduce this pause.
If another pause becomes necessary, independently verify process identity and
current control flow before assuming the same draining behavior.

Before resumption, check that no other selection runner exists. A new invocation
loads the frozen schedule and skips every existing trial JSON. Never delete a
trial, request ledger, trial ledger, or protocol file to make the runner retry.
Do not start concurrent copies of the outer runner: both can inspect the same
pending schedule, causing duplicate-reservation incidents.

Read-only/offline checks, then the already-authorized continuation:

```bash
python3 scripts/metaprompt-selection.py verify
python3 scripts/metaprompt-selection.py dry-run
python3 scripts/metaprompt-selection.py run --jobs 3
```

`run` verifies the frozen inventory before inference. It should reserve exactly
five new trials and finish at **100 trial reservations / 80 held-out records**.
Its batches are bounded, and infrastructure/quota incidents stop further
submission. Expected model-level `episode_limit` or `compile_failed` outcomes
remain scored failures and do not automatically stop the schedule.

An `interrupted` JSON is written before invocation and replaced on completion.
During an active process it can mean “in flight.” With no active process it is
unresolved evidence, not permission to replay. The ordinary resume command
skips it. Never silently delete such a marker or exceed either cap to repair it.

Do not rerun development or `recover-development`. Both development rounds
already consumed their allocation; recovery is intentionally closed after
freeze. There are no spare trial attempts after the remaining five.

Checkpoint ledger hashes, useful to identify unintended changes before resume:

```text
requests.json
d0a33d131c01da740d3de46b943a065696c9aaa2b32767f55211b6001e25eba0

trial-ledger.json
a77ecb6b2a794b647f7e423dfdecffcb5e8fa37f81c6eb14f713a87e5ae07428
```

These two ledgers will legitimately change when the five trials run. The protocol
and its frozen input hashes must not change.

## Appendix C: frozen boundary and repository ownership

Current protocol:

```text
benchmarks/metaprompt-selection/runs/selection-2026-10-03/protocol.json
SHA256 5aa62fbbf06a2c5bd559b973d4f02b45f8822d4b60c26e0d23f708c181af6f1a
54 frozen files; all verified at the pause.
```

Historical pilot:

```text
benchmarks/metaprompt/runs/pilot-2026-10-03/protocol.json
SHA256 685a65243d5251a82e1f8b75e54bb564e4b2c7758ae7ec536653ee3cd1bb76eb
82 frozen files; all verified at the pause.
```

The authoritative frozen inventory is `protocol.json -> files`, with paths
relative to that protocol's directory. Do not guess inventory membership from
a filename glob. It includes the new harness, runtime, MCP, native checks,
eval checker, sources, candidates, fixtures, review notes, launch/install
scripts and the five original focused test files.

In particular, do not edit:

```text
benchmarks/metaprompt-selection/selection.py
benchmarks/metaprompt-selection/selection_core.py
benchmarks/metaprompt-selection/selection_runtime.py
benchmarks/metaprompt-selection/selection_mcp.py
benchmarks/metaprompt-selection/selection_eval.py
benchmarks/metaprompt-selection/selection_native.py
benchmarks/metaprompt-selection/sources.json
benchmarks/metaprompt-selection/cases.json
benchmarks/metaprompt-selection/answer-key.json
benchmarks/metaprompt-selection/reference-solutions.json
benchmarks/metaprompt-selection/candidates/**
benchmarks/metaprompt-selection/research/**
scripts/metaprompt-selection.py
scripts/metaprompt-selection-skill.py
tests/test_metaprompt_selection.py
tests/test_metaprompt_selection_runtime.py
tests/test_metaprompt_selection_eval.py
tests/test_metaprompt_selection_native.py
tests/test_metaprompt_selection_install.py
```

The following derivative files were created after freeze and are **not** among
the 54 inputs. They may receive justified, tested analysis fixes, but must not
silently change primary scores or ranking:

```text
scripts/metaprompt-selection-analysis.py
tests/test_metaprompt_selection_analysis.py
```

Docs, this handoff, the saved prompt, and the ExecPlan are outside the frozen
inventory. Update them truthfully. New aggregate artifacts under the run are
derived outputs. Preserve the individual original trial records.

The repository was already very dirty before this implementation. Protected
pre-existing surfaces include the old pilot, its scripts/tests/reports/plans,
`dot_agents/skills/metaprompt/**`, `dot_agents/skills/metaprompt-alxve/**`,
`tests/test_metaprompt_contract.py`, `tests/test_metaprompt_integration.py`,
`docs/phone-ssh-public-ip.md`, phone SSH plans/postmortems, and skill-catalog
changes. Do not stage, discard or bundle these by inference.

Shared dirty files received limited additions from this selection task:

- `README.md`: the maintained-repository selection paragraph/commands.
- `docs/metaprompt-skills.md`: installed-skill wording and link to new selection.
- `docs/smoke-tests.md`: selection verification/runtime/staging/report checks.
- `tasks/lessons.md`: native handoff/checker calibration lesson.

The entire new `benchmarks/metaprompt-selection/` implementation and its new
selection scripts/tests/report/plan/spec belong to this task. No git index or
history mutation has occurred. Any future authorized commit must include matching
plan updates with their implementation; the current task does not authorize one.

No tracked configuration changed in this selection work. `refresh-config` was
therefore not run. Do not invoke it merely for this documentation handoff: it
snapshots live Codex config into the repo and could involve pre-existing work.

## Appendix D: candidates and maintenance evidence

Eligibility was set before results: native prompt-authoring skill, nonarchived
licensed GitHub repository with at least 1,000 stars; create, sharpen, reusable
template and coding-agent support; at least one substantive **post-introduction**
skill/reference/test change within 180 days. Moves, imports, formatting,
branding and unrelated repository activity do not qualify. Copied lineages are
deduplicated. Stars describe the repository, not the individual skill.

| Candidate ID | Native skill / repository | Stars at retrieval | Latest substantive change | Changes 90 / 180 days | License |
| --- | --- | ---: | --- | ---: | --- |
| `wshobson-patterns` | prompt-engineering-patterns / wshobson/agents | 40,179 | 2026-08-15 | 1 / 2 | MIT |
| `alireza-senior` | senior-prompt-engineer / alirezarezvani/claude-skills | 27,472 | 2026-06-11 | 0 / 1 | MIT |
| `sentry-prompt-optimizer` | prompt-optimizer / getsentry/skills | 1,034 | 2026-05-04 | 0 / 2 | Apache-2.0 |

Pins and native paths:

```text
wshobson/agents
156b7a5e7a8b93642628a339ee4039c925b34c7f
plugins/llm-application-dev/skills/prompt-engineering-patterns

alirezarezvani/claude-skills
19392f7a08264ed00486a251f5b2098321771f94
engineering-team/skills/senior-prompt-engineer

getsentry/skills
d18b7aa8ba878354e5c348310230e652f7690f9c
skills/prompt-optimizer
```

Concrete maintenance receipts, not generic “recently pushed” claims:

- Wshobson's [August 15 helper fix](https://github.com/wshobson/agents/commit/56a28c6e4d575f1813f777ddfeb956e069aac07a)
  stops repeated unimproved evaluations; [June 3](https://github.com/wshobson/agents/commit/3ce0342afde674b3a492bdc9271621e953322c11)
  expands native discovery scope.
- Senior's [June 11 change](https://github.com/alirezarezvani/claude-skills/commit/5acece10acd47513bbc7b0c91fe88f54df138adc)
  rewrites baseline/eval-first gates and helper behavior.
- Sentry's [April 24 change](https://github.com/getsentry/skills/commit/6a844a09d7981594d510fc9b2d6b022b4ed2e246)
  adds instruction-layer/tool-schema guidance;
  [May 4](https://github.com/getsentry/skills/commit/c190d369bcbaa6cfdd95e9edfdba040506b4db76)
  adds external-context and output/specification guidance.

Exact UTC retrieval timestamps, full file inventories/SHA256s, licenses and
independent cross-review are already in `sources.json`, `research/group-a.*`,
`research/group-b.*` and `research/cross-review.md`. They were checked using
primary GitHub APIs and actual diffs. A later audit saw 27,473 senior-repo stars;
do not erase the original timestamped 27,472 observation. A linked commit author
named `claude` does not prove independent human ownership.

Larger alternatives were explicitly researched and excluded: awesome-copilot
(39,667: introduction-only and no template variables), Davila templates
(32,353: no qualifying follow-up), Antigravity (47,224: scope/lineage/maintenance
issues), Jeffallan (11,719: only branding/backlinks inside the window), NeoLab
(1,742: stale substantive change), developer-kit (353: below threshold), and
Senior's marketing toolkit (lacks current coding-agent authoring scope).
The manifest contains package-specific reasons. Do not re-audit the whole market
tomorrow or change eligibility because a preferred candidate scores worse.

The installed `$metaprompt` remains the earlier **Majkey** adaptation. This run
does not replace it. Its low-star upstream and the older Talki comparison are
not finalists under this run's popularity requirement.

## Appendix E: experiment design and what the scores mean

- Five arms, same selected case IDs across arms. Schedule seed `20261003`.
- 26 fresh synthetic cases exist: 2 development and 24 held-out. The frozen
  schedule uses 16 distinct held-out cases, four per workflow, for each arm.
- Two development rounds each run the same 2 development cases per arm with
  distinct IDs; round two uses suffix `--d2`. Both rounds remain charged.
- Skill arms compile, then solve in a fresh fixture. Raw/minimal arms only solve.
  This measures a complete workflow with extra authoring compute, not an isolated
  causal effect of skill text under equal total computation.
- Noncoding grading is strict typed JSON equality. Extra prose/fences/fields and
  changed array order fail. Public requests specify keys/types/copy boundaries.
- Templates compile without bound values and must preserve exact `{{variables}}`.
  The same bindings are then applied once to all arms.
- Coding requires actual target/public-test reads, pre-fix public RED, target-only
  edit, public GREEN, stopping, correct final source and hidden assertions.
- Pure Python is executed under an AST allowlist and CPU/memory limits. Public
  `run_tests` uses the same restricted scoring boundary. No arbitrary shell,
  host path access, network, deployment or messages are exposed to the models.
- Hidden keys/reference answers never enter either model stage. Supplied facts
  are synthetic packets; local source IDs are not internet citations.
- Public native evals are author-written 1–20-case batches in one fresh no-tools
  context. Expected values stay in the checker. They are charged to the compiler
  allowance, are not independent held-out trials, and cannot prove real coding
  tool execution. A native report calling these “holdouts” does not make them
  the benchmark's private held-out cases.
- Usage includes every inference request, even aborted stages. Missing usage is
  unknown, not zero. Subscription token counts are not fabricated dollar prices.
- Compiler+solver cost is first use; solver-only cost is observed execution.
  Repeated reuse savings were not experimentally measured. Latency sums stage
  wall time, including nested waits, not parallel elapsed run time.

The frozen settings contain stale summary fields `allocation.total=90` and
`allocation.development_per_arm=2`. The actual schedule is authoritative:
**20 development + 80 held-out = 100**. `total_planned_trials` and recorded
second-round scheduling reflect the expansion. Preserve the frozen bytes and
disclose the stale summary instead of “fixing” the protocol.

Primary ranking uses equal workflow success and complete paired coverage.
An `episode_limit` or `compile_failed` is a terminal observed failure. An
infrastructure/interrupted/quota-truncated result prevents a complete default
recommendation. Exact score ties use latest substantive maintenance, then lower
known mean first-use input tokens, then stars. Do not choose the highest-star
repo in preference to a higher-scoring eligible skill.

This suite measures constrained factual delivery and small pure-Python repairs.
It does not measure prose taste, persuasion, production repositories, frontend
work, deployment quality or general prompt-engineering superiority. A small,
selected, unreplicated sample cannot establish universal superiority.

## Appendix F: known defects and necessary interpretation

### F1. Four final handoffs were not recognized

These have frozen `compile_failed/no_unambiguous_final_prompt` outcomes with no
solver call. They are **unmeasured downstream quality**, not observed incorrect
downstream answers. Preserve their scores and all compiler charges.

| Trial | Observed presentation missed by the parser | Separate native-process caveat |
| --- | --- | --- |
| `selection-sharpen-extraction-quotes--alireza-senior` | `FINAL PROMPT — candidate, structural gate failed`, prompt fence, second metric fence, `Saved as` line | Actual static clarity regression 90 → 85 |
| `selection-template-conflict--sentry-prompt-optimizer` | `Optimized Prompt — FINAL HANDOFF` heading; artifact link on following line | Native section matcher also misses the heading suffix; human-readable report has all eight sections |
| `selection-coding-headers--alireza-senior` | `FINAL PROMPT — prompts/final_prompt.txt` followed by underline and prompt text | Same-case baseline/final eval pair not observed |
| `selection-coding-chunks--alireza-senior` | Same em-dash final artifact form, with backticks | Same-case baseline/final eval pair not observed |

Artifacts and final messages are in the respective JSONs under `RUN/trials/`.
The final report should link representative records. A written 10/10 or 12/12
claim does not replace actual evaluation-pair evidence. Do not rerun these
solvers, change the parser, relabel them as successes, or delete their records.
If useful, bound their possible influence by showing how many unmeasured
outcomes could change a conclusion; do not invent those outcomes.

Six other current native failures exhausted the ten-request compiler allowance:
Wshobson on sharpen-extraction-quotes, coding-pairs and coding-chunks; Senior on
sharpen-summary-corrections and template-filter; Sentry on create-writing-draft.
They are not infrastructure failures. The frozen report must distinguish them
from completed wrong answers and from the four adapter failures.

### F2. One rendered raw template has an ambiguous boundary

`selection-template-draft` places `{{message_data}}. Keys ...` inline. Multiline
substitution makes its final `Fact: funding unknown` line run into the following
period/instructions. The public contract says to copy the remainder of each
Fact line verbatim, while the key expects only `funding unknown`.

Raw copied the instructions into the final fact; minimal retained the extra
period. Both failed primary grading. All three native arms passed, but this is
not clean evidence that they have better task ability: the control's rendered
data boundary is ambiguous.

The derivative analyzer includes
`sensitivities.omit_ambiguous_draft_binding`. It omits this exact case from every
arm, keeps each workflow at 25%, changes no primary result/ranking, consumes
zero inference, and does not reduce charged costs. It is explicitly **post hoc**.
Its defining test first failed for the missing function, then passed; input
records are checked unchanged. Report primary and sensitivity comparisons.

### F3. “Hard failure” is an overbroad eligibility bucket

The inherited scorer marks Markdown-fenced code `output_format` and any AST
allowlist rejection `unsafe_code`. Some rejected constructs can be harmless
pure Python. The selector excludes an entire candidate arm for any top-level
hard label, broader than the protocol's “serious authorization failures” phrase.
Actual denied fixture-path/target attempts use `unauthorized_tool_access`.
None of those labels proves a completed unauthorized host action.

Artifact-only `fixture_score` labels do not independently propagate to arm
eligibility; solver-output labels do. Preserve the frozen rule and explain this
strict contract/execution-boundary filter. At the checkpoint there are **zero
held-out hard labels**, so it has not affected eligibility. Recheck after the
last five trials. Never describe a format/allowlist failure as a security incident.

### F4. Native completion is not a common quality scale

Wshobson has no mandatory machine-checked native gates. Its checker returns
`complete=true` even for compiler limits, so that flag is vacuous for completion
comparison. Display “no mandatory gates” or explain the recorded value; report
usable final handoffs separately. Its optional optimizer contains demo/mock
provider behavior and was not executed as evidence of quality.

Senior requires the real reviewed static analyzer, no clarity regression,
token growth ≤10%, and the same 10–20 public cases without losing previously
passing cases. An unchanged 9/10 can pass its native no-regression rule; do not
invent an all-cases-perfect requirement. The wrapper fixes allowed arguments and
confines helper files; no arbitrary native script execution is available.

Sentry requires eight named sections and workflow-dependent references. Its
checks do not require a code fence or a ten-case minimum. Do not impose Senior's
native rules on Sentry. Neither skill's observable native gates prove semantic
quality; downstream primary success is separate.

### F5. Development repairs are already settled

Round one used 80 requests and exposed serial tool overhead, copy-span ambiguity,
and incomplete final-artifact extraction. Before held-out freeze, batch read/write,
remaining-request notices, public coding context, copy/type clarifications,
safe Python additions and explicit final Markdown-link handling were tested.

Three round-two native compilers had already emitted final artifacts which the
earlier adapter missed. Only their unused solver stages resumed. Original
records are archived under `development-recovery/`; no compiler was rerun or
charge refunded. A correct raw development repair hit a missing StopIteration
exception in the checker; its reproducer passed after a pre-freeze repair,
while the original development score remains preserved.

Development readiness means working complete handoffs and demonstrated shared
coding tools, not perfect candidate answers. Senior's development lost-RED/output
constraints were actual observed task failures, not reasons to tune answers.
Do not repeat development or reuse recovery to repair held-out outcomes.

## Appendix G: partial results and what can already be deduced

**These are checkpoint counts, not a final recommendation.** Each arm has four
create, four sharpen, four template and only three of four coding outcomes.

| Arm | Create | Sharpen | Template | Coding so far | Total so far |
| --- | ---: | ---: | ---: | ---: | ---: |
| Raw | 4/4 | 4/4 | 3/4 | 3/3 | 14/15 |
| Minimal | 4/4 | 4/4 | 3/4 | 3/3 | 14/15 |
| Wshobson | 4/4 | 3/4 | 4/4 | 1/3 | 12/15 |
| Senior | 4/4 | 2/4 | 3/4 | 1/3 | 10/15 |
| Sentry | 3/4 | 4/4 | 3/4 | 3/3 | 13/15 |

Useful bounded deductions, subject to final eligibility checks:

- Every completed native-arm downstream trial has succeeded so far. The native
  score differences currently reflect compiler limits and handoff failures,
  not different correctness among completed downstream answers.
- Each arm has exactly one outcome left. Senior can reach at most 11/16;
  Wshobson at most 13/16; Sentry at most 14/16. Each control already has 14
  successes and can reach 15/16. Thus no native skill can strictly outperform
  the controls on the primary success count in this run.
- If Sentry passes its last trial and remains eligible, it outranks Wshobson.
  If Sentry fails and Wshobson passes, both have 13/16; the frozen maintenance
  tie-break favors Wshobson (August 15 versus May 4). If both fail and remain
  eligible, Sentry leads 13/16 to 12/16. Let the analyzer apply the rule, including
  any new hard labels; do not manually lock in a winner now.
- The ambiguous draft case is the only completed control failure so far. The
  omission diagnostic is essential to a fair claim about optimizer value.
- A useful final answer can recommend the best-supported eligible **skill**
  while clearly recommending direct/minimal instructions for clear one-off tasks
  where this experiment shows no benefit from the extra authoring computation.

Do not say this proves the chosen skill's intrinsic prompts are universally
better. The user's request for a practical choice is compatible with a concrete
recommendation plus honest limits; it is not permission to claim superiority
that the experiment did not establish.

## Appendix H: analysis and final verification commands

After all five pending trials finish:

```bash
python3 scripts/metaprompt-selection.py report
python3 scripts/metaprompt-selection-analysis.py --run benchmarks/metaprompt-selection/runs/selection-2026-10-03
```

The first writes `RUN/results.json`. The second writes `RUN/analysis.json` and
prints a compact integrity/recommendation summary. It verifies the 54 frozen
files, fixed ranking string, expected held-out IDs/metadata, reservations,
per-stage limits and request evidence. It hashes its own code and saved inputs.
It computes status/workflow rates, known and unknown usage, compiler/solver/
first-use cost, native observations, and paired comparisons against raw/minimal.
Its 4,000-sample, fixed-seed, within-workflow paired bootstrap intervals are
**exploratory** for this tiny selected sample, not proof of universal superiority.

Check the reported fields, not just the exit code. Require:

```text
complete_balanced_holdout = true
expected_holdout_trials = observed_holdout_trials = 80
integrity_errors = []
trials_reserved = all_recorded_attempts.count = 100
requests_reserved <= 2000
every compiler/solver label <= 10
all arms have 16 trials, 4 per workflow
request evidence reconciles to the durable ledger
```

At pause `results.json`/`analysis.json` were not produced as complete results.
If they exist tomorrow, inspect their input hashes/counts and regenerate from
the final records; do not assume existence means completion.

Fresh focused command, already passed 62 tests before the handoff:

```bash
python3 -m unittest discover -s tests -p 'test_metaprompt_selection*.py' -q
```

The actual Codex CLI offline integration uses synthetic responses, rejects
outbound HTTPS, and verifies real fixture file/test effects. No model quota is
consumed by this suite. Static helper, atomic budget, native gates, extraction,
installation/rollback and derivative analysis have defining regressions.

Full discovery last ran **550 tests in 80.220s: 548 passed, 2 failed**. Complete
output was inspected at `/tmp/metaprompt-selection-final-repo-tests-v2.log`.
Both failures predate and lie outside this benchmark:

1. `test_ai_workflow_contract.AIWorkflowContractTest.test_push_policy_is_consistent_in_active_workflows`:
   existing `dot_agents/skills/commit-dirty/SKILL.md` lacks the exact expected
   push-policy sentence.
2. `test_second_brain_vault.SecondBrainVaultTest.test_exact_sanitized_tree_exists_without_unapproved_files`:
   existing `05 Daily Notes/2026-07-22.md` is outside that test's inventory.

Do not delete the note or edit the unrelated skill to make this task green.
If `/tmp` logs are gone, the postmortem preserves attribution. Rerun the broader
suite only if new code changes or another concern justify it; the current docs
handoff alone does not require an 80-second repeat.

Final documentation/integrity checks:

```bash
python3 scripts/metaprompt-selection.py verify
./scripts/executable_readme-recruiter-sync
git diff --check -- README.md docs/smoke-tests.md tasks/lessons.md
```

Also verify both protocol digests and all inventoried hashes again; the analyzer
checks only the new protocol. Check newly added local report/result links.
README sync previously returned `pass_no_change`; scoped diff/link checks passed.
No new tests are needed for simple reversible prose edits.

## Appendix I: documentation still to finish

`docs/metaprompt-selection.md` is a substantial scaffold with primary source
receipts, protocol, compatibility notes, defects, replay commands, optional
installation/rollback and Cursor handoff. Its opening and results section still
say pending. Replace those with a decision-first report after complete analysis.

Required final content:

1. A specific eligible skill choice under the frozen rule, why it is the best
   practical choice here, and how to invoke/install it later if desired.
2. All five arms' successes/16 and each workflow's successes/4. Show controls.
3. Completed task errors, compiler limits and adapter failures separately.
4. Compiler+solver first-use requests/input/output tokens and stage time, plus
   solver-only figures. Include failed attempts; state unknown values honestly.
5. Native source-specific observations, with Wshobson's vacuous gate caveat.
6. Primary paired comparisons and the equally omitted ambiguous-case diagnostic.
7. Direct links to raw failures, a successful coding trace, aggregate results,
   pinned source revisions and actual maintenance diffs.
8. Exact total attempts/requests and hashes; small-sample/fixture/runtime limits.
9. Validation: 62 focused passes, 548/550 broader with named unrelated failures;
   fresh freeze/README/link checks; no installed changes, commits or pushes.

Update the relevant introductions/paragraphs in `docs/metaprompt-skills.md` and
`README.md` once a winner exists; the currently installed Majkey `$metaprompt`
must not be described as automatically replaced. Update `docs/smoke-tests.md`
only if the documented verification procedure changes. Mark the last three
ExecPlan checklist items complete only after their actual work is done.

The report currently uses Wshobson as the **example** optional install. If another
skill wins, update that example to the chosen candidate and native directory.
The helper supports all three and was independently tested only under `/tmp`:

```bash
python3 scripts/metaprompt-selection-skill.py stage --candidate wshobson-patterns --destination ~/.agents/skills/prompt-engineering-patterns
python3 scripts/metaprompt-selection-skill.py rollback --candidate wshobson-patterns --destination ~/.agents/skills/prompt-engineering-patterns
```

Other candidate/directory pairs are `alireza-senior` / `senior-prompt-engineer`
and `sentry-prompt-optimizer` / `prompt-optimizer`. These commands are **optional
future installation guidance**, not actions authorized for the current task.
The helper verifies full pinned inventories and licenses, refuses collisions,
symlinks/tampering, and rolls back only an exact unchanged owned copy. Parent
destination must already exist. No sudo. No live picker-refresh claim was tested.

The final chat answer should lead with the choice and concrete evidence, not
implementation history. Include the report link, compact scores/source facts,
control value/cost caveat, and truthful verification. Avoid ending with only
“inconclusive” or asking whether to continue.

## Appendix J: environment, agents, and failure discipline

- Shell: bash. Codex CLI version verified earlier: **0.160.0**. Subscription
  authentication is configured; do not read or print auth files. No paid API
  keys are used by this benchmark.
- Default shell sandbox failed with a bubblewrap loopback-startup error earlier.
  `exec_command` with `sandbox_permissions: require_escalated` and a specific
  read/test/run justification has worked under automatic review. Do not keep
  retrying an unchanged default sandbox failure or claim approval was blocked
  when no rejection occurred. If future review rejects an action, report the
  exact action/reason and continue safe unaffected work.
- Writable roots are `/home/example/linux-config` and `/tmp`; `.git` and local
  instruction/config surfaces have read restrictions. No worktree is allowed.
- Agents `/root/candidate_sources`, `/root/runtime_audit`, `/root/fixtures`
  completed their bounded work. No agent owns an active edit or model run.
  Their relevant reports are saved in research/review/docs; don't depend on
  tomorrow having live agent handles. They were explicitly allowed by repo
  coordination rules and did not act as model graders.
- Canonical instructions: `dot_codex/AGENTS.md`; plan contract `.agent/PLANS.md`;
  preferences `dot_agents/skills/feedback-memory/feedback.log`; lessons
  `tasks/lessons.md`. Applicable system-design coding/context files were read
  earlier. Read any new stricter local instructions before changing scope.
- Unexpected task failures require a dated postmortem. Current grouped log is
  `docs/postmortem/2026-10-03-metaprompt-selection-validation.md`; a separate
  eval-source-path incident exists too. Intended TDD REDs, measured benchmark
  failure outcomes, and this user-requested scheduler pause are not accidental
  infrastructure failures.
- Earlier unsuccessful read/patch attempts are documented: guessed unpublished
  agent paths, wrong protocol-root guess, web cache misses, and two patch-context
  mismatches. Use exact known paths and inspect current patch context. Do not
  repeat source/API fetches or command failures without a changed condition.
- The run was roughly 69 MB before the final coding block; raw evidence can be
  large. Avoid dumping complete request payloads or transcripts to the chat.
  Read selected fields/records and retain artifacts rather than copying logs.

## Archived continuation instruction (already executed; do not rerun)

> Resume `/home/example/linux-config/docs/metaprompt-selection-handoff.md` and
> `plans/select-maintained-metaprompt-skill.md`. The user has resumed the paused
> work. Preserve all frozen inputs and unrelated dirty changes. Confirm no
> selection runner is active, then continue the five pending
> selection-coding-flatten arms with
> `python3 scripts/metaprompt-selection.py run --jobs 3`. Keep benchmark settings
> gpt-6.1-sol/medium regardless of the main assistant's reasoning setting. Do not
> rerun development, recover held-out failures, exceed 100 attempts/2,000 requests,
> install skills or commit/push. After all 80 held-out records exist, run the
> documented report and derivative analyzer, verify accounting and both frozen
> inventories, inspect failure/trace evidence, and complete the decision-first
> report and related docs. Include the four handoff limitations, ambiguous draft
> omission sensitivity, hard-label caveat and source-specific native-gate meaning.
> Recommend a concrete eligible skill under the frozen rule while clearly stating
> whether it adds value over raw/minimal controls. Preserve the two unrelated
> broader test failures. Finish with the choice, evidence and report link.
