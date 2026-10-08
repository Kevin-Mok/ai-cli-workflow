# Directory-size verification environment findings

Focused checks verify this task, while a broader incident-memory check has unrelated corpus gaps. This record also preserves incidental review tool failures.

- Symptom: `python3 -B tests/test_postmortem_memory.py` ran 26 tests; `WorkflowTest.test_actual_ledger_reference_status_and_coverage` failed because whole-corpus aliases under existing .worktrees were unregistered. The other 25 passed. Output was large; exact named failure and coverage reason were inspected.
- Impact: Cannot claim the broader incident corpus is clean. This task's targeted report checks pass; no unrelated ledger aliases are adopted or edited.
- Lookup: `unregistered aliases whole corpus coverage` searched reviewed knowledge; targeted checks versus whole-corpus scope are defined in references/workflow.md. Coverage gaps remain outside this task.
- Status/root cause: Existing whole-corpus coverage gaps; no implementation remedy attempted. Use targeted checks to establish only new task-report coverage and disclose broad test failure.
- Additional incidental review failure: Read-only reviewer guessed nonexistent scripts/executable_benchmark-directory-sizes; cat returned 1. Actual runner is tests/scripts/directory_sizes_benchmark.py. Correct path supplied, no file writes or source scans occurred. Follow-up: use supplied observed paths.
- Review finding: benchmark Ctrl-C cleanup only terminated children on timeout, risking orphaned separate-session Dust. Defining SIGALRM/KeyboardInterrupt test exercises this intentional RED path, with explicit cleanup of fixture processes. Fix always TERMs running processes in finally and protects startup with cleanup scope. Final nine-test contract run passes, including interruption reaping; no real-directory probe repeated.
- Verification/follow-up: Final focused results and targeted ledger checks recorded in plan. Corpus registration and native title MCP availability remain external limitations.
