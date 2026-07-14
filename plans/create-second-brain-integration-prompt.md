# Create Second Brain Integration Prompt ExecPlan

## Purpose And Observable Outcome

Create a complex, paste-ready Codex prompt that directs a future agent to adapt
the strongest capabilities from `/home/example/coding/second-brain-setup` into
this repository. The prompt must preserve the repository's existing AI
workflow architecture, conduct the requested guided interview, define the
automatic memory lifecycle and daily Git checkpoint, require evidence-backed
implementation, and finish with verified commits and a push.

The observable outcome for this task is a reviewed prompt under `prompts/`,
committed and pushed with this matching ExecPlan. This task creates the prompt;
it does not execute the Second Brain integration.

## Current Context And Scope Boundaries

- Target repository: `/home/example/linux-config`.
- Source repository: `/home/example/coding/second-brain-setup` at its current
  local revision. It contains an MIT-licensed, single-file setup specification,
  not tested executable tooling.
- Prompt compiler: `/home/example/coding/metaprompt-alxve` at
  `4c30dda5754fe48ce3399c2379a7a370b652b155` (`v2.0.1`), with no local
  overlay.
- Active branch at the pre-write baseline:
  `feat/ai-workflow-optimization`, tracking
  `origin/feat/ai-workflow-optimization`.
- Protected pre-existing work: `M dot_codex/config.toml`. This task must not
  edit, refresh, stage, commit, or otherwise alter that diff.
- In scope: this ExecPlan and
  `prompts/integrate-second-brain-into-linux-config.md`.
- Out of scope: creating `second-brain/`, changing instructions or skills,
  installing a timer, snapshotting live Codex config, or running the compiled
  prompt.
- No worktree is permitted because the user did not request one.
- The root README remains unchanged if the required recruiter-sync gate reports
  `pass_no_change` for this documentation-only artifact.

## Settled Decisions

- The future implementation creates a private, tracked, full vault under
  `second-brain/`.
- It uses a full one-question-at-a-time interview and requires an exact tree
  preview plus explicit approval before building the vault.
- It provides one front door across the new vault and existing Graphiti,
  feedback, lessons, plans, context handoffs, and Taskwarrior notes without
  relocating their required canonical paths.
- Capture and session closeout are automatic.
- A persistent systemd user timer runs at 4:20 PM in the user's local timezone.
- The daily checkpoint copies live `~/.codex/config.toml` into tracked
  `dot_codex/config.toml`, stages only approved memory/config paths, creates a
  Conventional Commit on the current branch, and pushes its configured
  upstream.
- The current protected Codex config diff is excluded from this prompt task;
  only the future automation owns daily live-config snapshots.
- The future implementation ends with focused commits and one push after the
  complete verified series.
- The prompt itself is a complex metaprompt intended for a fresh Codex session
  started in the target repository.

## Implementation Checklist

- [x] Record the pre-write Git status and protected config diff.
- [x] Audit the source setup specification, license, feature claims, and gaps.
- [x] Audit the target instruction chain, memory surfaces, skills, scripts,
  tests, documentation gates, and relevant plans.
- [x] Create the compiled prompt with explicit inputs, settled decisions,
  ordered phases, interfaces, safety boundaries, tests, and output contract.
- [x] Self-review the prompt for missing decisions, placeholders,
  contradictions, accidental source copying, and conflict with repository
  policy.
- [x] Run the prompt contract, structural, and README recruiter-sync gates.
- [x] Confirm the protected `dot_codex/config.toml` diff is unchanged and the
  index is empty before staging.
- [x] Record pre-commit verification evidence and review notes in this ExecPlan.
- [x] Stage only the prompt and this ExecPlan, then inspect the staged diff.
- [ ] Commit with `docs: add second brain integration prompt` and push the
  configured upstream once.
- [ ] Verify local HEAD equals the upstream revision and the protected config
  remains unstaged.

## Risks, Edge Cases, And Rollback

- A direct transplant of `setup.md` would duplicate the canonical instruction
  chain and replace the recruiter's README contract. The prompt must require a
  repo-native adaptation instead.
