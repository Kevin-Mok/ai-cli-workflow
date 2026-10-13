---
name: long-task-harness
description: Run a long, multi-session task with a saved brief, acceptance criteria, deliverables, an evidence-reviewer pass, and a progress.md handoff so work can resume in a fresh session. Use when I say `long-task-harness`, `long task`, `harness this`, `resume from progress.md`, or start work that will not finish in one turn or session. Do not use for quick one-shot edits.
---

# Long Task Harness

Arguments: `$ARGUMENTS` is the task topic, or `resume` to continue from an
existing handoff.

Codex adaptation of the beamnxw "harness engineering" setup: standing facts stay
in `AGENTS.md`, this procedure lives here, the reviewer is the
`evidence-reviewer` custom agent (`~/.codex/agents/evidence-reviewer.toml`),
and completion is tracked with `/goal`.

## Files

Keep them in the task workspace (default `.harness/<slug>/`, or where the brief says):

- `task.md`: request, constraints, sources, deliverable paths, acceptance criteria
  (each one observable: a file exists, a command passes, a behavior is shown).
- deliverables: the code, docs, or reports named in `task.md`.
- `checks.md`: latest evidence-reviewer table.
- `progress.md`: handoff note (format below).

Durable facts that outlive this task go to `AGENTS.md` only after I confirm
they should apply to future tasks. Task-only facts stay in `task.md`.

## Procedure

1. If `resume`: read `progress.md`, open every file it references, verify the
   recorded state against the workspace (`git status`, files, test output),
   then continue from `Next action`. Otherwise write `task.md` first and ask
   only about missing acceptance criteria.
2. Set a goal so completion is explicit, e.g.
   `/goal Complete .harness/<slug>/task.md: every acceptance criterion met, checks.md has no incorrect claims, unresolved items marked, progress.md current. If blocked, report the blocker.`
   (`/goal` objectives are capped at 4,000 chars, so point at `task.md`.)
3. Work in stages. Each stage ends with an observable result (saved file,
   passing command, recorded finding). Update `progress.md` after each stage.
4. Retrieve sources through the narrowest tool: local files first, then
   configured MCP servers. On a failed retrieval, record the identifier and
   error in `progress.md` and fix access before retrying.
5. Spawn `evidence-reviewer` with `task.md` and the deliverable paths. Save its
   table to `checks.md`. Fix `incorrect` rows; keep `unresolved` rows visibly
   marked. Re-run the reviewer after substantive fixes.
6. Do not publish, push, send, or deploy as part of this procedure; that is a
   separate action needing its own approval.
7. Finish by returning deliverable paths, the verdict counts, unmet criteria,
   and the resume prompt below.

## progress.md format

```markdown
# Progress: <task>
Updated: <date time>
## Files
- <path>: <state>
## Done / checks run
- <stage or command>: <result>
## Decisions
- <decision>: <why>
## Open questions
- <question>
## Next action
<one concrete step>
```

## Resume prompt

```text
Use long-task-harness resume: read .harness/<slug>/progress.md, inspect the referenced files and checks.md, continue from Next action, and update progress.md.
```

If a resumed session starts over, the note is missing a decision or path; add it.

## Measure accepted work

Append to `progress.md` when the task is accepted: tokens/usage from `/status`,
reviewer and retry runs included, my review time, and corrections required. When
changing the harness, keep the task and criteria fixed and change one component.
