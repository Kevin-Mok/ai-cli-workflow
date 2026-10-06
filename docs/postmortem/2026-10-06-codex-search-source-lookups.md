# Codex search public source lookup failures

This report records failed schema lookup guesses and the verified public-source fallback.

## Symptom and impact

Two guessed public raw GitHub paths returned HTTP 404 during schema research. A bounded incident lookup piped to head also printed BrokenPipeError after the consumer closed early. No conversation data was read and no application code ran.

## Lookup and applicability

The tracked incident lookup for `source 404` returned `local-current-source-retrieval`. Its guidance applies to moved public source paths: a failed guess is not evidence of missing capability. Read its reviewed reference section before further source retrieval. Avoid early-closing pipes for JSON lookup results.

## Cause, status, and resolution

The rollout index moved to codex-rs/rollout/src/session_index.rs. Public repository search identified that current path. Use primary source definitions and installed CLI help; do not guess session fields. Current public protocol definitions for SessionMeta, ResponseItem, and ContentItem were retrieved successfully. Schema verification completed from the current primary rollout wire definitions; no new reusable learning beyond the existing source-retrieval guidance.

## Verification and next steps

Record exact schema sources in the implementation plan and use only synthetic test content. Keep the prior privacy rejection respected by deriving structure from public code. This workaround does not guarantee older schema variants match current main.

Refresh preflight also tried unsupported `chezmoi diff --format=summary`; installed chezmoi rejected that flag without changes. Use installed command help and `chezmoi status` for a bounded inventory. This repeats existing source-retrieval guidance to verify command-specific flags.

Final verification: public SessionMeta/ResponseItem/ContentItem/EventMsg and history rollout wire format retrieved successfully before implementation; actual installed Codex 0.160.1 loaded the synthetic schema and displayed both saved messages. Supported chezmoi status/help and task-scoped refresh completed with exit 0. No new learning beyond current-source-retrieval and command-option verification.
