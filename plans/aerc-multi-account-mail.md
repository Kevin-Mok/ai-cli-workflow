# Aerc Multi-Account Mail ExecPlan

## Purpose and observable outcome

Ship `scripts/executable_setup-aerc-mail.sh`: a safe, repeatable setup tool
that installs shared dependencies and adds one Gmail or Outlook.com account per
invocation to a local aerc configuration. Gmail app passwords and Microsoft
client IDs live only in `pass`; Outlook OAuth tokens are managed by `oama`.

## Context and scope

- Design: `docs/superpowers/specs/2026-08-04-aerc-multi-account-mail-design.md`
- Script convention: `scripts/executable_setup-mosh.sh`
- Shell-test convention: `tests/scripts/executable_setup-mosh_test.sh`
- Shared manual verification: `docs/smoke-tests.md`
- Public command reference: `README.md`

The work creates a script, a fixture-only shell test, and matching docs. It
does not alter tracked aerc, dunst, or i3 configuration and never writes an
email address, credential, access token, or Microsoft client ID to this repo.

## Assumptions and settled decisions

- The operator adds accounts individually with `--add-gmail` or
  `--add-outlook`; eleven accounts are supported by repeated invocations.
- Gmail uses IMAPS `imap.gmail.com:993`, SMTPS `smtp.gmail.com:465`, and one
  app password retrieved by `pass show email/aerc/gmail/<label>`.
- Outlook uses IMAPS `outlook.office365.com:993`, SMTP STARTTLS
  `smtp-mail.outlook.com:587`, XOAUTH2, and `oama access <address>`.
- `oama`'s Microsoft device flow needs only a client ID. Its configuration
  supports `client_id_cmd`, so the script stores that ID in
  `pass show email/aerc/oama/microsoft-client-id` rather than YAML.
- `--install` may require sudo for packages; add and status actions must not.
- Direct IMAP is the initial notification surface. Maildir/mbsync remains
  expressly out of scope.

## Protected state, risks, and rollback

- Initial protected Git state: clean after commit `72c1547`; do not stage
  unrelated later changes.
- Generated XDG configuration is outside Git. Reject symlink targets; preserve
  backups of any regular configuration file before modifying it.
- Secret reads and status output must not print secret values. Tests use fake
  `pass` and `oama` commands only.
- oama distribution availability varies. The script installs it only when the
  selected package manager supplies a known package; otherwise it exits with a
  deterministic manual-install reference and changes no account configuration.
- Failed Outlook device authorization rolls back only the account block created
  by that invocation, leaving a pre-existing user configuration intact.

## Implementation checklist

- [x] Record the approved design and exact provider transport decisions.
- [x] Record the clean Git baseline and protected generated state.
- [x] Add a fixture-only shell test before implementation.
- [x] Run the new test and capture RED evidence because the script does not yet
  exist.
- [x] Implement argument validation, package detection, and `--install`.
- [x] Implement XDG target safety, private file permissions, hook insertion,
  and safe account-block append/rollback helpers.
- [x] Implement `--init-pass`, `--add-gmail`, `--add-outlook`, and `--status`.
- [x] Run the focused test to capture GREEN evidence.
- [x] Add the README command entry and a grouped smoke-test action/expected
  check; update this plan with exact evidence and review notes.
- [x] Run shell syntax validation, focused regression, documentation checks,
  and a fixture-backed manual entrypoint check.
- [x] Run `refresh-config` only if a tracked chezmoi-managed configuration
  target changes; this script/docs-only change does not require it.
- [x] Run the README recruiter-sync gate, inspect the staged diff, and commit
  the implementation, test, README, smoke test, and plan together.

## File-level implementation design

### `scripts/executable_setup-aerc-mail.sh`

Use Bash with `set -euo pipefail`. Accept exactly one action:
`--install`, `--init-pass GPG_KEY_ID`, `--add-gmail`, `--add-outlook`,
`--status`, or `--help`. Support `--dry-run` for actions that would write;
dry-run prints sanitized operations and neither invokes `pass insert` nor
starts OAuth.

Create `~/.config/aerc` and `~/.config/oama` only after checking each path and
target component is not a symlink. Use `umask 077`, `mktemp`, `mv`, and traps
for safe writes. Store ownership markers in generated account blocks:

```ini
# BEGIN aerc-mail-setup: gmail-work
[gmail-work]
...
# END aerc-mail-setup: gmail-work
```

This marker makes duplicate and rollback detection exact without editing other
user account sections. The first hook insertion creates an `aerc.conf` with
the documented `[hooks]` command. If `mail-received` already exists, leave it
untouched and report that choice.

Before storing a secret, require that `PASSWORD_STORE_DIR` (or its default)
exists and contains at least one `.gpg-id`; `--init-pass` explicitly runs
`pass init` for the given recipient. Use stdin to `pass insert --multiline`
with echo disabled. Never command-substitute a secret.

For Outlook, create or update only the `services.microsoft.client_id_cmd`
value in the config produced by `oama template`, retaining an original backup
first. The value is the fixed command:

```yaml
client_id_cmd: |
  pass show email/aerc/oama/microsoft-client-id
```

Reject an oama config that does not contain a `microsoft:` service block rather
than attempting unbounded YAML rewrite. Invoke `oama authorize microsoft
<address> --device` only after its account block is written; remove that exact
block if authorization exits nonzero.

### `tests/scripts/executable_setup-aerc-mail_test.sh`

