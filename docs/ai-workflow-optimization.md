# AI Workflow Optimization

This document holds the measurement baseline, policy decisions, and historical
provenance moved out of always-loaded instructions. The implementation plan is
[`plans/ai-workflow-optimization.md`](../plans/ai-workflow-optimization.md).

## Skills-efficiency measurement (2026-10-22)

The [current trim plan](../plans/skills-efficiency.md) and
[pass log](../benchmarks/trim/PROGRESS.md) track a new optimization series.
Its immutable baseline records 353 lines / 22,750 bytes for canonical AGENTS,
59 canonical skills, 37,619 recurring bytes and 403,458 on-demand body bytes.
The cull, complementary intake and mandatory admission passes are committed as
`bc0360c9`, `60c6e70f` and `6e9934c7`; the current
[comparison](../benchmarks/trim/COMPARISON.md) reproduces actual Git blobs.
The CASD pass moves conditional procedures verbatim and preserves every original
block. Canonical AGENTS:23,147B/357lines before, 8,982B/145lines
after. Static recurring context falls30,292→16,127B. Actual task context
depends on triggered reference loads; the moved text is retained, not deleted.

| Original section/procedure | Mandatory home |
| --- | --- |
| Start-of-turn checkpoint and Live Codex Task Titles | [Task titles](../dot_codex/references/task-titles.md) |
| System Design Routing | [System design](../dot_codex/references/system-design.md) |
| CLI decoration/progress and fish paste/copy procedure | [CLI and shell](../dot_codex/references/cli-and-shell.md) |
| Failure lookup, learning and immediate postmortem procedure | [Postmortems](../dot_codex/references/postmortems.md) |
| Conditional Session Memory | [Session memory](../dot_codex/references/session-memory.md) |
| README/manual checks, overview and configuration refresh | [Documentation/config](../dot_codex/references/documentation-and-config.md) |
| Commit workflow, delivery cadence and Handoff Format | [Delivery](../dot_codex/references/delivery.md) |
| Authority, safety, scope, planning, defining tests, feedback and verification | [Standing core](../dot_codex/AGENTS.md) |

The [block preservation map](../benchmarks/trim/casd-map.json) identifies all91
original blocks by source line, section, hash and retained home. Trigger routers
are mandatory. Screened native-session evidence found no frequent uncovered
complaint; safety plus observed copy/paste and completion controls remain.
Active user/developer instructions still govern. No model/effort or live config
was changed; no push, refresh-config or chezmoi apply is authorized.

## Completed trim series

Twelve pass commits end at79d1a8cb. Original37,619→14,399standing bytes
(9,404.75→3,599.75estimated tokens,−61.72%); descriptions13,462→4,727B,
SKILLbodies403,458→179,490B,59→27canonical skills under approved cull/intake.
The [final comparison](../benchmarks/trim/COMPARISON.md) uses exact committed
blobs; [saturation review](../benchmarks/trim/saturation.md) records rejected
candidates, protected sources and earlier-audit dispositions. Triggered references
remain extra; live config/runtime savings are unverified.239selectedtests/
391subtests pass; inherited collection/fixture/audit debt is disclosed in PROGRESS.
Model/effort and Claude permissions remain unchanged; no push/apply occurred.

## Audited Baseline

Captured on 2026-07-13 before Task 1 edits:

- Branch: `feat/ai-workflow-optimization`
- Working tree:
  - `M dot_codex/config.toml` (protected; never modify or stage)
  - `?? dot_agents/skills/metaprompt/` (approved protected baseline)
  - `?? plans/ai-workflow-optimization.md`
  - `?? prompts/integrate-system-prompts-leaks.md`
- Source archive revision:
  `5c86715f453f0eca188451a48bf5b165831d8b29`
- Protected metaprompt `SKILL.md` SHA-256:
  `8e5f9534182212e77a4607c74afd22aab4ceb05a4a740a02ce0c91f5ea86b94a`

Instruction sizes before the rewrite:

| File | Bytes |
| --- | ---: |
| `AGENTS.md` | 13,791 |
| `dot_codex/AGENTS.md` | 21,014 |
| Combined active instructions | 34,805 |

The root and canonical documents shared 12 duplicated top-level blocks:
Required Reading and Precedence, Prime Directive, Workflow Orchestration, Task
Management, Problem-Solving Approach, Workflow Principles, Code Principles, PR
Checklist, What Done Looks Like, Communication Standards, Failure Modes, and
Local Override Mechanism.

## Task 1 Decisions

