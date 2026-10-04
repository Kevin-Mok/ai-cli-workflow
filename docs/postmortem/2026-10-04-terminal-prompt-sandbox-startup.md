# Terminal prompt sandbox startup failure

- Date: 2026-10-04.
- Symptom: The first three read-only shell calls in the planning turn exited 1
  with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` before
  their requested commands ran.
- Impact: Repository and skill inspection was delayed. The failed calls made
  no repository changes. Plan mode prevented writing this incident note until
  the user authorized implementation in Default mode.
- Evidence: The same scoped reads succeeded through approved elevated
  execution, including `git status --short`, skill references, and terminal
  configuration. The Kitty version check returned `kitty 0.49.2` with exit 0.
- Root cause: Sandbox initialization could not configure its loopback
  interface. The underlying host restriction was not investigated in this task.
- Resolution: Continue the authorized document work through scoped approved
  execution. This is a workaround, not a sandbox repair.
- Current status: Prompt preparation is unblocked; sandbox startup remains
  unresolved. No terminal configuration change or installation is involved.
- Verification: Fresh read-only checks after the interruption exited 0,
  confirmed the pre-existing dirty state, and found all three intended new
  document paths absent before the first write. The approved prompt and its
  records were subsequently saved; artifact, reference, and whitespace checks
  exited 0. The failed sandbox calls did not prevent delivery.
- Next steps: Investigate the sandbox separately if ordinary execution remains
  unavailable. The workaround does not establish that sandbox startup is fixed.
- Follow-up: Preserve unrelated work. Keep this note and the
  [plan](../../plans/compile-terminal-workflow-prompt.md) with the
  [prompt](../../prompts/choose-terminal-workflow.md) in any future related
  commit. No commit or push is requested here.
