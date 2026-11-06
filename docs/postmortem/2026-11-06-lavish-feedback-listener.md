# Lavish feedback has no listening agent

Restore the review feedback loop by identifying the generating Codex conversation and attaching the supported foreground poll. Verify listener registration and real user-message delivery separately.

- Symptom: user screenshot shows Your agent is not listening, despite a visible Conversation input and Send to Agent button.
- Impact: page feedback cannot currently reach a running agent for questions or edits.
- Evidence: lavish-axi poll --help requires a foreground long poll; Codex background job completion is not guaranteed to resume the agent. Reply alone posts text and exits; it does not keep a listener alive.
- Lookup: searched Lavish listener poll feedback in tracked incident memory. Returned generic boundary and listener material, no specific verified Lavish routing remedy.
- Status/resolution: creator confirmed as Codex thread 01a1b28b-e50a-7753-88bb-e9543235de68 from its HTML-write and matching session-open transcript. Native send_message_to_thread resumed it and it started the supported foreground poll with owner job-search-creator. Parent independently verified live host inventory: open, pending_prompts=0, listener=job-search-creator. Actual user-message round trip verified: the user asked which codex session are you attached to; local host session state records delivery at 20:50:13Z and the creator reply naming its exact session at 20:50:30Z. pending_prompts=0; creator resumed its foreground listener.
- Next steps: identify creator, restore supported listener in that conversation when available, and verify feedback arrival. Do not claim persistent automatic wake-up from a foreground-only poll.

- Architecture evidence: installed lavish-axi 0.1.89 derives session identity from canonical file paths and stores no originating Codex thread. The poll owner is a label, not a router. Restoring the actual generator requires explicitly resuming that verified thread and polling there.
- Prevention: added the generating-conversation question/edit/Send & End checks to docs/smoke-tests.md and saved the user preference in the canonical feedback log.

- Verification boundary: sandbox `lavish-axi` inventory continued to show listener=none, while an approved host-level read showed the active listener. Treat sandbox inventory as potentially cached when localhost access is restricted; verify host state before declaring a live listener absent.
- Root cause: the generating turn had completed without a foreground listener or verified automatic wake path. Lavish does not persist a creator-thread route.
- Follow-up: keep the creator polling through each reply until review ends. Persistent automatic resumption after the conversation stops is not provided by the installed CLI. No new daemon, takeover, or artifact changes were made.

## Reusable connection regression

The new scripts/executable_lavish-connection-test replaces informal readiness
claims with a live nonce round trip. It observes delivery without competing for
the feedback poll, asks the agent for its own environment session ID, and requires
the foreground listener to resume before PASS. The expected ID is never embedded
in the challenge. Twenty real-CLI/local-HTTP fixture cases passed, including
processing gaps, queued feedback status, stale/wrong replies and timeout.

Fresh host run for session 9d81ca97d78a457f with expected creator
01a1b28b-e50a-7753-88bb-e9543235de68 returned PASS, exit 0, after about 18s.
Nonce: 5ac7c7dc765f4f4399877898a4c9c03e. The disconnected live check returned 1
before any test POST. This remains a point-in-time test, not automatic resumption.
The acknowledgement deadline cannot accept a late reply; an in-flight network
read may delay failure by up to five seconds.

Wrong-session live negative: nonce 46a97e616eec4c00a92f3af319d44e90 returned the actual creator ID, while the checker expected a different valid UUID. It rejected that reply with exit 1 after about 14s; plain output was ASCII. The negative-test wrapper asserted the failure and exited 0.

## Bare-command invocation follow-up

User ran the delivered executable without arguments and received the required
url/--expect-thread error. The checker required flags and gave no guided entry
point for an interactive terminal. Impact: the user could not start the check
from the bare executable. Relevant memory lookup: CLI no arguments required
guided prompts; generic boundary guidance and this incident matched, but no
specific no-argument workflow existed. Current status: test-first fix in progress
to prompt for missing URL/session ID, preserve explicit arguments, and fail
cleanly on EOF without sending feedback. No automatic session guess or registry.

Guided invocation resolution: a defining no-argument CLI test reproduced exit 2
with required URL/session flags before implementation. The checker now prompts
for missing values, preserves explicit flags, and rejects blank/EOF before any
message submission. Independent focused suite passed 24/24 in 5.945s; bounded
review found no material regression. A real fresh fish PTY launched the bare
executable and displayed both prompts; it was deliberately stopped before an ID
was entered, so no new live nonce was sent. README gate passed.

