# BTW shortcut inspection failures

This report records inspection errors while adding a file shortcut, and the safe deployment checks used to continue.

- Symptom: guessed script/function/catalog paths did not exist. A normal fish inspection also ran startup hooks that attempted writes outside the sandbox (fnm multishells, universal variables and generated aliases).
- Approval review: combined staging/commit/push was initially refused for unclear scope authorization. The explicitly invoked skill authorizes focused shortcut/docs commit and push. A safer stage-only request citing that authorization was approved; exact staged review excludes unrelated work.
- Additional evidence: initial Git staging was denied creating `.git/index.lock` in the read-only Git metadata mount. No index changes occurred; authorized Git delivery must use approved filesystem access.
- Impact: diagnostic noise and delay; no shortcut command was executed.
- Evidence: missing executable_refresh-config, sync-shortcuts.fish and .config/chezmoi/aliases/key_files; startup reported read-only filesystem errors. The tracked refresh-config.fish was readable.
- Lookup: searched `No such file directory guessed script path`; `local-discover-paths-before-reads` applies directly. Inventory paths first, and use no-config fish for isolated inspection.
- Cause: assumed entrypoint locations and used normal shell startup for a read-only lookup.
- Resolution: use discovered source paths, avoid normal startup for inspection, and request authorized filesystem access for actual refresh.
- Status: inspection workaround verified: tracked function and generator source reads succeeded. Scoped refresh-config completed and the installed interactive abbreviation checker passed, without executing the editor. Git delivery uses approved filesystem access.
- Learning: no new reusable guidance; existing path-discovery and sandbox-startup guidance covers these diagnostic failures.
- Follow-up: keep inspection shell startup isolated; the shortcut delivery requires refresh-config and a non-executing interactive abbreviation check. The editor is never launched during verification.
