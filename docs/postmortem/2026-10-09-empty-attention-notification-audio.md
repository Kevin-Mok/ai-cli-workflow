# Audio notifications without a user-facing result

Trace unwanted question-clip playback while Codex is still working, then restrict automatic audio to verified user-facing completions with a nonblank final response. Keep normal completed-answer audio and manual previews available.

## Symptom, impact, and evidence

The user reports “Can I ask you a question?” playing when nothing needs reading or answering. Live sound and speech are enabled, and installed event/sound handlers match repository bytes. The bridge accepts ordinary subagent completion and unknown metadata, with no check for final-response content. Recent live thread_spawn transcripts contain an inherited task_complete immediately on spawn, followed by active task_started records; root work continues. Guardian provenance is already excluded. This establishes an eligibility defect, but there is no historical playback log proving which specific event caused the reported sound.

## Lookup and environment

Read tracked postmortem-memory and systematic-debugging procedures. Query `notification repeated completion ordinary subagent unknown metadata` matched `local-notification-provenance-before-fallback`: provenance must precede audio fallback, but its previous ordinary-worker eligibility does not meet this user's current attention requirement. Prior permission-audio-flood report applies to loaded permission silence and owned queued-worker cleanup; permission requests are already rejected by the deployed bridge.

The first read-only shell launch failed before execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. Query `bwrap loopback Failed RTM_NEWADDR` matched `ext-sandbox-loopback` and `local-sandbox-loopback-approved-route`; their scoped approved execution workaround applies. Read-only `pwd`, status, source inspection, and live audio status then succeeded using that route. No sandbox settings changed. Independent review's broad candidate-path file inventory exited 2 on absent directories; inspect actual installed paths before further inventory. No files changed from that probe.

## Status and next steps

Resolved and deployed. Defining RED proved worker, unknown provenance, conflicting metadata and blank/missing final-response audio. The bridge now requires event-local nonblank last-assistant-message plus unambiguous cli/vscode metadata with no parent provenance. All helper/internal threads and unknown origins are silent. Valid root answers retain exact saved-title capture and missing-title MP3 fallback. The isolated CLI probe covers eight event scenarios. refresh-config completed with exit 0 and installed targets verify. Preserve all pre-existing dirty work. No commit or push requested.

## Verification and limits

Focused event/probe GREEN: 16 tests, exit 0. Full notification/speech regressions: 67 tests in 15.300s, exit 0; deliberate audio-error fixtures emit expected diagnostic warnings. Type check: zero errors/warnings, exit 0. Private Dunst: one test in 3.375s, exit 0. Installed eight-case probe: one playback for completion, zero for worker/empty/missing/unknown/ambiguous/parent/permission, exit 0, using a silent isolated player. Installed real-ID resolver: this user conversation eligible with exact saved title; helper agent ineligible. chezmoi verify exits 0; status preserves enabled sound/speech, ready Voice Contributor high voice and selected question clip. Independent review found no issues and reran all 16 event/probe checks successfully. README gate pass_no_change; diff check exits 0. Rollback can restore the event handler source and redeploy; speech disable restores older popup audio and therefore is not a guarantee of silence. Hardware listening and real subsequent user-facing completion remain manual acceptance checks.

## Documentation edit tooling failure

The first documentation-edit Python heredoc failed compilation with SyntaxError because a compound `with` statement followed a semicolon. No part of that heredoc executed and no files changed. Search `Python SyntaxError compound statement semicolon` was checked before retry; installed Python grammar and the exact error establish the correction: put `with` on its own statement line. Existing editing-contract guidance applies; no new product root cause. Retry the same scoped edits with valid multiline syntax.

## Broader concurrent-work validation

The broader Codex suite ran 191 tests in 48.235s and exited 1 with five session-priority/picker failures: priority ordering API missing, priority detail missing, new --sort handling missing, and async picker priority-refresh behavior missing. Those modules/tests changed concurrently outside this audio task. No notification failures were reported. Preserve that work and do not remedy it here. Audio handler/probe type check exits 0 with zero errors/warnings; private Dunst integration exits 0 (one test, 3.375s). Run complete focused audio regressions and record the broader limit.

Queue preflight correction: the first inventory omitted its os import and swallowed NameError, so its empty list was invalid evidence. Repeated with the correct import and only OSError handling: exact same-user installed event-play worker PIDs []. No queue termination needed when empty. refresh preflight: tracked/live Git config bytes match; Codex live reasoning xhigh and service tier default differ from tracked low/fast. The mandatory refresh snapshot preserves those existing live preferences.

## Final broader verification and learning

After concurrent picker implementation changed, reran the broader suite: 193 tests in 45.189s, exit 1, with one unrelated failure: `test_async_recap_preserves_query_and_uuid_and_ctrl_g_requests_selected` in RecentPickerTerminalTest. Its private picker could not start because installed fzf rejected `transform:... --helper restore ... {q}` (exit 2). Complete output saved at /tmp/codex-audio-final-regression.log and reviewed. No audio failures. This supersedes the earlier five-failure broad result; do not claim the entire repository suite passes. Leave concurrent picker work untouched.

Documentation edit retry succeeded with valid multiline syntax; README, guide, shared smoke checks, prior/current plans, feedback and local lesson updated. Sandbox workaround remains covered by existing findings. New learning: `local-notification-user-facing-completion` records the verified eligibility/deployment boundary; postmortem ledger and state-security reference are updated in the same task. Exact historical sound attribution and subjective hardware listening remain unproven; tests establish the repaired false-trigger paths. No commit/push requested or performed.
