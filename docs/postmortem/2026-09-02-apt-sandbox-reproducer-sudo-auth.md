# Apt Sandbox Reproducer Could Not Authenticate

## Symptom

The installer-warning diagnostic attempted to check package readability as the
`_apt` user with `sudo -n`, but the non-interactive session had no reusable
sudo credential.

## Impact

The disposable permission reproducer could verify the default `mktemp -d`
directory mode (`0700`) but could not complete the direct `_apt` read check.
No repository or system configuration changed.

## Evidence

- The user-reported install output states that `_apt` could not access the
  package under `/tmp/chatgpt-install.*`.
- The disposable reproducer reported a `0700` temporary directory and a
  `0664` package file.
- `sudo -n -u _apt` returned `sudo: a password is required`.

## Root Cause

The installer retained the default `mktemp -d` mode (`0700`). The named
package therefore could not be reached by apt's unprivileged `_apt` downloader,
which caused apt to fall back to an unsandboxed download path and emit the
warning.

## Resolution

- Added a test boundary that requires a `0711` package directory and `0644`
  package file at apt/dnf invocation.
- Confirmed RED against the old `0700` directory behavior.
- After the download succeeds, the installer now sets exactly those modes
  before the sole privileged package-manager command.

## Verification And Follow-up

- The focused test passed after the change for Ubuntu x64, Debian ARM64, and
  Fedora x64 installs, while retaining unsupported-input guards.
- `0711` permits traversal to the known file but not directory listing; `0644`
  permits apt to read the package without allowing other users to change it.
- No additional production download is needed for this already-installed app.
  A later normal installer run on an apt host should complete without the
  reported `_apt` inaccessible-package warning.
