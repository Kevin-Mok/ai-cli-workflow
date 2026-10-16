# Metaprompt benchmark


Raw request/response traces, runtime identifiers, trial ledgers and generated run files are private local evidence. Both benchmark `runs/` directories are ignored and removed from public history. This page retains reviewed aggregate findings and their limits; the public checkout no longer includes raw records for independently auditing those historical measurements. The harness and synthetic fixtures remain available for a new, separately budgeted run.

Source verification currently detects pin mismatches already present in the starting public revision. Preview and synthetic tests remain available, but do not start another inference run or silently repin frozen inputs. See the [source-pin incident](postmortem/2026-10-16-benchmark-source-pins.md).

For tasks as explicit as the tested summary contract, **use the original task
prompt**. The fixed minimal contract tied it. Talki and GitHub also passed that
case, with added compilation cost and no measured improvement. **There is no
supported overall skill winner, and this run cannot rank coding quality.**

This exploratory pilot ran on **gpt-6.1-sol, medium reasoning**, using Codex
subscription quota. It finished at the authorized **50-request cap**. All 14
scheduled held-out pairs were attempted; installed skills and defaults were
unchanged. These are synthetic tasks, not a sample of the user's real work.

## Executed results

Two held-out cases, seven arms, one fresh repetition per pair. Family weights
are equal. The summary case extracts decisions with missing owners/dates into
strict JSON. The coding case repairs an inclusive/exclusive window boundary,
rejects inverted bounds, and preserves the public Python signature.

| Arm | Summary | Coding | End-to-end successes | Compiler / solver requests |
| --- | --- | --- | --- | --- |
| Raw task prompt | Pass | Solver limit | 1/2 (50%) | 0 / 3 |
| Fixed minimal contract | Pass | Solver limit | 1/2 (50%) | 0 / 3 |
| Talki | Pass | Solver limit | 1/2 (50%) | 2 / 3 |
| GitHub | Pass | Solver limit | 1/2 (50%) | 2 / 3 |
| Local metaprompt-alxve | Wrong task | Wrong task | 0/2 | 7 / 2 |
| Installed metaprompt | Compiler limit | Compiler limit | 0/2 | 8 / 0 |
| Sentry | Compiler limit | Compiler limit | 0/2 | 8 / 0 |

Every arm has two attempted pairs, zero pending pairs and zero unsupported
pairs in this shared sharpening track. There were **four correct outputs, two
incorrect outputs, and eight episode-limit failures**. Six downstream sessions
returned a final answer; four passed (all on the summary case). That secondary
4/6 figure describes returned answers only; it does not replace the primary
4/14 end-to-end result. Held-out infrastructure failures and quota-truncated
pairs were both zero. Clarification continuations and observed tool-boundary
violations were zero. These counts do not establish absence of unmeasured
semantic constraint violations.

The cap was four requests per compiler and two per solver, including tool
continuations. Raw, minimal, Talki and GitHub coding solvers used their two
requests to list/read the fixture and stopped before returning code. Maintained
metaprompt and Sentry compilers spent their allowance accessing references.
Their lower completion rates show incompatibility with these tight request
limits; they do not demonstrate worse answers with sufficient tool turns.

The prepared suite contains 8 development and 24 held-out cases, four per family
across coding, research, summary, extraction, writing and templates. Only two
held-out cases and two development probes ran. The other four families, native
creation/template workflows, and the requested three repetitions remain
unexecuted under this explicit budget reduction.

## Representative evidence

- Alxve summary trial: the native save/fence/Run/Weight/go contract succeeded, but its exported prompt instructed another model to edit the task prompt and produce a changelog. The solver rewrote instructions instead of returning decision JSON. The coding trial repeated this wrong-task failure. The harness preserved that indirection; it did not silently add another optimization stage.
- Maintained summary trial: four requests read `UPSTREAM.md`, the router, general-task guidance and style guidance; no final prompt or saved artifact was produced before the limit. Sentry similarly listed files and read three references. Missing native-output flags here are consequences of the limit.
- Raw coding trial: fixture discovery/read exhausted the solver allowance. No code answer was graded. This is the clearest limitation of the pilot's coding comparison.
- Talki summary trial and GitHub summary trial: both preserved the missing-data and JSON requirements and matched the baselines' correct result.

