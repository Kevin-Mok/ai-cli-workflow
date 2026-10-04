# Group B source audit

## Research incident — 2026-10-03 package-key mismatch

A read-only package retrieval script stopped after the GitHub candidate because
it used the local key `sentry` for metadata saved under `getsentry`. No source
files, benchmark calls, or installed settings were affected. Correct the local
key mapping and resume the two pending repositories. A preliminary directory
inventory also reported that the new selection root did not yet exist; it has
now been created within the authorized research scope.

## Final eligibility findings

As of 2026-10-03. Exact repository star counts were retrieved through GitHub's
repository API; they measure each entire collection, not this particular skill.
Full retrieval timestamps, immutable revisions, inspected commit URLs and
file hashes are in [group-b.json](group-b.json).

| Native package | Exact repo stars | Substantive changes 90 / 180 days | Distinct substantive contributors 180 days | Decision |
|---|---:|---:|---:|---|
| getsentry/skills: prompt-optimizer | 1,034 | 0 / 2 | 1 | Eligible |
| github/awesome-copilot: prompt-optimizer | 39,667 | 0 / 0 | 0 | Introduction only; template variables expressly forbidden |
| NeoLabHQ/context-engineering-kit: prompt-engineering | 1,742 | 0 / 0 | 0 | Recent root copy/frontmatter edits do not establish content maintenance |
| Jeffallan/claude-skills: prompt-engineer | 11,719 | 0 / 0 | 0 | Recent changes only backlink/company/maintainer branding |
| davila7/claude-code-templates: prompt-engineer | 32,353 | 0 / 0 | 0 | Initial migration only, and no explicit reusable-template workflow |
| sickn33/antigravity-awesome-skills: prompt-engineer | 47,224 | 0 / 1 | 1 | Narrow alternative; variable-based template authoring not established |
| sickn33/antigravity-awesome-skills: prompt-engineering | 47,224 | 0 / 0 | 0 | Generic bulk limitations/risk metadata, overlapping NeoLab patterns |

Maintenance counts exclude introduction, moves, metadata, formatting, branding
and generic bulk boilerplate. The 180-day interval begins 2026-04-06 and the
90-day interval begins 2026-07-05. Contributor counts cover authors of qualifying
skill changes, not repository-wide contributors.

## Eligible package: Sentry prompt-optimizer

Pinned at `d18b7aa8ba878354e5c348310230e652f7690f9c`, nonarchived,
Apache-2.0. The complete package is in
[../candidates/sentry-prompt-optimizer](../candidates/sentry-prompt-optimizer):
`SKILL.md`, `SPEC.md`, `SOURCES.md`, four companion references, and the unchanged
repository `LICENSE`. Every byte was checked against GitHub contents fetched
with that explicit full commit SHA. The full SHA was independently resolved
from the commit API, rather than assumed from a tree identifier.

[Introduction, Apr19](https://github.com/getsentry/skills/commit/04f1e8301747ec34d01858176237349cd34e2779)
and the same-day package move receive no maintenance credit.
[Apr24](https://github.com/getsentry/skills/commit/6a844a09d7981594d510fc9b2d6b022b4ed2e246)
adds instruction-layer ownership, marker semantics and native tool-schema
separation. [May4](https://github.com/getsentry/skills/commit/c190d369bcbaa6cfdd95e9edfdba040506b4db76)
adds explicit external-context inventory, an output section and specification.
Both were inspected as diffs and change actual prompt guidance. Both authors
resolve to `dcramer`.

The native skill explicitly creates new prompts, refines existing prompts and
authors reusable templates. It covers coding-agent prompts through repository
context inventories and a complete coding-agent example. It is native prose
plus references; it requires no external API, API key or extra executable.
Provider API discussions in its model notes describe downstream prompt use.
Inner evaluation recommendations should be executed only within the approved
benchmark runtime and reported honestly when unavailable.

The native output is an eight-section package: Target, Success Criteria,
External Context, Optimized Prompt, Adapter Notes, Eval Set, Optimization Log,
Residual Risks. Extract **Optimized Prompt** without requiring a code fence the
source does not mandate. Existing-prompt outputs also include a concise
behavioral diff note. Load context-selected references exactly as directed:
new prompts use core-patterns, model-family-notes and transformed-examples;
existing prompts use meta-optimization-loop, core-patterns and model-family-notes.
`SOURCES.md` cites local skill-writer and external research as provenance; those
citations are not mandatory runtime dependencies.

## Exclusion evidence and lineage

GitHub's optimizer has exactly one path-history commit: its May14 introduction.
It also states a hard ban on placeholders and template variables. Large
collection star counts cannot overcome either failure.

NeoLab's native plugin skill and Aug7 root copy have identical current bytes.
The plugin's March name/frontmatter validation is outside 180 days; the previous
expertise expansion is Nov2025. The copy does not constitute a newly maintained
prompt-authoring implementation.

Jeffallan's latest substantive context-management addition is March23, before
the cutoff. Apr29 adds a documentation backlink. Oct3 adds company/maintainer
branding. Those last three changes were inspected, rather than counted as
substantive because their commit titles say `feat`.

Davila's package declares `vibeship-spawner-skills (Apache 2.0)` lineage and was
initially migrated from antigravity on Jan25. Its repository MIT license must
not erase imported Apache attribution. No later package change was found.

Antigravity's narrower `prompt-engineer` has a genuine Apr20 maintenance change:
[the missing conditional-clarification step](https://github.com/sickn33/antigravity-awesome-skills/commit/2a76f3260fc1bfcea894ac47d105afb70430a1fb),
including triggers and a three-question cap, authored by `xiaolai`. Its source
is the Feb4 import/enhancement from `ericgandrade/cli-ai-skills`. Its architecture
and debugging examples contain placeholders, but this alone does not establish
native reusable variable-based template authoring. Keep it a narrower
alternative rather than stretch the all-four gate. Its mention of Copilot CLI
availability is a runtime caveat; it issues no Copilot commands and the import
commit explicitly names Codex support.

The other antigravity `prompt-engineering` package adds only a generic three-line
limitations section and changes `risk: unknown` to `risk: none` in the recent
window. Its core patterns overlap the NeoLab opening. Additional inspected
`llm-prompt-optimizer` history also has only generic limitations after initial
introduction; `enhance-prompt` specializes in Stitch UI prompting rather than
all four benchmark workflows. Neither creates another finalist.

## Research incident resolution

The local `sentry`/`getsentry` metadata-key mismatch was corrected and retrieval
completed. A later commit/tree equality assertion failed because the returned
recursive-tree metadata SHA matched the branch commit SHA while the commit
object reported a distinct tree SHA. No package was published on that assertion.
The resolution was to independently fetch each full commit object and verify
every eligible package file against its explicitly pinned contents endpoint.
All eight Sentry package/license files matched. These were source-research
failures only; no model requests, credentials, installed settings or existing
benchmark files were touched.
