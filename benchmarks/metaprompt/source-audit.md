# Candidate source and scope audit

Audited 2026-10-03. `sources.json` pins five candidate packages, their full
file inventories, SHA-256 digests, licenses, supported suite workflows, and
interaction caveats. No model trials were run during source preparation.

## Candidate identity and provenance

| ID | Actual benchmark candidate | Pin | Files | License |
| --- | --- | --- | ---: | --- |
| metaprompt | Installed local Majkey prompt-authoring adapter, including installed extra references | `5c00259223196bd779c97d3234ef34a9a7119634` imported upstream | 50 | MIT |
| metaprompt-alxve | Installed repo-native legacy adapter; not raw upstream compiler | `4c30dda5754fe48ce3399c2379a7a370b652b155` conceptual source | 8 | MIT |
| talki | [Unmodified upstream package](https://github.com/talki-io/prompt-optimizer/tree/e5f5efe5925ce47073f143001d0a8e9de23b392a) | `e5f5efe5925ce47073f143001d0a8e9de23b392a` | 3 | MIT |
| sentry | [Unmodified upstream skill package](https://github.com/getsentry/skills/tree/c190d369bcbaa6cfdd95e9edfdba040506b4db76/skills/prompt-optimizer) plus root license | `c190d369bcbaa6cfdd95e9edfdba040506b4db76` | 8 | Apache-2.0 |
| github | [Unmodified upstream skill package](https://github.com/github/awesome-copilot/tree/b010c5ebfacdd78a45702481b77ec55ba033e373/skills/prompt-optimizer) plus root license | `b010c5ebfacdd78a45702481b77ec55ba033e373` | 2 | MIT |

Majkey's [pinned upstream package](https://github.com/Majkey25/prompt-engineering-skill/tree/5c00259223196bd779c97d3234ef34a9a7119634/prompt-engineering)
is retained inside the local candidate: original `SKILL.md` is `UPSTREAM.md`,
original UI metadata is `UPSTREAM.openai.yaml`, and 34 references, three helper
scripts, asset, and repository license are unchanged. All 41 imported files
were independently downloaded at the pin and matched their manifest SHA-256
and local snapshot bytes. Local entrypoint, metadata, provenance, and update
helper are separately identifiable and are not claimed as upstream originals.

The legacy conceptual source repository remote is
[Alxve99/metaprompt](https://github.com/Alxve99/metaprompt/tree/4c30dda5754fe48ce3399c2379a7a370b652b155).
The local adapter preserves its own compact entrypoint, output/save contract,
fresh standalone `go`, compilation references, and selective loading.
Its retained MIT license matches `git show` at that upstream commit exactly.
Its current local bytes are pinned by the complete SHA-256 inventory, not by
pretending the conceptual upstream revision identifies the local adapter.

Talki, Sentry, and GitHub downloads were independently verified against GitHub
Git-tree blob SHA-1 object IDs at their pinned commits; all 13 files matched.
Full actual license notices are retained, rather than inferred from repository
metadata. Source packages contain no caches. Snapshots should be treated as
immutable after trials begin; a later change requires a new provenance record.

## Installed comparison

Before preparation, the tracked current maintained adapter had 46 files while
the installed `~/.agents/skills/metaprompt` package had 50. Every shared file
matched exactly. Four extra installed legacy files were present:

- `references/compilation-rules.md`
- `references/examples.md`
- `references/execution-routing.md`
- `references/model-profiles.md`

The benchmark candidate includes all four extras because it tests the installed
skill. They are labeled local additions in `sources.json`; none belongs to the
41-file Majkey upstream import inventory. The maintained entrypoint does not
reference them, but their presence is a possible context contamination risk.
This preparation did not remove or modify installed files. Installed
`metaprompt-alxve` and its tracked current package matched exactly (8 files).

## Native scope

| Candidate | Sharpen existing | Create new | Reusable template | Create coding-agent prompt |
| --- | --- | --- | --- | --- |
| metaprompt | Supported | Supported | Supported | Supported |
| metaprompt-alxve | Supported, but compiles a rewrite instruction | Supported | Supported | Supported |
| talki | Supported | Explicitly excluded | Creation excluded; existing template editing supported | Creation excluded; existing coding-prompt editing supported |
| sentry | Supported | Supported | Supported | Supported |
| github | Supported | Supported | Explicitly excluded: no placeholders | Supported in chat format |

Unsupported workflow cases should be recorded as not applicable, not forced
through a synthetic draft to manufacture comparability. The `template` suite
workflow means template creation, not editing a pre-existing template. The
`coding` workflow means authoring a coding-agent prompt, not optimizing source
code. Capability classification comes from the pinned runtime instructions
and Sentry specification, not from inferred repository popularity.

## Compilation and extraction caveats

- **metaprompt:** local rules disable upstream silent autoprompt execution;
  generated prompts must be saved and shown in a prompt fence. Load
  `UPSTREAM.md` and only task-relevant references, rather than flattening the
  entire package into the model context. It has no legacy `go` gate.
- **metaprompt-alxve:** strict fresh standalone `go` is native behavior.
  Standard sharpening returns a prompt that asks another model to rewrite the
  supplied draft. Extraction must preserve this additional stage and not
  quietly execute it to make its result resemble a direct rewrite.
- **talki:** an optimize request normally returns only optimized prompt text.
  Direct explicit invocation enters Apply Mode, first displaying the full
  prompt and then adopting it as operating instructions. A benchmark that
  suppresses task execution must label this interaction adaptation. Preserve
  commands, paths, examples, schemas, and constraint strength verbatim.
- **sentry:** native return is an eight-section package. Extract the
  `Optimized Prompt` component and retain the surrounding eval/adapter package
  separately. Native baseline/candidate/holdout loops may require additional
  calls. A bounded single compilation cannot be called a completed native
  optimization loop or executed holdout evaluation.
- **github:** output is exactly one fenced chat prompt. It prohibits template
  placeholders and translates API-only mechanics into chat instructions.
  Missing required content is obtained by a downstream question or follow-up
  turn. Its mandatory reasoning closing line is candidate behavior, not a
  harness instruction.

No upstream-only Majkey ablation or raw Alxve comparison was added to the paid
suite. The parent benchmark owns raw/minimal baselines, budgets, trial runtime,
and the final scoring/extraction procedure.
