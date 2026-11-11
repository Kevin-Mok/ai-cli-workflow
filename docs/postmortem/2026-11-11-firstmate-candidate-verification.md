# Firstmate candidate verification used an incomplete directory

Record a verification-root mistake while preserving the isolated session-only
commit and checking the complete immutable candidate before delivery.

## Symptom and impact

A delegated postmortem-ledger check used the changed-file overlay as its knowledge
root. It exited 2 and reported 304 missing reference documents per report. The
overlay intentionally contains only changed files, so those failures do not show
broken committed references. No repository or live agent state was changed.

## Cause and resolution

The manifest directory was confused with its shadow entry, which names a full
candidate tree exported using git archive. The exact exported path is available
in the candidate manifest directory's shadow file. Re-run against that full tree,
not an overlay or the mixed working tree. Native session and wrapper controls
are unrelated to this verifier error.

## Lookup, status and learning

The existing local-discover-paths-before-reads guidance applies: use the exact
inventoried artifact rather than guessing a verification root. No new generalized
rule is needed. Status: resolved verification-root error. The complete immutable-tree README
gate and both incident checks passed with no missing-reference errors. Retirement
and whitespace checks also passed. Candidate link review separately found baseline
README links to absent local audio files and a malformed fragment; those links
were replaced with the existing sound-configuration guide, preserving behavior.
