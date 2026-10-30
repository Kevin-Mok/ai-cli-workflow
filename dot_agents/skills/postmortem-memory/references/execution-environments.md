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
- Symptoms: bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted; read-only commands fail before shell execution; patch helper cannot start; A necessary local HTTP test listener fails listen EPERM on127.0.0.1 in the restricted sandbox
- Applicability: Command runners whose restricted namespace cannot initialize loopback, or required local test listeners denied by the sandbox; distinguish environment permissions from application assertions and provider-classification bugs.
- Diagnostic checks: Confirm identical pre-execution error across independent harmless commands.; Capture repository status using a scoped command that actually executes.; Check that the target directory is a Git checkout rather than assuming one.; For listener failures, compare independent pure checks and rerun the same required socket command only under approved scoped loopback permission; do not alter the test or remove unrelated listeners.
- Remedy: Use the approved require_escalated route for the necessary scoped command when policy permits, or an available authorized workspace editor. Keep the host sandbox repair as separate outstanding work.
- Verification evidence: Multiple reports record successful approved source reads, status checks and verification after normal startup failed; application state was unchanged by failed launches. The PMO report separately records57 loader checks passing before a required bind failed,127 pure checks passing, then the approved combined25-file/276-test gate with typecheck/build passing.
- Limitations: Successful escalation does not repair default sandbox startup or authorize unrelated resources. One documentation report only prepared an add-only recovery and contains no completed verification. A passing socket gate does not fix the independently reproduced exclusive-end provider-classification defect or validate financial results.
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
  - [2026-10-30-review-loopback-permission.md](/home/kevin/coding/jay-tradingview/docs/postmortem/2026-10-30-review-loopback-permission.md) (SHA-256 `1317455932decd9baa5ba54f631cb4f51ab349e5baee102001ea418963bf9a35`; scoped required-listener verification).


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
  - [2026-10-06-burn-install-backup-preflight.md](/home/example/coding/track-codex-sessions/docs/postmortem/2026-10-06-burn-install-backup-preflight.md) (SHA-256 `7873cc3332ad`; 1 alias retained in [sources.json](../sources.json)).


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

## local-tmux-binding-command-transport

- Status: verified_fix
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: A multi-command tmux bind-key reload stores only select-pane while later copy-mode commands run immediately
- Applicability: Shell transport of semicolon-separated tmux binding bodies through the tmux client CLI.
- Diagnostics: Inspect list-keys for the full stored binding body after reloading.; Check whether escaped semicolons reached tmux as separate client command separators instead of part of the binding.
- Remedy: Write the intended binding configuration to a scoped file and use tmux source-file to install it. Restore only transient state caused by the failed reload; do not reset sessions/history.
- Verification: Initial list-keys showed only select-pane and current pane entered copy mode at position5. Scoped source-file restored full root and emacs/vi binding bodies; transient mode canceled. Subsequent PTY and isolated Kitty event checks passed.
- Limitations: Verified for installed tmux3.4 and these mouse bindings; do not infer all quoting or shell transport is fixed. Reload only authorized options.
- Source: [tmux scrolling diagnosis](../../../../docs/postmortem/2026-10-13-tmux-scrolling.md) (SHA-256 `8a1c8ba042b176a7612ebe0b94a68c6e1c912130bd3a9b11d10b1ae660574484`).

## local-virtualenv-interpreter-path-identity

- Status: verified_workaround
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: Resolving an installed Python virtualenv shebang symlink loses package metadata.
- Applicability: Read-only installed-package identity checks and isolated Python CLI benchmarks launched from a virtualenv shebang.
- Diagnostics: Read the installed entrypoint shebang literally.; Verify interpreter imports and distribution metadata before treating a resolved executable as equivalent.
- Remedy: Invoke the literal virtualenv interpreter path; verify Python, package metadata and source identity in that environment.
- Verification: The resolved system interpreter lacked package metadata. Literal installed-tool Python 3.12.3 imported the package and resolved Store/layout; all 39 Python modules plus package JSON matched the starting checkout.
- Limitations: Environment identity does not establish benchmark speed, arbitrary schema compatibility or activation of later source changes. Unknown benchmark SIGTERM sender remains unresolved.
- Source: [Tracker latency investigation](/home/kevin/coding/track-codex-sessions/docs/postmortem/2026-10-22-latency-discovery-paths.md) (SHA-256 `9fa4f1017c4bce1f9b7733a09c97b6e2562178e309755a63e28388e0c71cb52c`).

## local-cli-benchmark-startup-cache-parity

