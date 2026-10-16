# Smoke Tests

Use this checklist to confirm that a changed part of `/home/example/linux-config`
works as expected. Find its section, carry out the `Action`, and compare the
result with `Expected`. When a change adds a manual check or reveals a gap,
update the relevant entry or add one under the right area, replacing stale
checks rather than duplicating them. Post-commit, push and every task completion handoff
must select commands that directly exercise or verify the completed result through the
actual CLI, app, API, or generated artifact and expose an observable result.
Automated tests, linters, type checks, builds, Git hygiene checks and source-text
searches run before completion and any commit; do not use them to fill the handoff command list.

## Public History Audit

- Action: ./scripts/executable_audit-public-history --scope all --plain
  Expected: The CLI scans every Git commit and unique blob in the local object
  database, emits periodic progress to stderr during a long run, reports PASS
  with zero findings, and exits 0 without printing matched values.


## Directory Sizes

Install the pinned backend into a fresh disposable prefix. These checks inspect a small disposable backend directory; a real backup scan is an explicit opt-in.

- Action: ./scripts/executable_setup-directory-sizes --prefix /tmp/directory-sizes-smoke
  Expected: Dust 1.2.6 is installed into `/tmp/directory-sizes-smoke/bin/dust`, with no sudo. Repeating the command refuses to overwrite it.
- Action: ./scripts/executable_directory-sizes --backend /tmp/directory-sizes-smoke/bin/dust --depth 1 /tmp/directory-sizes-smoke
  Expected: Aligned binary sizes and quoted nested directory names appear on stdout after completion; allocated metric/target and status appear on stderr. No scanned contents or permissions change. Short scans can finish before indexing progress.
- Action: ./scripts/executable_directory-sizes --backend /tmp/directory-sizes-smoke/bin/dust --json --depth 0 /tmp/directory-sizes-smoke
  Expected: Valid JSON root with byte-size string and no displayed children; the whole tree was still scanned.
- Action: DIRECTORY_SIZES_REAL_BACKEND=/tmp/directory-sizes-smoke/bin/dust python3 -B tests/test_directory_sizes.py
  Expected: Nine tests pass, including allocated GNU du equality and explicitly measured logical directory-size difference, safe names, and separate-session interruption cleanup.
- Action: timeout --signal=TERM --kill-after=5s 20s ./scripts/executable_directory-sizes --backend /tmp/directory-sizes-smoke/bin/dust --depth 1 /mnt/usb-8tb/sys-backup/10-06-26.incomplete
  Expected: Run only when a new real probe is explicitly requested. Provisional indexing feedback appears during a long scan. If timed out, exit 124, no completed totals on stdout, and backend stopped/reaped. Reported permission errors return nonzero and withhold totals. Do not interpret progress as completed usage. See [measurements and limitations](directory-sizes.md).

## Codex Session Search

Run the installed command from any directory; before installation, use
`./scripts/executable_codex-search` from the repo root. Replace example search
phrases with text known to occur in your saved conversations. The synthetic
fixture below provides a repeatable picker check without using private history.

- Action: codex-search --help
  Expected: Usage, flag descriptions, examples and documentation paths appear;
  exit status is 0, without indexing or launching Codex. `-h` and no arguments
  also show help. Help works without rg or fzf installed.
- Action: codex-search -F "root"
  Expected: In a terminal, at most 20 newest matching sessions appear with a
  numbered directory/date header, optional title, one short highlighted excerpt
  and a complete copyable resume command. Untitled labels and standalone UUID
  rows do not crowd this compact view. A stderr footer reports any hidden
  matches and explains --limit 0/--pick. Resize the terminal to confirm excerpts
  fit its width. Run the same command again to confirm
  it reuses the private cache;
  progress and malformed-data warnings go to stderr. `csg` expands to `codex-search`
  in fish and the existing `cs` abbreviation still clears the terminal.
- Action: codex-search --details --limit 5 -F "root"
  Expected: At most five full blocks show title, exact timestamp, complete
  directory, UUID, up to five snippets and a quoted resume command. --limit 0
  removes the result cap; the underlying search still considers all sessions.
- Action: codex-search --limit 5 -F "root" | cat
  Expected: The pipe receives at most five full blocks, with no color escapes.
  Piped output without --limit includes all matching sessions.
- Action: NO_COLOR=1 codex-search --limit 5 -F "root"
  Expected: Compact terminal layout remains readable with color disabled.
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

### Codex recent picker best-effort startup

Run fixtures from `/home/example/linux-config`; they use invented sessions, the
actual CLI and real fzf, with no provider calls or sudo. Initial cold-cache
metadata/activity is preliminary; pending dialogue must not trigger inference.

- Action: codex-search --recent --pick --no-summaries
  Expected: Validated cached metadata opens the picker before full archive work
  finishes, including while another refresh holds the index lock. Cold caches
  begin with bounded native metadata and add rows as indexing progresses;
  remaining native titles catch up in the background.
  Uncached pending previews show `AI recap: indexing`; generic rows also show
  `[indexing]`. Cached pending recaps stay stale/unknown. Concise indexing and
  skipped-input status stays visible without per-file warnings flooding the UI. No model calls; Esc cancels safely.
- Action: codex-search --recent --pick --summary-count 0 --details
  Expected: Preview adds a bounded tail of background diagnostics, including
  skipped/unreadable source paths, while default output remains concise. Logs
  are private and temporary. Ctrl-G on an indexing row remembers its request
  and generates only after validated dialogue is available; automatic work
  remains off. Background indexing updates activity; the requested recap can
  update priority after dialogue is ready. Explicit --rebuild-index remains a
  full foreground refresh.
- Action: python3 tests/scripts/codex_startup_live_check.py --scenario all
  Expected: Cold, cached, malformed and locked-index cases reach real fzf from
  available metadata before archive completion; good rows remain usable,
  pending rows avoid inference, and exact resume/worker cleanup pass. No private history/provider calls; exit 0. Individual --scenario cold,
  cached, malformed or locked repeats that case.
- Action: python3 tests/scripts/codex_startup_live_check.py --command "$HOME/scripts/codex-search" --scenario all
  Expected: After refresh-config, the same disposable startup checks pass
  against the installed command and sibling modules; exit 0, no provider calls.

### Codex recent picker priority and Guardian refresh

Run these commands from any directory after installation; use the source command
from the repository root before installation. No sudo is needed. Ordinary
listing is cached-only; opening a picker can generate recaps unless disabled.

- Action: codex-search --recent --pick
  Expected: The `crg` picker ranks urgent, actionable, unknown, waiting, then
  complete sessions, with newest recorded activity breaking ties. Preview shows
  each priority and reason. Missing/legacy/stale priority ranks as unknown; stale
  evidence remains explicitly labelled. The newest summary-count sessions still
  form the automatic generation window, independent of priority order.
- Action: codex-search --recent --pick --sort recent --no-summaries
  Expected: Usable sessions appear newest-first by recorded activity, with
  additional rows arriving as background indexing progresses. Cached recaps
  remain readable; Ctrl-G and automatic refresh cause no model calls. Uncached generic rows show `[recaps off]`. Esc resumes nothing.
- Action: codex-search --recent --sort priority --details --limit 5
  Expected: At most five full blocks appear in cached priority order, with
  priority/reason and freshness visible; no model runs. Ordinary --recent listing
  without --sort remains newest-first and keeps its default limit of 20.
