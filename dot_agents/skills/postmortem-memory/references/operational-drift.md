# Operational drift and resource limits

Use these reviewed findings to compare a failure with prior evidence. Check applicability and diagnostics before choosing a remedy; keep its verification scope and limits explicit.

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
