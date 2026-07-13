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
- The full plan spans six tasks. Tasks 1 through 5 now cover compact instruction
  routing, the ExecPlan and Git delivery contracts, the deterministic doctor,
  progressive metaprompt disclosure, context handoffs, and the evidence-backed
  rejection of a redundant runtime skill. Task 6 implementation and final
  verification and all required reviews are complete. This finalized plan lands
  in the second planned commit before the verified series is pushed.
- The pre-existing `dot_codex/config.toml` diff remains protected from edits and
  staging. The pre-existing metaprompt baseline was hashed before its approved,
  measured Task 3 refactor.
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
- The pre-existing `brand-system-designer` slug is exposed from both tracked
  skill roots. The doctor keeps this as a non-blocking warning; do not choose an
  owner by deleting user files without explicit authorization.
- Rollback Task 1 by reverting only its instruction, policy, test, plan, and
  documentation files. Preserve the protected config diff and metaprompt tree.
- Roll back Tasks 2 through 6 by reverting the second planned commit, then
  reapply chezmoi so the doctor, skills, metaprompt layout, and Claude skill-link
  generator return to their prior tracked state. Preserve
  `dot_codex/config.toml` and the pre-existing duplicate skill directories.

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

### Task 2 Doctor Contract

- Command: `python3 tests/test_ai_workflow_doctor.py`
- Expected: All deterministic CLI, metric, drift, provenance, snapshot, and
  exit-code contracts pass.
- Observed: All seventeen tests passed and returned `OK`.
- Exit status: `0`.
- RED evidence: Before the executable existed, the same twelve-test suite
  produced eleven expected failures for the missing CLI and executable bit.
- Review RED evidence: Earlier regressions initially failed for a nested
  four-backtick fence, malformed nested schema-v1 fields, and simultaneous
  `--compare` plus `--snapshot`. A later captured RED run exposed five more
  gaps: cross-root duplicate detection, explicit source resolution, portable
  missing-archive behavior, cwd-independent installed invocation, and detailed
  text comparisons. All now pass; text findings also include actionable
  locations and provenance fields.
- Final specialist RED evidence: two added regressions failed because relative
  source archives used the caller CWD and valid balanced-parenthesis or
  angle-bracket CommonMark destinations became false errors. Relative archives
  now resolve from the audited repo root and both valid link forms pass.

### Task 2 Repository And Skill Checks

- Command: `./scripts/executable_ai-workflow-doctor --repo . --check`
- Expected: Exit `0` with no objective errors in the current AI workflow
  surface.
- Observed at the Task 2 checkpoint: Status `pass`; zero errors, zero warnings,
  9,817 active-instruction bytes, and 45 actual / 45 catalogued skills.
- Exit status: `0`.
- Command: `python3 /home/example/.codex/skills/.system/skill-creator/scripts/quick_validate.py dot_agents/skills/ai-workflow-doctor`
- Expected: The official validator reports a valid skill.
- Observed: `Skill is valid!`
- Exit status: `0`.
- Command: `./scripts/executable_ai-workflow-doctor --repo . --format json --compare /tmp/ai-workflow-baseline.json`
- Expected: An unchanged comparison has zero metric deltas and no added or
  resolved finding keys.
- Observed: All three active-total deltas were zero; added, resolved, and
  unchanged finding-key arrays were empty.
- Exit status: `0`.

### Task 2 Manual Forward Verification

- Manual action: Start a context-free agent with only the instruction to run
  the repo-tracked doctor JSON audit and report its evidence without writes.
- Expected: It reports the structured status and metrics, does not claim a
  semantic resolution absent from the findings, and provides the exact future
  compare command.
- Observed: It reported exit `0`, status `pass`, zero errors/warnings, 9,817
  bytes, 9,817 characters, about 2,455 tokens, and 45 / 45 skills. It reported
  no auto-resolution because findings were empty and returned the compare
  command using `/tmp/ai-workflow-baseline.json`.
- Status: PASS.

### Task 3 Metaprompt Contract And Measurement

- Command: `python3 tests/test_metaprompt_contract.py`
- Expected: The compact entrypoint, one-hop references, activation boundary,
  compile/gate behavior, post-go routing, metadata, and provenance exclusions
  pass.
