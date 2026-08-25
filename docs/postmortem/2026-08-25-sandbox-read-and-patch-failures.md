# Sandbox Read and Patch Failures

- Symptom: The initial read-only inspection and the standard patch helper both failed before performing their work with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; the first elevated recovery patch was also rejected as malformed.
- Impact: Required instruction, feedback, lesson, and Git-status checks were delayed, and no repository file changed until a corrected recovery patch was prepared.
- Evidence: The restricted read and patch attempts returned the sandbox network-namespace error. The malformed `git apply` attempt returned `error: corrupt patch at line 7` without applying changes.
- Root cause: The restricted sandbox could not create its required loopback network namespace. The first fallback patch omitted sufficient hunk context.
- Resolution: Retried read-only inspection through the approved elevated path, then validated exact zero-context `git apply` hunks before applying the narrow documentation recovery.
- Verification: `bash tests/test_fn_progress.sh`, `fish -n dot_config/fish/functions/fn-progress.fish`, `git diff --check`, and the README gate all passed after recovery.
- Current status: Resolved; the restricted patch helper failed again during follow-up, but no file changed until the validated elevated recovery path succeeded.
- Follow-up: Use the narrow elevated fallback only when the restricted sandbox reproduces this limitation, and validate patch hunk counts before invoking `git apply`.
- Additional symptom: The required `refresh-config` command was not found in the elevated execution PATH, so the tracked configuration deployment step exited before running.
- Additional impact: The source and regression test were initially updated and verified, but the installed Fish helper was not refreshed by the failed command.
- Additional evidence: `command -v refresh-config && refresh-config` exited 1 with no command path or refresh output.
- Additional resolution: The repository helper was sourced through Fish and invoked with `fish -ic 'refresh-config'`; it printed `REFRESH COMPLETE` and exited 0.
- Additional verification: The installed helper now prints `✅ Fortnite C7S4 is 8% complete!` without asterisks, and the focused regression, Fish syntax, and diff checks pass.
- Additional status: Resolved.
