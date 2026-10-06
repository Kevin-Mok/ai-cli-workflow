# Smoke Tests

Use this checklist to confirm that a changed part of `/home/example/linux-config`
works as expected. Find its section, carry out the `Action`, and compare the
result with `Expected`. When a change adds a manual check or reveals a gap,
update the relevant entry or add one under the right area, replacing stale
checks rather than duplicating them.

## Codex Session Search

Run the installed command from any directory; before installation, use
`./scripts/executable_codex-search` from the repo root. Replace example search
phrases with text known to occur in your saved conversations. The synthetic
fixture below provides a repeatable picker check without using private history.

- Action: codex-search --help
  Expected: Usage, flag descriptions, examples and documentation paths appear;
  exit status is 0, without indexing or launching Codex. `-h` and no arguments
  also show help. Help works without rg or fzf installed.
- Action: codex-search -iF "tool output"
  Expected: Matching sessions appear once per UUID,
  newest activity first, with optional title, timestamp, original directory,
  snippets and a copyable resume command. Run the same command again to confirm
  it reuses the private cache;
  progress and malformed-data warnings go to stderr. `csg` expands to `codex-search`
  in fish and the existing `cs` abbreviation still clears the terminal.
- Action: codex-search -F "tool-only phrase"
  Expected: After replacing the example with text present only in a saved tool
  result, no session matches (exit 1). Keep that exact phrase for the next check.
- Action: codex-search --all-text -F "tool-only phrase"
  Expected: The tool-result phrase now matches; system/developer instructions and
  reasoning stay excluded. Matching flags follow ripgrep behavior.
- Action: codex-search --pick -iF "tool output"
  Expected: The matching rows appear in fzf. Press Esc, then rerun and select a
  session whose recorded directory still exists.
  Esc launches nothing. Enter opens the selected history in its original
  directory through the normal Codex launcher. Inspect `/status` to confirm the
  directory without submitting a prompt. A missing or invalid recorded directory
  prevents resume. If fzf is absent, the error explains installation.
- Action: python3 tests/scripts/codex_search_live_check.py
  Expected: From the repo root, synthetic results and a real fzf picker appear.
  Press Esc to verify cancellation; rerun and press Enter to verify the stub
  receives the exact resume UUID and directory containing spaces. Exit 0;
  no real conversation opens.
- Action: python3 tests/scripts/codex_search_live_check.py --real-resume
  Expected: Enter opens the synthetic saved history in the installed Codex CLI.
  Inspect `/status` for its synthetic UUID and temporary original directory,
  then exit without submitting a prompt. This fixture uses a localhost-only
  provider and copies no private history.
- Action: codex-search -iF "tool output"
  Expected: After an ordinary Codex message adds this phrase, the matching log
  refreshes automatically; deleted source logs disappear from results.
- Action: codex-search --rebuild-index
  Expected: All local session logs are reparsed, with progress on stderr and
  exit 0. Large histories can take a minute or more. Original sessions stay
  unchanged; private cache directories are 0700 and files 0600.
- Action: codex-search --clear-cache
  Expected: Only this resolved Codex home's index is removed, retaining its
  lock and original sessions. Exit 0; the next search recreates the cache. See
  the [operator guide](codex-session-search.md) for tests, timings and rollback.

## VPS Codex Updates

- Action: ./scripts/executable_fix-vps-codex.sh --help
  Expected: Usage shows the default VPS, SSH overrides, dry run, prerequisites,
  and no sudo requirement; it does not connect.
- Action: ./scripts/executable_fix-vps-codex.sh --dry-run
  Expected: SSH diagnostics show paths, versions, ownership, inferred npm
  prefix, and the current Codex Node requirement. No repair files or npm
  caches are written; unrelated server login hooks remain outside the helper.
- Action: ./scripts/executable_fix-vps-codex.sh
  Expected: The helper installs into a user-owned prefix, prints a backup and
  rollback command if configuration changes, then reports SUCCESS only after
  a second SSH session runs the ordinary npm update and Codex version command.
  Repeating this action succeeds without duplicate configuration blocks.
  Fish cursor sequences or banners without trailing newlines do not cause
  environment/command-type/version parsing errors. Missing desktop-path
  warnings can still be printed by the existing VPS shell configuration.
- Action: ssh example-user@192.0.2.10
  Expected: In this new terminal, `command -v codex` resolves to the intended
  user installation and `codex --version` runs. Restart an existing Codex
  process to use its new executable. See the [repair guide](fix-vps-codex.md)
  for shell conflicts and configuration rollback.

## Skills And Docs

- Action: Add or change a repo-tracked skill under `dot_agents/skills/`.
  Expected: The skill definition, `dot_agents/skills/README.md`, and the
  root `README.md` stay aligned with the new workflow the skill adds or
  changes.
- Action: Run `open-pr` on a feature branch with a clear base branch and
  at least one changed file relative to that base.
  Expected: The skill inspects `git status`, current branch, `git
  merge-base`, merge-base `git log`, merge-base `git diff --stat`, and
  changed files before drafting a title/body; it lists inspected evidence,
  says what was not run or captured, and updates `docs/pr/` only when the
  repository workflow calls for a PR doc.
- Action: Run `commit-plan` on a dirty tree whose changes clearly include
  an older prerequisite change and a newer follow-up change.
  Expected: The proposed commits, optional manual commands, and commit
  message summary all list the older change before the newer follow-up.
- Action: Run `commit-session` after it establishes a safe, non-empty scoped
  set and a focused validation or rerun README gate reports a non-safety
  failure.
  Expected: The workflow records the failure as a warning, repairs any
  truthful in-scope README finding, and stages only the verified scoped files;
  unsafe or unattributed hunks and inseparable README repairs are reported
  residuals while other eligible files still commit.
- Action: Invoke `commit-session` in a disposable test repository after a
  directly observed edit, with missing `CODEX_THREAD_ID` or unavailable helper
  logs, a baseline-dirty touched file, unrelated staged work, and no upstream.
  Expected: It uses direct-write evidence, prioritizes touched files, includes
  safe matching docs/plans, commits separable session hunks, preserves unrelated
  working and staged changes, and reports the missing push target.
- Action: Invoke `commit-dirty` or `commit-plan-push` with reviewable requested
  changes, a deliberately failing check, an inseparable README conflict, and a
  prohibited secret/cache file in a disposable repository.
  Expected: It commits every eligible change in the requested scope, records
  failed checks and README residuals, excludes prohibited files, and reports
  the actual commit and push outcomes without bypassing hooks.
- Action: Invoke `commit-plan` with the same mixed scope.
  Expected: It plans every eligible group with warnings and companion docs,
  preserves prerequisite chronology, and performs no Git writes.
- Action: Finish a task that introduced a reusable manual verification
  step or exposed a missing smoke check.
  Expected: This document gains or updates a grouped `Action` +
  `Expected` entry instead of leaving the check only in chat, plans, or
  final notes.
