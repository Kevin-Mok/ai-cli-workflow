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

## Local Pre-commit Privacy Gate

Use disposable repositories for all negative candidates; never stage a secret
or make a test commit in this checkout. Installation alone creates no commit.

- Action: `python3 scripts/executable_privacy-gate install`, then repeat it.
  Expected: Both runs exit 0, preserve a prior hook and its permissions, and keep
  core.hooksPath unchanged. The scanner snapshot is refreshed on reinstall.
- Action: `python3 scripts/executable_privacy-gate status --plain`.
  Expected: Exit 0 and `Privacy gate active (scanner current).` without private
  filenames or values. Linked worktrees see the shared installation.
- Action: `python3 scripts/executable_privacy-gate check --plain --details`.
  Expected: The complete current index and effective author/committer identities
  are inspected locally. Safe candidates exit 0; findings exit 1 with safe
  categories/hashed path references; incomplete inspection exits 2. Existing
  pending/private identity findings must be repaired locally before committing.
- Action: `python3 tests/test_pre_commit_privacy_gate.py` and
  `python3 -m unittest discover -s tests -p test_checkpoint_privacy_gate.py`.
  Expected: Disposable actual Git commits prove safe commits/repairs, token/key/
  runtime/private-path refusal, index divergence, unusual paths, linked worktrees,
  local LFS verification, missing scanner/rules/object and conflict refusals,
  unchanged HEAD/index on refusal, and exact-tree plumbing integration. All
  synthetic values and secret-bearing filenames remain absent from captured output.
- Action: In a disposable installation run
  `python3 scripts/executable_privacy-gate uninstall`.
  Expected: Only the owned hook/bundle is removed, any previous hook is restored,
  and core.hooksPath remains unchanged. A changed active hook refuses removal.

### Resolving privacy-gate findings

- Action: After updating the scanner or reviewed-content policy, repeat
  `python3 scripts/executable_privacy-gate install`, then run `status --plain`
  and `check --plain`.
  Expected: The scanner snapshot is current. Existing reviewed source references,
  synthetic fixtures and public recovery runbooks pass only while their exact
  path/content/category approvals match. An edited approved blob requires review;
  adding a real-looking token is still refused. A missing/malformed approval
  manifest refuses inspection rather than silently disabling the gate.
- Action: For an approved public Git identity, keep the exact name/email pair only
  in a mode-0600 rules file outside the checkout and configure local
  `privacyGate.rules`. Run `check --plain` again.
  Expected: Only the approved metadata identity is permitted. Git user.name/email
  remain unchanged; the same email in arbitrary file content remains detectable.
  Never publish the private rules file or approve an identity without the user.

## Fish login startup

- Action: Open a new login terminal in the desktop session with `XDG_VTNR`
  unset (for example, `env -u XDG_VTNR fish --login`). Exit the child shell
  after checking its prompt.
  Expected: The normal prompt appears without `test: Missing argument` and no
  second graphical session starts.
- Action: Run `env -u DISPLAY -u XDG_VTNR fish --login -c 'echo startup-ok'`,
  then `env DISPLAY=:1 XDG_VTNR=1 fish --login -c 'echo startup-ok'`.
  Expected: Both reach `startup-ok` without the missing-argument diagnostic;
  a missing VT or an active display prevents automatic X startup.
- Action: On the real local virtual console 1 with no active display, log in
  normally when a graphical session is desired.
  Expected: The existing `startx -- -keeptty` path still launches X. Do not run
  this physical-console check inside an existing graphical session.

## Refresh conflict recovery

- Action: When refresh reports a changed target, open its private log and inspect
  `chezmoi diff` for that exact path before reconciling it. For the screensaver
  launcher, compare both contents and modes; after reviewing the change, use
  an exact-target apply, then rerun `refresh-config` normally.
  Expected: Reviewed mode-only drift is resolved without changing content;
  `chezmoi verify` for that target exits0, refresh reaches `REFRESH COMPLETE`,
  and unrelated conflicts retain overwrite protection. The `scripts` exclusion
  covers chezmoi run hooks, not ordinary files inside `~/scripts/`.
- Action: Run the installed `media-screensaver status --plain` after recovery.
  Expected: Status exits0 and reports monitor order and idle-monitor state.
  Missing browser-bridge suppression is reported honestly; no preview starts.

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
- Action: Run `python3 dot_agents/skills/ui-ux-pro-max/scripts/search.py "education dashboard" --design-system -p "LessonOps" -f markdown` from the source checkout.
  Expected: A candidate design system prints without credentials, network access or persisted files.
- Action: Run `python3 dot_agents/skills/ui-ux-pro-max/scripts/search.py "keyboard focus" --stack react`.
  Expected: React stack guidance prints; inspect the version/status applicability before using it.
- Action: Run `python3 dot_agents/skills/ui-ux-pro-max/scripts/search.py "zxqvnevermatch987654321" --domain ux`.
  Expected: Zero matches are disclosed explicitly, with no fabricated recommendation.
- Action: After normal shared-skill deployment, invoke `$ui-ux-pro-max` in Codex and `/ui-ux-pro-max` in Claude Code, then start a generic design request without either invocation.
  Expected: Explicit requests load the shared skill and supporting files; a generic request does not automatically load this skill. Deployment is required; not performed during evaluation.
- Action: sync-design-skills --dry-run
  Expected: Chezmoi previews only the five managed public-source refreshes and
  does not run the UI/UX Pro Max updater, authenticate any service, generate
  media, or spend credits.
