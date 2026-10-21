# Editing and shell transport

Use these reviewed findings to compare a failure with prior evidence. Check applicability and diagnostics before choosing a remedy; keep its verification scope and limits explicit.

## local-fish-optional-scalar-test

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Fish login prints `test: Missing argument at index 6` when an optional VT variable is unset.
- Applicability: Fish conditions comparing optional scalar environment variables, including combined `test -a` expressions.
- Diagnostic checks: Run the actual condition with unset and empty variables; cover both DISPLAY states and login/non-login shells. Substitute only the side-effecting X executable.
- Remedy: Quote the optional scalar comparison operand so an unset value remains an empty argument. Preserve existing X startup eligibility and argv.
- Verification evidence: Defining RED reproduced two missing-VT failures; all eight source scenarios passed after quoting. Three installed login startups passed with exit 0 and zero stderr bytes after allowing normal local startup writes.
- Limitations: No physical-console X session was launched. Inspect actual managed/ignored scope before inferring deployment from a raw template; this host's local Fish config is unmanaged. Subsequent normal refresh completed after a launcher-mode conflict was reconciled. Existing alias/GPG regressions were blocked by baseline fixture defects.
- Sources:
  - [Fish login missing VT](../../../../docs/postmortem/2026-10-20-fish-login-missing-vtnr.md); full hash and aliases live in [sources.json](../sources.json).

