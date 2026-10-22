# Operational drift and resource limits

Use these reviewed findings to compare a failure with prior evidence. Check applicability and diagnostics before choosing a remedy; keep its verification scope and limits explicit.

## local-screensaver-launcher-mode-drift

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: refresh stops at a changed media-screensaver target with prompt EOF even when launcher contents match.
- Applicability: Explicit installer mode0755 differs from chezmoi's executable mode0775 under configured umask002.
- Diagnostic checks: Compare source/live/rendered bytes and exact target diff, including permissions. Inspect actual managed/ignored targets before assuming a raw template will deploy.
- Remedy: When bytes agree and the permission delta is reviewed, reconcile only that exact target through chezmoi; keep the broad apply unforced and retry normal configured Fish refresh.
- Verification evidence: Target verify failed before repair and passed afterward with unchanged content. Real refresh completed all phases, exit0, with an empty private log. Installed status, original Fish startup and both focused regression checks passed.
- Limitations: Explicit reinstall can restore0755 and recreate drift; installer permission policy was not changed. Hook exclusion does not exclude ordinary executable files under the scripts directory. Do not force unknown content or permissions.
- Sources:
  - [Refresh launcher mode conflict](../../../../docs/postmortem/2026-10-20-refresh-screensaver-mode-conflict.md); reviewed hash and aliases in [sources.json](../sources.json).

## ext-buildx-install-activation