A separate post-run agent audit inspected all finalized outputs without changing
scores. It found no observed premature execution of the embedded task by a
compiler. GitHub added clarification/check guidance; Talki's coding prompt
retained a dangling context label without demonstrated impact. This audit was
unblinded and descriptive, not a calibrated subjective judge.

## Sources and workflow coverage

The [source audit](../benchmarks/metaprompt/source-audit.md) and
[pin manifest](../benchmarks/metaprompt/sources.json) record exact revisions,
licenses, local changes and SHA-256 hashes for 71 files across five packages.
The initial comparison revisions from the guide were retained. The maintained
candidate is the installed local Majkey adapter, including four leftover legacy
references; alxve is also a local adapter. Neither is labeled unmodified upstream.
The optional unmodified Majkey ablation was omitted to conserve the budget.

| Candidate | Sharpen | Create | Template creation | Coding prompt creation |
| --- | --- | --- | --- | --- |
| Installed metaprompt | Yes | Yes | Yes | Yes |
| Local metaprompt-alxve | Yes | Yes | Yes | Yes |
| Talki | Yes | Unsupported | Unsupported | Unsupported |
| Sentry | Yes | Yes | Yes | Yes |
| GitHub | Yes | Yes | Unsupported | Yes |

This is a static source audit, not successful dynamic coverage. All five support
sharpening an existing coding draft, the operation tested here. Unsupported
workflows were not converted into failures or removed to manufacture an overall
winner. The guide's [earlier selection evidence](metaprompt-skills.md#selection-evidence)
concerns maintenance and compiler examples, not downstream superiority.

## Protocol and validity limits

The [preregistered protocol](../benchmarks/metaprompt/PROTOCOL.md) and
frozen inventory
record sources, fixtures, hidden keys, fixed minimal wording, extraction rules,
settings and shuffled order (seed 20261003). Final inventory SHA-256:
`685a65243d5251a82e1f8b75e54bb564e4b2c7758ae7ec536653ee3cd1bb76eb`.
Development corrections retained prior inventories and all failed attempts.
No candidate, fixture, scorer, runtime or selection rule changed after held-out
execution began. A separate post-run analyzer derives request-level costs only;
it does not change scores or the frozen protocol.

Each stage used a fresh process and scratch fixture, the same requested model,
medium reasoning and a 180-second timeout. All 49 authenticated responses report
`gpt-6.1-sol`. Compilers received complete pinned packages and could request
references; solver packets and hidden keys were excluded. Solvers received the
same inputs/files for every arm, without skills, competing outputs or keys.
Mutable fixtures reset between stages. One fixed clarification reply was
available within the compiler cap; none was needed. No automatic answer retries
or best-of selection occurred.

Raw used the original task prompt unchanged. Minimal prepended the frozen task
contract. Extraction took the native saved prompt, unique prompt fence, GitHub
fence, Sentry optimized-prompt section or Talki text mechanically. Ambiguous or
contradictory displayed/saved prompts fail; no adapter improves their wording.
Alxve's gate metadata stayed outside the prompt, and compilation never received
a standalone `go`. Talki's explicit Apply Mode and Sentry's full evaluation loop
were not tested.

Strict JSON scoring checks values, types, ordering and output-only requirements.
Python checks enforce boundary behavior and callable parameters using hidden
assertions in a restricted pure-function subprocess. The supplied bugs failed
and independently written repairs passed before held-out execution. Only a
limited safe standard-library surface is executable by this grader; this is not
a benchmark of unrestricted repository engineering. Prepared writing checks do
not measure subjective quality; no model judge supplied task scores.