- `dot_codex/AGENTS.md` is the only active instruction body.
  `AGENTS.md`, `AGENTS.repo.md`, and `AGENTS-BASE.md` are compact routing
  or compatibility layers.
- `.agent/PLANS.md` defines the executable ExecPlan contract. Plans remain
  under `plans/` and their progress, evidence, and review notes land in the
  same commits as related work.
- Universal invariants stay always loaded. Conditional detail belongs in
  repo-tracked skills or one-level references.
- Git worktrees are opt-in. When explicitly requested, they live under the
  repository's `.worktrees/` directory.
- Single-commit workflows push after verification. Multi-commit workflows push
  once after the entire verified series. An explicit user request can override
  the cadence.
- Durable cross-task user preferences go to the canonical append-only
  `feedback.log`; repo-specific engineering lessons go to
  `tasks/lessons.md`. Do not duplicate one correction in both places.
- `refresh-config` retains its established live-Codex-config snapshot,
  chezmoi apply, shortcut regeneration, and fish reload behavior.

## TDD Evidence

RED:

- Command: `python3 tests/test_ai_workflow_contract.py`
- Exit: `1`
- Observed: `FFFFF`; five expected failures covered the missing plan
  contract, missing provenance document, duplicate active instruction blocks,
  missing canonical boundaries, and conflicting push policy.

GREEN evidence is recorded here after the policy and documentation changes pass
the same focused command.

GREEN:

- Command: `python3 tests/test_ai_workflow_contract.py`
- Exit: `0`
- Observed: six tests ran and returned `OK`.

Acceptance-review RED:

- Command: `python3 tests/test_ai_workflow_contract.py`
- Exit: `1`
- Observed: two focused failures exposed stale `commit-dirty` and
  `commit-session` metadata plus the duplicated delivery preference in
  `tasks/lessons.md`; the metadata and one-store boundary are now covered by
  the contract.

Independent-review RED:

- Command: `python3 tests/test_ai_workflow_contract.py`
- Exit: `1`
- Observed: eleven tests ran with five expected failures for the active-plan
  evidence shape, system-design routing, lazy README invariants, smoke wording
  and coverage, and byte labels.

Final GREEN:

- Command: `python3 tests/test_ai_workflow_contract.py`
- Exit: `0`
- Observed: all eleven tests ran and returned `OK`.

Post-change active instruction sizes:

| File | Bytes |
| --- | ---: |
| `AGENTS.md` | 690 |
| `dot_codex/AGENTS.md` | 9,127 |
| Combined active instructions | 9,817 |

The active pair fell by 24,988 bytes, or 71.8%, from the 34,805-byte
baseline. The protected metaprompt hash remained unchanged.

## AI Workflow Doctor

Task 2 adds `scripts/executable_ai-workflow-doctor` and the matching
`ai-workflow-doctor` skill. The standard-library CLI reports exact UTF-8 bytes,
Unicode characters, a labeled `ceil(characters/4)` token estimate, SHA-256
digests, skill-catalog alignment, normalized instruction duplication, bounded
local-reference health, plan-contract presence, cross-root duplicate skill
slugs, and source-provenance errors. Repeated section headings with different
bodies are only semantic-review candidates: the tool never guesses a winner or
changes policy.

The versioned JSON report is deterministic and omits timestamps, absolute repo
paths, mtimes, and Git state. `--snapshot` captures that report; `--compare`
reports metric deltas plus stable added, resolved, and unchanged finding keys.
They can run together: the comparison is printed while the new snapshot stays
a reusable base report without an embedded comparison. Schema-v1 snapshots are
validated through the nested active totals and finding keys before comparison.
Normal audits exit `0` even when they report findings, while `--check` exits `1`
for objective errors and leaves semantic warnings non-blocking. Usage, schema,
decoding, and I/O failures exit `2`. The default report is repository-local and
deterministic. Opt-in `--verify-sources` resolves declared local Git archives,
commits, primary paths, and supporting paths; an unavailable archive is a
non-blocking warning while a reachable mismatch is an error. Remote sources
remain structurally validated without network access. Relative local archive
paths resolve from the audited repository root, independent of caller CWD.

TDD and repository evidence:

- The initial twelve-test contract first produced eleven expected failures
  because the executable and executable bit did not exist.
- Independent review added regressions for CommonMark fences, malformed nested
  snapshots, combined compare plus snapshot output, actionable text details,
  cwd-independent installed invocation, explicit local source resolution with
  portable missing-archive behavior, and cross-root duplicate skills. The
  captured review RED run exposed five expected gaps; after the fixes, all
  covered behavior passed. A final specialist RED then caught caller-CWD
  dependence for relative archives and false errors for balanced-parenthesis or
  angle-bracket CommonMark destinations. After those fixes, all seventeen tests
  passed without a traceback. The official skill validator returned
  `Skill is valid!`.