- Action: setup-design-skills-timer --check
  Expected: The tracked helper and daily `Persistent=true` units validate
  without sudo; after `--enable`, `systemctl --user list-timers
  design-skills-sync.timer --no-pager` shows the next refresh.
- Action: Open the Codex skill picker and select `Commit 2 Plan & Push`.
  Expected: It invokes the stable `$commit-plan-push` skill with its managed
  title and `agents/openai.yaml` metadata. On a mixed dirty tree, it makes a
  best-effort pass over every safe, reviewable change, records validation
  warnings, leaves unsafe files as named residuals, and still attempts the
  configured push. In a fresh Codex session, type `$comm`: the first four
  matching skill titles are `Commit 1 Session`, `Commit 2 Plan & Push`,
  `Commit 3 Dirty`, and `Commit 4 Plan`, in that order. Numbers control the
  alphabetical tie-break; no unsupported priority field is relied on.
  Type `$commit-session` separately and confirm the original slug still resolves.
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
  Expected: After each commit, Codex promptly reports a high-level overview of completed work, verified results, remaining work, blockers and the next step, links the maintained active plan or `docs/task-status.md`, and starts with exactly 3 visible copy-pasteable direct verification commands with the working directory, expected results and sudo requirement. Each commit includes its matching status-document update; earlier milestones remain available. Intermediate reports use commentary and the final response repeats the current overview and commands. Push cadence is unchanged.

- Action: In fresh Codex sessions, complete documentation, configuration, analysis, planning and feature tasks without creating or pushing commits.
  Expected: Every final completion response starts with exactly 3 relevant visible copy-pasteable direct verification commands with working directory and sudo requirements. Each command has its own labeled example expected-output block immediately after it; silent success is explicit and variable values are placeholders. Commands exercise or verify the completed result or delivered artifact, without invented behavior, unrelated padding, automated test suites, linters, type checks, builds, Git hygiene checks or source-text searches. After the command/expected-output pairs, the summary order is **Verified → Use → Implemented**; commands stay in execution order outside collapsed details. Commit and push handoffs retain the same format. Runnable shell commands are standalone raw-text lines at column zero, one physical line each, using valid fish syntax; no fences, inline backticks, list prefixes, blockquotes, prompt markers, continuation backslashes or inserted line breaks. Code for reading, including source, JSON, diffs and illustrative shell code, uses language-tagged fenced blocks with meaningful indentation. Explanations, working directory and sudo requirements stay outside runnable lines; expected output has a separate labeled code block.
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

- Action: Select Super+3 (2850 K), then Ctrl+Alt+Up and Ctrl+Alt+Down.
  Expected: Cooler 3100 K, then warmer 2850 K. Repeated presses clamp at
  1000 and 6500 K. Super+grave resets; the next Down selects 6250 K.
  `~/scripts/redshift-control adjust 250` and `adjust -250` exercise the same
  helper and print the resulting kelvin value. Raw external Redshift commands
  are not tracked; choose a preset first if they have changed the filter.
  Each successful preset, adjustment and reset also shows `🌡️ Redshift` with
  the applied value (for example `2100 K`; reset `6500 K`) in Dunst for two
  seconds. Rapid adjustments edit the existing popup in place by reusing its
  notification ID, including at the limits. After expiry, the next change
  creates a fresh popup.
  Fish `redshift-set` and login calls to the shared helper also notify.

- Action: In an i3 desktop session, run `~/scripts/redshift-control set 2100`,
  then `~/scripts/redshift-control adjust 250` and `~/scripts/redshift-control reset`.
  Expected: Terminal output stays unchanged; Dunst shows 2100, 2350 and 6500 K.
  A failed Redshift operation shows no success popup and preserves saved state.
  If notify-send or the notification service is unavailable, successful changes
  still print their value and exit 0. Restore the preferred preset afterward.

- Action: Run `python3 scripts/smoke_redshift_keys.py`, then `python3 scripts/smoke_redshift_keys.py ~/.config/i3/config` and `python3 scripts/smoke_redshift_keys.py --live` after refreshing and reloading i3.
  Expected: Each prints PASS for 1–0 = 1800, 2300, 2850, 3350, 3900, 4400, 4950, 5450, 6000, 6500 K, Alt+Super presets and Super+2–0 presets, and grave reset plus Ctrl+Alt+Up/Down = +/-250 K. Alt+digits remain workspace shortcuts; Super+1 and Super+F11 select workspace 11. No sudo is needed; the live check requires a running i3 session.

- Action: After `refresh-config` and an i3 reload, hold Alt+Super and press the number-row keys `1` through `9`, then `0`; press Super+grave to reset.
  Expected: Redshift selects 1800K, 2300K, 2850K, 3350K, 3900K, 4400K, 4950K, 5450K, 6000K, and 6500K; 0 selects 6500 K and grave resets the filter. Alt+number still switches workspaces; Super+F11 selects workspace 11, and Super+1 selects workspace 11 without changing temperature. Super+2–0 retain their Redshift presets.
- Action: In the default i3 mode, hold Right Alt (X11 keycode 108) and press number-row `1`, `2`, then `0`; repeat with Left Alt and return to the original workspace. Run `xev -event keyboard` and press Right Alt alone if the physical key is uncertain; inspect `xmodmap -pm` for its modifier.
  Expected: Both Alt keys select workspaces 1, 2, and 10. `xev` reports keycode 108 and `Alt_R`; `xmodmap -pm` lists `Alt_R (0x6c)` under `mod1`. Test physical keys after login as well; synthetic events do not validate keyboard firmware.
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

