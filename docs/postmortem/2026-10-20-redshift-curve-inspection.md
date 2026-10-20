# Redshift curve inspection path errors

Record two unsuccessful optional file reads while locating the refresh helper. Use the discovered fish function and preserve the existing live i3 config.

## Symptom and impact

An rg query included nonexistent scripts/executable_refresh-config and a later sed read guessed scripts/executable_refresh-config-safe. Both emitted missing-file diagnostics; neither changed files. The actual helper is dot_config/fish/functions/refresh-config.fish.

## Diagnosis and lookup

Query: missing guessed file path read. The reviewed local-discover-paths-before-reads finding explicitly covers refresh-config being a Fish function. Inspection confirmed the tracked and installed function paths. Root cause: guessed executable names rather than discovered paths.

## Resolution and verification

Read the real function and ran fish -c refresh-config with scoped desktop permissions. It exited 0 and printed REFRESH COMPLETE. No retry of guessed paths. Source checker and six controller regression tests pass after preset changes. Live i3 still contains old modifier bindings; user clarification is pending before activation.

## Learning and follow-up

No new learning: local-discover-paths-before-reads already covers this exact error and remedy. Do not infer that successful refresh activates an intentionally unmanaged i3 config. Complete only scoped live binding changes after resolving modifier choice.

## Scoped activation guard

The first activation attempt exited 1 before writing: the expected old Super+1 workspace line was absent. A guard prevented overwriting live changes; inspect actual bindings before adapting the scoped patch. No reload occurred.

Resolved activation: inspection showed Super-only new temperatures and workspace 11 on Super+F11 already installed after refresh. Adapted the guarded patch to that observed state. Candidate checker and i3 -C both exited 0 (existing wheel binding deprecation diagnostics). Applied only Redshift bindings, reloaded successfully, and live checker passed both modifier families. No new learning: the established preserve-current-config and re-inspect-before-retry guidance applies. Remaining limitation: physical key feel and visible curve smoothness require human observation.

Delivery inspection also queried an absent optional .githooks directory; the privacy gate script was found and read directly. No hook files were modified. Existing path-discovery learning applies; no new reusable finding.

A delivery test was accidentally launched from the sparse candidate directory, which contains no tests folder; unittest discovery exited 1. This was a verification working-directory error, not a controller failure. Re-run controller tests from the repository root. Existing path/context discovery learning applies.
