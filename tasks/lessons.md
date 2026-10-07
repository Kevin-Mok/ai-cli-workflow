# Lessons

- In Bash prompt helpers that assign caller variables with `printf -v`, keep the helper's own local input variable under a different name; Bash dynamic scoping can otherwise leave the caller unset under `set -u`. Exercise an interactive dry run, not only syntax and non-interactive help paths.

- When a user widens README scope after an initial pass, update the documented surface to include every newly named repo entrypoint, not just the most obvious directories.
- When a user says a README tech-stack section must be based on the repo, derive it from tracked repo evidence and named core layers instead of generic stack language.
- When reframing the README, preserve requested navigation and coverage elements from the prior version, especially the hero screenshot, table of contents, and expanded non-AI dotfiles sections.
- When repo instructions require logging user corrections to `tasks/lessons.md`, create the file first if it does not already exist.
- When updating committed Codex config content, treat the current edited file as the source of truth for new additions, restore any deleted committed content, and do not duplicate entries while merging.
- When wrapping CLI diagnostics, do not trust exit status alone for subcommands that may still print a structured failure message; inspect the output for known error text before reporting success.
- When writing installer scripts for distro-packaged tools, do not assume the needed package exists in the user's current repositories; include a safe upstream fallback when the distro package source can vary.
- When a user points to a specific env-backed MCP checkout, prefer launching that checkout directly and verify that the default HTTP port is not already serving a different local app before keeping a URL-based MCP registration.
- When a user wants README wording to stay functionality-based, do not introduce explicit internal skill names there if the existing capability description is already accurate.
- When the user specifies a concrete new skill name, use that exact name instead of inventing a nearby alternative.
- When adding an i3 launcher for a CLI installed through shell-managed PATH, verify the command from a clean session and prefer a stable absolute entry point over `bash -lc` if shell startup can drop the binary.
- When ingesting external content with permission, record that permission explicitly and do not describe it as ownership.
- When importing external skills or templates, record the upstream source in tracked files near the imported material, not only in chat or plan notes.
- When writing a catalog-style README with many peer entries, organize it into meaningful category headings instead of leaving it as one flat list of same-level sections.
- When building a catalog for repo-local components or skills, link each entry directly to its canonical source file so the summary page also works as navigation.
- When a user says "README" after an ambiguous docs request in this repo, default the scope to the root `README.md` unless they explicitly name a different one.
- When shortening a recruiter/client-facing README, do not optimize for brevity so hard that the repo stops feeling substantial; keep the value proposition first and preserve enough technical proof to sell the work.
- When validating `sshd` config changes in setup scripts, account for runtime prerequisites like `/run/sshd` instead of assuming the validation environment already matches a started service.
- When a setup script fundamentally changes privileged system state, prefer making it require or self-acquire `sudo` up front instead of scattering best-effort `sudo` calls deeper in the flow.
- When exposing SSH on a custom port, check for `ssh.socket` systemd socket activation; `sshd_config` alone may not change the actual listening ports.
- When debugging public service exposure, add a host-side doctor path that can separate local listener/firewall issues from router, NAT, or ISP reachability.
- When a setup script applies a service config, do not use `try-reload-or-restart` if the service may be inactive; use logic that actually starts the service.
- When adding a personal-machine hardening script, default the target login user sensibly instead of forcing an explicit flag for the common single-user case.
- When a local Codex skill needs durable preferences in this repo, keep the mutable log in the chezmoi source tree and make the installed skill read and append that tracked file instead of maintaining a second copy under `~/.agents/skills`.
- When doing a commit plan, order the proposed commits from oldest changes to newest changes.
- When a user asks to ship only the current Codex session, leave unrelated dirty changes from other sessions uncommitted instead of bundling them into the same commit.
- When `commit-session` has strong direct file attribution but the original session missed its pre-write `git status --short`, do not fail the whole workflow; ship the directly observed touched files and leave unattributed dirties out.
- When a user explicitly asks to commit the current dirty work as one commit, collapse any earlier split-commit plan and ship the remaining changes together.
- Apply the newest delivery-cadence preference from the canonical feedback log.
- When a workflow will require the user to run commands manually, proactively package it in a script in the first response instead of listing raw commands, and include the exact `sudo` invocation when elevation is required.
- Do not wait for the user to remind you to script manual command workflows; treat that requirement as automatic.
- When validating or repairing symlinks in a script, resolve relative targets from the symlink's directory, not from the current working directory.
- When Python-based verification in this repo generates `__pycache__` or `.pyc` artifacts, add or keep repo-level ignore rules so those local caches do not pollute commit workflows.
- When a recruiter-facing README skill validates a README, enforce front-of-file hierarchy and hook strength, not just section presence; setup and command blocks should usually come after the repo has already sold why it matters.
- In /home/example/linux-config, when I change tracked configuration, run `refresh-config` before declaring the work done unless I explicitly tell you not to.
- In /home/example/linux-config, always edit the repo-tracked source first and then run `refresh-config` to apply it; do not treat live installed copies under `$HOME` as the primary edit target.
- In /home/example/linux-config, treat the repo-tracked `dot_codex/config.toml` as the source of truth; do not copy the live Codex config back into the repo during refresh workflows.
- In /home/example/linux-config, `refresh-config` now snapshots the live `~/.codex/config.toml` into `dot_codex/config.toml` before `chezmoi apply`; do not describe it as repo-to-home sync.
- Before proposing workflow isolation or branch-management steps in this repo, read and apply the canonical feedback log; do not suggest git worktrees unless the user explicitly asks for them.
- For README rewrites in this repo, fix the opening hook before cutting technical proof; the root README should stay technically in-depth enough to feel substantial to engineers.
- When a user approves a README structure as the repo default, encode that structure in `AGENTS.repo.md` instead of relying on memory or one-off docs edits.
- In /home/example/linux-config, when executing a multi-commit series, do not push after intermediate commits; hold pushes until the full series is finished unless the user explicitly asks for per-commit pushes.
- When a user clarifies that a workflow preference applies across repositories, record it as global guidance instead of narrowing it to the current repo.
- When a user names a keyboard-specific macro key like `Keychron Q11 M2`, do not assume it is a standard modifier or keysym; first map it through the repo's existing hardware-remap convention or confirm the emitted key with `xev`.
- When a user asks to keep an existing helper script, preserve that entrypoint and add a new sibling script for the new behavior instead of repurposing the original path.
- When changing a keybinding between helper scripts, confirm the actual target app or site instead of assuming it should remain in the same product family.
- When fixing multi-monitor floating-window placement in i3, verify the live window rect after the move command; a successful `i3-msg` exit code is not enough to prove the window landed on-screen.
- When debugging theming in this repo, verify the actual rendering surface before attributing the problem to terminal, editor, or VS Code config; similar-looking screenshots are not enough evidence on their own.
- When the user asks for terminal transparency and the configured opacity is visually imperceptible, treat that as a real bug and choose a clearly visible opacity level instead of insisting the subtle setting is "working."
- When the user says a Vim theme still looks plain or under-colored, do not treat “some highlight groups are non-default” as success; verify that the rendered syntax has enough visual separation to actually feel themed.
- When a user expects running Vim or Neovim sessions to react to wallpaper changes, do not assume terminal palette reloads are enough; verify and, if needed, add an editor-side wal refresh path for already-open sessions.
- When the user reiterates that git worktrees are opt-in, do not suggest or use them unless they explicitly ask for them.
- When generating docstrings for LeetCode scaffolds, wrap every docstring line to a Vim-friendly maximum width instead of leaving long prompt sentences unwrapped.
- When maintaining `commit-plan`, treat oldest-to-newest commit order as an execution invariant across the plan, manual commands, and message summary.
2026-04-10 - When asked to merge from a work tree, always push to `main` afterwards before proceeding.
- In /home/example/linux-config, when a README check passes structural headings but fails recruiter-first positioning, run the gate against opening-hook substance, hierarchy, and stack-vs-setup ordering before reporting it as acceptable.
- When a user says `pass edit` should use the terminal, distinguish the GPG password prompt from the editor: configure the tracked GPG Agent pinentry program rather than changing `EDITOR` or an i3 shortcut.