- Status: verified_fix
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: Source hashes match intended changes but only the baseline has valid project bytecode caches during complete CLI timing.
- Applicability: Python subprocess latency comparisons that copy source trees or run preparatory imports/selfchecks.
- Diagnostics: Inventory generated project caches on both sides, separately from deployable source identity.; Verify interpreter magic, cache flags and source timestamp/size; inspect bytecode read traces.; Remember that PYTHONDONTWRITEBYTECODE disables writes while existing valid caches can still be read.
- Remedy: Prepare isolated comparator copies with the same startup-cache policy; validate both before every report/index subprocess outside the wall timer. Keep preparatory imports from warming only one side. Preserve rejected observations and restart fair timing rather than subtracting a correction factor.
- Verification: Six valid baseline caches versus zero candidate caches reproduced the failed parity gate. Clean 40-file copies passed zero-versus-zero; runtime preflights enforce disabled writes, optimize0 and no cache prefix. Five-pair controls traced all six reads only on cached side; medians changed direction between two controls. Independent xhigh review approved source/protocol/cache identities and fair initialization.
- Limitations: This fixes private benchmark startup equivalence, not report performance, ambient variance or live activation. Old timings cannot drive retention/stopping. Prior full JSON parity remains semantic evidence only for identical source/content/options at its original absolute paths after bytecode equivalence is proved. Later same-source stale-index control differed by 4.933s in median; case-specific null controls do not supply a correction factor or a verified ambient-noise remedy. R6 fixed-six workflows all closed with source40/cache0 and original measurements preserved: same-code cold-status medians40.405324468 versus38.783259091 (wall1.622065377/CPU1.484028), larger than baseline/candidate repeat0.632088823. Independent attribution review99db6632 leaves R6 inconclusive/unretained/counter0; these controls are variation evidence, never a correction factor, universal noise floor, zero-effect proof or performance fix.
- Source: [Tracker latency investigation](/home/kevin/coding/track-codex-sessions/docs/postmortem/2026-10-22-latency-discovery-paths.md) (SHA-256 `9fa4f1017c4bce1f9b7733a09c97b6e2562178e309755a63e28388e0c71cb52c`).

## local-command-completion-launch-namespace

- Status: verified_workaround
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: An outer exec cell completes after nested exec_command yields, while a partial test log and sandbox ps are mistaken for a stopped host check.; Offline profile summary processing can fail after the profiled CLI and primary result have completed.
- Applicability: Long-running tool orchestration with nested exec sessions and different sandbox versus approved-host PID namespaces.
- Diagnostics: Retain exec_command session_id and resume it with write_stdin; use functions.wait only for an outer yielded exec cell.; Compare log growth and process visibility in the same approved namespace as command launch before declaring termination or retrying.; Distinguish the CLI return status from offline consumer/wrapper completion; inspect saved primary artifacts before any rerun.
- Remedy: Keep nested session handles until completion. If a handle was already discarded, await the original wrapper explicit per-command exit statuses and final source-hash manifest; do not start duplicate checks from a partial response or an unrelated PID namespace. If complete raw profile/results survive a secondary summary error, use a separately recorded offline consumer with pinned artifacts rather than repeating the profile. Derive offline postguard inputs from saved manifests and frozen files, not globals initialized in a previous adapter process.
- Verification: The partial pytest log advanced from51to74to82percent; approved host ps showed the original pytest alive while default ps saw only sandboxPID1. Without rerun, the original wrapper recorded610tests, Ruff, offlinebuild and279smoketests all exit0 with unchanged start/end task hashes. A later single cold-status profile returned0 before pstats(Path) failed; separate pstats(str(path)) processing recovered its summary/postguards with all seven primary hashes unchanged and no new CLI/profile execution.
- Limitations: This recovers completion evidence for an already instrumented wrapper, not a discarded tool handle or a truly terminated process. It does not diagnose unknown SIGTERM events, grant broader execution scope or prove that arbitrary partial logs represent success.
- Source: [Tracker latency investigation](/home/kevin/coding/track-codex-sessions/docs/postmortem/2026-10-22-latency-discovery-paths.md) (SHA-256 `9fa4f1017c4bce1f9b7733a09c97b6e2562178e309755a63e28388e0c71cb52c`).

## local-cli-benchmark-disposable-index-space

