# Metaprompt benchmark implementation and pilot

## Purpose and observable outcome

Execute the supplied benchmark specification (`prompts/benchmark-metaprompt-skills.md`)
and deliver a reproducible, resumable harness, immutable source pins, synthetic
fixtures, sanitized trial evidence, and a recommendation limited to measured
downstream results. The user authorized a **50-model-call pilot** on Codex
subscription quota with **gpt-6.1-sol, medium reasoning**, both stages.

Delivery note: that original request file and its compilation plan pre-date this
Codex session and are excluded from the session-only commit. The committed
[pilot protocol](../benchmarks/metaprompt/PROTOCOL.md), frozen manifest and
fixtures contain the implemented pilot contract and support replay independently.

## Context and scope

The existing [guide](../docs/metaprompt-skills.md) has maintenance evidence and
four compiler-only examples. Neither establishes downstream performance. Read
the canonical instructions, ExecPlan contract, durable preferences, relevant
lessons, skill provenance and evaluation helpers. This task executes the saved
specification; runtime mode is Default, so record the plan here without
pretending to switch modes or asking again for implementation authorization.

New code/data live under `benchmarks/metaprompt/`, with a reusable entrypoint
under `scripts/` and meaningful tests under `tests/`. Update only relevant
passages in README, the skill guide, and smoke tests. No installed skill,
default, Git worktree, commit, push, or production setting changes.

## Assumptions and decisions

- Five independent skill candidates plus raw and fixed minimal baselines.
  The installed Majkey and alxve packages are local adaptations, not claimed
  to be their unmodified upstreams. Optional Majkey ablation is omitted to
  preserve the explicit budget.
- Prepare 8 development and 24 held-out synthetic cases, four held-out per
  family. Execute a smaller preregistered subset as a pilot, preserving the
  full suite for later runs. Never claim these represent observed user tasks.
- Count actual inference requests where the runtime exposes/enforces them.
  Never substitute 50 multi-call sessions for 50 model calls. Runtime audit
  must establish the bound before inference; unavailable measurement is null.
- Source inspection, fixture creation, and runtime investigation are separate
  bounded subagent tasks, as required by repository coordination instructions.
  Their authoring effort is preparation overhead, outside trial inference;
  unavailable usage remains unknown.
- Deterministic scoring is primary. Subjective quality without an independent
  calibrated judge remains unmeasured; it cannot support a winner.
- Equal family weights, hard constraint violations cannot be offset by cost,
  paired resampling at case level, exploratory comparisons, practical minimum
  improvement 10 percentage points, and uncertainty before recommendation.

## Ordered implementation checklist

- [x] Capture initial status and read relevant context before modifying files.
- [x] Record sandbox startup incident and successful elevated read fallback.
- [x] Resolve target and budget with user; use gpt-6.1-sol / medium / 50 calls.
- [x] Pin complete candidate packages, hashes, licenses, scope and adapters.
- [x] Prepare and check 8 development / 24 held-out fixtures and hidden keys.
- [x] Write defining tests for scoring, failure accounting, budget, isolation,
  immutable protocol and resumption; observe RED before implementation.
- [x] Implement harness and controlled runtime, then obtain GREEN.
- [x] Freeze protocol, minimal baseline, subset/order, scoring and limits.
- [x] Execute development pilot before held-out trials; no holdout tuning.
- [x] Produce machine-readable results, cost/usage limitations and report.
- [x] Update guide, README, smoke tests and this plan; verify fresh and review.

## Risks, protected dirty state and rollback

Initial status already contained modified README, smoke tests, skill catalog,
feedback, metaprompt files, lessons and contract tests; new guide, upstream
imports, alxve, integration tests, several plans/prompts/postmortems, and SSH
documentation. Preserve all of it. Make additive benchmark-specific edits;
stage nothing. Rollback removes new benchmark files and only this session's
document hunks. Plan and incident belong with matching work in future commits.