- Status: **activation_pending**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Docker Buildx unavailable; check error omits install recovery; non-interactive sudo preflight rejects uncached credentials
- Applicability: Control-machine prerequisite installation on Ubuntu/Docker environments.
- Diagnostic checks: Check installed prerequisites to avoid duplicate installation.; Choose an available package candidate instead of assuming one package name.; Use an interactive sudo validation step when installation is authorized.
- Remedy: Use the corrected helper's explicit --install mode, then rerun --check in an authenticated terminal.
- Verification evidence: Helper regressions passed for alternative Buildx package names and uncached sudo; no system package was actually installed during implementation.
- Limitations: Code-level helper verification does not prove the control machine now has Buildx or that remote preparation/deployment ran.
- Sources:
  - [2026-10-02-buildx-prerequisite-install.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-02-buildx-prerequisite-install.md) (SHA-256 `cf43ab9afa7c`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-23-infrastructure-patch-failure.md](/home/example/coding/example-client-app/docs/postmortem/2026-09-23-infrastructure-patch-failure.md) (SHA-256 `bc27ed7ce2b0`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-cached-integration-prerequisites

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: optional integration cannot find postgres:16-bookworm; no-pull guard stops before container creation; cached PostgreSQL 16 alternative available
- Applicability: Isolated Docker integration intentionally prohibited from implicit image pulls.
- Diagnostic checks: Inspect local cached image tags and required major-version compatibility.; Check whether a documented image override exists.; Separate optional prerequisite failure from completed focused checks.
- Remedy: Use the explicit POSTGRES_TEST_IMAGE override with the compatible cached image; preserve the no-pull guard.
- Verification evidence: Complete infrastructure suites passed using cached postgres:16-alpine, including isolated role/restore checks; no image was pulled.
- Limitations: A different tag must satisfy the test's actual requirements; never silently pull or swap major versions to make tests pass.
- Sources:
  - [2026-10-04-vps-recovery-implementation.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-04-vps-recovery-implementation.md) (SHA-256 `db3fcc8d0ae1`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-vps-workflow-inspection.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-04-vps-workflow-inspection.md) (SHA-256 `409c6dd1137b`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-compose-app-parity

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: student route returns landing page; Docker API-only mode differs from local app-serving startup; bind mount hides image-built static exports; stale static exports survive source fixes; Linux reload watcher uses BSD stat flags
- Applicability: Local Docker and host startup paths intended to expose the same combined app/API surface.
- Diagnostic checks: Compare entry points, API-only flags and served routes.; Inspect bind mounts against image-built asset paths.; Compare source freshness to static exports and reload defaults.
- Remedy: Route both paths through the canonical app-serving startup; mount only shared data, build missing/stale exports and disable unnecessary reload in that app-serving workflow.
- Verification evidence: The report documents the root causes and implemented changes, but supplies no completed before/after command results.
- Limitations: These are grounded implementation remedies awaiting independent evidence in this record. Static-only worksheet IDs remain distinct from backend-owned IDs; do not infer deployment activation.
- Sources:
  - [2026-05-28-docker-start-app-local-parity.md](/home/example/coding/example-project-2/docs/postmortems/2026-05-28-docker-start-app-local-parity.md) (SHA-256 `3369dd68289c`; 5 alias(es), all retained in [sources.json](../sources.json)).

## ext-gitea-restart-mitigation

- Status: **verified_workaround**; root-cause confidence: **supported**; verification scope: **workaround**.
- Symptoms: Gitea stalls improve after service restart
- Applicability: Temporary recovery after preserving enough evidence to distinguish upstream application stalls from proxy failure.
- Diagnostic checks: Record response latency before/after restart.; Check whether abusive or expensive requests immediately resume.
- Remedy: A scoped service restart can restore availability temporarily while root-cause work continues.
- Verification evidence: The incident report records improved responsiveness after daemon reload and restart; subsequent incident shows restart alone did not hold under renewed traffic.
- Limitations: Restart is a state reset, not a permanent repair; preserve fault evidence first.
- Sources:
  - [2026-03-13-gitea-502-bad-gateway.md](/home/example/coding/fixes/docs/incidents/2026-03-13-gitea-502-bad-gateway.md) (SHA-256 `dd01b4879d0b`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-03-18-gitea-spam-induced-latency.md](/home/example/coding/fixes/docs/incidents/2026-03-18-gitea-spam-induced-latency.md) (SHA-256 `0739ee9baaa9`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-gitea-upstream-stall

- Status: **unresolved**; root-cause confidence: **supported**; verification scope: **none**.
- Symptoms: intermittent Gitea 502; root route quick but profile hangs; healthz intermittently 20–50 seconds; single thread near full CPU
- Applicability: Self-hosted Gitea with route-specific latency where proxy and upstream are both reachable.
- Diagnostic checks: Compare root/profile/health routes locally at the upstream and through the proxy.; Capture application logs, thread/CPU state and database configuration before restarting.; Use non-destructive incident capture; invasive dumps need their own scope.
- Remedy: Investigate the application/database bottleneck; proposed upgrades, PostgreSQL migration and proxy timeout tuning require validation and are not established fixes.
- Verification evidence: Nginx was stable and direct upstream profile requests stalled; incident report calls the cause a working theory and not permanently fixed.
- Limitations: Database locking/expensive query explanations remain hypotheses; a proposed timeout change may hide symptoms without removing the bottleneck.
- Sources:
  - [2026-03-13-gitea-502-bad-gateway.md](/home/example/coding/fixes/docs/incidents/2026-03-13-gitea-502-bad-gateway.md) (SHA-256 `dd01b4879d0b`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-missing-readme-gate-fallback

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: executable_readme-recruiter-sync missing; README gate not executable; git log --follow requires exactly one pathspec
- Applicability: Delivery workflows in repositories that lack the documented README wrapper.
- Diagnostic checks: Inspect installed skill requirements and actual README surfaces.; Use one path per git log --follow invocation or omit --follow for multiple paths.; Report automation availability independently of content validation.
- Remedy: Apply the installed README skill's concrete manual contract checks when allowed; preserve the missing-wrapper finding and use valid history commands.
- Verification evidence: Two reports record passed manual README reviews; shell/help/link checks and diff check passed in the earlier delivery incident.
- Limitations: This does not restore automation or waive unrelated required tests. One later report still had a truncated test suite blocking verification.
- Sources:
  - [2026-09-04-commit-validation-helper-missing.md](/home/example/coding/example-client-app/docs/postmortem/2026-09-04-commit-validation-helper-missing.md) (SHA-256 `488a3f8ccacd`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-22-readme-gate-missing.md](/home/example/coding/example-client-app/docs/postmortem/2026-09-22-readme-gate-missing.md) (SHA-256 `f48da0e0a70d`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-reader-retry-progress

- Status: **activation_pending**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Could not refresh unreacted tweet jump after midnight; ten-second scan restarts from midnight; reaction checks pause over four seconds; TimeoutError hidden as OSError
- Applicability: Paced Discord history/reaction scans with bounded retries and generation/selection invalidation.
- Diagnostic checks: Log exception class/status/progress instead of swallowing the cause.; Use a read-only live scan to observe timeouts and increasing checked-message progress.; Test invalidation on day/selection/reaction changes and isolation between generations.
- Remedy: Retain confirmed reacted-message IDs across failed attempts, reset progress on successful completion or relevant invalidation, and emit diagnostic context. Restart the updated bot within the operator's authorized scope before claiming activation.
- Verification evidence: Two defining RED failures preceded correction; 147 tests and Pyright passed; a read-only live scan progressed across two timeouts and found the target on attempt three.
- Limitations: The existing bot process was explicitly not restarted. A single request exceeding the ten-second budget remains a limitation; today-only selection intentionally excludes yesterday.
- Sources:
  - [2026-10-04-overnight-reader-jump.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-04-overnight-reader-jump.md) (SHA-256 `e44b69235005`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-recoverable-channel-activation

- Status: **activation_pending**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: inaccessible channel closes Gateway before repair; counting unavailable until channel validated
- Applicability: Bots designed to allow authorized channel replacement while online.
- Diagnostic checks: Test Gateway remains open with counting paused.; Verify replacement permissions before save/activation.; Test administrator authorization, competing repair operations and reader cancellation.
- Remedy: Keep the Gateway online in a recoverable setup state, serialize repair/dashboard operations, validate an authorized replacement and persist it only after success.
- Verification evidence: Seventy-seven offline tests, Pyright, compilation and shell syntax passed; implementation's live repair remained a manual smoke step.
- Limitations: The original remote permissions/ID fault is not diagnosed or fixed automatically. Live behavior requires activating updated code and checking authorized channel selection.
- Sources:
  - [2026-10-02-channel-recovery.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-02-channel-recovery.md) (SHA-256 `e2e684e02121`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-audio-sink-mute

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: applications playing but AUX speakers silent; PipeWire services healthy and analog sink MUTED
- Applicability: PipeWire/PulseAudio-compatible desktop output with healthy services and active application streams.
- Diagnostic checks: Inspect service health, default sink, explicit mute state and active stream routing with wpctl/pactl.; Confirm the intended output before restarting services or changing drivers.
- Remedy: Clear mute on the selected default sink and route active sink inputs to it; keep diagnostic mode read-only and service restart opt-in.
- Verification evidence: Focused fake-pactl regression and shell syntax passed; live wpctl after repair showed the analog sink at the original volume without MUTED and both application streams still routed there.
- Limitations: Healthy services and active streams alone do not prove audible physical output. This remedy requires evidence of mute/routing state; it does not diagnose every audio outage.
- Sources:
  - [33f83e3-aux-speaker-audio.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/33f83e3-aux-speaker-audio.md) (SHA-256 `68876a67a7c5`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-mime-drift-reconcile

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: refresh-config cannot open /dev/tty for MIME overwrite choice; FNLB association references removed desktop entry
- Applicability: Tracked versus installed MIME association drift causing a noninteractive ChezMoi prompt.
- Diagnostic checks: Read the actual tracked and live association and installed desktop identifier.; Run a target-scoped dry-run after reconciling the owned choice.
- Remedy: Align the tracked association with the intended installed desktop identifier; retain unforced conflict protection on the broad apply.
- Verification evidence: Focused association regression, target dry-run and full refresh all passed; refresh emitted REFRESH COMPLETE.
- Limitations: Earlier exact-target deployment only proved task-local deployment while full refresh remained incomplete. Future unrelated MIME choices still require reviewed ownership.
- Sources:
  - [2026-08-19-refresh-config-noninteractive-mime-prompt.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-19-refresh-config-noninteractive-mime-prompt.md) (SHA-256 `1ed007e686d3`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-time-bound-constant-drift

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: time-bound progress helper declares an event ended early; stale season label and date constants
- Applicability: Helpers depending on an externally changing fixed schedule.
- Diagnostic checks: Freeze the clock at an incident date.; Compare label, start and end values together against the intended schedule.
- Remedy: Update the related schedule literals together and exercise boundary dates through the real language entrypoint.
- Verification evidence: The deterministic Fish test confirms the corrected active label and schedule through the intended final active day.
- Limitations: The incident proves the stated historical schedule correction, not the current external schedule. Future values require current authoritative evidence.
- Sources:
  - [2026-08-04-fn-progress-stale-season-date.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-04-fn-progress-stale-season-date.md) (SHA-256 `6151f4584b44`; 2 alias(es), all retained in [sources.json](../sources.json)).

## ext-reader-event-cache-latency

- Status: **activation_pending**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Daily count publication waits for reaction/history scans; Successful scans erase cached positive reactions; Reader removal during history is overwritten by stale membership; Slow successful reconciliation immediately rescans
- Applicability: Discord reader features sharing accounting/routing coordination with bounded REST scans and sticky status publication.
- Diagnostic checks: Measure history, fetch and membership requests on cold/warm/live-event paths.; Hold history/fetch while applying reader additions/removals/deletions and selection changes.; Advance the clock during a successful scan beyond the reconciliation interval.; Verify live accounting and another server progress during network waits.
- Remedy: Keep scoped ID-only membership across successful warm updates, apply targeted events and treat persisted state as provisional after offline gaps. Run scans/publication outside routing and accounting locks; fence history snapshots and results with mutation versions. Start reconciliation cooldown at successful completion; merge complete quota history with live-send protection, deletion tombstones and reset guards. Separate fast edits from post-driven sticky relocation.
- Verification evidence: Defining RED-to-GREEN cache, live recovery and independent-review race regressions; 187 offline tests and cached Pyright passed. Synthetic warm and reader-add paths dropped from 51/52 reads to zero; cold work unchanged.
- Limitations: No live API or runtime restart performed. One-second publication is a healthy-path target, not a Discord latency guarantee. Periodic reconciliation still needs REST work and a request exceeding its two-minute budget can prevent progress.
- Sources:
  - [2026-10-06-count-update-latency.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-06-count-update-latency.md) (SHA-256 `e20c6026f866`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-native-title-current-intent

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: Kitty title describes a historical task quoted in session-review output while Codex works on the review itself.
- Applicability: Native Codex thread-name terminal titles after pasted historical output or a changed task.
- Diagnostic checks: Compare native name, Kitty title and actual current work; inspect the live request and title-call records before changing terminal settings.
- Remedy: Correct the identified native task name. Require current-intent title checkpoints at turn/resume/compaction entry and before substantive progress updates; discover deferred native title tools.
- Verification evidence: Native rename returned `Verify Second Brain sessions`; Kitty ls showed the same name with its activity glyph, exit 0. Strengthened instructions were deployed by refresh-config (exit 0), matched installed bytes, and passed independent reasoning review.
- Limitations: Title transport is verified; future instruction compliance remains a manual smoke check. Existing processes may retain old instructions. No polling or independent enforcement was added.
- Source: [Stale Codex title from a pasted session report](../../../../docs/postmortem/2026-10-08-stale-codex-task-title.md).

## local-notification-approval-event-queue

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: spoken task titles repeat during work without completion events; detached workers queue behind the playback lock.
- Applicability: Codex notification event-policy changes involving completion notify and already-loaded permission hooks.
- Diagnostic checks: Correlate task-complete counts with escalation requests; inspect same-user exact helper event-play workers only.
- Remedy: Gate on agent-turn-complete before resolving identity, remove the permission handler, stop enqueueing before cancelling revalidated owned detached audio groups, then restore prior activation. Loaded old hooks need the runtime gate.
- Verification evidence: 37 focused and 138 broader tests pass; private Dunst and type checks pass. Refreshed bridge handled ten permission calls silently with zero workers left queued.
- Limitations: Subjective future completion playback remains manual. A serialization lock prevents overlap but does not suppress obsolete event queues.
- Sources:
  - [2026-10-08-notification-permission-audio-flood.md](/home/example/linux-config/docs/postmortem/2026-10-08-notification-permission-audio-flood.md) (SHA-256 `a75ba67aec3c`; one alias retained in sources.json).

## local-notification-missing-clip

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: visible notification popups with neither clip nor speech; selected MP3 points to an absent checkout asset.
- Applicability: local clip-then-speech sequences that validate the selected MP3 before synthesis.
- Diagnostic checks: run installed `status --details`, inspect selected file existence and timestamped errors, and compare installed versus checkout copies. Check desktop mute separately rather than inferring speaker health from service status.
- Remedy: use the existing `set` command with an existing local clip outside the checkout, then `preview --title` to exercise both stages. A path correction needs neither a voice reinstall nor daemon restart.
- Verification evidence: installed status RED exit 1 then GREEN exit 0; offline Piper check and real preview exited 0. User confirmed both stages audible. Installed silent probes passed 14/14 notification and 6/6 question cases; independent accepted-question probe passed.
- Limitations: asset removal operation unknown; fixture playback proves routing rather than hardware output. User confirmed the real preview; a later natural event remains separate acceptance.
- Source: [Notification speech blocked by a missing clip](../../../../docs/postmortem/2026-10-16-notification-missing-clip.md).

## local-ubs-unattended-wallpaper-mount

- Status: **activation_pending**; root-cause confidence: **supported**; verification scope: **code**.
- Symptoms: wallpaper missing at i3 login, restored by manual `ubs`.
- Applicability: desktop assets live on a disk mounted through interactive sudo during graphical startup.
- Diagnostics: resolve the wallpaper symlink, inspect fstab and the mounted UUID, then check i3 PATH and noninteractive sudo authentication. A configured hook and compositor process do not prove wallpaper success.
- Remedy: use `scripts/enable-ubs-boot-mount.py` to preview and persist a UUID-based nofail systemd automount, with conflict refusal and fstab backup. Authenticate once in a terminal; preserve the current mount and sudo policy.
- Verification: two defining tests RED then GREEN; existing startup/pywal regression scripts passed. Actual host preview confirms the missing entry and sudo requires a password.
- Limitations: no privileged apply or fresh boot performed; wallpaper acceptance remains pending.
- Source: [UBS wallpaper startup](../../../../docs/postmortem/2026-10-20-ubs-wallpaper-startup.md).


## local-weather-epoch-hour-and-refresh

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: UTC hour flooring skips half-hour-zone current forecasts; mount-only dashboards keep stale data.
- Applicability: Hourly source selection with epoch timestamps and freshness-limited feeds in open browser tabs.
- Diagnostic checks: Reproduce Kolkata16:40 and execute the real page effect under a controlled clock/network/document lifecycle.
- Remedy: Select the latest supplied forecast instant at or before now. Refresh periodically and on visible-tab resume, prevent overlap, bound requests, clear expired data and clean up abort controllers/listeners/timers.
- Verification evidence: Reproductions RED,36 route+4 effect cases GREEN; typecheck/build passed. Deployment metadata and live API/desktop/mobile checked.
- Limitations: Controlled effect tests do not establish a ninety-minute unattended browser soak.
- Source: [Weather selection and refresh](/home/example/coding/scrape-weather/.worktrees/weather-app/docs/postmortem/2026-10-20-hour-selection-and-refresh.md) (SHA-256 `a70c4c1ebde8`; reviewed alias in [sources.json](../sources.json)).

## local-package-candidate-refresh

- Status: **verified_fix**; confidence: **confirmed**; verification scope: **code**.
- Symptoms: a successful Chrome upgrade is rejected against a candidate saved before apt update.
- Applicability: APT updaters comparing installed and repository versions.
- Diagnostics: simulate candidate advancement on metadata refresh, cached equality, newer installed versions and incomplete upgrades.
- Remedy: refresh before candidate selection/display and decision; re-read after installation; compare using dpkg Debian ordering and accept installed >= candidate. Label read-only cached checks explicitly.
- Verification: eleven updater cases and Bash syntax checks pass after RED. Live installed/candidate both156.0.8078.47-1; binary reports156.0.8078.47.
- Limits: no second privileged update or browser relaunch by the agent; configured repository availability and pinning determine the candidate.
- Source: [Chrome updater follow-up](../../../../docs/postmortem/2026-10-20-chrome-updater-silent-exit.md).

## local-ubs-repeat-without-shell-exports

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: UBS skips fast keyboard repeat without Fish exports.
- Applicability: i3 starts ubuntu-start directly before shell exports exist.
- Diagnostics: execute startup with missing, empty, partial and full repeat exports; inspect xset arguments and live X11 settings.
- Remedy: default absent/empty XSET_DELAY and XSET_RATE independently to 200/90; preserve overrides and the optional-command guard.
- Verification: defining regression RED then GREEN, four shell regressions and syntax passed; scoped refresh installed the correction; live checks confirmed defaults and partial/full overrides, restoring 200/90.
- Limitations: fresh i3 login and physical typing remain untested; requested rate 60 reports 62 on this server, so compare command arguments separately from effective rates.
- Source: [UBS keyboard repeat](../../../../docs/postmortem/2026-10-21-ubs-key-repeat.md).

## local-i3blocks-neighbor-theme-color

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms/applicability: i3blocks label differs from neighboring text despite inheriting the global default.
- Diagnostics: compare global bar color with neighboring helpers and wal color7.
- Remedy: use the same wallpaper theme color; preserve readable fallback if the palette is unavailable.
- Verification: defining RED, successful refresh and installed output #d0bce2 matching wal color7.
- Limitations: rendered screenshot comparison remains manual.
- Source: [Notis theme color](../../../../docs/postmortem/2026-10-21-notis-theme-color.md), SHA-256 `ce3b8711656b014f31a740873edebcd486fb92613b9082b676ebca0415130792`.

## local-vesktop-dm-notification-identity

- **status**: verified_fix
- **symptoms**: Discord sender-only direct messages display without speech.
- **applicability**: Dunst callbacks for the observed Vesktop desktop client.
- **diagnostics**: Inspect appname and nonblank title/body without printing message content; compare both Dunst route and parser.
- **confidence**: confirmed
- **remedy**: Route exact vesktop appname to the shared callback and allow nonblank visible sender/body when no channel suffix is present.
- **verification**: Unit RED/GREEN, isolated Dunst DM speech-only regression and installed synthetic WAV playback.
- **verification_scope**: runtime
- **limitations**: Appname is routing metadata, not authentication. Other clients need observed metadata. Non-message Vesktop notifications can also speak. Subjective listening and a new real incoming DM remain manual.
- **Report**: [2026-10-21-discord-dm-speech.md](../../../../docs/postmortem/2026-10-21-discord-dm-speech.md)

## local-scheduled-screensaver-visibility

- Status: verified_fix; confidence: confirmed; verification scope: runtime (isolated X11).
- Symptoms: the daily timer wakes displays successfully but playback ends within two seconds when browser coverage is absent; standard inactivity later blanks displays.
- Applicability: explicit scheduled X11 media playback beside conservative browser-gated idle activation.
- Diagnostics: inspect timer last-run, service-step status, preview lifetime, bridge availability and blanking/DPMS timeouts. Distinguish physical-input dismissal from successful duration acceptance.
- Remedy: use manual-preview policy for the explicit schedule, retain locked-session checks and idle safety, and hold connection-scoped XScreenSaverSuspend only during playback. Clear an already active server blank with XForceScreenSaver(ScreenSaverReset) after acquiring inhibition. Close/release in finally; never persistently disable global DPMS to hide the failure.
- Verification: eight timer and 58 broader tests passed. Isolated Xvfb verifies inhibition beyond the configured timeout, automatic blanking after exception cleanup and unchanged settings. Deployed sources matched; real playback entered three items but physical input ended duration probes.
- Limitations: real uninterrupted duration and next-morning hardware acceptance remain unobserved. Forced blanking and lockers retain control. Newly detected browser video or user input may dismiss playback.
- Source: [Morning blackout](../../../../docs/postmortem/2026-10-22-screensaver-morning-blackout.md); exact hash/alias in sources.json.

## local-discord-direction-isolates

- **status**: verified_fix
- **symptoms**: Discord channel/server metadata is spoken as part of the sender; browser channel notifications miss speech.
- **applicability**: Discord desktop notification titles containing Unicode direction isolates, including observed Vesktop metadata.
- **diagnostics**: Inspect title codepoints and app routing; U+2068 before # prevents the literal channel delimiter and triggers the Vesktop DM fallback.
- **confidence**: confirmed
- **remedy**: Remove U+2066–U+2069 before visible-text parsing; keep full suffix validation before speaking sender says message.
- **verification**: Unit83 and private Dunst1 pass after expected RED; type check0. Installed isolated Vesktop channel WAV1/MP3 0, both excluded bot probes silent. Source/live bytes match after refresh and activation.
- **verification_scope**: runtime
- **limitations**: Subjective listening and a new real incoming notification remain unobserved. Same-format apps can match; broader suite has unrelated socket and path-fixture failures.
- **Report**: [Discord direction isolates](../../../../docs/postmortem/2026-10-22-discord-direction-isolates.md)

## local-dunst-overlapping-audio-rules

- **status**: verified_fix
- **symptoms**: The same Vesktop channel notification is spoken twice.
- **applicability**: Dunst1.9.2 configurations with multiple matching script rules.
- **diagnostics**: Compare exact-client channel notifications against generic format fixtures; each matching rule invokes its script.
- **confidence**: confirmed
- **remedy**: Use one shared audio callback and classify in Python; avoid text deduplication that suppresses legitimate separate deliveries. Exclude normalized SaucyBot and Twitter Cap Bot senders from Discord speech.
- **verification**: Private daemon RED observed22 instead of21 playbacks. GREEN unit83/private daemon1/type0; installed Vesktop channel WAV1, excluded bots WAV0, no MP3.
- **verification_scope**: runtime
- **limitations**: Synthetic installed acceptance; subjective listening and next real incoming message remain manual. Global callback starts for unrelated displayed notifications but returns without playing.
- **Report**: [Discord speech and duplicate callbacks](../../../../docs/postmortem/2026-10-22-discord-direction-isolates.md)

## local-mpv-nonlinear-speech-volume

- **status**: verified_fix
- **symptoms**: Notification TTS dominates streaming audio; a linear percentage assumption makes attenuation too strong.
- **applicability**: Local Ryan notification speech played through mpv software volume.
- **diagnostics**: Compare live sink-monitor loudness and actual mpv-rendered PCM; silent per-stream captures do not establish silence.
- **confidence**: confirmed
- **remedy**: Use native mpv software gain only for speech WAVs, persist a validated0..100 setting atomically, and keep the user-selected75 default. Do not alter browser, system or intro-clip volume.
- **verification**: Actual rendering at100=-16.08LUFS and50=-34.13LUFS; installed set/query and one WAV at50 verified. User selected75 and confirmed replay.85 tests/type0; installed saved/fresh queries75 and source/live match after refresh.
- **verification_scope**: runtime
- **limitations**: Fixed gain cannot track future stream loudness. Exact Vole Twitch slider unavailable. Earlier broad suite retains unrelated socket/path-fixture failures.
- **Report**: [Discord speech volume calibration](../../../../docs/postmortem/2026-10-22-discord-direction-isolates.md)
