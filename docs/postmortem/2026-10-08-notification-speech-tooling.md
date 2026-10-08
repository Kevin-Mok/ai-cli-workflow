# Notification speech implementation tooling failures

This report records incidental editing and validation failures during notification speech implementation; feature RED failures are intentional and excluded.

- Symptom: temporary implementation writer stopped at hooks.json with NameError for missing json import, after writing helper, bridge and notify callback. No existing files lost.
- Lookup: reviewed postmortem-memory execution-environments ext-exec-function-scope; similar Python helper scope error, but this cause is simply omitted import. Inspect partial writes before resuming; do not rerun append-based generator.
- Resolution: write only missing hooks.json using explicit import; preserve prior edits.
- Setup validation: basedpyright initially produced 14 strict-default warnings and exit 1; typed argparse/JSON boundaries and intentional discarded returns corrected them. Agent reviewed 2026-10-06-context-helper-type-boundary.md; fresh setup check exits 0 with no diagnostics.
- Test refinement: Unicode worker payload test asserted raw JSON encoding rather than decoded content; assert exact decoded title so either valid JSON encoding is accepted.
- Integrated type check: bridge had two missing generic dict type arguments; specify dict[str, object] at metadata boundary.
- Read probes: guessed snapshot function/config-template paths and an old snapshot-loss report path did not exist; rg --files resolved actual sources. No state mutation.
- Review diagnostic: schema Counter.update(dict) misinterpreted dictionary values as counts; use dictionary keys. No production impact.
- Extended Dunst fixture: added speech-disable playback but retained final cumulative count 5, so observed 6 failed assertion; correct final cumulative expectation to 6. Existing lessons about fixture-derived expectations apply; production sequence itself matched required extra rollback playback.
- Status: verified tooling fixes: final 35 notification tests, 135 broader Codex tests, private Dunst and type checks pass. Runtime audio activation remains separate.
- Follow-up: retain task-scoped editing, inspect partial writes, type-check helper interfaces before deployment. No new reusable learning beyond existing Python scope/typed-boundary guidance.