- Status: verified_workaround
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: Repeated private per-case SQLite index copies exhaust /tmp before the next parity report starts, and even default sandbox setup fails with ENOSPC.
- Applicability: Private CLI benchmark runs retaining many disposable per-case index states alongside immutable sources, frozen inputs and raw evidence.
- Diagnostics: Check bytes and inodes in the execution namespace; distinguish setup failure from report mismatch.; Inventory exact completed-case cache files, check task ownership, symlinks and lock state, and record protected evidence hashes before cleanup.; Keep read-only protected evidence roots separate from disposable unlink roots; preserve an inherited external helper only by its exact approved path and SHA, never by broadening deletion scope.; Historical inventory sizes do not prove current existence or reclaimable capacity; compare fresh paths/stat observations with prior cleanup receipts and do not infer intervening deletion without earlier live evidence.
- Remedy: Under the existing exclusive measurement lock, reclaim only specifically inventoried completed per-case disposable indexes. Preserve source, frozen/native inputs, masters, raw stdout/stderr, manifests, results and active checkpoints; verify hashes and free space before resuming unchanged code/protocol. Budget subsequent copies and clean completed disposable states outside timed intervals.
- Verification: Case14 parity setup failed before CLI launch with13exactcases preserved. Approved cleanup removed150regular index.sqlite/wal/shm files from completed round1-fair states,20,747,673,600logical bytes; freebytes0to20,697,808,896. Parent independently rehashed714protected files; checkpoint13unchanged, ordinary sandbox restored and all26parity completed. Separately approved156parity-template unlinks reclaimed21,577,367,552bytes; parent verified156pathsabsent/197hashesunchanged. All26human cases then completed260timed subprocesses exit0 with headroom checks. A third approved150-file timing-state cleanup reclaimed20,747,468,800bytes before controls; parent verified exact paths and all43,799protected hashes before/after, free30,184,804,352bytes. First fresh-state projects control completed successfully. Later R6 audit overconstrained protected reads to the runtime root and rejected its own exact pinned external helper. A one-predicate path+SHA exception passed defining V1-RED/V2-GREEN and11fixtures, independent xhigh review, then same-primary real audit69936 with7823protected hashes preserved pre/post and only6templates removed; no report rerun. Later allocation-only +4096 drift on a copied template retained dev/inode/size/mtime and exact master DB bytes. V3 permits only index.sqlite with fresh authoritative-master SHA on that mismatch, keeps WAL/SHM strict and exact prior verifier pins, and passed defining RED/GREEN15fixtures/xhigh plus actual case2audit3881 with7846protected hashes and exact6cleanup; allocation delta recorded, kernel cause unproved. R6 human case25 preflight74832 and later case26 preflight10792 each actually exited1 at the unchanged actual/projected4GB floor before setup/report. The original transcript recovered the first exact traceback; the second output is separately saved. Transient free-space recovery allowed case25 with all four reviewed stages terminal0, but did not establish durable headroom. At that stop, prefix25/26 was held; the failure alone did not authorize further cleanup or a capacity remedy. Subsequent reviewed exact24 diagnostic/control cleanup23533 actually completed0 after inventory41889/audit84251 and a qualified fresh host/FD gate. All24absent, 73893protectedhashes matched before/after, 3319595008logicalbytes removed; profiles/raw/source/master/DATA/native/statuscache/catalog preserved. This scoped capacity recovery still requires a fresh case26 preflight; no performance or noise-attribution claim follows.
- Limitations: Verified scoped environment recovery and bounded parity/human-matrix lifecycle, not a product speedup, global cleanup authorization or guarantee against recurrence. Later fresh-control preflights use a conservative4GB floor; low-space rejection was not deliberately exercised. Completed runtime caches were intentionally removed while reproducible source/input/protocol/raw evidence and masters remain.
- Source: [Tracker latency investigation](/home/kevin/coding/track-codex-sessions/docs/postmortem/2026-10-22-latency-discovery-paths.md) (SHA-256 `9fa4f1017c4bce1f9b7733a09c97b6e2562178e309755a63e28388e0c71cb52c`).

## local-tracker-validation-runtime

