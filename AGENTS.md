# AGENTS.md

This repository keeps one active AI instruction body:
[`dot_codex/AGENTS.md`](dot_codex/AGENTS.md). Read and follow it before doing
work here.

Apply active user and developer instructions first, then the canonical document,
then any nested `AGENTS.md` or untracked `AGENTS.override.local.md` file that
adds stricter local constraints. Lower layers may specialize but never weaken a
higher layer.

[`AGENTS.repo.md`](AGENTS.repo.md) and
[`AGENTS-BASE.md`](AGENTS-BASE.md) are compatibility routing layers, not
independent policy sources. For non-trivial work, use the ExecPlan contract in
[`.agent/PLANS.md`](.agent/PLANS.md) and keep the active plan under
[`plans/`](plans/).
