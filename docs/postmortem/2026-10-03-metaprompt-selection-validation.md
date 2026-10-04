# Metaprompt selection validation

## Premature candidate inspection

- Symptom: a read-only `rg --files` inspection returned exit 2 because
  `benchmarks/metaprompt-selection/candidates/` had not yet been published by
  the source-audit agents.
- Impact: no data changed and no model quota was consumed. The independent
  offline CLI integration check in the same batch passed all three tests.
- Evidence: `rg: benchmarks/metaprompt-selection/candidates: No such file or directory`.
- Root cause: parent inspected an asynchronously produced path before the
  producing agent reported completion.
- Resolution/status: stop dependent inspection until publication; continue
  independent harness work. Source manifests and hashes will be verified after
  agent completion.
- Follow-up: check producer completion or path existence before dependent reads.

The same premature-read mistake recurred for `research/cross-review.md` while
the agent was still writing it (read-only `sed`, exit 2). No data or quota was
affected. The parent must wait for the producing agent's completion message,
not a progress message, before reading its final artifact.

## Public web cache misses

- Symptom: web extraction of the senior June 11 commit and Sentry's abbreviated
  May 4 commit URL returned cache misses. Wshobson's August 15 diff loaded.
- Impact: no benchmark or quota impact; no inference drawn from missing pages.
- Evidence: web results reported `Failed to fetch ...: Cache miss`.
- Resolution: use already collected full immutable commit IDs and primary
  authenticated GitHub API reads; cross-review those receipts independently.
- Follow-up: retain full commit URLs and local audit receipts in the report.

## Development copy-span ambiguity

- Symptom: the minimal control returned `audit the kiosk.` while the development
  key expected `audit the kiosk`; the fixture said to copy the wording after
  `Decision:` from a sentence ending with a period.
- Impact: this unscored calibration case has an ambiguous exact-match failure.
  The runtime completed normally and all reservations remain charged.
- Evidence: `selection-dev-create-brief--minimal.json` contains the source,
  output and `json_mismatch` score. No held-out outputs had been observed.
- Status: preserve the development observation; audit all held-out copy spans
  for explicit boundaries before freezing. Do not tune held-out keys to outputs.
- Next step: use quoted/bracketed or otherwise unambiguous source spans wherever
  exact verbatim comparison is required, and document the calibration limitation.

## Broader repository test failures

- Symptom: full unittest discovery completed 514 tests with two failures
  (exit 1); focused selection tests had passed 26 tests.
- Impact: the broader repository is not fully green. Complete output is retained
  at `/tmp/metaprompt-selection-repo-tests.log`; no benchmark inference used by
  the test suite.
- Status: identify both failure names and attribution before deciding whether
  they are safe, related fixes or unrelated pre-existing issues.
- Next step: inspect full failure tracebacks and report exact unresolved results.

Attribution: `test_push_policy_is_consistent_in_active_workflows` expects an
exact policy sentence absent from the existing commit-dirty skill;
`test_exact_sanitized_tree_exists_without_unapproved_files` finds an existing
`05 Daily Notes/2026-07-22.md` vault note outside its expected inventory. Neither
surface is touched by this benchmark. Preserve both and report them as unrelated
failures (512/514 passed in that full run).

Fresh full discovery after the final runtime changes ran 543 tests in 79.703s
(exit 1): 541 passed and the same two unrelated failures remained. Complete
output is `/tmp/metaprompt-selection-final-repo-tests.log`. The 55 focused
selection tests passed before protocol freeze. No unrelated fix was attempted.

After the seven derivative analysis tests were added, full discovery ran 550
tests in 80.220s (exit 1): 548 passed, with exactly the same two failures.
The complete output was inspected at
`/tmp/metaprompt-selection-final-repo-tests-v2.log`. All 62 focused selection
and analysis tests pass; no frozen implementation changed after execution began.

## Serial native tools consumed development allowance

