# Archived repository rename blocked

This report records GitHub’s archived-repository restriction and the bounded recovery for a requested repository rename.

## Symptom and impact

The requested gh repo rename returned HTTP 403: Repository was archived so is read-only. The repository remained under its original name; no deletion or content change was attempted.

## Lookup and evidence

Read the tracked postmortem-memory workflow. Searched “Repository was archived so is read-only”; no specific applicable finding was identified. Before the attempt, the API confirmed the old repository was private and archived; gh repo rename --help confirmed the explicit repository selector and noninteractive flag.

## Resolution and verification

Temporarily unarchived the private old repository, renamed it to ai-cli-dotfiles-archived, and restored its archived state in a finally block. GitHub returned the same repository ID, 369691497, with private=true and archived=true. Three fresh API reads confirmed the new name/state, the old name resolving to the new name, and ai-cli-workflow remaining public and unarchived. Every recovery and verification command exited 0.

## Status and limits

Resolved with verified live recovery. No deletion, code migration, visibility change, or local remote change occurred. External clone configuration and browser redirects were not tested. No new repository-specific engineering finding: this was a one-off GitHub administration restriction; its exact recovery evidence remains in this report. No commit or push was requested.