- The first live audit found two broken cross-skill links and two uncatalogued
  skills. The link targets now point to the existing `frontend-design`
  references, and `brand-system-designer`, `metaprompt`, and the doctor are in
  the catalog.
- At the Task 2 checkpoint, the repo passed `--check` with zero errors, zero
  warnings, 9,817 active-instruction bytes, and 45 actual / 45 catalogued
  skills.
- `/tmp/ai-workflow-baseline.json` is the Task 2 comparison baseline. An
  immediate comparison reported zero active-total deltas and no finding-key
  changes.
- A context-free forward run reproduced the same status and metrics, did not
  auto-resolve anything, and selected the explicit baseline compare command
  without adding evidence-free claims.

The adaptation is clean-room and pinned in
`dot_agents/skills/ai-workflow-doctor/SOURCE.md` to source revision
`5c86715f453f0eca188451a48bf5b165831d8b29` and
`Anthropic/Claude Code/bundled-skills/doctor/SKILL.md`.

## Metaprompt Progressive Disclosure

The existing metaprompt already compiled a context-free research prompt that
required current official sources, narrowed follow-up queries, prior-evidence
reuse, parallel independent checks, and a saturation stop condition. That
compile-time contract made a second archive-shaped research policy redundant,
so no `research-routing.md` or archive provenance file was added. Separately,
the post-refactor standalone `go` forward scenario executed the compiled prompt
and produced an official-source comparison.

Instead, Task 3 moved detailed compilation, execution-routing, and example
rules into three conditional one-hop references. The entrypoint retains the
activation contract, Trivial path, four-stage compile/gate flow, exact output
shape, standalone-run boundary, logistics riders, first-match route order,
portability, and user-language behavior.

| Metaprompt surface | Before | After | Change |
| --- | ---: | ---: | ---: |
| Always-loaded `SKILL.md` bytes | 21,213 | 2,855 | -86.5% |
| Always-loaded `SKILL.md` words | 3,442 | 404 | -88.3% |
| Complete skill Markdown bytes | 21,213 | 15,312 | -27.8% |

The seven-test extraction contract first failed on the 3,442-word entrypoint
and missing references/metadata, then passed after extraction. The official
skill validator also passed. Forward scenarios cover a lightweight Trivial
prompt, a current-source comparison whose revision contains `run` but must
re-gate, a standalone `go`, and a read-only multi-hypothesis CI audit.

### 2026-07-14 Curated Integration Follow-Up

The current skill is a curated synthesis of `metaprompt-alxve` v2.0.1 at
revision `4c30dda5754fe48ce3399c2379a7a370b652b155`, documented in
`dot_agents/skills/metaprompt/SOURCE.md` with its MIT notice. It selectively
adds reusable templates, example harvesting, target-system complements,
untrusted-input boundaries, long-context ordering, precedent slots, agent
permissions and budgets, media guidance, and conservatively dosed completion
checks. It does not import the upstream fast lane, overlay, PowerShell tooling,
branding, author-specific leak denylist, or unverifiable model claims.

The entrypoint remains under 500 words and progressively discloses one-hop
references. A fresh standalone `go` is still mandatory for every execution and
every high-stakes pass, including an original compile-and-run request. Reusable
prompts expose canonical `{{variable}}` slots, and judge/rewrite/re-check work
emits three separately runnable, separately gated prompt blocks.

The dated model-profile reference permits only direct official URLs, explicit
heuristics, or `unknown`, with an expiry rule that prevents stale guidance from
silently becoming fact. This follow-up records current behavior without
rewriting the historical measurements above. The integration deliberately does
not refresh tracked configuration or apply the package to the live skill; that
installation remains a later explicit user action.

## Compact Context Handoffs

`context-handoff` creates a maximum 600-word continuation artifact rather than
copying a transcript. It maps numbered done criteria to evidence, distinguishes
verified `None` from unchecked `Unknown`, groups repeated failures by stable
signature and retry condition, links large artifacts, preserves literal
protected state, and gives every next action an owner, action, expected result,
and stop condition.

The official initializer created the skill scaffold. Its six-test contract
first failed only because the skill files were absent, then passed with a
390-word `SKILL.md`; the official validator and workflow doctor also passed.
The clean-room adaptation is pinned in
`dot_agents/skills/context-handoff/SOURCE.md` to the recorded archive revision,
with the continuation prompt as the primary source and compact/rewind material
listed as supporting sources.

