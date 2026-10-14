# Rewrite Clone Missing Archival Objects

This incident records why the first isolated rewrite-clone setup stopped before sanitization. A normal clone copied the local `main` history but not objects reachable only through the source repository's remote-tracking refs; archival refs must be fetched from the already verified all-ref bundle.

## Symptom

Creating the first local archival branch in the temporary clone failed with `update_ref` because its target object did not exist in that clone.

## Impact

- No history filtering started.
- The original repository, refs, index, worktree, and remote were unchanged.
- The temporary clone is incomplete and will be removed before retry.
- The mode-restricted private bundle was successfully created and verified before the failure.

## Evidence

- The source has 698 commits across local and remote-tracking refs but only 689 on `main`.
- The ordinary clone followed local branch refs and did not transfer remote-tracking-only objects.
- The failed OID is reachable from a source remote-tracking ref and is covered by the verified `--all` bundle.

## Prior-Knowledge Lookup

- Query: `git clone local source remote-tracking ref nonexistent object update-ref bundle all refs`.
- Matches: reviewed fetch-before-ancestry guidance applies directly; an advertised or recorded object must be fetched before ref or ancestry operations. Fixture-stage guidance also supports proving prerequisites independently.
- Decision: fetch the complete remote-tracking namespace from the verified bundle into safe local archival branches instead of writing refs from absent OIDs.

## Root Cause

The preparation script assumed `git clone` would copy every object reachable from all namespaces in the source. Standard clone behavior copied advertised local branches, not the source's remote-tracking-only object closure.

## Current Status

Resolved before filtering.

## Resolution And Verification

The corrected setup fetched every archival tip from the verified all-ref bundle
into neutral local heads and reported all 698 original commits before filtering.
The completed sanitized graph retains every safe unique branch history on 18
public-safe heads.

## Follow-Up

- Treat ref creation and object transfer as separate prerequisites.
- Keep the original repository untouched until the isolated clone proves full commit coverage.
- The shared postmortem-memory ledger remains outside the authorized folder and is intentionally untouched.