Create a Bash test that makes a temporary HOME, XDG config/state, password
store, and PATH with fake `pass`, `oama`, package manager, and `notify-send`
executables. Assertions must cover:

- `--help` lists every action and the no-secret guarantee.
- Multiple actions and a malformed label fail without files created.
- `--add-gmail --dry-run` produces no config or pass log; a non-dry-run Gmail
  fixture writes IMAPS/SMTPS credential commands with `%40` address encoding.
- A duplicate managed label fails and does not append another block.
- `--add-outlook --dry-run` produces no OAuth call; normal fixture mode
  generates XOAUTH2 account URIs, oama `client_id_cmd`, and records one
  device-flow invocation without exposing the fake client ID.
- `--status` reports labels and provider kinds, exits nonzero for a missing
  secret, and never prints the fake secret.
- A symlink accounts target causes a safe failure.
- Gmail setup writes the declared `[hooks]` `mail-received` notification hook.
- A second Outlook account reuses the shared Microsoft client-ID credential and authorizes successfully.
- A symlinked `XDG_CONFIG_HOME` parent fails before any account file is created.

### Documentation

Add the script to the root README command table only after its `--help` output
is final. Document each action, the `sudo` requirement for `--install`, the
Google app-password and Microsoft-client-ID prerequisites, and that account
add actions are intentionally interactive.

Add one `docs/smoke-tests.md` entry with a single-line Action for the fixture
test plus Expected results that name direct IMAP, secret non-leakage, and no
real OAuth/package mutations.

## Verification plan and evidence

RED command:

```bash
tests/scripts/executable_setup-aerc-mail_test.sh
```

Expected before implementation: nonzero because the script path does not
exist. Record actual output and exit status in this plan.

GREEN and regression commands:

```bash
bash -n scripts/executable_setup-aerc-mail.sh
tests/scripts/executable_setup-aerc-mail_test.sh
git diff --check
```

Manual fixture check:

```bash
scripts/executable_setup-aerc-mail.sh --help
```

Expected: every action, the sudo boundary, external prerequisites, and the
individual-account workflow are described; no account or secret is requested.

## Progress, verification evidence, and review notes

- 2026-08-04: User approved the design and requested implementation.
- 2026-08-04: Upstream aerc manuals confirm `source-cred-cmd`,
  `outgoing-cred-cmd`, URL-encoded addresses, `check-mail = 5m`, IMAPS,
  STARTTLS, and XOAUTH2 transports. Upstream oama source confirms the built-in
  Microsoft device endpoint, required device-flow client ID, and
  `client_id_cmd` support.
- 2026-08-04 RED: `bash tests/scripts/executable_setup-aerc-mail_test.sh`
  exited 127 with `scripts/executable_setup-aerc-mail.sh: No such file or
  directory`, proving the new test exercised the missing entrypoint.
- 2026-08-04 GREEN: `bash -n scripts/executable_setup-aerc-mail.sh &&
  tests/scripts/executable_setup-aerc-mail_test.sh` exited 0. The fixture
  covered Gmail/Outlook account generation, dry-run behavior, duplicate and
  symlink rejection, OAuth device-flow invocation, and secret non-leakage.
- 2026-08-04 regression: Added a Gmail fixture assertion for the required `[hooks]` `mail-received` entry. It failed while `ensure_mail_hook` returned early on `[ -e "" ]`; removing that erroneous guard (and the matching accounts-file guard) restored hook creation. `bash -n scripts/executable_setup-aerc-mail.sh && bash tests/scripts/executable_setup-aerc-mail_test.sh` exited 0.
- 2026-08-04: The initial fixture run exposed a dry-run exit-status defect:
  an intentionally absent target file returned false under `set -e`. The
  private-file preparation helpers now return success on intentional dry-run
  non-writes; the focused fixture passed after that isolated correction.
- 2026-08-04 final verification: `bash -n scripts/executable_setup-aerc-mail.sh`,
  `bash -n tests/scripts/executable_setup-aerc-mail_test.sh`,
  `tests/scripts/executable_setup-aerc-mail_test.sh`,
  `scripts/executable_setup-aerc-mail.sh --help`, `git diff --check`, and
  `./scripts/executable_readme-recruiter-sync` all exited 0. The README gate
  returned `pass_no_change`.
- 2026-08-04: `refresh-config` was intentionally not run: this change adds a
  repo-owned script and documentation but no tracked chezmoi-managed config.
- 2026-08-04: Reviewed the staged aerc scope: script, fixture test, README entry, matching smoke-test hunk, and this plan only; no credential or unrelated file is staged. Commit ready.
- 2026-08-04 review follow-up: Independent review found that repeated Outlook setup failed on the shared Microsoft client-ID key and ancestor symlinks were followed. Added RED fixture coverage for both. Outlook additions now reuse an existing shared `pass` entry without reading its value; `ensure_no_symlink_component` rejects every path component before writes. `bash -n scripts/executable_setup-aerc-mail.sh && bash tests/scripts/executable_setup-aerc-mail_test.sh` exited 0.

## Handoff

Atomic work order: test (RED) → script (GREEN) → docs and current plan →
syntax/focused/manual verification → README gate → one focused commit.

Cursor prompt: “Implement `plans/aerc-multi-account-mail.md` exactly. Start by
running its RED shell test, keep all credentials and account addresses out of
Git and command output, use only fixture executables in tests, update the
README and smoke test with final verified flags, then record fresh commands,
outputs, and exit statuses in the ExecPlan before committing with a concise
Conventional Commit subject.”