- Symptom: Sentry exhausted its ten compiler requests after reading four
  references, saving three inputs, running a real baseline evaluation, and
  starting a candidate. It had not yet emitted its final native package.
- Cause: every serial reference/file operation required another inference;
  the first integration had only single-file tools. This reproduced part of the
  earlier pilot's discovery/IO overhead despite the higher stage ceiling.
- Resolution in progress: add confined batch read/write tools so native
  references and related files can be handled per request. Preserve every first
  development result and its quota charges. A second full development round uses
  the ten spare trial slots:20 development +80 scored=100 total, evenly20/arm.
- Verification: test batch paths/collisions and real CLI integration, then rerun
  development under the same ten-request stage/2,000-request global ceilings.

## Native final-link extraction caused a redundant continuation

- Symptom: Wshobson round2 created and evaluated a final prompt, reported
  `FINAL PROMPT` as a Markdown link, then the harness unnecessarily restarted
  authoring and exhausted the compiler allowance.
- Evidence: its preserved first compiler reply says `Optimization Complete!`
  and links `prompts/final_prompt.txt`; baseline and final public evals both
  completed 12/12. The adapter accepted plain final paths but missed a bold
  label plus Markdown link. Two continuation requests were wasted and remain
  charged.
- Root cause: incomplete mechanical native-output extraction, not prompt
  failure. The stage interpreted an unrecognized complete artifact as needing
  clarification.
- Resolution in progress: add a defining extraction regression, accept explicit
  final Markdown links, and permit development-only continuation into the unused
  solver stage from the original successful compiler reply. Archive the original
  trial, keep all compiler requests and failure evidence, and never rerun a
  consumed compiler or solver. No extra trial or request allowance is granted.

## Restricted Python omitted a standard iterator exception

- Symptom: a correct raw development repair used `next(iter(values))` and caught
  `StopIteration`; the checker raised NameError because the exception was absent
  from its restricted builtins. Public RED/GREEN actions completed normally.
- Evidence: `selection-dev-coding-bounds--raw--d2.json` retains submitted code
  and the checker traceback. A focused reproducer failed for the same reason.
- Root cause: `iter`/`next` were permitted without their standard exhaustion
  exception, making the execution environment inconsistent with Python.
- Resolution: allow standard safe exception classes; the same executable
  reproducer now passes. Preserve the original development score and classify
  it as a checker defect, not evidence against the raw control.
- Follow-up: freeze only after the repaired checker passes reference and
  regression tests; do not change held-out answers to fit outputs.

Calibration resolution: batch tools, explicit final Markdown-link extraction,
and standard iterator exceptions all passed their defining regressions before
freeze. Both rounds remain charged: 20 development attempts and 169 requests.
Only three unused solver stages resumed from original completed compiler
artifacts; the original records are archived in `development-recovery/`, and
no compiler was rerun. All round-two handoffs completed. Candidate task errors
remain errors; readiness verifies working infrastructure, not perfect answers.

## Analyzer protocol-path read

- Symptom: an analyzer preparation read guessed `protocol.json` at the package
  root and returned a missing-file error.
- Impact: read-only, no model calls, no held-out outputs inspected or files changed.
- Resolution: use the documented `runs/selection-2026-10-03/protocol.json` path.
  Analyzer ownership remains limited to two new, unfrozen derivative files.

## Stale allocation summary in frozen metadata

- Symptom: the independent runtime audit found `allocation.total=90` and
  `allocation.development_per_arm=2` in the frozen settings, although the actual
  frozen schedule contains 100 rows: 20 development and 80 held-out.
- Impact: the descriptive summary is stale after the second calibration round.
  Actual reservations, scheduled identities and 80 balanced held-out rows use
  the correct allocation; the 100-trial and 2,000-request caps remain enforced.
- Root cause: round-two schedule expansion did not update the allocation
  helper's original summary fields.