Sandbox startup currently fails at loopback configuration. Shell operations
use reviewed scoped escalation. Model tools must not gain host access as a
workaround. Unknown runtime call controls are a blocker to inference, not a
reason to exceed budget. User-auth and machine caches must never enter artifacts.
No tracked machine configuration changes are planned; `refresh-config` would
change installed state outside the prompt's explicit isolation requirement.

## Exact verification

- `python3 -m unittest discover -s tests -p 'test_metaprompt_benchmark*.py' -v`
  for RED then GREEN, including recorded compiler failures and pending runs.
- `python3 scripts/metaprompt-benchmark.py verify` for manifest integrity and
  fixture/schema checks; no model calls.
- `python3 scripts/metaprompt-benchmark.py dry-run` for schedule/cost bounds;
  must not use quota or mutate trial evidence.
- `python3 scripts/metaprompt-benchmark.py run` for authorized resumable pilot;
  frozen protocol and runtime feasibility checks precede any model request.
- `python3 scripts/metaprompt-benchmark.py report` rebuilds measured results
  from immutable raw evidence without inference.
- Existing metaprompt contract/integration/helper suites for nearby regressions.
- `git diff --check`, untracked-file whitespace check, source-pin revalidation,
  artifact secret screening and independent review of scoring/denominators.
- Manual dry-run and resume smoke entries use exact commands in the shared doc.

## Progress, evidence and review notes

- Initial four shell reads exited 1 before execution (`bwrap` network namespace
  startup). Elevated retries exited 0 and captured status. See
  [incident](../docs/postmortem/2026-10-03-metaprompt-benchmark-sandbox-startup.md).
- Local default was gpt-6-astra/max; user explicitly replaced the benchmark
  runtime with gpt-6.1-sol/medium. No API keys in shell; subscription requested.
- Initial checkpoint: no trial model calls had run before runtime and source
  inspection. Subsequent development evidence is recorded below; full-suite
  results are not claimed.
- Preparation completed: 71 pinned files across five skills, plus two baselines;
  all hashes verified. Installed maintained metaprompt includes four stale legacy
  reference files, preserved in its snapshot and explicitly identified.
- Local initial RED: nine behavioral tests failed for absent implementation.
  GREEN: initial ten tests passed after the documented collision exception fix.
  Independent review added regressions for ambiguous extraction, legacy gate
  validation and partially attempted budget stops. Latest combined run passed
  26 tests (exit 0); runtime tests continue to evolve during development only.
- Nearby regression suites passed: legacy contract 12, integration 7, upstream
  helpers 10, all exit 0. Five supplied buggy code fixtures failed the real
  scorer as expected. Syntax parsing passed. No installed mypy, pyright, ty or
  ruff executable was found; static type/lint checks remain unavailable.
- Frozen initial protocol and corrected development version retained. Two
  development attempts failed before inference, first on host context and then
  on missing fixture tools. Infrastructure evidence and prior attempts are
  durable. Global ledger reserves one accidental unauthenticated setup request
  (HTTP 401); no successful inference has occurred at this checkpoint.
- The source audit and runtime investigation were independently reviewed. The
  chosen pilot is all seven arms on two shared sharpening cases, one repetition;
  all other families and dynamic workflow coverage remain prepared only. This
  explicit reduction follows the user's 50-call pilot cap and cannot establish
  an overall winner. Exact protocol lives in
  [PROTOCOL.md](../benchmarks/metaprompt/PROTOCOL.md).
- Development raw extraction passed with the requested served model. The next
  compiler used three requests, but Codex refused both fixture MCP operations
  because they required approval under a noninteractive policy. This is a
  harness failure, not skill evidence. Five total requests are reserved,
  including setup. No held-out trial has started. Correct only the confined
  fixture tool approval configuration, verify it offline, retain the failed
  attempt and refreeze before retrying development.
- Pre-holdout review fixed displayed/saved prompt disagreement, public Python
  signature checks, and standalone report freeze verification. Their new RED
  tests failed as expected; the fresh combined suite passed **45 tests**, exit 0.
  All five buggy Python fixtures failed and independently written correct
  repairs passed. Source verification returned 32 cases, 7 arms, 71 pinned files.