- Status: verified_workaround
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: Tracker integration tests fail creating canonical Path.home .local/state/codex-time/locks in a read-only sandbox, or binding isolated Unix sockets.; An empty task-selected UV_CACHE_DIR makes offline setup/build unable to find cached hatchling; restricted default-cache access can fail opening sdists-v9/.git before collection; secondary async teardown may appear stuck.
- Applicability: This repository focused/full pytest, setup/build and smoke checks whose isolated fixtures still use canonical home locks, Unix sockets and the documented existing uv cache.
- Diagnostics: Read actual failure traces and retained source hashes before attributing failures to the candidate.; Distinguish Path.home canonical locks from XDG overrides; match process observations to launch namespace.; Check cache identity and preserve the original log; use per-test faulthandler diagnostics for a recurrent stall.
- Remedy: Run the existing isolated-fixture checks with explicitly requested approved normal permissions and the documented default uv cache; do not silently fall back to restricted execution; unset only the task-added empty cache override. Keep offline build and existing dependencies. Do not change product locking, weaken assertions, download dependencies or restart live services to satisfy sandbox failures.
- Verification: Restricted checks showed Errno30 canonical locks, Unix socket EPERM and uncached hatchling; after bounded diagnostic interrupts, the same unchanged candidate passed three exact failing writer/socket/FX representatives, full621tests, repositoryRuff, offline sdist/wheel and279smoketests plus exact1320000tokens/USD2.91/CAD3.9285. Parent checked all six source/test hashes before/after/current and explicit exit0 logs. Later retained-R4 focused restoration hit restricted cache Errno30 before collection; explicit normal permissions passed51tests with exact full source/test paths and matching start/end hashes. Fresh retained-final verification again incorrectly used restricted launch: defaultUVcacheE30 then privateUVoverride allowed621collection but27failed/182passed and FXepollstall; oneidentity-verifiedpytestSIGINT0/originalexit2, availabletraces explicitlypartial2e23ceb449b752e391cd454f0db2338aa432948da626b390556d8f7f2bd1d036. Lookupaf6255/reference0171f6 applied this existing normal-permission/defaultUVcache remedy. Corrected focused6passed5.51s/full621passed86.60s/mypy39/Ruff/offlinebuild/smoke279passed33.06s, exact1320000tokens/USD2.91/CAD3.9285@1.35; fullfilelogs/literalcontext/beforeafter40source-test maps bind final-summaryd3ce9d275ea93a93e50b53a474a9150c67ce38c8c80ef5d35d0c3ef5bcec18aa/rootread36c457/a6696c. No app/test/dependency changes; restrictedFXtimeout origin remainsunproved, correctedcontextpassonly.
- Limitations: Verified test/build environment workaround for isolated fixtures, not an optimization gain, general sandbox escape authorization, live deployment, or a diagnosis of every FX timeout. The restricted-run blank TimeoutError origin remains unproved; only its corrected-environment pass is established.
- Source: [Tracker latency investigation](/home/kevin/coding/track-codex-sessions/docs/postmortem/2026-10-22-latency-discovery-paths.md) (SHA-256 `9fa4f1017c4bce1f9b7733a09c97b6e2562178e309755a63e28388e0c71cb52c`).

## local-collaboration-idle-agent-dispatch

- Status: verified_workaround
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: A revision request delivered with collaboration.send_message to a completed worker produces no new turn or artifact.
- Applicability: The collaboration namespace when requesting additional work from an idle or completed child agent.
- Diagnostics: Read the actual tool lifecycle descriptions; inspect live agent state rather than infer execution from successful delivery.; Coordinate a single wake when another agent may already have issued a followup.
- Remedy: Use collaboration.followup_task to start authorized idle work; use send_message for information delivery. Retain actual completion evidence and do not treat running state as success.
- Verification: The consumer producer remained completed after parent send_message requests. An auditor followup_task started the bounded revision; parent observed running without duplicate wake. Producer published V2 consumer dbc0946a and readiness343889da with actual inline0e895e terminal0 and26 synthetic checks; parent reviewed the exact diff.
- Limitations: Verified dispatch recovery in the collaboration namespace only, not a product or benchmark gain, completion inferred from delivery, or a lifecycle contract for differently named native messaging tools.
- Source: [Tracker latency investigation](/home/kevin/coding/track-codex-sessions/docs/postmortem/2026-10-22-latency-discovery-paths.md) (SHA-256 `9fa4f1017c4bce1f9b7733a09c97b6e2562178e309755a63e28388e0c71cb52c`).

## local-cli-retained-manifest-path-order

- Status: verified_fix
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: An offline retained-cache audit rejects unchanged session-status.json because saved and current descriptor lists have different traversal order.
- Applicability: This tracker private benchmark descriptor comparison when a producer retains filesystem creation order and a verifier sorts rows.
- Diagnostics: Compare every saved/current descriptor by canonical path, including complete content SHA and every recorded stat field.; Inspect producer collection order, verifier sorting and positional zip comparisons before assuming a cache metadata change.
- Remedy: Require unique paths and exactly equal path sets, then compare all existing identity, permission and content fields by path; independently bind the current enumerated verifier and recognize only the exact historical producer tuple. Preserve immutable primary evidence and pin the corrected verifier independently; do not rewrite inventories, rerun timings or waive timestamp checks.
- Verification: First BCstatus adapter25947 and consumer70310 completed0; read-only audit93894 failed at positional retained comparison. Parent diagnosticc9117f31 found all eight retained files identical in every recorded field and SHA. Pure permutation reproducerf94427 failed frozenV2 as expected. Frozen V3 main de898ab9/helper e4a09b4b preserves all stable fields and exact path sets; fresh independent proof0844d88d passes all eight prior guards, four path-keyed groups, exact historical legacy then following-current real writers, omission/wrong-role/map negatives and four optimized refusals, with eleven file hashes unchanged. Current metadata publication95759 freshly verifies all9614 prior pins; static loader1cba74 accepts exact original V2 case01 release/map plus independently bound current verifier. Actual corrected case01 read-only audit24512 exited0 with receipt881ff0ea,9765protectedhashes,ten timed zeros/24captures, allsixruntime targets valid and zero deletions; completion6c20d0e4 binds actualargv/output. Original release, timing, consumer and inventory bytes stayed unchanged. Actual host gate98408 passed with qualified accessible visibility; clean57952/820c0f0d removed exactsix and preserved9768hashes; barrier82002/f198e3ea verified9770hashes, with actual cleanup78ca60d3 and barrierbed3fc57 external receipts. Five further fixed controls remain pending.
- Limitations: The cache-chmod-ctime precedent does not apply: no metadata drift was observed. Verification covers the first real control audit, guarded exact-six cleanup and completion barrier; five further controls remain pending. It is not a performance gain, permission to omit source/cache checks, or authorization for arbitrary verifier overlays. Original R6 remains unretained and stopping counter0.
- Source: [Tracker latency investigation](/home/kevin/coding/track-codex-sessions/docs/postmortem/2026-10-22-latency-discovery-paths.md) (SHA-256 `9fa4f1017c4bce1f9b7733a09c97b6e2562178e309755a63e28388e0c71cb52c`).

