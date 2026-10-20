# Redshift notification ID replacement

Verify actual notification identity when an update must edit the existing popup. Dunst stacking alone replaces the displayed popup but allocates new IDs.

## Symptom and evidence

The user requested editing in place. A live probe with notify-send --print-id around a shared controller call returned IDs 106 and 108, failing the same-ID assertion. Temperature remained 3000 K. Earlier one-entry history evidence established replacement, not stable identity.

## Status and next steps

Resolved: controller captures notify-send --print-id, stores the successful ID under the existing lock and passes --replace-id on later changes. Invalid saved IDs fall back to 0. The stack tag remains a fallback; notification errors still never fail temperature changes.

## Verification and follow-up

A later verification during active desktop use printed 3900 K twice but its final combined identity/state assertion failed. The immediately following diagnostic found 3150 K and separately logged two successful adjust-0 operations at 3150 K with ID 109 both times. This supports concurrent temperature adjustment; the first probe did not log enough detail to assign its failing assertion conclusively. Do not restore an older temperature over active user changes. Replacement was freshly verified with separate state and ID observations.

Defining test failed because --replace-id=123 was missing. A review also identified malformed saved notification IDs escaping best-effort handling; invalid UTF-8 and oversized decimal tests observed RED, then catching ValueError (including UnicodeDecodeError) made all 6 controller tests pass. Related binding/startup/fish/emoji regressions passed. Final refresh exited 0. Installed source equals tracked source. Live consecutive set-current and adjust-0 calls returned notification ID 109 both times at 3000 K; the final separate diagnostic confirmed 109/109 at 3150 K. Once a popup expires or Dunst restarts, a new popup/ID is expected. No visual animation inspection performed.

## Memory lookup

Query: `Dunst stack tag replace notification id`. Read `local-dunst-stacked-script-state`: it concerns history/audio transfer, not notification identity, so its remedy does not answer the user's request. New learning: stack-tag replacement does not prove stable notification identity; use explicit returned replacement IDs and verify them live.