- Action: Invoke `metaprompt-alxve` for a trivial request, then ask it to compile and
  run a current-source comparison; include `run` inside a revision before
  sending standalone `go`.
  Expected: The trivial prompt stays lightweight. Both prompts include the
  prompt/Saved/Run/Weight gate, and each saved `prompts/<kebab-case>.md`
  contains only its compiled prompt; a collision receives a non-destructive
  suffix. Neither embedded run phrase executes anything, and only fresh
  standalone `go` starts the current pass.
- Action: Invoke `metaprompt-alxve` for a reusable target-specific template with
  examples, a hostile supplied artifact, and a high-stakes
  judge/rewrite/re-check workflow; send `go` only for the first pass.
  Expected: The template uses canonical `{{variable}}` slots and `Template:
  yes`; material target adaptation is labeled; supplied instructions remain
  untrusted data; three numbered prompt blocks are independently runnable; and
  later passes remain gated until each receives its own fresh standalone `go`.
- Action: Invoke `$metaprompt` to sharpen a rough meeting-summary prompt, then
  request a reusable version with `{{meeting_notes}}` and a trivial fact prompt.
  Expected: Returns Sentry's eight sections: Target, Success Criteria, External
  Context, Optimized Prompt, Adapter Notes, Eval Set, Optimization Log and
  Residual Risks. The Optimized Prompt uses a prompt fence followed by its saved
  path; only that prompt is saved under `prompts/`. Preserves template variables
  and missing-data rules, uses a suffix on filename collisions, and does not
  execute the embedded production task. Prepared cases and executed evaluations
  are distinguished. No legacy `go` gate is imposed by this version.
- Action: In a fresh session in a disposable workspace, invoke `$metaprompt-run Create result.txt containing exactly metaprompt-run-ok followed by one newline. Preserve existing prompts. Do not commit, push, deploy or contact anyone.`
  Expected: **Metaprompt & Run** uses the current metaprompt workflow, presents
  its compact eight-section package, saves only the compiled prompt under
  `prompts/`, reads it back, then creates `result.txt` with exactly
  `metaprompt-run-ok\n` in the same turn. The final result links the saved prompt
  and reports actual verification. No extra `go` or permission question appears
  solely because compilation finished.
- Action: Invoke `$metaprompt-run` with a request whose prompt filename already exists, then request a summary of `{{meeting_notes}}` without supplying notes.
  Expected: The collision uses a new suffix and preserves the original file.
  Missing notes leave execution pending; the agent saves the compiled prompt
  when feasible and asks for the notes without inventing a summary. Explicit
  execution exclusions and normal tool permissions remain binding.
- Action: python3 dot_agents/skills/metaprompt/scripts/update_upstream.py --check
  Expected: Reports pinned and latest `getsentry/skills` prompt-optimizer commit IDs without modifying
  tracked or installed files. A successful check exits 0 even if an update
  is available; use the reviewed staging procedure in
  [the source record](../dot_agents/skills/metaprompt/SOURCE.md).
- Action: `python3 scripts/metaprompt-selection.py verify`, then
  `python3 scripts/metaprompt-selection.py dry-run`.
  Expected: three pinned native finalists, 27 verified package files, 26 valid
  reference answers and seven coding RED/GREEN pairs; the schedule contains
  20 development and 80 held-out attempts within the 100-trial/2,000-request
  ceilings. Count the actual schedule: its original allocation summary retains
  the pre-calibration 90/2 values. Neither command invokes a model. See the
  [selection report](metaprompt-selection.md) for the phase and resume contract.
- Action: Run `python3 tests/test_metaprompt_selection_runtime.py` and
  `python3 tests/test_metaprompt_selection_install.py`.
  Expected: the real CLI reads/writes fixture artifacts and executes public
  checks against synthetic responses with zero remote inference; pinned staging
  and rollback pass only in temporary directories, preserving collisions,
  modified copies, extra files and symlinks.
- Action: After an executed selection, run
  `python3 scripts/metaprompt-selection.py report`, then
  `python3 scripts/metaprompt-selection-analysis.py --run benchmarks/metaprompt-selection/runs/selection-2026-10-03`.
  Expected: recommendation and workflow rates derive from the complete paired
  held-out schedule; all development and failed reservations remain charged.
  Missing usage stays unknown, native completion is distinct from downstream
  correctness, and no skill is installed by reporting. Analysis verifies the
  frozen hashes and request evidence, writes `analysis.json`, and includes
  exploratory paired intervals without making model calls. For the completed
  run, `report` also prints the committed compact `summary.json` fields; its
  ignored `results.json` duplicates the retained per-trial records. For
  `selection-2026-10-03`, confirm 80 held-out rows, 100 total attempts,
  754 requests, no integrity errors, and Sentry selected at 14/16 against
  Wshobson 13/16, Senior 11/16 and both controls 15/16. The equally omitted
  ambiguous-template sensitivity leaves primary scores and costs unchanged;
  raw/minimal are 15/15 and Sentry's weighted success is 85.42%. Native gate
  flags must retain the documented heading-matcher and no-mandatory-gate caveats.
- Action: python3 scripts/metaprompt-benchmark.py verify
  Expected: Verifies seven variants, 71 pinned candidate files, and 32 synthetic
  fixtures (8 development, 24 held-out); makes no model calls or installed changes.
- Action: python3 scripts/metaprompt-benchmark.py dry-run
  Expected: Shows gpt-6.1-sol at medium reasoning, the 50-request cap, fixed pilot
  schedule, and pending cases. Does not use quota or reset an existing ledger.
- Action: python3 scripts/metaprompt-benchmark.py report
  Expected: Verifies frozen inputs and rebuilds machine-readable results from
  the frozen schedule and saved attempts without model calls. Changed frozen
  inputs stop reporting. Failures, pending pairs, unknown costs and limited coverage remain visible;
  see [benchmark replay and runtime status](metaprompt-benchmark.md).
- Action: python3 scripts/metaprompt-benchmark-analysis.py
  Expected: Derives request-level costs, including aborted episodes, from the
  frozen saved evidence. The 49 measured requests plus one setup attempt
  reconcile to the unchanged 50-request ledger; no model calls are made.
- Action: Finish a change with a user-observable CLI, browser, package, API, or
  rendered-config surface after automated tests pass.
  Expected: Verification still exercises the real user entrypoint, captures
  observed evidence, covers invalid input when relevant, and considers an
  adjacent edge probe when it would add useful runtime evidence instead of
  treating automated tests alone as runtime proof.

## Installed Skill Surface

- Action: Apply a tracked skill change to the live `~/.agents/skills/`
  install.
  Expected: The installed skill copy matches the repo-tracked source so
  future sessions see the same instructions and metadata.
- Action: sync-design-skills --dry-run
  Expected: Chezmoi previews only the five managed public-source refreshes and
  does not run the UI/UX Pro Max updater, authenticate any service, generate
  media, or spend credits.
- Action: setup-design-skills-timer --check
  Expected: The tracked helper and daily `Persistent=true` units validate
  without sudo; after `--enable`, `systemctl --user list-timers
  design-skills-sync.timer --no-pager` shows the next refresh.
