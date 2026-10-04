---
name: ai-workflow-doctor
description: Use when auditing a repository's AI instructions, skill catalog, local references, provenance, duplication, context size, or workflow drift; also use before and after instruction-surface optimization.
---

# AI Workflow Doctor

Check a repository's AI instructions for broken references, catalog drift, and
conflicting guidance. Run the narrowest audit, review its findings, repair
confirmed problems, and rerun it to report what changed.

<!-- ai-workflow-doctor: adapted -->

Run the installed doctor from any working directory instead of estimating workflow health from memory:

```bash
"$HOME/scripts/ai-workflow-doctor" --repo <repo>
```

Use `--help` for the complete interface. Select the narrowest operation that proves the task:

- Use the default text audit for a readable diagnosis.
- Use JSON when another check or agent needs stable structured evidence.
- Use `--check` for an objective pass/fail gate. Errors fail; semantic-conflict candidates remain non-blocking warnings for human review.
- Add `--verify-sources` when local provenance archives are available. Relative archive paths resolve from the audited repository root. Missing archives become explicit non-blocking warnings; reachable mismatches remain errors.
- Write a snapshot before an optimization and compare against it afterward. Treat metric deltas as evidence, not as automatic quality judgments.

Read every finding before acting. Repair deterministic errors at their source, preserve protected dirty state, and never auto-resolve a semantic warning or precedence conflict. Re-run the same command after changes and report the exact status, error/warning counts, active instruction bytes, character-based token estimate, and snapshot comparison when used.
