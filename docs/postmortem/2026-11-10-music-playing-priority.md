# Music block hides playing mpv behind paused Spotify

The music block should show active playback. Investigate its selection rule, reproduce the conflict, then verify the corrected selection and displayed-player controls.

## Symptom and impact
User reports Spotify paused while mpv is open, but music block retains Spotify. Source `select_player` returns immediately for Spotify regardless of playback state; existing tests and docs explicitly encode that rule.

## Lookup and evidence
Query `i3blocks music spotify paused mpv player` matched `local-displayed-owner-control-binding` and `local-browser-source-process-identity`. Retain owner-bound controls and dedicated browser identity. Prior preference for playing tracks applies; unconditional Spotify return overrides it.

## Status and next steps
Selection updated after RED: 46 tests produced five expected failures. Live D-Bus inspection confirmed one playing mpv among four instances and paused Spotify; original selection returned Spotify. GREEN: 46 focused and 79 i3blocks regression tests pass (both exit 0).

## Environment observations
`playerctl` is unavailable in this execution environment; helper uses busctl directly, so no installation is needed. A guessed refresh script path was absent; locate the existing fish function before activation. These are lookup limitations, not evidence about live media state. Sandboxed busctl could not connect (Operation not permitted); approved elevated read-only inspection succeeded.

Refresh attempt exited 1 before apply completed; private log `/tmp/refresh-config.xJyXjVN1.log`. Cause: pre-existing `dot_config/mimeapps.list` and `dot_config/private_mimeapps.list` map to the same destination. Left both untouched. Installed only the reviewed helper with `install -m 755`; source/live cmp exit 0. Installed execution returned a playing mpv filename in both text fields, color `#d4cfd2`, exit 0.

## Resolution and verification
Spotify returns early only when Playing. Otherwise all eligible candidates are ranked by playback state, Spotify tie priority, then existing source/name order. Invalid Spotify no longer hides a usable player. Dedicated browser identity and displayed-owner click checks remain intact.

Observed live deployment: installed helper emits playing mpv while Spotify was paused; no playback controls were sent. Fixture tests cover controls, paused ties, browser playback and unavailable metadata. Physical bar appearance and human clicks were not observed. Full refresh remains blocked by the unrelated MIME conflict.

## Learning decision
No new reusable finding: `local-displayed-owner-control-binding` already prescribes playing-first selection and owner-bound controls. This incident reapplies that existing rule; the narrowly scoped change adds regression coverage for the subsequently introduced unconditional Spotify priority. Environment-only failures are covered by existing execution/ownership guidance. Register this reviewed report with this explicit no-new-learning decision.
