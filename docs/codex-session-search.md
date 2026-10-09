# Search and resume Codex conversations

Use `codex-search` to find saved conversations across projects or return to the work that needs attention. Open `crg` for AI priority, inspect its recap and reason, then select a session in fzf to resume in its recorded directory. The picker opens from usable local metadata while archive indexing continues in the background, then refreshes as Guardian or another session updates the evidence.

## Install and use

Chezmoi installs [the executable source](../scripts/executable_codex-search) as `~/scripts/codex-search`. Run `refresh-config` after tracked configuration changes; it snapshots live Codex and Git config into tracked source, applies chezmoi, regenerates shortcuts and reloads fish abbreviations. Protect unrelated dirty source before that refresh. Python 3.11+ must be on PATH; pattern search also needs `rg` (ripgrep). `fzf` is optional and only required by `--pick`. Running the tool requires no sudo. On the repo's non-GUI hosts, `.chezmoiignore` excludes scripts; invoke the source directly there.

If `--pick` reports that fzf is missing, the search command itself is working;
install the optional picker dependency or put a trusted `fzf` binary on PATH.
On example-user's desktop, fzf 0.44.1 is now installed at `~/.local/bin/fzf`, already
on the fish PATH. It was installed without sudo from the checksum-verified
Ubuntu package. Retry the same `codex-search --pick "pattern"` command.
This user-local binary is outside chezmoi/Git; other hosts still need fzf separately.

```bash
codex-search --help
codex-search --recent
codex-search --recent --limit 0
codex-search --recent --pick
crg  # fish abbreviation for codex-search --recent --pick
codex-search --recent --pick --sort recent
codex-search --recent --sort priority --details --limit 5
codex-search --recent --pick --no-summaries
codex-search --recent --pick --summary-count 0
codex-search --recent --pick --summary-count 5 --summary-model MODEL
codex-search "cache.*refresh"
codex-search -i "resume"
codex-search -F "literal [brackets]"
codex-search --all-text -F "tool output phrase"
codex-search --pick "deployment"
codex-search --limit 5 "root"
codex-search --details --limit 0 "root"
codex-search -- "-flag"
```

In fish, `csg` expands to `codex-search`; `cs` retains its existing terminal-clear command. `--help`, `-h` or no arguments print usage, option descriptions, examples and documentation paths without indexing or requiring rg/fzf. Ordinary results go to stdout and can be piped; progress and warnings go to stderr. Exit codes are 0 for help, matches, completed maintenance or picker cancellation; 1 for no matches; 2 for invalid options, dependencies or runtime errors; 130 for interruption.

In a terminal, searches show the newest 20 matching sessions with an emphasized
directory, a readable UTC date, an optional title, one short excerpt and a
shell-quoted resume command. Actual ripgrep matches are highlighted; excerpts
fit the terminal width. `NO_COLOR=1` or `TERM=dumb` disables printed color.
`--plain` also disables printed color and uses ASCII decoration, including
truncation markers; in the recent picker it uses ASCII fzf borders. Conversation
text retains its original characters. Long resume commands stay complete so they
can be copied. A footer on stderr announces any
limit and points to `--limit 0` (all results) or `--pick` (browse all matches).

Use `--limit N` to choose the result count; 0 means all. `--details` shows the
full block: optional title, exact activity timestamp, recorded working directory,
UUID, up to five distinct matching snippets and resume command. For every full
block, use `codex-search --details --limit 0 "pattern"`. Piped output defaults
to all full blocks with no ANSI escapes; `--limit` can also bound a pipe.
The printed resume command remains:

```bash
codex resume -C '/path/with spaces/project' 00000000-0000-4000-8000-000000000001
```