- 2026-04-16: Fixed `readme-recruiter-sync` to resolve metadata repo-agnostically (`dot_agents/` first, then repo `.agents`, then `$HOME/.agents`, plus optional `READMERECRUITERSYNC_SKILL_DIR`) and derive repo root by walking up to nearest README. This prevents terminal-specific false failures in repos without local skill copy.
- 2026-04-27: When Graphiti MCP needs to be available on login, mount `/dev/sdc1` to `/mnt/linux-files-3` only when the device exists and start `docker compose -f ~/coding/graphiti/mcp_server/docker/docker-compose-neo4j.yml up -d`; skip startup cleanly if host port 8000 is already bound so startup can continue.
- 2026-07-12: When completing a bug fix or incident repair in `/home/example/linux-config`, add a concise linked postmortem under `docs/postmortem/` covering symptom, impact, evidence, root cause, resolution, verification, and follow-up.
- When compacting always-loaded instructions, validate the active plan against its contract and move conditional invariants into the named lazy reference instead of dropping them.
- 2026-07-14: When passing search patterns through a shell command, never place Markdown backticks inside a double-quoted argument; use a single-quoted or fixed-string pattern because command substitution can mutate external state. See the [early-push postmortem](../docs/postmortem/2026-07-14-shell-interpolation-early-push.md).
- 2026-07-14: A successful chezmoi dry-run of nested file targets does not prove a clean first install can create missing destination parents. Exercise the real empty-parent path; create only missing parents transactionally; preserve existing modes; reject symlinks; and keep the chezmoi file target list exact. See the [timer activation postmortem](../docs/postmortem/2026-07-14-timer-runtime-parent-not-installed.md).
- 2026-07-14: A fake external command that returns success regardless of argv can hide an invalid real CLI contract. Make installed-layout fixtures reject unexpected arguments and exercise the real mapping before shipping. See the [installed-resolution postmortem](../docs/postmortem/2026-07-14-installed-runtime-relative-chezmoi-path.md).
- 2026-07-14: Before running `refresh-config` while `dot_codex/config.toml` is a protected dirty file, run the snapshot dry-run and compare live/source ownership. The refresh workflow intentionally copies live to tracked, so use exact deployment targets when that overwrite is not authorized. See the [protected-config postmortem](../docs/postmortem/2026-07-14-refresh-config-protected-file-overwrite.md).
- When a multi-step terminal helper has a clear all-success outcome, suppress successful step noise and emit one conspicuous completion line only after every command succeeds; retain failure diagnostics.

