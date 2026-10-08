# Directory-size prompt sandbox startup failure

The default command runner failed before repository reads began. The approved scoped execution route permits prompt preparation; host sandbox repair remains separate.

- Date: 2026-10-08.
- Symptom: Initial command returned `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`, with no command-body output.
- Impact: Repository status and compiler reads were delayed; no files changed in the failed launch.
- Lookup: Query `bwrap loopback Failed RTM_NEWADDR` matched `local-sandbox-loopback-approved-route`, verified_workaround, in references/execution-environments.md. Identical startup error and absent shell output establish applicability. Permitted prerequisite reads were used to obtain the skill before lookup.
- Root cause: The wrapper could not initialize loopback; underlying host policy was not investigated.
- Resolution: Approved require_escalated source reads returned exit 0 and captured initial Git status before writes. The same route saved and read back the compiled prompt successfully.
- Verification: Exact prompt read-back matched the authored contents. Scoped commands ran successfully; default sandbox startup remains unresolved.
- Additional preparation failure: The handoff byte-count probe raised `ReferenceError: TextEncoder is not defined` in the functions JavaScript isolate before create_thread ran. The handoff is ASCII-only, so JavaScript string length equals its UTF-8 byte count; use that supported operation. No task was launched by the failed probe. This is an incidental runtime API availability assumption, not a task-execution failure.
- Fresh-task launch blocked: create_thread returned isError true with automatic approval rejection: it considered separate task creation and broad repository modifications/research/benchmarks/configuration work insufficiently authorized. No task started. Do not bypass the rejection by executing the compiled implementation in this conversation.
- Approval lookup: Query `create_thread approval rejected` produced no applicable reviewed finding among the top matches; rejection text itself governs. User has since supplied a benchmark directory, which authorizes that bounded read-only check but does not explicitly answer the pending launch approval.
- Follow-up evidence: The user-supplied reference directory was checked with a deliberate 20-second read-only baseline. Both du and sort produced zero output before intentional termination; no complete totals exist. The wrapper completed exit 0 and reaped both processes. This intentional timeout is not a new unexpected failure.
- Follow-up: Updated prompt saved with exact real-directory benchmark facts and verified by read-back; The user subsequently replied yes to explicitly approve fresh-task execution. create_thread succeeded and returned threadId `01a11c4a-fb7a-7813-8807-0101b356824f`; implementation and benchmark outcomes belong to that task and remain unverified here. Leave host sandbox repair outside this request.
- Learning: No new reusable guidance beyond local-sandbox-loopback-approved-route. Register this report with an explicit no-new-learning decision and run targeted coverage validation.
