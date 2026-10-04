# Group A native metaprompt source audit

Researched on 2026-10-03 using authenticated official GitHub API reads via
`gh api`. No model trials, installs, local skill changes, commits or worktrees.
The 90-day window starts July 5; 180 days starts April 6. Exact recorded stars
are repository popularity only, not evidence of skill quality. All repositories
are nonarchived and retain an actual MIT license notice.

| Native candidate | Repository stars | Latest substantive change | 90 / 180 changes | Distinct contributing identities in 180 days | Result |
| --- | ---: | --- | ---: | ---: | --- |
| wshobson prompt-engineering-patterns | 40,179 | 2026-08-15 | 1 / 2 | 2 | Eligible; complete 11-file package snapshotted |
| alireza senior-prompt-engineer | 27,472 | 2026-06-11 | 0 / 1 | 1 | Eligible; complete 8-file package snapshotted; scoped helper needed |
| alireza prompt-engineer-toolkit | 27,472 | 2026-06-11 | 0 / 1 | 1 | Excluded: current marketing specialization lacks coding-agent authoring support |
| developer-kit prompt-engineering | 353 | 2026-03-16 | 0 / 0 | 0 | Excluded: fewer than 1,000 stars and no qualifying change in 180 days |

`group-a.json` contains full immutable revisions, paths, license source,
per-file SHA-256, independent Git blob IDs, counted/excluded commits, evidence
URLs, workflow scope, runtime needs and contributor caveats. Excluded packages
were inspected in scratch but were not vendored as benchmark candidates.

## Maintenance evidence

