# Private digest command sandbox startup failure

Repository inspection could not start in the command sandbox. Approved commands bypass the unavailable sandbox so implementation can continue.

- Symptom: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` before command execution.
- Impact: initial read-only inspection and delegated inspections did not execute; no repository mutations occurred.
- Lookup: searched `bwrap loopback Failed RTM_NEWADDR`; execution-environments guidance documents the same pre-command environment boundary. Applicable because no command output or exit from the intended program exists.
- Cause: sandbox network namespace setup lacks permission; underlying environment issue remains.
- Resolution/status: verified workaround using require_escalated commands; git status and instruction reads exited 0.
- Verification: approved inspection returned repository status and source text. This does not prove normal sandbox repair.
- Next steps: continue authorized commands with approval review; do not retry default sandbox or infer application failures.
- Learning: no new learning; existing sandbox-startup guidance applies.
