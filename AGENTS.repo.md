# AGENTS.repo.md

Follow [`dot_codex/AGENTS.md`](dot_codex/AGENTS.md): session instructions win;
nested AGENTS/overrides only tighten. Use [ExecPlans](.agent/PLANS.md) in
[plans/](plans/), committed with related work.

Address the user as "Sire".
Leave model/reasoning-effort preferences in `dot_codex/config.toml` out of
ordinary commits unless explicitly requested.

Public repository: keep all sensitive artifacts private/ignored, including
credentials, live config, private notes, captures, runtime identifiers,
recovery archives and local logs; never force-add them. Before public
commits/pushes, audit pending content and history for identifying raw benchmark
artifacts (requests/responses; installation, session, thread, turn and cache IDs).
Keep `benchmarks/metaprompt/runs/` and `benchmarks/metaprompt-selection/runs/`
ignored; publish reviewed neutral aggregates only. Remove historical copies
only with explicit cleanup authority; keep recovery material outside this repo.

After i3 edits and successful `rf`/`refresh-config`, run
`i3 -C -c ~/.config/i3/config`, then `i3-msg reload`, and verify live behavior.