- Observed: All seven tests passed and returned `OK`.
- Exit status: `0`.
- Initial RED evidence: The unmodified 3,442-word skill produced three failures
  and four missing-file errors for the compact/reference/metadata contract.
- Review RED evidence: Two added assertions then failed for the lost standalone
  `go`/one-word-fact activation boundary and an execution reference that could
  load before `go`; both now pass.
- Command: `wc -wc dot_agents/skills/metaprompt/SKILL.md dot_agents/skills/metaprompt/references/*.md`
- Observed: The always-loaded entrypoint is 404 words / 2,855 bytes, down from
  3,442 words / 21,213 bytes. All four Markdown files total 15,312 bytes.
- Command: `python3 /home/example/.codex/skills/.system/skill-creator/scripts/quick_validate.py dot_agents/skills/metaprompt`
- Observed: `Skill is valid!`
- Exit status: `0`.

### Task 3 Manual Forward Verification

- Manual action: Run fresh Trivial, current-source Standard, and read-only
  Complex audit scenarios. Put `run` inside a Standard revision, then send
  standalone `go`.
- Expected: Trivial stays lean; the revision re-gates; standalone `go` executes;
  current research uses official sources; the large audit selects parallel
  workflow routing without mutating code.
- Observed: The Trivial output was one sentence plus the gate. The revision
  recompiled and re-gated without executing. Standalone `go` produced a cited
  GitHub/GitLab comparison from official sources. The Complex prompt selected a
  read-only parallel audit and, on `go`, asked for the missing logs/run IDs
  rather than fabricating evidence.
- Status: PASS.

### Task 4 Context-Handoff Contract And Forward Verification

- Command: `python3 tests/test_context_handoff_contract.py`
- Expected: Files, ordered headings, 600-word output cap, DC evidence mapping,
  None/Unknown semantics, failure grouping, literal next actions, metadata,
  provenance, catalog, and doctor compatibility pass.
- Observed: All six tests passed and returned `OK`.
- Exit status: `0`.
- Initial RED evidence: Before initialization, all six tests failed explicitly
  because required skill files were absent.
- Review RED evidence: A new literal-action assertion failed after a forward
  output said “original command.” The skill now requires literal executable
  commands or precise path-scoped edits and bans anaphora; the test and a fresh
  failure-heavy scenario pass.
- Command: `wc -w dot_agents/skills/context-handoff/SKILL.md`
- Observed: `390`, below the 500-word skill target.
- Command: `python3 /home/example/.codex/skills/.system/skill-creator/scripts/quick_validate.py dot_agents/skills/context-handoff`
- Observed: `Skill is valid!`
- Exit status: `0`.
- Manual action: Run fresh normal, low-context, and failure-heavy scenarios.
- Observed: All three returned the eight headings below 600 words. The normal
  handoff mapped verified/open DCs and protected state; low-context recovery
  kept missing facts Unknown and started from the authoritative plan; the
  failure-heavy retry grouped stable signatures and used literal commands,
  paths, change facts, and stop conditions without blind retries.
- Status: PASS.

### Task 6 Final Measurement And Workflow Checks

- Command: `./scripts/executable_ai-workflow-doctor --repo . --verify-sources --format json --compare /tmp/ai-workflow-baseline.json --snapshot /tmp/ai-workflow-final.json --check`
- Expected: A passing schema-v1 final snapshot, resolved declared local source
  evidence, no objective errors, and no active-instruction regression from the
  Task 2 baseline; any reviewer-added diagnostic must remain explicit.
- Observed: Exit `0`, status `pass`, zero errors, one warning, 46 actual / 46
  catalogued skills, 9,817 active bytes, and about 2,455 estimated tokens. All
  active-total deltas are zero. The added finding key
  `duplicate_active_skill_slug:brand-system-designer` identifies two
  pre-existing tracked copies across `.agents/skills/` and
  `dot_agents/skills/`; they remain because deleting user-owned files requires
  explicit authorization. The local archive commit and all declared
  primary/supporting paths resolved. The written snapshot remains
  comparison-free and reusable.
- Command: `chezmoi -S /home/example/linux-config apply -n -v /home/example/scripts/ai-workflow-doctor /home/example/.agents/skills/ai-workflow-doctor /home/example/.agents/skills/context-handoff /home/example/.agents/skills/metaprompt`
- Expected: Render the affected install surface without writing live files.
- Observed: Exit `0`; dry-run output proposed the cwd-independent installed
  doctor command plus doctor, context-handoff, and metaprompt
  source/metadata/reference changes under `~/.agents/skills/`.