## local-cli-retained-report-budget

- Status: verified_fix
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: A completed cold all-time overview control cannot publish offline evidence because retained overview report caches exceed an assumed per-case nonindex allocation cap.
- Applicability: This tracker private fixed-control resource contract, including collector, prefix, audit, cleanup and remaining-peak guards.
- Diagnostics: Sum current per-file allocated blocks within the exact retained state scope and verify SQLite exclusions; distinguish logical bytes from allocated bytes.; Compare cap provenance with actual report-cache sizes and keep original primary, raw captures, state files and identities hash-bound before recovery.; Inspect every consumer of the cap and historical measurement/master readiness before revising a versioned contract.
- Remedy: Versioned bounded revision: add only the observed19365888B overview report-pair reserve to unchanged5000000B overhead, yielding24365888B overview cap; preserve162057024B status caps and4000000000B actual/projected floor. Version all affected guards coherently, separately bind original case02 measurement and current collector/verifier, retain original AP2 master origin, and recover offline collection without timing rerun.
- Verification: Actual adapter32533 completed0; consumer8278 failed before summary/inventory at5000000B. Source/stat diagnosis finds six retained files19447808B, of which paired overview JSON caches19365888B and checkpoint/FX81920B. Read-only snapshotba7f6777 protects121nonruntime byte hashes and six runtime identities/fullSHAs. AP2 previous/setup/remaining guards and P3 share the cap; versioned correction is preparation only. Fresh independent runner41920 completed0 with12 normal writer flows,24 expected optimized refusals,Ruff0 and22current+10old hashes unchanged. Qualified-clear source/metadata review preceded actual publication29524. Preserved case02 CP3collector60100, P4audit83359, qualified hostgate80863, exact6clean77354 and barrier47031 all actually exited0. Summaryf48aa291/inventorya2bd869e/audit439c2b94/cleanup65ea014d/barrier0379e807 preserve original timing/setup/release,121 snapshot nonruntime hashes and retained19447808B report files. Final barrier verifies9949 protected hashes and exact6 absent. All six fixed workflows subsequently closed with parent evidence indexf60587a4:60timed integerzeros/144captures/36exact runtime files absent, originalprimary63142356 unchanged; final barrier33903/443c59f2 verifies10480protectedhashes. Subsequent current collector/audit/gate/clean/barrier flows passed with status/overview caps and4GB floor unchanged.
- Limitations: Verified private preserved-case and subsequent fixed-six workflow scope at these actual cache sizes. Future rounds still need fresh source/input/provenance/allocation/capacity guards. This does not resolve ambient timing attribution, establish R6 gain or regression, authorize arbitrary cap increases/global cleanup, or prove live activation.
- Source: [Tracker latency investigation](/home/kevin/coding/track-codex-sessions/docs/postmortem/2026-10-22-latency-discovery-paths.md) (SHA-256 `9fa4f1017c4bce1f9b7733a09c97b6e2562178e309755a63e28388e0c71cb52c`).

## local-extracted-guard-trace-line-offset

