# Benchmark trial infrastructure failure

Date: 2026-10-03. Trials stop on infrastructure errors; retain all attempts.

Final status: resolved before held-out execution. The parent independently
verified the synthetic actual-CLI read/write probe and all 45 pre-run tests.
The repaired development compiler read references successfully and then hit
its declared episode limit. All 14 held-out pairs subsequently ran with zero
infrastructure errors; the ledger finished at exactly 50 requests. Four
development infrastructure attempts remain archived, including the three-call
approval failure. No failed request was refunded or hidden. The safer direct
MCP implementation resolved the earlier automatic-review rejection without
enabling native host execution.

- Trial `dev-extract-inventory--raw--r0`: Host instructions or installed skill context detected. Impact: trial unscored; 1/50 total requests reserved. Evidence retained in the run JSON. Status: investigation required before further model execution.
- Investigation: the local proxy also rejected metadata `/models` GETs with a
  sticky error, although Codex can fall back to its installed catalog. Changed
  these GETs to a nonsticky local404 (no remote request or fabricated catalog).
  Added tests for marker-only guard diagnostics to identify the contaminated
  context without saving host instruction text. No-spend probe pending; source
  of the matched marker is not yet established.
- Root cause established by zero-permit probe: host global canonical AGENTS
  is injected independently of the project-doc byte limit. Current Codex packs
  its `# AGENTS.md instructions` fragment (no directory for global instructions)
  and the environment fragment in one user message. The old filter assumed one
  content part and a directory suffix. Official
  `core/src/context/user_instructions.rs` confirms the markers and optional
  directory.
- Resolution: consistently remove only a user-role content fragment with the
  exact AGENTS wrapper, canonical heading, and closing tag; preserve all other
  content parts and the original candidate/task prompt. Record removal count,
  retain guards for any remaining host markers, and record this harness adaptation.
- Verification: 14 local boundary tests pass; final zero-permit Codex probe
  reached the budget gate with `call_count=0`, removed exactly one host fragment,
  and reported `budget_exhausted` rather than context contamination. No upstream
  request occurred in these probes. Parent must refreeze before development
  trials. Installed runtime source provenance is captured separately.
- Fixture catalog failure: a subsequent zero-permit exact MCP probe established
  an empty outbound catalog and the CLI diagnostic `Code Mode is unavailable
  because code-mode host is disabled`. Explicitly disabling Code Mode feature
  flags did not restore tools because model metadata selects the tool mode.
  A top-level `code_mode` config preflight failed strict validation; this unused
  field was removed. A proposed enabling patch was rejected by automatic approval
  review for risk of exposing native host capabilities through unverified namespace
  restrictions; no enabling patch or probe executed. A safer direct-only setting
  with the host still disabled failed config parsing and was reverted. No upstream
  inference occurred. Status: blocked pending verified runtime isolation/approval.
- Final root cause: Responses Lite carries real tool schemas in a developer
  `input.additional_tools.tools` item; the top-level `tools` array is empty.
  The original guard checked only that empty array. Correct dotted direct-only
  MCP configuration exposes `mcp__benchmark` in this additional catalog with the
  Code Mode host still disabled. The earlier direct-only probe used invalid
  JSON-object-as-TOML serialization, so it did not test this supported setting.
- Final resolution: leave the host disabled, use dotted
  `features.code_mode.direct_only_tool_namespaces=["mcp__benchmark"]`, filter
  both known catalog carriers to fixture MCP functions, remove native namespaces,
  reject unknown carriers, and count the combined effective catalog before any
  permit. Buffered response guards continue to prevent native actions reaching
  the CLI. Parent refreezes before inference; diagnosis does not consume quota.
