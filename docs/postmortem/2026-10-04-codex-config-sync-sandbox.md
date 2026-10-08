# Codex config sync shell startup failure

The config sync encountered a sandbox startup failure. This records the evidence and the execution workaround.

- Symptom: the first read-only shell invocation exited 1 before executing commands.
- Evidence: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Impact: initial inspection was delayed; no files were changed by the failed invocation.
- Root cause: the environment denied bubblewrap loopback setup.
- Resolution: use approved elevated execution for this session.
- Verification: the elevated inspection exited 0 and read repository status and instructions successfully.
- Status: execution unblocked; sandbox restriction remains external to the repository.
- Follow-up verification: byte comparison and TOML parsing confirmed the repo config matches the live file and retains `tui.theme = "one-half-light"`.
