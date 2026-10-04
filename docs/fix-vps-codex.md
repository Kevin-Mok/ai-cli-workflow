# Repair Codex Updates On A VPS

This guide repairs Codex update permissions on a VPS so you can update it
normally from your own account. Preview the SSH diagnostics, run the repair
from your PC, then reconnect and check the updated command; saved rollback
instructions let you restore changed configuration if needed.

Run the [repair helper](../scripts/executable_fix-vps-codex.sh) on your local
PC. It connects using your existing SSH key or agent. **No sudo is needed
locally or on the VPS.** The default target is `example-user@192.0.2.10`.

Preview diagnostics first:

```bash
/home/example/linux-config/scripts/executable_fix-vps-codex.sh --dry-run
```

Apply the repair:

```bash
/home/example/linux-config/scripts/executable_fix-vps-codex.sh
```

Once it prints `SUCCESS`, reconnect your VPS terminal so its shell picks up
the repaired PATH. The script itself opens a second SSH session and checks
that `npm install -g @openai/codex` and `codex --version` work normally.
An existing Codex process keeps using its already-running executable until
you restart it.

## Options And Prerequisites

| Option | Behavior |
| --- | --- |
| `--host USER@HOST` | Change the destination; an existing SSH config alias also works. |
| `--port PORT` | Override the SSH port; otherwise use SSH configuration. |
| `--identity FILE` | Select a readable private-key file; its contents are never copied or printed. |
| `--dry-run` | Read diagnostics and current package metadata without repair writes or npm execution. |
| `--help` | Print usage without connecting. |

The PC needs Bash and OpenSSH. The VPS needs Linux, Python 3.8 or newer,
and bash or fish as its login shell. An encrypted SSH key must already be
unlocked in your agent. Host-key checking remains strict: if the host is
unknown, verify its fingerprint with your provider and establish a normal
SSH connection first. SSH password prompts are disabled; authentication or
connection failures keep SSH's exit status, usually 255. Invalid local
arguments exit 2; remote repair/verification failures exit 1.

The VPS needs outbound HTTPS to the npm registry and its configured registry
for the ordinary update check. Runtime fallback additionally uses
`nodejs.org`. Node's official Linux binaries must support the VPS libc.
Automatic runtime installation supports x86_64 and aarch64; other platforms
can reuse an already compatible installation.

## What Changes

The reported EACCES is a permission failure while modifying a system npm
installation. The helper reads the current Codex package's Node requirement
from the official npm registry and checks the initialized login environment.
It reuses compatible Node/npm. A compatible user-owned prefix, including
standard or exported custom fnm/nvm locations, is reused. Otherwise system
npm gets a prefix under `~/.local/share/codex-npm`, saved in `~/.npmrc`.
This prefix also becomes the destination for future global npm installs
by this user. Other npm settings and comments are preserved.

Only missing or incompatible Node/npm triggers a current LTS download from
Node's official distribution service. Its SHA256 must match the published
checksum, archive paths are checked, and binaries must run before shell
configuration changes. The runtime lives under `~/.local/share/codex-node`;
OS packages and running services are untouched. Future interactive shells
use that runtime, so newly launched Node applications can see the new version.

The PATH block is placed at the end of fish's `config.fish`, or in bash's
active login profile and `.bashrc`. A managed runtime gets no conflicting
`prefix=` setting in `.npmrc`; an existing prefix entry is removed with a
backup. If npm's configured cache is outside the home or contains entries
owned by another user, the helper selects `~/.cache/codex-npm` instead.
Codex's authentication, sessions, and configuration are not edited.

Dry run uses inherited SSH environment and file metadata. Its npm prefix
is explicitly labeled as inferred; apply obtains npm's effective prefix.
The helper does not run an additional login shell, npm, or an installer in
dry run. SSH server login hooks can have their own side effects.

Fish cursor-control sequences and startup banners without a final newline
are supported. Shell probes start on a fresh line so these do not corrupt
environment, command-type, or version parsing. Warnings about missing desktop
fish-function directories or pywal files may still appear from existing VPS
startup scripts; those warnings alone do not mean the repair failed. See the
[shell-handshake incident](postmortem/2026-10-03-vps-codex-shell-handshake.md).
Host-key advice is printed only for an SSH connection failure, not a remote
repair failure.

The helper stops for unsupported shells, symlinked configuration files,
unwritable destinations, custom npm userconfig locations, exported npm
prefix/cache/userconfig overrides, or shell aliases/functions shadowing
Codex/npm during verification. Its error explains what to inspect. It does
not change ownership of system directories or require root access.

## Backups And Rollback

Changed user files are backed up in a private directory under
`~/.local/state/fix-vps-codex/`. Apply prints the exact remote command for
the generated `rollback.py`. Run that command on the VPS, then reconnect.
The rollback refuses to overwrite a file edited after the repair.

Rollback restores configuration and PATH routing. It leaves downloaded
Node/Codex packages on disk, and does not downgrade a Codex package updated
in an existing user prefix. A failure before configuration changes can also
leave a downloaded user runtime or package cache; retrying is supported.
If verification fails after configuration changes, use the printed rollback
command or fix the named shell conflict and rerun.

## Verification And Handoff

Local automated checks:

```bash
python3 tests/test_fix_vps_codex.py
bash -n scripts/executable_fix-vps-codex.sh
./scripts/executable_fix-vps-codex.sh --help
```

The tests run the real remote payload against temporary homes, real bash/fish
shells, and substitutes for SSH, npm, and HTTPS downloads. They do not contact
the VPS. Follow the [VPS smoke checks](smoke-tests.md#vps-codex-updates) for
live acceptance. The [ExecPlan](../plans/fix-vps-codex.md) records progress;
the [accepted prompt](../prompts/fix-vps-codex.md) is a paste-ready continuation
prompt for Cursor or another coding agent. Suggested commit subject:
`fix: add SSH repair for VPS Codex updates`.

References: [npm's EACCES repair guidance](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally/),
[official Codex CLI docs](https://learn.chatgpt.com/docs/codex/cli), and
[Node's release metadata](https://nodejs.org/dist/index.json).
The [incident note](postmortem/2026-10-03-vps-codex-repair.md) distinguishes
local regression evidence from the pending live VPS repair.
