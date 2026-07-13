# AI Workflow Optimization Implementation Plan

> **For agentic workers:** Use `superpowers:subagent-driven-development` or
> `superpowers:executing-plans` task by task. Track progress with checkboxes and
> keep this plan in the same commits as the related implementation.

**Goal:** Reduce always-loaded AI instructions and add lazy, evidence-driven
workflow capabilities without weakening correctness or existing Codex and
Claude behavior.

**Architecture:** Keep one compact canonical instruction source, move
conditional procedures into repo-tracked skills, and enforce structural
invariants with a deterministic standard-library doctor. Adapt source ideas
through clean-room paraphrase with provenance rather than copying vendor text.

**Tech Stack:** Markdown agent instructions and skills, Python standard
library, Bash test harnesses, chezmoi installation, Codex and Claude skill
metadata.

## Current Context And Scope

- Work is active on `feat/ai-workflow-optimization` in the shared working
  tree. The approved prompt and this plan predate Task 1 implementation.
- The full plan spans six tasks. Task 1 owns instruction routing, the ExecPlan
  contract, Git delivery policy, matching README/smoke/provenance updates, and
  its focused contract test. Tasks 2 through 6 remain pending.
- The pre-existing `dot_codex/config.toml` diff and untracked
  `dot_agents/skills/metaprompt/` are protected from Task 1 edits and staging.
- Task 1's active Git metadata scope explicitly includes
  `dot_agents/skills/commit-dirty/agents/openai.yaml` and
  `dot_agents/skills/commit-session/agents/openai.yaml`.

## Assumptions

- `dot_codex/AGENTS.md` remains the one canonical instruction body for both
  Codex and the repo's Claude import; root AGENTS files remain routing shims.
- Short universal routing triggers stay canonical, while conditional procedures
  and narrative detail belong in repo-tracked skills or one-level references.
- The newest applicable entry in the canonical append-only feedback log wins
  over conflicting historical preferences.
- Standard-library contract tests and local documentation gates are sufficient
  for Task 1; later tasks own the doctor CLI and whole-branch runtime checks.

## Risks, Edge Cases, And Rollback

- Instruction reduction can silently remove a mandatory invariant. Mitigation:
  compare HEAD intent, test critical boundaries, and keep conditional rules in
  their named lazy reference rather than deleting them.
- `refresh-config` can overwrite the protected Codex config from live state.
  Do not run it during Task 1; Task 6 owns targeted live/tracked comparison.
- Historical feedback may contain obsolete push cadence. Apply the newest entry
  without rewriting append-only history, and keep lessons as a pointer.
- Rollback Task 1 by reverting only its instruction, policy, test, plan, and
  documentation files. Preserve the protected config diff and metaprompt tree.

## Verification Evidence

### Task 1 Contract Test

- Command: `python3 tests/test_ai_workflow_contract.py`
- Expected: All focused contract tests pass and the runner prints `OK`.
- Observed: Eleven focused contract tests passed and the runner printed `OK`.
- Exit status: `0`.

### Instruction Size

- Command: `wc -c AGENTS.md dot_codex/AGENTS.md`
- Expected: Combined active instructions are at most 24,363 bytes, a reduction
  of at least 30% from the 34,805-byte baseline.
- Observed: `AGENTS.md` is 690 bytes and `dot_codex/AGENTS.md` is 9,127
  bytes, for a 9,817-byte combined total.
- Exit status: `0`.

### Protected Metaprompt

- Command: `sha256sum dot_agents/skills/metaprompt/SKILL.md`
- Expected: SHA-256 remains
  `8e5f9534182212e77a4607c74afd22aab4ceb05a4a740a02ce0c91f5ea86b94a`.
- Observed: SHA-256 remained
  `8e5f9534182212e77a4607c74afd22aab4ceb05a4a740a02ce0c91f5ea86b94a`.
- Exit status: `0`.

### README And Diff Gates

- Command: `./scripts/executable_readme-recruiter-sync`
- Expected: Exit 0 with `pass_no_change`.
- Observed: `pass_no_change`.
- Exit status: `0`.
- Command: `git diff --check`
- Expected: Exit 0 with no whitespace errors.
- Observed: No output.
- Exit status: `0`.

### Task 1 Manual Verification

- Manual action: Start a context-free, read-only fresh agent in this repo and
  ask it to identify the canonical instruction file, explain the root AGENTS
  layers, and state the default one-commit and multi-commit delivery cadence
  without writing, staging, committing, or pushing.
- Expected: It identifies `dot_codex/AGENTS.md` as the single canonical policy
  body; says `AGENTS.md`, `AGENTS.repo.md`, and `AGENTS-BASE.md` are routing or
  compatibility layers; and says a verified single-commit workflow pushes
  after that commit while a multi-commit workflow pushes once after the
  complete verified series.