The [runtime record](../benchmarks/metaprompt/runtime-source.json) pins Codex CLI
0.160.0 and binary hashes. Normal subscription authentication routes through a
loopback gate that reserves every outbound request before forwarding. Only three
confined fixture MCP tools receive per-tool approval. Native host actions remain
disabled/filtered; recognized host AGENTS and live-skill injections are excluded.
Actual CLI fixture read/write was verified with injected responses and zero
upstream model calls. These equal harness adaptations differ from a normal
interactive Codex workspace. The recorder omits transport authentication headers and opaque encrypted
reasoning. Raw payloads can retain runtime correlation metadata, so run
artifacts stay private; storage filtering does not alter backend requests.

## Uncertainty and selection

Paired case-cluster bootstrap results are in the
machine-readable results.
Against either raw or minimal, Talki/GitHub have a 0-point difference with nominal
95% interval [0, 0]; the other skills have a −50-point difference with interval
[−50, −50]. **These collapsed intervals are not meaningful precision:** there is
only one case per family, so stratified resampling has no within-family variation.
There is also only one repetition. Treat all rankings as exploratory.

No arm meets the frozen selection rule: at least a 10-point paired improvement
over both baselines, uncertainty excluding zero, no hard violations, and adequate
coverage. Two of six families with dominant request-limit failures cannot support
an overall winner or generalize to the user's workload.

For already explicit tasks, raw is the provisional default; minimal is equally
supported. Neither lightweight optimizer justified its extra first-use cost on
the successful summary case. Talki/GitHub remain optional alternatives for
sharpening existing drafts, with no demonstrated quality advantage here. For
creating prompts/templates, the maintained `$metaprompt` remains the provisional
choice based on workflow support and maintenance evidence only. This pilot did
not measure its downstream quality. No installed default was switched.

The smallest useful follow-up is a diagnostic on a **fresh coding fixture**:
raw, minimal, Talki and GitHub, three fresh repetitions, compiler limit four and
solver limit six. Its strict upper bound is 96 requests, plus any separately
budgeted development probes. It would remove the observed solver bottleneck;
it still would not decide the overall authoring skill. A later balanced six-family
holdout must also allow maintained metaprompt/Sentry enough compiler turns and
include dynamic creation/template workflows. Additional runs require new budget
authorization and fresh cases; none were launched.

## Tokens, latency and costs

The ledger reconciles **41 held-out requests + 8 development requests + 1 setup
attempt = 50**. Setup returned an unauthenticated HTTP 401 with unknown token
usage. Development includes three requests lost to a diagnosed MCP approval
configuration failure; that attempt remains archived. Three other archived
infrastructure attempts forwarded zero inference requests. Held-out runs had no
infrastructure retries.

Request-level analysis
measures all 49 authenticated requests, including capped episodes: **329,058 input
tokens**, of which **158,080 were cached**, and **5,757 output tokens**, including
719 reasoning tokens. Summed measured stage wall time was **339.0 seconds**,
including development and archived failures; it excludes authoring, user wait
and the unmeasured setup duration. Deterministic grading used zero model calls
and about 0.0004 seconds of recorded grading time; the first development grading
duration was not recorded.

The frozen runner's `measured_usage` field contains CLI completed-turn totals
only and misses aborted-turn usage. The separate analyzer uses the preserved
per-request metadata, checks reconciliation with the ledger, and records hashes
of its script, results and protocol. Use that analysis for comprehensive costs.

The following are totals across each arm's **two held-out attempts**, including
failures; they are not estimated costs per successful completion. Input includes
cached tokens, and output includes reasoning tokens.

| Arm | Requests | Input tokens | Cached input | Output tokens | Stage seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Raw | 3 | 14,666 | 4,736 | 117 | 14.6 |
| Minimal | 3 | 14,749 | 0 | 77 | 10.3 |
| Talki | 5 | 31,967 | 4,736 | 400 | 30.9 |
| GitHub | 5 | 33,784 | 4,864 | 859 | 49.7 |
| Alxve | 9 | 62,200 | 32,896 | 3,021 | 126.2 |
| Maintained metaprompt | 8 | 63,748 | 41,728 | 257 | 29.6 |
| Sentry | 8 | 54,463 | 37,248 | 254 | 28.4 |

