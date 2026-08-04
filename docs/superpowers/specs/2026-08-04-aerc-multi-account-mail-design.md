# Aerc Multi-Account Mail Setup Design

## Purpose and observable outcome

Provide a repo-owned, account-at-a-time setup tool for one Outlook.com account
and up to ten Gmail accounts. An operator can install the shared dependencies,
add one Gmail account with an app password, add one Outlook account through
OAuth2, and inspect the resulting configuration without placing addresses,
passwords, OAuth tokens, or client IDs in this repository.

## Scope

The deliverable is a Bash script at
`scripts/executable_setup-aerc-mail.sh`, a focused shell test, a smoke-test
entry, and root-README command documentation.

The script manages only local XDG user configuration:

- `~/.config/aerc/aerc.conf` for the notification hook.
- `~/.config/aerc/accounts.conf` for aerc account sections.
- `pass` entries under a documented `email/aerc/` namespace for Gmail app
  passwords and the Microsoft application client ID.
- `~/.config/oama/config.yaml` through `oama`'s own generated template and a
  narrowly validated Microsoft service configuration.

It does not add i3 bindings or change the tracked dunst configuration. It
prints an optional scratchpad snippet so the operator explicitly decides
whether to add it to i3.

## Decisions

### Account-at-a-time workflow

The script has four actions:

- `--install` detects a supported package manager, installs available distro
  packages for `aerc`, `pass`, `gnupg`, `libnotify`, and `dunst`, and reports a
  clear manual `oama` installation path when the distro does not package it.
- `--add-gmail` prompts once for an account label, Gmail address, and app
  password using a hidden terminal prompt. It writes one `pass` entry and one
  aerc section.
- `--add-outlook` prompts once for a label, Outlook address, and registered
  Microsoft client ID. It stores the client ID in `pass`, configures oama to
  retrieve it from `pass`, writes one XOAUTH2 aerc section, and invokes
  `oama authorize microsoft <address> --device`.
- `--status` is read-only: it lists configured account labels and provider
  type, validates required executables, and checks that each expected secret
  lookup works without printing secret values.

The script permits any number of independent invocations. Labels must be
lowercase, hyphen-separated identifiers; duplicates fail before a config or
secret write. Existing managed account sections are never overwritten.

### Authentication and transport

Gmail uses direct IMAPS at `imap.gmail.com:993` and SMTP-over-TLS at
`smtp.gmail.com:465`. The account address is URL encoded in transport URIs;
the app password is retrieved only with `pass show` via aerc's credential
command settings.

Outlook.com uses IMAPS at `outlook.office365.com:993` and SMTP STARTTLS at
`smtp-mail.outlook.com:587`, both with XOAUTH2 tokens returned by `oama
access <address>`. OAuth credentials remain in oama's encrypted backend; aerc
receives short-lived access tokens only through credential commands. The
operator must enable IMAP in Outlook settings and register a Microsoft
application suitable for device-code flow.

Each account checks mail every five minutes. The direct-IMAP choice minimizes
setup complexity. The script documentation calls out that Maildir via
`mbsync` is the later reliability upgrade if direct-IMAP `mail-received`
hooks are not dependable for a provider.

### Notifications and secrets

The script creates the aerc `[hooks]` `mail-received` command only if a config
file does not already define that hook. The command uses `notify-send` with
the aerc account, sender name, and subject; dunst remains the notification
daemon already managed by this dotfiles repository.

All created config files are mode `0600`; their parent directories are mode
`0700` when newly created. The script rejects a symbolic link at every
managed configuration target and backs up a regular pre-existing target before
its first owned change. It never echoes credentials, calls `pass show` in
verbose output, or stages any generated home-directory configuration.

`pass` must already have a recipient configured. An optional
`--init-pass GPG_KEY_ID` action may initialize an empty password store
explicitly; the normal install and add actions never choose or generate a GPG
identity themselves.

## Error handling and rollback

Argument parsing rejects multiple actions, unknown options, malformed labels,
and malformed email addresses. Before changes, each add action checks command
availability, `pass` initialization, configuration ownership, duplicate
labels, and existing secret keys. A failed prerequisite causes no config
write.

The script writes new account snippets to a private temporary file, validates
the result structurally, then appends atomically. It registers cleanup for
temporary files. A timestamped backup is retained for a pre-existing aerc or
oama configuration file modified by the script; the script prints the precise
rollback path.

OAuth browser authorization is intentionally interactive. If it is cancelled
or fails, the created aerc account section is removed only when it is still
byte-for-byte the section created by the current invocation; otherwise the
script reports the safe manual cleanup path.

## Verification

The focused shell test uses temporary fake executables and XDG directories to
verify help text, option exclusivity, malformed labels, duplicate rejection,
Gmail credential-command generation, Outlook XOAUTH2 generation, non-leaking
status output, symlink rejection, and dry-run/no-write behavior. No test uses
real credentials, launches OAuth, or changes the host package database.

Manual verification after installation:

1. Run `scripts/executable_setup-aerc-mail.sh --status` and confirm all added
   account labels report their expected provider.
2. Run `aerc`, open each account, refresh its Inbox, and send a test message
   from both a Gmail and Outlook account.
3. Deliver a test message to each provider and confirm one dunst notification
   presents the account label, sender, and subject.
4. Optionally add the printed scratchpad snippet to local i3 configuration,
   reload i3, and confirm aerc can be shown and hidden without a second
   instance.

## Review notes

This design deliberately does not automate Google app-password generation or
Microsoft app registration because those operations require a signed-in web
session and an explicit security decision. It keeps the script useful for the
requested eleven-account setup while preserving user control over both.
