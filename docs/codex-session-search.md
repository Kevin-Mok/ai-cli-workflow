# Search and resume Codex conversations

Use `codex-search` to browse recent conversations or find words in saved user messages and assistant replies across projects. Refresh the private local index, inspect cached AI recaps or matching excerpts, then select a session in fzf to resume in its recorded directory.

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
fit the terminal width. `NO_COLOR=1` or `TERM=dumb` disables color. Long resume
commands stay complete so they can be copied. A footer on stderr announces any
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

`--recent` needs no pattern and sorts by the latest recorded session activity,
across all discovered directories. Creation time, source filesystem timestamps,
and recap-cache modification time do not determine order. Duplicate UUIDs follow
the existing newest-activity rule. Listing prints the newest 20 even in a pipe;
`--limit N` changes the count and `--limit 0` prints all. It reads cached recaps
without calling a model. `--recent` cannot be combined with a search pattern.
Recent browsing hides sessions without a saved title, `untitled` labels, and
titles beginning with `Guardian` (case-insensitive). This applies before limits
and automatic recap scheduling. These sessions remain available through pattern search.

`--recent --pick` opens fzf after discovery/index refresh, without waiting for
inference. All visible titled sessions appear regardless of `--limit`. Each row has
activity time, directory, title and cached recap headline/status. The preview
shows the goal, reported progress, current state and remaining work, or bounded
local user/assistant dialogue when there is no recap. Missing, generating, stale,
unavailable and partial recaps are labelled explicitly; a stale recap remains
visible as older evidence. AI recaps describe reported conversation state and
are not independent verification of completed work.

The newest 20 sessions form the default automatic batch. One worker visits them
newest first and skips current recaps. `--summary-count N` changes that newest-session
window; zero disables automatic work while keeping **Ctrl-G** available for the
highlighted session, including sessions outside the batch. Manual requests go
ahead of queued automatic work, after the active request finishes. Each eligible
UUID gets at most one attempt per opening. `--no-summaries` prohibits all model
calls, including Ctrl-G, while retaining cached recaps and local previews.

`--summary-model MODEL` overrides the configured model; otherwise the existing
Codex login and effective configured model are used. Recaps consume that account's
normal model allowance. Each attempt, including isolation preflight, times out after 120 seconds. Authentication
or rate/usage-limit errors stop the batch; other failures mark only that recap
unavailable and browsing continues. Reopen to retry. Exiting or resuming cancels
and reaps background work first.

Typing filters activity/directory/title, not changing recap text. The picker
freezes discovery order for that opening and updates recaps in place, preserving
the query and highlighted session. Reopen to discover new activity or sessions.
This uses fzf's local authenticated control listener; fzf 0.44.1 is verified.
Enter always resumes `codex resume -C DIR UUID`, with no initial prompt.

### How model runs are isolated

The worker supplies only the parser's decoded user/assistant dialogue as inert
data. Recognized injected context, developer/system instructions, reasoning and
tool records stay excluded. Each session supplies at most 32 KiB of UTF-8 dialogue,
preserving its opening and latest content. Long records may be clipped at either
boundary; omitted content marks the result partial. Output must contain exactly
five nonempty string fields (`headline`, `goal`, `progress`, `state`, `next_steps`)
and at most 150 whitespace-delimited words total; malformed output is discarded.

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

`rg` matches decoded text with its own regex semantics. Matching is line-oriented; a pattern cannot span newlines. `-i` ignores case and `-F` treats the pattern literally. Other rg options are not forwarded. Ripgrep's personal config is ignored to keep these options predictable. Unknown record types are ignored; malformed records and incomplete JSONL tails are skipped with counts and source paths, without printing their private payloads.

Schema sources verified before implementation: [rollout wire format](https://github.com/openai/codex/blob/main/codex-rs/history/src/rollout_payload.rs), [session metadata and events](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/protocol.rs), [response messages and content](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/models.rs), and [append-only title index](https://github.com/openai/codex/blob/main/codex-rs/rollout/src/session_index.rs). The installed CLI's `codex resume --help` verified UUID and `-C` support. Current upstream main can differ from older sessions; unsupported legacy formats and archived/compressed logs outside sessions/**/*.jsonl are not indexed.

## Cache and refresh

The cache lives under `${XDG_CACHE_HOME:-~/.cache}/codex-search/<SHA256-of-resolved-Codex-home>`. It contains private decoded conversation/tool text and source metadata; keep it out of Git, shared storage and backups that should exclude private conversations. Directories are restricted to 0700 and files to 0600; unexpected symlinks or ownership are rejected. Search, listing and indexing only read original sessions and make no network or model calls. Only the recent picker can start the explicitly controlled recap worker.

Every search compares source size, nanosecond modification/change times, device and inode. It reparses changed sources and removes deleted ones. Unchanged text files are reused. Parsing streams one JSONL record at a time, so memory scales with one record and per-session message digests rather than the full corpus. A file changed during parsing is marked for refresh next time. Atomic file replacement and a per-home flock serialize concurrent refresh/search/clear operations; the lock is released before fzf or Codex starts. Canonical role-labelled dialogue adds a third private per-source cache file and a content digest.

```bash
codex-search --rebuild-index
codex-search --rebuild-index -F "phrase"
codex-search --clear-cache
```

Recaps live in the same private cache under `recaps/`, keyed by UUID, normalized dialogue digest, model and recap-format version. Tool-only or metadata-only changes do not invalidate a recap. Atomic writes and per-UUID generation locks prevent duplicate concurrent generation; inference never holds the main index lock. Deleted source UUIDs lose their recap during maintenance.

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

The recent fixture drives real fzf in a disposable PTY with deterministic local recap subprocesses. It checks live previews, query/highlight preservation, Ctrl-G, selection and cancellation cleanup without sending anything to a model. It exits 0 on success.

The search and recent-picker fixtures accept `--fzf /absolute/path/to/fzf`
for a temporary trusted binary. `codex_search_live_check.py` uses a resume stub;
adding `--real-resume` opens synthetic history in the installed Codex CLI using
a localhost-only provider. Inspect `/status`, then exit without
sending a prompt. No private history is copied. Codex may warn about helper
binaries under `/tmp` and may append lifecycle data to its own synthetic log.

Follow the grouped [smoke tests](smoke-tests.md#codex-session-search) for ordinary printing, tool opt-in, incremental refresh, cancellation and interactive resume. `/status` is a local UI command; confirm the selected directory without sending a new prompt. Evidence, measured timings and remaining interactive checks are maintained in the [original implementation plan](../plans/codex-session-search.md) and [recent-session plan](../plans/codex-recent-sessions.md).

To roll back only recent browsing, run `codex-search --clear-cache`, restore
this change's hunks in `scripts/executable_codex-search`, remove the four new
`scripts/codex_search_*.py` modules and the `crg` addition, then run the protected
`refresh-config` workflow to reinstall the previous command. Remove only these
new installed module files if chezmoi retains them. Preserve `csg`, ordinary
search and all unrelated dirty edits. The previous command rebuilds its cache;
original session files stay unchanged. To restore full search display without
removing features, use `--details --limit 0`.