- Action: codex-search --recent --sort recent --limit 5
  Expected: At most five newest sessions appear by recorded activity; no model
  runs. Source filesystem and recap-cache times do not affect ordering.
- Action: codex-search --recent --pick --summary-count 0
  Expected: Automatic generation stays off. Highlight an uncached `[Ctrl-G]` row
  and press Ctrl-G: manual queued/generating progress appears, then its AI
  headline, priority and reason arrive. Manual requests outside the newest
  window work normally. Each unchanged generation key gets at most one attempt
  per opening; changed dialogue can receive a new attempt. Failed recaps show
  `[unavailable]` and explain why in the preview. Esc cancels and stops workers.
- Action: codex-search --recent --pick --no-summaries
  Expected: Cached priority determines order and local evidence refreshes with
  zero model calls, including Ctrl-G. While open, filter by a stable directory,
  highlight a session, and let Guardian or another pane update that session.
  Renames/activity/dialogue changes appear after background discovery; changed
  dialogue makes the older priority stale/unknown. Query and UUID stay stable
  during reorder while still matching. Newly discovered sessions appear and
  deleted ones disappear. Enter with zero matches resumes nothing.

- Action: codex-search --recent --sort priority --plain --limit 5
  Expected: At most five cached sessions appear with ASCII decoration and no
  printed color. Terminal separators/arrows/truncation markers use `|`, `->`
  and `...`; original conversation characters remain intact. No model runs.
- Action: codex-search --recent --pick --plain --no-summaries
  Expected: The recent picker uses ASCII fzf borders, cached priority and local
  evidence refresh with zero model calls; Enter/Esc retain their usual behavior.
- Action: python3 tests/scripts/codex_priority_live_check.py --scenario all
  Expected: From the repo root, the actual source CLI and real fzf use disposable
  sessions and a deterministic local runtime. Guardian append/rename updates
  dialogue/activity/title, urgent-to-complete regeneration reorders while keeping
  query/UUID, and Enter sends the exact UUID/cwd to a resume stub. Source bytes
  change only through fixture appends; watcher/workers and temporary runtime
  directories are removed. Cached/recent second opens and Ctrl-G make zero
  additional calls. Exit 0, no private history/provider calls, no sudo.
- Action: python3 tests/scripts/codex_priority_live_check.py --command "$HOME/scripts/codex-search" --scenario all
  Expected: After refresh-config, the same disposable checks pass against the
  installed command and its installed sibling modules, without private history
  or provider calls. Exact resume, source preservation and cleanup pass; exit 0.

### Codex recent picker layout

- Action: Run `crg`, select a session in `/mnt/usb-8tb/`, and resize the terminal between narrow and wide windows. Press Ctrl-/ twice, then Enter or Esc.
  Expected: The directory appears as `/m/usb-8tb>` beside the complete title when space permits, followed by the short timestamp, without large tab gaps. The full title wraps in the preview; the original directory remains there. The preview is on the right in wide windows and below in narrow ones; Ctrl-/ toggles it for full-width list reading. Enter resumes the original directory and UUID; Esc cancels.

- Action: Run `crg`, filter by directory and select an uncached Guardian review or untitled row. Request Ctrl-G on it and another waiting row; keep the picker open until ready. Repeat using only `Guardian` as the query, then clear it after the title changes.
  Expected: Generic rows show waiting position/time such as `[queued #2 12s]`, then a ticking `[generating 8s]` timer. Manual requests change queue position while retaining waiting time; generation starts a fresh timer. Once ready, the AI headline replaces either placeholder and its timer without reopening. Preview retains Original title, recap state and elapsed phase time. Directory query/UUID stay stable; an old-title-only query re-filters normally. Enter with no matches resumes nothing; meaningful native titles stay unchanged.

### Codex recent picker timezone

- Action: Run `crg` and inspect a session's activity timestamp in its row and preview.
  Expected: Both show the same Toronto time. For source `2026-10-08T16:17:14.030Z`, the row shows `Oct 8 12:17` and the preview shows `2026-10-08 12:17:14.030-04:00 (EDT)`. Winter timestamps use EST (-05:00); Enter resumes the selected session normally.

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
  `prompts/`, reads it back, then immediately starts exactly one new Codex
  conversation to create `result.txt` with exactly `metaprompt-run-ok\n`.
  The returned task identifier differs from the compiler’s; its initial
  instruction reads the saved prompt by absolute path without the old transcript.
  The compiler reports launch and the prompt link; the execution conversation
  reports the verified result. No extra `go` or permission question appears
  solely because compilation finished.
- Action: Run the same runner check with supplied task data large enough that the compiled prompt exceeds 1,000 UTF-8 bytes, then try it in a runtime without `mcp__codex_tui__create_thread`.
  Expected: The full saved prompt preserves the data; the native launch uses a
  file-path handoff of at most 1,000 UTF-8 bytes without truncating task content.
  If the tool is unavailable, execution stays pending and the compiler reports
  the limitation with the saved prompt link. It does not execute locally or fork
  a conversation. An ambiguous creation result is checked before any retry.
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
  Expected: `verify` currently exits 1 for the pre-existing source-pin mismatch
  documented in [the incident](postmortem/2026-10-16-benchmark-source-pins.md).
  Do not repin frozen inputs or start inference to bypass it. `dry-run` exits 0;
  the schedule contains
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
- Action: Only with privately restored frozen selection records, run
  `python3 scripts/metaprompt-selection.py report`, then
  `python3 scripts/metaprompt-selection-analysis.py --run benchmarks/metaprompt-selection/runs/selection-2026-10-03`.
  Expected: recommendation and workflow rates derive from the complete paired
  held-out schedule; all development and failed reservations remain charged.
  Missing usage stays unknown, native completion is distinct from downstream
  correctness, and no skill is installed by reporting. Analysis verifies the
  frozen hashes and request evidence, writes `analysis.json`, and includes
  exploratory paired intervals without making model calls. For the completed
  run, `report` also prints the private compact `summary.json` fields; its
  private `results.json` duplicates per-trial records. These raw artifacts are
  absent from a public checkout and must remain ignored after restoration. For
  `selection-2026-10-03`, confirm 80 held-out rows, 100 total attempts,
  754 requests, no integrity errors, and Sentry selected at 14/16 against
  Wshobson 13/16, Senior 11/16 and both controls 15/16. The equally omitted
  ambiguous-template sensitivity leaves primary scores and costs unchanged;
  raw/minimal are 15/15 and Sentry's weighted success is 85.42%. Native gate
  flags must retain the documented heading-matcher and no-mandatory-gate caveats.
- Action: python3 scripts/metaprompt-benchmark.py verify
  Expected: Currently exits 2 for the pre-existing candidate source-pin
  mismatch documented in [the incident](postmortem/2026-10-16-benchmark-source-pins.md).
  Makes no model calls or installed changes; do not silently repin frozen inputs.
- Action: python3 scripts/metaprompt-benchmark.py dry-run
  Expected: Shows gpt-6.1-sol at medium reasoning, the 50-request cap, fixed pilot
  schedule, and pending cases. Does not use quota or reset an existing ledger.
- Action: With privately restored frozen pilot records, run `python3 scripts/metaprompt-benchmark.py report`.
  Expected: Verifies frozen inputs and rebuilds machine-readable results from
  the frozen schedule and saved attempts without model calls. Changed frozen
  inputs stop reporting. Failures, pending pairs, unknown costs and limited coverage remain visible;
  see [benchmark replay and runtime status](metaprompt-benchmark.md).
