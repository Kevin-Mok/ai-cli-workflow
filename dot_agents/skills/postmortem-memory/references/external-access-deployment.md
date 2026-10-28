# External access and deployment

Use these reviewed findings to compare a failure with prior evidence. Check applicability and diagnostics before choosing a remedy; keep its verification scope and limits explicit.

## local-new-branch-push-transport

- Status: **verified_workaround**; root-cause confidence: **supported**; verification scope: **workaround**.
- Symptoms: SSH closes during a new feature branch's all-history pre-push scan.
- Applicability: Authorized feature delivery from an already-published base with this gate behavior.
- Diagnostic checks: Verify remote base/ref state and the hook's exact outgoing range; distinguish active scan progress from transport success.
- Remedy: Initialize only the authorized feature ref at its verified public base, then push normally with all hooks enabled.
- Verification evidence: Normal retry passed the outgoing-history privacy gate and exited 0; PR #4 opened from the feature branch.
- Limitations: Exact SSH timeout cause is unproved; no scanner or SSH fix. Never bypass findings or publish unpublished content through ref initialization.
- Sources:
  - [Alpha intro push transport](../../../../docs/postmortem/2026-10-28-alpha-intro-push-transport.md) (current reviewed hash and alias in [sources.json](../sources.json)).


## ext-compose-ansible-local-readiness

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Compose service refers to undefined network private; Ansible config file = None; shared variables outside normal discovery; secret template diffs unprotected
- Applicability: Staging Compose/Ansible definitions extending production and deploying alongside existing services.
- Diagnostic checks: Validate production and staging definitions separately with synthetic environment values.; Inspect effective Ansible config/inventory/shared-variable discovery.; Check Vault/local ignore rules and secret-diff protection.; Verify occupied ports and existing service snapshots before isolated rehearsal.
- Remedy: Provide staging top-level networks/volumes, explicit wrapper configuration/shared vars, encrypted Vault inputs and protected secret templates; use an existing-host deployment path that preserves current services.
- Verification evidence: Real Ansible/Compose tests passed; two isolated Ubuntu VM deployments verified HTTP/database persistence and full restore while existing PIDs/configuration stayed unchanged.
- Limitations: The real VPS was unchanged and blocked on unsupported OS. VM rehearsal is runtime evidence for the isolated fixture, not production activation.
- Sources:
  - [2026-10-02-staging-infrastructure-readiness.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-02-staging-infrastructure-readiness.md) (SHA-256 `e5094af323a6`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-interactive-sudo-boundary

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: sudo: a terminal is required to read the password; non-interactive apt installation cannot authenticate
- Applicability: System package installation requiring local interactive sudo credentials.
- Diagnostic checks: Distinguish missing authentication from absent package or failed hosting access.; Inspect whether the requested tool is already installed before retrying.
- Remedy: Have the authorized operator perform the installation in an authenticated local terminal; then verify the resulting executable and access. Preserve a rollback snapshot before remote edits.
- Verification evidence: The operator installed FileZilla, authenticated to hosting and downloaded a complete web-root snapshot without remote changes.
- Limitations: A successful hosting connection does not establish host PHP/mail, database, SSH or backup capabilities; audit those separately.
- Sources:
  - [2026-08-25-filezilla-install-authentication.md](/home/example/coding/example-client-app/docs/postmortem/2026-08-25-filezilla-install-authentication.md) (SHA-256 `cdd24288f220`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-mail-handoff-not-delivery

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: PHP mailSent true but inbox empty; relay HTTP 200 and backupSaved true; missing final SMTP/queue/bounce visibility
- Applicability: Notifications handed to a shared host's PHP mail transport after durable application persistence.
- Diagnostic checks: Separate database commit, relay authentication, private backup, mail handoff and final mailbox receipt.; Capture an exact test attempt for host trace or mailbox-owner confirmation.; Check protected configuration/backup URLs without revealing the underlying files.
- Remedy: Keep the durable database queue as the explicit manual follow-up path; obtain final recipient confirmation or host message-level trace before declaring delivery. A monitored provider or DNS/sender migration requires its own authorization.
- Verification evidence: Controlled Production lead/event persistence and protected relay handoff/backup were observed; final Gmail/Outlook receipt remained unconfirmed even after direct HTTP 200 diagnostics.
- Limitations: PHP mail acceptance and public SPF/DMARC records do not prove inbox delivery. File-transfer access cannot inspect mail queues. This report explicitly remains an operations readiness hold.
- Sources:
  - [2026-09-02-preview-php-relay-email-missing.md](/home/example/coding/example-client-app/docs/postmortem/2026-09-02-preview-php-relay-email-missing.md) (SHA-256 `2b0de67829ce`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-release-source-verification

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: Ubuntu community upgrade wiki HTTP 503; assumed old-releases archive path 404; EOL status incorrectly implies archive moved
- Applicability: Preparing EOL operating-system recovery when community documentation is unavailable.
- Diagnostic checks: Read current official release metadata and accessible source endpoints.; Verify upgrader package signatures against the established archive keyring.; Preserve release codenames and distinguish package availability from a successful upgrade rehearsal.
- Remedy: Use current official announcements/metadata and verified signed upgrader packages as fallback evidence; test actual archive endpoints rather than inferring relocation from EOL status.
- Verification evidence: Official release metadata remained accessible and independent research verified both destination upgrader signatures; archive endpoints were tested without upgrades.
- Limitations: No whole-host recovery or release upgrade was performed; accessible tools are not proof of safety or success on the target host.
- Sources:
  - [2026-10-04-vps-recovery-implementation.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-04-vps-recovery-implementation.md) (SHA-256 `db3fcc8d0ae1`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-supabase-network-fallback

- Status: **unresolved**; root-cause confidence: **supported**; verification scope: **none**.
- Symptoms: Supabase db query ECONNREFUSED over IPv6; allowlisting does not resolve refusal; inferred pooler hostname ENOTFOUND; DNS preflight filters connection candidates
- Applicability: Historical direct database verification blocked by IPv6 reachability or uncertain pooler endpoint.
- Diagnostic checks: Inspect address family and connection failure without exposing credential-bearing URLs.; Obtain the actual project pooler connection string rather than inventing hostname formats.; Separate name resolution, network restrictions and database authentication.
- Remedy: Try the known supported IPv4/pooler endpoint with required TLS; do not eliminate explicitly configured candidates solely from an inconclusive DNS preflight; report attempted sanitized hosts.
- Verification evidence: Reports document the errors and fallback implementations, but neither records a successful completed retry.
- Limitations: Candidate retry is not proof of connectivity or persisted rows. Keep credentials out of logs; current provider connection options need fresh verification.
- Sources:
  - [2026-08-10-supabase-check-lead-hostname-resolution-fallback.md](/home/example/coding/example-client-app/docs/postmortem/2026-08-10-supabase-check-lead-hostname-resolution-fallback.md) (SHA-256 `6dd26b19cf86`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-08-10-supabase-check-lead-ipv6-refused.md](/home/example/coding/example-client-app/docs/postmortem/2026-08-10-supabase-check-lead-ipv6-refused.md) (SHA-256 `78654b240d3c`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-vercel-authentication

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: vercel deploy Not authorized; No existing credentials found; Git push succeeds but Preview URL unavailable
- Applicability: Vercel CLI sessions without project-authorized credentials.
- Diagnostic checks: Check linked project and session authentication without printing tokens.; Resolve deployment status/URLs independently of Git push success.
- Remedy: Authenticate through the approved account/device flow and retry the intended deployment, then record actual deployment URLs/statuses.
- Verification evidence: Deployment and lookup returned authentication errors; the device flow was cancelled and no new Preview URL was obtained.
- Limitations: Do not infer deployment from a successful push; no Production environment, DNS or database changes were made.
- Sources:
  - [2026-10-02-vercel-deployment-authentication.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-02-vercel-deployment-authentication.md) (SHA-256 `01b1b6993e7c`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-authenticated-destination-review

- Status: **activation_pending**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: automatic approval rejects push because remote trust not established
- Applicability: Explicitly authorized push whose configured destination ownership is not yet supported by session evidence.
- Diagnostic checks: Read authenticated account identity and repository owner/permissions.; Confirm configured remote matches the owned repository.
- Remedy: Supply read-only ownership and push-permission evidence, then retry ordinary reviewed push without changing destination or bypassing controls.
- Verification evidence: Authenticated API identity, repository ownership and admin/push permission reads succeeded.
- Limitations: This report stops before the remaining push. Destination trust is verified; successful publication is not recorded here.
- Sources:
  - [2026-10-04-kitty-session-push-review.md](/home/example/linux-config/docs/postmortem/2026-10-04-kitty-session-push-review.md) (SHA-256 `3f361eba4c2c`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-chezmoi-executable-attribute

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: installed script permission denied despite Git execute bit; executable- prefix does not install executable mode
- Applicability: ChezMoi source naming for command deployment.
- Diagnostic checks: Inspect installed mode, source mapping and source attribute spelling.; Test a real isolated ChezMoi apply rather than only checkout execution.
- Remedy: Use executable_ with underscore in the source filename, preserve content and update references.
- Verification evidence: Isolated apply was RED before rename and GREEN afterward; 24 tests passed; refresh completed; installed PATH --help worked with matching bytes and executable mode.
- Limitations: Git source mode and a hyphen spelling are insufficient for installed ChezMoi attributes.
- Sources:
  - [2026-09-19-yt-dl-chezmoi-executable.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-19-yt-dl-chezmoi-executable.md) (SHA-256 `b209bbc732a5`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-current-source-retrieval

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: documentation schema urllib HTTP 404; legacy GitHub source module path moved; search-indexed skill directory returns 404; strict-config flag unsupported on features command
- Applicability: Public technical source research and installed-version config investigation.
- Diagnostic checks: Enumerate current upstream tree and follow official redirects.; Use installed CLI generated protocol schemas or offline probes when source path guessing fails.; Validate command-specific supported flags.
- Remedy: Use current primary source paths and real installed runtime evidence; do not infer configuration controls from stale examples or failed source guesses.
- Verification evidence: Official redirected schema/current modules were readable and installed CLI generated schemas; current upstream tree and local sources were successfully inspected.
- Limitations: A 404 does not prove capability absence. Online main source may differ from the installed pin; identify that limit.
- Sources:
  - [2026-10-03-metaprompt-runtime-source-fetch.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-runtime-source-fetch.md) (SHA-256 `8b15b73373e7`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-metaprompt-source-discovery.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-source-discovery.md) (SHA-256 `ebb2cc3948bd`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-endpoint-empty-probe-handling

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: ssh host-key scan empty on default port; ssh-keygen receives empty input and errors
- Applicability: SSH endpoint diagnosis on a documented nondefault port.
- Diagnostic checks: Confirm documented endpoint/port first.; Handle no-output/timeouts before piping to identity parsers.
- Remedy: Probe the intended port and compare returned host fingerprint; do not conclude endpoint identity from empty default-port output.
- Verification evidence: Documented port probe returned the matching fingerprint and read-only service/connectivity checks succeeded.
- Limitations: This proves that observed endpoint fingerprint at the inspected port, not universal public reachability or login authorization.
- Sources:
  - [2026-10-03-phone-ssh-diagnostic-shell-startup.md](/home/example/linux-config/docs/postmortem/2026-10-03-phone-ssh-diagnostic-shell-startup.md) (SHA-256 `013ed9b04134`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-installed-downloader-routing

- Status: **verified_fix**; root-cause confidence: **supported**; verification scope: **runtime**.
- Symptoms: normal yt-dl remains HTTP 403 after isolated test succeeded; PATH resolves obsolete installed yt-dlp
- Applicability: A dependency repair tested only in a temporary runtime while normal PATH still selects the old executable.
- Diagnostic checks: Compare command -v and --version for normal invocation versus test environment.; Confirm explicit JavaScript runtime support under wrapper config isolation.
- Remedy: Update the active installed dependency through its supported updater; verify the unchanged wrapper with the original input and enable supported runtime explicitly when ambient config is ignored.
- Verification evidence: Installed updater resolved the same URL; ffprobe verified 4K audio/video and close duration; later automatic extraction verification passed without JavaScript warnings.
- Limitations: No full decode was done in this installed-version incident. The precise extractor change remains unisolated; metadata verification is bounded.
- Sources:
  - [2026-09-19-yt-dlp-installed-version.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-19-yt-dlp-installed-version.md) (SHA-256 `c49a07a07687`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-mixed-camera-command-activation

- Status: **activation_pending**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: filename lexical order reverses actual capture order; mixed SDR/HLG stream copy emits DTS and decoder errors
- Applicability: Repository concat helper joining Pixel timestamp names and iPhone capture-metadata names.
- Diagnostic checks: Order Pixel by encoded timestamp and iPhone by usable creation_time.; Compare stream compatibility and use a short decoded real sample.
- Remedy: Select intended inputs explicitly and use the implemented reencode path to normalize mixed SDR/HLG clips while preserving source files.
- Verification evidence: Defining ordering and missing-reencode tests were RED; report points final focused/integration evidence to its plan.
- Limitations: This report leaves a full-length render and playback review manual. It does not itself record completed live full-helper activation; the separate repaired artifact incident does not prove every future helper run.
- Sources:
  - [2026-09-28-mixed-camera-concat.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-28-mixed-camera-concat.md) (SHA-256 `7765d3eb1d4b`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-temporary-downloader-update

- Status: **verified_workaround**; root-cause confidence: **supported**; verification scope: **workaround**.
- Symptoms: YouTube media HTTP 403 with obsolete extractor or SABR warnings
- Applicability: A live download checker using an old yt-dlp dependency.
- Diagnostic checks: Locate and version the executable actually used.; Retest with a current isolated dependency without altering user installation.; Probe streams/duration and decode the retained artifact when integrity is needed.
- Remedy: An isolated current yt-dlp runtime can establish whether the old extractor is implicated without cookies or system-package changes.
- Verification evidence: Isolated update completed the download, matched source duration and ID, retained audio/video and passed full decode.
- Limitations: The exact upstream extraction difference was not isolated; installed user dependency remained old after this workaround. Missing JavaScript runtime can still hide formats.
- Sources:
  - [2026-09-18-yt-dl-live-download.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-18-yt-dl-live-download.md) (SHA-256 `7992a59ace1f`; 2 alias(es), all retained in [sources.json](../sources.json)).
