# Consolidate Repeated Wins

Use when proposing skill promotion from repeated successful feedback patterns.
Keep normal append-only logging and private-context exclusions in the entrypoint.

## Consolidation (repeated wins become skills)

Method borrowed from the `continuous-learning-v2` skill in
[affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code/tree/main/skills/continuous-learning-v2)
(MIT, (c) 2026 Affaan Mustafa): atomic patterns, evidence-backed confidence,
then promotion. Its hooks, observer agent, and storage are not used here.

1. Candidate: one atomic trigger -> action pattern from `feedback.log` or `tasks/lessons.md`.
2. Threshold: propose promotion only after it applied successfully 3+ times in separate sessions, each with cited evidence (date plus commit, PR, or log line). Fewer or uncited = keep it as a lesson.
3. Target: prefer merging into an existing skill's `SKILL.md` and avoid growing the skill count; a new skill needs a stated reason no existing skill fits.
4. Shrink: each proposal names the lesson entries it retires. Once applied, append `YYYY-MM-DD - consolidated into <skill>: <entries>`; never delete or rewrite old lines in append-only files.
5. Ask the user before writing any skill (the step 8 one-time-or-permanent question); show the target, diff, evidence, and retired entries.

Return to [the skill entrypoint](../SKILL.md) for the shared workflow and boundaries.