`--pick` lists all matching sessions with directory and a snippet, regardless of `--limit`. Enter hands the exact UUID and directory to the normal `codex` executable on PATH, preserving the existing launcher. Esc or Ctrl-C in fzf launches nothing. A missing, relative, unrecorded or non-printable directory makes resume unavailable; restore that directory before trying again. No initial prompt is supplied. Selection defaults from FZF_DEFAULT_OPTS/FZF_DEFAULT_OPTS_FILE are ignored so custom binds or multi-selection cannot change this action.

## Browse recent sessions and recaps

`--recent` needs no pattern. Ordinary listing defaults to the latest recorded
session activity across all discovered directories; `--sort priority` instead
uses cached AI priority. Both listing modes read the cache without calling a
model. Listing prints 20 sessions even in a pipe; `--limit N` changes the count
and `--limit 0` prints all. Creation time, source filesystem timestamps and
recap-cache modification time do not determine activity order. Duplicate UUIDs
follow the existing newest-activity rule. `--sort` requires `--recent`, which
cannot be combined with a search pattern.

`--recent --pick` opens fzf from validated cached metadata without waiting for
a full archive refresh or its index lock. Explicit `--rebuild-index` completes
full indexing before opening the picker. A cold cache starts with a bounded
set of newest native session metadata; additional usable sessions appear as
background indexing proceeds. Startup title lookup is bounded; remaining native
titles catch up in the background. `--limit` does not cap the picker. `crg` and
`--recent --pick` default to AI priority; `--sort recent` restores newest-first.
Each row shows an abbreviated directory, title and activity time. The preview
shows priority, its reason and freshness, alongside the goal, reported progress,
current state and remaining work, or bounded local user/assistant dialogue when
there is no recap. Missing, queued, generating, stale,
unavailable and partial recaps are labelled explicitly; a stale recap remains
visible as older evidence. AI recaps describe reported conversation state and
are not independent verification of completed work.

Uncached pending previews show `AI recap: indexing`; generic rows also show an
`[indexing]` badge. An older cached recap remains visibly stale and ranks as
unknown until validated dialogue is available. Cold-cache native metadata and
activity are preliminary until full parsing supplies recorded activity. No inference starts
from pending metadata. Ctrl-G on a pending row remembers the request and waits
for its dialogue to become ready. You can browse and cancel while the archive
is still indexing; all history may not be ready at opening.

Priority orders sessions as **urgent**, **actionable**, **unknown**, **waiting**,
then **complete**, with latest recorded activity breaking ties. Urgent means
evidence of an issue needing immediate attention; actionable means unfinished
work you can advance now; waiting means an external dependency prevents the next
step; complete requires reported completion with verification and no evidenced
remaining action. Unknown covers insufficient or conflicting evidence. Missing
priority, legacy recaps and stale evidence rank as unknown. An older priority
and reason may stay visible in the preview, explicitly labelled stale, until
fresh inference arrives.
AI supplies priority and its reason in the same recap call; ranking adds no
separate model request.

The newest 20 sessions form the default automatic batch. One worker visits them
newest first and skips current recaps. `--summary-count N` changes that newest-session
window; zero disables automatic work while keeping **Ctrl-G** available for the
highlighted session, including sessions outside the batch. Manual requests go
ahead of queued automatic work, after the active request finishes. Each
UUID/dialogue/model/format generation key gets at most one attempt per opening. A
changed dialogue can receive a new attempt; title-only, activity-only and tool-only
changes reuse the recap and cause no additional model call. `--no-summaries`
prohibits all model calls, including Ctrl-G, while retaining cached recaps and
local previews.

`--summary-model MODEL` overrides the configured model; otherwise the existing
Codex login and effective configured model are used. Recaps consume that account's
normal model allowance. Each attempt, including isolation preflight, times out after 120 seconds. Authentication
or rate/usage-limit errors stop the batch; other failures mark only that recap
unavailable and browsing continues. Reopen to retry. Exiting or resuming cancels
and reaps background work first.

