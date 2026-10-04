# Select a maintained metaprompt skill

## Purpose and observable outcome

Give example-user a concrete, evidence-backed default skill recommendation from a
popular, maintained GitHub repository. Publish pinned source receipts, an
equal-workload benchmark, raw sanitized observations, costs, limits, and exact
installation/rollback guidance. Do not install or replace a skill.

## Context and boundaries

The historical `benchmarks/metaprompt/` pilot exhausted 50 requests with little
completed coverage. It and its frozen implementation are protected unchanged.
New work lives in `benchmarks/metaprompt-selection/`, a new entry script, focused
tests, this plan, the saved prompt, and related documentation. Initial
`git status --short` was captured before modifications: extensive pre-existing
metaprompt, phone SSH, README, smoke-test, lesson and untracked benchmark work
must be preserved. No worktrees, installations, commits, pushes or default
configuration changes are authorized by this implementation.

## Settled decisions

- Use Codex subscription, `gpt-6.1-sol`, medium reasoning for both stages.
- The approved replacement allocation is at most 100 complete trial attempts,
  at most 10 compiler and 10 solver inference requests per trial, and a durable
  global ceiling of 2,000 inference requests. Development and failures count;
  reservations are never refunded. This supersedes the exhausted old pilot.
- Eligibility requires a native prompt-authoring skill in a nonarchived repo
  with at least 1,000 stars, a usable license, all four workflows, and at least
  one substantive post-introduction skill/reference/test change within 180 days.
- Exclude moves, imports, formatting, bot churn and unrelated repo activity.
  Deduplicate copied lineages. Stars describe the repository, not the skill.
- Audit create, sharpen, reusable template, and coding-agent workflows equally.
- Choose at most five eligible independent finalists before model outputs,
  ordered by latest substantive change, change count180, then repository stars.
  Raw and fixed minimal-contract controls are additional arms.
- Each arm initially gets two development trials. The documented calibration
  round uses the ten spare attempts, making four development trials per arm.
  Allocate equal held-out trials in multiples of four within the 100-trial
  ceiling; prefer distinct cases.
- Verify native workflows offline and in development before scored execution.
  Freeze protocol, sources, fixtures, scoring and settings before held-out work.
- Use executable, schema and source checks, no unmetered model grading. Weight
  each workflow 25%; exclude serious authorization violations from default
  selection. Exact ties: maintenance, lower first-use cost, then stars.
- Give the best-supported practical choice with calibrated uncertainty even if
  the controls tie or outperform skills. Do not imply universal proof.

## Ordered implementation checklist

- [x] Capture baseline and read applicable repo/skill/context instructions.
- [x] Preserve historical pilot; save the approved scope and authorization.
- [x] Audit native skills and evidence; pin complete packages and licenses.
- [x] Create fresh development and held-out fixtures with private scoring keys.
- [x] Write failing tests for budgets, scheduling, isolation and public tests.
- [x] Implement isolated, resumable harness and real-CLI offline integration.
- [x] Independently verify pins, eligibility, fixtures and reference solutions.
- [x] Run development trials per arm; resolve harness faults before scoring.
- [x] Freeze held-out protocol before observing scored outputs.
- [x] Execute the balanced held-out schedule within both ceilings.
- [x] Derive results, cost accounting, recommendation and limitations from traces.
- [x] Update guide, README, smoke checks and review/verification evidence.

## Risks, edge cases and rollback

Small samples establish a practical choice, not broad statistical superiority.
Static JSON writing tasks measure constrained factual delivery, not prose taste.
Native helper requirements must be honored through narrow reviewed capabilities
or recorded as compatibility failures, never silently skipped. Read/write tools
must not expose private scoring keys. Compiler references may need multiple
requests; manifests are supplied initially and stage ceilings are 10 requests.
Provider errors and interruptions consume reservations and remain visible.
Rollback is removal of this task's new files and only its attributable doc
hunks; historical data and pre-existing user changes remain intact.

## Verification

Automated: focused unittest suite for schedule fairness, durable 100/2,000
ceilings, per-stage limits, interrupted resumption, prompt extraction, private
key isolation, public-test execution, reference answers and known buggy
fixtures. Run the actual Codex CLI against an offline synthetic provider before
paid work; exercise reference reads, artifact writes and public tests. Verify
source SHA256s and frozen inputs before held-out execution. Run relevant broader
repository tests and inspect actual results, not just process exit codes.

Manual/runtime: inspect pinned upstream diffs, candidate eligibility, compiler
deliverables, coding target writes/public tests, request-level usage (including
aborted episodes), balanced denominators and report links. Installation guidance
is reviewed and tested without modifying installed skills.

## Progress and evidence

2026-10-03: Preparation delegated to three existing agents: Group A source audit,
Group B source audit, and fresh fixtures. They are not authorized to invoke any
benchmark models. Parent owns runtime, accounting, combined manifest and report.
Source audit has confirmed that some popular collections contain narrow or
stale prompt skills; repository activity will not substitute for skill history.