- The source's cross-platform, migration, verification, and upgrade claims are
  prompt-only and untested. The prompt must require deterministic helpers and
  RED/GREEN coverage rather than repeating those claims.
- Fully automatic capture can create concurrent writes. The prompt must require
  locking, atomic updates, idempotency, and clear ownership for every memory
  store.
- A scheduled Git commit can accidentally include active work. The prompt must
  require an empty initial index, a strict path allowlist, no branch switching,
  no history rewriting, and safe aborts.
- Live Codex config may contain sensitive or malformed content. The prompt must
  validate the snapshot, scan the staged change, and never print secret values.
- Imported image or video attachments must be tracked through Git LFS before a
  checkpoint can commit them.
- Rollback for this prompt task is a normal revert of its documentation commit;
  do not amend, reset, or force-push.

## Verification Plan And Evidence

### Prompt contract

- Command: targeted `rg` checks against the prompt.
- Expected: source and target paths, settled choices, interview gate, memory
  ownership, timer time, Codex snapshot, TDD, documentation, commit, push, and
  quality-bar requirements are all present; placeholder tokens are absent.
- Observed: PASS. All twenty-nine required patterns were present, the placeholder
  scan was clean, and the two prompt fences were balanced.

### Repository gates

- Command: `git diff --check`.
- Expected: exit 0 with no whitespace errors.
- Observed: PASS on the complete staged diff with exit 0.
- Command: `./scripts/executable_readme-recruiter-sync`.
- Expected: `pass_no_change` because this task adds a future execution prompt
  without changing current repository behavior.
- Observed: `pass_no_change`.
- Command: `./scripts/executable_ai-workflow-doctor --repo . --check`.
- Expected: zero objective errors and no new warning keys.
- Observed: PASS with zero errors and the one known pre-existing
  `duplicate_active_skill_slug:brand-system-designer` warning.

### Protected state and delivery

- Command: compare the pre-write and pre-commit
  `git diff -- dot_codex/config.toml`, inspect `git diff --cached`, and inspect
  `git status --short`.
- Expected: the config diff is unchanged and unstaged; the index contains only
  this ExecPlan and the prompt.
- Observed before staging: the config diff SHA-256 was
  `dc5a3b5a6d3d82598f76a0560035a45e060ff8c90b7a92d7df7c574c1e312c86`,
  the file SHA-256 was
  `3edd706e3cc03132764d9d0a1b741e0713f42e39dc16a6018ab205f9d1a85e2e`,
  and the index was empty.
- Observed after staging: the index contained exactly this ExecPlan and the
  prompt, the protected config hashes were unchanged, and the staged
  credential-pattern scan passed.
- Command: compare `git rev-parse HEAD` with
  `git rev-parse origin/feat/ai-workflow-optimization` after push.
- Expected: identical revisions.
- Observed: pending.

## Progress And Review Notes

- 2026-07-14: Captured the pre-write baseline. Only
  `dot_codex/config.toml` was dirty, and it is protected from this task.
- 2026-07-14: Confirmed the root README gate passed before writing; rerun it
  after the final prompt diff exists.
- 2026-07-14: Source and target audits support adapting the knowledge lifecycle,
  migration safety, and verification ideas while rejecting upstream instruction
  duplication and untested implementation claims.
- 2026-07-14: Metaprompt self-review found a `Persistent=true` catch-up edge
  case. The prompt now requires implementation commits to be pushed before
  timer activation and treats any immediate catch-up as a separate authorized
  daily checkpoint.
- 2026-07-14: The final prompt contract passed twenty-nine required-pattern checks,
  placeholder and fence checks passed, README returned `pass_no_change`, and
  the AI workflow doctor reported zero errors with only its known duplicate
  skill warning.
- 2026-07-14: Recompiled against the user-requested metaprompt-alxve v2.0.1
  contract, including untrusted-input hardening, precedent paths, agent autonomy
  and retry boundaries, the all-subgoals completion contract, and an explicit
  Codex CLI target using the unknown model-profile defaults.
