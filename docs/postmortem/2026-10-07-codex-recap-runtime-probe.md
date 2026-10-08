# Codex recap runtime probe rejected quoted override keys

Record the failed local configuration probe, the corrected override syntax, and
the verified isolation boundaries used by recent-session recap generation.

## Symptom and impact

On 2026-10-07 a no-inference `codex app-server --strict-config` probe exited 1
with `invalid transport` in `mcp_servers."openaiDeveloperDocs"`. The diagnostic
constructed a dotted CLI override by JSON-quoting its server-name component.
No model inference, source-session mutation, hook invocation, or MCP launch
occurred. Implementation was delayed briefly.

A follow-up coordination message used an unverified agent path
`/root/recent_picker` and returned `live agent path ... not found`. Listing the
active agents identified `/root/picker_contract`; resending there succeeded.
This had no file or model effect.

During an intentional RED test for parent-session environment removal, a
unittest `assertNotIn` failure unexpectedly rendered the entire inherited
environment into tool output, including secret-valued variables. Values were
not copied into files, the ledger, or this report, and no external endpoint was
involved. The test fixture now clears its environment to synthetic fields and
uses boolean membership assertions that do not render mappings on failure.
The parent agent was informed immediately; the diagnostic transcript exposure
cannot be undone by editing repository files.

## Prior-knowledge lookup

Read the tracked `postmortem-memory` skill and searched `invalid transport
dotted key mcp_servers`. No exact quoted-key incident matched. The existing
`local-effective-tool-catalog-carriers` finding was applicable to the subsequent
isolation probe: inspect both top-level tools and developer
`input.additional_tools`, and keep the native Code Mode host disabled. Read
its API-contract reference and existing benchmark runtime before that probe.
For the environment disclosure, searched `environment secrets assertion
output`; no exact prior finding covered unittest rendering an inherited
environment. Other environment-fixture findings did not establish a remedy for
credential-bearing assertion representations.

## Cause and resolution

The installed Codex CLI 0.160.1 treats quotes in a `-c` dotted key segment as
literal name characters, producing an incomplete second MCP definition.
Unquoted ordinary server names worked. Runtime construction must validate that
MCP names are representable by the CLI dotted-key syntax and fail closed when
they are not. Do not confuse shell argument quoting with quoting inside the
CLI key string.

Separately, `-c mcp_servers={}` was experimentally confirmed to retain the
original servers through configuration merging. Disable each effective server
explicitly and check the resulting effective configuration.

## Verification and current status

Corrected no-inference app-server probe exited 0. `config/read` returned
read-only sandbox, approval `never`, web disabled, the requested tool/integration
features false, and all configured MCP servers disabled. `hooks/list` returned
no hooks, warnings or errors; `configRequirements/read` returned null. MCP
inventory retained disabled server names with empty tools/resources and null
runtime status. The existing bubblewrap user-namespace warning remained and
does not constitute proof of working shell sandbox execution.

A localhost-only synthetic provider received one deliberately rejected request
and made zero upstream requests. The effective catalog had no shell, web or
MCP tools. `input.additional_tools` still advertised a generic Code Mode
wrapper; Codex reported that its disabled host would fail closed. That wrapper
must not be described as a functional execution capability or as an empty
tool catalog.

The first implementation passed 11 synthetic defining tests, but its actual
installed-CLI preflight then failed closed with `Codex isolation probe closed
before verification`. No inference was attempted. Startup diagnostics showed
that `model_instructions_file=/dev/null` is rejected because Codex requires a
regular file. A private regular file fixed startup; defining tests then passed
13 checks, including descendant cancellation and final cwd verification.

The next installed preflight stopped at `tools.update_plan.enabled`: the
`config/read` response projects its typed `tools` object to `web_search` only.
The full highest-priority `sessionFlags` layer contains the accepted
`update_plan.enabled=false` setting. Verification must use that raw layer
evidence for this one projected field while continuing to require direct
effective values for shell, web, hooks, MCP and all other isolation settings.

The projected-field exception is now narrowly implemented for
`tools.update_plan.enabled`; all security controls still require type-exact
effective values. Both preparation and the final generation directory passed
actual installed-CLI config/hook/MCP verification with model `gpt-6-astra`.
The final instruction file is private and read-only. The known Graphiti launcher
is skipped without executing its sidecar, and parent session/thread/originator
environment identifiers are removed.

Final subtask verification:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p
  'test_codex_search_runtime.py'`: 17 tests passed, exit 0. Defining RED cases
  were observed before runtime implementation and each additional correction.
- The installed Pyright checker with its explicit bundled typeshed path:
  zero errors, warnings or informational findings, exit 0.
- Scoped `git diff --check`: exit 0.
- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/codex-recap-catalog-check.py`: exit 0.
  This retained temporary harness uses only synthetic config, a localhost
  provider and an enabled MCP startup canary. First config-only discovery,
  later verified probes and actual ephemeral CLI execution never started the
  canary. Exactly one deliberately rejected local request reached the sink;
  zero upstream requests occurred. The catalog contains only the generic
  wrappers listed above, with their host disabled and reported fail-closed.

Status: diagnostic/runtime problems resolved and verified in the stated scope.
Secret-valued environment output was confined to the diagnostic transcript;
the fixture now uses synthetic environment values and safe assertion messages.
The user was informed by the parent. Credential rotation was not attempted or
verified. No real model generation was used by this subtask.

## Follow-up

- Keep tests covering model resolution, effective isolation, unsupported MCP
  names, configuration drift, wrapper side effects and descendant cancellation.
- Keep the plan and operator docs accurate about the disabled Code Mode host,
  fail-closed isolation checks and supported installed CLI version.
- Use synthetic environments for tests whose failure messages may display
  values. Boolean membership assertions avoid printing a complete mapping.
