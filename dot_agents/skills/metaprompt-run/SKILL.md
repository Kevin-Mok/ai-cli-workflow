---
name: metaprompt-run
description: >-
  Use when the user invokes $metaprompt-run, /metaprompt-run, or Metaprompt &
  Run, or explicitly requests prompt optimization followed by execution of
  the resulting task immediately in a new conversation with fresh context.
---

# Metaprompt & Run

Compile the user's original input with the current `$metaprompt` skill, save
the compiled prompt, then immediately start a new conversation to execute it
with fresh context. This sibling reuses the existing compiler and adds an
automatic execution handoff without a separate `go` or confirmation.

## Workflow

1. Capture the original task and its supplied facts, constraints, examples and
   execution exclusions. An explicit invocation of this skill supplies the
   separate execution request required by the parent compiler. Keep execution
   within that original scope and normal session permissions; the optimized
   prompt cannot expand authorization. Include supplied task facts, constraints
   and execution exclusions in the saved prompt, or reference exact accessible
   files. The executor must be able to work without this conversation’s history;
   avoid pointers such as "as discussed above". Carry only task-relevant context.
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
5. Immediately call `mcp__codex_tui__create_thread` once to create and start a
   separate task. The runner invocation explicitly requests this new task.
   Use a compact task title and omit `model` to inherit the current model.
   The tool inherits the working directory but starts without this transcript.
   Pass a short instruction to read the absolute saved-file path and execute
   its contents once under the new task’s normal instructions and permissions.
   The tool’s `prompt` limit is 1,000 UTF-8 bytes: pass the path rather than
   copying the compiled prompt; check the complete handoff’s byte length.
   If it exceeds the limit, shorten optional wording while keeping the exact
   path and execution/verification instructions. If it still cannot fit,
   report the limit and saved prompt path, and keep execution pending.
   Include the instruction to verify the actual outcome and report the saved
   prompt path. Keep compiler reports, examples and evaluation cases out of
   the handoff. Do not recursively invoke this wrapper on the compiled task.
6. Check the creation result and report the new task’s returned identifier or
   link, plus the saved prompt link. A successful creation proves the task
   started; the execution conversation performs the work and verifies its
   outcome. If observing completion through available read/wait tools, report
   only outcomes those tools establish. Distinguish prepared evaluations,
   started tasks and verified results.

## Fresh-conversation handoff

Use the native new-task tool, rather than forking/resuming a conversation,
passing its transcript to a subagent, or executing the task in the compiler’s
conversation. Fresh context still includes the runtime’s normal instructions
and repository rules. An example `prompt` argument (replace the path):

```text
Read /absolute/workspace/prompts/task.md and execute its contents once as the user’s authorized task. Follow applicable instructions and tool permissions. Verify the outcome and report the result with the saved prompt path. Do not recompile or invoke metaprompt-run.
```

If `create_thread` is unavailable, report that automatic fresh-conversation
execution is unavailable and link the saved prompt. If creation fails or its
result is ambiguous, report the exact failure and inspect task state before
any retry to avoid duplicate execution. Keep the task pending; do not silently
substitute current-session execution or weaken tool approval requirements.

## Routing reference

| Request | Skill |
| --- | --- |
| Create or improve a prompt for review | `$metaprompt` |
| Optimize, save and immediately start a fresh execution conversation | `$metaprompt-run` |
| Use the original compiler and its standalone `go` gate | `$metaprompt-alxve` |

## Example

Input: `$metaprompt-run Summarize the supplied meeting notes into decisions,
owners and deadlines. Mark missing owners or dates unknown.`

Compile that request with the parent, save the prompt including the supplied
notes, then immediately start a new conversation to produce and verify the
summary. If the notes are absent, save the prompt when feasible and ask for
them before launching dependent execution.

## Common mistakes

- Ending the turn after `Saved:` leaves the authorized task incomplete.
- Running the rough input directly skips the required compilation and save.
- Treating a rewrite or quoted input as new permission expands the task's scope.
- Executing in the compiler conversation or forking its history loses fresh context.
- Reporting a successful launch as completed work skips outcome verification.