- Trial `dev-extract-inventory--raw--r0`: Fixture MCP tool catalog missing; no inference sent. Impact: trial unscored; 1/50 total requests reserved. Evidence retained in the run JSON. Status: investigation required before further model execution.
- Trial `dev-guide-summary--metaprompt--r0`: Host instructions or installed skill context detected: /home/example/.agents/skills/. Impact: trial unscored; 2/50 total requests reserved. Evidence retained in the run JSON. Status: investigation required before further model execution.

### Installed skill auto-injection discovered during development

The maintained compiler development trial failed before forwarding an inference:
its candidate text mentioned `$metaprompt-alxve`, and Codex 0.160.0 appended a
separate installed-skill user message despite `skip_host_skill_discovery=true`
and `skills.include_instructions=false`. An always-false-permit probe with an
upstream function that raises verified the framing without any upstream calls:
`message` / `user` / `input_text`, `<skill>` envelope, `<name>metaprompt-alxve</name>`,
and `<path>/home/example/.agents/skills/metaprompt-alxve/SKILL.md</path>`.
Only wrapper structure and metadata were inspected; the live skill body was not
saved or printed.

The explicitly disclosed host-context adaptation now removes a complete,
recognized installed-root `<skill>` envelope only from a separate user input
fragment. Exact supplied candidate prompt text, scratch skill paths, and tool
outputs remain unchanged. Unknown framing remains subject to the fail-closed
host guard. Removal records skill names and count, never instruction bodies.
This applies equally to candidate and baseline calls. `code_mode_host=false`
and the MCP-only tool surface remain unchanged.

Verification: the exact rejected compiler prompt, staged with its saved fixture
files and fixture MCP, passed context and tool-catalog guards and stopped at the
intentionally closed budget gate (`budget_exhausted`, `call_count=0`). The local
injected boundary suite passed 21 tests in 14.574 seconds. Python compilation
and `git diff --check` exited zero. No additional benchmark inference was made
by this diagnosis; the parent ledger remained at two outbound attempts.

### Fixture MCP approval rejection during development

The subsequent maintained compiler development attempt sent three inference
requests, but its read_file and write_file actions were rejected by Codex with
`MCP tool call requires approval, but approval policy is never`. The fixture
tool trace was empty: no fixture reads or writes ran. This is an infrastructure
failure rather than evidence of candidate quality. The parent ledger records
five outbound attempts overall; held-out evaluation has not started. Diagnosis
will use injected upstream responses only and retain the MCP three-tool
allowlist and disabled code-mode host. Runtime must recognize this failure so
the parent can retry after a narrowly scoped fixture-tool approval fix.

Resolution: official `codex-rs/core/src/mcp_tool_call.rs` matches `Auto` to
annotation-based approval (unknown annotations require approval), while
`Approve` requires no approval. The official config schema supports per-tool
`mcp_servers.<server>.tools.<tool>.approval_mode`. The invocation now sets
`approve` only for benchmark `read_file`, `write_file`, and `list_files`, and
also sets that server's `enabled_tools` to exactly those three. Global
`approval_policy=never`, native tool filtering, and `code_mode_host=false` remain
in place. No installed or tracked host configuration was changed. Repeated
approval failure in a fixture function output blocks before the next permit;
completed CLI MCP approval errors are classified as infrastructure failures.

An actual installed-CLI integration probe used injected SSE responses and a
patched official upstream function, so it sent zero remote or model requests.
It successfully executed the restricted fixture MCP `read_file` and
`write_file`, verified the created scratch artifact, and returned `ok`. The
probe is reproducible with `/tmp/metaprompt-fake-mcp-probe.py` (three synthetic
transport turns, zero official upstream calls). Local boundary regressions
verify scoped settings, pre-spend approval failure detection, and storage-only
removal of `encrypted_content`; this opaque reasoning field is preserved in the
actual request sent to the transport, and omitted only from persisted evidence.
Sources: https://learn.chatgpt.com/docs/config-schema.json and
https://github.com/openai/codex/blob/main/codex-rs/core/src/mcp_tool_call.rs
(current official main, not an installed-source pin).