- Action: At a fresh i3 login, before opening Fish, hold a key in a text field.
  Then run `xset q`. For manual startup, run
  `env -u XSET_DELAY -u XSET_RATE ~/scripts/ubuntu-start` and query again.
  Expected: Repetition starts after 200 ms at 90 repeats/second; `xset q`
  reports those values even without Fish exports. A nonempty `XSET_DELAY`
  or `XSET_RATE` overrides only that value; an empty value uses its default.
  Missing optional `xset` does not prevent other startup helpers from running.

- Action: Run `python3 scripts/enable-ubs-boot-mount.py --check` from the repo root
  with the intended ext4 wallpaper disk mounted at `/mnt/linux-files-3`, then run
  it once with `sudo` and `--apply`. Repeat `--check` afterward.
  Expected: The preview shows the mounted disk's UUID. Apply prints an fstab
  backup path; the repeated check says the boot mount is already configured.
  Conflicting entries are refused. No disk is formatted or unmounted.

- Action: Start a fresh Ubuntu/i3 session on the desktop host where
  `/dev/sdc1` is present and Graphiti is checked out at
  `/home/example/coding/graphiti/mcp_server`.
  Expected: `ubuntu-start` mounts `/dev/sdc1` at `/mnt/linux-files-3`
  after configuring `sudo python3 scripts/enable-ubs-boot-mount.py --apply`
  once from the repo root. The UUID-based systemd automount makes the wallpaper
  available without a sudo prompt in i3. Confirm the wallpaper is visible before
  opening a terminal or running `ubs` manually. It mounts the disk before
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

## External 8 TB Automatic Mounting

Preview the existing disk configuration, install the UUID-specific rules once with administrator authentication, then verify a safe power cycle. This setup mounts the disk on arrival and on access without requiring it to be powered on during boot.

- Action: From the repo root, run `python3 scripts/enable-usb-8tb-automount.py --check`, then `sudo python3 scripts/enable-usb-8tb-automount.py --apply`. Repeat `--check`.
  Expected: Preview reports installation pending until applied. Apply backs up the changed fstab, installs the udev rule and reloads systemd/udev. Repeated preview reports configuration installed (it does not certify runtime). An existing mounted filesystem remains mounted; automount startup is deferred until next boot if necessary. Conflicting entries/rules are refused. No data is formatted or erased.
- Action: After installation, inspect `systemctl status 'mnt-usb\x2d8tb.mount' --no-pager` and `findmnt --mountpoint /mnt/usb-8tb` while the disk is on.
  Expected: The mount is active and the ext4 source UUID is e2f4a51f-954a-4168-a1af-2c9645d3f00a. Do not count an autofs-only row as the disk being mounted.
- Action: Close applications using the drive, unmount it successfully with `sudo umount /mnt/usb-8tb`, switch it off, then switch it on and wait for device discovery before running `findmnt --mountpoint /mnt/usb-8tb` without first browsing the directory.
  Expected: The UUID-specific udev event eagerly mounts the ext4 disk again. Repeat this sequence to confirm reattachment. If unmount reports busy, leave the drive powered on and close its users; never pull power on a mounted filesystem.
- Action: On a convenient reboot with the drive off, check that login succeeds, then turn the drive on and open `/mnt/usb-8tb`. Inspect the mount and automount units.
  Expected: Boot proceeds without the disk; automount is available, the drive mounts when it arrives, and its files appear at the fixed path. An access while absent fails after approximately five seconds of device waiting; no files should be written into an unmounted backing directory.
- Action: To undo installation, remove only `/etc/udev/rules.d/99-usb-8tb-automount.rules`, restore the printed fstab backup after checking for later edits, then reload systemd and udev. Reboot when convenient to retire the automount without disrupting users of the disk.
  Expected: The previous boot-only mount policy returns. Disk contents remain untouched.

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

- Action: Press left Super (keycode 133)+M twice while audio is playing.
  Expected: Each press toggles speaker mute/unmute, the volume block updates, and a two-second Audio popup shows Muted or Unmuted. Rapid presses update that popup in place without stacking; the second press restores the original mute state, and no text is typed. Repeat with the mute media key; it shares the same popup. Redshift keeps its separate popup.

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
  Expected: `DVI-D-0` is 2048x1152 at `+0+0`, `DP-2` is 3840x2160 at `+2048+0`, `HDMI-0` is 1920x1080 at `+5888+0`, and i3 shows bars on all three monitors with the middle 4K bar ordered `volume`, `spotify`, `calendar`.
- Action: Play a long song and add workspace buttons on DP-2 until the status area is crowded, then remove the extra workspace buttons.
  Expected: Volume sits near the center of DP-2, immediately left of the song. The song fills available space and ends in an ellipsis when too long; compact text puts the title before the artist. More workspace buttons shorten the song and move volume right only as necessary. Calendar shortens, then hides, before volume can be clipped. A short or absent song retains volume's centered position. Volume clicks and song controls still work. Workspace buttons alone consuming the entire display exceed i3bar's physical capacity.
- Action: Right-click the volume block twice, then left-click twice on each bar.
  Expected: Right-click keeps audio muted; left-click keeps audio unmuted. Neither
  changes the playback device. Middle-click still sets 15%, and scrolling still
  changes volume by 3%.
