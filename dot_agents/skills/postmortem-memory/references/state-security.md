# State and security boundaries

Use these reviewed findings to compare a failure with prior evidence. Check applicability and diagnostics before choosing a remedy; keep its verification scope and limits explicit.

## ext-csp-safe-browser-probe

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: wait_for_function string predicate blocked; unsafe-eval disallowed by Content Security Policy
- Applicability: Playwright probes against pages with a strict production CSP.
- Diagnostic checks: Determine whether the failing evaluator is part of the harness rather than the application.; Keep independent console, HTTP and external-request checks.
- Remedy: Use locator assertions to wait for control state; retain the strict CSP.
- Verification evidence: Corrected integrated browser probe completed search/context paging and attachment download with empty console/HTTP/external-request failures; CSP unchanged.
- Limitations: This verifies the corrected probe path; avoid relaxing CSP to satisfy a harness helper.
- Sources:
  - [2026-10-04-browser-csp-probe.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-browser-csp-probe.md) (SHA-256 `5cfb990b3e57`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-gitea-abuse-exposure

- Status: **verified_workaround**; root-cause confidence: **supported**; verification scope: **runtime**.
- Symptoms: new Gitea PID immediately CPU-heavy; junk unauthenticated route traffic; slow SQL and indexer cancellation under abuse
- Applicability: A personal Gitea instance where public registration/browsing is unnecessary during recovery.
- Diagnostic checks: Audit service access settings and logs for abusive route patterns.; Separate observed abuse reduction from hypotheses about SQLite amplification.
- Remedy: Disable unnecessary registration and OpenID signup, require sign-in for viewing when that matches the service's intended audience, then restart under the authorized operational scope.
- Verification evidence: The live access restrictions stopped the abusive expensive-route traffic and the service became responsive without an Nginx change.
- Limitations: Restricting browsing changes public access and is not a universal remedy for public forges. Database amplification remains a supported theory; PostgreSQL migration and upgrade were follow-ups, not completed fixes.
- Sources:
  - [2026-03-18-gitea-spam-induced-latency.md](/home/example/coding/fixes/docs/incidents/2026-03-18-gitea-spam-induced-latency.md) (SHA-256 `0739ee9baaa9`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-locked-authorization-deadline

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: reset confirmation expires while awaiting quota lock; moderator permission revoked during queued mutation; pre-lock authorization allows stale reset
- Applicability: Queued privileged mutations whose authorization/deadline can change during lock waits.
- Diagnostic checks: Hold the mutation lock, queue a request, expire its deadline or revoke permission, then release.; Fetch current member roles and effective permissions at the point of mutation.
- Remedy: Recheck original deadline and current permissions inside the same lock immediately before mutation; use the locked returned prior value for queued feedback.
- Verification evidence: Expected failing reproductions preceded correction; final 51 tests and Pyright passed.
- Limitations: Development used no live Discord server. Runtime activation and real command smoke checks remain separate.
- Sources:
  - [2026-10-02-reset-confirmation-queue.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-02-reset-confirmation-queue.md) (SHA-256 `255ebb927c01`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-retryable-adapter-and-schema-check

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: OSError ends status/midnight worker; failed worker prevents shutdown; malformed SQLite schema passes --check; channel dereference before ready
- Applicability: Long-running Discord adapters with persisted counters and asynchronous startup/shutdown.
- Diagnostic checks: Inject HTTP/OSError/TimeoutError/client transport failures.; Validate actual SQLite columns, integrity, ID types and counter consistency.; Test pre-ready calls and shutdown after worker failure.
- Remedy: Normalize expected transport failures into retryable adapter outcomes, guard unset channels, shut down safely after failed workers, and validate persisted structure/data before reporting success.
- Verification evidence: Each recovery/schema/readiness reproducer was RED before correction; 30 tests passed and Pyright reported zero errors/warnings.
- Limitations: No real live Discord testing occurred; documented outage/atomicity limits remain. Code verification is not process activation.
- Sources:
  - [2026-10-02-adapter-verification.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-02-adapter-verification.md) (SHA-256 `7981990b082b`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-runtime-root-ownership-boundary

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: runtime destination rejects shared /tmp ancestor; repeat rehearsal changes generated credentials; credential-preservation guard correctly refuses redeployment
- Applicability: Temporary isolated deployment fixtures with protected reusable credentials and runtime directories.
- Diagnostic checks: Scope ownership checks within the workflow-owned runtime root.; Keep symlink rejection for every ancestor.; Reuse a mode-protected state directory for repeated harness invocations.
- Remedy: Enforce ownership only on owned runtime destinations while retaining ancestor symlink checks; reuse protected saved credentials across repeated rehearsals.
- Verification evidence: Host regressions and real Ubuntu rehearsal passed after correcting the boundary and state-dir handling; full infrastructure suite passed.
- Limitations: Do not weaken credential-preservation or other-writers guards to satisfy a fixture; shared ancestors may be valid while owned destinations still require strict controls.
- Sources:
  - [2026-10-04-vps-workflow-inspection.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-04-vps-workflow-inspection.md) (SHA-256 `409c6dd1137b`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-vps-recovery-implementation.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-04-vps-recovery-implementation.md) (SHA-256 `db3fcc8d0ae1`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-safe-error-correlation

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Preview lead submission 500 without reference; raw Supabase error exposed to browser; configuration errors differ by route
- Applicability: Server routes persisting sensitive lead/attribution data and browser support flows.
- Diagnostic checks: Audit each branch for stable codes and request IDs.; Compare deployment environment variables to actual failing route configuration.; Correlate browser reference to structured server logs without logging personal inputs.
- Remedy: Use a shared safe error contract with stable codes and UUID references; log route/status/code/reference only. Correct missing server configuration and test persistence independently of notifications.
- Verification evidence: Sixteen focused tests and build passed; protected Preview and Production submissions later created matching lead/conversion rows and normal success state.
- Limitations: The full suite/typecheck/lint initially remained blocked by a pre-existing truncated test file; successful controlled data-path checks do not establish email delivery.
- Sources:
  - [2026-08-17-preview-lead-submission-diagnostics.md](/home/example/coding/example-client-app/docs/postmortem/2026-08-17-preview-lead-submission-diagnostics.md) (SHA-256 `552f9e8c9851`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-snapshot-consistency-durability

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: relevance cursor stale during ingestion; successful media rename lacks directory fsync; queued channel starts after authentication failure
- Applicability: Concurrent readers and durable file/database operations.
- Diagnostic checks: Test relevance cursors across an ingestion revision.; Inject directory fsync and integrity failures.; Queue work behind terminal authentication failure.
- Remedy: Bind relevance cursors to transaction-consistent message revisions; fsync media directory entries before committing success; stop queued channel work after terminal authentication failure.
- Verification evidence: Expected regressions preceded narrow fixes; final 97 backend tests plus lint/mypy passed.
- Limitations: SQLite success does not itself prove renamed file entries survived power loss; filesystem durability checks must be explicit.
- Sources:
  - [2026-10-04-review-findings.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-review-findings.md) (SHA-256 `cc3fd381068a`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-snapshot-persisted-paths

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: snapshot path traversal through persisted ../ path; manifest claims complete despite missing attachments
- Applicability: Backup/snapshot exporters using persisted relative paths and attachment availability state.
- Diagnostic checks: Resolve and validate source containment and destination containment independently.; Test malformed persisted paths and queued/failed media.; Compare manifest completeness to every known attachment.
- Remedy: Use normalized constrained paths for both source and destination; include every known attachment in the manifest and exit nonzero for missing media.
- Verification evidence: Reviewer reproduced traversal; expected RED regressions preceded fixes; final 97 backend and nine browser tests passed.
- Limitations: These regressions used synthetic data. Source containment alone never guarantees safe destination construction.
- Sources:
  - [2026-10-04-review-findings.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-review-findings.md) (SHA-256 `cc3fd381068a`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-transactional-migration-validation

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: migration commits before validation; SQLite comparison accepts text IDs; rejected migration leaves schema partially changed
- Applicability: Persisted schema migrations and stored identifier validation.
- Diagnostic checks: Inject rejected migration and compare prior schema version, columns and data.; Check stored SQLite types rather than relying on coercive comparisons.
- Remedy: Wrap DDL, schema version changes and validation in one explicit transaction; require integer types for stored override IDs and reject malformed data actionably.
- Verification evidence: Rejected-v1 migration and malformed-ID regressions were RED then GREEN; 51 tests and Pyright passed.
- Limitations: Test validation does not establish migration of a live user's database; preserve backup and rollback scope.
- Sources:
  - [2026-10-02-reset-confirmation-queue.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-02-reset-confirmation-queue.md) (SHA-256 `255ebb927c01`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-benchmark-host-context-guard

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: benchmark receives global AGENTS despite discovery-disabled flags; installed skill auto-injection contaminates candidate context
- Applicability: Isolated Codex CLI evaluation harness with explicitly excluded host instruction context.
- Diagnostic checks: Use zero-permit probes to inspect wrapper metadata without saving instruction bodies.; Recognize exact AGENTS and separate installed-root skill envelopes.; Keep guards for unknown framing and preserve supplied candidate/task content.
- Remedy: Apply disclosed symmetric host-context removal only to recognized user fragments; record counts/names rather than bodies and fail closed on remaining contamination.
- Verification evidence: Zero-permit probes reached budget gate without upstream calls; boundary regressions passed and all 14 held-out pairs later ran with no infrastructure errors.
- Limitations: This is an explicitly isolated benchmark adaptation, not permission to strip normal repository instructions. Runtime framing is version-sensitive.
- Sources:
  - [2026-10-03-metaprompt-benchmark-trial-infrastructure.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-benchmark-trial-infrastructure.md) (SHA-256 `8e4453378c36`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-browser-source-process-identity

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: artist metadata admits YouTube uploader as song; different Chrome profiles share MPRIS owner; proc cmdline arrives as one space-separated entry
- Applicability: Selecting one browser application while excluding other sites that omit source URLs.
- Diagnostic checks: Compare actual D-Bus owner/PID for the intended and unwanted source.; Verify separate --user-data-dir, not only profile picker identity.; Test both NUL-tokenized and rewritten single-entry proc command lines.
- Remedy: Launch a dedicated user-data directory, resolve the live MPRIS owner to its process and require the exact directory for selection and controls; preserve Spotify fallback.
- Verification evidence: 33 media tests and launcher regression passed; sign-in/playback established independent owner/process; installed helper rendered the intended dedicated source.
- Limitations: Sites within the dedicated process remain indistinguishable; reserve it for the intended player. Live YouTube-playing/FlaviBot-paused separation was fixture-covered, not observed at final deployment.
- Sources:
  - [2026-09-20-youtube-media-filter.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-20-youtube-media-filter.md) (SHA-256 `b4c0cf347c97`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-displayed-owner-control-binding

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: bar displays wrong player while browser track is active; cache write failure retains old click target; unresponsive browser hides healthy fallback
- Applicability: MPRIS status selection and click controls across multiple players.
- Diagnostic checks: Inspect structured live metadata and playback status.; Reproduce cache-write failure, stale identity and unresponsive-source cases.; Bind controls to last rendered unique owner and recheck current capabilities.
- Remedy: Prefer eligible playing tracks with a deterministic tie rule, read healthy fallback before potentially hanging calls, clear obsolete click state on cache failure, and require consumed display state plus current owner/capability validation before controls.
- Verification evidence: 24 new regressions and existing desktop checks passed; installed helper matched source and live rendering selected the actually playing browser over paused Spotify.
- Limitations: No live playback controls were sent; clicks/transitions were fixture-tested. MPRIS checks and actions are not atomic; a browser may retain stale paused metadata.
- Sources:
  - [2026-09-19-flavibot-now-playing.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-19-flavibot-now-playing.md) (SHA-256 `1fa8a032a220`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-fail-safe-test-transport

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: expected local 403 instead receives official HTTP 401 during RED; test accidentally sends unauthenticated network request
- Applicability: Proxy safety-boundary tests before the rejecting feature exists.
- Diagnostic checks: Inject fake upstream unconditionally, including expected local-rejection cases.; Prohibit real transport suite-wide.
- Remedy: Make the reproducer incapable of public network regardless of absent/regressed guard; preserve and conservatively account for the unintended attempt.
- Verification evidence: Fake-only RED demonstrated missing guard without network; subsequent guard tests passed with real upstream forbidden.
- Limitations: No model output was observed for the unintended 401, and server-side execution/billing was not independently known. A guard under test is not sufficient test isolation.
- Sources:
  - [2026-10-03-runtime-red-test-uninjected-upstream.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-runtime-red-test-uninjected-upstream.md) (SHA-256 `105198976749`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-ignored-merge-collision-preflight

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Git ort merge overwrites ignored file despite --no-overwrite-ignore; literal bracket ignore pattern is not actually ignored
- Applicability: Git helpers protecting local ignored data during non-fast-forward merges and cleanup.
- Diagnostic checks: Verify ignored fixtures with git check-ignore, including literal glob escaping.; Compare NUL-separated ignored paths with computed incoming merge paths, including file/directory and directory-rename collisions.
- Remedy: Preflight ignored-data collisions explicitly before merging, retaining Git protection flag as a second check; preserve unrelated ignored directories and real conflict resolve/abort behavior.
- Verification evidence: Git 2.43.0 disposable reproducer overwrote ignored file with the flag; seven protection regressions and all 32 tests passed after explicit preflight.
- Limitations: The flag alone is insufficient for the demonstrated strategy/version. Do not reject every ignored path or create/merge a worktree without authorization.
- Sources:
  - [2026-10-05-worktree-ignored-merge-safety.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-05-worktree-ignored-merge-safety.md) (SHA-256 `316458264532`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-intentional-capture-target-apply

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: refresh snapshots live config then prompts to overwrite same target; chezmoi persistent lock while original interactive process remains; blank Git helper assignments cause whitespace failure
- Applicability: A refresh intentionally captures live Codex/Git configuration before an otherwise protected broad apply.
- Diagnostic checks: Inspect the exact target named by ChezMoi and existing interactive process.; Validate the captured diff and normalize only semantically blank helper assignments.
- Remedy: Force-apply only each intentionally captured managed target, then leave the broad apply unforced for unrelated conflicts.
- Verification evidence: Focused regression was RED/GREEN; a live refresh completed snapshots, exact applies, broad apply, shortcut sync and Fish reload without prompts; captured Git whitespace check passed.
- Limitations: Never generalize exact-target force to the full apply. Protected dirty-source ownership still requires preflight.
- Sources:
  - [2026-08-17-refresh-config-snapshot-prompt.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-17-refresh-config-snapshot-prompt.md) (SHA-256 `a019916583c5`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-ledger-invalid-link-diagnostic

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: argument of type NoneType is not iterable; malformed sources null hides finding field diagnostic
- Applicability: Persisted JSON with malformed source or finding link lists
- Diagnostic checks: Inject null or non-string link fields in a temporary ledger; Read complete structured errors, not just the nonzero exit
- Remedy: Validate field types and guard reciprocal-link membership before using malformed values; retain actionable finding and field errors.
- Verification evidence: Each defining temporary-fixture regression failed for the expected gap, then all 24 helper tests passed after minimal fixes; corrected discovery found no additional old reports.
- Limitations: Schema checks cannot establish that human-authored prose or source claims are true.
- Sources:
  - [2026-10-05-postmortem-memory-coverage-review.md](/home/example/linux-config/docs/postmortem/2026-10-05-postmortem-memory-coverage-review.md) (SHA-256 `65b00c1d9bc4`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-scoped-fixture-mcp-approval

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: MCP tool call requires approval but approval policy is never; fixture trace empty after requests spent
- Applicability: Authorized isolated benchmark fixture MCP under never-approval global policy.
- Diagnostic checks: Check actual per-tool approval behavior with synthetic CLI responses.; Separate infrastructure failure from candidate-quality failure and retain every charge.
- Remedy: Approve only the named fixture read/write/list tools and keep the exact enabled-tools allowlist, native filtering and disabled host; detect repeated approval failure before another permit.
- Verification evidence: Actual installed-CLI synthetic integration probe executed confined fixture reads/writes with zero remote/model calls; boundary tests passed; subsequent held-out execution had zero infrastructure errors.
- Limitations: This approval setting applies only to the controlled fixture, not arbitrary MCP tools. The original failed attempts stayed archived and charged.
- Sources:
  - [2026-10-03-metaprompt-benchmark-trial-infrastructure.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-benchmark-trial-infrastructure.md) (SHA-256 `8e4453378c36`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-quota-reset-chronological-replay

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Old reset cohort returns after manual reset and bridges work across the reset.; Raw latest stale quota reading overstates remaining allowance.
- Applicability: Allowance-report replay joining account-wide quota snapshots to counted working time across manual resets.
- Diagnostic checks: Replay A, B, stale A chronological reset sequence; assert no elapsed-work duplication.; Replay rising used-percent followed by a stale lower reading; compare latest to accepted evidence.; Record distinct reset identities at one timestamp; verify conflict excludes attribution instead of relying on sort order.
- Remedy: Replay chronological reset retirement; ignore stale returns and choose latest from accepted non-stale evidence. Group each stream timestamp before retirement: conflicting same-timestamp reset identities clear pair baselines and add explicit quality. Preserve jitter and gap exclusions.
- Verification evidence: Three defining counterexamples failed intentionally before their corrections; 15 focused tests and final 101-test suite passed, with mypy 16 modules, Ruff/build and 47 smoke checks green.
- Limitations: Checks cover sanitized local fixtures; quota remains account-wide and model mix cannot identify intrinsic model cost. Live installation is a separate verification.
- Sources:
  - [2026-10-06-burn-reset-cohort-review.md](/home/example/coding/track-codex-sessions/docs/postmortem/2026-10-06-burn-reset-cohort-review.md) (SHA-256 `7301d78866bb`; 1 alias retained in [sources.json](../sources.json)).

## local-recap-cache-concurrent-lifecycle

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Concurrent clear aborts reads, lock contention leaves stale generating state, or interrupted atomic writes block maintenance.
- Applicability: Asynchronous local recap caches with concurrent read/maintenance/generation.
- Diagnostic checks: Delete between exists/read, release a competing lock without a save, and leave a safe atomic temporary file after writer termination.
- Remedy: Treat disappearing files as missing, reconcile lock liveness without consuming attempts, and clean owned regular atomic temporaries under the maintenance lock. Preserve lock inodes and reject unsafe paths.
- Verification: All three defining cases observed RED; 17 recap, seven picker and eight recent CLI tests pass, with active-inference index-lock and cancellation checks.
- Limitations: Synthetic subprocess coverage is not provider availability evidence.
- Source: [Recent cache races](../../../../docs/postmortem/2026-10-07-codex-recent-cache-races.md).

## local-inherited-environment-assertion-output

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: unittest assertion prints a whole inherited environment, including credential-bearing values.
- Applicability: tests or diagnostics whose assertion operands include sensitive mappings.
- Diagnostic checks: inspect failure formatting; use synthetic cleared fixture environments and safe variable-name-only reporting.
- Remedy: use `patch.dict(..., clear=True)` for the fixture environment and boolean membership assertions, then record any actual disclosure without values and inform the user.
- Verification evidence: all seventeen runtime tests passed after fixture hardening; no environment dump was written to repo artifacts or a separate temporary log.
- Limitations: this prevents recurrence in the fixture but cannot erase transcript exposure. Credential rotation was not attempted or verified.
- Sources:
  - [2026-10-07-codex-recap-runtime-probe.md](/home/example/linux-config/docs/postmortem/2026-10-07-codex-recap-runtime-probe.md) (SHA-256 `85c19fb97675`; see [sources.json](../sources.json)).