Implementation tooling note: an initial Python source-replacement command had a
quoting SyntaxError before any write. The worker used apply_patch successfully;
no source damage occurred. This is covered by existing shell-transport guidance,
with no new general remedy.

## Self-contained preset smoke test

The user clarified the intended primary command: create a preset static mockup,
start its own creator, and verify that route without asking for IDs. Bare mode
now launches normal configured codex exec with automatic approval review in an
owned private temp directory; its creator copies the preset byte-for-byte and
opens Lavish. The harness captures thread.started identity, locates only that
owned page, and uses the existing nonce check. It stays foreground after PASS
for actual questions/edits, ending only owned page/process group on review end.
Explicit URL/ID mode remains for verifying other real editors separately.

Real configured smoke run created session 01a1b2bc-7345-73d2-acc4-d57ca7a47d7d
and page ed32a53224d302d5 in ~28s. Nonce92bc1a4185b74793b254f868de9b7015
passed in ~13s. Parent intentionally interrupted after interactive-ready PASS;
checker exited130 and acceptance wrapper exited0. Independent host state showed
the test page ended, exact preset bytes matched, and original job-search listener
remained active. This run preceded final descendant-cleanup/preset-enforcement
and explicit-Chrome prompt refinements; final fixture coverage verifies those.

Review-driven RED/GREEN cases cover creator early exit, owned TERM-ignoring child
cleanup despite exited leader, preset tampering before any visible PASS, and
startup JSON body deadline. Creator preview now explicitly uses google-chrome
with Lavish --no-open; no default browser, model override or approval bypass.
A helper follow-up hit the agent-thread limit; source inspection directly
confirmed --no-open instead of spawning/retrying helpers. No data was changed
by that failed tool call; no new general learning beyond bounded source fallback.

Final bounded review verified all six creator/bootstrap invariants with no unresolved finding. Regression suite now has29 cases, including late registration during shutdown; independent runner results are recorded in the active plan. No additional model run was needed for those isolated cleanup safeguards.

## Prepared manual edit request and expected chat result

User requested an informative prefilled message and expected results in terminal
and Lavish chat log. Installed app has no composer-draft endpoint, and its
sandbox blocks direct parent DOM access. The supported artifact SDK queuePrompt
instead prepares an unsent Conversation card; Send to Agent remains user action.
After automatic PASS the owned page receives a stable-key helper requesting
heading Connection verified, unchanged visible styling, own-session confirmation,
and helper removal in the same edit to avoid reload requeue. Existing textarea
text is untouched. Bare nonce ACK must contain the expected-result notice before
PASS, and terminal prints the matching expected heading/creator ID.

RED observed missing helper, missing terminal notice, and acceptance without chat
notice. One new fixture initially omitted its end event and timed out; corrected
fixture then failed for the intended missing-notice branch before the guard was
implemented. Independent31 suite passed but exposed a pre-existing timer cleanup
race: delayed callback read its state.json after TemporaryDirectory deletion.
Tracked/joined fixture timers before directory teardown; final rerun is recorded
in plan. No installed package edits or automatic manual-message submission.

Live current demo e8e4efa34f8ad1e9 was updated with the helper. An expected-result
chat notice was posted only after checking for no unacknowledged delivered notes.
Fresh host Chrome snapshot showed original heading, Expected result agent notice,
QUEUED manual request and Send to Agent button. No send/click/edit was performed;
the actual manual edit/removal remains a user check. Existing launched processes
need a rerun for the new terminal-print behavior. Future bare runs prepare it
automatically after their handshake.

Post-completion coordination boundary: an unsolicited cross-thread status question arrived. An attempted factual reply was rejected by automatic approval review as unrelated communication without explicit user authorization. No reply was delivered and no workaround/retry was used. User-facing Lavish work remains complete. Follow-up: do not expand completed tasks into unsolicited cross-thread coordination.

Manual-result visibility issue: user screenshots show successful manual heading edit and creator reply, but terminal repeats generic waiting forever. Impact is misleading test progress/no final manual result in terminal. Loop currently observes only process liveness. Memory lookup found no applicable remedy; adding test-first completion detection without sending more feedback.

