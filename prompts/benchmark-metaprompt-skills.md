Build and run a reproducible benchmark in `/home/example/linux-config` to determine which prompt-authoring skill I should use for my actual work. Start with `docs/metaprompt-skills.md`. Its maintenance comparison and small prompt-output trial do not establish downstream task quality. Produce an evidence-based recommendation scoped to the tested tasks and runtime.

Read the applicable repository instructions, skill sources, provenance, and existing evaluation helpers. Capture Git status and preserve unrelated changes. Maintain an ExecPlan for the benchmark. Test candidates in isolated scratch directories without changing installed skills or defaults or creating Git worktrees.

Compare these variants:

- The installed `$metaprompt`: local adapter over Majkey25 prompt-engineering.
- The preserved `$metaprompt-alxve`.
- talki-io prompt-optimizer.
- getsentry prompt-optimizer.
- GitHub awesome-copilot prompt-optimizer.
- The original task prompt, unchanged, with no optimizer.
- A minimal task-contract baseline, written before results are seen.

Use the revisions linked in the guide as the initial comparison set. Verify actual sources, licenses, local modifications, and content hashes; pin everything. Distinguish the local Majkey adapter from its upstream package. Do not silently substitute newer revisions or count a renamed copy as another independent candidate. If useful and affordable, compare unmodified Majkey upstream as a separately labeled adapter ablation.

First establish the target runtime and execution budget from available context. Record exact compiler and downstream model IDs, settings, tools, and limits; use the same compiler runtime across skills and the same downstream runtime across outputs. If the target or spending limit remains unknown, ask for those missing choices while preparing the suite. Estimate total calls and cost before paid runs and enforce the agreed cap. Use current official documentation for runtime capabilities and pricing; mark unavailable usage measurements unknown.

Freeze the protocol before scored runs:

1. Define two tracks: a shared prompt-improvement comparison on supported tasks, and workflow coverage for creation, sharpening, reusable templates, and coding-agent prompts. Inspect each skill's supported scope. Report unsupported features separately from failures and publish comparison denominators. A narrow skill must not win the overall recommendation merely because difficult categories were excluded.
2. Create separate development and held-out sets, with a practical starting target of 8 development and 24 new held-out cases. Cover coding/debugging with executable fixtures, factual research with fixed source packets, summarization, structured extraction, constrained writing, and reusable templates tested on unseen inputs. Include missing facts, inaccessible files, conflicting evidence, authorization boundaries, and stopping conditions. Use the guide's four existing examples only as development regressions. Label synthetic cases; do not imply they came from my real usage. Reduce scale only for an explicit budget constraint and label the result a pilot.
3. Write task-specific acceptance checks, expected answers or rubrics, category weights, retry rules, a practical improvement threshold, and the selection rule before seeing scores. Default to equal task-family weights unless my workload supports another mix. Keep answer keys and hidden tests out of compiler and solver context. Never tune on the holdout set; revised candidates require a fresh holdout.

Measure actual downstream outcomes through two stages:

- Compile or optimize each task under the candidate's complete pinned instructions and relevant references. Preserve native interaction contracts, using a fixed scripted reply policy where needed. Log clarification turns, loaded references, saved artifacts, premature execution, invented requirements, lost constraints, and unusable outputs. Any extraction adapter must be disclosed; it must not secretly improve the prompt or erase a workflow failure.
- Execute the resulting prompt against the task fixture in a fresh downstream session. That session receives the appropriate task inputs and tools but no optimizer instructions, competing outputs, or answer key. Reset mutable fixtures between runs. Run both baselines against identical fixtures. Count compilation failures in end-to-end results rather than dropping them.

Start with a development pilot to validate the harness, then run at least three fresh end-to-end repetitions per held-out case and eligible variant within budget. Randomize execution order and isolate cases from shared conversation history. Hold runtime settings, context access, retry allowances, and timeouts constant. Any native workflow with additional optimization calls must have its budget and overhead reported separately. Keep infrastructure failures visible and distinct from task failures; never cherry-pick successful retries.

Make downstream task success the primary metric. Prefer executable tests, schema checks, exact expected facts, and source-supported claims. For subjective criteria, use a frozen rubric with anonymized outputs and randomized presentation order; record the independent judge, calibration examples, and limitations. Do not use a skill's self-rating or prompt attractiveness as evidence. Report constraint and authorization violations as hard failures that brevity or cost cannot offset.

Report per-case results, per-category success, supported coverage, failure counts, clarification burden, and end-to-end tokens, latency, and cost, including skill loading, optimization, and grading overhead. Distinguish first-use cost from prompt reuse. Compare paired case-level outcomes with uncertainty intervals that account for repeated runs of the same task; repetitions are not independent tasks. Treat rankings across many candidates as exploratory unless the design supports stronger inference. Report ties or insufficient evidence when appropriate.

Deliver a runnable, resumable harness with dry-run support, meaningful tests for scoring and failure accounting, pinned manifests, fixtures, sanitized raw prompts and outputs, and machine-readable results. Keep benchmark artifacts durable and exclude secrets and machine-local caches. Include exact replay commands through a reusable script.

Write `docs/metaprompt-benchmark.md` with the executed protocol, results table, representative failures, uncertainty, costs, and artifact links. Update `docs/metaprompt-skills.md` to distinguish earlier selection evidence from the new results; update smoke tests and README where the new commands require it. State what ran, what was only prepared, and all blockers.

Finish with the best default for the tested workload, any task-specific alternatives, and whether a skill improves enough over the raw/minimal baselines to justify its overhead. If there is no clear winner, give a provisional choice and the smallest additional experiment that could resolve it. Do not claim universal superiority or switch my installed default automatically.
