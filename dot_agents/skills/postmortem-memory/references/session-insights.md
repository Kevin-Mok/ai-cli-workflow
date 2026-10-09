# Session insight evidence

Use these findings when maintaining private session summaries and deterministic commit evidence. Reproduce the observed boundary, apply the narrow remedy and preserve uncertainty where evidence remains incomplete.

## local-session-insights-command-effects

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: A nominally read-only recorded Git command with an output option creates uncommitted work but reports all committed.; Executable Git helpers or hooks can create effects not represented by recorded patch evidence.
- Applicability: Deterministic session-to-commit attribution from successful tool events in shared repositories.
- Diagnostic checks: Reproduce git show --output in a temporary repository after a verified owned commit. Exercise executable post-commit hooks and filters actually applied by file attributes.
- Remedy: Validate recorded command arguments with conservative allowlists and account for applicable executable helpers; unsupported effects retain unknown status while preserving verified commit counts.
- Verification evidence: Eighteen new RED cases preceded the guard fix; 58 commit-evidence tests and final 334-test suite passed.
- Limitations: Arbitrary shell writes, dynamic wrappers and unverifiable historical ownership remain unknown; this is code verification, not live activation.
- Sources:
  - [2026-10-08-ctp-insights-verification.md](/home/example/coding/track-codex-sessions/.worktrees/ctp-session-insights/docs/postmortem/2026-10-08-ctp-insights-verification.md) (SHA-256 `ddcf72b87847944658ae57777a6dc1957c3ae26ecb57de97e5e4116b1230d86b`; reviewed in [sources.json](../sources.json)).

## local-bounded-json-nesting

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Byte-bounded deeply nested JSON raises RecursionError and breaks discovery for unrelated valid sessions.
- Applicability: Local bounded JSONL transcript discovery and dialogue extraction.
- Diagnostic checks: Place a deeply nested unrelated metadata header beside a valid transcript. Append a nested malformed dialogue record and require partial usable evidence.
- Remedy: Catch RecursionError at both discovery and per-record parsing boundaries; skip invalid headers and mark incomplete dialogue partial without copying raw input to diagnostics.
- Verification evidence: Both nested-header and nested-record tests failed before the fix, then passed; final 334-test suite passed.
- Limitations: Bounds protect memory and known parser failures but do not establish support for every historical transcript schema.
- Sources:
  - [2026-10-08-ctp-insights-verification.md](/home/example/coding/track-codex-sessions/.worktrees/ctp-session-insights/docs/postmortem/2026-10-08-ctp-insights-verification.md) (SHA-256 `ddcf72b87847944658ae57777a6dc1957c3ae26ecb57de97e5e4116b1230d86b`; reviewed in [sources.json](../sources.json)).

## local-implicit-model-cache-identity

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Unchanged summaries regenerate when effective Codex model is implicit and local configuration has no explicit model.; No-summaries marks a freshly generated unchanged default-model entry stale.
- Applicability: Private derived-summary caches using an existing configured Codex CLI/provider.
- Diagnostic checks: Use unchanged dialogue and an empty model configuration for two consecutive generations. Change the model-selection configuration and require invalidation without an arbitrary-model wildcard.
- Remedy: Cache a validated model-selection fingerprint of configuration and CLI identity alongside the effective model; reuse only matching evidence and selection, and label model/configuration drift stale.
- Verification evidence: Consecutive default-model runs reproduced two generations before the fix; reuse/invalidation regression and final 334-test suite passed.
- Limitations: Unreadable configuration cannot establish freshness; this code evidence does not establish compatibility with future CLI isolation schemas.
- Sources:
  - [2026-10-08-ctp-insights-verification.md](/home/example/coding/track-codex-sessions/.worktrees/ctp-session-insights/docs/postmortem/2026-10-08-ctp-insights-verification.md) (SHA-256 `ddcf72b87847944658ae57777a6dc1957c3ae26ecb57de97e5e4116b1230d86b`; reviewed in [sources.json](../sources.json)).
