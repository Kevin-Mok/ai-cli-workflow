# Paths and ownership

Use these reviewed findings to compare a failure with prior evidence. Check applicability and diagnostics before choosing a remedy; keep its verification scope and limits explicit.

## ext-container-host-ownership

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: host API 500 reading root-owned vault index; root:root mode 0600 local-data; EACCES npm install or next build
- Applicability: Container/root processes writing bind-mounted runtime data or host frontend artifacts.
- Diagnostic checks: Inspect owner and permissions on failing data/build paths.; Compare container UID/GID to the host operator.; Preflight host readability/writability before server startup.
- Remedy: Run shared-data writers with the host UID/GID; scope an ownership repair to known affected runtime/build trees and provide an early actionable error.
- Verification evidence: Report records the causal permissions and changed Compose UID/GID/startup preflight, but no completed verification command evidence.
- Limitations: Historical defaults of 1000:1000 do not fit every host. Ownership repair needs correct scope and privileges; never recursively change unrelated source/home trees.
- Sources:
  - [2026-05-28-docker-start-app-local-parity.md](/home/example/coding/example-project-2/docs/postmortems/2026-05-28-docker-start-app-local-parity.md) (SHA-256 `3369dd68289c`; 5 alias(es), all retained in [sources.json](../sources.json)).