- Command: `cmp -s /home/example/.codex/config.toml dot_codex/config.toml`
- Expected: Compare protected live/tracked config without overwriting either.
- Observed: Exit `0`; both SHA-256 values were
  `3edd706e3cc03132764d9d0a1b741e0713f42e39dc16a6018ab205f9d1a85e2e`.
- Command: `bash tests/test_claude_skill_links.sh`
- Expected: Directory-link installation preserves supporting references,
  removes only managed legacy links, remains idempotent, and refuses to
  replace a real user directory.
- RED/GREEN: The initial fixture failed against legacy flat `<name>.md` links;
  after the directory-link migration it passed all reference reachability,
  cleanup, idempotency, and conflict-safety checks.
- Exit status: `0`.
- Command: `python3 -m unittest discover -s tests -p 'test_*.py'`
- Expected: All Python workflow contracts pass.
- Observed: 41 tests passed in 2.220 seconds.
- Exit status: `0`.
- Commands: `bash tests/scripts/executable_codex_test.sh` and
  `bash tests/test_refresh_config_function.sh`
- Expected: Existing Codex and refresh-config workflow regressions pass.
- Observed: Both exited `0`. Direct file execution first returned `126` because
  these test files are non-executable; invoking their Bash interpreter ran the
  tests successfully. The protected config hash remained unchanged afterward.
- Command: `./scripts/executable_readme-recruiter-sync`
- Expected: The required README gate passes without an unrelated rewrite.
- Observed: `pass_no_change`.
- Exit status: `0`.

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
                   [--snapshot PATH] [--compare PATH] [--verify-sources]
                   [--check]