Manual-completion fix: initial CLI regression reproduced missing EDIT TEST PASS
for the completed edit. Added one-time completion monitoring and30s phase-aware
idle progress. Review independently reproduced two false-PASS cases in the first
predicate: regex matched h1 inside comments/scripts, and an expected-ID substring
could occur in another creator's reply. Defining regressions failed for all3
cases before correction. Final predicate uses HTMLParser and an explicit own
CODEX_THREAD_ID field, plus delivered/done request, subsequent reply, helper
removal and resumed live listener with matching state identity. Manual request
now specifies the own-ID reply format. Existing expected-output behavior stays.
Read-only host test of the pictured session returned completed=true and live
listener=true without sending anything. Existing process must restart to load
updated terminal behavior. Final independent results are in active plan.

Successful smoke never concludes: user reached EDIT TEST PASS but process remained in review keepalive. Prior design intentionally left it open; latest user intent requires a concluding smoke test. Memory lookup reviewed existing lifecycle material; it does not justify post-success waiting. Add failing no-user-end regression then return through owned-resource cleanup after TEST COMPLETE. No unrelated session should be closed.

Auto-conclusion regression run exposed4 test assertion failures: naive substring counting also counted the new instructional mention of EDIT TEST PASS, even for negative cases. Corrected assertions to count actual anchored success-report lines, preserving positive and negative expectations; no production check was relaxed. Final rerun recorded in plan.

Auto-conclusion resolution: after EDIT TEST PASS bare mode prints TEST COMPLETE and returns through the existing owned-resource finally, exit0. Old indefinite post-success review wait removed; early cancellation still possible. Latest real test82ce5e2c5321e805 / creator01a1b2f1-0ad9-7db0-94d1-73ab0dba78bd was confirmed complete independently and ended via CLI, so its old terminal can return. Screenshot referenced a different older creator; current terminal URL is authoritative. Docs/preset updated; defining no-user-end fixture proved prior hang before the fix.

Automatic E2E follow-up: user requested a smoother run. Bare mode now targets a
no-click create/nonce/SDK-send/edit/cleanup flow rather than preparing manual
feedback. Explicit existing-page mode must remain nonce-only. Worker defining
test initially failed to import because a triple-double-quoted Node harness was
nested in the fake creator's triple-double-quoted Python string (line189). No
implementation changed; fixture quoting is being corrected before observing
actual RED. This is test-authoring transport, not a product runtime failure.

Automatic E2E fixture follow-up: first full35-case suite had34 passes and one flaky fake-creator JSONDecodeError while reading state.json during a direct truncating write. Production state reader already retries partial JSON. Worker is adding bounded/appropriate fixture read retry and rerunning; this affects fixture authoring, not a real model/runtime failure.

Automatic E2E resolution: bare mode now uses the supported Lavish SDK queue+send
for the owned disposable edit, requires no clicks, bounds the edit phase, and
prints4 stages with5s progress. Final TEST COMPLETE follows confirmed cleanup,
not merely an end command exit. Review reproduced unknown/unreadable and still-
open cleanup false success; bounded rereads plus ended-record confirmation fixed
both. Independent36/36 tests passed21.399s; source reviewer5/5 claims verified.
Real normal-config no-input run exited0: creator01a1b2fd-49c9-77a3-83d7-8352a84cda02,
pagefd6a9b92bbc5a68b, noncec36955e81a3c482da40776a1ede1130b. Independent host read
confirmed ended, exactly2 messages, verified edit and no owned listener.
No unrelated editors or global settings changed. The latest user explicitly
authorized automatic edit submission in the disposable smoke only; normal
reviews and explicit existing-page checks retain their prior submission scope.

Session delivery prerequisite: scope helper missed observed orchestrated writes, so reviewed direct-write evidence sets scope. Oversized new checker/tests were split mechanically into cohesive sub-20k-byte modules;36 tests and exactly36 pytest collected cases passed after split. Plan condensed to final decisions/evidence; incident retains chronology. Optional upstream-marker lookup found no SOURCE.md and changed no files. Existing oversized README/smoke/guidance/ledger may retain non-safety file-size warnings; do not bundle unrelated edits or bypass hooks to silence them.
