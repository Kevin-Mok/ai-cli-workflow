# Task: Public History Sanitization

This task rewrites the copied dotfiles repository so it can be published without exposing secrets or personal information. It inventories and sanitizes all reachable Git history, preserves safe provenance, adds public setup guidance, proves the result clean, removes the private remote, and writes a redacted external report without pushing.

## Request

Sanitize `/home/example/ai-cli-dotfiles-public`, a copy of a private chezmoi dotfiles repository, across every retained commit. Sensitive material includes credentials and keys; auth, session, cookie, browser, and history data; contact and location data; other people's names; network/private URL details; employer/client information; and personal notes.

## Constraints

- Preserve as many original commits, messages, authors, dates, and ordering relationships as safely possible.
- Prefer placeholders or chezmoi variables over deletion; remove only irreducibly unsafe file classes and drop only commits that become empty.
- Audit with available dedicated scanners plus independent manual/pattern review.
- Scrub commit messages and Git identities as well as trees/blobs.
- Keep the MIT license.
- Add `.gitignore` coverage for local-only files and README guidance for supplying personal values.
- Never push. Remove `private-origin` after verification.
- Touch no other project or user configuration. `/tmp` may hold the requested report and temporary protected/audit material needed for a safe atomic rewrite.
- Never reproduce a sensitive value in tracked docs, chat, logs intended for handoff, or the external report.

## Deliverables

- Rewritten Git history and retained public-safe branches in `/home/example/ai-cli-dotfiles-public`.
- Updated `.gitignore`, `README.md`, `plans/public-history-sanitization.md`, and task/status/incident documentation.
- Evidence table at `.harness/public-history-sanitization/checks.md`.
- Current handoff at `.harness/public-history-sanitization/progress.md`.
- Final redacted report at `/tmp/ai-cli-dotfiles-public-REPORT.md`.

## Observable Acceptance Criteria

1. Full-history scanners and manual review find no confirmed sensitive content in any retained commit, message, identity, ref, reachable object, or remaining local Git object.
2. The final report records original versus rewritten counts and any explained delta without revealing discovered values.
3. Every finding category is mapped to replacement, templating, safe placeholder, or path removal, with rotation advice and uncertainty listed.
4. Safe original message text, primary authorship, dates, topology, and order are preserved; only empty rewritten commits disappear.
5. The existing MIT license remains.
6. `.gitignore` covers local-only state and README explains how to supply private values outside version control.
7. Protected pre-existing media are classified before publication; any rejected paths and their LFS payloads are absent from all retained history and local object storage.
8. `private-origin` and all other remotes are absent; no push occurred.
9. Original refs, reflogs, backup refs, raw rules/findings, and unreachable sensitive objects are absent from the completed copy.
10. An evidence reviewer reports no incorrect completion claim; unresolved uncertainty remains explicit.