- Actual CLI fixture read/write passed with synthetic upstream responses and
  **zero model requests**. Only the three confined fixture tools have explicit
  per-tool approval; host tools and Code Mode host remain disabled. The failed
  development attempt retains its original recorded status and raw evidence,
  with the diagnosis explicitly correcting it to infrastructure failure.
- Final development compiler read four pinned references successfully, then
  reached the preregistered four-request episode cap before producing its
  artifact. This valid workflow failure is retained without a result-dependent
  retry. Total ledger at held-out start: 9/50 requests. Final protocol frozen;
  no further changes to benchmark inputs are allowed during scored execution.

## Final evidence and handoff

- Frozen held-out execution completed all 14 pairs: 4 successes, 2 wrong-task
  answers, 8 episode-limit failures. No pending, unsupported, quota-truncated,
  or infrastructure-failed held-out pairs. The cap stopped further requests at
  exactly 50: 41 held-out, 8 development and 1 setup attempt. No scored retry or
  post-holdout change to candidate/fixture/scorer/runtime/selection inputs.
- All 49 authenticated responses reported `gpt-6.1-sol`; request payloads use
  medium reasoning. Primary scores provide no overall winner. Tight solver
  caps preclude coding-quality conclusions; the report explicitly recommends
  the raw baseline only for comparably clear tested tasks.
- Added `scripts/metaprompt-benchmark-analysis.py` as a separate post-run
  reporting layer. CLI turn totals omit capped episodes, so it uses preserved
  request-level usage, checks the ledger, and hashes its inputs/script. It
  neither edits nor rescores the frozen experiment. Its two defining RED tests
  failed before implementation and passed after it.
- Final `python3 -m unittest discover -s tests -p
  'test_metaprompt_benchmark*.py' -v`: **47 tests passed**, exit 0, 16.978 seconds.
  Earlier adjacent suites remain recorded above (12 + 7 + 10 passing tests).
- Final `python3 scripts/metaprompt-benchmark.py verify`: exit 0, 32 cases,
  7 arms and 71 pinned files. `dry-run`, `report`, both `run --phase` resume
  commands, and the analysis script exited 0. SHA-256 comparisons before/after
  proved the quota ledger, protocol and every raw/archived trial unchanged.
  Resuming this complete run made no model requests.
- Comprehensive known usage: 329,058 input tokens (158,080 cached), 5,757 output
  tokens (719 reasoning), 339.0 seconds summed stage wall time. Setup usage,
  subscription dollar cost, and preparation/audit usage remain unknown.
  Deterministic grading uses zero model calls. Saved request accounting includes
  aborted episodes; repeated prompt reuse was not executed.
- Fresh `git diff --check` and `./scripts/executable_readme-recruiter-sync
  /home/example/linux-config` passed (README: `pass_no_change`). Owned-file
  whitespace, Python syntax, report/plan local links, and saved artifact
  credential-field screening passed. Static type/lint executables remain
  unavailable, as recorded above.
- Independent final review recomputed request-level analysis and verified the
  report's scores, denominators, collapsed uncertainty intervals and limitations.
  A separate read-only output audit covered all 14 trials; no observed premature
  compiler execution. Neither audit changed scores or consumed benchmark quota.
- README, guide, smoke tests, report, incident resolutions and this plan match
  the delivered commands. One append-only local engineering lesson records the
  runtime/accounting pitfall. No installed skill/default or tracked machine
  configuration was changed; no refresh, worktree, commit or push was performed.
  Preserve the original dirty work when preparing any future focused commit.

The [report](../docs/metaprompt-benchmark.md) includes exact replay commands,
automated/manual checks, artifact links, the Cursor handoff, Conventional Commit
suggestion, and the smallest useful newly budgeted follow-up. Rollback remains
removal of benchmark-owned files plus only their additive documentation hunks;
do not erase quota evidence to reuse the authorization.
