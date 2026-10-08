# Recent-session implementation shell startup failure

The shell wrapper failed before repository reads. Use the approved scoped execution route to implement the requested recent-session browser; sandbox repair remains separate.

- Date: 2026-10-07.
- Symptom: Both initial read-only commands exited 1 with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`, without command-body output.
- Impact: Context retrieval delayed; failed commands changed no files.
- Lookup: `bwrap loopback Failed RTM_NEWADDR` matched `local-sandbox-loopback-approved-route`, verified_workaround, in `references/execution-environments.md`. The identical pre-execution symptom establishes applicability; approved retrieval reads were prerequisites to lookup.
- Evidence: Scoped elevated repository status, prompt, source and skill reads returned exit 0. Initial dirty status was captured before the first successful write and saved privately in `/tmp/codex-recent-initial/status.txt`.
- Root cause: Wrapper loopback setup is denied; underlying host policy was not investigated.
- Resolution/current status: Approved scoped execution works. Default sandbox startup remains unresolved.
- Verification: Required repository guidance and existing search implementation are readable with the scoped route, exit 0.
- Follow-up: Continue authorized implementation and verification without changing host security policy. Preserve pre-existing dirty files and do not commit or push.
- Learning: No new reusable lesson beyond `local-sandbox-loopback-approved-route`; this is another verified workaround instance, not a host fix. Register the reviewed hash with an explicit no-new-learning decision and run the targeted check.
