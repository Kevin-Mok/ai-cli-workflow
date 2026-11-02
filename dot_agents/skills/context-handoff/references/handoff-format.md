# Handoff Artifact Format

Use this format when creating or returning a handoff. Shared evidence, recovery,
retry and authorization controls remain in the entrypoint.

Return only the handoff, at most 600 words, using the eight headings below in order.

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

Return to [the skill entrypoint](../SKILL.md) for shared workflow and safeguards.