- Resolution: preserve frozen bytes. The report and derivative analyzer use the
  actual frozen schedule and durable ledgers, and disclose the discrepancy.
  The analyzer does not consume the stale fields. No scoring, execution or
  ranking change is made after freeze.
- Follow-up: a separately authorized future harness version should derive
  summary allocation fields from its final schedule and test their agreement.

## Documentation patch context mismatch

- Symptom: a multi-file documentation patch was rejected because its final,
  unnecessary context hunk did not match the report.
- Impact: no model requests or frozen inputs were involved. Inspect both target
  files before retrying, because a multi-file patch can leave earlier hunks.
- Root cause: an unused trailing context hunk was included in the patch.
- Resolution: remove that hunk and apply only the current, inspected sections;
  verify the resulting report and smoke-check text.

## Frozen eligibility labels are broader than authorization failures

- Symptom: read-only source review found that the inherited Python scorer labels
  Markdown-fenced code `output_format` and all AST allowlist rejections
  `unsafe_code`. Both frozen summarization and derivative analysis exclude a
  candidate arm for any top-level hard-failure label.
- Discovery timing: 16 held-out outcomes existed, with zero held-out coding
  records. An independent reviewer confirmed this from source alone, without
  inspecting candidate answers.
- Impact: the filter also covers format mistakes and unsupported pure Python;
  those labels do not establish a serious authorization violation. Actual
  fixture scope denials use the separate `unauthorized_tool_access` label.
  Artifact-only fixture-score labels do not propagate to arm eligibility.
- Root cause: a broad inherited failure bucket was reused for a narrower
  planned eligibility rule without separating its semantic categories.
- Resolution/status: preserve the frozen scores and ranking. Describe the
  actual filter as strict contract/execution-boundary eligibility, list any
  observed labels and their effect, and never call a format or unsupported-code
  rejection an observed security incident. Assess impact when all rows finish.
- Follow-up: a future benchmark version should give task-contract, unsupported
  execution-boundary, and actual authorization outcomes distinct fields before
  freezing. No held-out regrading or code change is made here.

## Held-out final candidate was not handed downstream

- Symptom: `selection-sharpen-extraction-quotes--alireza-senior` completed ten
  compiler requests but recorded `compile_failed/no_unambiguous_final_prompt`.
- Evidence: the saved compiler output labels a fenced prompt
  `FINAL PROMPT — candidate, structural gate failed`, names
  `prompts/final_prompt.txt`, then uses another text fence for metric results.
  The native static gate also failed (clarity 90 to 85); its public evaluations
  reported 12/12 with no regression. No solver request was made.
- Root cause: the mechanical handoff did not recognize this final-candidate
  presentation. The native process separately remained incomplete because its
  static clarity gate failed. These are distinct observations.
- Impact: frozen end-to-end success is false, but downstream prompt quality is
  unmeasured. Do not call it an observed wrong downstream answer.
- Resolution/status: retain the original record, score and charges; disclose
  this adapter limitation with a direct trial link. No held-out recovery,
  parser change or additional inference is permitted in this frozen run.
- Follow-up: include explicit final-candidate labels, multiple metric fences
  and `Saved as` artifact lines in a future version's pre-freeze contract tests.

The same limitation also affected
`selection-template-conflict--sentry-prompt-optimizer`: its explicit
`Optimized Prompt — FINAL HANDOFF` heading is followed on the next line by the
link to `prompts/final_prompt.txt`. The final template exists and the report
contains all eight human-readable sections, but the extractor expects a label
and link on the same line, and the native section matcher does not accept this
heading suffix. It records an unmeasured downstream outcome and a missing
Optimized Prompt section. Preserve both frozen observations and disclose the
adapter cause; do not interpret them as a bad downstream answer or as proof
that the skill omitted its final prompt. Bound any possible ranking effect
without inventing a downstream result.

