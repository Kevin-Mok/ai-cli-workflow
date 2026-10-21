# Sire session validation warnings

Record the checks that did not pass during the contained Sire asset and commit-session guidance update. Keep these limits separate from successful local playback and avoid changing unrelated runtime code to make this commit green.

## Symptoms and impact

- The generic skill-creator `quick_validate.py` rejects the existing `disable-model-invocation` frontmatter key. The field predates this task and was explicitly supplied by the user. The validator therefore cannot certify this skill unchanged; do not remove the invocation boundary to satisfy it.
- `python3 -B tests/test_codex_notification_sound.py` returned 1: 68 of 69 tests passed. `EventProbeTests.test_real_event_cli_probe_exercises_audio_and_silent_paths` failed with `Directory not empty` during temporary smoke-directory cleanup. A detached-worker cleanup race is a hypothesis, not an established root cause.
- Earlier optional source reads used nonexistent skill/refresh-script paths. Discovery resolved the actual Ponytail package path and Fish refresh function; no user configuration repair was needed.

## Lookup and applicability

Searched tracked postmortem memory for `TemporaryDirectory Directory not empty skill validator disable-model-invocation`. Broad results did not establish a remedy for either validation warning. `local-discover-paths-before-reads` applies to the optional read failures: inventory actual paths rather than infer executable filenames. Neither failed validation justifies changing the notification playback implementation in this asset/documentation task.

## Status and evidence

The first staged privacy check blocked a machine-specific home-path alias in this report's memory-ledger entry. Replace that public alias with the repository's neutral `/home/example/` convention and rerun the gate. Keep physical alias translation in a disposable private validation fixture; it does not belong in the published ledger.

The two validation warnings remain unresolved and were not retried or hidden. All 12 question-notification tests passed. Asset decoding, live selection, preserved original clip and local preview passed. README gate returned `pass_no_change`; refresh-config returned 0. An independent five-scenario review accepted force-mode containment, secret exclusion, privacy-gate enforcement, mixed-hunk ownership and missing-upstream handling.

## Follow-up and learning

Investigate the temporary-directory lifecycle independently before claiming that test green. Use a validator supporting this repository's invocation metadata before claiming generic skill validation. No new reusable remedy is established: retain an explicit no-new-learning ledger decision rather than invent a verified fix. These warnings do not weaken the mandatory privacy gate or authorize unrelated dirty files.
