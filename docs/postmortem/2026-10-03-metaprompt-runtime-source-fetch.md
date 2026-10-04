# Runtime audit public-source retrieval failure

- Date: 2026-10-03.
- Symptom: a read-only Python urllib request to the documented Codex config
  schema URL returned HTTP 404; subsequent raw GitHub source paths also returned
  404 through the web fetcher.
- Impact: runtime capability investigation was delayed. No benchmark model
  calls, credential reads, installed settings changes, or trial artifacts occurred.
- Evidence: urllib reported `HTTP Error 404: Not Found`; web fetches of legacy
  `core/src/tools/spec.rs` and `core/src/features.rs` reported 404.
- Root cause: the docs route redirects in the web reader but was unavailable to
  urllib, and source modules have moved from the guessed legacy paths.
- Resolution: read the official redirected schema through the web tool and
  inspect the official GitHub model-provider modules and locally generated
  CLI protocol schemas.
- Verification: installed CLI 0.160.0 generated app-server schemas successfully;
  official model-provider source and config schema were readable via web.
- Status: resolved. Use actual current source paths; do not infer runtime controls
  from stale config examples or simplified reachability diagnostics.
- A subsequent no-inference configuration preflight using `codex --strict-config
  features list` exited 1 because this installed CLI rejects `--strict-config`
  for the features command. No model calls occurred. Validate invocation fields
  against the official schema instead; the real exec retains strict validation.
- Further stale paths `core/src/context.rs` and
  `prompts/templates/agents/hierarchical.md` also returned404 during guard
  investigation. The actual current source is
  `core/src/context/user_instructions.rs`; no inference resulted from these
  documentation requests.

A later attempted lookup of `core/src/context/skill_instructions.rs` through
the GitHub web reader returned 404. This guessed path was not used as evidence
for skill filtering. Instead, an installed-CLI offline, always-false-permit probe
verified the exact separate user `<skill>` wrapper metadata; no upstream
inference or live instruction-body logging occurred.
