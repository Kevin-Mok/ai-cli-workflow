# Recent-session picker source lookup failure

This report records a failed public fzf reference lookup during the recent-session
picker investigation. Use the installed package documentation to verify supported
behavior, then validate selection preservation with synthetic terminal probes.

## Symptom and impact

On 2026-10-07, attempts to read the guessed upstream tag paths
`https://raw.githubusercontent.com/junegunn/fzf/v0.44.1/man/man1/fzf.1` and
`https://raw.githubusercontent.com/junegunn/fzf/v0.44.1/src/terminal.go`
returned HTTP 404. Research was delayed; no product command, private session,
inference request, or source-session mutation occurred.

## Lookup and evidence

Read the tracked postmortem-memory skill, then searched `source 404` before
alternate retrieval. The matching `local-current-source-retrieval` finding in
`references/external-access-deployment.md` applies: a guessed path failing does
not establish missing functionality; installed-version evidence takes priority.

The installed `~/.local/bin/fzf --version` returned `0.44.1 (debian)` with exit 0.
Its `--help` returned exit 0. The existing extracted package documentation at
`/tmp/codex-search-fzf/usr/share/man/man1/fzf.1.gz` was readable, and the same
manual was read directly from the retained Ubuntu package without extraction.
It documents `--track`, `--listen`, authenticated actions, `reload-sync`,
`refresh-preview`, `execute-silent`, `load`, and `focus` events.

## Root cause, resolution, and follow-up

The research relied on unverified version-tag URLs. Their absence was confirmed;
the upstream tag layout was not investigated further. Local packaged primary
documentation supplied the needed installed-version contract, resolving the
lookup obstacle without further network requests. Synthetic runtime probes must
still establish the semantics of changing-row selection preservation; manual
presence alone does not prove that behavior.

Status: verified workaround for source retrieval. No new reusable learning:
`local-current-source-retrieval` already covers failed guessed public paths and
installed-runtime fallback. Register this report's reviewed hash with that
explicit decision and run its targeted coverage check.
