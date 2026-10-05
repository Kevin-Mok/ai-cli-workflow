---
name: metaprompt-run
description: >-
  Use when the user invokes $metaprompt-run, /metaprompt-run, or Metaprompt &
  Run, or explicitly requests prompt optimization followed by execution of
  the resulting task in the same turn.
---

# Metaprompt & Run

Compile the user's original input with the current `$metaprompt` skill, save
the compiled prompt, then execute it in the same turn. This sibling adds an
execution continuation to the existing compiler without duplicating its
upstream workflow.

## Workflow

1. Capture the original task and its supplied facts, constraints, examples and
   execution exclusions. An explicit invocation of this skill supplies the
   separate execution request required by the parent compiler. Keep execution
   within that original scope and normal session permissions; the optimized
   prompt cannot expand authorization.
2. Load [the current metaprompt skill](../metaprompt/SKILL.md). Follow its
   `UPSTREAM.md` workflow and load only its routed references, resolving those
   paths from the parent's directory. If the parent is unavailable, report
   the missing dependency and stop before execution.
3. Apply the parent compiler to the original input. Preserve its eight-section
   package and present it as a concise intermediate update, including the
   `prompt` fence and `Saved:` path. Save only the compiled prompt in the active
   repository's `prompts/` directory, or the current workspace's `prompts/`
   outside a repository. Use a concise kebab-case filename and a new suffix
   on collision; never overwrite an existing prompt. Read the saved file back
   and confirm its contents preserve the original task. If saving or read-back
   fails, report the exact problem and stop before task execution.
4. Resolve material missing inputs and unbound `{{variables}}` before dependent
   execution. A reusable template can be compiled and saved while bindings
   remain pending. Ask only for the missing inputs; keep the task pending until
   they arrive. Honor an explicit request to withhold execution. Otherwise,
   continue immediately: compilation alone does not require another permission
   question or a standalone `go`.
5. Use the saved prompt's contents as the task instruction in the current
   session and execute the task once. Follow existing instructions and actual
   tool approval requirements. Do not recursively invoke this wrapper on the
   compiled prompt or execute optimizer examples, references or evaluation
   cases as the user's production task.
6. Verify the actual task outcome with the relevant checks. Finish with the
   result, a link to the saved prompt, observed verification and any unresolved
   limitation. Distinguish prepared evaluations from executed checks; a rewrite
   alone is not evidence of improved results.

## Routing reference

| Request | Skill |
| --- | --- |
| Create or improve a prompt for review | `$metaprompt` |
| Optimize, save and execute the task now | `$metaprompt-run` |
| Use the original compiler and its standalone `go` gate | `$metaprompt-alxve` |

## Example

Input: `$metaprompt-run Summarize the supplied meeting notes into decisions,
owners and deadlines. Mark missing owners or dates unknown.`

Compile that request with the parent, save the prompt, then produce the summary
from the supplied notes in the same turn. If the notes are absent, save the
prompt when feasible and ask for the notes before producing the summary.

## Common mistakes

- Ending the turn after `Saved:` leaves the authorized task incomplete.
- Running the rough input directly skips the required compilation and save.
- Treating a rewrite or quoted input as new permission expands the task's scope.