`selection-coding-headers--alireza-senior` is a third observed handoff variant:
it writes `FINAL PROMPT — prompts/final_prompt.txt` followed by an underline
and the prompt text. The artifact exists, but the parser recognizes a colon
or same-line Markdown link, not this em-dash form. Its downstream stage is
unmeasured. Separately, its native same-case baseline/final evaluation pair
was not observed; a written claim of 10/10 simulation is not sufficient proof.

`selection-coding-chunks--alireza-senior` adds a fourth observed handoff failure:
`FINAL PROMPT —` followed by the backticked final artifact path and prompt text.
It has the same em-dash presentation limitation as the headers case, plus a
separate unobserved same-case evaluation pair. At the clean pause, all four
handoff failures remain charged and have no downstream solver result.

## Inline template binding makes the draft control ambiguous

- Symptom: both controls fail `selection-template-draft` by retaining extra
  text in the final fact. Inspection shows the raw template places
  `{{message_data}}. Keys ...` inline. After multiline substitution, the final
  `Fact: funding unknown` shares a line with the period and later instructions.
- Evidence: the public contract says to preserve the remainder of each Fact
  line verbatim; raw includes the following instructions and minimal includes
  the appended period. The hidden key expects only `funding unknown`.
- Root cause: a line-exact copy rule was added without delimiting the multiline
  variable in the rendered raw template. The public rendered boundary is
  ambiguous, so this is not clean evidence of inferior control task ability.
- Resolution/status: preserve primary frozen outcomes and every charge. Add a
  clearly labeled post-hoc sensitivity comparison omitting this one case from
  every arm, retaining equal workflow weighting. It does not change the frozen
  recommendation, rerun a model, or assign an invented correct answer.
- Follow-up: validate rendered templates with adversarial multiline values,
  including their final line, before future freezes. Report both primary and
  sensitivity control comparisons and their limits.

A documentation patch initially included an unrelated plan-context hunk and
was rejected before writing. This repeats the context-mismatch incident above;
the corrected patch contains only inspected context and touches no frozen file.

## Final impact and verification, 2026-10-04

The user resumed the clean pause. Exactly five remaining trials completed, all
successfully, and the runner exited 0 at 100 attempts / 754 requests. The
primary report and independent derivative calculation agree: Sentry 14/16,
Wshobson 13/16, Senior 11/16, both controls 15/16. All six compiler-limit and
four adapter-handoff failures remain unchanged and charged. No held-out
recovery, parser repair or additional grading inference occurred.

The overbroad hard-label filter has no observed eligibility effect: every
held-out arm has zero labels. Final saved-output inspection shows the section
matcher limitation is broader than the one failed Sentry handoff: twelve of
sixteen reports use an `Optimized Prompt — FINAL`/`— FINAL HANDOFF` suffix
which the strict matcher rejects. One other report hits the compiler cap.
Its recorded native-check count is therefore 3/16, while fourteen usable
prompts reached correct downstream results. Those measurements are reported
separately without rewriting the recorded flags. Wshobson's vacuous flag and
Senior's 9/16 native checks are likewise disclosed.

The ambiguous-template omission is implemented only in the unfrozen derivative
analyzer. It gives raw/minimal 100%, Sentry 85.42%, Wshobson 81.25% and Senior
66.67% under unchanged 25%-per-workflow weighting. Primary scores, selection,
original artifacts and charges remain unchanged.

Fresh focused verification passed 62 tests (exit 0), all 27 pinned package
files, 26 reference answers and seven coding RED/GREEN pairs. All 54 selection
and 82 historical frozen inputs still match. Both final aggregates reconcile
754 observed/reserved requests with no missing usage or integrity errors;
all requests requested/served gpt-6.1-sol/medium with HTTP 200, within the
ten-request stage limits. The last broader run remains 548/550 with the two
attributed unrelated failures above. Frozen defects remain documented limits
for a separately authorized future harness version, not silently repaired facts.