- Action: With privately restored frozen pilot records, run `python3 scripts/metaprompt-benchmark-analysis.py`.
  Expected: Derives request-level costs, including aborted episodes, from the
  frozen saved evidence. A public checkout lacks these records; keep restored
  output private and ignored. The 49 measured requests plus one setup attempt
  reconcile to the unchanged 50-request ledger; no model calls are made.
- Action: Finish a change with a user-observable CLI, browser, package, API, or
  rendered-config surface after automated tests pass.
  Expected: Verification still exercises the real user entrypoint, captures
  observed evidence, covers invalid input when relevant, and considers an
  adjacent edge probe when it would add useful runtime evidence instead of
  treating automated tests alone as runtime proof.

## Installed Skill Surface

- Action: After refresh-config, run `chezmoi source-path ~/.agents/skills/last30days/SKILL.md`
  and `chezmoi source-path ~/.agents/skills/find-skills/SKILL.md`.
  Expected: Both resolve into this repo's `dot_agents/skills/` directories.
- Action: Run `python3 ~/.agents/skills/last30days/scripts/last30days.py --help`.
  Expected: Offline usage output appears without starting research or requiring credentials.

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

## Personal context and project knowledge

The skill automatically informs relevant development choices and preserves an
explicit conversational entry point. These checks cover compact retrieval,
source-backed project knowledge, private learning, and installation. Automated
checks use invented temporary data; real notes are never repository fixtures.

- Action: python3 -B -m unittest discover -s tests -p 'test_personal_context*.py' -v
  Expected: Synthetic discovery, source-level example-user Mok commit evidence, HEAD matching, nested Git ownership, summaries, provenance, bounded retrieval, source changes, cache rebuilds, correction/forgetting suppression, concurrency, containment, permissions, absent/corrupt storage, and installed-layout checks pass.
- Action: basedpyright dot_agents/skills/personal-context/scripts/context_store.py
  Expected: The installed basedpyright checker reports zero errors and warnings for the typed JSON/CLI and dynamically loaded knowledge interface; runtime tests remain necessary for storage and privacy behavior.
- Action: python3 -B -m unittest discover -s tests -p 'test_second_brain_skill.py' -v
  Expected: Automatic private retrieval and explicit discussions remain outside session capture, tracked feedback, Second Brain, and Graphiti. Session focus and closeout retain their own confirmation boundaries.
- Action: python3 -B tests/test_personal_context_skill.py
  Expected: Frontmatter and implicit metadata parse, relevant choice triggers and mechanical-work exclusion are documented, supporting references resolve, and a fresh layout links the whole skill. Python 3.12+ and PyYAML are required.
- Action: python3 ~/.agents/skills/personal-context/scripts/context_store.py validate
  Expected: Initialized storage reports safe validation/revision/count metadata only. Missing or invalid authoritative storage produces an actionable error without replacing it or printing private records.
- Action: python3 ~/.agents/skills/personal-context/scripts/context_store.py topics
  Expected: A compact topic index supports selective retrieval. Missing storage reads empty without creating directories.
- Action: python3 ~/.agents/skills/personal-context/scripts/context_store.py projects --query python
  Expected: The searchable catalog defaults to eight records and 6,000 serialized characters, indicates omissions, supplies bounded detail references, and qualifies summaries as contributions supported by example-user Mok authored commits rather than exclusive ownership.
- Action: python3 ~/.agents/skills/personal-context/scripts/context_store.py brief --topic design
  Expected: A bounded relevant brief preserves scope, basis, confirmation status, evidence dates, implications, and IDs. Missing/stale/malformed caches rebuild; unavailable cache writes fall back to direct projections; invalid authoritative records remain preserved.
- Action: python3 ~/.agents/skills/personal-context/scripts/context_store.py foundation --coding-root /home/example/coding --batch-size 8
  Expected: An explicitly authorized read-only foundation pass discovers Git/manifest roots, including nested projects; skips dependencies, generated/cache/VCS internals, personal-context, sensitive payloads, and symlink escapes; indexes only relevant tracked sources whose latest modifying commit author matches example-user Mok exactly, case-insensitive; rejects email inference, untracked files, modified working-tree bytes, and projects without source author evidence; resolves nested manifest Git owners; records author_evidence, committed blob hashes, evidence dates, qualified summaries, gaps, and cross-project findings privately. Historical unavailable/deleted records cannot support current recurring findings. Reports counts and safe coverage metadata. Later relevant refreshes use --project ID and fingerprints.
- Action: In a fresh Codex session, ask for a development architecture or design direction with a plausible personal or cross-project connection, without invoking the skill by name.
  Expected: It uses topics and selected briefs, continues the active task, and asks only about consequential gaps/conflicts. Current project/audience requirements govern; source patterns establish technical observations rather than confirmed personal preferences.
- Action: In another fresh session, request a mechanical file rename with all choices supplied.
  Expected: No unnecessary personal-context lookup or check-in occurs.
- Action: In a fresh Codex session, invoke `$personal-context` without a topic, then supply a real development dilemma.
  Expected: It uses compact relevant context, opens with one useful conversational question, follows answers, and connects learnings to concrete tradeoffs without requiring a ExampleProject goal or implementation task.
- Action: During relevant work or an explicit discussion, state a durable preference, correct it, decline a question, and mark another answer temporary; retrieve the topic later.
  Expected: Meaningful saved updates are briefly reported. Corrections supersede older guidance and invalidate caches; declined questions are not repeated by default; temporary/excluded answers are not persisted; interpretations remain unconfirmed.
- Action: Ask to forget a structured learning or project record, then refresh the relevant foundation and retrieve it again.
  Expected: Matching records, related retaining questions, dependent findings, and cache content are removed; key/ID-only suppression prevents restoration. Original source notes remain unless explicitly included in the forget request. Private learning and retrieval contents never enter raw capture, tracked feedback, the vault, Graphiti, or other services.

## Second Brain

- Action: second-brain sessions review --refresh-limit 0
  Expected: Interactive bat/less viewer with folder, session, time, recap and
  next-step emoji cues. Space/Page Down scrolls, /text searches, q quits with
  success. No inference occurs; privacy/stale warnings remain local and readable.
- Action: Run `second-brain sessions review --limit 1 --refresh-limit 0`, then press `r` inside the pager.
  Expected: The complete selected report reloads, discovering newer sessions and
  generating missing/stale recaps with the normal bounded budget. Slow refresh
  emits elapsed progress; q exits after the new report opens. Positive explicit
  --refresh-limit budgets persist; unchanged recaps are reused without inference.
- Action: second-brain sessions review --refresh-limit 0 --no-pager
  Expected: The same emoji report prints directly, without opening a viewer.
- Action: second-brain sessions review --refresh-limit 0 | cat
  Expected: Clean text through the pipe; no pager subprocess or ANSI sequences.
- Action: NO_COLOR=1 second-brain sessions review --refresh-limit 0
  Expected: Pager navigation and emoji layout remain; bat emits no ANSI colors.
- Action: second-brain sessions review --limit 1
  Expected: Slow discovery/inference emits ongoing elapsed activity to stderr
  every five seconds; then bat/less opens the newest directory's three recaps.
  Fast cached reviews emit no progress noise; no percentage or ETA is invented.
  Missing/stale recaps are generated before the report opens. The pager is a
  snapshot: press r to rediscover sessions, refresh recaps and reopen the report;
  q exits. Unchanged recaps require no new inference.