## ext-fish-safe-argv-transport

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: fish Unexpected ')' for unopened parenthesis; nested shlex quoting fails before sudo; Bash/Dash pass but actual fish helper fails
- Applicability: SSH launchers embedding Python source/backslash escapes through a fish login shell.
- Diagnostic checks: Run the actual launcher source under fish as well as POSIX shells.; Verify the password never appears in argv, encoded arguments or logs.; Separate parse failure before sudo from authentication rejection.
- Remedy: Base64-encode the JSON argument vector and use a constant quote-safe Python execvp launcher; keep passwords exclusively on stdin.
- Verification evidence: Actual-source fish regression failed before fix; six transport tests passed across fish/Bash/Dash; remote read-only marker and operator inventory retry succeeded.
- Limitations: Base64 is transport encoding, not encryption. Preserve strict host verification and avoid putting secrets in the encoded vector.
- Sources:
  - [2026-10-04-vps-recovery-sudo.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-04-vps-recovery-sudo.md) (SHA-256 `916c731f2bfb`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-manual-git-hunk-truncation

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: Unexpected end of file transforming new TSX test; outer describe closure absent; zero-context Git hunk declares too few added lines
- Applicability: Hand-constructed Git patches whose declared line counts do not match payload.
- Diagnostic checks: Compare hunk counts to actual payload and inspect the complete modified file.; Ensure test collection reaches the intended RED assertion after syntax repair.
- Remedy: Restore the omitted closure using a checked narrow edit; prefer supported patch tooling over hand-counted transport.
- Verification evidence: The report states the closure was restored and suite rerun, but records no explicit pass result; the same issue recurred on a later fallback patch.
- Limitations: A transform failure is a harness/edit failure, not the intended behavioral RED. Do not claim the regression passed from this report alone.
- Sources:
  - [2026-08-19-test-patch-truncation.md](/home/example/coding/lucas/lucas-java-4/docs/postmortem/2026-08-19-test-patch-truncation.md) (SHA-256 `e7d2ca15f869`; 2 alias(es), all retained in [sources.json](../sources.json)).

## ext-patch-delimiter-validation

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Invalid patch: last line must be *** End Patch; inserted patch line missing + prefix; missing files after malformed patch command
- Applicability: Transporting patch text through shell or patch tools.
- Diagnostic checks: Validate the end delimiter and every added-line prefix.; Confirm actual file creation before running dependent validation.
- Remedy: Correct patch framing before retrying and rerun the intended test setup against the created files.
- Verification evidence: The infrastructure report explicitly marks the initial malformed delimiter resolved before intended RED setup; later missing-prefix attempts report no applied files.
- Limitations: Other fixture/sudo/application checks in the same living report were still in progress; patch syntax repair alone is not their verification.
- Sources:
  - [2026-09-23-infrastructure-patch-failure.md](/home/example/coding/example-client-app/docs/postmortem/2026-09-23-infrastructure-patch-failure.md) (SHA-256 `bc27ed7ce2b0`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-patch-operation-contract

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: apply_patch duplicate target; Delete and Add for same path rejected; empty hunk rejected; conflicting patch operations
- Applicability: Patch-tool rewrites of existing files.
- Diagnostic checks: Check one supported operation per path and nonempty hunks.; Inspect status/diff after rejection before assuming no partial edits.
- Remedy: Use an Update operation for an existing-file rewrite; avoid delete/add pairs for one path in one patch and remove empty hunks.
- Verification evidence: Guide rewrites completed using Update operations; storage report records syntax correction; later infrastructure documentation used a single authorized write after rejection.
- Limitations: Prefer in-place updates to preserve existing state. Some tools can partially apply multi-file hunks, so rejection alone is not proof of atomicity.
- Sources:
  - [2026-10-05-guide-patch-operation-conflict.md](/home/example/coding/codex-usage/docs/postmortem/2026-10-05-guide-patch-operation-conflict.md) (SHA-256 `105f85ae3484`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-storage-patch-replacement.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-storage-patch-replacement.md) (SHA-256 `95a6a94a4f06`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-final-static-checks.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-final-static-checks.md) (SHA-256 `c4b9eee4d99b`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-vps-workflow-inspection.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-04-vps-workflow-inspection.md) (SHA-256 `409c6dd1137b`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-pipefail-full-output-drain

Chrome updater follow-up: a large Bash policy producer returned status 1 on the broken pipe (not necessarily 141). Drain policy output fully and handle a failed query explicitly before interpreting its result. The six-scenario regression passes; a subsequent user sudo run confirms visible activity and installation, while the original silent-failure environment remains unconfirmed. See [Chrome updater silent exit](../../../../docs/postmortem/2026-10-20-chrome-updater-silent-exit.md).

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: installer only prints banner then exits; apt-cache pipeline status 141; early parser exit under pipefail causes SIGPIPE
- Applicability: Shell pipelines whose producer can exceed the pipe buffer and whose parser exits after an early match.
- Diagnostic checks: Reproduce with package-policy output larger than a pipe buffer.; Inspect every pipeline status under pipefail.; Exercise cached/uncached sudo cases without requiring a real install.
- Remedy: Drain all producer output while selecting the candidate; use the same full-drain rule for collection presence checks. Print chosen packages before authentication.
- Verification evidence: Large-output regression failed before correction then passed with both Docker and Ubuntu package names and uncached-auth fixture cases.
- Limitations: Short fake output can hide SIGPIPE. Real package installation remains a separately tracked operator step.
- Sources:
  - [2026-10-02-buildx-prerequisite-install.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-02-buildx-prerequisite-install.md) (SHA-256 `cf43ab9afa7c`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-python-integration-syntax

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: IndentationError unexpected indent across test imports; str object is not callable in formatted conditional text
- Applicability: Adjacent Python feature integrations that alter indentation or combine strings with a parenthesized conditional.
- Diagnostic checks: Inspect the fully assembled source block, not only a patch hunk.; Run compilation with SyntaxWarnings promoted and full test import collection.; Compare stale fixture assertions to intentionally changed display rules before modifying them.
- Remedy: Align assignments to the existing enclosing block and add explicit string concatenation where a parenthesized expression would otherwise be parsed as a call; then verify the complete module and regressions.
- Verification evidence: Indentation repair passed 136 tests and Pyright; formatted status repair passed 97 tests, type checks and compilation with SyntaxWarnings as errors.
- Limitations: These are syntax/integration fixes; changing a stale assertion requires independent confirmation of the intended behavior, not a generic green-test shortcut.
- Sources:
  - [2026-10-02-cap-exemption-status.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-02-cap-exemption-status.md) (SHA-256 `85df04c55624`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-reader-recovery-indentation.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-03-reader-recovery-indentation.md) (SHA-256 `3568288a66de`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-remote-login-shell

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: SSH auth succeeds but fish rejects POSIX conditionals; remote audit exit 127; fish Expected end of statement
- Applicability: SSH accounts with a non-POSIX configured login shell.
- Diagnostic checks: Identify the remote login shell and how SSH interprets command text.; Exercise a harmless explicit-shell read-only probe before maintenance commands.
- Remedy: Invoke an explicit POSIX shell and transport the audit script on standard input instead of relying on the account login shell's syntax.
- Verification evidence: The sh -s retry exited 0 and returned OS, capacity, ports, services, Docker and sudo information.
- Limitations: Shell startup warnings may remain separate dotfiles issues; an explicit inner shell still needs a quote-safe outer launcher.
- Sources:
  - [2026-10-02-vps-audit-shell.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-02-vps-audit-shell.md) (SHA-256 `f1c860c739ca`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-stale-patch-context

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: apply_patch expected text not present; paragraph rewrapped after review; multi-file patch stops on stale context
- Applicability: Edits after concurrent/preceding changes or documentation rewrapping.
- Diagnostic checks: Re-read the exact current block before retrying.; Inspect the entire status/diff after rejection; multi-file attempts may have partially applied independent hunks.
- Remedy: Use smaller targeted patches against current contents and preserve earlier edits. Do not retry the same stale context blindly.
- Verification evidence: Guided-build cleanup completed with 21 tests, lint, build and diff check passing; several bot reports record corrected context and full suites passing.
- Limitations: Reports differ in patch atomicity: one relay attempt applied its first two hunks before stopping. Never assume rejection implies every file is unchanged.
- Sources:
  - [2026-08-19-guided-build-cleanup-patch.md](/home/example/coding/lucas/lucas-java-4/docs/postmortem/2026-08-19-guided-build-cleanup-patch.md) (SHA-256 `30e44e709a5b`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-08-19-raise-pitch-patch-mismatch.md](/home/example/coding/lucas/lucas-java-4/docs/postmortem/2026-08-19-raise-pitch-patch-mismatch.md) (SHA-256 `822d744595d3`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-02-relay-rollout-workflow-context.md](/home/example/coding/example-client-app/docs/postmortem/2026-09-02-relay-rollout-workflow-context.md) (SHA-256 `1495be749834`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-02-staging-infrastructure-readiness.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-02-staging-infrastructure-readiness.md) (SHA-256 `e5094af323a6`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-02-cap-empty-candidate-patch.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-02-cap-empty-candidate-patch.md) (SHA-256 `99571b401bab`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-02-dashboard-format-patch.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-02-dashboard-format-patch.md) (SHA-256 `00647cf1f533`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-final-static-checks.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-final-static-checks.md) (SHA-256 `c4b9eee4d99b`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-stdin-consumed-by-child

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: backup rehearsal standalone log empty; docker compose exec consumes later bash -s checks; script exits without expected evidence markers
- Applicability: Shell scripts sent on stdin that launch child commands inheriting the same stream.
- Diagnostic checks: Identify child commands that read inherited stdin.; Require explicit success/failure markers in evidence logs rather than trusting an empty log or exit status.
- Remedy: Redirect noninteractive child query stdin from /dev/null so it cannot consume the parent script stream; rerun the complete evidence harness.
- Verification evidence: Fresh isolated rehearsal completed with explicit backup, restore and failure markers; parent independently inspected logs and unchanged service snapshots.
- Limitations: This protects script transport and does not itself validate backup correctness; retain independent hash/restore evidence.
- Sources:
  - [2026-10-04-vps-workflow-inspection.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-04-vps-workflow-inspection.md) (SHA-256 `409c6dd1137b`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-bash-dynamic-output-scope

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: answer: unbound variable after interactive prompt; help and noninteractive dry-run pass
- Applicability: Bash helper writing a named caller variable with printf -v under set -u.
- Diagnostic checks: Exercise real interactive dry-run input.; Check helper local names against caller output variable names.
- Remedy: Use a distinct helper-local input name so printf -v reaches the caller output variable under Bash dynamic scoping.
- Verification evidence: Same interactive dry-run completed selection, confirmations and plan with no writes; syntax/help checks also passed.
- Limitations: Syntax and noninteractive checks did not exercise this path. The successful dry-run performed no privileged or destructive action.
- Sources:
  - [2026-09-27-hdd-wizard-prompt-unbound.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-27-hdd-wizard-prompt-unbound.md) (SHA-256 `cbffe02452f9`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-large-artifact-argument-limit

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: Argument list too long (os error 7); serialization command rejected before execution
- Applicability: Large reviewed artifacts transported through command arguments
- Diagnostic checks: Distinguish tool rejection before execution from partial writes; Measure artifact size; parse final output and reconcile source coverage
- Remedy: Write the authorized file through bounded chunks or a file stream, then validate the whole artifact.
- Verification evidence: Eight bounded writes produced valid 112,282-byte JSON; independent discovery matched all 76 external hashes and 87 aliases.
- Limitations: Chunking does not validate content or make writes atomic. Avoid placing secrets in command arguments.
- Sources:
  - [2026-10-05-postmortem-memory-artifact-transport.md](/home/example/linux-config/docs/postmortem/2026-10-05-postmortem-memory-artifact-transport.md) (SHA-256 `9dcef1a66ab8`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-login-output-newline-handshake

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Could not read login shell environment despite SSH exit 0; Fish ESC[6 q precedes marker without newline; ordinary remote failure incorrectly suggests host-key repair
- Applicability: Parsing marker-prefixed output from noisy login shells over SSH.
- Diagnostic checks: Probe raw startup bytes and number of exact marker lines.; Test real Fish cursor output and Bash banner without final newline.; Distinguish SSH transport exit 255 from remote command errors.
- Remedy: Print a newline after login startup before every parsed command; retain exact marker validation and restrict host-key advice to transport failures.
- Verification evidence: All 24 tests and Bash syntax passed; read-only real VPS probe correctly captured environment/type/version with exit 0.
- Limitations: The probe did not install or upgrade anything. Missing desktop startup warnings remain separate, and live update acceptance is still pending.
- Sources:
  - [2026-10-03-vps-codex-shell-handshake.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-vps-codex-shell-handshake.md) (SHA-256 `7c3664ca54b8`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-nested-language-literal-emission

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Perl replacement consumes Fish variables; literal $1 appears in shell source; Substitution replacement not terminated; bulk markup replacement creates Python SyntaxError
- Applicability: Fallback editing or generation crossing shell, Perl, Fish, Python and markup quoting boundaries.
- Diagnostic checks: Inspect exact resulting lines after each edit, including dollars, backreferences and embedded quotes.; Run the target language parser before regression execution.; Inspect partial changes after a multi-step replacement fails.
- Remedy: Prefer small explicit line edits or a reviewed generated diff; emit the target language variables literally and verify escaping on a sample before bulk replacement.
- Verification evidence: Fish syntax and focused regressions passed after literal rewrites; glyph fixtures collected and all 39 tests passed after quotes were corrected.
- Limitations: A failed compound edit may leave earlier mutations. The shell/transport syntax validator does not validate the generated language.
- Sources:
  - [2026-08-24-fn-progress-fish-variable-expansion.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-24-fn-progress-fish-variable-expansion.md) (SHA-256 `7966e31d8492`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-16-refresh-config-logging-edit-failure.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-16-refresh-config-logging-edit-failure.md) (SHA-256 `7f4b543adb96`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-16-rf-fix-edit-failure.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-16-rf-fix-edit-failure.md) (SHA-256 `964edca771b0`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-24-playback-glyph-test-expectations.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-24-playback-glyph-test-expectations.md) (SHA-256 `254846844ad9`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-regex-global-flags

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: Python re.error global flags not at the start after alternation
- Applicability: Temporary read-only documentation verification regex.
- Diagnostic checks: Inspect inline flag position before using checker output as evidence.
- Remedy: Put one global flag at the beginning or pass re.MULTILINE to the regex, then rerun the entire interrupted checker and inspect the artifact independently.
- Verification evidence: Corrected checker exited 0 and validated word count, labeled blocks, Bash examples and formatting; root independently reviewed the guide.
- Limitations: The failed checker supplies no verification evidence. This was not production-code failure; no tracked checker rewrite was necessary.
- Sources:
  - [2026-10-05-worktree-guide-verification-regex.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-05-worktree-guide-verification-regex.md) (SHA-256 `58d8926a1a6c`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-shell-command-substitution

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: read-only rg search unexpectedly executes git push; Markdown backticks inside double-quoted shell argument
- Applicability: Any shell-transported text containing backticks or command substitution.
- Diagnostic checks: Inspect quoting before executing shell strings.; Check refs and dirty state after an unexpected mutation.
- Remedy: Use literal single-quoted or otherwise correctly shell-escaped fixed-string patterns; treat shell command strings as code. Disclose accidental external changes and preserve published history.
- Verification evidence: Upstream movement and remaining uncommitted scope were measured; protected bytes stayed unchanged. Subsequent literal search patterns avoided interpolation.
- Limitations: Correcting quoting cannot undo a completed external action. Do not rewrite published history without authorization.
- Sources:
  - [2026-07-14-shell-interpolation-early-push.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-07-14-shell-interpolation-early-push.md) (SHA-256 `ead88fffd8f6`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-stale-patch-context

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: Failed to find expected lines; corrupt patch at line; wrapped prose or printf line mismatch; combined patch may leave prior hunks
- Applicability: Scoped edits after source changed, or fallback unified diffs when normal helper is unavailable.
- Diagnostic checks: Re-read exact current lines/tails, including embedded literal newline escapes.; Inspect target files to determine atomic versus partial failure.; Validate a generated patch before apply.
- Remedy: Regenerate the narrow diff against inspected current text; match complete source lines, remove unnecessary context hunks, apply only remaining changes and rerun focused/whitespace checks.
- Verification evidence: Reports record unchanged or inspected partial state, successful exact-context replacement and relevant checks passing.
- Limitations: Do not infer all tools are atomic. Verify each target after multi-file patch failure; avoid reapplying already completed hunks.
- Sources:
  - [2026-08-25-sandbox-read-and-patch-failures.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-25-sandbox-read-and-patch-failures.md) (SHA-256 `b1c6a9fa959e`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-01-smoke-test-patch-tooling.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-01-smoke-test-patch-tooling.md) (SHA-256 `139e9c6c9013`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-02-apply-patch-sandbox-failure.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-02-apply-patch-sandbox-failure.md) (SHA-256 `6622c74c1bad`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-24-mismatched-verification-commands.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-24-mismatched-verification-commands.md) (SHA-256 `46e5b1e40987`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-24-playback-glyph-test-expectations.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-24-playback-glyph-test-expectations.md) (SHA-256 `254846844ad9`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-27-hdd-wizard-patch-context-mismatch.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-27-hdd-wizard-patch-context-mismatch.md) (SHA-256 `7eba7d132adb`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-metaprompt-benchmark-validation.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-benchmark-validation.md) (SHA-256 `95a98d719b14`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-metaprompt-selection-validation.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-selection-validation.md) (SHA-256 `21607fa9f53f`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-kitty-scrollbar-inspection.md](/home/example/linux-config/docs/postmortem/2026-10-04-kitty-scrollbar-inspection.md) (SHA-256 `cac81ac1cb8c`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-metaprompt-session-scope.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-04-metaprompt-session-scope.md) (SHA-256 `ac02deccdb08`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-vps-prompt-delivery-patch-context.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-04-vps-prompt-delivery-patch-context.md) (SHA-256 `39c67958db27`; 1 alias(es), all retained in [sources.json](../sources.json)).


## local-codex-rendered-command-copy

- Status: **activation_pending**; root-cause confidence: **supported**; verification scope: **code**.
- Symptoms: Wrapped command selections may retain padding/hard breaks despite one physical source line; observed raw Python/JSON/diff blocks show literal fences and uniform color, while formatted view shows colors and indented hard command wrapping.
- Applicability: Codex CLI 0.162.0 npm TUI and the observed mixed-content/selection paths; verify version and rendering path before applying elsewhere.
- Diagnostic checks: Separate source syntax, visible colors, native selection bytes and exact clipboard/paste acceptance. Inspect startup raw mode separately from current view. Compare bare one-line fish commands with tagged Python/JSON/diff reading blocks in both views; verify exact wrapped selection/paste in a fresh fish terminal. Stale clipboards or wrong selection boundaries establish no copy outcome.
- Remedy: Apply the current bare-command/fenced-reading-code distinction without requiring session-wide raw rendering. Raw startup and /raw/Alt+R are supported copying options, not selective-rendering guarantees. Preserve the existing setting until an observed supported alternative meets actual paste and code-color requirements; otherwise report the exact observed limitation. See the [official configuration reference](https://developers.openai.com/codex/config-reference/).
- Verification evidence: Historical config deployment, no-inference config/read and refresh/install checks passed; the user confirmed raw fish-block colors separately. New screenshots show raw Python/JSON/diff uniform text and formatted token/diff colors. Native formatted clipboard fragments contain padding/hard breaks, but outer selection boundaries were invalid. Five source commands and syntax checks passed in fresh fish processes, exit 0; no rendering setting was changed.
- Limitations: Exact bare-command selection/paste/execution remains unverified. Invalid automation boundaries are not a raw-copy failure. Historical shell colors do not establish Python/JSON/diff colors or clipboard repair. No supported alternative has been shown to satisfy both outcomes; no binary/renderer/terminal patch was made.
- Sources:
  - [historical rendered-copy report](../../../../docs/postmortem/2026-10-09-codex-wrapped-command-padding.md) (reviewed historical source; prior user-confirmed shell colors preserved).
  - [mixed-content comparison](../../../../docs/postmortem/2026-10-09-codex-mixed-content-rendering.md) (reviewed current source; exact paste remains pending).

## local-ast-utf8-edit-columns

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Temporary AST edit produces SyntaxError near a multibyte character; byte columns were used as string indices.
- Applicability: Python source editing with AST line/column spans and Unicode text.
- Diagnostic checks: Compare UTF-8 byte offsets with character positions; parse each proposed file before writing and inspect already-written targets separately.
- Remedy: Convert byte columns to character positions (or consistently edit encoded bytes), replace right to left and parse before writing.
- Verification evidence: Corrected helper and seven defining tests passed; root independently parsed script/skill/benchmark sources and passed a multibyte offset probe.
- Limitations: Code editing correctness only; live activation and protocol safety require separate checks.
- Sources:
  - [CLI emoji edit offset incident](/home/example/linux-config/docs/postmortem/2026-10-09-cli-emoji-edit-offsets.md).
