# Directory sizes

Inspect allocated disk usage with one Dust scan and a nested directory report. Install the pinned backend, choose a target and display depth, watch provisional indexing counts, then read the completed report. This wrapper improves feedback during long scans; benchmarks here do not show faster completed scans.

## Setup and usage

Requires Linux, Python 3, and [Dust](https://github.com/bootandy/dust) (tested version 1.2.6). The setup helper also needs [GitHub CLI](https://cli.github.com/) and network access. It downloads the pinned Linux x86_64/aarch64 MUSL release using GitHub's release API and installs into an explicit writable prefix. It needs no sudo, extracts only the regular executable, and refuses to overwrite an existing installation.

From the repository root:

```bash
./scripts/executable_setup-directory-sizes --prefix /tmp/directory-sizes-tools
./scripts/executable_directory-sizes --backend /tmp/directory-sizes-tools/bin/dust --depth 1 /mnt/usb-8tb/sys-backup/10-06-26.incomplete
```

The `/tmp` installation is disposable. For persistent setup, run the same helper with `--prefix "$HOME/.local"` and add `$HOME/.local/bin` to your PATH. If `dust` is already on PATH, omit `--backend`. The script follows the repository's `scripts/executable_*` convention; after normal chezmoi deployment its name is `~/scripts/directory-sizes`.

```bash
./scripts/executable_directory-sizes --depth 2
./scripts/executable_directory-sizes --threads 1 --depth 2 -- '/path/with spaces'
./scripts/executable_directory-sizes --depth 1 -- ./-leading-dash-directory
./scripts/executable_directory-sizes --json --depth 2 /path/to/directory
./scripts/executable_directory-sizes --apparent-size --depth 2 /path/to/directory
```

These PATH-based examples require installed Dust. No target defaults to home or root: omitting the target scans the current directory. If your current directory is home/root, explicitly choose a smaller target. `--depth 0` displays only the root; `--depth 1` adds immediate directories. **All descendants are still scanned.** `--threads` defaults to at most eight; try one on rotational storage, where concurrent seeks can be slower. `--help` describes every option. Target directory symlinks are rejected; pass the real directory explicitly.

Readable output aligns binary sizes and quotes names so spaces, newlines, dash prefixes and terminal controls stay distinguishable. Paths in results are relative to the target shown on stderr. JSON contains Dust's selected tree, with byte-size strings such as `"4096B"`, escaped names and children. Siblings retain Dust's size ordering. A root row is the total, not a sum to add to all descendant rows.

## Progress and completeness

The wrapper supplies initial status on stderr, then relays Dust's provisional `Indexing`/`Preparing` counts at most once per second. These counts are useful scan feedback, **not completed directory totals**. Small scans can finish before a progress tick. Results are buffered outside the target and published to stdout only after successful backend completion and validation. No shell, deletion UI, source cache, or persistent scan database is used; each invocation starts one backend scan. Backend configuration is replaced with an empty temporary TOML file so local filters cannot quietly change accounting.

Dust may exit zero after permission/other scan errors. The wrapper captures every non-progress stderr record, prints the diagnostics, returns nonzero, and withholds stdout. Ctrl-C returns 130; SIGTERM returns 143. Both terminate and reap the backend, without publishing incomplete totals. A bounded operator probe can use:

```bash
timeout --signal=TERM --kill-after=5s 20s ./scripts/executable_directory-sizes --backend /tmp/directory-sizes-tools/bin/dust --depth 1 /mnt/usb-8tb/sys-backup/10-06-26.incomplete
```

Timeout exit 124 means the bounded probe did not complete. Dust's metadata helper can silently omit an entry that disappears or cannot be stat'ed, so absence of diagnostics does not establish an atomic snapshot or complete visibility of a changing tree. Use a stable tree and GNU du cross-check when exact accounting matters. The wrapper's success footer says “without reported errors”; it does not claim filesystem consistency. Reading directory metadata may update filesystem access times according to mount policy, as with GNU du; the scripts issue no source writes.

## Accounting and backend choice

Primary docs and tagged source were researched with `gh api`, including current release options:

| CLI | Allocated accounting and scanning | Presentation / installation | Decision |
| --- | --- | --- | --- |
| [Dust 1.2.6](https://github.com/bootandy/dust/releases/tag/v1.2.6) | Parallel; includes directory allocation; inode/device hardlink dedup | Directory-only nested depth report, JSON, stderr indexing progress; prebuilt Linux release | Selected; simplest matching nested report, with wrapper error gate |
| [gdu 5.38.0](https://github.com/dundee/gdu/releases/tag/v5.38.0) | Parallel and sequential modes; deliberately excludes directory allocation | Nested TUI, progress and noninteractive depth; prebuilt Linux release | Directory-accounting difference and hidden depth-output error markers add complexity |
| [dua 2.45.1](https://github.com/Byron/dua-cli/releases/tag/v2.45.1) | Parallel; tracks traversal errors and reports failure status | TUI and aggregate depth; aggregate includes file rows; progress requires stderr TTY; prebuilt Linux release | Good alternative, but directory-only reporting needs more adaptation |

Dust's [accounting source](https://github.com/bootandy/dust/blob/v1.2.6/src/platform.rs), [traversal](https://github.com/bootandy/dust/blob/v1.2.6/src/dir_walker.rs), [error handling](https://github.com/bootandy/dust/blob/v1.2.6/src/main.rs), and [progress](https://github.com/bootandy/dust/blob/v1.2.6/src/progress.rs) establish the material semantics:

- Allocated default uses `st_blocks × 512`, including directories. Sparse file holes consume no allocated bytes. Extremely over-preallocated files can differ from GNU du because Dust caps reported allocation above rounded logical size plus `blksize × 65536`; this backend behavior is retained.
- Allocated hardlinks count once by inode/device. Different traversal order can attribute a shared inode to different subdirectories, while the root total agrees on ordinary stable fixtures.
- Symlinks are not traversed. A link to a directory can appear as a directory row, but its size is the link's allocation, not the target's contents. Broken links are retained in accounting.
- Optional **logical** mode counts every hardlink name and includes directory `st_size`. GNU `du --apparent-size --count-links` counts each link name but **omits directory sizes**. Thus the fixture comparison adds known directory metadata sizes to that logical comparator; it does not conflate logical and allocated bytes. Logical mode can greatly overstate sparse-file disk usage.

[gdu directory accounting](https://github.com/dundee/gdu/blob/v5.38.0/pkg/analyze/file.go), [gdu depth output](https://github.com/dundee/gdu/blob/v5.38.0/stdout/stdout.go), [dua aggregate traversal](https://github.com/Byron/dua-cli/blob/v2.45.1/src/aggregate.rs) and [dua exit handling](https://github.com/Byron/dua-cli/blob/v2.45.1/src/main.rs) support the comparison. Interactive navigation and scan progress are distinct from a completed sorted result; this wrapper supplies progress and a final static nested report.

## Verification and measurements

On 2026-10-08, nine focused tests passed using the installed Dust release. Fixtures cover nested/empty directories, ordinary and sparse files, hardlinks, directory and broken symlinks, unusual names, invalid inputs, missing dependencies, nonzero/diagnostic backend completion, and interruption of both wrapper and benchmark harness. Allocated fixture totals match GNU du exactly. Logical totals exceed GNU du's equivalent hardlink comparator by exactly the three known directory metadata sizes (12,288 bytes). A separate real-Dust permission fixture at uid 1000 returned 1 with zero stdout and a path-specific permission diagnostic.

Commands, from the repository root:

```bash
DIRECTORY_SIZES_REAL_BACKEND=/tmp/directory-sizes-tools/bin/dust python3 -B tests/test_directory_sizes.py
python3 -B tests/scripts/directory_sizes_benchmark.py --backend /tmp/directory-sizes-tools/bin/dust --output /tmp/directory-sizes-results.json
```

For an explicitly requested real probe, add `--reference /mnt/usb-8tb/sys-backup/10-06-26.incomplete` to the benchmark command. This adds exactly one 20-second run each for wrapper allocated, GNU du allocated plus sorting, and the user's separate logical plus sorting baseline. It terminates and reaps processes, including if the harness is interrupted. Do not automatically repeat real probes to chase better numbers.

[Saved measurements](directory-sizes-benchmark.json) use Dust 1.2.6 and GNU du/sort 9.4. The fixture has 30,000 1KiB files, 120 two-level branches, an empty directory, a 512MiB sparse file, one hardlink and one directory symlink; display depth is two. Three repetitions rotate command order. Metadata is warm from fixture creation, OS caches are uncontrolled, and caches were never dropped.

| Fixture command | Completion seconds, three runs | Median first completed output |
| --- | --- | --- |
| Final wrapper, 8 threads | 0.2554 / 0.2514 / 0.2493 | 0.2452 s |
| Dust directly, 8 threads, progress disabled | 0.1603 / 0.1659 / 0.1908 | 0.1643 s |
| `du -d 2 -h` piped to `sort -h` | 0.0942 / 0.0855 / 0.0830 | 0.0841 s |

The wrapper's initial status appeared in 0.040–0.044 seconds; those runs finished before meaningful indexing feedback. GNU du completed faster on this fixture. Runtime includes startup, output processing and cleanup, not an isolated metadata-walk timer.

The real tree is ext4 on rotational USB `/dev/sdd1`, mounted at `/mnt/usb-8tb` (7.3T disk). Each command ran once with uncontrolled caches, sequentially in the order below. This is neither a cold-cache trial nor proof of the bottleneck. The reference scan preceded the final JSON text renderer and descriptor-cleanup refactor; its scanner, thread count, timeout, progress and allocated accounting were the same. Only disposable fixtures were remeasured after those changes.

| Reference command, depth 1 | Observation at 20-second limit |
| --- | --- |
| Wrapper, allocated, 8 threads | Initial status 0.0402 s; meaningful indexing feedback 0.2414 s; zero stdout; incomplete, wrapper exited 143 after cleanup (20.2645 s total) |
| `du -d 1 -h` plus `sort -h`, allocated | Zero stdout/stderr; incomplete; both processes terminated and reaped (20.0323 s total) |
| `du -d 1 -h --apparent-size` plus `sort -h`, logical baseline | Zero stdout/stderr; incomplete; both processes terminated and reaped (20.0022 s total) |

The final observed Dust progress was 557,700 indexed files and a provisional 493GiB, **not a complete total**. No permission or vanished-entry diagnostic was observed during the bounded probes; backend diagnostics may appear only at scan completion, so access completeness and tree stability remain unknown. No source reads used sudo, and no backup data, permissions, or caches were changed. No total-speed comparison is possible on this unfinished reference tree.

The broader `python3 -B tests/test_postmortem_memory.py` run passed 25/26 tests; `WorkflowTest.test_actual_ledger_reference_status_and_coverage` failed on existing unregistered `.worktrees` report aliases. Targeted checks for all task incident reports pass. No tracked configuration files changed, so `refresh-config` was not required; scripts, tests, docs and reviewed knowledge are the task changes.

## Review and handoff

The [atomic plan](../plans/fast-directory-sizes.md) records RED/GREEN evidence and rollback boundaries. Run the focused tests above, then the [manual smoke checks](smoke-tests.md#directory-sizes). To hand this work to Cursor, paste: “Review scripts/executable_directory-sizes and executable_setup-directory-sizes against docs/directory-sizes.md and plans/fast-directory-sizes.md. Preserve all pre-existing dirty work, run tests/test_directory_sizes.py with the pinned Dust backend, inspect benchmark cleanup, and do not repeat real backup scans, commit, or push without a request.” Suggested future commit subject: `feat(scripts): add guarded Dust directory size reports`. Nothing was committed or pushed in this task.
