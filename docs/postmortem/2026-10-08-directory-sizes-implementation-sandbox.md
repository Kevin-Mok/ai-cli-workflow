# Directory-size implementation sandbox startup

The default runner failed before task commands executed. Approved scoped execution allows the implementation to continue; host sandbox repair stays outside this task.

- Symptom/evidence: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; initial read/status command exited 1 without shell output.
- Impact: No repository files changed; task reads delayed.
- Lookup: `bwrap loopback Failed RTM_NEWADDR` matched `local-sandbox-loopback-approved-route` (verified_workaround). Same pre-execution error establishes applicability.
- Resolution/verification: Approved require_escalated repository reads and initial git status exited 0. This bypass is verified, while normal sandbox startup remains unresolved.
- Root cause: Wrapper loopback initialization rejected; underlying host policy not investigated.
- Follow-up: Use scoped approved execution, preserve existing dirty files, leave host repair separate.
- Learning: No new reusable guidance; existing local sandbox workaround applies.

- Additional tool failure: Native title update later failed with HTTP transport error to the local MCP endpoint. Initial title was set successfully. Keep the existing title while the tool is unavailable; no host changes or retries made. This affects naming only.