Wshobson's [August 15 fix](https://github.com/wshobson/agents/commit/56a28c6e4d575f1813f777ddfeb956e069aac07a)
adds an early stop to the native optimizer when deterministic variants do not
improve the current prompt. It prevents repeated evaluation of identical
variants and is a real executable helper behavior change within the skill
package, rather than unrelated repository activity. Contributor: `rahul188`.
The [June 3 update](https://github.com/wshobson/agents/commit/3ce0342afde674b3a492bdc9271621e953322c11)
expands native trigger semantics to templates, debugging, structured prompting
and few-shot requests; contributor `yanghaod2278827`. This metadata change is
counted because it changes the native skill's applicability, not formatting.
The original October 2025 addition is excluded. April/July model-name-only
example replacements and May's extraction of existing entrypoint material into
`references/details.md` are conservatively excluded from substantive counts.
The latest substantive change is to the optional optimizer helper, not a claim
that August changed every authoring pattern.

Alireza's [June 11 senior rewrite](https://github.com/alirezarezvani/claude-skills/commit/5acece10acd47513bbc7b0c91fe88f54df138adc)
changes the native runtime to baseline/eval-first iteration and no-regression
gates, removes hardcoded model/pricing assumptions, and changes both optimizer
and agent-config helper behavior. It is plainly post-introduction substantive
maintenance. May's directory relocation is excluded; the old
`engineering-team/senior-prompt-engineer` path was also queried, confirming
October 2025 introduction and no additional post-April substantive change.
The June commit author resolves to the linked GitHub account `claude`. The
count of one is a recorded contributor identity, not proof of human ownership
or one active human maintainer.

The [June 11 toolkit overhaul](https://github.com/alirezarezvani/claude-skills/commit/aecfb8e0bb71dbf1413082f86b33a5c4c9b8f416)
is counted as real maintenance: it replaces generic templates with marketing
assets and supplies marketing-specific eval/governance rules. However, the
current native entrypoint and references specialize in marketing; the old
software-code-review template was removed. Its current "survey coding"
reference means classification of survey text, not authoring a coding agent.
This exclusion follows actual scope, not missing output ceremony or a narrow
interpretation of a broad prompt-authoring skill. Previous marketing-skill
path history was also queried; March introduction/updates precede the window,
and May's move does not count twice.

Developer-kit's [March 16 change](https://github.com/giuseppe-trisciuoglio/developer-kit/commit/68f3ca57c4f3cad12b713a79f9facab8ffdd8a99)
adds routing/overview and constraints, including a warning about exposing
hidden reasoning. Its prior real refactoring/testing changes also predate
April 6. These were inspected, but neither changes the current star/recency
exclusion. Merge commits and markdown-only fixes are not duplicate maintenance.

## Native capability and output

**Wshobson** supports new prompt drafting, refinement, variable templates and
coding prompts through its general native pattern workflow, code-assistant
system prompt, debugging CoT template and code-review role. It has no mandatory
final artifact/fence/section wrapper. The complete package includes six
references, two assets, one optimizer helper, native entrypoint and root MIT
license. Its [immutable native package](https://github.com/wshobson/agents/tree/156b7a5e7a8b93642628a339ee4039c925b34c7f/plugins/llm-application-dev/skills/prompt-engineering-patterns)
is retained without local adapters.

**Senior** supports all four workflows through generic meta-prompt creation,
existing-prompt optimization, templated pattern construction and agent/tool
prompt design. This is a broad native engineering authoring/evaluation skill;
there is no separate coding-authoring invocation or required presentation
wrapper. Examples and references supply the capability rather than forcing
all requests through a rigid compiler protocol. The [immutable package](https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/engineering-team/skills/senior-prompt-engineer)
contains entrypoint, three references, three stdlib scripts and MIT license.

Extraction must be declared mechanically before trials: an explicitly named
final prompt artifact, one unambiguous final prompt fence, or explicitly titled
Final/Optimized/Revised Prompt section. Never add a skill-specific rewrite stage
or select the best artifact using downstream scores. For senior, `baseline.json`,
`revised.json` and `eval_results.json` are evaluation artifacts, not prompts;
`current_prompt.txt` is the starting draft, and `revised.txt` is its example
final revised prompt. Create/template output filenames are not fixed natively.
Multiple candidate prompts require an explicit final identification.

## Senior required helper and bounded runtime

Native existing-prompt optimization requires baseline analysis and revision
comparison. Exact commands from the pinned source:

```bash
python3 scripts/prompt_optimizer.py current_prompt.txt --analyze --json --output baseline.json
python3 scripts/prompt_optimizer.py revised.txt --analyze --compare baseline.json
python3 scripts/prompt_optimizer.py revised.txt --analyze --json --output revised.json
```

The first Operating Rule also permits `--analyze --output baseline.json`.
The output JSON includes `token_count`, `clarity_score`, `structure_score`,
`issues`, `suggestions`, section/example information and optional estimated
cost. No price argument means `estimated_cost: null`. The structural gate is
revision clarity at least baseline and token estimate at most 1.10 times
baseline. A task-level no-regression eval remains separately required; static
metrics do not prove actual model performance.

The complete helper source uses stdlib argparse, json, re, sys, pathlib, typing
and dataclasses. It has no network, subprocess, dynamic execution, environment
or credential reads. It reads only the prompt and optional baseline paths,
and writes the explicitly supplied output path. Native `Path.write_text`
overwrites existing outputs and paths are unconstrained in the raw CLI.
A fixed `run_skill_check` action is feasible without model API keys: bind to
this exact pinned script/digest, expose only analyze plus optional compare,
validate every input path beneath scratch, and restrict output to declared
helper-owned artifacts with controlled collision handling. No arbitrary command,
shell expression, arbitrary Python, pricing fetch or API client is needed.
The structural comparison gate can be a fixed local check, not model-written
shell. The other two supplied scripts apply only to RAG/agent-config tasks,
and are not required for generic drafting/refinement.

Scratch-only executable verification: baseline analyze/save returned exit 0;
revision compare returned exit 0 and the expected comparison output. Its
baseline JSON parsed with all documented fields and null cost. This helper
check used no model/API inference. The entrypoint also demands 10–20 public
eval cases before optimization; the harness must supply or let the compiler
prepare public cases and preserve any unexecuted eval limitation. Never expose
hidden benchmark expected outputs to satisfy this native precondition.

## Optional tooling and limits

Wshobson does not require its helper for prompt authoring. That helper imports
numpy; its default `main()` uses a mock sentiment client and writes
`optimization_results.json`. An injected real client would make model calls.
Running the demo does not establish prompt quality on a real model. SDK,
embedding, vector-store and external-provider examples are optional integration
patterns; the native textual authoring workflow needs no paid API credentials.
Do not silently run provider examples or a real injected client outside the
benchmark request ledger. Several reference examples retain older API shapes
and strong reasoning/style assumptions; popularity does not validate them.

The excluded toolkit tester can run static checks, but `--runner-cmd` invokes
an arbitrary subprocess. Its versioner writes local history. Do not broaden
shell privileges to accommodate it. Developer-kit examples describe measurement
utilities and provider integrations, but no such execution changes its hard
eligibility failures.

All 19 vendored eligible files were byte-verified against immutable GitHub Git
blob objects and then SHA-256 verified against the research inventory. Actual
MIT notices are retained in full. Neither installed skills nor the historical
`benchmarks/metaprompt/` evidence was changed.
