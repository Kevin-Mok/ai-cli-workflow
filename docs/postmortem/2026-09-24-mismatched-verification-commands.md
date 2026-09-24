# Mismatched verification commands

## Symptom and impact

Repository inspection/verification used an incorrect path and language tool:
the refresh function was first sought at a nonexistent script path, and `bash -n`
was run against a Python helper. The test-writing skill's referenced companion
file and generic test configuration paths were also absent from this repo. The
README skill was initially sought under the repo's `.agents` directory rather
than the installed user skill path. Two later documentation patches had stale
context and were rejected without changing files. These attempts did not change
product state; they delayed final checks.

## Evidence and root cause

The repository stores `refresh-config` as a Fish function at
`dot_config/fish/functions/refresh-config.fish`. The i3 now-playing helper is
Python, so `bash -n` reported a syntax error at its Python tuple declaration.
The rejected patches expected wording that no longer existed after earlier
documentation updates. The missing companion/config files reflect this repo's
layout. The README skill lookup used the wrong root. These mistakes came from
assuming paths and patch context before checking them.

## Resolution and verification

Use the tracked Fish function path for refresh workflow review and validate the
helper with Python's AST parser. The now-playing suite passed all 36 tests, the
Spotify and desktop layout regressions passed, and Python AST validation plus
`git diff --check` exited 0. The full refresh completed; its log and installed
helper comparison passed. The earlier adjacent check chain had stopped at the
mismatched syntax command and was rerun successfully with the proper validator.

## Follow-up

Select syntax checks from the target file's declared language and inspect the
tracked helper path and current documentation context before invoking tools.
No product state or unrelated tracked files were changed by the failed checks.