Activity timestamps in the recent picker and its preview use Toronto time
(`America/Toronto`). Rows use a compact date and 24-hour time (`Oct 8 12:24`);
the preview retains the year, seconds, UTC offset and seasonal EDT/EST label. Stored
timestamps and activity sorting remain unchanged.

Rows show an abbreviated directory, the title, then the short activity date,
with tight spacing. `/mnt/usb-8tb/` displays as `/m/usb-8tb>`; the full directory
stays in the preview and resume command. The preview wraps the full title and
recap, sits on the right in wide windows, and moves below in narrow windows.
Ctrl-/ toggles the preview to give the list the full window width when needed.

Rows named `Guardian review` or `(untitled)`, including missing names, use their cached AI recap headline as the title,
including stale cached headlines; the preview keeps the original native title
and recap status. Meaningful native titles stay unchanged. Without a cached
headline, the row keeps its native title until a recap arrives; the new headline
then appears in the list and preview without reopening.
Generation runs in the background. Generic rows show `[queued #2 12s]` for their
position in the waiting queue and time spent waiting, then `[generating 8s]` with
a fresh timer when generation starts. Timers update in whole seconds, including
configuration verification, and disappear when the current AI title is ready.
The queue position excludes the active request; Ctrl-G moves a waiting session
ahead without resetting its waiting time. Total provider work is unknown, so no
percentage or ETA is invented. The preview shows phase and elapsed time for every
session; another picker's elapsed time is measured from first observation here.
Missing titles outside the active queue show `[Ctrl-G]`; disabled generation
shows `[recaps off]`, and failures show `[unavailable]` with the reason in preview.
`--no-summaries` can still use cached headlines without generating new ones.

Typing filters activity/abbreviated directory/title, not the recap body. A
background reader indexes newest sources first in passes of at most 20 sources,
checking a roughly one-second soft budget between files and releasing the index
lock between passes. A single large file can exceed that budget after the UI
has opened. It publishes usable rows incrementally and continues checking for local
updates in the background. Guardian updates are ordinary local session/title
evidence; no separate callback is needed. Renames, activity, changed dialogue,
new sessions and deleted sessions appear without reopening. Large scans can take
longer; concise indexing progress remains visible while the picker stays usable.
Malformed or incomplete records are skipped without per-file warnings flooding
the UI. The default preview keeps a concise skipped/unreadable-input summary.
`--details` adds a bounded tail of background diagnostics in the preview, including
source paths; worker logs are private and temporary. Raw payloads stay excluded.
The newest-session automatic window is reevaluated after refresh. Priority and
activity changes reorder rows, while the entered query and highlighted UUID stay
selected while that session still exists and matches. A query matching only
`Guardian review` may lose that row when its AI title arrives; clear the query to
see the updated title. Enter with no matches resumes nothing. `--no-summaries`
still refreshes local evidence and cached recaps, with zero model calls.
This uses fzf's local authenticated control listener; fzf 0.44.1 is verified.
Enter always resumes `codex resume -C DIR UUID`, with no initial prompt.

### How model runs are isolated

The worker supplies only the parser's decoded user/assistant dialogue as inert
data. Recognized injected context, developer/system instructions, reasoning and
tool records stay excluded. Each session supplies at most 32 KiB of UTF-8 dialogue,
preserving its opening and latest content. Long records may be clipped at either
boundary; omitted content marks the result partial. Output must contain exactly
seven nonempty string fields (`headline`, `goal`, `progress`, `state`,
`next_steps`, `priority`, `priority_reason`). The text fields, including the
reason and excluding the single priority label, may contain at most 150
whitespace-delimited words total. `priority` must be one of the five supported
tiers; malformed output is discarded. Legacy five-field recaps remain readable
with unknown priority.