Preparation evidence: `python3 -m unittest discover -s tests -p
'test_metaprompt_selection*.py' -v` passed 16 tests (exit 0), following observed
RED tests for the missing implementation, draft extraction and harmless typing
imports. Three tests drive the actual CLI against a synthetic upstream, assert
zero outbound HTTPS calls, and verify real MCP read/write/test effects.
`python3 scripts/metaprompt-selection.py verify` passed (exit 0): three finalists,
27 pinned files, 26 passing reference answers, seven public/hidden coding
RED/GREEN pairs, 90 scheduled trials (10 development plus 80 scored).

Finalists selected before any live model output: wshobson-patterns (40,179 repo
stars, August 15 substantive helper fix), alireza-senior (27,472, June 11 native
workflow rewrite), sentry-prompt-optimizer (1,034, May 4 context/runtime update).
The runtime supports reviewed static helpers. Review found senior requires real
public evaluation, so add a bounded batch `evaluate_prompt` action sharing the
same compiler-stage ten-request allowance and global ledger. Public cases are
compiler-authored; hidden keys never enter either stage. Batched evaluations
test generated outputs without tools and are not independent held-out evidence.
Both controls retain identical downstream capability. No extra budget is added.

Independent fixture review made JSON-only output, exact keys and expected types
explicit in the raw and authoring requests. It also caught premature draft
extraction and harmless Python rejection, now covered by passing regressions.

First development round finished:10 trials,80 charged inference requests.
Both coding controls and Sentry's coding workflow completed; five skill compiler
episodes exhausted the ten-request allowance. Serial reference/file operations
were a major cause. Add read_files/write_files with identical scope enforcement,
live remaining-request notices, and explicit public coding files for authoring.
The second development round uses all ten spare trial slots:20 development plus
80 scored =100 total,20 attempts per arm. Do not refund or overwrite round1.
Second round uses distinct `--d2` trial IDs and version2 clarified copy spans.
This is a calibration change before any held-out output, not post-hoc tuning.

Primary success remains downstream objective correctness and authorized coding
actions. Native section/reference/helper/eval completion is a separate measured
dimension: it must not silently substitute an invented perfection criterion for
the senior skill's actual no-regression rule. All live inner evaluations share
the compiler stage allowance. Unexecuted native gates remain explicitly unverified.

Full repository unittest discovery ran514 tests (exit1):512 passed; unrelated
existing failures are the commit-dirty exact push-policy sentence and an extra
second-brain July22 daily note. Both are preserved and documented in the
selection validation postmortem. Focused selection tests passed38 after batch
tools and the offline staging/rollback helper were added.

Calibration complete:20 reserved development attempts,169 inference requests.
Three explicit Markdown final-link handoffs were missed by the earlier adapter;
the defining regressions now pass. Continue only their unused solver stages from
original final artifacts, archiving original records under development-recovery/
and retaining all compiler charges. No new trial or compiler call was made for
recovery. Every round2 native compiler and solver completed. Readiness requires
completed handoffs plus a demonstrated shared coding runtime, not perfect model
answers; the senior coding answer's lost output/RED constraints remain observed
task failures. The raw control's StopIteration checker defect is fixed by a
passing reproducer; original development grading is retained as calibration.

Fresh pre-freeze checks:55 focused tests passed (exit0); all26 references and
seven public/hidden coding pairs passed integrity checks; all27 pinned source
files matched. Historical protocol SHA256 remains
685a65243d5251a82e1f8b75e54bb564e4b2c7758ae7ec536653ee3cd1bb76eb,
and every file in that frozen inventory still matches. All three install/rollback
helpers were independently exercised only under/tmp. README sync returned
pass_no_change after scoped links were added. No installed configuration changed.

Held-out protocol frozen at SHA256
5aa62fbbf06a2c5bd559b973d4f02b45f8822d4b60c26e0d23f708c181af6f1a.
`python3 scripts/metaprompt-selection.py run --jobs 3` is executing the80 held-out
rows. No frozen input/code/test/source file may be edited after this point.
Additional analysis is derived from frozen trials only and must not alter their
scores, source selection or ranking rule. Report/documentation updates are outside
the input inventory. Parallelism3 changes throughput, not requests per trial.

Fresh broader verification ran543 tests in79.703s (exit1):541 passed, with only
the same commit-dirty sentence and second-brain extra-note failures. The full
tracebacks were inspected; both remain outside this task. Derivative analysis
is being tested independently using synthetic records and cannot change any
frozen score or selection rule.

Read-only review before any held-out coding record found an overbroad inherited
eligibility bucket: output_format and all unsafe_code allowlist rejections can
exclude an arm along with actual unauthorized_tool_access. Preserve the frozen
implementation and explicitly distinguish these categories in the report. The
observed filter is strict contract/execution-boundary compatibility, broader than
the intended serious-authorization-only filter. Report its actual effect after
completion; do not mislabel unsupported pure code as a security incident.

