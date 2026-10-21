# Sire notification intro and contained session commits

Preserve the working local Sire intro in Git and make forced session commits retain useful task work without collecting unrelated changes. Add the asset and selection instructions, verify playback, update the commit skill, and ship only attributable changes.

## Scope and decisions

- `scripts/sire.mp3`: reusable 4,550-byte offline Ryan recording of `Sire.` at pace 0.95. No local paths or settings are bundled.
- Update notification documentation, its existing smoke checks, the README entry, and `dot_agents/skills/commit-session/SKILL.md`.
- Explicit `force commit-session` requests a meaningful nonempty commit, preserving session containment, privacy checks and hooks. It never implies force-push.
- Protect every dirty path captured before this session; README and smoke checks contain unrelated changes, so stage only this task's hunks. The untracked `:memory:.ses` has no established attribution and stays excluded.

## Checklist

- [x] Capture Git status and confirm `main` with upstream `origin/main`.
- [x] Observe baseline failure: commit-session stopped with no commit after local-only work; live setting initially selected the old question clip.
- [x] Generate and select Sire locally; preserve the original clip.
- [x] Preserve the MP3 and document selection and speech order.
- [x] Add forced-commit fallback with containment and safety boundaries.
- [x] Validate asset decoding, selection, speech order, skill decisions and README (warnings below).
- [x] Run refresh-config and targeted audio apply.
- [x] Review and stage only attributable files/hunks; run privacy gate.
- [x] Prepare the verified session commit and configured upstream push (results reported in delivery).

## Verification and progress

- Original local preview with `--title 'Your notification message will follow Sire.' --details`: exit 0. MP3 decoding, selected path, enabled speech and preserved original were checked successfully.
- Earlier scope helper returned `unsafe`: no repo-writing actions. Direct writes in this task now establish attribution; helper results must be reconciled with them.
- README gate before edits: `pass_no_change`.
- Fresh asset decoding passed; metadata contains only the encoder tag, duration 0.496327 seconds. Installed preview after targeted `chezmoi apply` returned 0. Two refresh-config runs returned 0. README gate passed.
- Focused notification tests: 68/69 passed; event-probe temporary-directory cleanup failed. Question tests: 12/12 passed. Generic skill validation rejects pre-existing `disable-model-invocation`; retain that field. See the [validation report](../docs/postmortem/2026-10-21-sire-session-validation.md); its targeted memory check passed.
- Independent skill evaluation passed five decision scenarios: public asset/private setting, mixed README/missing metadata, secrets-only, failed privacy gate/safe subset, and missing upstream.
- Scope helper still cannot detect Code Mode writes and returns `unsafe`; use directly observed file/hunk writes for containment.
- Staged candidate contains eight session files, including only Sire hunks in README/smoke and one new ledger record. The first privacy gate blocked a home-path alias; neutralizing it produced a fresh PASS. The exact staged ledger/report check passed through disposable physical-alias translation. Commit hooks and the immediate pre-commit privacy gate remain enabled.
- Manual acceptance: hear only Sire followed by the message; confirm a naturally occurring notification separately. Automated playback exit status does not prove subjective sound quality.

## Risks, review and rollback

The MP3 is public reusable synthesized audio without notification content. No hook or playback logic changes. A forced workflow must still report concrete safety/permission blockers rather than fabricate work. Roll back the selection with the existing `set` command pointing at the preserved original clip. Restore the prior skill wording if the fallback proves too broad. Never stage the unrelated README/smoke hunks or private sound JSON.

## Commit milestone

Planned subject: `feat(notifications): preserve Sire intro and forced session commits`.
Implementation and contained candidate verification are complete. Execute the commit and upstream push after this pre-commit record; their observed hash and result belong in the delivery response. Nonblocking validation warnings above; no known safety blocker. Suggested Cursor follow-up: "Investigate EventProbeTests.test_real_event_cli_probe_exercises_audio_and_silent_paths temporary-directory cleanup without changing notification eligibility; reproduce before fixing." Manual follow-up: hear a naturally occurring notification. No playback logic changed.