```

**Produces:** Deterministic instruction metrics and structural validation.

- [x] Run baseline agent scenarios without the skill and record concrete
      omissions or over-broad behavior.
- [x] Write CLI tests first for text/JSON output, snapshots, comparisons,
      normalized duplicate blocks of at least 200 characters, broken local
      references, missing plan contracts, uncatalogued skills, missing source
      provenance, and `--check` exit codes; verify they fail.
- [x] Implement the minimal standard-library CLI to pass the tests. Semantic
      conflicts must be reported for agent review, not guessed by regex.
- [x] Initialize and write the concise skill, `SOURCE.md`, and
      `agents/openai.yaml`; point it at the executable instead of duplicating
      CLI documentation.
- [x] Run code tests, skill validation, and forward scenarios before marking
      this task complete.

### Task 3: Reduce Metaprompt's Always-Loaded Context

**Files:**

- Modify: `dot_agents/skills/metaprompt/SKILL.md`
- Create: `dot_agents/skills/metaprompt/references/compilation-rules.md`
- Create: `dot_agents/skills/metaprompt/references/execution-routing.md`
- Create: `dot_agents/skills/metaprompt/references/examples.md`
- Create/update: `dot_agents/skills/metaprompt/agents/openai.yaml`
- Test: `tests/test_metaprompt_contract.py`

**Produces:** A behavior-preserving, progressively disclosed metaprompt whose
always-loaded `SKILL.md` is under 500 words while detailed compilation,
execution-routing, and example guidance remains available one hop away.

- [x] Run baseline scenarios against the unmodified skill. Its compiled prompt
      required current sources, narrowed queries, prior-evidence reuse,
      parallel independent checks, and a saturation stop, so a second
      research-routing policy would be redundant. The post-refactor standalone
      `go` forward run separately executed official-source research.
- [x] Write the extraction contract first and verify it fails on the unmodified
      3,442-word skill and missing reference/metadata files.
- [x] Extract detailed rules mechanically into three one-hop references; do
      not add a baseline-shaped `research-routing.md` or source provenance for
      behavior that was not adapted from the archive.
- [x] Preserve the mandatory compiled-prompt output and explicit `go` gate.
- [x] Validate metadata and forward-test trivial, standard, and complex
      research prompts before continuing.

### Task 4: Add Compact Context Handoffs

**Files:** Create `dot_agents/skills/context-handoff/` with `SKILL.md`,
`SOURCE.md`, and `agents/openai.yaml`.

**Produces:** A maximum 600-word handoff with Goal and Done Criteria,
Constraints, Decisions, Current State, Evidence and Failed Attempts, Artifacts,
Blockers, and Ordered Next Actions.

- [x] Run baseline handoff scenarios without the skill and capture omissions,
      transcript duplication, or weak next actions.
- [x] Initialize the skill and write the minimum positive output contract that
      addresses those failures.
- [x] Forward-test normal handoff, low-context, and failure-heavy scenarios;
      confirm referenced artifacts replace large copied content.
- [x] Validate metadata and word budget before continuing.

### Task 5: Confirm Runtime Verification Is Already Covered

**Files:** Record the baseline decision in this plan and
`docs/ai-workflow-optimization.md`; do not create a redundant skill.

**Produces:** An evidence-backed `already covered` decision that avoids another
always-available routing layer and its activation ambiguity.

- [x] Run a context-free baseline scenario without the proposed skill.
- [x] Confirm the existing verification rules reject test-only completion,
      require the actual user entrypoint, rendered/install evidence, invalid
      input, and consider an adjacent probe when it would add useful evidence.
- [x] Reject `runtime-verify` as redundant; preserve the measured baseline in
      `.superpowers/sdd/runtime-baseline-report.md` and the durable decision in
      the optimization document.

### Task 6: Integrate Documentation, Smoke Coverage, And Measurement

**Files:** Modify `README.md`, `dot_agents/skills/README.md`,
`docs/smoke-tests.md`, `docs/ai-workflow-optimization.md`,
`run_after_install-claude-skills.sh.tmpl`, `tests/test_claude_skill_links.sh`,
and this plan.

- [x] Record the adopt/adapt/already-covered/reject matrix and source paths.
- [x] Document the doctor CLI, optimized instruction hierarchy, shared
      Codex/Claude skill installation, two new capabilities, and the
      behavior-preserving metaprompt refactor.
- [x] Add stable Action/Expected smoke tests for doctor checks, metaprompt
      research routing, handoff shape, runtime verification, and skill
      discovery.
- [x] Replace legacy flat Claude skill links with documented directory links so
      one-hop references remain reachable; cover migration, idempotency, and
      non-symlink conflict safety with an isolated Bash regression.
- [x] Compare post-change metrics to `/tmp/ai-workflow-baseline.json` and record
      the results without inventing unavailable runtime token measurements.
- [x] Run focused tests, full workflow tests, README gate, targeted chezmoi
      dry-run, and live/ tracked Codex config comparison.
- [x] Request task and whole-branch reviews; fix every Critical or Important
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
- Task 2 completed with seventeen passing doctor tests and a valid compact skill.
  Its pre-review checkpoint had a clean 45 / 45 catalog audit, zero errors or
  warnings, a stable snapshot comparison, and a passing context-free forward
  scenario; final reviewer-added diagnostics are recorded under Task 6.
- Task 3 completed with seven passing contract tests, official validation,
  Trivial/Standard/Complex forward scenarios, and reviewer-driven activation
  and post-go routing fixes. Always-loaded metaprompt bytes fell 86.5%.
- Task 4 completed with six passing contract tests, official validation, three
  forward scenarios, and a reviewer-driven literal-action regression. Final
  skill size is 390 words; skill semantics have no remaining Critical or
  Important findings.
- Task 5 rejected a redundant runtime skill after its context-free baseline
  already demanded the real entrypoint, observed evidence, invalid input, and
  recommended an adjacent probe when relevant.
- Final clean-room re-review found no Critical or Important findings and found
  no exact normalized 80-character lines or 15-word windows copied from the
  source archive across the changed text files.
- Final doctor re-review found no Critical or Important findings after RED/GREEN
  fixes anchored relative source archives to the audited repo and accepted
  balanced, escaped, and angle-bracket CommonMark destinations.
- Final whole-branch review found no Critical or Important findings after all
  41 Python tests, shell regressions, three skill validators, doctor gates,
  README gate, chezmoi dry-run, config hashes, and diff checks passed.
- Combined active instruction bytes fell from 34,805 to 9,817 (71.8%).
- The protected `dot_codex/config.toml` diff remains untouched and excluded from
  the finalized implementation commit.