## Review notes

Closeout verification, 2026-10-04: README sync returned `pass_no_change`; scoped
`git diff --check` passed; all 39 checked local selection-document links resolve.
Fresh verification of both protocol digests and their complete 54/82-file
inventories found no mismatch. All 102 derivative evidence hashes (100 trials
and two ledgers) still match, and primary/derivative counts, scores and selection
agree. The report, installed-skill guide, README, smoke checks and completed
handoff reflect final outcomes. All checklist items are complete. No skill,
tracked configuration, git index or history was changed by this continuation.

Final execution and analysis, 2026-10-04: all five remaining flatten trials
completed successfully. The run is closed at 100 attempts / 754 requests:
20 development / 169 requests and 80 held-out / 585 requests. Both report and
derivative analyzer select Sentry (14/16), ahead of Wshobson (13/16) and Senior
(11/16); raw and minimal each achieve 15/16. The same 16 cases appear in each
arm, four per workflow. No integrity errors, unknown usage, orphan requests,
interrupted outcomes or held-out hard labels remain. Every request requested
and served gpt-6.1-sol/medium with HTTP 200; no stage exceeds ten requests.

Observed first-use costs across 16 held-out attempts: Sentry 190 requests /
1,882,732 input tokens, Wshobson 152 / 1,989,074, Senior 179 / 2,847,639,
raw 32 / 167,163, minimal 32 / 168,235. All failures stay charged. The entire
run uses 8,820,646 input and 202,133 output tokens; cached/reasoning subsets are
reported separately. Solver-only counts have unequal reached-stage denominators;
no dollar or repeated-reuse saving is inferred.

Final saved-heading review confirms Sentry's native-check count (3/16) has twelve
Optimized Prompt suffix mismatches plus one compiler-limit case. Wshobson's
16/16 native flag remains vacuous; Senior's actual recorded count is 9/16.
The report separates these flags from usable handoffs and correct downstream
results. It links all four unmeasured adapter failures and actual successful
coding RED/GREEN actions, retains every frozen score, shows exploratory paired
intervals, and reports the equal omission sensitivity (controls 100%, Sentry
85.42%, Wshobson 81.25%, Senior 66.67%). There is no evidence that a metaprompt
stage improves on already explicit control instructions in this suite.

2026-10-04: User resumed the paused work. Verified no existing runner, no
interrupted checkpoint records, 95 attempts / 702 requests, and all 54 frozen
input hashes before continuing only the five unreserved flatten trials with
`run --jobs 3`. Fresh offline verification passed all 62 focused tests, all 27
package hashes, all 26 reference answers and seven coding RED/GREEN pairs.
Both the new and historical frozen inventories match (54 and 82 files).
No development, previous held-out trial, installation or default change was
repeated.

User-requested pause and detailed continuation capture, verified at
2026-10-04 00:09:45 UTC (October3 Toronto):75/80 held-out outcomes persisted,
95/100 trial attempts and702/2000 inference requests (169 development +533 held-out).
The parent-only SIGINT let the submitted batch drain; process exited130
intentionally. No active/interrupted records or benchmark parent remain.
Only the five selection-coding-flatten arms are unreserved. All702 request
records reconcile to the ledger, with no orphan/mismatched labels; every record
requests/serves gpt-6.1-sol with medium reasoning, and none lacks a usage object.
New54-file and historical82-file frozen inventories both match their original
protocol hashes. Preserve the pause until the user resumes. The comprehensive
handoff is [docs/metaprompt-selection-handoff.md](../docs/metaprompt-selection-handoff.md).
The main assistant may use lower reasoning tomorrow; benchmark settings must
remain frozen. Completion/analysis/recommendation checklist items remain open.

Held-out inspection found one ambiguous rendered control:
selection-template-draft appends instructions to the last line of its multiline
binding despite a line-exact copy rule. Add a separate post-hoc sensitivity
omitting that case from every arm, still weighting each workflow25%. Preserve
the primary scores, recommendation and all request charges. This diagnostic
must not assign a hypothetical correct answer or consume additional inference.
The separate derivative implementation passed its defining RED/GREEN test;
all62 focused tests now pass (exit0). Both derivative files are outside the
54-file frozen inventory. At this checkpoint58 held-out outcomes are recorded,
and544 requests are reserved, including development. Primary inputs are unchanged.
Final broader regression after the diagnostic:550 tests in80.220s,548 passed,
the same2 unrelated failures (exit1). Complete output inspected; no new failure
was introduced by the analysis code.

The developer's active Default mode remains in effect; the plan is recorded
here as the approved implementation ledger. Explicit authorization resolves the
execution skill's generic worktree/commit and approval suggestions. Any future
authorized commit must include this plan with its related implementation.