- Action: Open the Codex skill picker and select `Commit Plan & Push`.
  Expected: It invokes the stable `$commit-plan-push` skill with its managed
  title and `agents/openai.yaml` metadata. On a mixed dirty tree, it makes a
  best-effort pass over every safe, reviewable change, records validation
  warnings, leaves unsafe files as named residuals, and still attempts the
  configured push. Picker ordering is controlled by Codex; no unsupported
  priority field is relied on.
- Action: sync-superpowers-release --dry-run
  Expected: The helper runs `chezmoi apply --refresh-externals` in dry-run
  mode for `~/.codex/superpowers` and
  `~/.agents/skills/superpowers`, rendering the latest
  `obra/superpowers` release archive without writing files.
- Action: setup-superpowers-release-timer --enable
  Expected: The optional timer installs and enables without sudo, with the daily 05:00 local-time schedule and `Persistent=true` configured.
- Action: setup-superpowers-release-timer --check
  Expected: The installed units validate successfully from the standard `$HOME/linux-config` checkout.
- Action: systemctl --user list-timers superpowers-release-sync.timer
  Expected: The timer row shows its next 05:00 local-time trigger.
- Action: journalctl --user -u superpowers-release-sync.service
  Expected: This is an inspection step; the journal may be empty until the scheduled 05:00 run or a `Persistent=true` catch-up run occurs.
  An empty journal does not mean enabling the timer failed or that enabling immediately ran the service.
- Action: setup-superpowers-release-timer --disable
  Expected: The timer is stopped and disabled while the managed unit files remain installed.
- Action: setup-superpowers-release-timer --disable
  Expected: Cleanup remains idempotent: the timer stays stopped and disabled without sudo.

## Personal-context chatbot

The chatbot is explicitly invoked. These checks cover adaptive conversation,
private structured learning, and installation. Automated checks use invented
temporary data; real personal notes are not fixtures or repository artifacts.

- Action: python3 -B -m unittest discover -s tests -p 'test_personal_context*.py' -v
  Expected: Synthetic storage and installed-layout tests pass, including explicit-only metadata, selective reads, source/inference labels, corrections, retry safety, forgetting, declined questions, invalid JSON, containment, permissions, and concurrent updates.
- Action: python3 -B tests/test_personal_context_skill.py
  Expected: Frontmatter and explicit-only metadata parse, supporting references resolve, and a fresh installed layout links the complete skill. This check needs Python 3.12+ and PyYAML; it does not depend on a machine-local copy of the system skill validator.
- Action: python3 ~/.agents/skills/personal-context/scripts/context_store.py validate
  Expected: After initialization, the installed helper reports only safe schema/revision/count metadata. Missing or invalid private memory produces an actionable error without replacing it or printing its contents.
- Action: In a fresh Codex session, invoke `$personal-context` without a topic.
  Expected: It uses relevant private context, opens with one useful conversational question, and follows answers across turns. It does not require a ExampleProject goal or an implementation task.
- Action: Invoke `$personal-context Let's discuss a development choice I'm struggling with.` and supply a real dilemma.
  Expected: Follow-ups respond to the dilemma and connect learnings to concrete options and tradeoffs. Current project/audience requirements remain authoritative over personal visual taste.
- Action: During an invoked discussion, state a preference, correct it, decline a question, and mark another answer temporary. Later invoke the skill again.
  Expected: Durable updates are summarized and remembered privately; the correction supersedes old guidance, the declined question is not repeated by default, and the temporary answer was not persisted. Interpretations remain visibly unconfirmed.
- Action: Ask the invoked skill to forget one structured learning, then resume that topic in a later invocation.
  Expected: All structured versions of that key are removed and automatic reimport is suppressed. The chatbot explains when original source notes still contain it; those notes are not silently edited.
- Action: Start a separate ordinary coding request without invoking the chatbot.
  Expected: No personal-context read, write, check-in, or indirect invocation through Second Brain/feedback-memory occurs. Private discussions never enter tracked feedback, raw capture, Graphiti, or the vault.

## Second Brain

- Action: python3 -B -m unittest tests.test_second_brain_command tests.test_second_brain_timer tests.test_second_brain_skill -v
  Expected: Fixture-only deferred reminders support private `someday` records, future-date scheduling, 04:00 persistent promotion, count-only status, opt-in private listing, and no tracked-vault reminder text.
- Action: scripts/executable_second-brain defer --help
  Expected: Help exposes the private defer command without printing or creating reminder text.
- Action: scripts/executable_setup-second-brain-timer --check
  Expected: After the verified install, the checkpoint and deferred 04:00 timer units both validate without sudo.


- Action: scripts/executable_second-brain status --format json
  Expected: The source entrypoint reports schema version 1, the Toronto-local
  date, the three approved active projects, Inbox state, and up to three recent
  Daily Notes without exposing raw text or modifying tracked files.
- Action: env -C /tmp second-brain status --format json
  Expected: The installed command resolves the chezmoi source vault from an
  unrelated directory and reports the same safe status fields.
- Action: scripts/executable_second-brain doctor --format text
  Expected: The read-only text audit reports a passing vault without printing
  private raw capture or changing tracked files.
- Action: scripts/executable_second-brain doctor --format json --check
  Expected: The deterministic schema-version-1 report exits 0 with no objective
  errors; unsafe imports, hard links, visibility, secrets, and non-LFS media
  would make the check fail without leaking their content.
- Action: scripts/executable_second-brain migrate --help
  Expected: Help lists inventory, plan, apply, and verify without reading or
  copying any migration source.
- Action: python3 -B -m unittest tests.test_second_brain_migration tests.test_second_brain_migration_apply -v
  Expected: Fixture-only inventory, approval, source-policy, collision,
  exclusive-create, resume, and checksum contracts pass; no real user path is
  migrated.
- Action: scripts/executable_second-brain upgrade --dry-run
  Expected: The read-only schema-v1 preview exits 0 with an empty operations
  list for the complete initial vault and changes no file.
- Action: python3 -B -m unittest tests.test_second_brain_command tests.test_second_brain_concurrency -v
  Expected: Fixture-only capture, focus, and closeout retries are idempotent,
  changed payloads and concurrent editor saves conflict safely, closeout rolls
  back only its own unchanged write, raw text stays in private XDG state, and
  a held mutation lock blocks writes until it is released.
- Action: Run `scripts/executable_snapshot-codex-config --dry-run`, then run
  `scripts/executable_snapshot-codex-config` with a valid live Codex config and
  its normal chezmoi mapping.
  Expected: The dry run validates both owned regular files, the strict size
  boundary, TOML, likely-secret content, and mapping without changing the
  tracked target; the normal run is either an exact noop or one atomic,
  mode-preserving target update, and neither result prints config contents.
- Action: On an attached branch with a configured upstream and clean index,
  make one sanitized allowlisted note change strictly smaller than 1,000,000
  bytes, then run `scripts/executable_second-brain checkpoint --dry-run`.
  Expected: Content-free JSON lists only allowlisted candidates, including the
  config target when its live bytes differ; no path is staged, committed, or
  pushed, while sensitive, secret-like, oversized, or non-LFS content fails
  closed.
