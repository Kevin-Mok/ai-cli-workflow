# Fish home-path task sandbox startup

The default runner failed before any shell command executed. The approved scoped runner allowed the shortcut task to continue.

## Evidence and impact

Initial status/skill read exited 1: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. No repository mutation occurred. Scoped require_escalated reads then exited 0.

## Lookup and resolution

Query: `bwrap loopback Failed RTM_NEWADDR`. Matching `local-sandbox-loopback-approved-route` is applicable to this exact pre-execution failure. Reviewed execution-environments guidance confirms the alternate route is a verified workaround, not a host repair. Root cause is runner loopback initialization denied by host policy; the deeper host restriction is uninvestigated.

## Status and follow-up

Verified workaround: approved scoped execution completes. Continue only the requested shortcut/helper edits and verification. Default sandbox repair remains outside scope. No new learning beyond the existing finding.

## Helper discovery correction

An inspection tried `dot_config/fish/functions/snapshot-codex-config.fish` and exited 1 because that file does not exist. No mutation occurred. Discover the snapshot executable with `rg --files` rather than assuming it is a fish function. Existing helper-discovery lessons apply; no new reusable learning.

## Normalization fixture verification

First GREEN run: normalization assertions passed, but three section assertions failed (sys versus cdn). The existing heuristic compares common prefixes up to their last slash, so fixture `cn ~/coding` ties with sys paths; it lacks the trailing slash needed for a stronger directory-prefix match. Live tcs preview correctly selected cdn using richer actual templates. Keep the normalization regression focused using the existing explicit section routing aid instead of changing unrelated section heuristics. Expected normalization assertions and no-op checks remain intact.