- Action: ~/scripts/flavibot-browser
  Expected: After refresh-config, opens https://flavibot.xyz/music-player in a separate Chrome process using ~/.local/share/flavibot-chrome. Sign in once and start playback. Later launches reuse that directory; existing Chrome profiles are untouched. Follow the [short usage guide](flavibot-browser.md) for daily use. Reserve this window for FlaviBot and use ordinary Chrome for YouTube.
- Action: ~/.config/i3blocks/scripts/now_playing_mpris
  Expected: While FlaviBot or Spotify plays, emits `▶ Artist - Title` for both full_text and short_text, with the triangle small and raised via Pango; when paused, emits `‖ Artist - Title` with the pause mark rendered the same way. Both markers sit centered rather than touching the bar's lower edge. The third line is pywal color7. The 4K status wrapper measures the live bar font, DPI and workspace buttons to fit this text with an ellipsis; its raw config retains an invisible compact form as a fallback. The bar follows within five seconds and shows no state glyph when no player is eligible. Title-only songs are also eligible; artist/title regex matching is no longer used.
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
- Action: In Kitty, print 200 numbered lines, press Ctrl+A, then Ctrl+Shift+C and paste into an editor. Repeat after selecting a smaller region first.
  Expected: The highlight includes the earliest retained line above the screen through the last visible line; pasted text includes the first and last numbered lines. Ctrl+A replaces the shell/application line-start shortcut. Selection is limited to retained history (50,000 configured lines).
- Action: Repeat inside tmux, including from an existing copy selection with either emacs or vi mode keys. Press Ctrl+A twice, copy with Ctrl+Shift+C, then Escape and type at the prompt.
  Expected: All retained text in the active pane is selected and copied, including wrapped lines and offscreen history. Repeating Ctrl+A selects the same complete text. Escape returns to live input; Ctrl+Space remains the tmux prefix.
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
an existing local short MP3; this checkout bundles `scripts/sire.mp3`.

- Action: `~/scripts/codex-notification-activate --open-kitty`
  Expected: Your notification-bus Dunst restarts and a fresh Kitty process opens;
  existing terminals remain open. Its history/queue clears; the sound setting is
  unchanged (disabled on a fresh installation).
- Action: `~/scripts/codex-notification-sound status`
  Expected: A fresh installation reports aligned sound/speech state and voice readiness.
  `status --plain --details` uses ASCII and reveals machine-local JSON/error-log paths. No local sound-path
  setting is bundled. An already configured machine reports its selected path.
- Action: Run `chezmoi apply "$HOME/scripts/sire.mp3"`, then `~/scripts/codex-notification-sound set "$HOME/scripts/sire.mp3"`.
  Expected: With an existing clip at that path, sound is enabled through local
  mode-0600 JSON. The MP3 stays intact; `set` only stores its path.
  Selecting another filename with spaces preserves the entire path.
- Action: If visible popups have neither clip nor speech, run `~/scripts/codex-notification-sound status --details`, correct a missing clip path with `set`, then run `~/scripts/codex-notification-sound preview --title "Notification audio check" --details`.
  Expected: A stale path reports an error before either audio stage. After selecting an existing clip, status reports it enabled and preserves the existing speech setting. With the voice ready, preview plays the clip then the sentence and exits 0 without a daemon restart. Historical error-log entries retain their old timestamps.
- Action: `~/scripts/codex-notification-sound preview`
  Expected: One clip plays without a popup; exit 0 on success. Invalid/missing
  files or unavailable mpv report errors and exit 1 without affecting popups.
- Action: With Sire selected and the voice installed, run `~/scripts/codex-notification-sound preview --title "Your notification is ready."`.
  Expected: "Sire" plays once, then Ryan reads "Your notification is ready."; the old question phrase is absent. The original question MP3 remains intact.
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

Scroll, select and copy with familiar gestures. Start a left-button selection,
drag to the pane's first text row, and keep holding there to scroll into older
output while extending the same selection. Stay inside the text area, below
Kitty's titlebar; no wheel movement is needed. Release, then copy
with Ctrl+Shift+C; the highlight and viewport remain in place. Escape returns
to live input. The history-mode status line shows the copy and exit shortcuts.
Use the disposable helper below after refresh-config; no sudo is needed.
Use a pane at least three text rows tall for the tmux 3.4 edge-release workaround.

- Action: Run ~/scripts/tmux-scrollback-smoke, then hold Shift and wheel up over the text with no mouse button held.
  Expected: Earlier numbered HISTORY lines appear. Plain wheel also browses history at a shell, and Alt+wheel remains available. New panes retain up to 50,000 rows; record 000001 is reachable in the 3,000-record fixture. Existing panes retain their old limit and discarded output cannot be recovered.
- Action: In the fixture, left-drag from a numbered line to the first text row. Keep the button held and the pointer stationary inside that row until more than two screens scroll past; do not hold Shift. Release, move away, press Ctrl+Shift+C and paste into an editor. Include a long WRAPPED logical line ending in END.
  Expected: Older numbered rows continue appearing without wheel events. One continuous blue selection grows across screens and persists after release. The pasted text includes every selected record and wrapped logical line in order, without extra newlines at soft wraps; the viewport stops when released and stays in place through repeated copying. The status line shows Copied.