- Action: In a disposable clone with a local test upstream, exercise a safe
  LFS-media `checkpoint --no-push` followed by a normal checkpoint, an
  arbitrary failing pre-push hook, a generic commit-command failure, and a
  rejected push; then clone the remote and run `git lfs pull`.
  Expected: The successful commit uses
  `chore(second-brain): checkpoint YYYY-MM-DD` and an immutable tree of exact
  allowlisted paths; the arbitrary hook and unrelated tags are not sent, the
  fresh clone recovers exact LFS bytes, cleanup never consumes concurrent state,
  and an upload, commit, or ref-push failure preserves the local evidence
  without moving the remote branch.
- Action: Only after the verified implementation series is pushed, run
  `scripts/executable_setup-second-brain-timer --enable`, then `--check` and
  inspect `systemctl --user list-timers second-brain-checkpoint.timer`.
  Expected: No sudo is requested; the installed launcher, runtime-package
  modules, and units match their chezmoi sources; generated bytecode is not a
  managed target; and unexpected runtime-package root entries fail before
  activation. A clean first install creates only its missing install parents,
  preserves modes on existing parents, and rolls back newly created parents if
  any later parent is unsafe. The timer is enabled with `Persistent=true`, and
  its next local trigger is 16:20. Any immediate catch-up is handled as a
  separate authorized daily checkpoint.
- Action: After one timer checkpoint, run
  `journalctl --user -u second-brain-checkpoint.service`, then run
  `scripts/executable_setup-second-brain-timer --disable` twice, including once
  from the installed layout with the source checkout and chezmoi unavailable.
  Expected: The journal reports an actionable content-free outcome without
  note or config contents, and both disable calls leave the user timer stopped
  and disabled without sudo while preserving the managed unit files; disable
  requires neither chezmoi nor the source checkout.

## Repo Instructions

- Action: Start a fresh Codex or Claude Code session in this repo and ask it to describe the canonical instruction file and delivery cadence without creating or pushing commits.
  Expected: It identifies `dot_codex/AGENTS.md` as the single policy body, treats the root AGENTS files as routing layers, and explains that a verified single-commit workflow pushes once while multi-commit work waits until the complete verified series; no Git write occurs.
- Action: Add or change a standing workflow rule in `dot_codex/AGENTS.md`.
  Expected: The corresponding public docs and reusable verification guidance stay in sync with that rule in the same change.
- Action: Ask a fresh Codex or Claude Code session to write a how-to guide.
  Expected: Directly below the title, it gives a short, plain-language overview
  of the purpose, intended outcome, and main steps before detailed instructions
  or commands; the explanation is direct and easy to understand.
- Action: In a disposable clone, ask a fresh Codex or Claude Code session to handle and then resolve an unexpected task failure.
  Expected: It immediately creates one dated postmortem under `docs/postmortem/`, records the initial symptom, impact, evidence, current status, and next steps, then updates that same file with root cause, resolution, verification, and follow-up; deliberate RED tests and intentionally exercised failure paths do not create one.
- Action: Start non-trivial work from a plan under `plans/`, then inspect the plan before the related commit is prepared.
  Expected: The plan follows `.agent/PLANS.md` with assumptions, checkboxes, verification evidence, review notes, and progress updates intended for the same commit as the work they describe.
- Action: Run `./scripts/executable_ai-workflow-doctor --repo . --check` from the repository root.
  Expected: The command exits `0` when the AI workflow surface has no objective structural errors; any semantic-conflict candidate is labeled as a non-blocking human-review warning rather than auto-resolved.
- Action: With a declared local provenance archive available, run
  `./scripts/executable_ai-workflow-doctor --repo . --verify-sources --check`.
  Expected: Declared Git commits plus primary and supporting paths resolve;
  reachable mismatches fail the gate, while an unavailable local archive is an
  explicit non-blocking warning and remote sources are not fetched.
- Action: Run `./scripts/executable_ai-workflow-doctor --repo . --format json --snapshot /tmp/ai-workflow-smoke.json`, then compare the unchanged repo with `--format json --compare /tmp/ai-workflow-smoke.json`.
  Expected: The snapshot is valid deterministic schema-version-1 JSON, and the comparison reports zero active-instruction deltas with no added or resolved finding keys.

## Keyboard And Input

- Action: Start a fresh X session on a desktop host that applies this repo's shell and `Xmodmap` config, open a terminal, type a short word, and press Backspace once.
  Expected: Exactly one character is deleted and opening a new bash shell does not rewrite the active keyboard remap.
- Action: Open Neovim with the tracked config, enter the command-line window with `q:`, wait long enough for `CursorHold`, then exit back to the file.
  Expected: Neovim does not raise `E11` for `checktime` while the command-line window is open.
- Action: Remap `Keychron Q11` `M2` to `Print`, start a fresh i3 session on a desktop host with the external keyboard config enabled, press `Print`, drag a screenshot region, and paste into an image-capable app.
  Expected: `scrot` captures the selected region, saves it under `~/Pictures/screenshots/desktop/unsorted/`, and the pasted clipboard contents match the captured image.
- Action: Run `/home/example/scripts/screenshot-all-monitors` from an X session with the three desktop monitors active.
  Expected: One PNG is created under `~/Pictures/screenshots/desktop/unsorted/` with the `screenshot-YYYY-MM-DD_HH:MM:SS.png` naming format, and the image contains the full left-to-right desktop across all three monitors.
- Action: Start a fresh i3 session on a multi-monitor setup, press `Menu` on the monitor you are actively using, and grant microphone permission or install Dark Reader in the dedicated Speechnotes browser profile if needed. Press `Menu` again while the Speechnotes window is focused.
  Expected: i3 startup prewarms a hidden Speechnotes app window, the first `Menu` press recalls it nearly instantly on the current monitor in a centered `1180x820` floating window instead of between displays, extensions remain installable in the dedicated profile, and a second `Menu` press while it is focused hides it back to scratchpad instead of opening another browser window.

## Fish Helpers

- Action: Run `fish -c 'source ~/.config/fish/functions/fn-progress.fish; fn-progress'` during C7S4.
  Expected: The helper identifies the season as C7S4, shows the August 20 through November 1, 2026 schedule, prints a nearest-whole-number percentage, and reports labeled elapsed and remaining whole-day counts rather than an ended message before that timestamp. With a current level, for example `fn 75`, it also reports the whole-day difference ahead of or behind the pace required to reach level 200 by season end and estimates how many whole days remain to reach level 200 at the current level pace. It also shows average levels earned per elapsed season day.
  See the [C7S4 variable-expansion postmortem](postmortem/2026-08-24-fn-progress-fish-variable-expansion.md).

- Action: Connect a Pixel 9 over USB, unlock it, set USB mode to
  `File transfer`, then run `/home/example/scripts/mount-pixel-9`.
  Expected: The script creates `/mnt/pixel-9` when needed, mounts the
  phone with `jmtpfs`, remounts a stale broken `jmtpfs` mount when the
  directory returns input/output errors, reports `Mounted Pixel 9 at
  /mnt/pixel-9`, and exits cleanly with an actionable hint if the phone
  is locked or not in file-transfer mode.
