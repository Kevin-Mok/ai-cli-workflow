# AGENTS.repo.md

Repository-specific Codex policy is canonical in
[`dot_codex/AGENTS.md`](dot_codex/AGENTS.md). This compatibility layer exists
for tools that expect a root addendum; it does not add a second instruction
body.

Read the canonical document before working. Active-session instructions still
win, while nested `AGENTS.md` and untracked `AGENTS.override.local.md` files
may only add stricter local constraints.

Non-trivial work follows [`.agent/PLANS.md`](.agent/PLANS.md), with live plans
stored under [`plans/`](plans/) and committed alongside the related work.

Treat model and model-reasoning-effort changes in `dot_codex/config.toml` as
personal local preferences. Ordinary commit workflows must leave them out
unless the user explicitly asks to include them.

Address the user as "Sire" in every chat message.

This is a public repository. Keep any artifact containing sensitive information private, ignore it before generation or adoption, and never force-add it to a public commit. This includes credentials, live configuration, private notes, request/response captures, runtime identifiers, recovery archives and machine-local logs. Review and publish a neutral aggregate summary only when useful.

Before a public commit or push, remove identifying raw benchmark run artifacts, including recorded requests/responses and installation, session, thread, turn, and cache identifiers. Keep `benchmarks/metaprompt/runs/` and `benchmarks/metaprompt-selection/runs/` private and ignored; publish only reviewed aggregate findings. If identifying artifacts were committed, remove their historical copies as part of an explicitly authorized history cleanup. Audit pending file contents as well as Git history, and preserve recovery material outside the public repository.

Whenever i3 configuration changes, after `rf` (`refresh-config`) successfully applies the changes, validate the deployed i3 config with `i3 -C -c ~/.config/i3/config`, then run `i3-msg reload` and verify the affected live behavior before completion.
