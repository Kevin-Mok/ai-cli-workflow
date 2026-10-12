# Imported skill source-tree execution failure

Run imported skill commands from their installed paths, because chezmoi source filenames can differ from Python import names. The package bytes are intact and the installed CLI loads successfully.

## Symptom and impact

Running python3 -B dot_agents/skills/last30days/scripts/last30days.py --help exited 1 with ModuleNotFoundError: No module named lib.private_files. This affected the source-tree verification command, not the installed package.

## Lookup and diagnosis

Searched tracked postmortem-memory for chezmoi source executable private python import. No exact prior finding was established for this filename collision. chezmoi source-path resolves the installed scripts/lib/private_files.py to scripts/lib/literal_private_files.py: literal_ escapes the reserved chezmoi private_ prefix. Direct source-tree execution therefore cannot import the original module name.

## Resolution and verification

Correct the verification surface to the actual installed package; do not rename upstream modules or break chezmoi mapping. python3 -B /home/example/.agents/skills/last30days/scripts/last30days.py --help exited 0 with full usage output. Every one of the 157 package files matched its rendered source SHA-256. No package implementation fix is needed.

## Learning and limits

No new reusable learning recorded in the ledger: this is a verification-surface mistake already covered by the policy to exercise installed entrypoints. The plan now explicitly uses the installed path. Research and external source authentication were not exercised.