- Observed: The fresh agent identified `dot_codex/AGENTS.md` as canonical;
  described `AGENTS.md` as the root routing shim, `AGENTS.repo.md` as a
  compatibility routing layer with no independent policy, and
  `AGENTS-BASE.md` as a deprecated compatibility shim; and reported that a
  verified single commit pushes after verification while a multi-commit series
  pushes once after the complete series is verified unless the user requests
  another cadence. It performed no Git writes.
- Status: PASS.

## Global Constraints

- Work on `feat/ai-workflow-optimization` in the existing working tree; do not
  create a worktree.
- Preserve the pre-existing `dot_codex/config.toml` modifications and never
  stage them as part of this work.
- Treat the pre-existing untracked `dot_agents/skills/metaprompt/` as the
  approved baseline; record its original SHA-256 and preserve its core
  compile-and-gate behavior.
- Source archive revision:
  `5c86715f453f0eca188451a48bf5b165831d8b29`.
- Use clean-room paraphrases. Never copy vendor prompt bodies, hidden policies,
  tool schemas, personalities, or binary-extracted skills verbatim.
- Keep only universal invariants in always-loaded instructions. Put verbose or
  conditional guidance in skills or one-level references.
- Keep each `SKILL.md` below 500 words where practical and validate every skill
  with baseline and forward scenarios before moving to the next skill.
- Combined `AGENTS.md` and `dot_codex/AGENTS.md` bytes must fall at least
  30% from the 34,805-byte baseline with no required-behavior regression.
- Single-commit workflows push after verification. Multi-commit workflows push
  once after the full verified series.
- Update README, skill catalog, smoke tests, provenance, and plan progress in
  the same commits as the behavior they document.

---

### Task 1: Persist Baseline And Streamline The Instruction Contract

**Files:**

- Create: `.agent/PLANS.md`
- Create: `docs/ai-workflow-optimization.md`
- Modify: `AGENTS.md`, `AGENTS.repo.md`, `dot_codex/AGENTS.md`
- Modify: affected Git workflow skills, their active metadata, and canonical
  feedback memory
- Modify: `dot_agents/skills/commit-dirty/agents/openai.yaml`
- Modify: `dot_agents/skills/commit-session/agents/openai.yaml`
- Test: `tests/test_ai_workflow_contract.py`

**Produces:** One canonical instruction body, compact routing shims, an
executable plan contract, and one push policy.

- [x] Capture instruction sizes, duplicate blocks, current Git state, source
      revision, and the protected metaprompt hash.
- [x] Write the contract test first and verify it fails for the missing plan
      contract, duplicated active instructions, and conflicting push policy.
- [x] Add `.agent/PLANS.md` with decision-complete requirements, checkboxes,
      assumptions, verification evidence, review notes, and same-commit plan
      updates.
- [x] Keep `dot_codex/AGENTS.md` canonical; convert root `AGENTS.md` and
      `AGENTS-BASE.md` to concise routing/compatibility layers and move
      historical provenance to the optimization document.
- [x] Collapse redundant planning, decomposition, subagent, verification, and
      done-output prose without removing bug reproduction, docs, testing,
      safety, and verification invariants.
- [x] Canonicalize worktree, push, refresh, feedback-memory, and lessons
      boundaries. Append the chosen push preference to the canonical feedback
      log; never rewrite old entries.
- [x] Run the focused contract test and record red/green evidence.

### Task 2: Build The AI Workflow Doctor

**Files:**

- Create: `scripts/executable_ai-workflow-doctor`
- Create: `dot_agents/skills/ai-workflow-doctor/`
- Test: `tests/test_ai_workflow_doctor.py`

**CLI:**

```text
ai-workflow-doctor [--repo PATH] [--format text|json]
                   [--snapshot PATH] [--compare PATH] [--check]
```

**Produces:** Deterministic instruction metrics and structural validation.

- [ ] Run baseline agent scenarios without the skill and record concrete
      omissions or over-broad behavior.
- [ ] Write CLI tests first for text/JSON output, snapshots, comparisons,
      normalized duplicate blocks of at least 200 characters, broken local
      references, missing plan contracts, uncatalogued skills, missing source
      provenance, and `--check` exit codes; verify they fail.
- [ ] Implement the minimal standard-library CLI to pass the tests. Semantic
      conflicts must be reported for agent review, not guessed by regex.
- [ ] Initialize and write the concise skill, `SOURCE.md`, and
      `agents/openai.yaml`; point it at the executable instead of duplicating
      CLI documentation.
- [ ] Run code tests, skill validation, and forward scenarios before marking
      this task complete.