- Action: Copy unrelated text in another application, return to the retained tmux selection, press Ctrl+Shift+C again and paste into the editor.
  Expected: The entire original selection replaces the unrelated clipboard text. No mouse button needs to be held while copying. A copy request without a selection shows a selection hint instead of clearing the clipboard.
- Action: Press Escape, type hello and Enter, then press Ctrl+D at empty live input to close the fixture.
  Expected: Escape returns to the live tail in one step and INPUT hello confirms normal typing. Wheel-down alone also exits wheel-entered copy mode if you have not started a selection; after selecting, use Escape. Only the disposable fixture closes.
- Action: Run ~/scripts/tmux-scrollback-smoke --app-mouse. Try plain wheel/click, then Shift+wheel up, release Shift and repeat the held-edge drag/release/copy check.
  Expected: Ordinary application gestures produce APP_MOUSE records. Shift+wheel explicitly opens tmux history despite app mouse ownership; the same multi-screen selection/copy flow works. Escape returns to the application. Alt+C also opens history without a wheel. Alt+wheel remains an alternative. tmux history is separate from an application's private document history.
- Action: In a fresh raw Kitty shell without tmux, select text normally and copy with Ctrl+Shift+C. In tmux, hold Shift while dragging to deliberately select the visible Kitty screen, then copy with Ctrl+Shift+C.
  Expected: Native Kitty selection copying remains available. Ctrl+Shift+C chooses the native Kitty selection when one exists, otherwise the highlighted tmux selection. Native Shift-drag cannot select tmux-owned older output. The shortcut works both from an interactive fish shell and the i3 launcher using fish -c tmux-attach; the shell may own the foreground process group while tmux is another member.
- Action: Separately try dragging the right edge of the tmux fixture.
  Expected: Installed tmux 3.4 has no draggable pane history scrollbar (native support first appears in 3.6); edge dragging selects text rather than giving raw Kitty thumb parity. The scroll/copy flow above uses pane-owned history.

### Prepared tmux scrollbar preview

Preview native pane scrollbars using the separately installed tmux 3.8 binary.
The default tmux and existing sessions keep running on their original server.
This requires `~/.local/opt/tmux-3.8/bin/tmux`; it is a local preparation,
not an automatic bootstrap dependency. No sudo is needed.

- Action: Run ~/scripts/tmux-scrollback-smoke --scrollbar.
  Expected: A separate Kitty window opens a disposable tmux 3.8 server with a right-edge pane scrollbar and 3,000 numbered history records. The helper prefers ~/.local/bin/kitty when installed, so an older /usr/bin/kitty earlier on PATH cannot reject the modern configuration. No configuration-error dialog appears. Current school-2 windows and all other sessions remain running.
- Action: Grab the pane scrollbar thumb at the right edge and drag it upward, then back downward. Press Escape, type hello and Enter, then Ctrl+D at empty input.
  Expected: The pane shows earlier numbered HISTORY records without selecting text. Escape returns to live input, INPUT hello appears, and Ctrl+D closes only the disposable preview.
- Action: Repeat with ~/scripts/tmux-scrollback-smoke --scrollbar --app-mouse.
  Expected: The tmux pane scrollbar still browses history while plain wheel/click events over the application produce APP_MOUSE records. Only preview processes are cleaned up on exit.

Preparing this binary does not add a scrollbar to already-running school-2.
Activating it there requires a separately approved migration to a new server;
do not kill the shared 3.4 server or replace its client while work is active.
The current edge-selection regression suite passes 24/24 on 3.4 and 20/24 on
3.8: stationary top/bottom edge gestures differ in both copy-mode tables.
The preview checks scrollbar dragging; it does not certify replacement of the
existing selection workflow. Resolve those differences before migration.

### Kitty and Codex scrolling

Use a fresh Kitty window after refresh-config: a larger history cannot recover
lines an older window already discarded. This checks one scrollbar per Kitty
terminal window. Inside tmux, use wheel/Alt+wheel or Alt+C copy mode for pane-owned history; see the tmux checks above.
The fixture uses the normal Kitty configuration without overrides. Ordinary
Codex launches use the persistent tui.alternate_screen = "never" setting;
restart or resume an existing Codex session to pick up that default.
Keep the fixture at least 40 columns wide through the first history check so
wrapping all 10,000 records fits inside the configured 500,000-line buffer.
Kitty's native history limit is 500,000 lines; tmux keeps its separate
50,000-line limit per pane.

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
  Expected: The script immediately prints that it is checking Chrome, refreshes APT metadata, then displays the installed and refreshed candidate versions. It upgrades `google-chrome-stable` only when installed is older, re-reads the candidate after installation, and accepts installed versions equal to or newer than that candidate. A failed policy query prints an actionable error instead of exiting silently. `--check` remains read-only and uses cached metadata. Relaunch Chrome and check `chrome://settings/help` afterward.
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

- Action: Run `fish --no-config -c 'source ~/.config/fish/key_abbr.fish; abbr --show | string match "abbr -a -- va *"'` after refresh.
  Expected: `abbr -a -- va 'cd ~/coding/twitch-grid'`. Repeating the absolute
  directory request previews a no-op. If chezmoi excludes the live catalog,
  reconcile only the reviewed catalog and regenerate shortcuts; preserve
  unrelated managed-file conflicts.

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
  Expected: Output shows red DND/queue markup or `Notis` using wallpaper color7
  (the same color as volume/date) without changing pause.