- 2026-09-19: A browser music dashboard can publish usable MPRIS metadata without a site URL. Inspect live player state before adding a Discord bridge, document browser-wide selection, and bind i3block clicks to the last displayed unique owner rather than reselecting a different player at click time. See [FlaviBot now-playing](../docs/postmortem/2026-09-19-flavibot-now-playing.md).

- 2026-09-19: In chezmoi sources, use `executable_` (underscore) for installed commands; Git executable bits and an `executable-` prefix are insufficient. Test a real isolated apply and the installed PATH command, not only checkout execution.

- 2026-09-20: Chrome profile-picker profiles can share one browser process and MPRIS owner. For source-specific media filtering, verify a distinct --user-data-dir process and independent MPRIS identity before recommending profile isolation as a solution. See [YouTube media filter investigation](../docs/postmortem/2026-09-20-youtube-media-filter.md).

- 2026-09-28: A short `ffmpeg -c copy` probe of an iPhone MOV can lose container `creation_time`; preserve that timestamp explicitly before testing capture-order logic on trimmed samples. See [concat sample metadata loss](../docs/postmortem/2026-09-28-concat-sample-metadata-loss.md).

- 2026-09-28: Before using FFmpeg concat demuxer with `-c copy`, compare video time bases, codec parameters, color formats, and rotation. A zero FFmpeg exit can still produce a frozen second segment; verify video/audio durations and decode across the boundary. See [the Logic/iPhone join postmortem](../docs/postmortem/2026-09-28-logic-1377-stream-copy-freeze.md).

- 2026-10-03: When retaining a skill under a new name, migrate its metadata assertions with its test root while keeping all behavioral assertions intact; inspect the complete contract suite before the first GREEN run. See [metaprompt integration validation](../docs/postmortem/2026-10-03-metaprompt-integration-validation.md).

- 2026-10-03: SSH helpers that parse login-shell output must establish a newline boundary after startup; fish can emit cursor-control bytes without a newline. Test every parsed shell command with noisy real fish startup, not only clean PATH fixtures. See [VPS shell handshake](../docs/postmortem/2026-10-03-vps-codex-shell-handshake.md).

- 2026-10-03: For Codex subscription benchmarks, count outbound inference requests rather than CLI sessions, verify real fixture tool execution with injected zero-inference responses before paid trials, and sum request-level usage even when an episode aborts. Report request-cap failures separately from wrong answers; preserve every development attempt and freeze scoring before held-out execution. See [benchmark runtime diagnosis](../docs/postmortem/2026-10-03-metaprompt-benchmark-trial-infrastructure.md).

- 2026-10-03: Calibrate native skill handoffs before freezing a benchmark: explicit final Markdown links are valid artifacts, standard Python helpers need matching standard exceptions, and infrastructure readiness must not require every candidate to answer correctly. Preserve original development records and resume only unused stages, keeping all charges. See [selection validation](../docs/postmortem/2026-10-03-metaprompt-selection-validation.md).

