---
name: context-handoff
description: Use when handing off or resuming long-running work after interruption, context compression, agent transfer, or a context-window boundary.
---

# Context Handoff

<!-- context-handoff: adapted -->

Create a continuation artifact, not a transcript summary. Return only the
handoff, at most 600 words, using the eight headings below in order.

Assign `DC#` IDs to every known done criterion and write exactly one evidence
record for every listed DC. Status meanings are strict: `met = verified pass`;
`open = known incomplete`; `failed = latest evidence contradicts it`;
`unknown = evidence is unavailable or stale`. Each record maps
`check → observed result → evidence link or recovery action`.

Use None only after an explicit check confirmed absence. Use Unknown when
something was not checked. Do not infer from absent or stale evidence. When
context is incomplete, make recovery from the authoritative plan, status, log,
or source artifact the first applicable next action.

Group repeated failures by stable failure signature. Record attempt count,
what changed between attempts, and an observable retry condition. Do not
propose the same retry while its condition is unchanged. Link artifacts instead
of copying logs, transcripts, code, or plans. Preserve literal paths, branches,
commands, protected-state constraints, and security restrictions.

```markdown
## Goal and Done Criteria
Goal: <one sentence>
- DC1: <observable acceptance criterion>

## Constraints
- <literal protected state, command, scope, or safety constraint>

## Decisions
- <settled decision and concise rationale>

## Current State
- <confirmed branch, work item, owner, and implementation/test state>

## Evidence and Failed Attempts
- DC1 — <met|open|failed|unknown> — <check> → <observed result> — <evidence link or recovery action>
- Failure: <stable signature> — Attempts: <count> — Last evidence: <link> — Changed since: <fact> — Retry when: <condition>

## Artifacts
- [artifact](path): <why the next agent needs it>

## Blockers
- None — <check that confirmed absence>
- or Unknown — <authoritative source or action needed>
- or <blocker and evidence>

## Ordered Next Actions
1. Owner: <agent or role> — Action: <exact command or edit> — Expected: <observable result> — Stop if: <condition>
```

Every next action includes `Owner:`, `Action:`, `Expected:`, and `Stop if:`.
Its Action contains a literal executable command or a precise path-scoped edit.
Never use anaphora such as original command, same command, or as above. Prefer
the smallest action that restores evidence or advances an open DC.