- Action: second-brain sessions review
  Expected: Five most recently worked-in eligible directories, each with up to
  three newest session recaps. Directory and within-directory order follow
  native activity; completed work is included, Guardian/helpers excluded. Public
  policy/skill reads do not hide recent sessions. Rows show Toronto-local times,
  complete wrapped recap/evidence sections, a current next step, check history
  with dispositions/IDs, aligned session/source/resume data and coverage footer.
- Action: second-brain sessions review --limit 1 --refresh-limit 0 --plain
  Expected: The newest directory with up to three sessions; zero model calls,
  wrapped ASCII text, no ANSI sequences. A missing recap remains “Recap not
  generated” because --refresh-limit 0 disables generation. Rerun without that
  flag to generate it. ASCII output has no pager; the interactive emoji view
  also supports r to enable the normal budget after a zero-preview launch.
  No sudo is required.
- Action: second-brain sessions review --limit 1 --details
  Expected: The same full emoji report as the default for the three selected
  sessions, with evidence, source/resume data, check IDs and coverage footer;
  no raw Markdown headings, truncation or dense semicolon lists.
- Action: second-brain sessions review --limit 1 --refresh-limit 0 --format json
  Expected: Clean existing JSON structure, with flat selected sessions grouped
  by directory and ordered newest first within it.
- Action: second-brain sessions review --all --refresh-limit 0 --details
  Expected: Complete eligible historical inventory; explicit --limit conflicts
  with --all. Formatting never resolves checks or regenerates unchanged recaps.
- Action: second-brain sessions refresh --limit 1 --format json
  Expected: At most one queued changed source, metadata-only output; scheduled
  refresh keeps its independent processing budget.
- Action: python3 -B tests/scripts/second_brain_sessions_review_check.py --pager-check
  Expected: Disposable fixture adds a new source while bat/less is open, presses
  r and verifies discovery plus missing recap generation after zero preview;
  Space scrolling and q exit remain normal,
  plus normal five-directory/three-session, JSON/plain and no-pager contracts.
  Real conversations/private digest are untouched. Requires less, no sudo.
- Action: python3 -B tests/scripts/second_brain_sessions_review_check.py
  Expected: Disposable sources verify five directories with three recaps each,
  independent refresh budgets, details/JSON, helpers, privacy, old checks,
  preserved resolutions and zero-inference repeats. No real private state or
  native conversations are modified; no sudo is required.

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
  tracked target; the normal run is also read-only, and neither result prints config contents.
- Action: On an attached branch with a configured upstream and clean index,
  make one sanitized allowlisted note change strictly smaller than 1,000,000
  bytes, then run `scripts/executable_second-brain checkpoint --dry-run`.
  Expected: Content-free JSON lists only allowlisted candidates, including the
  config target only when its tracked bytes were deliberately edited; no path is staged, committed, or
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

- Action: In a disposable clone, ask Codex to make two small authorized commits and follow the commit-status overview policy.
  Expected: After each commit, Codex promptly reports a high-level overview of completed work, verified results, remaining work, blockers and the next step, links the maintained active plan or `docs/task-status.md`, and includes 5–10 copy-pasteable direct verification commands with the working directory, expected results and sudo requirement. Each commit includes its matching status-document update; earlier milestones remain available. Intermediate reports use commentary and the final response repeats the current overview and commands. Push cadence is unchanged.

- Action: In fresh Codex sessions, complete documentation, configuration, analysis, planning and feature tasks without creating or pushing commits.
  Expected: Every final completion response includes 5–10 relevant copy-pasteable direct verification commands with working directory and sudo requirements. Each command has its own labeled example expected-output block immediately after it; silent success is explicit and variable values are placeholders. Commands exercise or verify the completed result or delivered artifact, without invented behavior, unrelated padding, automated test suites, linters, type checks, builds, Git hygiene checks or source-text searches. Commit and push handoffs retain the same format. Runnable shell commands are standalone raw-text lines at column zero, one physical line each, using valid fish syntax; no fences, inline backticks, list prefixes, blockquotes, prompt markers, continuation backslashes or inserted line breaks. Code for reading, including source, JSON, diffs and illustrative shell code, uses language-tagged fenced blocks with meaningful indentation. Explanations, working directory and sudo requirements stay outside runnable lines; expected output has a separate labeled code block.
