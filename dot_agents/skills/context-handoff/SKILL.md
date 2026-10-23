---
name: context-handoff
description: Use for long tasks, acceptance criteria, progress.md, or handing off and resuming work after interruption, context compression, agent transfer, or a context-window boundary.
---

# Context Handoff

<!-- context-handoff: adapted -->

Manage long work through a saved brief and evidence, then create a continuation
artifact when handing off. Keep task-only facts in the task workspace; add
standing policy to AGENTS.md only after the user confirms it should persist.

## Long-task procedure

Use this branch for a long task, `harness this`, or work spanning sessions.
Default workspace: `.harness/<slug>/`, unless the task names another path.

1. For new work, write `task.md`: request, constraints, sources, deliverables,
   and observable acceptance criteria. Ask only for consequential missing criteria.
   For resume, read `progress.md` and every referenced file, including `checks.md`;
   verify workspace state before continuing the recorded next action.
2. Reuse the existing goal. Create a goal only when the user requested one;
   point its objective at `task.md` and its acceptance criteria. Keep the goal
   active until current evidence proves each criterion; report unresolved items.
3. Work in stages ending with saved output or an observed check. Update
   `progress.md` after each stage with paths, checks, decisions, questions and
   one concrete next action. Retrieve local sources before configured MCP tools;
   record failed source identifiers and errors before fixing access and retrying.
4. Spawn `evidence-reviewer` with `task.md` and deliverable paths. Save its
   claim-to-evidence table in `checks.md`; fix `incorrect` rows and visibly mark
   `unresolved` rows. Re-run the reviewer after substantive fixes.
5. Do not publish, push, send, or deploy from this procedure without separate
   authorization. Return deliverables, verdict counts, unmet criteria and a
   resume prompt: `Use context-handoff: read .harness/<slug>/progress.md, inspect
   its artifacts and checks.md, continue the next action, and update progress.md.`
6. When accepted, record available usage (including reviewers/retries), user
   review time and corrections in `progress.md`; label unknown measurements.
   Evaluate harness changes with the same task and criteria, one component at a time.

## Handoff artifact

Return only the handoff, at most 600 words, using the eight headings below in order.

Assign `DC#` IDs to every known done criterion and write exactly one evidence
record for every listed DC. Status meanings are strict: `met = verified pass`;
`open = known incomplete`; `failed = latest evidence contradicts it`;
`unknown = evidence is unavailable or stale`. Each record maps
`check → observed result → evidence link or recovery action`.

Use None only after an explicit check confirmed absence. Use Unknown when
something was not checked. Do not infer from absent or stale evidence. When
context is incomplete, make recovery from the authoritative plan, status, log,
or source artifact the first applicable next action.

Group repeated failures by stable failure signature. Record attempt count,
what changed between attempts, and an observable retry condition. Do not
propose the same retry while its condition is unchanged. Link artifacts instead
of copying logs, transcripts, code, or plans. Preserve literal paths, branches,
commands, protected-state constraints, and security restrictions.

```markdown
## Goal and Done Criteria
Goal: <one sentence>
- DC1: <observable acceptance criterion>

## Constraints
- <literal protected state, command, scope, or safety constraint>

## Decisions
- <settled decision and concise rationale>

## Current State
- <confirmed branch, work item, owner, and implementation/test state>

## Evidence and Failed Attempts
- DC1 — <met|open|failed|unknown> — <check> → <observed result> — <evidence link or recovery action>
- Failure: <stable signature> — Attempts: <count> — Last evidence: <link> — Changed since: <fact> — Retry when: <condition>

## Artifacts
- [artifact](path): <why the next agent needs it>

## Blockers
- None — <check that confirmed absence>
- or Unknown — <authoritative source or action needed>
- or <blocker and evidence>

## Ordered Next Actions
1. Owner: <agent or role> — Action: <exact command or edit> — Expected: <observable result> — Stop if: <condition>
```

Every next action includes `Owner:`, `Action:`, `Expected:`, and `Stop if:`.
Its Action contains a literal executable command or a precise path-scoped edit.
Never use anaphora such as original command, same command, or as above. Prefer
the smallest action that restores evidence or advances an open DC.
