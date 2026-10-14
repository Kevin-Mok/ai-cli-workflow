# Restored Markdown Had Extra EOF Blank Lines

This postmortem records a staged formatting check failure after public-tip documentation was restored from its temporary safety copy.

## Symptom

`git diff --cached --check` reported an extra blank line at EOF in ten restored Markdown files.

## Impact

The staged snapshot was not ready to commit. The issue affected whitespace only; tests, audit evidence, and repository history were unchanged.

## Evidence

- Every diagnostic was `new blank line at EOF`.
- Direct tail inspection showed one empty line after the final content line in exactly the reported files.

## Current status

Resolved before commit.

## Root cause

The restored copies retained two terminal newline characters where the repository check expects a single final newline.

## Resolution

Normalize only terminal blank lines in the ten reported Markdown files, restage them, and repeat the staged whitespace check.

## Verification

After normalizing only terminal blank lines and restaging, `git diff --cached --check` exited successfully with no output.

## Follow-up

- Run `git diff --check` before staging large recovered documentation sets when practical.
- Preserve content bytes during safety backups, then apply repository formatting gates after restoration.