### Task 3: Add Research Routing To Metaprompt

**Files:**

- Modify: `dot_agents/skills/metaprompt/SKILL.md`
- Create: `dot_agents/skills/metaprompt/references/research-routing.md`
- Create: `dot_agents/skills/metaprompt/SOURCE.md`
- Create/update: `dot_agents/skills/metaprompt/agents/openai.yaml`

**Produces:** Conditional broad-to-narrow retrieval, competing-hypothesis
queries, prior-evidence retrieval, bounded output, and saturation stopping.

- [ ] Run baseline scenarios against the unmodified skill and record failures.
- [ ] Add one short conditional hook; move enough detail out of `SKILL.md` that
      its byte count does not increase.
- [ ] Preserve the mandatory compiled-prompt output and explicit `go` gate.
- [ ] Validate metadata and forward-test trivial, standard, and complex
      research prompts before continuing.

### Task 4: Add Compact Context Handoffs

**Files:** Create `dot_agents/skills/context-handoff/` with `SKILL.md`,
`SOURCE.md`, and `agents/openai.yaml`.

**Produces:** A maximum 600-word handoff with Goal and Done Criteria,
Constraints, Decisions, Current State, Evidence and Failed Attempts, Artifacts,
Blockers, and Ordered Next Actions.

- [ ] Run baseline handoff scenarios without the skill and capture omissions,
      transcript duplication, or weak next actions.
- [ ] Initialize the skill and write the minimum positive output contract that
      addresses those failures.
- [ ] Forward-test normal handoff, low-context, and failure-heavy scenarios;
      confirm referenced artifacts replace large copied content.
- [ ] Validate metadata and word budget before continuing.

### Task 5: Add Runtime-Surface Verification

**Files:** Create `dot_agents/skills/runtime-verify/` with `SKILL.md`,
`SOURCE.md`, and `agents/openai.yaml`.

**Produces:** Verification records with Action, Expected, Observed, Evidence,
and one Adjacent Edge Probe for CLI, API, browser, package, or rendered-config
surfaces.

- [ ] Run baseline scenarios without the skill and capture test-only or
      evidence-free completion claims.
- [ ] Initialize a concise routing skill that composes existing Playwright,
      screenshot, and verification skills; it must never replace automated
      tests.
- [ ] Forward-test CLI, browser, and no-runtime-surface scenarios.
- [ ] Validate metadata and ensure the skill abstains when automated tests
      already prove the complete observable behavior.

### Task 6: Integrate Documentation, Smoke Coverage, And Measurement

**Files:** Modify `README.md`, `dot_agents/skills/README.md`,
`docs/smoke-tests.md`, `docs/ai-workflow-optimization.md`, and this plan.

- [ ] Record the adopt/adapt/already-covered/reject matrix and source paths.
- [ ] Document the doctor CLI, optimized instruction hierarchy, shared
      Codex/Claude skill installation, and the three new capabilities.
- [ ] Add stable Action/Expected smoke tests for doctor checks, metaprompt
      research routing, handoff shape, runtime verification, and skill
      discovery.
- [ ] Compare post-change metrics to `/tmp/ai-workflow-baseline.json` and record
      the results without inventing unavailable runtime token measurements.
- [ ] Run focused tests, full workflow tests, README gate, targeted chezmoi
      dry-run, and live/ tracked Codex config comparison.
- [ ] Request task and whole-branch reviews; fix every Critical or Important
      issue and re-run covering tests.

## Commit Plan

1. `refactor: streamline AI workflow instructions`
2. `feat: add AI workflow optimization skills`

Run the README gate before each commit. Keep this plan's matching progress
updates in each commit, leave `dot_codex/config.toml` unstaged, and push once
after the complete verified series.

## Review Notes

- Task 1 completed on 2026-07-13. The focused contract test first failed with
  five expected failures, then passed after the instruction, policy, and
  documentation changes.
- Acceptance review added contract coverage for the `commit-dirty` and
  `commit-session` OpenAI metadata prompts and made `tasks/lessons.md` point
  to the newest canonical feedback preference instead of duplicating it. The
  final focused suite passes all six tests.
- Independent review restored exact system-design routing, moved README
  narrative invariants into the lazy README contract, brought this active plan
  into compliance with `.agent/PLANS.md`, and corrected smoke and byte labels.
  Strengthened assertions first failed in five expected areas, then all eleven
  focused tests passed.
- Final re-review found no Critical or Important findings after a context-free,
  read-only manual routing check was recorded as `PASS` and covered by the
  contract test.
- Combined active instruction bytes fell from 34,805 to 9,817 (71.8%).
- The protected `dot_codex/config.toml` diff and metaprompt baseline were not
  modified. Tasks 2 through 6 remain pending.
