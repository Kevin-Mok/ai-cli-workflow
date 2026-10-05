# Metaprompt & Run shell sandbox startup failure

This record explains the shell startup failure encountered while creating
Metaprompt & Run, its effect on the task, and the execution workaround.

## Symptom and impact

- On 2026-10-04, the first five read-only shell commands exited 1 before
  executing, including the initial repository status check and skill reads.
- The shared error was `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- No requested command ran and no repository files changed in those attempts.

## Evidence and current status

- Retrying the same reads with `sandbox_permissions: require_escalated`
  succeeded with exit 0. The initial `git status --short` was captured before
  any repository write; its pre-existing changes are protected.
- Task work can continue through the reviewed execution path. The sandbox
  startup problem itself remains unresolved.

## Root cause and resolution

- The sandbox wrapper could not configure its loopback network interface.
  The evidence identifies the failing operation, not the host policy causing it.
- Approved execution outside the broken wrapper restored read access without
  changing repository or host security settings.

## Verification and next steps

- Read-only retry results: repository status, canonical instructions, ExecPlan
  contract, and the current metaprompt package all returned exit 0.
- Use the approved execution path for this task's checks and configuration
  refresh. The required refresh exited 0 with `REFRESH COMPLETE`; its complete
  log is `/tmp/refresh-config-20261004-180258-727117.log`. Installed runner bytes
  and parent reference were verified; live Codex/Git and protected dirty source
  bytes were preserved. Focused checks are recorded in the
  [task plan](../../plans/add-metaprompt-run.md).
- Follow up on host sandbox permissions separately; this skill change does
  not attempt to repair the sandbox.

## Related inspection failure

- A later read-only search exited 2 because it included the absent path
  `dot_config/fish/conf.d`. The actual refresh helper was still located under
  `dot_config/fish/functions/refresh-config.fish`; no files changed.
- Cause: a directory assumption in the inspection command. Continue using
  discovered paths only and inspect the exact helper before refresh.
- A helper read later exited 1 because it assumed a fish function path for
  `snapshot-codex-config`; discovery located the actual executable at
  `scripts/executable_snapshot-codex-config`. The refresh function itself
  was read successfully. Read the discovered executable before preflight.