- Action: In the live Codex TUI, request the five cases from [the formatting plan](../plans/single-line-codex-commands.md#evaluation-cases): a visibly wrapped bare command, quoted spaces/punctuation, a pipeline, fish substitution and a mixed response with Python/JSON/diff plus expected-output blocks. Select each runnable line, paste into a fresh fish terminal and execute it; inspect the actual clipboard text and visible syntax colors separately. Compare the existing mode with /raw or Alt+R without changing the persisted setting.
  Expected: Each selected command contains the exact one-line command text with no presentation padding, fence markers or inserted hard newlines, and produces its documented output without cleanup. Python, JSON and diff blocks retain indentation and show actual syntax colors; language tags alone are insufficient evidence. Raw command presentation does not require session-wide raw rendering. Record copying, execution and colors independently for each mode. Persist an alternative supported setting only if observed evidence meets both requirements; otherwise record the exact installed-TUI limitation and keep runtime acceptance pending.

- Action: Start a fresh Codex or Claude Code session in this repo and ask it to describe the canonical instruction file and delivery cadence without creating or pushing commits.
  Expected: It identifies `dot_codex/AGENTS.md` as the single policy body, treats the root AGENTS files as routing layers, and explains that a verified single-commit workflow pushes once while multi-commit work waits until the complete verified series; no Git write occurs.
- Action: Review CLI/script/helper output in its default view, then use `--details` and `--plain` when supported or `CLI_PLAIN=1` for legacy helpers; use the safe commands in [the output guide](cli-output.md).
  Expected: Human-facing headings, progress, prompts, successes, warnings and errors have appropriate decorative emojis. Text remains understandable without glyphs; narrow output stays readable. Plain mode removes decoration, `NO_COLOR` suppresses ANSI while keeping emojis, JSON/CSV and protocol/status tokens remain clean, and silent tools remain silent. Raw diagnostics appear under details with actionable accuracy warnings.
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

- Action: Run `python3 scripts/smoke_redshift_keys.py`, then `python3 scripts/smoke_redshift_keys.py ~/.config/i3/config` and `python3 scripts/smoke_redshift_keys.py --live` after refreshing and reloading i3.
  Expected: Each prints PASS for 2–6 = 1800, 2100, 2400, 2700, 3000 K, unchanged keys 1/7–9, and 0/grave reset. No sudo is needed; the live check requires a running i3 session.

- Action: After `refresh-config` and an i3 reload, hold Alt+Super and press the number-row keys `1` through `9`; press Alt+Super+0 or Alt+Super+grave to reset.
  Expected: Redshift selects 1200K, 1800K, 2100K, 2400K, 2700K, 3000K, 4800K, 5400K, and 6000K; 0 and grave restore the default color temperature.
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
- Action: Run `snapshot-codex-config --dry-run` with its normal mapping.
  Expected: Both files are validated without writes; private values stay local.
- Action: Run `fish -ic 'refresh-config'` after reviewing source changes and
  local differences privately.
  Expected: Live Codex/Git files do not enter source; scripts, externals and
  removals are excluded. Conflicts stop without adoption. Shortcuts regenerate,
  elapsed progress appears during slow apply, and REFRESH COMPLETE confirms success.
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
- Action: In a fresh Codex process, paste session-review output whose first recap is an old video repair, and ask the agent to improve the Second Brain review output. Continue into verification, then resume the task in a new process.
  Expected: Before its first substantive progress update, the saved conversation name and Kitty title describe the Second Brain review, not the quoted video repair. Later progress updates and resume keep the title aligned with the actual task/phase; another conversation's name stays unchanged. This checks agent instruction compliance as well as title transport.
- Action: Narrow a split, switch between split and tabbed layouts, and toggle fullscreen on and off.
  Expected: Titles stay within their available width without overlapping neighboring windows. Fullscreen hides the titlebar; leaving fullscreen restores it. No extra header appears inside the terminal transcript.
- Action: Observe an agent while working, awaiting input, and after verified completion; then resume that conversation.
  Expected: Codex's native activity/attention indicator remains available. The summary reflects the current phase or verified result, and its saved conversation name persists across resume.
- Action: In a Codex environment without the native title tool, use /rename to set a short task name.
  Expected: The existing native name remains until manually renamed. The titlebar displays the manual name without introducing a polling service or another model request.
- Action: Repeat the existing Kitty scrolling checks below in a titled window.
  Expected: The scrollbar, paging, selection and inline Codex history still behave as documented.

### Desktop notification font comparison

Check large text throughout popups about 669px wide with naturally growing height, or add `--compare` for old/new references. Run refresh-config and `~/scripts/codex-notification-activate` first. The font is 23.25 points, 1.5 times the preceding 15.5-point size; desktop DPI scales actual pixels. No sudo.

- Action: Run `~/scripts/notification-font-test`.
  Expected: Codex and Discord samples have large titles and body text throughout, wrap without clipping at about 669px rendered width and last 15 seconds. Height follows the text up to 600 logical pixels; long messages are not forced into 16:9. Samples avoid the codex-kitty audio rule.
- Action: Send one sample with `~/scripts/notification-font-test --app codex`, then run `xwininfo -name Dunst` while visible.
  Expected: Actual rendered width is about 669px including the frame on the current 135-DPI desktop; height grows with wrapped text. Check runtime dimensions rather than only deployed config.
- Action: Run `~/scripts/notification-font-test --compare --app codex`.
  Expected: One Codex sample shows the same sentence at 15.5 pt and 23.25 pt. The smaller line is deliberately the old-size reference.
- Action: Run `~/scripts/notification-font-test --app discord --plain`.
  Expected: Only the Discord sample appears, with large chat text throughout; terminal output is ASCII.

### Terminal notification Markdown bold

Apply with refresh-config, then activate the callback in existing Kitty instances without restarting terminals or resetting notification state. Check bold, literal/code and unchanged plain text through native Kitty delivery; no sudo. Only Markdown strong emphasis is supported.

- Action: Run `~/scripts/notification-markdown-test --activate-all`.
  Expected: Prints an acknowledged activation count and shows a native popup whose title/body render bold emphasis without surrounding double asterisks. Literal HTML is escaped. Existing terminals and native click/focus behavior remain usable.
- Action: Run `~/scripts/notification-markdown-test --case literal --plain`.
  Expected: Bold renders; literal `<span>` and `&` display as text, while double asterisks inside code/escaped markers stay literal. Terminal output is ASCII.
- Action: Run `~/scripts/notification-markdown-test --case plain --plain`.
  Expected: Plain sample text arrives unchanged through Kitty. Popup width/font match the current Dunst settings.
- Action: Click a native sample, then request a real unfocused Codex completion with `**bold**` in its answer.
  Expected: Sample click focuses its originating Kitty window; the Codex popup formats emphasis while existing focus suppression, notification IDs and sound provenance remain native.
- Action: If activation fails, run `~/scripts/notification-markdown-test --details` after opening Kitty.
  Expected: Concise error by default; requested details expose the remote activation failure. New Kitty instances load the callback automatically.

### Codex notification sound

Apply the [notification sources](codex-notification-sound.md), restart Dunst
(which clears its history/queue), and start a fresh Kitty process. No sudo is
needed. Activation is a one-time installation/update step; afterward open Kitty
normally. Changing the clip needs only `set`. The popup checks below assume `speech disable`; optional speech is checked afterward. Live audio acceptance requires
an existing local short MP3; this checkout does not bundle audio assets.

- Action: `~/scripts/codex-notification-activate --open-kitty`
  Expected: Your notification-bus Dunst restarts and a fresh Kitty process opens;
  existing terminals remain open. Its history/queue clears; the sound setting is
  unchanged (disabled on a fresh installation).
- Action: `~/scripts/codex-notification-sound status`
  Expected: A fresh installation reports aligned sound/speech state and voice readiness.
  `status --plain --details` uses ASCII and reveals machine-local JSON/error-log paths. No clip or local sound-path
  setting is bundled. An already configured machine reports its selected path.
- Action: `~/scripts/codex-notification-sound set "$HOME/scripts/can-i-ask-you-a-question.mp3"` if that installed clip exists; otherwise select another existing local MP3.
  Expected: With an existing clip at that path, sound is enabled through local
  mode-0600 JSON. The MP3 stays intact; `set` only stores its path.
  Selecting another filename with spaces preserves the entire path.
- Action: If visible popups have neither clip nor speech, run `~/scripts/codex-notification-sound status --details`, correct a missing clip path with `set`, then run `~/scripts/codex-notification-sound preview --title "Notification audio check" --details`.
  Expected: A stale path reports an error before either audio stage. After selecting an existing clip, status reports it enabled and preserves the existing speech setting. With the voice ready, preview plays the clip then the sentence and exits 0 without a daemon restart. Historical error-log entries retain their old timestamps.
- Action: `~/scripts/codex-notification-sound preview`
  Expected: One clip plays without a popup; exit 0 on success. Invalid/missing
  files or unavailable mpv report errors and exit 1 without affecting popups.
- Action: `~/scripts/codex-notification-sound smoke tagged`
  Expected: One synthetic Dunst popup and one playback. This checks the Dunst
  rule/player; it does not establish real Codex origin detection.
- Action: `~/scripts/codex-notification-sound smoke kitty`
  Expected: An ordinary Kitty popup with Codex-looking text and no sound.
- Action: In a fresh local Kitty/Codex session with notifications enabled,
  submit a normal task and focus another app before the turn completes.
  Expected: One completion popup and one playback. Clicking its existing
  action focuses the originating Codex terminal, even if another Kitty
  terminal was active. Content and expiry remain unchanged.
- Action: In that session, exercise an ordinary task that requires approval,
  then focus another app while Codex awaits the approval.
  Expected: One approval popup and one playback; approval still works normally.
- Action: Complete another task while keeping its Codex terminal focused.
  Expected: Existing focus suppression is unchanged. When no popup is emitted,
  there is no audio. Do not use synthetic OSC 9 emission for this check.
- Action: `~/scripts/codex-notification-sound disable`
  Expected: Local setting is removed, MP3 stays intact, and subsequent popups
  remain visible and silent. Invalid sound config never breaks popup delivery.

The automated private-daemon check also covers queued display, duplicate
stacking, suppression and history. Dunst 1.9.2 may sound once on recall of a
silently stacked duplicate; normal already-sounded history stays silent.

- Action: Run `~/scripts/setup-codex-notification-speech --install`, then `--check` and `~/scripts/codex-notification-sound preview --title "Smoke-test VPS backup"`.
  Expected: Pinned Piper 1.8.0 and English Voice Contributor high voice at pace 0.95 verify without sudo; preview plays exactly one MP3 followed by that title. Repeating check/preview without internet succeeds, and temporary WAVs disappear.
- Action: After deployment, start/resume affected conversations, then run `~/scripts/codex-notification-sound speech enable`.
  Expected: Status shows enabled and ready. No hook trust is required. A tagged Dunst smoke popup is silent; existing popup actions and content remain unchanged.
- Action: Use two named conversations sharing a terminal. Complete focused/background turns, rename one and complete again, then request permission including an automatically reviewed request while the task continues. Also complete an ordinary spawned agent with its own saved title.
  Expected: Each user-facing completed answer with nonblank final text plays exactly one MP3 then its exact current saved title, never the visible or parent conversation's title. Ordinary spawned agents (including inherited completion on spawn), internal reviewers and permission requests/reviews during work stay silent. Focused completion sounds without forcing a popup. Unknown/mismatched identity or ambiguous provenance and empty/missing answers stay silent; only a verified user-facing answer with a missing title falls back to MP3 only.
- Action: From `~/linux-config`, run `python3 -B scripts/smoke_codex_notification_events.py --installed --plain`; use `--case worker`, `empty`, `missing`, `unknown`, `ambiguous`, `parent` or `permission` to repeat one scenario.
  Expected: No hardware audio or setting changes. The deployed bridge runs against isolated event metadata and a silent fake player; completion reports `PASS completion: 1 playback(s)` and each false trigger reports zero. Each case shows progress; mismatches exit 1.
- Action: Trigger simultaneous completions and preview a Unicode title with quoted shell-sensitive text. Temporarily make the Piper environment unavailable and repeat, then restore it.
  Expected: Complete audio sequences never overlap; text is spoken literally. Unavailable synthesis retains one MP3, logs the failure and does not delay Codex or change permission decisions.
- Action: After deployment, start/resume Codex and inspect `/hooks` for enabled/trusted blocking and async question entries running `python3 /home/example/scripts/codex-notification-event`; let a real task queue a nonblocking follow-up question.
  Expected: The TUI shows a queued question, the selected question MP3 plays once, then Voice Contributor speaks one concise sentence about the question itself. Choices and the task title are omitted. Work continues and answering through Shift+Left still works.
- Action: Queue two questions together, then exercise a blocking question in Plan mode.
  Expected: Each request plays one MP3 then one sentence; multiple prompts share that sentence, and a blocking question announces before you answer. Rejected async requests, helpers and permission reviews do not announce.
- Action: From `~/linux-config`, run `python3 -B scripts/smoke_codex_question_events.py --installed --case question --plain`; repeat with `multi-question`, `question-blocking`, `question-worker`, `question-empty` and `question-secret`.
  Expected: Valid cases report two silent fixture-player calls (clip then exact spoken sentence); worker, empty and secret cases report zero. No real audio, settings changes, sudo or voice downloads.
- Action: Run `~/scripts/codex-notification-sound speech disable`, then repeat a displayed completion/approval and a focused completion.
  Expected: Displayed popups regain their original single MP3. Focus suppression again suppresses audio, and the selected MP3 remains configured.

### Local Codex voice auditions

Compare the ten numbered local voices, then replay favorites with new wording before selecting one. Install Piper with the existing speech setup helper first. No sudo; first model downloads require internet. Voice auditions do not change speech activation or the selected notification voice.

- Action: `mpv --no-config --no-video ~/scripts/Voice Contributor-celebrate.mp3`.
  Expected: The committed Voice Contributor high reference sample reads the celebrate line at pace 0.95, without the separately retained question intro.
- Action: `~/scripts/codex-voice-auditions --list`, then `--samples`.
  Expected: Stable numbers 1–10 (Amy through Jenny Dioco), region/model IDs, and three shared sample sets; no download or audio.
- Action: `~/scripts/codex-voice-auditions`.
  Expected: All ten run in numbered order with visible names, the question clip then speech per voice, a remaining-gap reading and saved WAVs/manifest. Synthesis overlaps the clip, audio never overlaps within a sequence, and downloads/slow generation report ongoing elapsed activity.
- Action: `~/scripts/codex-voice-auditions --voice 1 6 --sample celebrate --offline`.
  Expected: Cached Amy and Voice Contributor play with identical upbeat wording and their original numbers, no network downloads. If either model is missing, an actionable offline warning appears before playback.
- Action: `~/scripts/codex-voice-auditions --voice 6 --text "All done! The tests passed, and your changes are ready."`.
  Expected: Voice Contributor alone reads the literal custom line after the question clip; number 6 and name appear immediately before speech. Compare naturalness and energy by listening.
- Action: `~/scripts/codex-voice-auditions --voice 1 --sample celebrate --length-scale 0.9 --offline`.
  Expected: Amy uses a brisker pace, with the question clip and measured remaining gap; notification settings retain their prior values.
- Action: `~/scripts/codex-voice-auditions --voice 1 --render-only --output-dir /tmp/codex-voice-check --offline`.
  Expected: One nonempty WAV plus manifest.json; no audio. Manifest records voice number/name, wording and pace; clip-gap field is null for rendering.
- Action: `~/scripts/codex-notification-sound preview --title "All done! The tests passed."`.
  Expected: Selected Voice Contributor high voice at the celebrate pace (0.95) is synthesized during the MP3; one MP3 then one title with reduced remaining wait. Simultaneous notifications remain serialized; failure retains the existing MP3 fallback. Approval speech remains silent.

### Short Voice Contributor introduction

After refresh-config, try the stored introduction and custom text in your existing fish shell; no abbreviation reload is required. No sudo; the default saved MP3 needs mpv, while custom words also need installed Piper.

- Action: Type `rintro` and press Enter in interactive fish.
  Expected: Immediately plays the exact saved example-user introduction in Voice Contributor's voice, without the question clip.
- Action: `fish -c 'rintro --help'`.
  Expected: Usage with --text, exit 0, no audio; command resolves without abbreviations.
- Action: `rintro --text "Welcome back! Your changes are ready."`.
  Expected: Voice Contributor reads those custom words only, with no question clip; notification settings remain unchanged.
- Action: `~/scripts/Voice Contributor-intro --help`, then `~/scripts/Voice Contributor-intro --text`.
  Expected: Help shows default text and --text usage without audio; missing words exit 2 with usage.
- Action: `~/scripts/codex-notification-sound preview --speech-only --title "Only Voice Contributor speech." --plain`.
  Expected: Speech only, even without a configured question clip. Blank titles are rejected before children; missing/failed voice returns nonzero with an actionable warning.
- Action: `mpv --no-config --no-video ~/scripts/Voice Contributor-intro.mp3`.
  Expected: The same literal default introduction; no synthesis delay or question clip.

### tmux pane history scrolling

Scroll, select and copy with familiar gestures. Shift+wheel works without
holding a mouse button. Drag a selection once, release the button, then copy
with Ctrl+Shift+C; the highlight and viewport remain in place. Escape returns
to live input. The history-mode status line shows the copy and exit shortcuts.
Use the disposable helper below after refresh-config; no sudo is needed.

- Action: Run /home/example/scripts/tmux-scrollback-smoke, then hold Shift and wheel up over the text with no mouse button held.
  Expected: Earlier numbered HISTORY lines appear. Plain wheel also browses history at a shell, and Alt+wheel remains available. New panes retain up to 50,000 rows; record 000001 is reachable in the 3,000-record fixture. Existing panes retain their old limit and discarded output cannot be recovered.
- Action: While viewing history, drag across part of a numbered line, release the mouse button, move the pointer away, then press Ctrl+Shift+C. Press it a second time and paste into another app.
  Expected: The blue highlight persists after release. The clipboard contains exactly the selected text; repeated copying keeps the same text and viewport. The status line shows Copied to confirm the action. No mouse button needs to be held while pressing the shortcut. A copy request without a selection shows a selection hint instead of clearing the clipboard.
- Action: Press Escape, type hello and Enter, then press Ctrl+D at empty live input to close the fixture.
  Expected: Escape returns to the live tail in one step and INPUT hello confirms normal typing. Wheel-down alone also exits wheel-entered copy mode if you have not started a selection; after selecting, use Escape. Only the disposable fixture closes.
- Action: Run /home/example/scripts/tmux-scrollback-smoke --app-mouse. Try plain wheel/click, then Shift+wheel up, drag/release and Ctrl+Shift+C.
  Expected: Ordinary application gestures produce APP_MOUSE records. Shift+wheel explicitly opens tmux history despite app mouse ownership; the same released-selection copy flow works. Escape returns to the application. Alt+wheel remains an alternative. tmux history is separate from an application's private document history.
- Action: In a fresh raw Kitty shell without tmux, select text normally and copy with Ctrl+Shift+C. In tmux, hold Shift while dragging to deliberately select the visible Kitty screen, then copy with Ctrl+Shift+C.
  Expected: Native Kitty selection copying remains available. Ctrl+Shift+C chooses the native Kitty selection when one exists, otherwise the highlighted tmux selection. tmux launched from an ordinary fish shell supports the same shortcut.
- Action: Separately try dragging the right edge of the tmux fixture.
  Expected: Installed tmux 3.4 has no draggable pane history scrollbar (native support first appears in 3.6); edge dragging selects text rather than giving raw Kitty thumb parity. The scroll/copy flow above uses pane-owned history.

### Kitty and Codex scrolling

Use a fresh Kitty window after refresh-config: a larger history cannot recover
lines an older window already discarded. This checks one scrollbar per Kitty
terminal window. Inside tmux, use wheel/Alt+wheel or Alt+C copy mode for pane-owned history; see the tmux checks above.
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

## Fish Alias Skill

Check the shortcut skill using disposable fixture sources before making a live
request. The fixture suite does not execute mapped commands or install the cbn
example. Live requests preserve active conflicts with exactly `# ` and refresh
changed mappings; file source keys gain `n` in fish.

- Action: Run `fish --no-config -c 'source ~/.config/fish/key_abbr.fish; abbr --show | string match -r "^abbr -a -- (?:v|kav|kad) .*"'` after refresh-config.
  Expected: `v` expands to `vesktop`, `kav` to `killall vesktop`, and `kad`
  to `killall discord`. Inspection launches no apps and kills no processes;
  the previous `v ./start.sh voice` mapping remains commented in the source.
- Action: python3 -B tests/test_fish_alias.py
  Expected: Command `cbn codex-time burn day` lands in the work section; directory
  and file paths, including spaces/quotes, route correctly. Active cross-source
  conflicts use effective fish names (`bn` file becomes `nbn`), inactive branches
  and unrelated bytes remain intact, identical requests are no-ops, missing or
  ambiguous inputs fail before edits, and generated fish syntax passes. Absolute
  executables with arguments remain commands; stored backticks retain their exact
  text. Pasted `/home/example` directory prefixes become `~`, including quoted
  or escaped spaces; repeated absolute requests are no-ops. Similar usernames,
  embedded home strings, commands and file mappings remain unchanged. Template
  delimiters in new requests are rejected before rendering.
- Action: python3 /home/example/.agents/skills/fish-alias/scripts/fish_alias.py --help
  Expected: Installed helper describes JSON-stdin input, `--repo` and preview
  default; `--apply` is required to write. Readable output is the default;
  `--plain` selects ASCII, `--details` exposes diffs/error evidence, and
  `--json` exports structured results. No mapped command executes.
- Action: python3 -c 'import json,subprocess; r=subprocess.run(["python3","/home/example/.agents/skills/fish-alias/scripts/fish_alias.py","--json"],input=json.dumps({"input":"cbn codex-time burn day"}),text=True); raise SystemExit(r.returncode)'
  Expected: JSON preview reports command routing and work section, showing
  `cbn "codex-time burn day"` and any active conflicts without changing sources.
  If the mapping is already installed, reports a no-op instead.
- Action: fish -n ~/.config/fish/key_abbr.fish
  Expected: Exit 0 after refresh; syntax only, no supplied commands execute.

- Action: From `/home/example/linux-config`, run `rg -n '^cto ' aliases/key_aliases.tmpl` and `fish --no-config -c 'source ~/.config/fish/key_abbr.fish; abbr --show' | rg '^abbr .* -- cto '`.
  Expected: The work template maps `cto` to `codex-time overview`, and the live
  fish definition has the same expansion. These checks do not execute the command.

- Action: From `/home/example/linux-config`, run `rg -n '^ctp ' aliases/key_aliases.tmpl` and `fish --no-config -c 'source ~/.config/fish/key_abbr.fish; abbr --show' | rg '^abbr .* -- ctp '`.
  Expected: The work template and installed fish abbreviation map `ctp` to
  `codex-time projects`; inspection does not execute the mapped command.

- Action: From `/home/example/linux-config`, run `rg -n '^tcs ' aliases/key_dirs.tmpl` and `fish --no-config -c 'source ~/.config/fish/key_abbr.fish; abbr --show' | rg '^abbr .* -- tcs '`.
  Expected: Source has `tcs ~/coding/track-codex-sessions` in cdn; installed fish
  expands tcs to `cd ~/coding/track-codex-sessions`. Inspect only; no cd executes.

- Action: In a fresh fish session, inspect `abbr --show | string match -- "abbr -a -- tbo *"` without running the expansion.
  Expected: `abbr -a -- tbo 'cd /mnt/usb-8tb/obs'`; the shortcut remains registered after refresh.

Live Codex usage: `$fish-alias cbn codex-time burn day`. To create the mapping,
invoke this as an actual request, inspect the reported source/section/conflicts,
then verify the refresh result. Repeating it must produce a no-op. Directory
example: `$fish-alias pj ~/coding/my-project/`. File example:
`$fish-alias re README.md` produces `nre` under existing generator conventions.


## Full-system Backup And Guarded Recovery

Run these checks from `/home/example/linux-config`. The automated and help checks
need no sudo and use disposable fixtures; they do not erase or mount host disks.
Actual source preflight, backup, resync and access repair require sudo. Follow
[the recovery guide](backup-pc-recovery.md) for supported mounts and the
separate disposable-VM boot acceptance check.

- Action: `python3 -B -m unittest discover -s tests -p 'test_backup_pc*.py'`
  Expected: All backup, progress and VM fixtures pass. Corrupt bundles, unsafe
  disks, changed identities and declined erase confirmation cause no disk writes.
  Live vanished files are accepted while permission/I/O errors remain fatal;
  generated artifacts are readable by the invoking sudo user without changing
  copied home metadata. Resource budgets and incomplete home resync are covered.
- Action: `python3 -B tests/test_backup_pc_vm.py`
  Expected: Disposable initialization stages the entrypoint and both helper
  files together. Dry-run creates nothing, device/symlink inputs are rejected,
  and the boot phase disconnects source, backup and live ISO. These assertions
  do not establish guest bootability or Secure Boot support.
- Action: `bash -n scripts/executable_backup-pc`
  Expected: Exit 0; the standalone Bash entrypoint parses without execution.
- Action: `./scripts/executable_backup-pc backup --help`
  Expected: Explicit `--live`, integer `--resource-percent` (default 75) and
  `--dry-run` are shown; no files change.
- Action: `./scripts/executable_backup-pc sync-home --help`
  Expected: Required bundle/source arguments and optional live/dry-run flags
  appear. Home-only sync preserves the existing system archive and does not
  publish an incomplete bundle as a complete recovery backup.
- Action: `./scripts/executable_backup-pc access --help`
  Expected: Scoped generated-artifact access repair accepts `--bundle` and
  optional `--user`; copied home ownership remains untouched.
- Action: `./scripts/executable_backup-pc excludes`
  Expected: Built-in exclusions print without sudo. Cache/runtime data are
  omitted while persistent application state remains eligible for backup.
- Action: `./scripts/backup-pc-vm-check --help`
  Expected: Init, backup, restore and boot phases are listed. For runtime
  acceptance, execute the guide’s workflow using only disposable virtual images,
  then record login/data/UUID results with the source and backup disconnected.


## Example Client graphical VPS recovery

Run from the PC using the [project runbook](/home/example/coding/example-client-app/docs/graphical-vps-restore.md). This is independent of backup-pc and does not modify the production VPS.

- Action: Run `bash /home/example/coding/example-client-app/scripts/infra/graphical-vps.sh check`, then the documented sudo setup stage only for new USB rehearsal paths.
  Expected: Actionable prerequisite output, full original-image verification, new isolated VM disks/media and retained original backups. Open virt-manager through the normal-user open-proof stage.
- Action: Complete the marked guest's proof stage and the offline GNOME exchanges, using the documented PC/guest stages.
  Expected: Original UUID/files/configured database/local-service checks and a current-session complete report gate the separate desktop clone; signed same-release packages install without guest Internet. Record actual GNOME login/reboot screenshots.
- Action: Run the project status and finish stages after acceptance.
  Expected: Exact owned domain UUIDs/network none, normal shutdown and BACKING IMAGE UNCHANGED. Public TLS/external bots/production upgrades remain separate evidence.

## Sanitized repository migration

These checks inspect the replacement checkout and private recovery journal. Use the default state directory, or pass the same `--state-dir` used at cutover. No sudo is required. Run from `~/linux-config`.

### Preview and repeat execution

**Action:** Run `python3 scripts/executable_migrate-ai-cli-workflow --dry-run` after migration.

**Expected:** Verification succeeds and reports already migrated; no files change. Before migration the preview inventories paths and worktrees, validates local identity data, and performs no clone or cutover.

### Verify recovery and configuration

**Action:** Run `python3 scripts/executable_migrate-ai-cli-workflow --verify`, then inspect the private journal's accepted/quarantined path lists. Run a fresh fish shell's `refresh-config` and verify once more.

**Expected:** Origin/main/upstream identify the sanitized repository, chezmoi uses the active checkout, reviewed bytes and archived worktree content remain intact, and private Git/Codex settings are unchanged. Refresh applies reviewed files, shows elapsed progress, excludes scripts/externals/removals, and never copies live settings or adopts conflicts.

### Audit pending and historical content

**Action:** Run `./scripts/executable_audit-public-history --scope all`. The migration verifier independently scans pending file bytes using the sanitized auditor.

**Expected:** No historical or pending findings. This is a bounded scanner result, not proof that no possible secret exists.

### Recovery rehearsal

**Action:** Use disposable repositories and temporary HOME to run the migration integration tests before a live cutover. In a recovery situation, run the migration helper's `--rollback` with its recorded state directory.

**Expected:** Dirty nested/external worktrees survive; clone/render/apply failures preserve or restore the old checkout; interrupted recovery succeeds only when current state matches recorded before/intended states. Subsequent user edits cause refusal and remain untouched. The sanitized candidate remains privately recoverable after rollback.

### Rejected-transfer retry

**Action:** After a content-rejected attempt reports rollback, inspect only path/category diagnostics using `--details`, fix the reviewed source, and regenerate its source/destination hashes. Keep the old recovery directory and use a new `--state-dir` for retry, verification, and rollback.

**Expected:** Real credentials remain rejected; synthetic fixture source passes the same transfer guard used by apply. Logs name rejected paths without exposing values. The previous journal/candidate remain intact, and the new attempt never reuses a rolled-back state directory.

### Concurrent-change refusal

**Action:** Stop other sessions using the active checkout, then preview with `--dry-run --details` and an unused `--state-dir`. Keep every prior failed directory. Review category/count diagnostics if the preview or apply refuses.

**Expected:** Index stat-cache refresh alone does not trigger refusal. Changed HEAD, staged blobs/modes/flags, resolve-undo, working files or ignored entries remain protected. New failed-attempt journals keep the initial and differing fingerprints privately. No cutover or live writes occur after a preparation refusal. A successful preview cannot guarantee writers remain idle afterward.

### Migration preserves local integrations

Action: Run the reviewed migration, then verify existing Claude client settings, MCP declarations and the local Second Brain project contract.

Expected: Existing local integration files and project contracts retain their working bytes; public neutral defaults are retained only in source. Scripts, externals and removals remain excluded.

## Portable home storage offload

**Action:** Preview `scripts/executable_home-storage-offload --destination /mnt/storage` using your actual mounted destination. Inspect the estimate before adding `--apply`.

**Expected:** Preview changes no files. Apply checks mount identity, space and content verification, preserves original folders for recovery during moves, then cleans only the documented caches. No private mount path is assumed or stored in source.

## Notification source outlines

Use disposable data for helper checks; no sudo is required. Live previews can
play audio, so exercise them deliberately.

- Action: Run the configured notification preview from its source Kitty terminal or tmux pane, then exercise a real completion/question event.
  Expected: A verified source has an outline only during player playback; focus stays unchanged. Closing or unavailable outline support does not suppress audio.

- Action: Run `dot_config/i3blocks/scripts/executable_dnd` with no click event.
  Expected: Status markup shows DND/queue state or notif without changing pause.
  The helper is available but is not added to an i3blocks configuration here.

## Neovim clipboard startup

Use disposable data for helper checks; no sudo is required. Live previews can
play audio, so exercise them deliberately.

- Action: Start Neovim normally on X11 with xclip installed and no explicit clipboard provider; repeat with an explicit provider or Wayland session.
  Expected: Neovim 0.11.1 or newer selects xclip without a synchronous xsel clipboard read; explicit and Wayland providers keep their normal selection.

## Public benchmark evidence boundary

**Action:** In a disposable repository using this checkout's `.gitignore`, create a raw JSON file under each benchmark `runs/` root and an aggregate report outside those roots; run normal `git add .`.

**Expected:** Both raw files remain ignored; the aggregate report is eligible for staging. Actual run directories, request/response traces and raw ledgers remain private.

**Action:** In a disposable Git repository, commit JSON containing an installation or session UUID, including nested serialized JSON, then remove it and run `executable_audit-public-history --repo <fixture> --scope all --plain`.

**Expected:** The auditor reports `runtime_identifier` without printing values and exits 1. Removing the latest file alone does not clear its historical finding. Use synthetic fixture values only.
