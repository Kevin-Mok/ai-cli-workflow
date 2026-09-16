# ChatGPT Desktop Linux Installer

## Purpose And Observable Outcome

Add a reusable installer that downloads and installs the official ChatGPT
desktop package for a supported Ubuntu, Debian, or Fedora host and processor
architecture. On this Ubuntu 24.04.1 x86_64 machine, it must select the
official x64 Debian package and install it through `apt`.

## Current Context, Relevant Files, And Scope Boundaries

- Create `scripts/executable_install-chatgpt-linux` as the user-facing shell
  installer.
- Create `tests/test_install_chatgpt_linux.sh` to run the installer against
  controlled OS, architecture, downloader, and package-manager doubles.
- Update `docs/smoke-tests.md` with the reusable manual verification.
- Update `README.md` in the existing Core Command Reference because this adds
  a user-facing command.
- The official guide supports Ubuntu 24.04/26.04, Debian 13, and Fedora
  43/44 on x64 or ARM64. It installs `.deb` packages with `apt` and `.rpm`
  packages with `dnf`.
- Protected pre-existing dirty state: `dot_agents/skills/feedback-memory/feedback.log`,
  `dot_config/vesktop/settings/quickCss.css`, and
  `dot_config/vesktop/settings/settings.json` are out of scope.

## Assumptions And Decisions

- The installer will use `/etc/os-release` by default, with an override only
  for hermetic tests.
- It downloads the package to a temporary directory, cleans it on exit, and
  uses only the final package-manager command with `sudo`.
- Unsupported distributions, unsupported versions, unsupported architectures,
  or missing required commands fail before download or privilege escalation.
- Exact package URLs are the official distribution-and-architecture links
  published by OpenAI at implementation time.
- Non-goals: installing on unsupported distributions, auto-launching or
  signing in to ChatGPT, and implementing the documented update command.

## Ordered Implementation Checklist

- [x] Record the supported matrix, current host facts, scope, and protected
  dirty state.
- [x] Write the failing shell test for Ubuntu x64 installation and supported
  error paths.
- [x] Run the test and confirm it fails because the installer is absent.
- [x] Add the minimal installer with detection, download, cleanup, and narrow
  privileged package install behavior.
- [x] Run the focused test, shell syntax check, and invalid-input runtime
  checks.
- [x] Document the command in the README and grouped smoke-test checklist.
- [x] Re-run relevant verification and record observed evidence here.
- [x] Add a failing package-manager-boundary test for apt sandbox readability.
- [x] Apply the minimum package and parent-directory permission change.
- [x] Re-run the focused regression test with the package-manager permission
  boundary enforced by its executable fixtures.

## Risks, Edge Cases, And Rollback

- The upstream package URLs can change; the installer reports the selected
  package URL before downloading so failure is diagnosable.
- A partial download or package-manager error must leave no retained temporary
  package file; cleanup is handled by a shell trap.
- The installer changes system package state only after an explicit `sudo apt`
  or `sudo dnf` command. Rollback is the normal package-manager removal of
  `chatgpt`.
- Existing user configuration and the protected dirty files remain untouched.

## Exact Verification

- RED: `bash tests/test_install_chatgpt_linux.sh` exits nonzero because the
  installer does not exist.
- GREEN/regression: `bash tests/test_install_chatgpt_linux.sh` exits zero and
  verifies package selection, downloaded destination, and the package-manager
  arguments for Ubuntu x64, Debian ARM64, Fedora x64, and unsupported distro,
  architecture, and supported-distro version input.
- Syntax: `bash -n scripts/executable_install-chatgpt-linux` exits zero.
- Manual: on a supported host, run `./scripts/executable_install-chatgpt-linux`;
  confirm the printed selected URL matches the official guide and approve only
  the final package installation password prompt.

## Progress, Verification Evidence, And Review Notes

- 2026-09-02: `sed -n '1,40p' /etc/os-release` reported Ubuntu 24.04.1 LTS;
  `uname -m` reported `x86_64`.
- 2026-09-02: The official guide was verified: supported Ubuntu 24.04/26.04,
  Debian 13, and Fedora 43/44 package downloads use apt or dnf respectively.
- 2026-09-02 RED: `bash tests/test_install_chatgpt_linux.sh` exited nonzero
  with `installer is missing or not executable` before implementation.
- 2026-09-02 GREEN: the focused test exited 0 and exercised Ubuntu x64,
  Debian ARM64, Fedora x64, and unsupported distro/architecture paths through
  command doubles; `bash -n scripts/executable_install-chatgpt-linux` exited
  0.
- 2026-09-02 final verification: the focused test again exited 0 with the
  added Ubuntu 22.04 rejection; an actual-host invalid-architecture invocation
  rejected `i686` before download or elevation; `git diff --check` exited 0.
- 2026-09-02: The sandboxed patch helper failed repeatedly while reopening
  existing files; the scoped patch-utility recovery is recorded in the linked
  postmortem.
- Review: The script is intentionally install-only. The official package adds
  its signed repository for later package-manager updates; this helper leaves
  updates to the documented normal package-manager workflow.
- Rollback: remove the installed `chatgpt` package with the host distribution's
  normal package manager.
- 2026-09-02 incident: real `apt install` succeeded but warned that `_apt`
  could not read the package in the `0700` `mktemp -d` directory. The plan is
  extended to make the named package readable and its parent traversable at the
  package-manager boundary, without making the directory listable or writable
  by other users.
- 2026-09-02 RED: the focused test failed with `apt cannot traverse the
  temporary package directory` while the installer still used the default
  `0700` `mktemp` directory.
- 2026-09-02 GREEN: after `chmod 711` on the directory and `chmod 644` on the
  downloaded package, the fixture verified those modes at both apt and dnf
  invocation boundaries. Repeating the full 391 MB production download solely
  to reproduce the non-fatal warning is intentionally out of scope; the test
  directly enforces its actual file-access preconditions.