## ext-missing-shared-feedback-path

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: canonical feedback log path absent in another repository; no project tasks/lessons.md; inherited instructions assume linux-config-relative paths
- Applicability: Shared Codex instructions used from repositories without the Linux configuration repository layout.
- Diagnostic checks: Locate the actual canonical feedback store separately from the active repository.; Check whether project-specific lessons exist and create only within authorized scope.
- Remedy: Use the real shared canonical history rather than inventing substitute preferences; surface an unavailable authoritative source before dependent decisions. Keep repo-specific lessons local.
- Verification evidence: The report records creation of local lessons, but the shared feedback-path instruction gap remains unresolved.
- Limitations: An absent local file never proves there are no durable user preferences. Current canonical routing can later supersede the historical path rule.
- Sources:
  - [2026-09-02-relay-rollout-workflow-context.md](/home/example/coding/example-client-app/docs/postmortem/2026-09-02-relay-rollout-workflow-context.md) (SHA-256 `1495be749834`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-open-workbook-snapshot

- Status: **verified_workaround**; root-cause confidence: **supported**; verification scope: **workaround**.
- Symptoms: load_document returned None; AttributeError on doc.Sheets; original workbook open in GUI LibreOffice
- Applicability: Migration of a saved XLSX currently open in another LibreOffice process.
- Diagnostic checks: Check the load result before dereferencing it.; Inspect lockfile and active office processes without modifying the open artifact.; Hash the original before and after migration.
- Remedy: Copy the saved file to a private migration snapshot, load that copy, and export a separate deliverable.
- Verification evidence: Migration exited 0 with zero formula errors; 19 tests passed before final copy polish; original remained unchanged.
- Limitations: The open-file interaction is supported by lock/process evidence, not an exhaustive office-runtime diagnosis. The snapshot does not include unsaved GUI changes.
- Sources:
  - [2026-10-05-workbook-load-returned-no-document.md](/home/example/coding/codex-usage/docs/postmortem/2026-10-05-workbook-load-returned-no-document.md) (SHA-256 `4601b6d2bdf8`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-optional-path-discovery

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: No such file or directory for tests/conftest.py; missing .agent/PLANS.md; assumed archive/cli.py or pyproject.toml absent; working directory does not yet exist
- Applicability: Fresh repositories, parallel implementation outputs and inherited workflow paths.
- Diagnostic checks: Use rg --files or existence checks before naming optional files.; Coordinate completion of a parallel dependency rather than racing or duplicating installation.; Inspect installed source when an assumed stub path is absent.
- Remedy: Read the observed inventory, wait for shared outputs when required, and use actual project entry points or canonical external plan contract. Create a task-owned temporary directory from an existing working directory before using it.
- Verification evidence: Reports record corrected reads and completed CLI help probes; storage/UI harnesses subsequently ran once dependencies and directories were ready.
- Limitations: An absent optional path is not proof of missing durable user preferences or a broken saved configuration; feedback-path gaps need separate treatment.
- Sources:
  - [2026-10-04-discord-adapter-review.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-discord-adapter-review.md) (SHA-256 `5e329a29b1a3`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-ops-docs-cli-probe.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-ops-docs-cli-probe.md) (SHA-256 `df7f68ac1a59`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-review-probes.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-review-probes.md) (SHA-256 `3a811769558f`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-storage-test-directory-probe.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-storage-test-directory-probe.md) (SHA-256 `59a97c61e309`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-ui-harness-discovery.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-ui-harness-discovery.md) (SHA-256 `7dbee454bc18`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-02-diagnostic-environment.md](/home/example/coding/kitty-codex/docs/postmortem/2026-10-02-diagnostic-environment.md) (SHA-256 `f1a2914a99f5`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-23-infrastructure-patch-failure.md](/home/example/coding/example-client-app/docs/postmortem/2026-09-23-infrastructure-patch-failure.md) (SHA-256 `bc27ed7ce2b0`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-02-buildx-prerequisite-install.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-02-buildx-prerequisite-install.md) (SHA-256 `cf43ab9afa7c`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-02-staging-infrastructure-readiness.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-02-staging-infrastructure-readiness.md) (SHA-256 `e5094af323a6`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-vps-recovery-implementation.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-04-vps-recovery-implementation.md) (SHA-256 `db3fcc8d0ae1`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-vps-workflow-inspection.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-04-vps-workflow-inspection.md) (SHA-256 `409c6dd1137b`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-02-guild-router-verification.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-02-guild-router-verification.md) (SHA-256 `293deda16a75`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-reader-jump-sandbox.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-03-reader-jump-sandbox.md) (SHA-256 `1942248bc40c`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-restart-review-file-inventory.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-03-restart-review-file-inventory.md) (SHA-256 `349de06e5063`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-sandbox-initialization.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-03-sandbox-initialization.md) (SHA-256 `dd1bd38a1680`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-scaffold-working-directory

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: scaffold/dependencies created in shared parent; delegated write path resolves outside requested repository
- Applicability: Repository scaffolding in a shared directory containing sibling projects.
- Diagnostic checks: Capture the absolute cwd and target before mutation.; Check sibling status against the pre-existing baseline after any misplaced write.
- Remedy: Use explicit target working directories or absolute task-scoped paths; avoid shared-root delegated patch operations.
- Verification evidence: Misplaced generated setup/dependencies were removed; sibling Git status checks reconfirmed no newly changed sibling source or commits.
- Limitations: Cleanup applies only to proven task-created artifacts. Never remove ambiguous sibling or pre-existing files.
- Sources:
  - [2026-08-19-scaffold-path.md](/home/example/coding/lucas/lucas-java-4/docs/postmortem/2026-08-19-scaffold-path.md) (SHA-256 `3f75e089d72e`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-clean-install-parent-transaction

- Status: **activation_pending**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: chezmoi unit apply failed on first install; launcher and units exist but runtime package parent is missing; parent-dirs changes existing restrictive modes
- Applicability: Exact nested ChezMoi targets installed into clean or restrictive directory layouts.
- Diagnostic checks: Exercise a real empty-destination install rather than only rendering a dry-run.; Check parent identity, ownership, symlink rejection and existing modes.; Inject mkdir/open/swap failures and verify rollback.
- Remedy: Create only missing parent directories in a descriptor-relative checked transaction, preserve existing modes, and roll back newly created parents on pre-apply failure; retain the exact file target list.
- Verification evidence: Clean-home, mode, symlink, swap and rollback regressions pass; real ChezMoi test installs exactly 27 intended files.
- Limitations: The report explicitly leaves real timer activation, installed identity, trigger and journal confirmation for later upstream activation. Code/real-filesystem tests do not establish live timer activation.
- Sources:
  - [2026-07-14-timer-runtime-parent-not-installed.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-07-14-timer-runtime-parent-not-installed.md) (SHA-256 `a375190b94c2`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-discover-paths-before-reads

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: No such file or directory during read-only inspection; guessed helper suffix or skill root; optional SOURCE.md missing; producer artifact not yet published
- Applicability: Repository and upstream research where names, extensions, source roots or asynchronous artifacts are uncertain.
- Diagnostic checks: Inventory known existing roots with rg --files before targeted reads.; Distinguish Fish functions from external scripts and exact case-sensitive names.; For delegated artifacts wait for producer completion, not a progress message.; Inspect every result in a batch; later success may hide an earlier missing-path error.
- Remedy: Use inventoried paths and test optional-path existence. Refresh is a Fish function; snapshot-codex-config is an external Python executable. Read the current package tree rather than reusing guessed upstream paths.
- Verification evidence: Reports record corrected inventory reads succeeding and authorized checks continuing without changing product state in the failed reads.
- Limitations: Missing optional files and rg no-match status are diagnostic outcomes, not proof of a runtime defect. Repository layout can change; rediscover it.
- Sources:
  - [2026-08-19-skill-import-environment-inspection.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-19-skill-import-environment-inspection.md) (SHA-256 `2982fc3ec711`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-19-flavibot-now-playing.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-19-flavibot-now-playing.md) (SHA-256 `1fa8a032a220`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-19-now-playing-width.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-19-now-playing-width.md) (SHA-256 `949a5aa25daa`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-19-yt-dl-chezmoi-executable.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-19-yt-dl-chezmoi-executable.md) (SHA-256 `b209bbc732a5`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-19-yt-dl-fps-tolerance.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-19-yt-dl-fps-tolerance.md) (SHA-256 `4a1cb1922a22`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-24-mismatched-verification-commands.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-24-mismatched-verification-commands.md) (SHA-256 `46e5b1e40987`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-27-daily-size-script-inspection-paths.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-27-daily-size-script-inspection-paths.md) (SHA-256 `62976fbc4c7c`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-commit-skills-shell-startup.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-commit-skills-shell-startup.md) (SHA-256 `8ff682250e36`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-metaprompt-benchmark-sandbox-startup.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-benchmark-sandbox-startup.md) (SHA-256 `f26e4ae4c28f`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-metaprompt-selection-eval-source-path.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-selection-eval-source-path.md) (SHA-256 `24c41ccc0bdd`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-metaprompt-selection-validation.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-selection-validation.md) (SHA-256 `21607fa9f53f`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-metaprompt-source-discovery.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-source-discovery.md) (SHA-256 `ebb2cc3948bd`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-phone-ssh-diagnostic-shell-startup.md](/home/example/linux-config/docs/postmortem/2026-10-03-phone-ssh-diagnostic-shell-startup.md) (SHA-256 `013ed9b04134`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-codex-snapshot-function-probe.md](/home/example/linux-config/docs/postmortem/2026-10-04-codex-snapshot-function-probe.md) (SHA-256 `b62c0e81b60b`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-documentation-overview-inspection.md](/home/example/linux-config/docs/postmortem/2026-10-04-documentation-overview-inspection.md) (SHA-256 `93e982d69334`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-instructional-overview-inspection.md](/home/example/linux-config/docs/postmortem/2026-10-04-instructional-overview-inspection.md) (SHA-256 `0f56b5ce50ca`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-kitty-scrollbar-inspection.md](/home/example/linux-config/docs/postmortem/2026-10-04-kitty-scrollbar-inspection.md) (SHA-256 `cac81ac1cb8c`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-metaprompt-replacement-validation.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-04-metaprompt-replacement-validation.md) (SHA-256 `0e80df68a1dd`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-metaprompt-run-sandbox-startup.md](/home/example/linux-config/docs/postmortem/2026-10-04-metaprompt-run-sandbox-startup.md) (SHA-256 `cb1c6c04ce36`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-metaprompt-session-scope.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-04-metaprompt-session-scope.md) (SHA-256 `ac02deccdb08`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-05-postmortem-memory-sandbox-startup.md](/home/example/linux-config/docs/postmortem/2026-10-05-postmortem-memory-sandbox-startup.md) (SHA-256 `d9ba347c48d3`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-mutable-guide-versus-pin

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: approval rejects editorial changes to mixed-purpose SOURCE.md; blanket provenance exclusion includes maintained how-to
- Applicability: Documentation edits near pinned source identity and mutable maintenance procedures.
- Diagnostic checks: Classify content rather than excluding entire filename class.; Check native pin manifest and preserved URLs/revisions/dates.
- Remedy: Separate maintained overview changes from immutable source bytes and obtain exact required approval when review blocks the former; validate every pin afterward.
- Verification evidence: After explicit approval scoped patch applied, all eight native SHA256 digests matched and source identity/fenced examples were preserved.
- Limitations: Approval was task-specific. This finding does not authorize edits to immutable provenance or bypass automatic review.
- Sources:
  - [2026-10-04-instructional-overview-scope-review.md](/home/example/linux-config/docs/postmortem/2026-10-04-instructional-overview-scope-review.md) (SHA-256 `a760b4965cac`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-package-traversal-modes

- Status: **activation_pending**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: apt warns package inaccessible to _apt; temporary directory mode 0700 prevents downloader traversal; sudo -n diagnostic requires password
- Applicability: A downloaded package in a private mktemp directory passed to apt/dnf.
- Diagnostic checks: Inspect directory traversal permissions separately from package file permissions.; Use a boundary test at the package-manager invocation when direct _apt impersonation is unavailable.
- Remedy: After successful download set the owned package directory to 0711 and package file to 0644 before the sole privileged install command.
- Verification evidence: Defining test observed old 0700 RED, then passed for Ubuntu x64, Debian ARM64 and Fedora x64.
- Limitations: The direct _apt check could not authenticate and a later real apt install remained pending. 0711 permits traversal to a known file without listing; no live production download was claimed.
- Sources:
  - [2026-09-02-apt-sandbox-reproducer-sudo-auth.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-02-apt-sandbox-reproducer-sudo-auth.md) (SHA-256 `2b2f86835299`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-refresh-snapshot-ownership

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: refresh-config changes protected dirty dot_codex/config.toml; live config snapshot overwrites intentional repository version; broad refresh approval rejected for unrelated configuration
- Applicability: Configuration refresh with pre-existing intentional live/source divergence or protected dirty source.
- Diagnostic checks: Run snapshot-codex-config --dry-run.; Record source/live hashes and inspect ownership before refresh.; Verify whether broad refresh is authorized to copy live config into tracked source.
- Remedy: Stop the overwrite when ownership conflicts; use exact owned deployment targets where authorized. If an overwrite occurred, restore only the attributable source bytes from reliable pre-session evidence and preserve current live content.
- Verification evidence: Protected source checksum was restored exactly while live bytes stayed unchanged; other reports deployed only owned desktop targets and left protected Codex/Git settings intact.
- Limitations: refresh-config intentionally snapshots live to repository and then applies configuration. A ChezMoi dry-run does not authorize replacing protected source content; this guidance does not exempt routine required refresh without a real ownership conflict.
- Sources:
  - [2026-07-14-refresh-config-protected-file-overwrite.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-07-14-refresh-config-protected-file-overwrite.md) (SHA-256 `1a69d8d4b4e1`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-08-24-sandbox-network-namespace-check.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-24-sandbox-network-namespace-check.md) (SHA-256 `2de93f627696`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-19-flavibot-now-playing.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-19-flavibot-now-playing.md) (SHA-256 `1fa8a032a220`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-session-attribution-direct-evidence

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: session_scope returns unsafe empty candidates despite observed nested writes
- Applicability: Authorized session-scoped delivery when helper cannot parse current transcript format.
- Diagnostic checks: Review successful nested tool actions and captured initial dirty baseline.; Inspect task-owned files and separable overlapping hunks independently.
- Remedy: Use the workflow-permitted direct-write evidence fallback and stage only attributable files/hunks; leave ambiguous unrelated dirties untouched.
- Verification evidence: One report records independently reviewed scope; later focused attribution reviewed 13 staged files and left unrelated smoke hunk unstaged, with staged whitespace and focused checks passing.
- Limitations: The scope helper parser itself remains unrepaired. Empty attribution is not proof of no writes; timestamps alone do not establish ownership.
- Sources:
  - [2026-10-04-metaprompt-session-scope.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-04-metaprompt-session-scope.md) (SHA-256 `ac02deccdb08`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-05-metaprompt-run-commit-attribution.md](/home/example/linux-config/docs/postmortem/2026-10-05-metaprompt-run-commit-attribution.md) (SHA-256 `b04818228c5c`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-vps-prompt-session-scope-attribution.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-04-vps-prompt-session-scope-attribution.md) (SHA-256 `96ed63357f3c`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-skip-worktree-and-scoped-state

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: git status clean but HEAD lacks local config setting; checkout-index snapshot omits tracked config; aggregate source/live byte check fails despite correct scoped value
- Applicability: Protected local configuration and index flags during scoped delivery.
- Diagnostic checks: Inspect git ls-files -v, HEAD/index blobs and intended semantic field.; Separate current local/runtime state from committed scope.; For exported snapshots compare all tracked index blobs and use NUL-delimited paths.
- Remedy: Preserve skip-worktree and unrelated local bytes; construct only the authorized hunk against HEAD and validate the staged candidate. Restore omitted snapshot files from their index blobs without changing flags.
- Verification evidence: Authorized staged blob equaled HEAD plus the requested addition; flags were preserved; corrected exported snapshot passed 261 documentation links.
- Limitations: Status alone is not commit evidence; byte equality may be too broad when concurrent sessions or serialization differ. Scope ownership still requires direct evidence.
- Sources:
  - [2026-10-04-kitty-scrollbar-inspection.md](/home/example/linux-config/docs/postmortem/2026-10-04-kitty-scrollbar-inspection.md) (SHA-256 `cac81ac1cb8c`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-metaprompt-post-push-verification.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-04-metaprompt-post-push-verification.md) (SHA-256 `2cdff05044ae`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-metaprompt-session-scope.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-04-metaprompt-session-scope.md) (SHA-256 `ac02deccdb08`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-vps-user-prefix-repair-pending

- Status: **activation_pending**; root-cause confidence: **supported**; verification scope: **code**.
- Symptoms: npm global Codex update EACCES under system prefix; home containment check rejects home parent; fake npm prefix has off-by-one lib directory
- Applicability: Repairing a VPS CLI installation owned by a system prefix.
- Diagnostic checks: Inspect effective npm prefix, ownership and shell command routing on the actual host.; Allow the home root only for parent writability while retaining contained writable targets.; Make npm substitutes match real prefix semantics.
- Remedy: Use the checked helper to install into writable user scope and persist routing; runtime replacement is conditional on verified compatibility and final acceptance requires a second SSH session.
- Verification evidence: 22 isolated tests passed for permissions, routing, rollback, archive rejection and recovery; Bash syntax passed.
- Limitations: VPS live dry-run/apply acceptance remains pending. Disposable homes/service substitutes do not prove remote upgrade.
- Sources:
  - [2026-10-03-vps-codex-repair.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-vps-codex-repair.md) (SHA-256 `3f4f62937662`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-backup-swap-alias

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime** (preflight only).
- Symptoms: valid swap fstab /dev/disk/by-uuid alias rejected as unsupported/missing.
- Applicability: backup preflight matching fstab identifiers to lsblk canonical partition names.
- Diagnostic checks: compare alias resolution and canonical name, type and source-disk ancestry.
- Remedy: resolve absolute device aliases and LABEL/PARTUUID references before lookup, retaining conventional topology guards.
- Verification: alias regression RED then GREEN, actual-machine read-only live source/destination preflight passed, 37-test backup suite passed.
- Limitations: no full-machine backup or restored disk boot tested; runtime scope covers preflight only.
- Sources: [live backup swap alias report](/home/example/linux-config/docs/postmortem/2026-10-06-live-backup-swap-alias.md) (SHA-256 `1b1f947831f523ac1cdfce6a55b31d628e3d300587e05f31df0e629d78665901`).

## local-backup-invoker-artifact-access

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Sudo-created backup archives and logs unreadable by invoking user
- Applicability: Private backup bundle artifacts created by a privileged backup process.
- Diagnostic checks: Inspect bundle and archive/log UID/modes. Verify generated artifact scope separately from copied-home metadata.
- Remedy: Resolve invoking sudo account through pwd and assign only bundle directory and known generated regular files. Apply on startup, publication and failure; provide scoped access repair and skip symlinks. Never recursively chown copied home.
- Verification evidence: Ownership/account regressions RED then GREEN; complete 62-test backup suite passes including interruption cleanup and publication. Installed helper matches source after refresh-config.
- Limitations: Existing root-owned bundle repair and fresh real-archive read require local sudo authentication. No restored boot verification.
- Sources:
  - [2026-10-07-backup-owner-access.md](/home/example/linux-config/docs/postmortem/2026-10-07-backup-owner-access.md) (SHA-256 `595e229ca8d6`; 1 alias).

## local-shared-index-commit-race

- Status: **unresolved**; root-cause confidence: **supported**; verification scope: **none**.
- Symptoms: Reviewed session-only staged paths expand before commit in a shared working tree.
- Applicability: Concurrent sessions using one Git index during scoped commits.
- Diagnostic checks: Compare reviewed staged paths/blobs with final commit tree and upstream hash.
- Remedy: Enforce explicit reviewed path scope at commit creation. If scope contamination has already been published, pause and obtain the user decision; here the user chose to preserve history and document the incident. Prevention remains unverified.
- Verification evidence: Five reviewed files became twelve in commit 5451db5. It was local at the initial remote check, but another session subsequently published it and follow-up f8f044e; fresh HEAD, origin/main and ls-remote agree on f8f044e. Recovery not attempted. User chose to keep published history intact and close delivery with a documentation follow-up.
- Limitations: Concurrent actor identity is unknown; no recovery or prevention test has passed.
- Source: [ctp staging race](/home/example/linux-config/docs/postmortem/2026-10-08-ctp-session-staging-race.md).

## local-git-index-same-filesystem-publish

- Status: verified_fix
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: Scoped Git commit succeeds but os.replace of a /tmp reconciliation index into .git/index fails with OSError18 Invalid cross-device link
- Applicability: Publishing an isolated/reconciled Git index when temporary and repository filesystems differ.
- Diagnostics: Distinguish successful commit creation from post-commit index cleanup failure.; Compare current index with the captured original before replacing it; stop on concurrent changes.; Check source/destination device IDs and preserve unrelated staging.
- Remedy: Create the publication temporary file inside .git, copy/flush/fsync intended bytes, retain permissions and atomically rename on that filesystem under an owned index lock. Preserve the existing commit; do not reset/amend history.
- Verification: Initial commit8d2d0da succeeded with16 intended paths; /tmp->.git rename failed. Same-filesystem repair verified original bytes unchanged, intended index bytes published, commit intact and no residual staged diff.
- Limitations: Verified for this scoped commit/index state; changed real indexes require fresh reconciliation. Do not overwrite unrelated staged work or bypass hooks.
- Source: [tmux index reconciliation](../../../../docs/postmortem/2026-10-13-tmux-commit-index-reconciliation.md) (SHA-256 `da79e08750d7ab5a19b06981cea8fc9d45a83c36021eec65729cad5f83b0203c`).

## local-git-fetch-before-ancestry

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Fetch-first push rejection followed by an unfetched remote object ancestry error128.
- Applicability: Remote-ref comparison after concurrent updates or unfetched advertised hashes.
- Diagnostic checks: Fetch the authorized branch first; distinguish exit0/1 from errors; review graph, delta and protected dirty state.
- Remedy: Fetch the authorized branch, then perform valid ancestry and delta checks; preserve local commits and use a reviewed normal merge when required, without history rewriting.
- Verification evidence: The unfetched182713c object caused exit128. Fetch returned0; both session commit ancestry probes against fetched182713c returned1 without object errors. Clean normal merge was prepared and unrelated local overlays retained.
- Limitations: Ancestry verification and prepared local merge do not prove a subsequent push succeeded. Ambiguous conflicts or concurrent workspace changes require fresh review.
- Sources:
  - [2026-10-13-tmux-session-push-divergence.md](/home/example/linux-config/docs/postmortem/2026-10-13-tmux-session-push-divergence.md) (SHA-256 `3681884d70de`; aliases retained in [sources.json](../sources.json)).

## local-git-owned-index-lock-check

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: write-tree fails on index.lock already owned by the calling helper.
- Applicability: Scoped commit helpers retaining a real-index guard while validating a prepared merge tree.
- Diagnostic checks: Confirm owned lock, intact HEAD/MERGE_HEAD and exact captured index bytes.
- Remedy: Copy the guarded index and validate through a separate GIT_INDEX_FILE; avoid lock-taking operations on the real index until its guard is released. Keep atomic same-filesystem publication and normal hooks.
- Verification evidence: Under the owned real-index lock, copied-index write-tree returned0 with the reviewed merge tree and real index bytes unchanged; helper was corrected accordingly.
- Limitations: This probe verifies the lock interaction only; independently verify commit parents/scope and push reachability.
- Source: [tmux merge index lock](/home/example/linux-config/docs/postmortem/2026-10-13-tmux-merge-index-lock.md) (SHA-256 `7223eaacbad03dcbf3e6d08e497ec2a150ee1e7ef30804506e1c88a7c2c26b98`).