- Action: Run `/home/example/scripts/unmount-pixel-9` after mounting the
  Pixel 9 with `/home/example/scripts/mount-pixel-9`.
  Expected: The script unmounts `/mnt/pixel-9` with `fusermount`,
  stops processes that keep the mount busy, reports `Unmounted Pixel 9
  from /mnt/pixel-9`, and exits cleanly if the phone is already
  unmounted.
- Action: If tracked `dot_codex/config.toml` contains an intentional protected
  change, run `snapshot-codex-config --dry-run`, then compare the live and
  tracked files byte-for-byte before `refresh-config`.
  Expected: The dry-run validates both files without changing either one; a
  failed byte comparison identifies the divergence, so the operator stops and
  reconciles ownership instead of overwriting the protected tracked version.
- Action: Run `fish -ic 'refresh-config'` after changing tracked repo
  configuration on a machine where chezmoi and the shell helpers are available
  and the live Codex config is approved to overwrite the tracked copy.
  Expected: The live `~/.codex/config.toml` and `~/.gitconfig` overwrite their
  tracked sources, ChezMoi force-applies only those two targets without prompts,
  then applies other targets normally; shortcuts regenerate, the helper returns to the invoking Fish session, and
  one bold `REFRESH COMPLETE` line confirms the successful workflow.
- Action: Run `fish -c 'backup-phone-storage'` from a machine that can
  reach the phone over SSH on port `8022`.
  Expected: If Termux has `rsync` installed, `rsync` copies the shared
  storage tree from `$PHONE_IP:/data/data/com.termux/files/home/storage/`
  into `/mnt/linux-files-3/pixel-9`, following Termux storage symlinks
  such as `dcim -> /storage/emulated/0/DCIM`, while showing transfer
  progress, ETA, the current path, and rsync `xfr#/to-chk` counters;
  otherwise the helper exits early with an install hint instead of
  failing mid-transfer.
- Action: Mount an iPad at `/mnt/ipad`, then run
  `rsync-media-date 2026-07-28 /mnt/ipad /mnt/linux-files-3/concerts/jcole`.
  Expected: The July 28 `.MOV`, `.MP4`, and `.M4V` originals beneath
  `/mnt/ipad/DCIM` copy directly into the J. Cole folder with rsync progress,
  overwriting same-named files and creating no DCIM subdirectories.
- Action: ./scripts/executable_largest-day-file-size /mnt/usb-8tb/concerts
  Expected: Three lines report the local dates with the largest combined
  regular file sizes, largest first, using binary units such as
  `2026-08-21 30.5 GiB`. Nested files count, symlinks do not, and equal totals
  put the earlier date first. The command makes no changes and requires no sudo.
- Action: ./scripts/executable_concat-timestamped-videos /mnt/usb-8tb/concerts/logic /tmp/logic-joined.mp4 --list-only
  Expected: `/tmp/logic-joined.ffconcat.txt` lists top-level Pixel and iPhone clips in capture-time order, reading Pixel times from filenames and iPhone times from MOV metadata. Other top-level videos, including an existing `logic.mp4`, remain eligible and sort after timestamped clips. It omits the nested `juicy-j` folder, creates no output video, and needs no sudo.
- Action: ./scripts/executable_concat-timestamped-videos /mnt/usb-8tb/concerts/logic /mnt/usb-8tb/concerts/logic/logic-pair.mp4 --clips PXL_20260928_011900910.mp4 IMG_1377.MOV --list-only
  Expected: `logic-pair.ffconcat.txt` lists exactly the Pixel clip followed by `IMG_1377.MOV`; it excludes `logic.mp4` and all other clips. No output video is created. Remove the list file or use a fresh output name before repeating the check.
- Action: ./scripts/executable_concat-timestamped-videos /mnt/usb-8tb/concerts/logic /mnt/usb-8tb/concerts/logic/logic-pair.mp4 --clips PXL_20260928_011900910.mp4 IMG_1377.MOV --reencode
  Expected: Creates a new SDR H.264/AAC `logic-pair.mp4` with continuous playback and audio across the hard cut. The iPhone HLG source is tone-mapped to SDR, so HDR/Dolby Vision metadata is not retained. The original clips remain unchanged; the command refuses an existing output and needs no sudo.
- Action: ffprobe -v error -show_entries stream=codec_type,duration -of csv=p=0 /mnt/usb-8tb/concerts/logic/logic-pair.mp4
  Expected: The re-encoded pair has video and audio durations close to the sum of the two source clips; neither stream ends at the first clip boundary. Decode or play frames across that boundary before treating a successful FFmpeg exit as proof of a good join.
- Action: python3 tests/check_concat_boundary.py --directory /mnt/usb-8tb/concerts/logic --seconds 2
  Expected: Uses `logic.ffconcat.txt` to select the original clips, excluding `logic.mp4` and unrelated camera files; makes a short stream-copy join and contact sheet for each adjacent pair under a printed `/tmp/concat-boundary-*` directory. Each sample decodes successfully. Review every `boundary.png` across the join and note any reported timestamp warnings; the contact sheets cannot assess audio continuity.

## Claude Code

- Action: Run `chezmoi apply` (or `refresh-config`) on a machine with this repo applied, then check `~/.claude/CLAUDE.md`.
  Expected: `~/.claude/CLAUDE.md` exists and contains a single `@/home/example/linux-config/dot_codex/AGENTS.md` import line, confirming Claude Code will load the shared instruction document globally.
- Action: After `chezmoi apply`, check `~/.claude/skills/` for skill symlinks.
  Expected: `~/.claude/skills/` contains one directory symlink per skill with
  a top-level `SKILL.md` (for example,
  `~/.claude/skills/metaprompt -> ~/.agents/skills/metaprompt`), so supporting
  `references/`, scripts, assets, and metadata remain reachable. Managed legacy
  `<name>.md` links are removed; `README.md` and the `superpowers` entry are not
  linked because they have no top-level `SKILL.md`.
- Action: Launch Claude Code in any project directory and run `/commit-dirty` (or another tracked skill).
  Expected: Claude Code resolves `~/.claude/skills/commit-dirty/SKILL.md` through
  the shared directory and follows the repo-tracked workflow.
- Action: Run `bash tests/test_claude_skill_links.sh`.
  Expected: The isolated installer fixture links a complete skill directory,
  exposes a supporting reference, removes only the matching managed legacy
  link, remains idempotent, and refuses to replace a real user directory.
- Action: After applying this repo, launch Codex and verify `/commit-dirty` still works.
  Expected: `~/.agents/skills/commit-dirty/SKILL.md` is unchanged and Codex
  resolves the skill normally; Claude wiring adds directory symlinks only and
  does not touch the Codex skill surface.

## Codex And Graphiti

