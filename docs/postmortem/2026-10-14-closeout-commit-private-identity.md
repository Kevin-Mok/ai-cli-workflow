# Closeout Commit Used A Private Git Identity

This postmortem records how the terminal all-object audit caught a private Git
identity in the final local documentation commit before publication.

## Symptom

The post-commit generic audit failed with one email-class finding in the newest
commit object. A field-level diagnostic that printed only match counts confirmed
that both the author and committer headers used an unsafe email domain; the
commit message had no finding.

## Impact

The newest local commit was not safe to publish. No push occurred, the tree
content remained clean, and the finding was limited to commit metadata.

## Evidence

- The all-object audit checked 691 commits and 5,191 unique blobs, then reported
  one email finding in the newest commit object.
- The diagnostic reported one unsafe-domain match in each identity header and
  zero matches in the message without printing either address.
- The current worktree scan, 11 focused tests, and README gate still passed.

## Current status

Resolved. The latest documentation commit is recreated with the established
public maintainer identity, then its replaced object is removed from reflogs and
the local object database.

## Root cause

The closeout commit command relied on ambient Git identity configuration. The
earlier public commits explicitly supplied the public-safe noreply identity, but
that requirement was not carried into this final follow-up commit.

## Resolution

Amend only the unpushed closeout documentation commit with an explicit public
author and committer identity and signing disabled. Expire reflogs immediately,
prune the replaced commit and its obsolete blobs, and rerun the audit over every
remaining object.

## Verification

- The amended commit has only the established public-safe identity and no
  email finding in its message or headers.
- The final all-object audit passes across 691 commits and 5,192 unique blobs
  with zero findings.
- Git reports no reflogs, unreachable objects, remotes, LFS paths, or local LFS
  payloads; the worktree is clean and no push occurred.

## Follow-up

- Every commit created during a history-sanitization task must set the approved
  public author and committer explicitly, even when repository defaults exist.
- Keep the terminal all-object scan after the last commit; a pre-commit blob
  scan cannot detect unsafe commit headers that do not exist yet.
