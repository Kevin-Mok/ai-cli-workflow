---
name: readme-recruiter-sync
description: Use when handling commit or push requests, refreshing the root README, or changing repo behavior that can make the root README stale, especially when the README needs to sell the repo clearly to recruiters before setup details take over
---

# Readme Recruiter Sync

Keep the root `README.md` aligned with the repository before commit or docs
workflows ship changes. Focus on truthfulness, recruiter-first information
hierarchy, runnable onboarding, repo-based tech-stack explanation, and a
consolidated recruiter-facing hook. Read the contract, compare README claims
with the actual files and commands, and repair or report each gap.

## Quick Start

1. Read `references/readme-contract.md`.
2. Inspect the root `README.md` and the files the current change touches.
3. Verify whether the README still matches the repository and recruiter-readability bar.
4. If any issue is fixable now, return `update_in_same_change` and include safe README repairs in the matching commit.
5. Return `blocked` only for the README repair when it cannot safely be included; report the finding and continue eligible commits.

## Outcome States

- `pass_no_change`: README is accurate and passes the recruiter-first gate.
- `update_in_same_change`: README can be made compliant in the same change and must be edited alongside the scope change.
- `blocked`: the README repair cannot safely enter scope; report it while continuing eligible commits.

## Workflow

1. Determine whether the gate applies.
   - Always apply before commit or push workflows finalize work.
   - Apply when the user asks for README work directly.
   - Assume it applies when changes touch `AGENTS.md`, `AGENTS.repo.md`, `dot_codex/`, `dot_agents/`, `plans/`, setup flows, documented commands, or repo positioning.
   - Resolve skill metadata from repo-local `dot_agents/skills/readme-recruiter-sync`, then repo-local `.agents/skills/readme-recruiter-sync`, then `$HOME/.agents/skills/readme-recruiter-sync` (or `READMERECRUITERSYNC_SKILL_DIR` when explicitly set).
2. Ground every README claim in repo evidence.
   - Read the relevant config, skills, scripts, docs, and existing README sections.
   - Prefer tracked files over memory.
3. Audit the front-of-file hierarchy before checking coverage.
   - Default to a recruiter-first structure unless the user explicitly asks for a different order.
   - Require a substantive opening hook: at least two sentences (or short paragraph), and at least ~35 words.
   - The opening must explicitly answer: What is this repo, who benefits, and why it matters.
   - Recruiter-facing value should be consolidated near the top and not repeatedly scattered across distant sections.
   - Surface proof early: the opening hook plus `Tech Stack And Why Chosen` should appear before setup-heavy sections.
   - Move `Quick Start`, `How to run`, dense command blocks, and other setup-heavy content later by default.
   - If the README has top-level `Quick Start`, `Install`, `Setup`, `How to run`, or a major fenced code block before both
     - the opening recruiter-facing hook/section, and
     - `Tech Stack And Why Chosen`,
     the README is stale unless operator-first ordering was explicitly requested.
   - Treat these as stale even if technically correct:
     - generic one-line intros
     - recruiter-facing value duplicated in multiple distant sections
     - stack rationale buried below setup blocks
     - a feature/browse section used as the opening hook substitute
4. Check required coverage from `references/readme-contract.md`.
   - install/bootstrap
   - day-to-day use
   - core command flags or options for README-documented entrypoints
   - repo-based tech stack and rationale
   - recruiter-facing value consolidated into the opening hook
5. Verify commands and flags before documenting them.
   - Use local `--help`, usage output, or script source.
   - If a command has no meaningful flags to explain, state that directly in the README.
6. Keep the tech stack section grounded in the repo.
   - Center it on repo-evidenced layers: `chezmoi`, Codex CLI/config, AGENTS chain, local skills, Graphiti MCP/Neo4j, terminal tooling, and Python/Bash automation.
   - Pair each layer with one concise "why chosen" rationale.
7. Choose the final outcome state:
   - `pass_no_change`: no issues.
   - `update_in_same_change`: any fixable README issue is present.
   - `blocked`: README repair cannot safely enter this scope; continue other eligible commits.

## Default Order

Prefer this order unless the user explicitly asks for another order:

1. Title plus longer opening hook
2. `Tech Stack And Why Chosen`
3. Optional architecture/implementation snapshot
4. Install, bootstrap, day-to-day commands, and deeper operator docs

## Commit Flow Rules

- Run this required check for commit and push workflows. Its non-safety findings are warnings; attempt safe repairs and continue committing eligible work.
- Never waive the gate because the diff is small.
- Never fabricate recruiter copy, installation steps, tech-stack claims, or CLI flags.
- If `README.md` contains unrelated dirty work, include only safely separable in-scope repairs. Report any remaining README conflict without blocking other eligible work.

## Output Contract

When the state is not `pass_no_change`, list each issue as:
- `coverage` or `hierarchy`
- the specific stale section/claim
- line/evidence evidence that triggered the mismatch
