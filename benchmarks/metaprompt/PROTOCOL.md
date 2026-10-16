# Metaprompt pilot protocol


Raw run artifacts are private local output under the ignored `runs/` directory. Public aggregate findings are retained in `docs/metaprompt-benchmark.md`; the public history excludes request traces, runtime identifiers and raw ledgers.

For a native save contract, the verified saved prompt must match the single
displayed prompt fence, ignoring terminal newline characters only. Contradictory
saved and displayed prompts are compilation failures; extraction cannot choose
one to conceal the discrepancy.

Written before scored outputs on 2026-10-03. The machine-readable frozen
inventory in `runs/pilot-2026-10-03/protocol.json` records exact hashes, settings,
schedule and baseline wording. Any development-only protocol corrections retain
the prior inventory in `protocol-history/`; held-out execution forbids revision.

## Scope and selection

The user authorized Codex subscription usage, **gpt-6.1-sol / medium** for both
stages, with a hard **50 outbound inference-request cap**. This replaces the
original broad experiment with an explicitly limited pilot. An accidental
unauthenticated setup request returned 401 and conservatively reserves one of
those attempts. Native tool continuation requests, scripted clarifications,
transport errors, and retries all consume the same durable cap before forwarding.
Preparation-agent usage is unavailable and is reported separately as unknown.

Development probes: raw baseline on `dev-extract-inventory`, then the maintained
adapter on `dev-guide-summary`. All seven variants are scheduled on
`hold-summary-partial` and `hold-coding-window`. Both receive the shared request
to sharpen an existing task prompt, including the coding draft; Talki supports
this operation. Each pair has one repetition. Candidate order is randomized
within each case with seed 20261003. No result-dependent repeats or best-of
selection. The planned schedule has 16 end-to-end trials and a lower bound of
28 requests including the setup reservation; tool continuations increase this
up to the enforced ceiling of 50. Stop on infrastructure error for diagnosis.

The prepared suite retains 8 development and 24 held-out synthetic cases, four
per family. Research packets are fixed synthetic documents, not real web facts.
The guide's four examples appear only in development. No held-out output may be
used to tune candidates, extraction adapters, scoring, or selection.

## Two tracks and denominators

1. **Shared improvement:** all seven candidates, two task families, one repeat,
   14 scheduled held-out end-to-end pairs. Unsupported cases are never counted
   as failures. These two existing-draft cases are supported by all candidates.
2. **Workflow coverage:** the source audit classifies creation, sharpening,
   reusable templates, and coding-agent creation; 32 fixtures are prepared.
   Dynamic creation/template/coverage trials are **not executed in this pilot**.
   Static support is not evidence that a workflow succeeded.

This reduction sacrifices the requested three held-out repetitions and four
families under the explicit budget. It cannot establish the best overall skill
for the user's work. Narrow candidates cannot win through omitted categories.

## Runtime and interaction

Every compiler/solver episode starts a fresh ephemeral Codex process and fresh
scratch fixture. Same model, medium reasoning, 180-second timeout, filtered MCP
tool environment, fixed inputs and retry policy for all variants. Compilers may
make four inference requests; solvers two. A compiler that ends with a question
and no usable artifact/fence receives at most one fixed scripted reply, sharing
its four-request budget. No standalone legacy `go` is sent during compilation.
The separate solver receives the accepted prompt in a new session.

Complete pinned skill instructions and references are available, with the
entrypoint in initial context and relevant references selected by the compiler.
MCP exposes only relative `read_file`, `list_files`, and exclusive `write_file`.
Compiler writes are limited to `prompts/`; a coding solver may replace only its
declared target fixture file, and other solver artifacts are limited to
`artifacts/`. A modified target and the returned code must both pass hidden checks.
The compiler receives neither task packets nor answer keys. The solver receives
the same task packets/files under every arm, with no skill instructions, other
outputs, or answer keys. Mutable scratch fixtures are recreated every episode.

Codex subscription authentication stays inside normal CLI handling. A custom
provider routes inference through an ephemeral loopback quota gate to the normal
official backend. It forwards no request without a durable permit. No headers or
credentials are logged. Native tool definitions are identically filtered to the
three fixture tools and unexpected native actions are rejected before execution.
Only those three confined fixture tools receive explicit per-tool approval;
global noninteractive approval and disabled host tools remain in force. An
offline synthetic-response probe verifies actual CLI read/write execution
without inference. Persisted payloads omit opaque encrypted reasoning blobs;
the requests forwarded to the backend are unchanged by that log redaction.
Host-injected instructions are excluded using an explicit reviewed adaptation;
candidate instructions remain intact. Buffered transport latency is wall time,
not time to first token. This controlled runtime differs from an unrestricted
interactive Codex workspace. Installed skills and defaults are untouched.