- Status: verified_workaround
- Confidence: confirmed
- Verification scope: code
- Symptoms: An extracted-guard unittest has the expected failure count, but its displayed traceback appears to fail a different source assertion than the compiled guard.
- Applicability: Python guard/reproducer fragments compiled under a filename whose on-disk text omits an added wrapper/header.
- Diagnostics: Preserve actual output, input hashes and positive controls; do not accept totals alone.; Reconstruct the exact compiled text from pinned wrapper and fragment; map traceback code positions to its AST assertions.; Compare displayed linecache text with the capture and account for each wrapper or dedent explicitly.
- Remedy: Interpret the preserved traceback with the exact compiled-to-captured line map; append a qualified clarification while preserving original raw trace and prior incorrect interpretation. Do not rerun the target or change guards solely to clean printed source text.
- Verification: Actual OLD-RED61c9c9 returned1 with8tests,5intended failures,0errors and3positive controls; all13pins unchanged (output4c655621/pins68639c2f). Pinned test05db3081 prepends one function-header line to capture7fda3b00. Parent9340ed and independent xhigh review confirm compiledline3 is capturedline2 lineageassert, compiledline7 is capturedline6 status-only delta; candidate-map equality is compiledline8 and not reached. Separate clarification preserves the raw output/false observed_note; no test rerun or source modification.
- Limitations: This verifies diagnostic interpretation only, not a runtime behavior change or new harness GREEN. One-line offset applies only to this exact wrapper/capture; other wrappers, compiler transformations and filenames require their own mapping. Future runtime/publication/benchmark eligibility remain independently gated.
- Source: [Tracker latency investigation](/home/kevin/coding/track-codex-sessions/docs/postmortem/2026-10-22-latency-discovery-paths.md) (SHA-256 `9fa4f1017c4bce1f9b7733a09c97b6e2562178e309755a63e28388e0c71cb52c`).

## local-cli-tool-completion-output-fields

