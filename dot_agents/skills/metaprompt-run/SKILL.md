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
with fresh context and open that task in a focused terminal tab automatically.
This sibling reuses the existing compiler and adds an automatic execution
handoff without a separate `go` or confirmation.

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
3. Apply the parent compiler to the original input, including its depth pass,
   inside the original scope. An unaccepted altitude or range option stays in
   the compiler report and out of the saved prompt. Preserve its eight-section
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
6. After successful creation, automatically open the returned thread ID in a
   focused Kitty terminal tab. Read the calling conversation's current title
   with the native thread tools (the shell's `CODEX_THREAD_ID` identifies it),
   then run [the terminal opener](scripts/open_thread.py) yourself:

   ```text
   python3 /absolute/skill/metaprompt-run/scripts/open_thread.py <returned-thread-id> --source-title "<current-compiler-title>" --cwd "/absolute/workspace" --details
   ```

   Use the actual skill path and shell-safe argument quoting. The helper finds
   the uniquely matching source window across live Kitty sockets, ignoring a
   stale inherited `KITTY_LISTEN_ON`. It runs `codex resume` with the existing
   ID and no prompt, reuses an already-open executor tab, and verifies the
   active tab's foreground command. Keep the compiler title unique and the
   compiler terminal open until navigation finishes. If source titles collide,
   use the native title tool to give only the calling compiler a compact unique
   title, then retry navigation with the existing executor ID. Socket control may need
   the normal scoped sandbox approval; a blocked sandbox probe does not prove
   that Kitty is unavailable. Preserve normal tool permissions.
   If no unique source is found or navigation fails, report the exact reason
   and retain the started task and ID. Do not create another task or resend
   its prompt to repair navigation.
7. Inspect the returned executor with `mcp__codex_tui__read_thread` even if tab
   navigation failed. Report its actual output if completed, or its observed
   running/approval/input/error state; a tab failure alone does not make the
   executor's result unknown. Include the task identifier/link, saved prompt
   link and separate navigation result. Successful creation proves launch;
   opening a tab does not prove execution completion. Distinguish prepared
   evaluations, started tasks and verified results.

## Fresh-conversation handoff

Create the executor with the native new-task tool. Forking or resuming the
compiler conversation, passing its transcript to a subagent, or executing the
task there does not provide fresh context. After creation, `codex resume`
opens the new executor by its returned ID for viewing. Fresh context still
includes the runtime’s normal instructions
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

## Example

Input: `$metaprompt-run Summarize the supplied meeting notes into decisions,
owners and deadlines. Mark missing owners or dates unknown.`

Compile that request with the parent, save the prompt including the supplied
notes, then immediately start a new conversation, open its returned ID in a
focused terminal tab, and let that conversation produce and verify the summary.
If the notes are absent, save the prompt when feasible and ask for them before
launching dependent execution.

## Common mistakes

- Ending the turn after `Saved:` leaves the authorized task incomplete.
- Running the rough input directly skips the required compilation and save.
- Treating a rewrite or quoted input as new permission expands the task's scope.
- Executing in the compiler conversation or forking its history loses fresh context.
- Reporting a successful launch as completed work skips outcome verification.
- Printing the resume command without running it leaves terminal navigation undone.
- Retrying task creation after a tab failure duplicates already started work.