- Action: After applying the secondary-bar configuration and reloading i3,
  inspect the left monitor's bar, right-click its `Notis`/`DND` indicator twice,
  then left-click it twice.
  Expected: The indicator appears immediately left of volume, switches to DND when
  paused by right-click, and returns to `Notis` matching volume/date on left-click.
  Repeated clicks keep the selected state. External pause changes appear
  within two seconds; restore the original pause state after checking.

- Action: Right-click the notification block to enable DND. Note the existing
  `dunstctl count waiting`, then send two distinct `notify-send` test notifications.
  Left-click the block to enable notifications after checking the queue.
  Expected: No test popup appears while paused; waiting count increases by two
  and the bar shows `DND (N)` within two seconds. On resume, both test popups
  are delivered and the block returns to `Notis`. Restore the original pause state.

## Metaprompt terminal handoff

Use disposable data for helper checks; no sudo is required. Live previews can
play audio, so exercise them deliberately.

- Action: Invoke Metaprompt & Run with a small supplied task in a disposable workspace, and inspect its existing-thread terminal handoff.
  Expected: The local depth pass respects accepted scope. One execution UUID is created, the matching Kitty instance opens or reuses its tab, and failed navigation preserves that UUID.

## Neovim clipboard startup

Use disposable data for helper checks; no sudo is required. Live previews can
play audio, so exercise them deliberately.

- Action: Start Neovim normally on X11 with xclip installed and no explicit clipboard provider; repeat with an explicit provider or Wayland session.
  Expected: Neovim 0.11.1 or newer selects xclip without a synchronous xsel clipboard read; explicit and Wayland providers keep their normal selection.

## Context Mode retrieval

Use disposable data for helper checks; no sudo is required. Live previews can
play audio, so exercise them deliberately.

- Action: Run the Context Mode demo from the repository root with --case index, --case search and --case empty after the pinned package is installed.
  Expected: Disposable MCP state reports index/stats, matching retrieval and no-result behavior respectively. Existing client configuration is unchanged.

## Code-review graph checks

Use disposable data for helper checks; no sudo is required. Live previews can
play audio, so exercise them deliberately.

- Action: Run the code-review-graph smoke helper in --mode cli and --mode mcp with an existing reviewed binary.
  Expected: CLI caller/incremental checks pass; MCP exposes exactly four query tools and leaves an unbuilt graph unbuilt.

## Public benchmark evidence boundary

**Action:** In a disposable repository using this checkout's `.gitignore`, create a raw JSON file under each benchmark `runs/` root and an aggregate report outside those roots; run normal `git add .`.

**Expected:** Both raw files remain ignored; the aggregate report is eligible for staging. Actual run directories, request/response traces and raw ledgers remain private.

**Action:** In a disposable Git repository, commit JSON containing an installation or session UUID, including nested serialized JSON, then remove it and run `executable_audit-public-history --repo <fixture> --scope all --plain`.

**Expected:** The auditor reports `runtime_identifier` without printing values and exits 1. Removing the latest file alone does not clear its historical finding. Use synthetic fixture values only.

### Media conveyor screensaver

- Action: Update with `./scripts/executable_media-screensaver install`, then run `./scripts/executable_setup-screensaver-timer` twice from an X11 desktop terminal; inspect `systemctl --user list-timers --all media-screensaver-daily.timer`.
  Expected: Both installs succeed without sudo, the timer is active with the next local 10:00 AM trigger, and the existing idle service is unchanged. Enabling after 10:00 AM does not catch up an inactive timer; suspend across 10:00 AM may launch on resume. Missing/outdated launcher or missing DISPLAY produces an actionable error.
- Action: Start `media-screensaver-daily.service` from the unlocked desktop, dismiss with physical input; repeat while locked and while browser bridge coverage is unavailable. Disable with `./scripts/executable_setup-screensaver-timer --disable`.
  Expected: Displays power on and idle monitoring resumes before allowed playback starts without a five-minute wait; input dismisses it. Locked/uncertain-lock sessions skip playback; missing browser coverage leaves scheduled playback visible, while idle automatic activation stays suppressed. Disabling removes future daily triggers and leaves running playback alone.
- Action: Start the daily service with the browser bridge unavailable and leave the desktop untouched beyond the configured screen blanking/DPMS timeout; then dismiss with physical input and inspect `xset q`.
  Expected: Scheduled playback clears an already blanked X11 screen and stays visible past that timeout; dismissal releases inhibition and the original timeout/DPMS settings are unchanged. A locked session still skips playback.
- Action: Run `~/linux-config/scripts/executable_setup-screensaver-timer --test` in the X11 desktop; do not touch input for ten seconds, then dismiss playback. Repeat and press Ctrl+C during the wait.
  Expected: Displays turn off, wake ten seconds later and show manual preview without changing the daily timer. Ctrl+C during the wait wakes displays and exits without preview.
- Action: Dismiss manual previews, type `sofss` (or `sofs`) and press Enter in fish before 10 AM; leave the desktop untouched until 10 AM. Repeat after 10 AM when the next-day wait is acceptable.
  Expected: The daily timer is armed before idle/daily playback stops and displays power off. At the next local 10 AM displays wake, idle monitoring resumes and scheduled playback starts when unlocked even without browser coverage. Input can wake displays early; suspend can delay the timer. The command does not power off the computer or enforce a blackout through input.