Generation uses noninteractive ephemeral Codex in a private temporary directory
whose working subdirectory is read-only. It does not resume or change the original
conversation or create a browsable recap session. Supported installed-CLI overrides
set read-only sandboxing and disable hooks, connectors/apps, plugins, MCP servers,
shell and web capabilities, instruction/skill discovery and telemetry. A local
app-server preflight verifies effective settings, hooks and MCP availability before
inference; an empty `mcp_servers={}` alone is insufficient because Codex deep-merges
configuration. Unverifiable isolation leaves generation unavailable and browsing
usable. Isolation is verified against Codex 0.160.1; different installed versions
must pass the same runtime checks.

## What is searched

Discovery recursively scans JSONL files under `${CODEX_HOME:-~/.codex}/sessions`; `session_index.jsonl` only supplies titles. Multiple source copies of a UUID produce one result. Default text consists of decoded user and assistant messages; mirrored event/message records do not duplicate snippets. Event-only historical logs also work. Recognized injected user context blocks, system/developer messages, reasoning, turn context, compaction summaries and binary attachments are excluded. An IDE's `## My request for Codex:` delimiter removes its context prefix. `--all-text` additionally searches known tool call/output records, including decoded JSON arguments, while retaining instruction exclusions.

`rg` matches decoded text with its own regex semantics. Matching is line-oriented; a pattern cannot span newlines. `-i` ignores case and `-F` treats the pattern literally. Other rg options are not forwarded. Ripgrep's personal config is ignored to keep these options predictable. Unknown record types are ignored; malformed records and incomplete JSONL tails are skipped without printing their private payloads. The recent picker keeps its default summary concise and exposes bounded background diagnostics in the preview only with `--details`; ordinary search and explicit rebuild can report skipped counts and source paths.

