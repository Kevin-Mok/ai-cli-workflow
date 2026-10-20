---
name: ui-ux-pro-max
description: Search offline UI/UX guidance, palettes, typography, charts and framework guidelines; generate a candidate design system. Explicit invocation only.
disable-model-invocation: true
---

# UI/UX Pro Max

Search the bundled design data, propose a design system suited to the project, and verify the resulting interface. Invoke with `$ui-ux-pro-max` in Codex CLI or `/ui-ux-pro-max` in Claude Code. This is a pinned local adaptation of the upstream skill; see [SOURCE.md](SOURCE.md) and [LICENSE](LICENSE).

## Inspect and search

Read the project's instructions, audience, existing design tokens, components and package manifest first. Preserve its stack and established design decisions. Use this skill's own `scripts/search.py` (resolve it relative to this SKILL.md); the shared installed path for both agents is `~/.agents/skills/ui-ux-pro-max/scripts/search.py`. Python 3 with the standard library is sufficient; do not install the npm CLI or run an updater.

Generate a candidate system with `python3 <skill-dir>/scripts/search.py "<product and audience>" --design-system -p "<project>" -f markdown`. This performs deterministic BM25 retrieval and rule-based synthesis from local CSVs, without an LLM API or network call. Treat the output as suggestions, not an accessibility or quality certification. Reconcile it with the project's tokens rather than replacing them automatically.

Supplement only where needed:

- `python3 <skill-dir>/scripts/search.py "keyboard focus modal" --domain ux`
- `python3 <skill-dir>/scripts/search.py "form validation" --stack react`
- `python3 <skill-dir>/scripts/search.py "elegant serif" --domain typography`

Use `--help` for supported domains/stacks, `--json` for structured output and `--full` for untruncated guidance. Use the actual detected stack. Run stack search separately from `--design-system`, which ignores `--stack`. Explicit legacy framework versions can yield no curated matches. Never invent a database match: if count is zero, retry once with clearer keywords, then disclose the miss and identify any general fallback advice.

## Save and implement

Search and generation print output by default. Persist only when requested, with `--design-system --persist --output-dir "<destination-project-root>" -p "<project>"`; optional `--page "<page>"` writes an override. Inspect existing `design-system/<project-slug>/MASTER.md` and page files first. Existing MASTER files are preserved unless `--force` is supplied; do not force replacement without authorization. Check the returned persistence status rather than assuming a write succeeded.

Implement only the requested interface changes, reusing existing components. Font suggestions may contain Google Fonts imports, and examples may mention external packages; inspect their licences and network/privacy implications in the destination app before adopting them. No font binaries or JavaScript packages are installed by this skill.

Render the resulting UI and check keyboard/focus access, contrast, reduced motion, responsive layout and text overflow. Run the destination project's relevant checks. Report actual search matches, design decisions and observed verification; distinguish unrendered recommendations from verified results. Existing design, critique and animation skills remain useful for craft decisions; this skill's distinct role is local searchable evidence.