- Action: Run `~/scripts/media-screensaver orient` (or add `--media DIR`) and choose a video; move the mouse and use the keyboard inside the review window.
  Expected: The chooser starts in the selected library, playback loops muted, rotation and Save/Cancel controls stay visible, and ordinary input does not dismiss review.
- Action: Open `~/scripts/media-screensaver orient --file '/absolute/path/problem.mov'`, rotate left/right until upright, save and reopen; reset with Use metadata and save. Repeat a change using Cancel and window close.
  Expected: Left/right describe the displayed picture, two clicks turn it 180°, saved corrections survive reopening, Use metadata removes them when saved, and Cancel/close preserve the previous saved value. Originals have unchanged hashes. Space-containing paths work.
- Action: Preview a small directory with that corrected video for 35 seconds without physical input; include already-upright portrait/landscape clips, missing-metadata and rotated-metadata clips. Replace a disposable corrected file and reopen review; separately back up the private orientation JSON, make it malformed, and try review/save before restoring the backup.
  Expected: Metadata plus additional correction stays upright across all slots and loops, with preserved aspect ratio and black bars. Changed files ignore stale corrections. Malformed JSON warns, playback remains available, Save fails visibly without replacing data, and Cancel releases playback.

- Action: After refreshing and reloading i3, press left Alt (keycode 64)+Shift+S and release the keys; repeat with Super+Shift+S; wait without moving the mouse, then move it.
  Expected: Releasing the shortcut starts the Hevin preview without opening a terminal; subsequent physical input dismisses it. Super+S still opens Spotify and Alt+S still selects stacking layout.

- Action: Load the generated fish abbreviations, type `ss` and press Space to inspect its expansion, then run it.
  Expected: It expands to `~/scripts/media-screensaver preview` and starts immediate playback even without the browser bridge; physical input dismisses it. The previous slideshow mapping remains commented in the command template.

- Action: Install with `./scripts/executable_media-screensaver install`, enable the unpacked extension from `~/scripts/media_screensaver/browser` in each Chrome/Chromium profile, reload existing tabs and run `~/scripts/media-screensaver status`.
  Expected: The stable extension ID is fpologomejgfmlemideffbaallaejhbb, status explains current bridge coverage, and native state contains only geometry/playback/IDs with private permissions. An uncovered visible browser profile suppresses automatic activation.
- Action: If status reports an unavailable browser bridge, verify **Load unpacked** was completed in every Chrome profile (installing the native host alone is insufficient), enable the extension and reload existing tabs, then run `~/scripts/media-screensaver status` again.
  Expected: A connected bridge replaces the generic unavailable-bridge reason with readiness or a specific playback/coverage reason. Keyboard/mouse use resets the idle count normally; restarting the service alone does not install the extension.
- Action: Record `xrandr --listmonitors`, run `~/scripts/media-screensaver demo --report /tmp/conveyor-demo.jsonl` with a fresh report path, and watch item #1 for 35 seconds without touching keyboard/mouse.
  Expected: All three screens have media at launch. Item #1 travels left → middle → right → exit on successive ten-second advances with 750ms slides, letterboxing stays black, and report playback timestamps continue across moves. After exit there are no child players and monitor geometry matches the original.
- Action: Launch `ss` twice with a multi-file photo/video library, then preview a directory containing just one disposable image or video.
  Expected: Each launch selects random media for all three outputs without a twenty-second fill delay; adjacent selections differ when possible, while a one-file library fills all outputs with that file. A repeat across launches is valid random selection. No persistent black rectangle obscures a picture; intended aspect-ratio bars remain black.
- Action: Preview a small library containing portrait photos, HEIC, one-second clips, a longer video and a corrupt file; repeat with `--media /nonexistent/synthetic-media`.
  Expected: Portrait/HEIC images fit without cropping, short videos loop, long videos stop on exit, corrupt items are skipped without stopping other cards, and the missing directory reports an actionable error. Originals are unchanged.
- Action: In a covered active Chrome tab, play a visible video on the middle output, move it to each side, pause/resume, enter fullscreen, and repeat with a second window, an iframe player, a background tab, and audio-only playback.
  Expected: Only actively playing visible active-tab video intersecting the middle output blocks activation; pause/end, side-only video and audio do not. Moving/resuming qualifying video dismisses the running screensaver promptly. Uncertain geometry/coverage suppresses activation with a status reason.
- Action: Start `~/scripts/media-screensaver service`, confirm `systemctl --user status media-screensaver.service` is active, leave the desktop untouched for five minutes, then move the mouse/type; repeat while the bridge is disabled and while the session locks/suspends normally.
  Expected: The unit runs the idle daemon and is started on subsequent i3 logins. A healthy unblocked bridge permits activation after 300 idle seconds; activity dismisses and releases all pipelines. Missing/stale bridge prevents automatic activation but allows manual preview. Existing lock, suspend and display settings remain intact.
- Action: With the idle service active, run `systemctl --user kill --signal=TERM --kill-whom=main media-screensaver.service`, wait six seconds, and inspect its status and journal; then stop it with `systemctl --user stop media-screensaver.service` and start it again with `~/scripts/media-screensaver service`.
  Expected: Termination is followed by a new daemon PID after five seconds and a fresh idle clock; deliberate stop leaves the service inactive and releases any owned preview. Starting again succeeds without duplicate monitors.

### Notification speech volume

- Action: Run `~/scripts/codex-notification-sound speech-volume 75`, then run it again without the number.
  Expected: Both report `Speech volume: 75%`; the value persists for future speech. Browser/system and intro-clip volume remain unchanged.
