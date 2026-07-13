# AI Workflow Optimization

This document holds the measurement baseline, policy decisions, and historical
provenance moved out of always-loaded instructions. The implementation plan is
[`plans/ai-workflow-optimization.md`](../plans/ai-workflow-optimization.md).

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
