# ExecPlan: Add a TPM Bootstrap Installer

## Purpose and observable outcome

Provide a tracked, executable helper that installs or fast-forwards the tmux
plugin manager (TPM), repairs the known quoted bootstrap line when present,
and reloads an active tmux server. Users can discover the helper and its
follow-up `prefix + I` action in the root README and smoke checklist.

## Context, scope, and decisions

- `scripts/executable_install-tmux-tpm.sh` is the installer implementation.
- `README.md` documents every public entrypoint it tells users to run; this
  change adds the helper with its sole `--help` option and no invented flags.
- `AGENTS.repo.md` records that tracked Codex model-selection preferences are
  local by default and not part of this installer commit.
- `docs/smoke-tests.md` captures the real installation check because the
  installer changes a user's TPM checkout and active tmux server.
- The protected pre-existing worktree includes the separate `commit-session`
  workflow update, an unrelated model-preference test, and prompt files.
  They remain outside this commit except for a distinct README hunk prepared
  specifically for this installer.
- No live install runs during automated verification because it fetches from
  GitHub and modifies `~/.tmux`; syntax and help output are the safe checks.

## Checklist

- [x] Capture the dirty worktree and isolate the TPM installer from unrelated
  configuration and commit-session work.
- [x] Inspect the installer source and verify its documented `--help` surface.
- [x] Add README, policy, and smoke-test documentation that matches the
  installer behavior.
- [x] Run shell syntax, help-output, Markdown whitespace, and README-gate
  checks; record exact results below.
- [x] Inspect the intended staged diff and commit only the installer bundle.

## Risks, rollback, and verification

- Risk: a live run mutates `~/.tmux/plugins/tpm` and contacts GitHub. Mitigate
  by limiting automated checks to `bash -n` and `--help`; users opt into the
  live smoke action explicitly.
- Risk: ordinary commit workflows capture personal model changes. Mitigate by
  stating the narrow `dot_codex/config.toml` exclusion in `AGENTS.repo.md`.
- Rollback: revert the installer, its README and smoke entries, policy
  addition, and this plan in one commit; no generated repository state exists.
- Automated checks: `bash -n scripts/executable_install-tmux-tpm.sh`,
  `scripts/executable_install-tmux-tpm.sh --help`, `git diff --check`, and
  the README recruiter gate.

## Progress, verification evidence, and review notes

- Initial inspection found the installer is untracked and executable, with no
  repository test harness for TPM. Its safe executable surface is `--help`.
- Documentation is intentionally coupled to the feature commit so the public
  command reference cannot get ahead of the implementation.
- `bash -n scripts/executable_install-tmux-tpm.sh` exited 0. Its `--help`
  output lists the documented TPM clone/update, executable, bootstrap repair,
  reload, and `prefix + I` behavior. `git diff --check` exited 0 and
  `./scripts/executable_readme-recruiter-sync` returned `pass_no_change`.
- Staged review contains only the installer, its two README hunks, its smoke
  check, the local-model policy, and this ExecPlan; unrelated session work is
  unstaged.
