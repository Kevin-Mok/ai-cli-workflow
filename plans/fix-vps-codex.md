# Repair VPS Codex Updates Over SSH

## Purpose And Observable Outcome

Provide one local executable, `scripts/executable_fix-vps-codex.sh`, which
diagnoses and fixes npm EACCES for Codex on a Linux VPS. A subsequent SSH login
must find the user-owned Codex installation and successfully run the ordinary
`npm install -g @openai/codex` command without sudo.

## Current Context And Scope

The screenshot shows a denied rename under `/usr/lib/node_modules/@openai`,
not evidence of an incompatible Node release. Local Codex 0.160.0 declares
Node `>=16`; remote requirements must be obtained from package metadata when
the script runs. The existing local fnm helper assumes a particular runtime
layout and its dry run changes files, so it is not reused as a VPS repair.

Protected initial dirty work: `docs/phone-ssh-public-ip.md`, the Phone To PC
SSH section of `docs/smoke-tests.md`, two pre-existing sandbox postmortems
dated September 30 and October 3, and `plans/diagnose-phone-ssh-access.md`.
No staging, commit, push, or remote repair is authorized by this handoff.

Scope includes the saved accepted prompt, new helper and tests, usage guide,
README entry, smoke checks, this plan, and incident notes. No worktree.

## Assumptions And Decisions

- Default SSH target: `example-user@192.0.2.10`; allow host, port, and identity
  overrides. Existing key/agent and SSH configuration are used. Host keys
  must already be trusted; fail closed on unknown or changed keys.
- The local entrypoint is Bash; its remote payload uses Python 3 standard
  library for JSON, subprocesses, backups, and official runtime downloads.
  Support Linux with bash or fish as login shell. Fail actionably otherwise.
- Dry run runs diagnostics and reads HTTPS metadata only; no remote temp
  files, npm commands that write caches, installs, or config writes.
- Reuse compatible Node/npm and a healthy writable user prefix. System npm
  gets a user-owned prefix. Avoid incompatible prefix settings for an active
  version manager; stop on ambiguous ownership/configuration.
- Only missing/incompatible Node/npm triggers an isolated official current
  LTS runtime under the user's home, verified against official SHA256 sums.
  Do not replace OS packages or change service runtimes.
- Back up changed user configuration privately and generate a rollback
  helper. Persist PATH for the detected shell. Repeat runs must not add
  duplicate shell blocks. A second SSH session verifies normal updating.
- Creating and locally testing the script is authorized; running it against
  the VPS remains the user's task. Do not claim a live repair or live proof.

## Ordered Implementation Checklist

- [x] Capture initial status; inspect instructions, accepted prompt, existing
  helper, preferences, and local installed Codex manifest.
- [x] Save the accepted prompt after leaving Plan Mode.
- [x] Write and observe failing behavioral tests with isolated SSH/npm
  substitutes, including an unwritable system prefix.
- [x] Implement diagnostics, minimal user-owned repair, backups, and fresh
  session verification, plus official runtime fallback when necessary.
- [x] Cover bash/fish, reruns, dry-run immutability, failed SSH/download/npm,
  PATH conflicts, runtime compatibility, and rollback in local tests.
- [x] Update README, usage guide, smoke checks, and incident notes.
- [x] Run focused checks, independent review, and final diff/status review;
  record exact evidence and unresolved live verification here.

## Risks And Rollback

Custom shell functions, aliases, startup output, version managers, root-owned
home files, and unusual npm config can change which binaries are used. Stop
with evidence when normal shell resolution contradicts the selected repair.
Never print entire npm config, environment, auth files, or private keys.
Back up only files changed, with private permissions. Restoring those files
reverts routing to the original installation; downloaded user packages may
remain. Updates within an existing user prefix are not package downgrades.

## Verification And Review Notes

Planned automated commands: `python3 tests/test_fix_vps_codex.py`,
`bash -n scripts/executable_fix-vps-codex.sh`, CLI help and argument checks,
README gate, and `git diff --check`.
Manual checks: local `--dry-run`, apply, fresh SSH `codex --version`, and a
second apply to prove repeatability. These require the user to run the helper.
The failed shell sandbox during prompt compilation is recorded separately;
read-only inspection succeeded using approved escalation.

RED: `python3 tests/test_fix_vps_codex.py` ran 13 tests, with 11 failures
because the requested script was absent (exit 1). Initial implementation
then exposed a home-parent containment bug and a fixture prefix error;
both are recorded in the incident note. Initial GREEN: all 13 passed.

Independent review identified shell-function shadowing, interrupted-runtime
retry failure, loss of newlines surrounding a managed block, and archive
symlink-parent traversal. Five added regression scenarios reproduced these
issues plus an external backup-state symlink (21 tests, five expected RED
failures). After corrections, all 21 tests and Bash syntax passed (exit 0).
The review was read-only and made no remote connections.

Implementation limits: dry run can only infer npm prefix without executing
npm; apply confirms it. Current package engines must use the supported
`>=major[.minor[.patch]]` form, otherwise the helper stops for review.
Unknown/changed host keys fail closed. Real remote installation and network
compatibility are not yet verified. No tracked runtime configuration was
changed locally; this change adds a standalone executable and documentation.

Final local checks: `./scripts/executable_fix-vps-codex.sh --help`,
`bash -n scripts/executable_fix-vps-codex.sh`,
`./scripts/executable_readme-recruiter-sync` (`pass_no_change`), and
`git diff --check` all exited 0. The six newly created task files passed
existence and whitespace inspection; the repair helper is executable.
Final review added a duplicate-archive-member regression: it failed for the
expected missing guard, then passed after duplicate-name rejection, sequential
resolved-path checks, and final link validation. The latest run of
`python3 tests/test_fix_vps_codex.py` passed all 22 tests (exit 0), followed by
passing Bash syntax, README gate, and diff-whitespace checks (exit 0).

Concurrent unrelated metaprompt migration work appeared during this session.
Preserve all of it. In shared files, this task owns only the VPS command row
in README and the VPS Codex Updates section in smoke-tests; all other dirty
hunks belong to prior/concurrent work. Nothing was staged or committed.
Keep this plan with its implementation/docs if a commit is requested later.

## Follow-up: Fish Startup Handshake

The user ran apply and reported failure before installation while reading
the login environment. Missing desktop fish-function and pywal paths were
also printed. Preserve the same repair scope and all concurrent dirty work.

- [x] Reproduce the framing failure and establish the cause with read-only
  diagnostics; do not run the repair against the VPS.
- [x] Correct shell-result transport and add defining regressions first.
- [x] Update docs, smoke coverage, incident evidence, and rerun focused checks.

Read-only SSH confirmed fish emits `ESC[6 q` without a newline immediately
before the environment marker: one marker, zero marker-prefixed lines, and
shell exit 0. Three regressions failed as expected before the correction.
Central `login_run` adds a newline before all three parsed shell commands;
host-key advice is limited to SSH exit 255. All 24 local tests and Bash syntax
passed (exit 0). A second read-only probe using the corrected production
functions passed environment, command-type, and CLI-version parsing on the
actual VPS (exit 0, Codex 0.114.0). No remote update was run. Independent review
confirmed all parsed interactive-shell consumers are covered.