Schema sources verified before implementation: [rollout wire format](https://github.com/openai/codex/blob/main/codex-rs/history/src/rollout_payload.rs), [session metadata and events](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/protocol.rs), [response messages and content](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/models.rs), and [append-only title index](https://github.com/openai/codex/blob/main/codex-rs/rollout/src/session_index.rs). The installed CLI's `codex resume --help` verified UUID and `-C` support. Current upstream main can differ from older sessions; unsupported legacy formats and archived/compressed logs outside sessions/**/*.jsonl are not indexed.

## Cache and refresh

The cache lives under `${XDG_CACHE_HOME:-~/.cache}/codex-search/<SHA256-of-resolved-Codex-home>`. It contains private decoded conversation/tool text and source metadata; keep it out of Git, shared storage and backups that should exclude private conversations. Directories are restricted to 0700 and files to 0600; unexpected symlinks or ownership are rejected. Search, listing and indexing only read original sessions and make no network or model calls. Only the recent picker can start the explicitly controlled recap worker.

Ordinary search, listing and explicit `--rebuild-index` refresh compare source size, nanosecond modification/change times, device and inode. It reparses changed sources and removes deleted ones. Unchanged text files are reused. Parsing streams one JSONL record at a time, so memory scales with one record and per-session message digests rather than the full corpus. A file changed during parsing is marked for refresh next time. Atomic file replacement and a per-home flock serialize concurrent refresh/search/clear operations; the lock is released before fzf or Codex starts. Canonical role-labelled dialogue adds a third private per-source cache file and a content digest. The recent picker starts with usable metadata and performs these checks in bounded background passes; ordinary pattern search and explicit rebuild still finish full indexing before results.

```bash
codex-search --rebuild-index
codex-search --rebuild-index -F "phrase"
codex-search --clear-cache
```

Recaps live in the same private cache under `recaps/`, keyed by UUID, normalized
dialogue digest, model and recap-format version. Tool-only or metadata-only
changes do not invalidate a recap. Atomic writes and per-UUID generation locks
prevent duplicate concurrent generation. The worker snapshots bounded dialogue
under the main index lock, then releases it before inference. A result for older dialogue cannot overwrite newer
evidence. Deleted source UUIDs lose their recap during maintenance.

Clear removes this home's indexed text, recap data and manifest, retaining stable lock files and maintenance metadata to prevent concurrent lock races. An in-flight result cannot recreate a cache that was cleared or removed during its run. The next search rebuilds. A cache-format version change or corrupt manifest also triggers a rebuild. Metadata-preserving edits can evade stat comparison; use `--rebuild-index` if necessary. First indexing needs time and disk space for decoded text; broad patterns scan all matching lines even though display snippets are capped.

## Verification and rollback

All committed test messages are synthetic. Run these focused checks from the repo:

```bash
python3 -m unittest discover -s tests -p 'test_codex_search*.py'
bash tests/scripts/executable_codex_test.sh
git diff --check
```

A disposable live fixture also exercises ordinary printing and the real picker:

```bash
python3 tests/scripts/codex_search_live_check.py
python3 tests/scripts/codex_recent_live_check.py
python3 tests/scripts/codex_recap_isolation_check.py
python3 tests/scripts/codex_search_live_check.py --real-resume
```

The isolation fixture uses the actual CLI with an invented local configuration
and a localhost-only provider that deliberately rejects its sole request. It
verifies effective tool exposure and a disabled MCP canary with zero upstream
model calls. For an explicitly chosen single live synthetic recap using the
current login/model, run `python3 tests/scripts/codex_recap_live_check.py --live`;
this consumes normal account allowance and must not be repeated as a batch.

The recent fixture drives real fzf in a disposable PTY with deterministic local
recap subprocesses. Its progress case uses the real SummaryManager and private
cache, replacing only the external runtime. It checks visible timer ticks,
queue-to-generation timer reset, Guardian/untitled title adoption, priority
reordering, query/UUID preservation, Ctrl-G, selection and cancellation cleanup
without sending anything to a model. It exits 0 on success.

The Guardian priority fixture runs the actual selected CLI and its sibling
modules with disposable synthetic sessions. It replaces only the external
Codex runtime; the real SummaryManager, SessionWatcher and fzf handle the
append/title rename, changed activity/dialogue, urgent-to-complete regeneration
and reorder. It verifies the query and selected UUID survive, Enter sends the
exact UUID/directory to a resume stub, and background processes and temporary
runtime directories are removed. Cached and newest-first second opens use
`--no-summaries`, including Ctrl-G, with zero additional generation. Neither
command below reads private sessions or calls a provider. Run from the repo
root, without sudo; the second verifies installed code after refresh-config.

```bash
python3 tests/scripts/codex_priority_live_check.py --scenario all
python3 tests/scripts/codex_priority_live_check.py --command "$HOME/scripts/codex-search" --scenario all
```

Expected: Guardian evidence refreshes, complete moves below actionable, exact
resume/cleanup passes, and cached/recent opens report zero additional calls.

### Check best-effort picker startup

Use the disposable startup fixture to verify that the actual CLI reaches real
fzf before archive indexing finishes. It uses invented local sessions and no
provider calls. Run from `/home/example/linux-config`, without sudo. The default
scenario is `all`; select one case to repeat a specific startup condition.
After refresh-config, the installed invocation exercises installed sibling
modules. These expected results describe the synthetic checks, not observed
private-history timings.

```bash
python3 tests/scripts/codex_startup_live_check.py --scenario all
```

Expected: Cold, cached, malformed and locked-cache cases reach the picker using
available metadata, preserve exact selection/resume, and clean up workers.

```bash
python3 tests/scripts/codex_startup_live_check.py --scenario cold
```

Expected: Native metadata supplies initial rows before delayed older archive
work completes. Pending dialogue is visibly indexing; usable rows can be browsed.

```bash
python3 tests/scripts/codex_startup_live_check.py --scenario cached
```

Expected: Validated cached rows supply the initial UI, with exact UUID/directory
resume and no foreground full-index dependency.

```bash
python3 tests/scripts/codex_startup_live_check.py --scenario malformed
```

Expected: Good neighboring data remains usable, with no per-file warning flood.
Default summary stays concise; details retain bounded background diagnostics.

```bash
python3 tests/scripts/codex_startup_live_check.py --scenario locked
```

Expected: Another process holding the index lock does not prevent initial UI.
Enter resumes the selected UUID while the lock remains held; background work
is reaped.

```bash
python3 tests/scripts/codex_startup_live_check.py --command "$HOME/scripts/codex-search" --scenario all
```

Expected: The same startup checks pass through the installed command and modules,
without provider calls or changes to private history.

For direct checks, run the following commands from `/home/example/linux-config`;
no sudo is needed. Expected-output blocks are examples, not captured results.
Titles, reasons, directories, UUIDs and timestamps depend on your local sessions.
Press Esc to close each picker; Enter resumes its highlighted session.

```bash
./scripts/executable_codex-search --recent --pick
```

Expected output:

```text
fzf lists urgent, actionable, unknown, waiting, then complete sessions.
Preview: priority, reason, freshness and recap. Queued/generating timers tick.
```

Keep this picker open, filter by a stable directory and highlight a session.
Continue that session or let Guardian update its title/dialogue in another pane.
The updated evidence and order appear after background discovery/inference;
the query and highlighted UUID remain stable while still matching.

```bash
./scripts/executable_codex-search --recent --pick --sort recent --no-summaries
```

Expected output:

```text
fzf lists newest recorded activity first and refreshes local source changes.
Cached recaps remain visible. Uncached generic rows show [recaps off].
No model calls; Ctrl-G generates nothing.
```

```bash
./scripts/executable_codex-search --recent --sort priority --details --limit 5
```

Expected output:

```text
At most five full session blocks, ordered by cached priority then activity.
Priority and its reason are visible; stale or missing priority is labelled.
No model calls.
```

```bash
./scripts/executable_codex-search --recent --sort recent --limit 5
```

Expected output:

```text
At most five sessions, newest recorded activity first. No model calls.
```

```bash
./scripts/executable_codex-search --recent --pick --summary-count 0
```

Expected output:

```text
No automatic inference. A missing generic row shows [Ctrl-G].
Press Ctrl-G: queued/generating progress, then an AI headline and priority.
```

```bash
./scripts/executable_codex-search --recent --pick --no-summaries
```

Expected output:

```text
Cached priority determines order; missing, legacy or stale priority is unknown.
Local updates refresh the picker. No model calls or generation timers.
Press Ctrl-G, then Esc: nothing is generated or resumed.
```

The search and recent-picker fixtures accept `--fzf /absolute/path/to/fzf`
for a temporary trusted binary. `codex_search_live_check.py` uses a resume stub;
adding `--real-resume` opens synthetic history in the installed Codex CLI using
a localhost-only provider. Inspect `/status`, then exit without
sending a prompt. No private history is copied. Codex may warn about helper
binaries under `/tmp` and may append lifecycle data to its own synthetic log.

Follow the grouped [smoke tests](smoke-tests.md#codex-session-search) for ordinary printing, tool opt-in, incremental refresh, cancellation and interactive resume. `/status` is a local UI command; confirm the selected directory without sending a new prompt. Evidence, measured timings and remaining interactive checks are maintained in the [original implementation plan](../plans/codex-session-search.md),
[recent-session plan](../plans/codex-recent-sessions.md),
[priority and Guardian-refresh plan](../plans/codex-session-priorities.md) and
[best-effort startup plan](../plans/codex-picker-best-effort-startup.md).

To roll back only recent browsing, run `codex-search --clear-cache`, restore
this change's hunks in `scripts/executable_codex-search`, remove the four new
`scripts/codex_search_*.py` modules and the `crg` addition, then run the protected
`refresh-config` workflow to reinstall the previous command. Remove only these
new installed module files if chezmoi retains them. Preserve `csg`, ordinary
search and all unrelated dirty edits. The previous command rebuilds its cache;
original session files stay unchanged. To restore full search display without
removing features, use `--details --limit 0`.