## Adoption Decisions

| Candidate pattern | Decision | Local result |
| --- | --- | --- |
| One canonical instruction body with small routing shims | Adapt | Active instruction context fell 71.8% while preserving repo boundaries. |
| Deterministic workflow health check | Adopt | Standard-library doctor with versioned JSON, stable snapshots, drift checks, and human-only semantic review. |
| Evidence-linked compact continuation | Adopt | `context-handoff` adds bounded, retry-safe, acceptance-mapped handoffs. |
| Progressive disclosure for a large skill | Adapt | Metaprompt's always-loaded bytes fell 86.5%; detailed rules remain conditional. |
| Additional metaprompt research-routing policy | Already covered | Baseline compilation required narrowed queries, evidence reuse, parallel checks, official citations, and a saturation stop; a separate post-refactor `go` run executed that research. |
| Separate runtime-verification skill | Already covered | Existing rules already reject test-only completion, require the real entrypoint, rendered/install evidence, and invalid-input coverage, and consider an adjacent probe when relevant. |
| Vendor prompt bodies, hidden policy, tool schemas, personalities, or binary-extracted skills | Reject | They are brittle, non-portable, unsafe to copy, and unnecessary for the local workflow outcomes. |

Skills continue to install from this repo to `~/.agents/skills/` for Codex.
Claude Code's documented personal-skill layout is
`~/.claude/skills/<name>/SKILL.md`, with supporting files beside the entrypoint,
and its documentation supports skill-directory symlinks. The post-apply
generator now links each whole `~/.agents/skills/<name>` directory into that
layout, removes only its matching managed legacy `<name>.md` link, and refuses
to overwrite a real destination directory. This preserves metaprompt's
conditional references without creating a second source of truth. See the
[official Claude Code skills documentation](https://code.claude.com/docs/en/skills).

The final schema-v1 snapshot at `/tmp/ai-workflow-final.json` passes with zero
errors, one warning, 46 actual / 46 catalogued skills, and 9,817
active-instruction bytes. All active-total deltas from the Task 2 baseline are
zero. Reviewer-added detection contributes one finding key for the pre-existing
`brand-system-designer` slug in both `.agents/skills/` and
`dot_agents/skills/`. Both tracked copies are retained because repo policy
forbids silently deleting user-owned files; the non-blocking warning keeps the
ownership ambiguity visible until deletion is explicitly authorized. Explicit
source verification resolved the pinned local archive commit and all declared
primary/supporting paths. A targeted chezmoi dry-run renders all three affected
installed skills without writes. The live and protected tracked Codex config
compare byte-for-byte, so `refresh-config` was not used to rewrite the
user-owned diff.

## Instruction Provenance

The previous canonical document merged repo-agnostic guidance from these
sources. Keeping this history here preserves auditability without paying its
context cost in every agent session.

| Source | Source file | Selection |
| --- | --- | --- |
| upwork | `/home/example/coding/upwork/AGENTS.md` | Excluded user-specific workflow preferences. |
| zoo-blog | `/home/example/coding/zoo-blog/AGENTS.md` | Retained the shared baseline. |
| example-user | `/home/example/coding/example-user/AGENTS.md` | Retained the shared baseline. |
| spotify-library-intelligence-dashboard | `/home/example/coding/spotify-library-intelligence-dashboard/AGENTS.md` | Retained the shared baseline. |
| portfolio-site | `/home/example/coding/portfolio-site/AGENTS.md` | Retained the shared baseline. |
| quit-weed | `/home/example/coding/quit-weed/AGENTS-BASE.md` | Included the generic base and omitted its project companion. |
| nomar-stocks | `/home/example/coding/nomar-stocks/AGENTS.md` | Excluded the launch checklist. |
| stb-mkt-all/prod-fix | `/home/example/coding/stb-mkt-all/prod-fix/AGENTS.md` | Kept repo-agnostic sections only. |
| stb-mkt-all/production | `/home/example/coding/stb-mkt-all/production/AGENTS.md` | Kept repo-agnostic sections only. |
| stb-mkt-all/history | `/home/example/coding/stb-mkt-all/history/AGENTS.md` | Kept repo-agnostic sections only. |

The broader optimization work audits
`/home/example/coding/system_prompts_leaks` at the recorded revision. Only
clean-room, principle-level adaptations are allowed: do not copy vendor prompt
bodies, hidden policy, tool schemas, personalities, or binary-extracted skills
verbatim. Material adaptations must keep source provenance near the resulting
skill or in this document.
