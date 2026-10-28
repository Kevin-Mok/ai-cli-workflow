# Local Skills Catalog

These repo-tracked skills provide reusable Codex workflows. Choose by task below
and open the linked source. This catalog covers `dot_agents/skills/`; external
skills and Codex built-ins have separate install and provenance boundaries.
The approved relevance cull retains `last30days` and merges overlapping planning
and handoff workflows instead of removing their safeguards.

## Instruction Quality And Memory

- [`lean-instructions`](lean-instructions/SKILL.md): Apply measured instruction
  efficiency techniques when adding to AGENTS.md or adding/editing a skill.
- [`ai-workflow-doctor`](ai-workflow-doctor/SKILL.md): Audit active instruction
  context, references, plan contracts, provenance and skill-catalog drift.
- [`skill-eval`](skill-eval/SKILL.md): Evaluate a named skill with real tasks,
  human-calibrated binary grading and blind comparisons.
- [`feedback-memory`](feedback-memory/SKILL.md): Append durable cross-task user
  preferences to the canonical feedback log.
- [`postmortem-memory`](postmortem-memory/SKILL.md): Retrieve reviewed incident
  remedies before troubleshooting and keep their evidence and learning current.
- [`personal-context`](personal-context/SKILL.md): Retrieve relevant personal and
  source-backed project briefs. Private records stay outside tracked artifacts.
- [`second-brain-session`](second-brain-session/SKILL.md): Retrieve established
  project/session context and prepare confirmation-gated session closeouts.
- [`context-handoff`](context-handoff/SKILL.md): Maintain a long-task brief,
  observable acceptance criteria, goal, evidence review and progress note; hand
  off strict criterion-by-criterion evidence after interruption or compression.

## Git And Delivery

Delivery remains best-effort within verified scope. Planning-only requests stay
read-only; unsafe content and unrelated work remain excluded. Matching plans,
tests and documentation accompany the change they describe.

- [`commit-plan-push`](commit-plan-push/SKILL.md): Plan dirty work oldest-to-newest.
  Planning-only mode inspects and proposes without Git writes; explicit execution
  requests create safe coherent commits, then push once after the full series.
- [`commit-dirty`](commit-dirty/SKILL.md): Verify and ship the authorized dirty
  worktree in a focused commit, reporting failed checks and unsafe residuals.
- [`commit-session`](commit-session/SKILL.md): Ship only verified changes touched
  during the current session, preserving unrelated work and staged changes.
- [`readme-recruiter-sync`](readme-recruiter-sync/SKILL.md): Check README truth,
  onboarding, usage, stack rationale and recruiter value at the delivery gate,
  during README work, or when a documented public interface changes.
- [`smoke-test-capture`](smoke-test-capture/SKILL.md): Maintain reusable grouped
  Action/Expected manual checks with the change that creates or alters them.

- [`grok-cli-handoff`](grok-cli-handoff/SKILL.md): Verify remote-assistant
  authorization, local checkout evidence and cooperative STOP handling.

## Explicit Task Workflows

- [`night`](night/SKILL.md): Run an explicitly requested unattended overnight job
  on a local branch, commit without pushing, and leave a handoff note.
- [`morning`](morning/SKILL.md): Read the night handoff and branch, summarize the
  evidence, and gather choices before taking the next action.
- [`next-tasks`](next-tasks/SKILL.md): Propose a bounded set of verifiable tasks
  from current repository evidence, then execute only the selected task.
- [`fish-alias`](fish-alias/SKILL.md): Add or replace a fish command, directory or
  file shortcut using the established mappings and conflict handling.

## Prompts And Research

- [`metaprompt`](metaprompt/SKILL.md): Create, sharpen or template prompts using
  Sentry's pinned workflow and save the compiled artifact without executing it.
  See the [source and reviewed update record](metaprompt/SOURCE.md).
- [`Metaprompt & Run`](metaprompt-run/SKILL.md) (`$metaprompt-run`): Compile and
  save the request, then start one fresh Codex conversation to execute it within
  the user's existing authorization.
- [`last30days`](last30days/SKILL.md): Research recent community and web discussion
  and check source health. Its imported package has a local [source record](last30days/SOURCE.md).

## Frontend And Browser Work

- [`frontend-design`](frontend-design/SKILL.md): Build frontend web interfaces
  from confirmed audience, use cases and brand context; save agreed missing
  design context in `.impeccable.md` for later sessions.
- [`brand-system-designer`](brand-system-designer/SKILL.md): Develop repo-native
  visual identity, logo, typography, favicon and social asset guidance.
- [`playwright`](playwright/SKILL.md): Automate real browser navigation,
  screenshots, extraction and UI debugging. Load it before Playwright commands.

- [`vercel-react-best-practices`](vercel-react-best-practices/SKILL.md): Explicit
  React/Next.js performance review against pinned Vercel guidance.
- [`shadcn`](shadcn/SKILL.md): Explicit shadcn/ui component, registry and preset
  work; load detailed workflows and rules only when needed.
- [`impeccable`](impeccable/SKILL.md): Pinned explicit web design commands for
  critique, audit, refinement and implementation.

The pinned local Impeccable replaces its moving external installer; see
[the managed design guide](../../docs/design-skills.md). Codex's
`.system` imagegen and openai-docs skills remain runtime-provided rather than
copied into this catalog. A source cull does not delete installed or upstream
files. Live installation changes and catalog reloads require their own verified
workflow; the trim task performs neither refresh-config nor chezmoi apply.
