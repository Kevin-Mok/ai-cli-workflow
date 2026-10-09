# rintro abbreviation did not resolve as a command

The saved Voice Contributor shortcut failed in the user's existing fish shell. Add an autoloadable function and verify command resolution without abbreviations.

## Symptom and evidence

User invocation `rintro --text "Welcome back! Your changes are ready."` returned command not found. Live reproducer `fish --no-config -c 'rintro --help'` exited 127 before implementation. The installed Voice Contributor wrapper exists; only the abbreviation was defined.

## Impact and root cause

The shortcut relied on interactive abbreviation expansion and shell reload state. An abbreviation does not provide callable command resolution.

## Status and next steps

Resolved: added autoload function, updated usage docs and fish-alias skill. Six intro tests and 53 notification tests pass; refresh-config completed, deployed function exists, and normal fish command resolution returns usage with exit0. README gate passes. An isolated no-config fish omits the user function path; defining fixtures explicitly include their function directory. A discarded mock attempted to use reserved command as a function name; corrected defining tests failed solely for absent rintro before GREEN. A path search used unverified filenames and exited2; no source mutation resulted. Search finding local-shortcut-stored-text-verification concerns shortcut encoding; it does not establish command availability.

Lookup query: fish abbreviation command not found existing shell. Existing shortcut encoding guidance was reviewed; it does not cover callable resolution. New local engineering lesson and fish-alias guidance capture this distinction. Remaining limit: other shells use the full wrapper path.
