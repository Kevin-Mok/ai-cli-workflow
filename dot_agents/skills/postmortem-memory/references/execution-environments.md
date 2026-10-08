# Execution environments

Use these reviewed findings to compare a failure with prior evidence. Check applicability and diagnostics before choosing a remedy; keep its verification scope and limits explicit.

## ext-exec-function-scope

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: kitty +runpy NameError: encoded is not defined; inline reproducer works but saved generator cannot resolve helper
- Applicability: Python code executed by exec inside a function rather than ordinary module globals.
- Diagnostic checks: Inspect the host's execution scope.; Reject a reproducer's arbitrary exit 1 unless expected evidence text is present.
- Remedy: Place imports, helpers and generator code inside one main function to obtain normal lexical scoping.
- Verification evidence: Saved reproducer emitted the expected REPRODUCED marker with intentional exit 1 and no stderr; wrapper and shell syntax checks passed.
- Limitations: This fixes diagnostic script scoping and does not fix the diagnosed terminal defect.
- Sources:
  - [2026-10-02-reproducer-scope.md](/home/example/coding/kitty-codex/docs/postmortem/2026-10-02-reproducer-scope.md) (SHA-256 `72e877985bbb`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-explicit-wrapper-shell

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: Playwright helper Permission denied; shared shell wrapper readable but not executable; documented Codex-home wrapper absent
- Applicability: Trusted installed shell helpers missing executable mode or installed under a different catalog root.
- Diagnostic checks: Locate the actual installed wrapper and inspect its mode.; Read the helper before choosing its interpreter.
- Remedy: Invoke the known trusted shell helper explicitly with bash at its actual installed path; leave owner-managed executable-mode repair separate.
- Verification evidence: Lucas browser smoke checks completed via bash; Example Client browser retry used the installed Agents-root wrapper without changing its mode.
- Limitations: This does not repair permissions or justify executing an unknown file; use the helper's actual language interpreter.
- Sources:
  - [2026-08-19-playwright-wrapper-permission.md](/home/example/coding/lucas/lucas-java-4/docs/postmortem/2026-08-19-playwright-wrapper-permission.md) (SHA-256 `b74810048e27`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-08-17-preview-lead-submission-diagnostics.md](/home/example/coding/example-client-app/docs/postmortem/2026-08-17-preview-lead-submission-diagnostics.md) (SHA-256 `552f9e8c9851`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-project-browser-cache

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Playwright Chromium headless executable absent; browser tests fail before assertions; project .cache/ms-playwright installed but home cache searched
- Applicability: Project-local Playwright browser installations.
- Diagnostic checks: Inspect the configured browser cache and installed executable before reinstalling.; Check PLAYWRIGHT_BROWSERS_PATH in both wrapper and direct test invocations.
- Remedy: Use the project test wrapper or export its existing project browser cache path for direct runs.
- Verification evidence: UI harness later executed normally with the explicit path; storage/API integration passed 42 tests and the final integrated report passed nine browser tests.
- Limitations: The initial storage-only report deferred final browser verification; later UI/integration reports supply execution evidence. This path correction is not a frontend defining RED failure.
- Sources:
  - [2026-10-04-storage-full-suite-browser-preflight.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-storage-full-suite-browser-preflight.md) (SHA-256 `30e11e61cb02`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-ui-harness-discovery.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-ui-harness-discovery.md) (SHA-256 `7dbee454bc18`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-review-findings.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-review-findings.md) (SHA-256 `cc3fd381068a`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-qemu-isolated-capabilities

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: Android bundled QEMU lacks standard VM options; extracted QEMU missing VGA ROM; probe needs unavailable TCG module
- Applicability: Isolated blank-VM rehearsals using locally extracted QEMU packages.
- Diagnostic checks: Inspect the selected binary and available acceleration/modules before launch.; Use a serial-only fixture if no VGA ROM is supplied.; Confirm cleanup targets only registered task-owned processes.
- Remedy: Use the compatible distribution QEMU fixture with explicit serial/headless configuration and available KVM acceleration instead of assuming a bundled emulator provides all required capabilities.
- Verification evidence: The isolated Ubuntu/KVM rehearsal and bounded cleanup probe passed; no global packages or existing services changed.
- Limitations: These fixture settings require available KVM; they do not apply blindly to hosts without hardware acceleration.
- Sources:
  - [2026-10-04-vps-workflow-inspection.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-04-vps-workflow-inspection.md) (SHA-256 `409c6dd1137b`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-sandbox-loopback

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted; read-only commands fail before shell execution; patch helper cannot start
- Applicability: Command runners whose restricted network namespace cannot initialize loopback; distinguish runner startup from application or repository failure.
- Diagnostic checks: Confirm identical pre-execution error across independent harmless commands.; Capture repository status using a scoped command that actually executes.; Check that the target directory is a Git checkout rather than assuming one.
- Remedy: Use the approved require_escalated route for the necessary scoped command when policy permits, or an available authorized workspace editor. Keep the host sandbox repair as separate outstanding work.
- Verification evidence: Multiple reports record successful approved source reads, status checks and verification after normal startup failed; application state was unchanged by failed launches.
- Limitations: Successful escalation does not repair default sandbox startup or authorize unrelated resources. One documentation report only prepared an add-only recovery and contains no completed verification.
- Sources:
  - [2026-10-05-command-sandbox-unavailable.md](/home/example/coding/codex-usage/docs/postmortem/2026-10-05-command-sandbox-unavailable.md) (SHA-256 `22c89b43cf56`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-shell-sandbox.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-shell-sandbox.md) (SHA-256 `d7eb9c7bda4e`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-02-diagnostic-environment.md](/home/example/coding/kitty-codex/docs/postmortem/2026-10-02-diagnostic-environment.md) (SHA-256 `f1a2914a99f5`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-08-19-patch-helper-sandbox.md](/home/example/coding/lucas/lucas-java-4/docs/postmortem/2026-08-19-patch-helper-sandbox.md) (SHA-256 `de03df56ae06`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-08-26-documentation-patch-sandbox.md](/home/example/coding/example-client-app/docs/postmortem/2026-08-26-documentation-patch-sandbox.md) (SHA-256 `445a13994ce1`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-02-relay-rollout-workflow-context.md](/home/example/coding/example-client-app/docs/postmortem/2026-09-02-relay-rollout-workflow-context.md) (SHA-256 `1495be749834`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-23-shell-sandbox-loopback-inspection.md](/home/example/coding/example-client-app/docs/postmortem/2026-09-23-shell-sandbox-loopback-inspection.md) (SHA-256 `7b5b788fe247`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-02-shell-sandbox-migration-review.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-02-shell-sandbox-migration-review.md) (SHA-256 `2e03b4ee2669`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-02-sandbox-initialization.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-02-sandbox-initialization.md) (SHA-256 `64647a949ddb`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-prompt-save-sandbox-initialization.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-03-prompt-save-sandbox-initialization.md) (SHA-256 `3de23b848b99`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-reader-jump-sandbox.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-03-reader-jump-sandbox.md) (SHA-256 `1942248bc40c`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-sandbox-initialization.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-03-sandbox-initialization.md) (SHA-256 `dd1bd38a1680`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-overnight-reader-jump.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-04-overnight-reader-jump.md) (SHA-256 `e44b69235005`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-08-17-preview-lead-submission-diagnostics.md](/home/example/coding/example-client-app/docs/postmortem/2026-08-17-preview-lead-submission-diagnostics.md) (SHA-256 `552f9e8c9851`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-06-count-update-latency.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-06-count-update-latency.md) (SHA-256 `e20c6026f866`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-embedded-python-diagnostic-scope

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: kitty +runpy generator NameError despite ordinary Python expectation
- Applicability: Diagnostic execution inside Kitty embedded Python scope.
- Diagnostic checks: Use explicit config and finalized keyboard mode data.; Try an explicit loop when top-level comprehension/generator name scope differs.
- Remedy: Use the demonstrated explicit-loop read-only probe rather than assuming normal module top-level scope.
- Verification evidence: Corrected probe exited 0 and showed finalized key actions; configuration parse and runtime reload checks passed.
- Limitations: The failure was diagnostic scope, not a Kitty runtime defect. Visual/drag acceptance still needed its manual check.
- Sources:
  - [2026-10-04-kitty-scrollbar-inspection.md](/home/example/linux-config/docs/postmortem/2026-10-04-kitty-scrollbar-inspection.md) (SHA-256 `cac81ac1cb8c`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-exact-launcher-runtime-version

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: CLI config probe rejects valid reasoning effort on old binary; interactive Fish and i3 fnm alias select different Codex installs
- Applicability: GUI shortcut launching a CLI installed through multiple shell-managed runtimes.
- Diagnostic checks: Compare exact Node and CLI paths/version from interactive shell and shortcut.; Use isolated minimal config to distinguish wrong binary from intended invalid-setting probe.
- Remedy: Point the shortcut to the verified supported runtime and preserve existing user model settings instead of changing them to fit the old diagnostic binary.
- Verification evidence: Exact deployed Node/CLI pair parsed full config, refresh completed and i3 reload succeeded; all active Kitty instances accepted reload.
- Limitations: Current runtime acceptance is version-specific. Automated parsing/reload does not establish visual acceptance in a fresh session.
- Sources:
  - [2026-10-04-kitty-scrollbar-inspection.md](/home/example/linux-config/docs/postmortem/2026-10-04-kitty-scrollbar-inspection.md) (SHA-256 `cac81ac1cb8c`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-hidden-prompt-lock

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: refresh appears stuck and holds chezmoi persistent state lock; suppressed overwrite prompt; futex wait and later lock timeout
- Applicability: Broad noninteractive refresh encountering a locally modified target.
- Diagnostic checks: Inspect processes, lock holder and captured output.; Determine whether an interactive decision is waiting rather than assuming deadlock.
- Remedy: Use noninteractive keep-going apply, continue independent shortcut refresh and report REFRESH PARTIAL with nonzero status and actionable conflicts.
- Verification evidence: Fixed live helper completed within 20 seconds, printed the conflict/partial result and left no ChezMoi process; focused regression and Fish syntax passed.
- Limitations: A partial refresh is not REFRESH COMPLETE. Resolve remaining association ownership before claiming the full workflow succeeded.
- Sources:
  - [2026-09-16-refresh-config-mime-tty.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-16-refresh-config-mime-tty.md) (SHA-256 `dc0ddec4ba6d`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-i3-hidden-workspace-titlebar-probe

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: i3 normal border with zero decoration height on an inactive workspace; early screenshot captures the prior workspace; existing scrot filename may be suffixed
- Applicability: Live i3/X11 titlebar validation after changing window borders.
- Diagnostic checks: Check workspace visibility and fullscreen state.; Use actual_deco_rect for modern split leaves with deco_rect fallback; handle null names and missing heights.; Allow compositor rendering and inspect the actual fresh screenshot path.
- Remedy: Briefly display the target workspace, inspect rendered titlebar geometry and a uniquely named screenshot, then restore original focus.
- Verification evidence: The zero-height calling-task decoration became 1280x30 and the fresh screenshot showed the live titlebar. A temporary new resumed TUI showed the persisted short name without project suffix; narrow/tabbed/fullscreen checks exited 0.
- Limitations: Diagnostic correction only; i3 rendering and default sandbox remain unchanged. Does not guarantee model instruction compliance for every future task.
- Sources:
  - [2026-10-05-kitty-overview-inspection.md](/home/example/linux-config/docs/postmortem/2026-10-05-kitty-overview-inspection.md) (SHA-256 `a3ed49e13527`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-language-appropriate-validator

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: bash -n reports syntax error on Python tuple; Fish functions probe fails on external Python executable
- Applicability: Mixed-language repository verification and command inspection.
- Diagnostic checks: Read shebang/source language and command type before selecting a validator.; Rerun checks skipped by a failing chain.
- Remedy: Use Python AST/compilation for Python, Fish syntax for Fish and Bash syntax for Bash; inspect external executable source rather than asking Fish for its function definition.
- Verification evidence: Correct Python AST check and focused desktop suites passed; external snapshot script and its dry-run interface were read successfully.
- Limitations: A successful partial chain does not prove later skipped checks. A language mismatch is a diagnostic error, not necessarily broken source.
- Sources:
  - [2026-09-24-mismatched-verification-commands.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-24-mismatched-verification-commands.md) (SHA-256 `46e5b1e40987`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-codex-snapshot-function-probe.md](/home/example/linux-config/docs/postmortem/2026-10-04-codex-snapshot-function-probe.md) (SHA-256 `b62c0e81b60b`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-nonexecuting-shell-tests

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: Permission denied invoking tracked shell test directly
- Applicability: Repository shell tests intentionally stored with mode 100644.
- Diagnostic checks: Inspect tracked mode and nearby test convention.
- Remedy: Invoke the test with bash when its tracked mode is intentionally non-executable.
- Verification evidence: Mode 100644 matched neighboring tests; focused and existing refresh tests both passed through bash.
- Limitations: No blanket chmod is justified. Executable entrypoints have a different deployment contract.
- Sources:
  - [2026-08-24-refresh-config-regression-test-permissions.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-24-refresh-config-regression-test-permissions.md) (SHA-256 `91764a91f053`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-sandbox-loopback-approved-route

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted; shell or patch helper fails before command execution; wrapper may return success without requested command output
- Applicability: Bubblewrap-backed command or patch startup in this environment; a task is authorized but its default wrapper cannot initialize loopback.
- Diagnostic checks: Check whether any command body ran; compare error text with expected command output.; Repeat the same bounded operation only through an approved available execution route.; Capture Git status before the first successful write and inspect output as well as wrapper status.
- Remedy: Use the reviewed alternate execution route for the same task scope. For unavailable patch tooling, use a reviewed scoped diff and verify the resulting changes.
- Verification evidence: Many independent reports record identical reads failing before startup and the same reads succeeding with exit 0 through approved execution; relevant focused checks subsequently passed.
- Limitations: This unblocks tasks; it does not repair Bubblewrap or establish the underlying host policy. Ordinary sandbox startup remains unresolved. Do not broaden permissions or edit host security settings based on these reports.
- Sources:
  - [2026-08-19-skill-import-environment-inspection.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-19-skill-import-environment-inspection.md) (SHA-256 `2982fc3ec711`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-08-24-fn-progress-patch-helper-sandbox.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-24-fn-progress-patch-helper-sandbox.md) (SHA-256 `4635e517ae36`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-08-24-sandbox-network-namespace-check.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-24-sandbox-network-namespace-check.md) (SHA-256 `2de93f627696`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-08-25-sandbox-read-and-patch-failures.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-25-sandbox-read-and-patch-failures.md) (SHA-256 `b1c6a9fa959e`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-08-30-sandboxed-fn-progress-inspection.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-30-sandboxed-fn-progress-inspection.md) (SHA-256 `684ef4b01e18`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-01-smoke-test-patch-tooling.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-01-smoke-test-patch-tooling.md) (SHA-256 `139e9c6c9013`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-02-apply-patch-sandbox-failure.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-02-apply-patch-sandbox-failure.md) (SHA-256 `6622c74c1bad`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-16-restart-ethernet-inspection.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-16-restart-ethernet-inspection.md) (SHA-256 `09e3922576e4`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-18-metaprompt-sandbox-startup.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-18-metaprompt-sandbox-startup.md) (SHA-256 `410b576ca465`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-18-sandbox-loopback-read-failure.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-18-sandbox-loopback-read-failure.md) (SHA-256 `29eb0f5d12f3`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-19-flavibot-now-playing.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-19-flavibot-now-playing.md) (SHA-256 `1fa8a032a220`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-19-now-playing-width.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-19-now-playing-width.md) (SHA-256 `949a5aa25daa`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-19-yt-dlp-installed-version.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-19-yt-dlp-installed-version.md) (SHA-256 `c49a07a07687`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-22-commit-inspection-sandbox.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-22-commit-inspection-sandbox.md) (SHA-256 `b30d0ee5a132`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-24-repository-shell-sandbox-startup.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-24-repository-shell-sandbox-startup.md) (SHA-256 `9afa7c8d7077`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-27-shell-sandbox-startup-failure.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-27-shell-sandbox-startup-failure.md) (SHA-256 `02d9084d19c4`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-28-command-sandbox-loopback-startup.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-28-command-sandbox-loopback-startup.md) (SHA-256 `f26e7e43d741`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-30-secret-audit-shell-sandbox-startup.md](/home/example/linux-config/docs/postmortem/2026-09-30-secret-audit-shell-sandbox-startup.md) (SHA-256 `cc5aeccc249f`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-benchmark-prompt-sandbox-startup.md](/home/example/linux-config/docs/postmortem/2026-10-03-benchmark-prompt-sandbox-startup.md) (SHA-256 `82c2fb83b052`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-commit-skills-shell-startup.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-commit-skills-shell-startup.md) (SHA-256 `8ff682250e36`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-metaprompt-benchmark-sandbox-startup.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-benchmark-sandbox-startup.md) (SHA-256 `f26e4ae4c28f`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-metaprompt-shell-startup.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-shell-startup.md) (SHA-256 `2603192066fe`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-phone-ssh-diagnostic-shell-startup.md](/home/example/linux-config/docs/postmortem/2026-10-03-phone-ssh-diagnostic-shell-startup.md) (SHA-256 `013ed9b04134`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-vps-codex-repair.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-vps-codex-repair.md) (SHA-256 `3f4f62937662`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-codex-config-sync-sandbox.md](/home/example/linux-config/docs/postmortem/2026-10-04-codex-config-sync-sandbox.md) (SHA-256 `1d94d0c30da1`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-metaprompt-replacement-validation.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-04-metaprompt-replacement-validation.md) (SHA-256 `0e80df68a1dd`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-metaprompt-run-sandbox-startup.md](/home/example/linux-config/docs/postmortem/2026-10-04-metaprompt-run-sandbox-startup.md) (SHA-256 `cb1c6c04ce36`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-terminal-prompt-sandbox-startup.md](/home/example/linux-config/docs/postmortem/2026-10-04-terminal-prompt-sandbox-startup.md) (SHA-256 `3f98c41411b3`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-05-postmortem-memory-sandbox-startup.md](/home/example/linux-config/docs/postmortem/2026-10-05-postmortem-memory-sandbox-startup.md) (SHA-256 `d9ba347c48d3`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-vps-bootstrap-prompt-sandbox-startup.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-04-vps-bootstrap-prompt-sandbox-startup.md) (SHA-256 `66d697b22da8`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-05-worktree-guide-sandbox-startup.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-05-worktree-guide-sandbox-startup.md) (SHA-256 `9a2fa7b009ac`; 1 alias(es), all retained in [sources.json](../sources.json)).

  - [2026-10-06-backup-recovery-sandbox-startup.md](/home/example/linux-config/docs/postmortem/2026-10-06-backup-recovery-sandbox-startup.md) (SHA-256 `281cd2e0f1c5`; approved scoped reads verified; default runner remains unavailable).

## local-systemd-installed-prerequisite

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: systemd-analyze verify reports ExecStart not executable or missing; static unit assertions pass before deployment
- Applicability: Live systemd unit verification referencing a helper not yet deployed.
- Diagnostic checks: Resolve the installed ExecStart path and executable mode.; Apply owned helper and unit targets before live verification.
- Remedy: Deploy the exact helper and unit paths, verify live units, then enable using the checked setup command.
- Verification evidence: Six tests passed; setup --check and --enable passed; the timer listing showed its next trigger.
- Limitations: Static source validity does not establish installed executable availability.
- Sources:
  - [2026-08-19-design-skills-systemd-predeploy-verify.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-19-design-skills-systemd-predeploy-verify.md) (SHA-256 `884bacd6e8bf`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-managed-backup-preflight

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: System Python cannot import a uv-managed application while deriving backup path.; Shell continues installation after backup preflight failure.
- Applicability: Operational backup/install sequences for applications managed by an isolated Python environment.
- Diagnostic checks: Check which interpreter executes application imports.; Verify backup bytes, schema version and timing relative to the first upgrade save; do not infer success from subsequent setup.
- Remedy: Use standard-library-only path derivation or explicit managed uv execution, make backup success a checked fail-fast precondition, and verify actual backup metadata before install. Recovery secured the still-version-2 ledger before first upgrade save.
- Verification evidence: Independent backup read confirmed version 2, 37,678,191 bytes, mode 0600 and recorded SHA-256. Later checked version-3 backup retained 268,207 quota observations; installed service and 16 modules verified healthy.
- Limitations: Recovery occurred after restart and is not a successful original pre-install backup. It preserved pre-upgrade state; it does not retroactively repair the original unchecked shell sequence.
- Sources:
  - [2026-10-06-burn-install-backup-preflight.md](/home/example/coding/track-codex-sessions/docs/postmortem/2026-10-06-burn-install-backup-preflight.md) (SHA-256 `86f1c43db1e7`; 1 alias retained in [sources.json](../sources.json)).


## local-codex-nonfatal-exec-metadata

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Restricted Codex inference reports unexpected tool activity although only error metadata and an agent message were emitted.
- Applicability: Pinned native Codex 0.160.1 exec JSON event consumers that reject tool activity.
- Diagnostic checks: Inspect only sanitized event and item type counts, not raw provider diagnostics. Check released exec_events.rs semantics for each candidate metadata type.
- Remedy: Permit the documented nonfatal error item alongside reasoning/agent_message; continue rejecting every actual tool and unknown item. Preserve raw error text privately.
- Verification evidence: Defining metadata regression failed before correction; 16 learning tests and full 203 suite passed. Real saved-login strict-schema inference then passed in 4.145s with usage counts.
- Limitations: This is specific to the reviewed release. Nonfatal metadata is not success by itself; require successful process completion and schema validation. Actual systemd execution remains unverified.
- Source: [AI alpha integration validation](/home/example/coding/ai-twitter-alpha/docs/postmortem/2026-10-06-integration-validation.md) (SHA-256 `c11665ca0e0c`; reviewed alias in [sources.json](../sources.json)).


## local-cancellable-terminal-browser-owner

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Cancelled asyncio.to_thread(input/getpass) leaves an executor thread blocking asyncio.run shutdown.; Child human timeout does not bound a parent still awaiting terminal input.
- Applicability: Linux asyncio CLI setup with visible-browser handoffs and hidden token prompts.
- Diagnostic checks: Exercise cancellation in a real PTY subprocess and require timely process exit. Check terminal echo is disabled before the prompt appears and restored after cancellation. Use distinct parent human and whole-worker deadlines.
- Remedy: Use cancellable fd readiness for terminal input; disable echo before hidden prompts and restore it in finally. Bound parent human waits, sanitize worker events, and terminate only the child process group created by the supervisor.
- Verification evidence: Real PTY and subprocess RED/GREEN regressions passed; 11 worker tests and full 203 suite passed. CLI sandboxed Chrome fixture shut down cleanly.
- Limitations: TTY behavior was verified on Linux. This does not establish live X/MFA, human takeover, or Discord account setup.
- Source: [AI alpha integration validation](/home/example/coding/ai-twitter-alpha/docs/postmortem/2026-10-06-integration-validation.md) (SHA-256 `c11665ca0e0c`; reviewed alias in [sources.json](../sources.json)).


## local-model-thread-lock-lifetime

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Cancelling to_thread releases the app run lock while model subprocess work continues.
- Applicability: Async pipelines calling a bounded synchronous model/fetch engine while holding a process lock.
- Diagnostic checks: Cancel after the model thread starts; verify a second owner cannot acquire the run lock until bounded cleanup completes.
- Remedy: Shield the model task and retain the run lock while its own deadline-limited work drains after cancellation; keep unacknowledged evidence queued and propagate cancellation afterward.
- Verification evidence: Executable cancellation regression failed before the change and passed after it; pipeline 11 and full 203 tests passed, with no delivery or tweet acknowledgement after cancellation.
- Limitations: The synchronous engine must really enforce deadlines. First cancellation may wait for bounded cleanup; do not apply this to unbounded workers.
- Source: [AI alpha integration validation](/home/example/coding/ai-twitter-alpha/docs/postmortem/2026-10-06-integration-validation.md) (SHA-256 `c11665ca0e0c`; reviewed alias in [sources.json](../sources.json)).


## local-playwright-explicit-sandboxed-channel

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: Downloaded Playwright Chromium reports No usable sandbox on a host where packaged Chrome can run sandboxed.
- Applicability: Local Playwright 1.63.0 persistent-profile workflows on this inspected Linux host.
- Diagnostic checks: Run a synthetic-only launch with chromium_sandbox=True and inspect the failure privately. Test the same complete fixture with an explicitly selected installed channel, including persisted cookies and headless restart.
- Remedy: Keep the sandbox enabled. Allow an explicit configured chrome channel only after its fixture passes; do not silently fallback or alter OS sandbox policy. Give synthetic persistent cookies future expiry and test expiration separately.
- Verification evidence: Default Chromium 153 remained blocked. Installed Chrome 146 passed headed/headless persistence, private synthetic twscrape import, collision, expiry, renewal and shutdown through the completed CLI.
- Limitations: The bundled-browser host defect remains. Chrome 146/Playwright 1.63 compatibility is demonstrated only for this fixture; live accounts, future versions and real human takeover remain unverified.
- Source: [AI alpha integration validation](/home/example/coding/ai-twitter-alpha/docs/postmortem/2026-10-06-integration-validation.md) (SHA-256 `c11665ca0e0c`; reviewed alias in [sources.json](../sources.json)).


## local-systemd-venv-runtime-paths

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: systemd rejects a quoted WorkingDirectory as non-absolute.; Resolving a venv Python symlink can remove its installed-package context.
- Applicability: Rendered systemd user units for a Python application installed in a virtual environment.
- Diagnostic checks: Run actual systemd-analyze --user verify, including path quoting/expansion edge cases. Exercise the installed package and unit command outside the source checkout.
- Remedy: Use a neutral WorkingDirectory=/ with absolute app/config arguments when cwd is unnecessary. Prefer the regular installed console script so its shebang retains the venv, and escape systemd arguments according to each field semantics.
- Verification evidence: Actual unit parser caught WorkingDirectory and executable-dollar defects before fixes; 7 service fixtures plus temporary installed-wheel help/status/rendering and systemd verification passed.
- Limitations: Unit parsing and equivalent manager environment tests do not prove an activated user-service process. Activation still requires its own reviewed live check.
- Source: [AI alpha integration validation](/home/example/coding/ai-twitter-alpha/docs/postmortem/2026-10-06-integration-validation.md) (SHA-256 `c11665ca0e0c`; reviewed alias in [sources.json](../sources.json)).

## local-dbus-readiness-no-activation

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Private Dunst fixture autoactivated default daemon during dunstctl readiness; Name acquisition conflict before defining integration RED
- Applicability: Private DBus service fixtures whose readiness commands address an activatable service.
- Diagnostic checks: Compare daemon PID/ownership with DBus activation logs. Check whether readiness targets the service before it owns its name.
- Remedy: Poll org.freedesktop.DBus.NameHasOwner without addressing the service, then verify the explicitly launched daemon is alive before service calls.
- Verification evidence: Corrected RED contained no competing activation; private Xvfb/DBus integration passed and cleaned its own daemon.
- Limitations: This proves fixture startup ownership, not live desktop audio or production daemon repair.
- Source: [Dunst fixture startup](/home/example/linux-config/docs/postmortem/2026-10-07-dunst-fixture-startup.md) (SHA-256 `0ecc5a5310ac`).