- Action: Start a fresh Ubuntu/i3 session on the desktop host where
  `/dev/sdc1` is present and Graphiti is checked out at
  `/home/example/coding/graphiti/mcp_server`.
  Expected: `ubuntu-start` mounts `/dev/sdc1` at `/mnt/linux-files-3`
  using `sudo` when elevation is needed, allowing the operator to enter
  a password instead of silently skipping the mount. It does this before
  applying the `autorandr 4k-3-monitor` profile and the Sukana wallpaper
  through `/home/example/scripts/apply-pywal-theme`, starts at most one
  `picom` compositor, starts `dunst` for notifications
  when available, applies the full 20-button X pointer map without the
  partial-button warning, skips missing optional helpers such as `numlockx`
  without shell errors, then starts the compose Neo4j service with `docker compose -f
  docker/docker-compose-neo4j.yml up -d neo4j`; startup does not try to
  bind Graphiti MCP to host port `8000`.
- Action: Launch `codex` from a shell where `~/scripts` shadows the real Codex binary and Graphiti is installed at `/home/example/coding/graphiti/mcp_server`.
  Expected: The wrapper creates or reuses `${XDG_STATE_HOME:-$HOME/.local/state}/codex-launch/graphiti.pid`, appends Graphiti startup output to `graphiti.log`, and then hands off to the real Codex CLI with the original arguments intact.

## USB SATA Disk Initialization

- Action: bash scripts/hdd-init-wizard.sh --help
  Expected: Usage describes the interactive command, explicit destructive confirmations, and dry-run mode without changing disk or mount state.
- Action: bash scripts/hdd-init-wizard.sh --dry-run
  Expected: Diagnostics show block devices, recent USB/storage messages when readable, USB devices when `lsusb` exists, and only whole disks in the selection list. When no USB disk is detected, the output suggests dock power, cable, switch, and port checks. No partition, filesystem, mount, or fstab write occurs.
- Action: bash scripts/hdd-init-wizard.sh
  Expected: On a host with a USB SATA disk, the wizard blocks the Ubuntu system disk and any disk with mounted children, requires the exact path and any required `ERASE <path>` phrase, then shows all destructive commands before the final `INITIALIZE <path>` confirmation. Cancel before that final phrase to leave the disk untouched. Do not enter the final phrase as part of this smoke check.

## Vim

- Action: Open Vim in a terminal on a host using this repo's rendered `~/.vimrc`, then quit immediately with `:q`.
  Expected: Vim paints the normal editor screen right away and returns to the shell without stopping at a `Press ENTER` prompt for an unsupported option such as `mousescroll`.
- Action: Open Vim in a terminal with the rendered config, wait idle for at least one second on an empty buffer, enter insert mode, type a few characters, then quit with `:q!`.
  Expected: Vim remains responsive after idling, accepts normal keyboard input immediately, and exits without feeling stuck in a redraw or autosave loop.
- Action: Open Vim or Neovim in a terminal after running `wal -i <wallpaper>` and compare the editor background and accent colors against the active terminal palette.
  Expected: Vim loads the `wal` colorscheme by default so the editor palette tracks the current `pywal` theme, the main editing surface, line-number column, fold column, sign column, and end-of-buffer area stay opaque with the current `pywal` background color, and Python syntax looks intentionally color-separated instead of collapsing into a nearly monochrome editor.
- Action: Keep terminal Vim or Neovim open on a Python file, run `/home/example/scripts/apply-pywal-theme <wallpaper>` from another shell, then idle briefly in the editor or refocus the window.
  Expected: The running editor picks up the new `pywal` colors without reopening, including both the background surfaces and the stronger syntax colors.
- Action: Open Vim or Neovim on a Python file that contains nested calls and colon-terminated block headers such as `async def`, `if`, `try`, or `async with`, then scroll the mouse wheel up and down.
  Expected: Scroll-down from a block header enters the first indented statement in that block, while scrolling from ordinary statements jumps to the next or previous nonblank line whose indentation is the same or lower.
- Action: Open Neovim in a Python project with a local `.venv` or `venv`, type `Path(` and `requests.`, and use the normal leader shortcuts on a Python symbol.
  Expected: Blink completion offers Python members and auto-import suggestions, `Up` and `Down` move between suggestions, signature help appears when typing a function call, and `<leader>do`, `<leader>g`, `<leader>rn`, and `<leader>fi` drive the Neovim LSP actions instead of the old YCM commands.
- Action: Open a Markdown file in Vim, press `<F8>`, and edit headings, lists, tables, and fenced code blocks while the preview is open.
  Expected: `markdown-preview.nvim` opens a live browser preview on a free localhost port with GitHub-like dark styling and updates as the file changes.
- Action: With the Markdown preview already open in Vim, press `<F9>`.
  Expected: The preview stops and restarts cleanly on the same file without falling back to the old `InstantMarkdownPreview` commands.

## Audio

- Action: With PipeWire audio playing but silent through the AUX speakers, run `./scripts/executable_fix-aux-speaker-audio --fix`.
  Expected: The current default analog sink is unmuted and active playback streams remain routed to it; `--diagnose` reports the selected sink and service state.

## Terminal

- Action: ./scripts/executable_install-chatgpt-linux
  Expected: On Ubuntu 24.04/26.04, Debian 13, or Fedora 43/44 with an x64 or
  ARM64 processor, the script prints the matching official `.deb` or `.rpm`
  URL, downloads it to temporary storage, and prompts for sudo only for the
  final `apt install` or `dnf install`; unsupported OS versions and processor
  architectures fail before download or elevation. On apt hosts, installation
  completes without the `_apt` sandbox warning about an inaccessible temporary
  package file.
- Action: Run `./scripts/executable_install-tmux-tpm.sh --help`, then run
  `./scripts/executable_install-tmux-tpm.sh` on a host with tmux configured.
  Expected: Help describes the TPM install/update and `prefix + I` follow-up;
  the install creates or fast-forwards `~/.tmux/plugins/tpm`, ensures its
  `tpm` entrypoint is executable, and reloads the active tmux server when one
  is reachable.
- Action: Run `refresh-config`, then `gpgconf --kill gpg-agent`; open a new terminal and run `pass edit <non-sensitive-test-entry>`.
  Expected: When GPG needs the store password, `pinentry-curses` prompts in that initiating terminal and `pass` continues to the configured editor after successful authentication.
- Action: Run `/home/example/scripts/apply-desktop-display-layout`, reload i3, and inspect `xrandr --query`.
  Expected: `DVI-D-0` is 2048x1152 at `+0+0`, `DP-2` is 3840x2160 at `+2048+0`, `HDMI-0` is 1920x1080 at `+5888+0`, and i3 shows bars on all three monitors with the new middle 4K bar using the combined active `spotify`, `volume`, and `calendar` blocks.
- Action: ~/scripts/flavibot-browser
  Expected: After refresh-config, opens https://flavibot.xyz/music-player in a separate Chrome process using ~/.local/share/flavibot-chrome. Sign in once and start playback. Later launches reuse that directory; existing Chrome profiles are untouched. Follow the [short usage guide](flavibot-browser.md) for daily use. Reserve this window for FlaviBot and use ordinary Chrome for YouTube.