On the successful summary case, first-use Talki took two requests and 15.4 seconds;
its solver component took one request and 7.0 seconds. GitHub took two requests
and 26.5 seconds, with one solver request and 5.0 seconds. Raw used one request
and 4.5 seconds. Reusing a compiled prompt avoids compilation, but repeated
reuse/cache behavior was not executed. The analyzer separates compiler and
observed solver components; absent solver episodes are not successful zero-cost
reuse. Single observations do not support stable latency rankings.

Actual subscription dollar cost and remaining account quota are unknown.
Authoring, preparation-agent and qualitative-audit usage are unmeasured and are
not represented as zero; the 50-request gate applies to benchmark inference.
Official [model information](https://developers.openai.com/api/docs/models/gpt-6.1-sol),
[API pricing](https://developers.openai.com/api/docs/pricing),
[noninteractive execution](https://learn.chatgpt.com/docs/non-interactive-mode)
and [configuration](https://learn.chatgpt.com/docs/config-file/config-reference)
were retrieved on 2026-10-03. API prices do not establish subscription charges.

## Replay and verification

From the repository root with Python 3; no sudo is required. These commands use
no model quota:

```bash
python3 scripts/metaprompt-benchmark.py verify
python3 scripts/metaprompt-benchmark.py dry-run
python3 -m unittest discover -s tests -p 'test_metaprompt_benchmark*.py' -v
```

The authenticated Codex CLI is needed for an authorized incomplete run:

```bash
python3 scripts/metaprompt-benchmark.py run --phase development
python3 scripts/metaprompt-benchmark.py run --phase holdout
```

The original private run finished at its cap. A public checkout does not
include its ledger, so the execution commands above are not read-only rechecks.
Restore privately retained records or authorize a new budget before execution.
The offline `report` and analysis commands also require those private records. Only diagnosed pre-holdout development infrastructure fixes may use
`refreeze-development` and `--retry-infrastructure`; this scored run cannot be
refrozen. Another experiment needs a separately authorized budget and new run.

The [ExecPlan](../plans/benchmark-metaprompt-skills.md) records tests, protected
pre-existing work, review and rollback. [Smoke tests](smoke-tests.md#skills-and-docs)
cover the reusable commands. Incidents retain the
[sandbox failure](postmortem/2026-10-03-metaprompt-benchmark-sandbox-startup.md),
[validation corrections](postmortem/2026-10-03-metaprompt-benchmark-validation.md),
[runtime failures](postmortem/2026-10-03-metaprompt-benchmark-trial-infrastructure.md),
[source lookup issue](postmortem/2026-10-03-metaprompt-runtime-source-fetch.md) and
[setup request](postmortem/2026-10-03-runtime-red-test-uninjected-upstream.md).

Final verification: 47 benchmark/analysis tests passed; source verification,
report/analysis rebuild, whitespace/link/credential-field checks and README
validation passed. Both resume commands left the ledger and every raw trial
byte-for-byte unchanged and made no requests. Static type/lint executables were
unavailable; Python syntax checks passed. An independent review reconciled all
result, request and cost totals with the saved evidence.

Paste-ready Cursor handoff:

> Read plans/benchmark-metaprompt-skills.md and docs/metaprompt-benchmark.md.
> Preserve all pre-existing work, frozen sources and trial evidence. Run the
> benchmark tests, verify, dry-run, report and analysis commands. Confirm the
> 50-request ledger is unchanged and report hashes reconcile. Do not rerun or
> tune scored cases, change installed skills, or authorize additional quota.
> A new experiment needs fresh held-out cases, a separate ledger, and explicit
> user budget approval. Keep related documentation and plan updates together.

Suggested commit: `feat(benchmarks): add metaprompt pilot harness`. Keep the
harness, source snapshots, fixtures, evidence, tests, report, incidents and plan
in the same focused change. No commit or push was requested or performed.
