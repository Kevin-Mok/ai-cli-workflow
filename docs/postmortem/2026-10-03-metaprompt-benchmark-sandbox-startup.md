# Metaprompt benchmark sandbox startup failure

- Date: 2026-10-03
- Symptom: Four initial read-only shell commands exited 1 before execution:
  `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Impact: Benchmark setup reads were delayed. No candidate or fixture ran and
  none of those commands changed repository files.
- Evidence: Scoped elevated retries exited 0 for `git status --short`, the
  benchmark prompt, canonical instructions, and repository context.
- Root cause: The sandbox could not configure its loopback interface. The
  underlying host restriction is outside this benchmark's scope.
- Resolution: Use approved, scoped elevated shell operations for this task.
- Current status: Setup is unblocked; the ordinary sandbox remains unresolved.
- Verification: Initial Git status was captured before this first write.
- Next steps: Prepare isolated candidates and fixtures; treat runtime failures
  separately from measured task failures.
- Follow-up: Preserve all pre-existing dirty work. Keep this incident and the
  benchmark ExecPlan with their related implementation in any future commit.

## Fixture directory discovery

- During preparation, a fixture worker ran `ls benchmarks/metaprompt`; it
  exited 2 because the new benchmark directory did not yet exist.
- Impact: None beyond the discovery command; no fixture execution occurred.
- Root cause and resolution: New output directory, created as part of the
  authorized benchmark. Use existence checks for optional paths in future.
- Status: Preparation continues; creation will be verified with the suite.