- Action: ~/.config/i3blocks/scripts/now_playing_mpris
  Expected: While FlaviBot or Spotify plays, emits `▶ Artist - Title` for both full_text and short_text, with the triangle small and raised via Pango; when paused, emits `‖ Artist - Title` with the pause mark rendered the same way. Both markers sit centered rather than touching the bar's lower edge. The third line is pywal color7. The bar follows within five seconds, retains the artist even when space is constrained, and shows no state glyph when no player is eligible. Title-only songs are also eligible; artist/title regex matching is no longer used.
- Action: Open the dedicated FlaviBot window with no song loaded while Spotify is available, then repeat with Spotify closed.
  Expected: Generic “FlaviBot - Music Player” metadata never appears, whether exposed as a page-title string or artist “FlaviBot” plus title “Music Player”; the block shows Spotify when available and clears its text and click state otherwise. Real FlaviBot song titles, including title-only songs, remain eligible.
- Action: Play YouTube in ordinary Chrome, pause FlaviBot in its dedicated window, and pause Spotify.
  Expected: The block retains the paused FlaviBot song and never shows YouTube. Ordinary Chrome is excluded by process identity, regardless of title, channel, or playback status. YouTube opened inside the dedicated FlaviBot window would still qualify; origin is not exposed by Chrome.
- Action: Play Spotify with dedicated FlaviBot paused, then pause both; close the dedicated FlaviBot window and finally Spotify.
  Expected: Playing Spotify wins over paused FlaviBot; with both paused, FlaviBot wins. Closing the dedicated browser falls back to Spotify, including paused tracks. With neither eligible player, text and click state clear even if ordinary Chrome is playing.
- Action: With a stable track shown, left-, middle-, and right-click the music block, first with dedicated FlaviBot selected and then with Spotify selected. Try a click immediately after the shown track changes or its player closes.
  Expected: Supported actions are PlayPause, Previous, and Next on the last displayed player's unique D-Bus connection only. Stale state (over 15 seconds), changed tracks, unavailable players, or unsupported actions do nothing; clicks never redirect to another player. Global media-key behavior remains unchanged.
- Action: Focus a workspace on the left monitor, press `Alt++` until it moves across the middle 4K monitor to the right monitor, then press `Alt+-` to move it back.
  Expected: Workspace movement follows the physical left-middle-right monitor order and reverses cleanly.
- Action: Launch the primary terminal from an i3 binding that uses this repo's rendered config, then press Super+C to start a fresh Codex session.
  Expected: The normal terminal windows open in `kitty`. The Codex shortcut also uses Kitty and passes --no-alt-screen so its transcript is retained in native terminal history.
- Action: Keep one or more `kitty` windows open, run `/home/example/scripts/apply-pywal-theme <wallpaper>` or trigger one of the wallpaper-changing shortcuts, and then open one additional `kitty` window.
  Expected: The already-open `kitty` windows refresh to the new vivid `pywal` palette without a manual restart, the newly opened `kitty` window uses the same updated colors, and the terminal keeps the repo-configured light translucency without falling back to the earlier heavy wallpaper bleed-through.
- Action: Run `/home/example/scripts/apply-pywal-theme <wallpaper>` with a bright or high-saturation wallpaper, then inspect the i3 workspace bar and focused window chrome.
  Expected: The bar and focused workspace/client colors still feel vivid, but text and icons remain clearly readable against the workspace backgrounds instead of landing on low-contrast combinations such as pale icons over bright yellow backgrounds.
- Action: Open a terminal, run `./scripts/executable_setup-st.sh --skip-install`, and inspect both `~/.config/st/config.def.h` and your `st` source checkout `config.def.h`.
  Expected: The script renders the tracked template into both config locations, preserving the repo's pywal, font, copy/paste, and scrollback settings while printing the exact `sudo make -C <st-source-dir> install` command for the final compile step.
- Action: Open `st`, run enough output to exceed one screen, then scroll upward with the mouse wheel and `Shift+PageUp`.
  Expected: `st` keeps a deep local scrollback buffer so you can continue moving upward through old output instead of stopping after one screen.
- Action: While still scrolled up in `st`, drag-select older output, press `Ctrl+Shift+C`, then paste it elsewhere with `Ctrl+Shift+V`.
  Expected: The copied text comes from the scrolled-back output, and the copy/paste shortcuts match the normal terminal habit without forcing tmux copy mode for basic selection.

### Kitty and Codex overviews

Kitty's i3 titlebar displays Codex's activity indicator and a short summary of
what the agent is doing now. After refresh-config, reload i3 and launch a new Codex
process, including codex resume, to load the updated title settings and instructions.
Switching threads inside an existing TUI is not a startup-config reload. Automatic
summaries also rename saved conversations; they update at meaningful transitions, without
periodic /btw requests. Fullscreen hides i3 titlebars. No sudo is needed.

- Action: Inspect existing Kitty windows after deployment, then open a new Kitty terminal and start Codex using Super+C or codex.
  Expected: Each Kitty window has one titlebar. New/resumed Codex shows an activity indicator and a short current-work summary without the project suffix; ordinary shells show their normal title. Other applications retain their existing border behavior.
- Action: Run two independent Codex conversations in the same repository with different tasks, then change the objective or move to a meaningful new phase in one conversation.
  Expected: Each agent uses its own 3–5-word summary (at most 36 characters). The changed conversation updates its title without renaming the other; the label describes the work rather than the most recent shell command.
- Action: Narrow a split, switch between split and tabbed layouts, and toggle fullscreen on and off.
  Expected: Titles stay within their available width without overlapping neighboring windows. Fullscreen hides the titlebar; leaving fullscreen restores it. No extra header appears inside the terminal transcript.
- Action: Observe an agent while working, awaiting input, and after verified completion; then resume that conversation.
  Expected: Codex's native activity/attention indicator remains available. The summary reflects the current phase or verified result, and its saved conversation name persists across resume.
- Action: In a Codex environment without the native title tool, use /rename to set a short task name.
  Expected: The existing native name remains until manually renamed. The titlebar displays the manual name without introducing a polling service or another model request.
- Action: Repeat the existing Kitty scrolling checks below in a titled window.
  Expected: The scrollbar, paging, selection and inline Codex history still behave as documented.

### Kitty and Codex scrolling

Use a fresh Kitty window after refresh-config: a larger history cannot recover
lines an older window already discarded. This checks one scrollbar per Kitty
terminal window. Inside tmux, use its Alt+C copy mode for pane-owned history.
The fixture uses the normal Kitty configuration without overrides. Ordinary
Codex launches use the persistent tui.alternate_screen = "never" setting;
restart or resume an existing Codex session to pick up that default.
Keep the fixture at least 40 columns wide through the first history check so
wrapping all 10,000 records fits inside the configured 50,000-line buffer.

- Action: /home/example/scripts/kitty-scrollback-smoke
  Expected: A separate window titled “Kitty scrollback smoke test” opens with 10,000 numbered history records and wrapped text. A narrow window first prompts you to widen it to at least 40 columns and press Enter. No sudo, model request, or configuration change is needed. The window keeps the current pywal colors and 0.9 opacity, with a thin rounded scrollbar at the right edge; hovering makes it wider and easier to grab.
