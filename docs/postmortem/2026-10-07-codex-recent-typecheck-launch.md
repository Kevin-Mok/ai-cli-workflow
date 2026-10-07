# Cached Pyright launch did not locate its bundled typeshed

Directly launching a cached Pyright JavaScript entrypoint did not locate standard-library stubs. Locate the package's typeshed before treating those diagnostics as application defects.

- Date: 2026-10-07.
- Symptom: Type check exited 1 with 1675 errors and 17 warnings, beginning with missing builtins/sys and undefined standard types in Python's own typing modules.
- Impact: No useful typing verdict yet; no source mutation or runtime failure.
- Evidence: Cached JavaScript entrypoint was invoked directly because pyright/mypy/ty were absent from PATH. Python unit tests run normally.
- Lookup: `pyright typeshed builtins missing`; compare any returned guidance with the missing standard-library diagnostics before retry.
- Root cause/status: The direct cached entrypoint did not resolve its fallback typeshed automatically. Passing its existing `pyright/dist/dist/typeshed-fallback` via `--typeshedpath` restored useful analysis. The remaining 14 project diagnostics were optional-value narrowing gaps; explicit guards for PIPE handles, validated roles/index entries and resolved model/runtime removed them.
- Verification: Fresh scoped Pyright with the explicit bundled typeshed exits 0 with zero errors, warnings or information messages. All 89 search tests pass. No type-checker dependency was installed and no diagnostics were suppressed.

## Installed verification fixture correction

A source-text abbreviation check unexpectedly failed with `cs` count2. Existing
generated aliases contain two definitions; source occurrence count is not the
effective Fish expansion. The first `abbr --show crg` attempt also printed the
full inventory because this installed Fish does not filter show output by that
argument. No production alias behavior changed. The corrected read-only check
captures `fish --no-config` output privately, parses only crg/csg/cs, and verifies
final effective values: recent picker, ordinary search, and terminal clear.
Installed recent listing from `/` then passed with synthetic UUID/directory and
unchanged source. No reusable product change is warranted; keep validation tied
to effective runtime state and use filtered captures for verbose tools.