- Action: Run `~/scripts/codex-notification-sound speech-volume 101`, then query the value.
  Expected: Clear 0–100 validation error, exit2; previous volume remains75.

### Discord channel and DM notification speech

Apply the helper and Dunst rule using the notification guide, restart Dunst once,
and enable `discord-speech`. No sudo. The probes are synthetic and play local audio.

- Action: Run `~/scripts/codex-notification-sound status --plain`.
  Expected: Discord speech enabled, Ryan ready; existing Codex speech/clip state unchanged.
- Action: Run `~/scripts/codex-notification-sound smoke discord`.
  Expected: Normal popup `(A) Alex (#normie, Active)` / `hai`; Ryan says `(A) Alex says hai` with no intro clip.
- Action: Run `~/scripts/codex-notification-sound smoke discord-unicode`.
  Expected: Normal Unicode-channel popup; Ryan says `Alex says hello`, without channel/server text.
- Action: Run `~/scripts/codex-notification-sound smoke discord-dm`.
  Expected: Synthetic Vesktop popup `Alex` / `hello from a direct message`; Ryan says `Alex says hello from a direct message` with one WAV and no intro clip.
- Action: Run `~/scripts/codex-notification-sound smoke discord-isolates`.
  Expected: Unicode channel popup with invisible direction isolates; Ryan says only `Alex says hello` exactly once, without channel/server text or an intro clip. The fixture uses Vesktop identity to catch overlapping rules. While watching a stream, speech should sit below it at the default 75% software volume; browser/system volume stays unchanged.
- Action: Run `~/scripts/codex-notification-sound smoke discord-saucybot`.
  Expected: Popup contains tweet fixture text and a URL; Ryan says only `SaucyBot sends tweet` exactly once, without contents, URL or intro clip.
- Action: Run `~/scripts/codex-notification-sound smoke discord-links`.
  Expected: Ryan says only `Alex sends link`; neither surrounding prose nor URL is spoken.
- Action: Run `~/scripts/codex-notification-sound smoke discord-link-only`.
  Expected: Popup appears; Ryan says only `Alex sends link`, with no intro clip.
- Action: Run `~/scripts/codex-notification-sound smoke discord-twitter-cap-bot`.
  Expected: Popup appears with no speech or intro clip. Twitter Cap Bot sender matching ignores case and covers channels and DMs.
- Action: Run `~/scripts/codex-notification-sound smoke discord-unrelated`.
  Expected: Normal `Voice: listening` popup with body `nerd-dictation is ready`; no speech.
- Action: Disable `discord-speech`, repeat a matching probe, then enable it again. Check status before and after.
  Expected: Matching popup is silent while disabled; Codex speech and selected clip remain unchanged.
- Action: Receive a real Discord channel notification without sending a message for this test.
  Expected: If its complete title matches, hear sender says message once, with normal popup behavior. Sender-only Vesktop DMs speak sender says message; unknown-app sender-only notifications remain silent. Client-muted messages never reaching Dunst remain silent. Record subjective listening separately.

## Kitty font shortcuts

- **Action:** Focus a Kitty window and press Ctrl+Shift+Up/Down, Ctrl++/Ctrl+-
  and Ctrl+= (Ctrl++ is Ctrl+Shift+= on a US keyboard).
  **Expected:** Each press increases/decreases its font by one point; other OS
  windows keep their size.
- **Action:** Press Ctrl+Super++ to enable i3 gaps, then Ctrl+Shift+0 to remove them.
  **Expected:** Gaps change as before; Ctrl++ remains available to Kitty.

## Kitty monitor font sizing

- **Action:** Open new default and Ctrl+Return terminals on the current output;
  run `~/scripts/kitty-monitor-font status`.
  **Expected:** Both use baseline19pt: main19pt, left14.12pt, right11.31pt.
  Existing terminal zoom and placements remain unchanged. A new tmux window
  inherits its containing Kitty font size.
- **Action:** When convenient, explicitly launch12pt and19pt fixtures. Move
  each window and its whole workspace to
  DVI-D-0, HDMI-0 and DP-2; repeat three times with another terminal unfocused.
  **Expected:** Left targets are8.92/14.12pt, right7.14/11.31pt, main12/19pt
  within Kitty rounding. Returning to main restores exact baselines; independent
  windows/instances are unaffected. Compare physical letter height visually.
- **Action:** Zoom a side terminal, return to DP-2, launch a new side terminal,
  and restart `kitty-monitor-font.service` while a terminal is scaled. Inspect
  helper status after two seconds and move back to DP-2.
  **Expected:** Zoom becomes the updated baseline; new terminals use their actual
  launcher size; service restart causes no second shrink. Unknown outputs and
  missing sockets are skipped; service heartbeat reports unavailable sockets.
- **Action:** Run `~/scripts/kitty-monitor-font-smoke --plain`.
  **Expected:** Disposable Xvfb/Kitty checks end in PASS for both baselines,
  round trips, restart, zoom, restore and unfocused/cross-instance isolation.
  Existing desktop windows stay untouched; this does not accept physical sizing.
- **Action:** For rollback, remove the new i3 autostart line, refresh/reload i3,
  then run `~/scripts/kitty-monitor-font restore` while Kitty remains running.
  **Expected:** Service stops and tracked windows regain main baselines; no
  global DPI, remote-control restrictions or launcher settings change.
