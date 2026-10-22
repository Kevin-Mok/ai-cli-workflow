# sofss missing after shortcut refresh

Investigate why a successful configuration refresh omitted the newly added fish shortcut, then verify the deployed abbreviation before delivery.

## Symptom and impact

`refresh-config` exited 0 and reported REFRESH COMPLETE, but the generated `~/.config/fish/key_abbr.fish` did not contain `sofss`. The screensaver timer update succeeded; the interactive shortcut was not yet usable.

## Evidence and status

- The fish-alias helper added `sofss` to `aliases/key_aliases.tmpl` with zero conflicts.
- Refresh completed successfully; generated abbreviation file was rewritten.
- A focused `rg -n sofss` against the generated file returned no match.
- Status: resolved; deployed fish abbreviation verified, no blackout command executed.

## Lookup and next steps

Read tracked postmortem-memory skill before remediation. Search: `fish abbreviations refresh shortcut missing template`. Compare tracked template, rendered source and generator inputs; then update the correct source/deployment path and verify the focused fish expansion.

The search returned general path discovery and refresh ownership guidance. The launcher-mode drift reference recommends inspecting exact managed/ignored targets; applicable as a diagnostic, but its mode-only remedy did not apply here. The earlier `2026-10-08-cto-alias-sandbox-startup.md` documents the narrow live-alias append precedent.

## Cause, resolution and verification

The generator reads `~/aliases/key_aliases`, which chezmoi reports as ignored/unmanaged. Editing the tracked template and running a successful refresh therefore did not update that live input. Added only the exact `sofss` row to the live source after checking conflicts, preserving existing mappings. Repeated refresh completed with exit 0; focused `abbr --show` output now includes the expected sofss expansion. `fish -n` on the generated file passed. Daily timer inspection shows the next local 10 AM trigger and deployed display-on/idle-start steps.

No new reusable learning: narrow live alias reconciliation and exact managed/ignored-target inspection already have precedent. Register this report as a reviewed no-new-learning decision. Physical display blackout and the overnight timer are intentionally left for manual acceptance.
