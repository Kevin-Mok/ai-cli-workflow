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
