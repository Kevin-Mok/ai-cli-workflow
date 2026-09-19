# Sandbox loopback setup blocked repository inspection

- **Date:** 2026-09-18
- **Symptom:** Initial read-only shell commands failed before execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- **Impact:** Repository guidance and worktree state could not be inspected through the normal shell tool.
- **Evidence:** Both the initial instruction read and `git status --short` returned the same sandbox error with exit status 0 from the wrapper but no command output.
- **Status:** Resolved; the restricted shell and patch helper both reproduced the same setup failure, while approved elevated inspection succeeded.
- **Resolution:** Used the narrowly scoped elevated fallback after validating exact file context; no unrelated dirty files were modified.
- **Verification:** `bash tests/test_fn_progress.sh`, `fish --no-execute dot_config/fish/functions/fn-progress.fish`, `git diff --check`, live `fn-progress 75`, and `refresh-config` all completed successfully.
- **Follow-up:** Keep the elevated fallback limited to this repository when sandbox loopback setup fails again.
