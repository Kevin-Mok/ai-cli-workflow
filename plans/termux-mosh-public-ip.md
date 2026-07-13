# Termux Mosh Public-IP Setup Plan

> **For agentic workers:** Execute this plan with the repository's test-first
> shell-script conventions. Keep this plan with the implementation and docs in
> the same commit.

**Goal:** Make the existing public-IP SSH path usable from Termux through
Mosh, plus safe one-way SSH file-transfer helpers.

## Checklist

- [x] Add a failing shell contract test for the Termux bootstrap interface.
- [x] Add an idempotent Termux bootstrap that installs `mosh`, `openssh`, and
  `rsync`; configures a named SSH host; and installs Mosh, SCP, and rsync
  helper commands.
- [x] Document the required PC firewall and router UDP `60000:61000` forwarding
  alongside the existing public-IP SSH workflow.
- [x] Add a durable Remote Access smoke check for running the bootstrap and
  validating Mosh over cellular data.
- [x] Run shell syntax checks and the focused script tests.
- [x] Record the implementation review and verification results below.

## Assumptions

- Termux already has a working key-based SSH route to the PC's public endpoint.
- The PC runs the existing `scripts/executable_setup-mosh.sh` helper.
- The router can forward UDP `60000:61000` to the PC and the ISP permits
  inbound UDP.

## Review

- Added an idempotent Termux bootstrap and focused shell contract tests.
- Kept the existing SSH key and agent selection behavior intact while adding a
  named `pc-remote` host and one-way transfer helpers.
- Verified the README gate, focused tests, shell syntax, optional ShellCheck,
  whitespace, and Git diff checks on 2026-07-13.
