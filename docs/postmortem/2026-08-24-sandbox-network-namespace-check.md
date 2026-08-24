# Sandbox network-namespace check failure

- Symptom: The initial read-only repository inspection command failed before producing command output with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Impact: Repository status and the `fnprogress` definition were not inspected in that attempt.
- Evidence: The command exited during sandbox setup.
- Root cause: The sandbox could not create its loopback network namespace; the elevated retry allowed read-only inspection and the targeted edit.
- Resolution: The requested function change was applied and verified; the broad refresh workflow was not run because it could overwrite unrelated dirty configuration.
- Status: Complete for the requested source change.
- Follow-up: Apply the tracked function through the normal configuration workflow only after reviewing the unrelated dirty state or explicitly approving the broad refresh.
