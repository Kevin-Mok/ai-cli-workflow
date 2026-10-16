# Native metaprompt skill selection


Raw request/response traces, runtime identifiers, trial ledgers and generated run files are private local evidence. Both benchmark `runs/` directories are ignored and removed from public history. This page retains reviewed aggregate findings and their limits; the public checkout no longer includes raw records for independently auditing those historical measurements. The harness and synthetic fixtures remain available for a new, separately budgeted run.

Source verification currently detects pin mismatches already present in the starting public revision. Preview and synthetic tests remain available, but do not start another inference run or silently repin frozen inputs. See the [source-pin incident](postmortem/2026-10-16-benchmark-source-pins.md).

**Choose Sentry's `prompt-optimizer` if you want a metaprompt skill.** It had
the highest observed end-to-end success among the three eligible native skills:
**14/16**, versus Wshobson's **13/16** and Senior's **11/16**. Its repository had
**1,034 stars** at the October 3, 2026 audit, with two inspected substantive
skill changes inside 180 days, latest May 4; none were inside 90 days. The
[pinned native package](https://github.com/getsentry/skills/tree/d18b7aa8ba878354e5c348310230e652f7690f9c/skills/prompt-optimizer)
and actual maintenance diffs are linked below.

For clear one-off tasks like these fixtures, **use direct instructions**.
Raw and minimal controls both scored **15/16** with much less authoring cost.
Sentry is the best-supported skill choice from this run; the experiment did
not demonstrate a benefit from adding a metaprompt stage to an already explicit
task. The lead over Wshobson is one case, and adapter defects limit confidence
in claims about the skills themselves.

Completed October 4, 2026: **80/80 balanced held-out outcomes**, plus 20
development attempts, using **754/2,000 authorized inference requests** within
the **100-attempt cap**. All requests requested and served `gpt-6.1-sol` with
medium reasoning. No active, interrupted or infrastructure-truncated trial
remains. The benchmark installed no finalist. In a later authorized change on
October 4, `$metaprompt` was migrated to the chosen Sentry package; see the
[replacement plan](../plans/replace-metaprompt-with-sentry.md) for deployment
verification. The benchmark's native results and frozen inputs are unchanged.

The primary summary
and request-level analysis
agree on Sentry. Accounting reconciles with no integrity errors or missing
usage fields. The [handoff](metaprompt-selection-handoff.md) preserves the
earlier pause and now records completion.

This is a fresh selection benchmark. The earlier
[metaprompt pilot](metaprompt-benchmark.md) remains separate and unchanged. Source
research, fixtures, runtime and trial evidence live under
[benchmarks/metaprompt-selection](../benchmarks/metaprompt-selection/). The
[active plan](../plans/select-maintained-metaprompt-skill.md) records implementation and
verification progress.

## Measured results and practical choice

Each workflow has four cases per arm and contributes 25% of the primary score.
Compiler failures count against end-to-end success. Controls are comparators;
the frozen selector chooses among eligible native skills only.

| Arm | Create | Sharpen | Template | Coding | Total | Primary success |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **Sentry prompt-optimizer** | 3/4 | 4/4 | 3/4 | 4/4 | **14/16** | **87.50%** |
| Wshobson prompt-engineering-patterns | 4/4 | 3/4 | 4/4 | 2/4 | 13/16 | 81.25% |
| Senior prompt engineer | 4/4 | 2/4 | 3/4 | 2/4 | 11/16 | 68.75% |
| Raw instructions | 4/4 | 4/4 | 3/4 | 4/4 | 15/16 | 93.75% |
| Minimal prefix | 4/4 | 4/4 | 3/4 | 4/4 | 15/16 | 93.75% |

Sentry completed all four coding cases, while Wshobson exhausted its compiler
allowance on two. Every completed native downstream trial succeeded: 14/14
for Sentry, 13/13 for Wshobson and 11/11 for Senior. The observed differences
therefore concern successful delivery through this capped compiler/solver
workflow. They do not distinguish answer quality among completed native trials.

Wshobson has stronger popularity and more recent maintenance evidence: 40,179
repository stars and an August 15 substantive change. Sentry wins under the
prespecified success-first rule; no tie-break was needed. Senior's lower result
includes three adapter handoff failures, so it cannot fairly be described as
having produced five wrong downstream answers.

| Arm | Compiler allowance exhausted | Final handoff not recognized | Completed downstream mismatch | Hard labels |
| --- | ---: | ---: | ---: | ---: |
| Sentry | 1 | 1 | 0 | 0 |
| Wshobson | 3 | 0 | 0 | 0 |
| Senior | 2 | 3 | 0 | 0 |
| Raw | 0 | 0 | 1 | 0 |
| Minimal | 0 | 0 | 1 | 0 |

Both control mismatches occurred on the same ambiguous template binding,
discussed below. None of the four unrecognized handoffs received a downstream
solver call. Their quality is unmeasured; the original failures remain scored.

## Observed cost

These totals cover **all 16 held-out attempts per arm**, including failed
compilers and nested public evaluations. Input counts include repeatedly sent
context and cached tokens; cached counts are a subset, not an additional charge.
Stage time sums compiler and solver wall time, including nested waits. It is
not the elapsed duration of the parallel experiment.

| Arm | First-use requests | Input tokens | Cached input subset | Output tokens | Summed stage seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sentry | 190 | 1,882,732 | 1,461,376 | 71,509 | 2,759.3 |
| Wshobson | 152 | 1,989,074 | 1,474,176 | 50,370 | 2,070.3 |
| Senior | 179 | 2,847,639 | 2,382,720 | 40,172 | 1,908.2 |
| Raw | 32 | 167,163 | 93,056 | 1,845 | 156.1 |
| Minimal | 32 | 168,235 | 90,496 | 1,433 | 137.5 |

Sentry averaged **117,671 input tokens per attempt**, versus **10,448** for raw,
and used **190 versus 32 requests** over the same scheduled cases. Its input
volume was lower than either other native skill, but it used more requests and
produced more output. These measurements do not establish a monetary or
subscription-quota multiplier; no API dollar price is assigned.

Compiler-only totals were Sentry 160 requests / 1,721,870 input / 70,114 output
tokens; Wshobson 131 / 1,876,113 / 49,543; Senior 160 / 2,748,678 / 39,181.
The controls have no compiler stage. The corresponding observed solver stages
were:

| Arm | Trials reaching solver | Solver requests | Input tokens | Output tokens | Summed solver seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sentry | 14 | 30 | 160,862 | 1,395 | 129.9 |
| Wshobson | 13 | 21 | 112,961 | 827 | 85.1 |
| Senior | 11 | 19 | 98,961 | 991 | 93.8 |
| Raw | 16 | 32 | 167,163 | 1,845 | 156.1 |
| Minimal | 16 | 32 | 168,235 | 1,433 | 137.5 |

Solver totals have different denominators because failed compilations never
reach that stage. They are not evidence that the skill makes execution cheaper.
Repeated reuse of a saved prompt was not measured, so no amortization or
break-even claim is made.

The whole selection run, including calibration, consumed **754 requests**:
169 development and 585 held-out. Across all attempts, 571 were compiler
requests and 183 solver requests. Usage totals are **8,820,646 input tokens**
(6,859,264 cached), **202,133 output tokens** (17,298 reasoning), with zero
unknown usage fields. Reasoning tokens are a subset of output tokens. All
reservations remain charged; the earlier 50-request pilot is separate.

## Paired comparisons and the ambiguous template

Raw and minimal have identical case-level success, so each native skill has the
same comparison against either control. Differences below are percentage
points of equally weighted workflow success. Intervals use 4,000 fixed-seed
paired bootstrap samples within workflows. This is a tiny, selected synthetic
sample with multiple comparisons and no repeated trials; these exploratory
intervals do not establish general superiority.

| Native skill | Primary difference vs either control | Exploratory 95% interval |
| --- | ---: | ---: |
| Sentry | −6.25 pp | [−25.00, +12.50] pp |
| Wshobson | −12.50 pp | [−31.25, +6.25] pp |
| Senior | −25.00 pp | [−50.00, 0.00] pp |

`selection-template-draft` puts `{{message_data}}. Keys ...` inline. Substituting
multiline data joins its final `Fact: funding unknown` line to the following
instructions, although the contract asks for exact line copying. The
raw result
retained those instructions in the final fact; the
minimal result
retained the period. The key expects only `funding unknown`. All three native
arms passed, but that case provides ambiguous evidence of an optimizer benefit.

A **post-hoc sensitivity** omits this exact case from every arm, leaving four
create, four sharpen, three template and four coding cases. Each workflow still
weighs 25%, so the weighted score need not equal successes divided by 15.

| Arm | Remaining successes | Weighted success | Difference vs either control | Exploratory 95% interval |
| --- | ---: | ---: | ---: | ---: |
| Sentry | 13/15 | 85.42% | −14.58 pp | [−31.25, 0.00] pp |
| Wshobson | 12/15 | 81.25% | −18.75 pp | [−37.50, −6.25] pp |
| Senior | 10/15 | 66.67% | −33.33 pp | [−56.25, −12.50] pp |
| Raw | 15/15 | 100.00% | — | — |
| Minimal | 15/15 | 100.00% | — | — |

This diagnostic changes no primary score, ranking, charge or saved output and
uses no additional inference. It reinforces the practical case for direct
instructions on already explicit tasks. It does not prove universal performance
outside these fixtures.

## Candidates and selection evidence

The shortlist requires at least 1,000 repository stars, a nonarchived licensed
package, native coverage of creation, sharpening, reusable templates and coding
agent prompts, substantive post-introduction maintenance within 180 days, and
independent source lineages. Counts exclude introductions, moves, formatting,
branding and generic repository churn. The 90-day window starts July 5, 2026;
the 180-day window starts April 6, 2026.

| Native skill / repository | Exact repository stars at retrieval | Retrieval UTC | Latest substantive package change | Changes 90 / 180 days | Recorded qualifying authors, 180 days | License |
| --- | ---: | --- | --- | ---: | ---: | --- |
| [prompt-engineering-patterns / wshobson/agents](https://github.com/wshobson/agents/tree/156b7a5e7a8b93642628a339ee4039c925b34c7f/plugins/llm-application-dev/skills/prompt-engineering-patterns) | 40,179 | 2026-10-03T22:34:16.986652Z | 2026-08-15T20:49:35Z | 1 / 2 | 2 | MIT |
| [senior-prompt-engineer / alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/engineering-team/skills/senior-prompt-engineer) | 27,472 | 2026-10-03T22:34:17.001868Z | 2026-06-11T15:28:22Z | 0 / 1 | 1 | MIT |
| [prompt-optimizer / getsentry/skills](https://github.com/getsentry/skills/tree/d18b7aa8ba878354e5c348310230e652f7690f9c/skills/prompt-optimizer) | 1,034 | 2026-10-03T22:36:06.171123Z | 2026-05-04T17:40:37Z | 0 / 2 | 1 | Apache-2.0 |

These stars belong to entire repositories, not individual skills. They support a
popularity filter, not prompt quality. The independent cross-review later saw
27,473 stars for the senior repository at 22:38:27.777741Z; both timestamped
observations are retained. Recorded commit-author identities do not establish
independent human ownership. Exact pins, native bytes, licenses, hashes and
retrieval evidence are in [sources.json](../benchmarks/metaprompt-selection/sources.json),
with [Group A](../benchmarks/metaprompt-selection/research/group-a.md),
[Group B](../benchmarks/metaprompt-selection/research/group-b.md) and
[independent cross-review](../benchmarks/metaprompt-selection/research/cross-review.md).

The wshobson [August 15 diff](https://github.com/wshobson/agents/commit/56a28c6e4d575f1813f777ddfeb956e069aac07a)
adds an early stop for repeated, unimproved helper evaluations; its
[June 3 diff](https://github.com/wshobson/agents/commit/3ce0342afde674b3a492bdc9271621e953322c11)
expands native discovery to templates and related prompting tasks. Senior's
[June 11 diff](https://github.com/alirezarezvani/claude-skills/commit/5acece10acd47513bbc7b0c91fe88f54df138adc)
changes baseline/eval-first gates and helper behavior. Sentry's
[April 24 diff](https://github.com/getsentry/skills/commit/6a844a09d7981594d510fc9b2d6b022b4ed2e246)
adds instruction-layer and tool-schema guidance; its
[May 4 diff](https://github.com/getsentry/skills/commit/c190d369bcbaa6cfdd95e9edfdba040506b4db76)
adds external-context inventory and output/specification guidance. These are
inspected package changes, not repository activity counts.

Larger collections were also considered and excluded. GitHub awesome-copilot
(39,667 stars) had only the package introduction and forbids template variables.
Davila's collection (32,353) had no later substantive change for the package.
Antigravity (47,224) lacked sufficiently evidenced variable-template coverage
for one package; another had generic bulk edits and overlapping NeoLab lineage.
Jeffallan (11,719) had only branding/backlink changes inside the window. NeoLab
(1,742) had no substantive recent package change; a copied path was not new
maintenance. Developer-kit (353) failed the popularity and maintenance filters.
Senior's marketing toolkit was excluded because its current native scope does
not cover coding-agent authoring. Exact package-specific evidence and reasons
remain in the source manifest; these exclusions do not rank unrelated skills or
assert that a large collection is poor quality.

## Protocol and native compatibility

Five arms are frozen: three native finalists, raw task instructions, and a fixed
minimal instruction prefix. Twenty development trials comprise two rounds of two
cases per arm. Eighty held-out trials comprise sixteen fresh cases per arm, four
per workflow: create, sharpen, template and coding. Total cap: **100 trials** and
**2,000 inference requests**, with at most ten requests per compiler stage and ten
per solver stage. Failed, interrupted and continuation requests consume quota;
there is no automatic replay or refund. Jobs default to two; this held-out run
uses three concurrent jobs. Development fixes were completed before freezing
and held-out execution. The frozen protocol SHA256 is
`5aa62fbbf06a2c5bd559b973d4f02b45f8822d4b60c26e0d23f708c181af6f1a`.

The frozen `allocation.total=90` and `development_per_arm=2` summary fields
predate the second calibration round. The actual frozen schedule and durable
ledgers are authoritative: 20 development plus 80 held-out, 100 total. Both
reporting paths use the actual schedule; frozen metadata is preserved unchanged.

All arms use the same downstream packets, files and template bindings. Templates
compile without bound values, then bind the same named inputs in every arm.
Skill arms include a compiler stage; raw and minimal arms invoke only the solver.
Results therefore compare complete authoring-and-execution workflows with
different amounts of model computation. They cannot isolate the effect of skill
text from the effect of additional authoring computation. First-use accounting
includes both stages, including failed and nested requests.
Fixtures and reference answers are synthetic; no real usage-frequency claim is
made. The suite contains more cases than the selected held-out schedule, chosen
before scores using the recorded seed. The
[fixture notes](../benchmarks/metaprompt-selection/fixture-notes.md) document
construction, public acceptance contracts and limitations.

Native packages are copied without content rewrites, retaining their relative
references and scripts. Each compiler sees only its own skill, authoring request,
allowed context and public coding files. Hidden answers and held-out template
bindings are unavailable. Final prompts are extracted mechanically from explicit
native final labels, artifacts or sections; the harness must not choose whichever
variant scores best or silently rewrite a candidate's output.

Wshobson's authoring uses native patterns and references; its optional optimizer
has mock/demo behavior and dependency examples, which are not evidence of real
model improvement. Senior's required deterministic analyzer is exposed through
a narrowly fixed `run_skill_check` wrapper, preserving its pinned implementation
while confining paths and output files. Static clarity/token measures do not prove
its task-level no-regression gate. Sentry uses its native eight-section report;
its Optimized Prompt section is handed downstream without inventing a fence rule.
Native workflow completion and downstream success are reported separately.
Wshobson has no mandatory machine-checked native gates in this adapter; its
`native_workflow.complete=true` can therefore appear even when compilation
exhausts its allowance. Treat that flag as not applicable for process-completion
comparison. Its actual usable handoffs and downstream results remain measured.
Senior and Sentry checks have different source-specific requirements and are
also not a shared semantic-quality scale.

Compiler tools support reading/writing fixture files and a public batch evaluator.
A skill may author 1–20 public examples and evaluate its prompt in one fresh
no-tools model context. Expected answers remain in the checker. Public eval calls
share the ten-request compiler allowance and global budget; they are not hidden
benchmark trials. Batched JSON comparison is limited evidence: it does not provide
interactive coding tools, broad statistical replication or independent real-world
tasks. Unexecuted native gates must remain explicitly unverified.

Solvers work in isolated fixture repositories. Coding checks require actual target
and public-test reads, a target-only edit, observed public RED/GREEN checks and
stopping after success, as well as correct final code and hidden assertions.
Native shell, network, deployment and external messages are unavailable. A
request cap or infrastructure failure must be distinguished from a completed
wrong answer. Subscription token usage is reported when observed; no invented
API dollar price is attached.

Source review before any held-out coding record found an eligibility caveat.
The frozen scorer's `hard_failures` bucket includes code-format errors and all
Python allowlist rejections, and the selector excludes an arm for any such
top-level label. This is broader than the intended serious-authorization filter.
`output_format` and `unsafe_code` do not establish an observed scope violation;
actual denied fixture access is labeled `unauthorized_tool_access`. Original
scores and ranking stay frozen. All 80 held-out records have **zero top-level
hard labels**, so this overbroad filter did not exclude any finalist or change
the observed choice.

## Failure evidence and native checks

Both development rounds are preserved. Calibration added confined batch file
tools, clarified exact-copy boundaries, recognized explicit final Markdown
artifact links, and corrected a restricted-Python exception omission. Three
already completed native compiler artifacts continued into their unused solver
stages; original records are archived, compiler charges retained, and no compiler
was rerun. Development-only recovery closes after freeze. All second-round
handoffs completed; readiness does not require perfect candidate answers.

The six held-out compiler limits were Wshobson on extraction-quotes, coding-pairs
and coding-chunks; Senior on summary-corrections and template-filter; Sentry on
create-writing-draft. Each exhausted the ten-request compiler allowance. For
example, Wshobson's chunks record
contains ten compiler requests and no solver stage. These are measured capped
workflow failures, with no observed downstream answer to grade.

Four other failures expose the frozen adapter's final-prompt parser:

| Saved trial | Presentation the parser missed | Separate native-process observation |
| --- | --- | --- |
| Senior extraction-quotes | `FINAL PROMPT — candidate, structural gate failed`, prompt fence, second metric fence, and `Saved as` artifact line | Actual static clarity regression 90 → 85 |
| Sentry template-conflict | `Optimized Prompt — FINAL HANDOFF` heading, with the artifact link on the next line | The native section matcher also rejected the heading suffix; all eight human-readable sections were present |
| Senior coding-headers | `FINAL PROMPT — prompts/final_prompt.txt`, underline, then prompt text | Same-case baseline/final public evaluation pair not observed |
| Senior coding-chunks | Same em-dash form with a backticked artifact path | Same-case evaluation pair not observed |

Visible final artifacts exist in these records, but none reached a solver.
Preserving the frozen scores prevents tuning the parser against held-out
results. No recovery, retry or inference was performed for them. Written
10/10 or 12/12 claims do not replace actual native evaluation traces.

The impact can be bounded without inventing answers. Holding all other outcomes
fixed, resolving only these four unknown downstream results could leave Sentry
between 14 and 15 successes, Senior between 11 and 14, and Wshobson at 13.
Senior could tie Sentry if all three of its unknowns passed and Sentry's did
not; the maintenance tie-break would then favor Senior. These are possible
bounds, **not rescored results**. They limit how confidently this run can rank
intrinsic skill quality, while the actual recorded workflow still selects Sentry.

| Native skill | Usable handoffs / 16 | Recorded native checks complete / 16 | Interpretation |
| --- | ---: | ---: | --- |
| Sentry | 14 | 3 | Twelve outputs used an `Optimized Prompt — FINAL` or `— FINAL HANDOFF` suffix rejected by the section matcher; the thirteenth missing-section result was the compiler-limit case. The low recorded count is strongly affected by this matcher. |
| Wshobson | 13 | Not applicable | Recorded flag is 16/16 because there are no mandatory machine-checked native gates, including on its three compiler limits. |
| Senior | 11 | 9 | Six records lack an observed same-case public evaluation pair; two have static clarity regression and two static token regression. These reasons overlap across seven records. |

Sentry's twelve suffixed headings were inspected in the saved compiler replies;
their section-check failures were retained. Native check flags, usable handoffs
and downstream correctness are three different measurements. Senior's actual
rule allows an unchanged imperfect public score with no previously passing case
lost; no invented 100% public-eval gate was added.

For concrete successful execution, Sentry's headers trial
records `read_files` of `headers.py` and `public_tests.py`, a failing public
`run_tests`, a target-only write changing the implementation to preserve order
and duplicates while stripping/lowercasing strings, then a passing `run_tests`.
The solver stopped after green; final code and fixture artifact both passed
hidden assertions. The raw trace establishes those actions independently of
the assistant's completion claim. Its separate native heading mismatch remains
visible in the same record.

## Limits and verification

These cases measure constrained factual JSON, source selection, extraction,
structured message drafts, template reuse and small pure Python repairs. Writing
cases do not measure prose style or persuasion. Coding fixtures do not represent
large repositories, frontend design or production deployments. Passing a limited
public eval or static helper is not proof of general task quality. A small
synthetic selection cannot establish universal superiority.

Before freeze, all 55 focused selection tests passed, all 27 pinned files
matched, all 26 reference answers passed, and seven coding bugs failed their
public and hidden checks before the reference fixes passed. Fresh broader
discovery passed 548 of 550 tests; the two existing failures concern an exact
commit-dirty policy sentence and a second-brain vault inventory. Their complete
attribution and calibration repairs are recorded in the
[validation postmortem](postmortem/2026-10-03-metaprompt-selection-validation.md).
Fresh completion checks on October 4 passed all **62 focused tests** (exit 0),
all 27 source-file hashes, all 26 reference answers and seven coding RED/GREEN
pairs. The separate sensitivity's defining test had first failed because its
function was absent, then passed without changing primary records. All **54 new
frozen files** and all **82 historical frozen files** still match. The historical
protocol SHA256 remains
`685a65243d5251a82e1f8b75e54bb564e4b2c7758ae7ec536653ee3cd1bb76eb`.

Final accounting verifies exactly 100 reservations and records, with 80 held-out
rows covering the same 16 cases in every arm; every workflow has four rows per
arm. All 754 observed requests reconcile to the durable ledger, all requested
and served `gpt-6.1-sol`/medium with HTTP 200, no stage exceeds ten requests,
and no usage metric is missing. The derivative analysis preserves evidence
hashes and its own code hash. Neither frozen code nor the historical pilot was
changed after this run began. The README gate returned `pass_no_change`, scoped
`git diff --check` passed, and all 39 checked local selection-document links
resolve. All 102 derivative evidence hashes (100 trials and two ledgers) match.
No tracked configuration changed, so `refresh-config` was not needed.

## Reproduce and verify

From the repository root, read-only/offline preparation:

```bash
python3 scripts/metaprompt-selection.py verify
python3 scripts/metaprompt-selection.py dry-run
python3 tests/test_metaprompt_selection.py
python3 tests/test_metaprompt_selection_runtime.py
python3 tests/test_metaprompt_selection_native.py
python3 tests/test_metaprompt_selection_eval.py
python3 tests/test_metaprompt_selection_install.py
python3 tests/test_metaprompt_selection_analysis.py
```

The runtime test uses the actual Codex CLI and real fixture MCP with synthetic
upstream responses and forbidden remote HTTPS. It checks real files and tool logs,
not assistant claims. The install suite verifies pinned copying, collision and
symlink rejection, tampering/extra-file preservation and guarded rollback.
Reference answers pass deterministic checks; supplied coding bugs fail public and
hidden assertions before repair.

The following commands make subscription model requests or freeze/report the
specified run. They describe the reusable workflow. The public checkout omits prior ledgers;
restore private records or explicitly authorize a fresh budget before execution:

```bash
python3 scripts/metaprompt-selection.py develop --development-round 1 --jobs 2
python3 scripts/metaprompt-selection.py develop --development-round 2 --jobs 2
python3 scripts/metaprompt-selection.py freeze
python3 scripts/metaprompt-selection.py run --jobs 2
python3 scripts/metaprompt-selection.py report
python3 scripts/metaprompt-selection-analysis.py --run benchmarks/metaprompt-selection/runs/selection-2026-10-03
```

Inspect privately retained run artifacts
for the durable trial/request ledgers, development settings, frozen protocol,
individual compiler/solver transcripts and aggregate results. Confirm that each
arm has the same sixteen held-out cases and four cases per workflow, original
failed reservations remain counted, and no key/reference solution entered model
inputs. Check coded tool traces against actual artifacts and public results.
Review native reports and compiled prompts for lost constraints, invented facts,
unsupported evaluation claims and premature task execution. Do not tune against
held-out results or edit frozen inputs to improve scores.

The private local `summary.json` contains every aggregate field printed by `report`.
The command also rebuilds a local, ignored `results.json`, whose `rows` duplicate
all 100 private individual trial records (about 75 MiB). Regenerate the compact
summary without inference with
`python3 scripts/metaprompt-selection.py report > benchmarks/metaprompt-selection/runs/selection-2026-10-03/summary.json`.
The derivative analyzer reads individual trials and ledgers directly. No frozen
input, trial, ledger or analysis hash was changed by this packaging choice.

## Optional installation and rollback

No finalist was installed or made the default during this benchmark. The later
replacement uses the `metaprompt` alias; the commands below are only for a
separate native `prompt-optimizer` installation and are unnecessary for that
alias. The helper
stages a complete pinned native package and license from local verified sources;
it never downloads or invokes a model. It refuses existing destinations,
symlinks, source escape and tampered inventories. The destination parent must
already exist. Staging all three packages and rolling them back was tested only
inside temporary directories.

An optional installation of the recommended pinned Sentry package:

```bash
python3 scripts/metaprompt-selection-skill.py stage --candidate sentry-prompt-optimizer --destination ~/.agents/skills/prompt-optimizer
```

Open the staged SKILL.md and native references, confirm the name and file contents,
and start a fresh agent session to discover `$prompt-optimizer`. Staging is not evidence
that an already running picker refreshed. This copies a package; it does not
change existing metaprompt skills, aliases or defaults.

Guarded rollback of that exact unchanged copy:

```bash
python3 scripts/metaprompt-selection-skill.py rollback --candidate sentry-prompt-optimizer --destination ~/.agents/skills/prompt-optimizer
```

Rollback refuses modified files, extra files/directories, symlinks and the pinned
benchmark source tree. Preserve personal modifications separately before deciding
how to remove a changed copy; do not bypass the guard with an indiscriminate
recursive deletion. No sudo is required for a user-owned destination.

## Handoff

Paste-ready Cursor audit prompt:

> Review plans/select-maintained-metaprompt-skill.md and docs/metaprompt-selection.md, then
> audit benchmarks/metaprompt-selection against its frozen protocol, source hashes
> and durable ledgers. Preserve old pilot evidence and unrelated dirty work. Do
> not run models, change frozen fixtures, install skills or select prompt variants
> by score. Check native package lineage, helper confinement, hidden-key exclusion,
> equal create/sharpen/template/coding allocation, actual coding read/write/public
> RED/GREEN/stopping evidence, native completion versus downstream correctness,
> cap failures versus wrong answers, and complete observed usage accounting. Run
> the documented offline tests. Reconcile the report with actual run artifacts;
> state incomplete evidence and unsupported generalizations explicitly. Keep any
> plan/doc corrections with their related implementation in a focused commit.

Suggested Conventional Commit subject, when delivery is authorized:
`feat(benchmarks): compare maintained native metaprompt skills`.
No commit or push is performed by this report.