- 2026-10-04: For Kitty diagnostics, load the explicit config path and inspect finalized `keyboard_modes`; avoid top-level generator scope assumptions in `kitty +runpy`. Run existing terminal regressions before editing so stale st-only launcher assertions are distinguishable from new failures. See [Kitty scrollbar inspection](../docs/postmortem/2026-10-04-kitty-scrollbar-inspection.md).

- 2026-10-04: Verify an i3 Codex shortcut using its exact Node and CLI paths; fnm's default alias can select an older runtime than interactive fish. Do not change current model settings to accommodate the wrong diagnostic binary. See [the launcher mismatch](../docs/postmortem/2026-10-04-kitty-scrollbar-inspection.md).

- 2026-10-04: A clean `git status` for `dot_codex/config.toml` may reflect skip-worktree, not committed content. Inspect `git ls-files -v` and HEAD before session scoping; ship only the authorized hunk while preserving the flag and unrelated live settings. See [the commit-scope probe](../docs/postmortem/2026-10-04-kitty-scrollbar-inspection.md).

- 2026-10-03: Validate the rendered form of reusable benchmark templates with multiline bindings: a trailing instruction can become part of the last data line and invalidate exact-copy controls. After a freeze, preserve primary results and disclose an equal-arm omission sensitivity instead of silently repairing the scored fixture. See [selection validation](../docs/postmortem/2026-10-03-metaprompt-selection-validation.md).

- 2026-10-04: Validate an explicitly designated external data root against its current repository topology. A blanket no-Git guard can reject the authorized private destination; test a narrow exact-root exception while retaining ancestor, arbitrary-root, installed-skill, and link protections. See [private context root](../docs/postmortem/2026-10-04-personal-context-private-root.md).
- 2026-10-04: Keep skill smoke checks reproducible from repository tests; managed system-skill helper paths can become unavailable after refresh. Locate an intact validator rather than rebuilding one from fragments, and rerun any checks skipped by a failed command chain. See [validator after refresh](../docs/postmortem/2026-10-04-personal-context-validator-after-refresh.md).

- Source coverage must compare discovered reports and selected-root ledger aliases in both directions; exclude actual template artifacts without skipping incidents that mention templates.
- When checking source versus installed packages, compare the deployable file set and account for documented cache exclusions and concurrent shared-ledger updates. Preserve another task’s new evidence instead of restoring a stale deployment snapshot.

- 2026-10-05: Validate i3 titlebars on a visible workspace using `actual_deco_rect` (with `deco_rect` fallback), not stale hidden-workspace geometry. Allow a compositor frame and use a unique screenshot path; scrot can suffix an existing filename. See [the overview probe investigation](../docs/postmortem/2026-10-05-kitty-overview-inspection.md).

- 2026-10-06: Local Codex JSONL indexing must validate discriminant types and UTF-8 text after JSON decoding; syntax-valid records can still contain arrays in type fields or lone surrogates. Preserve good neighboring records and cover terminal-control cwd plus early-closing pipe behavior. See [search record validation](../docs/postmortem/2026-10-06-codex-search-malformed-records.md).
- 2026-10-06: fzf selection wrappers should capture stdout only and inherit stderr for the UI. Verify real picker presentation as well as stubbed argv; real resumed Codex may append lifecycle records even with zero prompts. See [picker stream verification](../docs/postmortem/2026-10-06-codex-search-picker-ui.md).
- 2026-10-06: A bounded search excerpt also needs bounded highlight work: skip rg submatches outside its byte window before decoding offsets. Preserve matched trailing CR characters, escape controls before coloring, and test both dense lines and narrow Unicode PTYs. See [search output readability](../docs/postmortem/2026-10-06-codex-search-output-readability.md).

- 2026-10-06: When splitting a portable skill helper, load siblings relative to __file__ and describe the dynamic callable/validated JSON boundary with an explicit Protocol and TypedDict. Preserve direct-file-import tests and rerun basedpyright as well as CLI tests. See [context helper imports](../docs/postmortem/2026-10-06-context-helper-sibling-import.md) and [typed boundary](../docs/postmortem/2026-10-06-context-helper-type-boundary.md).
- 2026-10-07: Recent-session recap reads must tolerate concurrent cache clearing; count attempts after acquiring generation ownership and clean safe orphan atomic files under the maintenance lock. Verify the actual CLI index lock during a sleeping inference, not only after the batch. See [cache lifecycle review](../docs/postmortem/2026-10-07-codex-recent-cache-races.md).
