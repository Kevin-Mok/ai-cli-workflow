# Staged File-Size Guard

The guard keeps authored files manageable by checking Git's staged bytes. Stage
an edit, run the guard, and split any blocked module by responsibility before
committing. No new dependencies are needed: it uses the existing Python 3 and Git.

## Rules

- Estimated tokens are exactly bytes / 4; the limit is 20,000 bytes (5,000 tokens).
- New files above the limit are blocked. Existing files above the limit may
  stay the same size or shrink; any growth above the limit blocks the commit.
- Partial staging uses index blobs, never working-copy content. Deleted files,
  symlinks and submodules are ignored. Detected renames use the original HEAD
  blob as their baseline; an undetected rewrite/rename is conservatively new.
- Every blocked file shows tokens, growth in tokens/bytes, and the minimum
  split count: ceil(bytes / 20,000).

Run `python3 -B scripts/file_size_guard.py` to check the current index; success
is silent. `--plain` (or `CLI_PLAIN=1`) removes decorative output. `--report`
counts eligible tracked HEAD blobs and prints the ten largest; it does not
include unstaged edits. Exit codes: 0 allowed/report, 1 blocked, 2 inspection error.

## Commit hook installation

The existing [public privacy gate](../README.md#local-pre-commit-privacy-gate)
remains authoritative. The size installer preserves an executable regular
pre-commit hook as `pre-commit.file-size-previous`, then runs it before checking
staged sizes. Its failure stops the commit; any index changes it makes are
included in the size check. Install the privacy gate first when enabling both.

To opt in, run `python3 -B scripts/install_commit_hook.py` from the checkout
root; `--plain` (or `CLI_PLAIN=1`) selects ASCII output. Exit 0 means
installed/already matching; exit 1 means refused or failed. The installer
symlinks only `pre-commit` into the common Git hooks directory, preserving
pre-push/git-lfs hooks and never setting `core.hooksPath`. It refuses a configured
`core.hooksPath`, an existing symlink, a non-executable hook, or a conflicting
backup. Resolve those locally without overwriting existing protections.

Linked worktrees share that hooks directory. Installation therefore affects all
of them; keep the source checkout available. The hook runs the guard in the
checkout being committed, which must contain the guard and config. To roll back,
remove only the installer-created pre-commit symlink and rename the preserved
`pre-commit.file-size-previous` back to `pre-commit` when present. Undo wrapper
installations in reverse order; do not remove the privacy bundle or its backups.
Nothing is installed by cloning or running the tests/smoke. Live installation
is an explicit local action and is not performed by this change.

## Exemptions

Edit only [config/file-size-guard.json](../config/file-size-guard.json).
`skip_globs` uses case-sensitive Python fnmatch patterns against the full path
and each nested suffix (so `data/*` also matches nested data directories).
Defaults cover lockfiles, minified/maps, generated/dependency/build/data trees,
benchmark run output, vendored benchmark candidates and known upstream assets.

`grandfathered_max_bytes` maps exact existing paths to reviewed integer byte
ceilings (at least 20,000). It permits growth only up to that finite ceiling;
new files still use 20,000 bytes even if named in the map. Existing oversized
files can always stay the same size or shrink. Freeze each exception to the
reviewed file size and ratchet it down when practical; avoid wildcard exclusions
for authored files. The HEAD report still counts these files above 20,000 bytes.

`upstream_markers` recognizes staged regular provenance/license files. SOURCE.md
exempts its non-root directory; license-only detection is limited to directories
matching `upstream_globs` (skill and benchmark upstreams). Root or authored app
licenses do not exempt code. `generated_markers` recognizes comment-header
notices in the first 2,000 staged bytes, excluding quoted generator strings.
Configured binary extensions, NUL bytes in the first 8,000 bytes, staged `-diff`
attributes, and staged LFS attributes/pointers are skipped. These are heuristics; misleading markers
or broad globs can exempt authored code, so review config changes carefully.
The report uses HEAD contents and attributes (Git 2.43+ for `--report`).

## When blocked

Group by responsibility. Keep each new module under 5,000 tokens, move code
verbatim, leave the original as a thin re-exporting entry point, then run tests.
The split count is a lower bound; cohesive boundaries may require more files.
Split authored modules rather than adding broad exemptions. Named legacy documentation ceilings require an explicit review of the final byte count.

## Verification

`python3 -B -m unittest tests.test_file_size_guard -v` exercises real temporary
Git repositories: new files, grandfathered shrink/growth, exact threshold,
partial staging, unusual paths, deletions, renames and exemptions.

`python3 -B scripts/smoke_file_size_guard.py --plain` demonstrates block/allow
results and preserved privacy-hook enforcement in a disposable local repository without changing this checkout.