- Action: Drag the scrollbar thumb to the start, middle, and end of the fixture history.
  Expected: You can reach HISTORY 000001, intermediate records, and HISTORY 010000. The thumb remains grabbable even with a long history; the track is unobtrusive until hovered.
- Action: Press Shift+PageUp repeatedly, then Shift+PageDown, then Ctrl+Shift+End.
  Expected: The view moves by pages through native history and returns to the newest output. These modified keys control Kitty; plain PageUp/PageDown remain available to the foreground application.
- Action: Drag-select an older record, copy it with Ctrl+Shift+C, paste it into an editor, then resize the test window.
  Expected: The copied number and text match the selected record. Wrapped text remains readable after resizing, and scrolling does not leave persistent rendering artifacts.
- Action: Return to the bottom, press Enter to start streaming, then scroll several pages up while new lines arrive.
  Expected: 300 STREAM records arrive over about 30 seconds. The older text stays in view while output continues; Ctrl+Shift+End returns to the live tail. Once the stream finishes, press Enter to close only the fixture window.
- Action: Start Codex normally from a fresh Kitty window using codex or codex resume, let a normal task produce several screens of output, then drag its scrollbar and use Shift+PageUp/PageDown. Repeat with Super+C.
  Expected: Earlier Codex transcript output remains reachable through Kitty's native history while the session runs. Plain launches use the persistent inline-mode default; Super+C also passes --no-alt-screen and uses the same Codex 0.160.0 installation as the current shell. Already-running sessions retain their original mode. The fixture checks terminal mechanics, while this step verifies actual Codex rendering and streaming behavior.

## YouTube Downloader

- Action: Run refresh-config, then yt-dl --help in Fish
  Expected: Chezmoi installs ~/scripts/yt-dl with execute permission and current source content. Shows the URL argument, /mnt/linux-files-3/yt-vids default, and -o/--output-dir override without requiring downloader dependencies.
- Action: yt-dl 'https://www.youtube.com/watch?v=oLOzkH0zVZo' -o /tmp/yt-dl-smoke
  Expected: In a fresh output directory, creates a lowercase kebab-case title-only filename without a video ID or JSON sidecar, selects yt-dlp's best available video/audio without a resolution cap or MP4 preference, merges separate streams into MKV without transcoding, then automatically checks actual video/audio with ffprobe against fresh yt-dlp formats before printing the absolute final path. Stderr shows download percentage, speed, and ETA during transfer, then the quality-check status and VERIFIED resolution/FPS and whether 4K was verified or not reported. Repeating the command preserves existing media; a lower-resolution or more-than-1%-lower-FPS existing file fails verification and suggests a fresh -o directory. Inconclusive extraction also returns nonzero. Network/platform failures return nonzero with diagnostics.
- Action: python3 tests/check_yt_dl_live.py
  Expected: Retains media in a fresh /tmp/yt-dl-live-* directory and prints PASS only after matching video ID, nonempty file, audio/video streams, duration, and full decode checks succeed. Requires network access, current yt-dlp, ffmpeg, and ffprobe.

## Remote Access

- Action: tests/scripts/executable_setup-aerc-mail_test.sh
  Expected: Fixture-only Gmail and Outlook additions use direct IMAP and their
  respective password/OAuth credential commands; malformed or duplicate labels
  and symbolic targets fail safely; dry runs, status, and test output never
  expose credential values or invoke real OAuth or package mutations.
- Action: Run `sudo ./scripts/executable_setup-mosh.sh` on a Linux host
  meant to accept remote `mosh` sessions.
  Expected: The script installs `mosh` when missing, opens
  `60000:61000/udp` in `ufw` or `firewalld` when one is active, and
  prints whether SSH server bootstrap still needs attention before
  remote clients can connect.
- Action: From Termux on cellular data, run the copied
  `executable_setup-termux-mosh.sh` bootstrap with the PC's existing public
  SSH host, user, and port, then run `ssh pc-remote true` and `pc-mosh`.
  Expected: The bootstrap installs `mosh`, `openssh`, and `rsync`, makes the
  one-way `pc-push`, `pc-pull`, and `pc-sync-*` helpers available, and starts
  a Mosh session through the PC's forwarded `60000:61000/udp` range without
  exposing an SSH server from Android.
- Action: Run `sudo ./scripts/executable_update-chrome.sh` on a Debian or Ubuntu host with the Google Chrome apt repo configured.
  Expected: The script prints the installed and candidate Chrome versions, refreshes apt metadata, upgrades `google-chrome-stable` when needed, and ends with matching installed and candidate versions.
- Action: Run `sudo ./scripts/executable_update-vesktop.sh` on a Debian or Ubuntu host with network access to Vesktop's official download endpoint.
  Expected: The script prints the installed and latest upstream Vesktop versions, downloads and installs the official amd64 `.deb` when needed, and ends with matching installed and latest versions.

## Shared Postmortem Memory

Use these checks to verify retrieval from another repository and learning from a
changed report. The helper commands are read-only; the reusable smoke script writes
only a disposable temporary fixture and requires no sudo.

- Action: python3 -B tests/test_postmortem_memory.py
  Expected: Discovery, aliases, privacy pruning, unreadable paths, changed/missing
  sources, reference/schema contracts, retrieval, status scope and full reviewed
  corpus coverage pass.
- Action: cd /tmp && python3 -B /home/example/linux-config/dot_agents/skills/postmortem-memory/scripts/postmortem_memory.py search "bwrap loopback"
  Expected: It prefers tracked knowledge and returns reference sections with
  verified_workaround status, applicability and source links. Elevation success
  does not claim a repaired sandbox.
- Action: python3 -B scripts/smoke_postmortem_memory.py
  Expected: A cross-repository lookup finds the known workaround; changing a
  synthetic report fails targeted coverage until its reviewed hash and guidance
  are updated. The result remains activation_pending after code verification.
  The script prints PASS and removes its temporary fixture.
- Action: python3 -B dot_agents/skills/postmortem-memory/scripts/postmortem_memory.py scan --root /home/example/coding --root /home/example/linux-config
  Expected: All reviewed physical report aliases remain accounted for with no
  new/changed/unregistered/missing sources or unreadable paths. Copied content is
  one hash; personal-context/private material and dependency/build/git paths are
  excluded before reads. Genuine incidents about template failures remain eligible.
- Action: python3 -B dot_agents/skills/postmortem-memory/scripts/postmortem_memory.py check --postmortem /home/example/linux-config/docs/postmortem/2026-10-05-postmortem-memory-coverage-review.md
  Expected: The current report hash/alias, reciprocal finding links and all
  reference contracts validate. This targeted result does not imply full coverage.
- Action: Ask a fresh agent in another repository to handle a reported bug, then create or materially update its postmortem.
  Expected: It reads postmortem-memory, searches and records applicability before
  retries/remedies; it keeps the immediate living report and directly updates
  tracked linux-config knowledge in the same task, then runs targeted coverage.
  If permissions block that tracked write, it reports the exact path and pending
  learning instead of writing installed memory. A novel search miss leads to a
  new reproducer and review, not an invented known fix.