- Status: verified_fix
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: A successful independent audit is followed by a host-gate KeyError because the root-generated completion record used audit_sha256 instead of independent_audit_sha256.; A sealed current-case completion passes its local reader but the next parity preflight fails on missing recording_scope and five further resume-envelope fields.
- Applicability: This private R7 parent-owned tool-completion writer and every connected collector, driver, prefix and next-preflight consumer; not application accounting or a general alias policy.
- Diagnostics: Read all connected consumers and their exact output, scope and hash fields before constructing parent records; current-case acceptance alone does not prove a resumable prefix.; Bind receipt digest separately from output digest, preserve actual status/argv, and verify typed phase/case/preparation/readiness/role bindings at the next consumer boundary.; Check whether any successful dependent receipt or immutable prefix seals a malformed derived record; the earlier unsealed-only amendment exception never applies to a sealed completion.
- Remedy: Use explicit consumer fields for audit, gate, cleanup and barrier. For a barrier completion add literal recording_scope plus phase, strict-integer case_number, case, independent_audit_sha256 and cleanup_sha256 from its hash-bound immutable barrier. Validate the serialized candidate through the actual reader and exercise the actual first-case writer through the next preflight/resume consumer; do not prefill missing fields only in a fixture. Preserve the old sealed receipt and start a fresh namespace requiring all26cases when the closed pilot cannot resume. The earlier exact root-owned unsealed audit-receipt amendment remains a historical narrow exception requiring original-byte backup, unchanged primary evidence, no dependent references and the inherited lock.
- Verification: Original audit-field RED522d7357 and readerGREENbd104beb led to the separately verified unsealed amendment3e628b96, fresh gate27367, exact6cleanup67773 and barrier43593; original invalid41485e8f and all primary artifacts remain preserved. Later actual next-case preflight failed because sealed9f17ff13 lacked all six resume fields despite local completion acceptance. After the test-only fence was qualified, RED5223b73b exposed7intended missing-envelope failures/0errors. Exact root-v3 constructor31a24333 derives the six fields from the barrier; GREEN51d02ee2 passed4observer controls,3default/3plain actual-constructor-next-preflight checks andF821 with34pins unchanged. Frozen production guards were not relaxed; old sealed9f17ff13 was not amended. Fresh namespace publication10051/d4de77 then actually completed0 (proofd1434b64), preserving10871hashes/93Pfiles/221closed-pilot files. New case01 driver22946,collector33077,audit37169,gate52901,clean91482,barrier80740 all completed0; barrierb2ef5da2/completioned4d1c87 carries all six resume fields, twoJSONpairs/eightcaptures/exact6absent and10988final hashes. Actual case02preflight10615/8bc385 completed0 with preflight87ca20a9/entry64aec199 and10989prior hashes, verifying the real next-consumer boundary. Old sealed9f17ff13 remains unchanged. Full real fresh parity subsequently closed26cases/156actualactions0/47of47wholeJSONpairs/188captures (closurec9d9c588/root8b8385). Actual full26audit34076/def2e1, sharedgate37917/c1a1b2, exact3clean38403/cdad09 and handoff84618/598dbf all completed0; completion814b9708 binds audit+inventory, handoff69cd0391 binds exact shared scope/hash links, all11697protected/masterDBWAL preserved. Bindingd428347d was content-checked as a Notes candidate then exclusively published byte-identically after handoff; unchanged actual human.phase_binding passes11699pins with main-equivalent context and no root/validator patch. Firsthumanpreflight37584/246773 is now actual0: output6e6dd5b242996dcb36e6f0dc29548120be145f51101c4bb9622373fcf29d4b1b,4662B,entrynull; all11699pins/inputs/runtime/both4GBfloors passed and no normalhumanmaster created. Later all26human workflows closed:52warmups/260timed0/624captures. Corrected independent offline aggregatec9e3a8 returned0, closure2d5ca333738459896127c985a6fb25217c9ef59ed8367012731f829baca41b1e validates156primaryactions0+156metadatawriters0,312returnedrows0, canonical/rawlinks and all six-field barrier envelopes; matrixf04934b3e450df0bed344e677b8fe59c7755e17eb2aae50dd45a845cd02b1afc, finalbarrier740e9049/completionb09d6c6c. Initial offline reader42d7ab assumed flat external status fields for nested adapter/postconsumer envelopes; lookupb974c3/reference7ce61f and actualschema7de2df/de13a5 guided reader-only correction without any CLI rerun or receipt/input amendment. Independent global humanaudit40971 subsequently completed0: canonical445ed8184a740f92737febe8984a077ecfa93b3e6c94321b200ec1558ec10b2b/rawd60b456e4b12c6b603fb17b1dffd5cb95a07da0485a779eb08ba9cd2b320a11e verifies12879protected/312returned0/260timed/624captures/150absentruntime; rootfullread518c90/af4ce0. Candidate guardedarchivea66374d4 and restore5ad4d1 (restore4a5dd1d131981b557e2d7ef6c5c8217cd138776f163633a6b1c3b2ae4a21edc0) restored only3ISOmodules+test toretaineda5; private candidate evidence remains historical/unchanged.
- Limitations: The earlier audit-field amendment remains confined to the original unsealed case. Completion/resume/shared contracts are verified through owned fixtures and real fresh26JSON parity closure, full26audit/exact3shared cleanup/handoff and unchanged canonical phase-binding validation. This never repairs or credits the old sealed pilot. All26human workflow completion proves actual consumer/receipt boundaries, not attributable speed. Global humanaudit is accepted and guarded candidate archive/restoration toretaineda5 completed. Corrected xhigh ruling is inconclusive/unretained/counter0 with no verified gain or regression; R7 is incremental a5-to-ISO only, never task-original-to-final. Task-original package61ed3a55 still has unknown Git40. Separate original-to-retaineda5 direct cumulative comparison is now completed and parent-verified (result0065465fe9f9dc82f1984cf600d9cbf7d18c8fc3ed241ed5f4ea2cf47e07477c/verificationb3e0b0462c82f19e5f67d6582e9fd0e4f74badfd45f3d2f31aed6bb7c943c14b), with both gains and a consistent coldalloverview wall+CPU regression whose cause remains open; completion validity establishes no performance remedy. R7is unretained/restored; direct cumulative evidence is separate and does not erase adverse cases or prove plateau. Final stopping and any new improvement commit still require their own evidence; no additional timing solely to rescue the marginal ISO batch is recommended. Never amend sealed receipts, raw reports, source/input/master snapshots, pre-existing user work or history; no product activation claim follows.
- Source: [Tracker latency investigation](/home/kevin/coding/track-codex-sessions/docs/postmortem/2026-10-22-latency-discovery-paths.md) (SHA-256 `9fa4f1017c4bce1f9b7733a09c97b6e2562178e309755a63e28388e0c71cb52c`).

## local-linux-owned-audit-dir-fd-context

- Status: verified_fix
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: A Python test audit fence rejects a legitimate owned os.open basename with dir_fd because it resolves that basename against repository CWD; the same mistake can reject owned temporary-directory cleanup.
- Applicability: The hash-reviewed Linux owned-fixture audit observer for descriptor-relative os.open when Python audit event arguments omit dir_fd; test-only scope.
- Diagnostics: Preserve the initial setup error and distinguish0tests/1error from the intended target RED.; Inspect the actual syscall arguments and audit tuple; compare descriptor-relative target with the fence CWD interpretation.; Verify the owned directory FD through /proc/self/fd, canonical nonsymlink components and matching stat/fstat device+inode before admitting one synchronous audit observation.
- Remedy: Use a test-only observer that delegates the original os.open arguments unchanged while supplying verified owned dir_fd context to one matching synchronous audit event. Reject unscoped relative paths, outside directory descriptors, escapes, aliases and protected absolute writes; restore the previous thread-local context afterward. Keep production filesystem calls and guards unchanged.
- Verification: Initial39c143f6 failed in owned fixture setup before target assertions. Observer8838a60f corrected only the Linux test observation context; four controls passed. Qualified targetRED5223b73b then reached7intended constructor-envelope failures/0errors. GREEN51d02ee2 passed the same4observer controls and3default/3plain actual writer/next-preflight methods plusF821 with34source/proof pins unchanged. Old failed fixture/evidence were preserved; no actual W/home/pilot/repository operation was allowed by this probe.
- Limitations: Verified only in this owned Linux test process and its synchronous one-use observer contract. This is not a production sandbox, a general Python audit security guarantee, portable dir_fd behavior, authority to allow arbitrary relative paths, or evidence of application performance/live activation. The full captured operational writer template was never executed.
- Source: [Tracker latency investigation](/home/kevin/coding/track-codex-sessions/docs/postmortem/2026-10-22-latency-discovery-paths.md) (SHA-256 `9fa4f1017c4bce1f9b7733a09c97b6e2562178e309755a63e28388e0c71cb52c`).