## Baselines, extraction and failures

Raw is the original `task_prompt`, unchanged. Minimal prepends the literal task
contract in `fixture-notes.md`; both receive identical solver inputs. Template
bindings, when run in a future suite, are applied once after compilation; changed
slot sets fail. No template input is disclosed to its compiler.

Extraction is mechanical: a uniquely identified saved artifact, a single prompt
fence, GitHub's single chat fence, Sentry's `Optimized Prompt` component, or
Talki's complete native text. Multiple prompt fences fail as ambiguous. Store
the full native output and adapter label; never rewrite the extracted prompt.
The local skills must fulfill their actual prompt/save metadata; alxve must
also show Run/Weight/go. Missing contract elements fail compilation. Its native
rewrite-prompt output is sent downstream unchanged, not secretly rewritten.
Sentry's larger native evaluation loop is not claimed to run. Talki is tested
on existing-prompt optimization, not explicit Apply Mode.

Compilation failures count in end-to-end denominators. A global quota stop after
compilation counts as an attempted truncated trial; never-started pairs remain
pending. Infrastructure failures are separately labeled and retained, including
failed development attempts. They are not reclassified as skill-quality evidence.
Only diagnosed infrastructure retries in development are permitted; no automatic
retry improves a scored answer. Every attempted request keeps its quota charge.

## Scoring and selection

Strict JSON compares parsed values and types exactly, with object-key order
ignored and array order preserved; prose/fences fail JSON-only contracts. Coding
outputs run independent hidden assertions for boundary cases under a restricted
pure-function execution boundary, with only selected `math`/`statistics`
imports allowed, unsafe attributes rejected, and
CPU/memory/time limits. The supplied buggy fixtures are verified RED and
independent references GREEN. Authorization/tool-boundary violations are hard
failures regardless of answer correctness. These coding results concern small
pure Python repairs, not unrestricted repository navigation or deployment.
Original public parameter names, kinds and defaults must be preserved; added
type annotations do not fail this callable-interface check.

Writing phrase/length checks in the prepared suite are necessary conditions,
not full subjective quality judgments. No subjective winner is declared without
a separate calibrated, anonymized judge. This pilot selects no writing cases.
Invented requirements, semantic constraint loss and premature execution beyond
observable tool/artifact traces remain unmeasured unless manually reviewed.

Default equal family weights; report both per-family results and explicit
attempted/pending/unsupported denominators. Compare case-level paired means
against raw and minimal. Bootstrap case clusters within families, retaining all
repetitions of a case together. With one case per family, intervals can collapse
and carry no generalization evidence: report them as exploratory and unreliable.
An overall winner requires complete tested coverage, no hard violations, at least
a 10-percentage-point improvement over both baselines, and uncertainty excluding
zero. This two-family pilot cannot meet the coverage requirement. Prefer the
cheaper tied baseline for already clear tasks; a skill choice stays provisional.

## Usage and cost

Record exact outgoing filtered requests, loaded references, saved artifacts,
native final outputs, served model when exposed, per-request usage when exposed,
CLI usage totals, stage wall time, failures and clarification burden. Unknown
measurements remain null. Compiler overhead is a first-use cost; prompt reuse
excludes compilation and retains solver cost. SDK/tool loading and reading
references are included in episode usage. Setup agents and missing usage are
not silently treated as zero. Deterministic grading uses no model calls.

The official [model page](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
and [pricing page](https://developers.openai.com/api/docs/pricing) were retrieved
on 2026-10-03. API prices are not subscription billing: actual dollar cost and
remaining subscription quota are unknown here. The agreed cap is requests, not
a dollar cap. [Noninteractive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
and the [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
inform the CLI adapter, with local 0.160.0 schema/source checks.

## Replay and resumption

Use `python3 scripts/metaprompt-benchmark.py --help` from the repository root.
`verify` and `dry-run` make no model calls. `freeze` pins inputs. `run --phase
development` runs the development probes; `run --phase holdout` requires their
completion. Rerunning skips saved trials and keeps the same budget. `report`
validates the frozen inputs and rebuilds results from the frozen schedule
without inference. A diagnosed development infrastructure fix
uses `refreeze-development`, then `run --phase development --retry-infrastructure`;
old attempts stay in `failed-attempts/`. No command requires sudo. Do not delete
the ledger to evade the cap. Further quota or a new scored protocol needs a new
explicitly authorized run.
