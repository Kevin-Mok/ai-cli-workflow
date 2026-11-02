# Persist dual-jack audio

Save the working ALC897 front-headphone/rear-speaker setup and restore its mixer switches through one script used by both `ubs` and i3 startup.

## Context and decisions

`ubs` expands to `ubuntu-start`; i3 already launches that same script. Add one hook there rather than another i3 command. The installed `/lib/firmware/hda-jack-retask.fw` already assigns both output pins to one association; save its exact non-secret pin configuration for recovery. Do not reload drivers, restart PipeWire, move streams, or change volume. Discover the ALC897 card with `aplay -l`, since card numbers can change. Other machines without ALC897 skip safely.

## Scope and protected work

Change only the new helper/test, one startup hook, README, an Audio smoke entry, the mapping snapshot, and this plan. Initial dirty files: smoke-tests.md, postmortem-memory reference files/sources.json, fn-progress.fish/test, Vesktop settings, and an untracked SSH postmortem. Preserve all existing edits. Live ubuntu-start is older than source; its only difference is the superseded redshift command. No i3 configuration edit is needed.

## Checklist

- [x] Resolve shortcuts, startup route and working hardware mapping.
- [x] Observe defining test RED, then add minimal helper and startup hook.
- [x] Save mapping and update README/manual smoke check.
- [x] Run focused tests, syntax checks, refresh-config and deployed helper.
- [x] Record final evidence and limitations.

## Verification and risks

Run `python3 -m unittest discover -s tests -p test_dual_jack_audio.py -v` with fake ALSA executables: card-number independence, only unmute operations, safe no-card skip, actionable failure, plain output. Run the existing AUX helper regression. Inspect that startup calls the helper; execute installed helper and inspect live mixer switches after refresh. User confirmed both outputs audible before implementation. Reboot/login is not performed; existing HDA retask firmware is a prerequisite and is saved for recovery. Roll back by removing the startup call and helper; current hardware routing is unchanged.

## Review and delivery

Cursor continuation prompt: Review scripts/executable_set-dual-jack-audio and its ubuntu-start hook; run the focused tests, then verify both jacks audibly after a new i3 login without changing volume or restarting audio. Commit subject: `feat(audio): restore dual-jack playback at desktop startup`.

## Commit-session milestone

User authorized session-only commit and push. Session `01a19e7f-4054-7071-9811-6d0e83fe15de`; scope helper returned unsafe because it detected no repo-writing events, so directly observed edits and the captured initial dirty baseline define scope. Include only this session's Audio smoke entry and one report ledger record from mixed files; exclude all pre-existing hunks. Focused tests (4/4), startup integration, AUX regression and shell syntax passed again this turn. README executable gate returned `pass_no_change`. Completed work: helper, startup integration, firmware recovery snapshot, tests and documentation. Blockers: none identified. Remaining delivery: staged privacy gate, focused commit, one push to configured `origin/main`; report exact outcome separately. Full ubs/reboot/login checks remain intentionally unperformed.

## Final evidence

- RED: four defining unittest failures before the helper existed (exit 1).
- GREEN: `python3 -m unittest discover -s tests -p test_dual_jack_audio.py -v`, 4/4 passed; `bash tests/test_ubuntu_start.sh`, `bash tests/test_fix_aux_speaker_audio.sh`, and `bash -n scripts/executable_set-dual-jack-audio scripts/executable_ubuntu-start` all exit 0. Startup fixture executes the audio hook once without Fish exports.
- Installed both reviewed scripts directly because migration exclusions leave `ubuntu-start` unmanaged by chezmoi. `cmp` confirmed both installed copies match source and the firmware snapshot matches `/lib/firmware/hda-jack-retask.fw`.
- `fish -c refresh-config` completed with exit 0 and `REFRESH COMPLETE`; existing unrelated edits remained present. README gate: update_in_same_change, documented new behavior/options in the existing Day-to-Day section; original recruiter/stack/setup ordering retained.
- Installed helper and `--plain` both exit 0. Live Master stayed 61/87 (70%), Front/Surround stayed 87/87 (100%), all switches on; PipeWire stayed 46%, mute no. Help exit 0. No audio service restart or i3 reload required because the existing i3 startup entry already calls ubuntu-start.
- `git diff --check` for touched existing files passed. Postmortem records the scoped access workaround, guessed paths and unmanaged-script apply fallback; tracked ledger has explicit no-new-learning decision.
- Not performed: reboot/new i3 login, whole-repo suite, full `ubs` execution (would also affect displays/mounts/apps), or wrapped clipboard/TUI paste checks. Short invocation commands avoid wrapping; no renderer changes. User's listening confirmation predates the persistence helper. Startup deliberately unmutes Master/Front/Surround; volume levels remain user-controlled. The existing matching HDA retask boot mapping remains required.