## local-headless-tsx-loader-without-ipc

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: A pure TypeScript smoke command launched through the tsx executable fails at listen EPERM on a temporary tsx IPC pipe before calculation.
- Applicability: Headless TypeScript scripts that need the installed tsx loader but do not require the tsx CLI process IPC listener.
- Diagnostic checks: Distinguish launcher IPC failure from script calculation failure; inspect the exact denied listener path.; Run the same script via node --import tsx in the same default sandbox, then exercise the documented npm entrypoint.
- Remedy: For a pure headless script use node --import tsx script.ts rather than the tsx executable. Keep necessary application listeners and permission boundaries unchanged.
- Verification evidence: The original npm smoke failed at listen EPERM /tmp/tsx-1000/15.pipe. The direct Node loader succeeded; changing only the package script made the actual npm plain/JSON smoke exit 0 in the default sandbox with one costed synthetic round trip.
- Limitations: This avoids unnecessary launcher IPC; it does not repair or relax the sandbox listener restriction and does not prove a server or live trading path works.
- Source: [2026-10-29-backtest-cli-ipc.md](/home/kevin/coding/jay-tradingview/docs/postmortem/2026-10-29-backtest-cli-ipc.md) (SHA-256 `765fac437cd606073bcc5c7957f8b18b638bb6df88b672b9dcef070af4946add`).

## local-agent-slot-before-followup

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: Following up a completed agent is rejected with agent thread limit reached while the root and three other active children occupy the configured four execution slots.
- Applicability: Queued optional agent work in an orchestrator with a known bounded active execution pool; completed agent history does not itself reserve a free active slot.
- Diagnostic checks: Compare the configured active-slot cap with current root/child activity rather than counting only completed agent identities.; Wait for a worker completion notification before retrying the queued follow-up; verify the resumed turn actually starts.
- Remedy: Keep optional work queued until an existing active task demonstrably finishes, then resume it without interrupting required workers or repeatedly retrying at the cap.
- Verification evidence: The rejected request started no child turn or external mutation. After causal_backtest_core returned FINAL_ANSWER, the queued core_incident_learning turn started successfully and resumed three-report registration.
- Limitations: This observes a permitted resumption after capacity frees; it neither raises nor bypasses the configured concurrency limit and does not establish capacity behavior for a different orchestrator.
- Source: [2026-10-29-agent-capacity.md](/home/kevin/coding/jay-tradingview/docs/postmortem/2026-10-29-agent-capacity.md) (SHA-256 `1e3b9a2b7686d476a701a1dd03adbd93077d85e037e917344bbdb00d384550e7`).

## local-inert-test-archives

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: Vitest discovers an archived .test.ts under a Git-ignored cache and fails its relocated relative imports
- Applicability: Preserved retired experiments stored inside a project tree where the test runner still scans matching test suffixes.
- Diagnostic checks: Inspect the discovered failing file path rather than assuming Git ignore excludes it from test collection.; Distinguish retired archived artifacts from committed active regression tests.; Preserve archive bytes and verify the full active suite after making the archive inert.
- Remedy: Give the preserved archived test an inert suffix such as .test.ts.txt, or use a location already excluded by the runner. Do not delete or weaken active tests or change production discovery merely to hide a failure.
- Verification evidence: The initial combined gate passed276 active tests but failed on the relocated archived suite. Renaming only the archive suffix preserved its contents; the fresh gate passed25 files/276 tests, typecheck and build.
- Limitations: Git and test-runner discovery remain independent. The suffix remedy applies to intentionally retired artifacts, never to an active failing regression; the underlying test-runner configuration was not changed.
- Source: [2026-10-30-archived-test-discovery.md](/home/kevin/coding/jay-tradingview/docs/postmortem/2026-10-30-archived-test-discovery.md) (SHA-256 `a9888c3128bdd7ad095eb8e860a03971185d5d9ee63673eadcd4c62dda2af664`).
