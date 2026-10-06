# Search and resume Codex conversations

Use `codex-search` to find words in saved user messages and assistant replies across projects. Search once to build a private local cache, repeat searches with ripgrep patterns, then copy the printed command or select a session with fzf to resume in its original directory.

## Install and use

Chezmoi installs [the executable source](../scripts/executable_codex-search) as `~/scripts/codex-search`. Run `refresh-config` after tracked configuration changes; it snapshots live Codex and Git config into tracked source, applies chezmoi, regenerates shortcuts and reloads fish abbreviations. Protect unrelated dirty source before that refresh. Python 3 and `rg` (ripgrep) must be on PATH. `fzf` is optional and only required by `--pick`. Running the tool requires no sudo. On the repo's non-GUI hosts, `.chezmoiignore` excludes scripts; invoke the source directly there.

If `--pick` reports that fzf is missing, the search command itself is working;
install the optional picker dependency or put a trusted `fzf` binary on PATH.
On example-user's desktop, fzf 0.44.1 is now installed at `~/.local/bin/fzf`, already
on the fish PATH. It was installed without sudo from the checksum-verified
Ubuntu package. Retry the same `codex-search --pick "pattern"` command.
This user-local binary is outside chezmoi/Git; other hosts still need fzf separately.

```bash
codex-search --help
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

## What is searched

Discovery recursively scans JSONL files under `${CODEX_HOME:-~/.codex}/sessions`; `session_index.jsonl` only supplies titles. Multiple source copies of a UUID produce one result. Default text consists of decoded user and assistant messages; mirrored event/message records do not duplicate snippets. Event-only historical logs also work. Recognized injected user context blocks, system/developer messages, reasoning, turn context, compaction summaries and binary attachments are excluded. An IDE's `## My request for Codex:` delimiter removes its context prefix. `--all-text` additionally searches known tool call/output records, including decoded JSON arguments, while retaining instruction exclusions.

`rg` matches decoded text with its own regex semantics. Matching is line-oriented; a pattern cannot span newlines. `-i` ignores case and `-F` treats the pattern literally. Other rg options are not forwarded. Ripgrep's personal config is ignored to keep these options predictable. Unknown record types are ignored; malformed records and incomplete JSONL tails are skipped with counts and source paths, without printing their private payloads.

Schema sources verified before implementation: [rollout wire format](https://github.com/openai/codex/blob/main/codex-rs/history/src/rollout_payload.rs), [session metadata and events](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/protocol.rs), [response messages and content](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/models.rs), and [append-only title index](https://github.com/openai/codex/blob/main/codex-rs/rollout/src/session_index.rs). The installed CLI's `codex resume --help` verified UUID and `-C` support. Current upstream main can differ from older sessions; unsupported legacy formats and archived/compressed logs outside sessions/**/*.jsonl are not indexed.

## Cache and refresh

The cache lives under `${XDG_CACHE_HOME:-~/.cache}/codex-search/<SHA256-of-resolved-Codex-home>`. It contains private decoded conversation/tool text and source metadata; keep it out of Git, shared storage and backups that should exclude private conversations. Directories are restricted to 0700 and files to 0600; unexpected symlinks or ownership are rejected. Search/indexing only reads original sessions and makes no network or model calls.

Every search compares source size, nanosecond modification/change times, device and inode. It reparses changed sources and removes deleted ones. Unchanged text files are reused. Parsing streams one JSONL record at a time, so memory scales with one record and per-session message digests rather than the full corpus. A file changed during parsing is marked for refresh next time. Atomic file replacement and a per-home flock serialize concurrent refresh/search/clear operations; the lock is released before fzf or Codex starts.

```bash
codex-search --rebuild-index
codex-search --rebuild-index -F "phrase"
codex-search --clear-cache
```

Clear removes this home's data and manifest, retaining the lock to prevent concurrent lock races. The next search rebuilds. A cache-format version change or corrupt manifest also triggers a rebuild. Metadata-preserving edits can evade stat comparison; use `--rebuild-index` if necessary. First indexing needs time and disk space for decoded text; broad patterns scan all matching lines even though display snippets are capped.

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
python3 tests/scripts/codex_search_live_check.py --real-resume
```

Use `--fzf /absolute/path/to/fzf` for a temporary binary. The first invocation
uses a resume stub; the second opens synthetic saved history in the installed
Codex CLI using a localhost-only provider. Inspect `/status`, then exit without
sending a prompt. No private history is copied. Codex may warn about helper
binaries under `/tmp` and may append lifecycle data to its own synthetic log.

Follow the grouped [smoke tests](smoke-tests.md#codex-session-search) for ordinary printing, tool opt-in, incremental refresh, cancellation and interactive resume. `/status` is a local UI command; confirm the selected directory without sending a new prompt. Evidence, measured timings and remaining interactive checks are maintained in the [implementation plan](../plans/codex-session-search.md).

To roll back, run `codex-search --clear-cache`, remove only the session-search executable and `csg` addition from chezmoi source, and remove the installed `~/scripts/codex-search` if chezmoi retains it after source removal. Run the same protected `refresh-config` procedure to regenerate abbreviations. Preserve other alias/doc edits. Original session files are unchanged and need no restoration. To restore the full display without removing the tool, use `--details --limit 0`. Reverting only the readability change requires no cache rebuild.
