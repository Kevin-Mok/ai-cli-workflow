# Commit skill update: shell startup failure

- Symptom: initial status and skill reads failed with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` (exit 1).
- Impact: no repository changes occurred; inspection required escalation.
- Evidence: both initial shell calls failed before execution; escalated `git status --short` succeeded.
- Root cause: the environment denied bubblewrap network namespace setup.
- Resolution: use approved escalated shell calls for this task. The underlying sandbox remains unavailable.
- Verification: repository status and skill source reads succeeded with exit 0 under escalation.
- Follow-up: retry ordinary sandbox execution in a later session; preserve the existing dirty tree.
- Discovery note: a guessed `snapshot-codex-config.fish` path did not exist; locate its tracked entrypoint with `rg --files` before reading it.
