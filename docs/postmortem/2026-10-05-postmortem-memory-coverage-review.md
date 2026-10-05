# Shared-memory source coverage review gaps

Independent review found two ways the new helper could claim complete coverage without accounting for genuine reports. Add defining temporary-fixture regressions, narrow template detection, and report missing registered sources before shipping the memory.

## Symptom and impact

A dated `template-substitution-failure.md` incident was excluded because its name contained template. Deleting a registered source then running full check returned success with zero discovered reports. Both gaps could hide incomplete source review.

## Evidence and current status

The reviewer reproduced both cases in disposable fixtures. Both defining regressions failed for the expected omissions, then passed after minimal repairs. Corrected discovery finds no additional old reports; the new living review report itself requires ledger registration.

## Root cause and resolution

Template exclusion used substring matching, and coverage compared only discovered sources to the ledger. Narrow template detection to actual template artifact names and compare registered aliases within selected scan roots against discovery. Search must remain useful when originals are unavailable; full check must report missing evidence.

## Verification and next steps

RED output records both omissions. After repair, all 23 then-current helper tests passed (exit 0). A third malformed-link regression exposed a generic TypeError diagnostic; guard reciprocal membership after field validation to retain actionable finding/field errors. Complete coverage follows ledger registration of this same report. Review any newly discovered reports before claiming completeness.

Final focused verification: all 24 helper tests passed after the third diagnostic repair (exit 0). Full corpus registration and integration checks are recorded in the matching plan; no older report was newly discovered by narrowed template detection.
