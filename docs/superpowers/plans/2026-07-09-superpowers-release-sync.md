# Superpowers Release Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Manage the external Superpowers bundle with chezmoi from the latest upstream release archive and expose a manual refresh command.

**Architecture:** Chezmoi owns the installed `~/.codex/superpowers` tree as an exact archive external sourced from the latest GitHub release. A small Bash helper wraps the precise `chezmoi apply --refresh-externals` command so manual updates are repeatable.

**Tech Stack:** chezmoi externals, chezmoi GitHub template functions, Bash, Markdown docs.

---

### Task 1: Convert Superpowers External To Release Archive

**Files:**
- Modify: `.chezmoiexternal.toml.tmpl`

- [x] **Step 1: Verify the release URL template expression**

Run: `chezmoi execute-template '{{ (gitHubLatestRelease "obra/superpowers").TarballURL }}'`
Expected: Prints the latest Superpowers release tarball URL.

- [x] **Step 2: Replace the git-repo external**

Set `.codex/superpowers` to `type = "archive"`, use the latest release
tarball URL, `stripComponents = 1`, and `exact = true`.

### Task 2: Add Manual Refresh Helper

**Files:**
- Create: `scripts/executable_sync-superpowers-release`

- [x] **Step 1: Run the missing-helper red check**

Run: `./scripts/executable_sync-superpowers-release --help`
Expected: Fails because the helper does not exist yet.

- [x] **Step 2: Add the helper**

Create a Bash script that supports `--dry-run`, defaults the source
directory to `$HOME/linux-config`, and runs:

```bash
chezmoi -S "$source_dir" apply --refresh-externals -v "$HOME/.codex/superpowers" "$HOME/.agents/skills/superpowers"
```

### Task 3: Update Docs And Smoke Coverage

**Files:**
- Modify: `README.md`
- Modify: `dot_agents/skills/README.md`
- Modify: `docs/smoke-tests.md`

- [x] **Step 1: Document the install behavior**

Update the README and skill catalog to say Superpowers is installed from
the latest release archive, not cloned from `main`.

- [x] **Step 2: Document the command**

Add `sync-superpowers-release` to the README command reference and smoke
tests.

### Task 4: Verify

- [x] **Step 1: Syntax-check the helper**

Run: `bash -n scripts/executable_sync-superpowers-release`
Expected: exits 0.

- [x] **Step 2: Check the helper help path**

Run: `./scripts/executable_sync-superpowers-release --help`
Expected: prints usage and exits 0.

- [x] **Step 3: Dry-run the release refresh**

Run: `./scripts/executable_sync-superpowers-release --dry-run`
Expected: chezmoi renders the latest release external and previews the
Superpowers target changes without applying them.
