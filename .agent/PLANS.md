# ExecPlan Contract

An ExecPlan is a living, decision-complete implementation record for work that
has three or more steps, changes multiple files, or requires an architecture
decision. Store it at `plans/<task-slug>.md` and write it so another engineer
can continue without reconstructing intent from chat. Define the outcome and
scope, plan the implementation and checks, then keep progress, evidence, and
review notes current through delivery.

## Required Sections

Every ExecPlan must contain:

- purpose and observable outcome
- current context, relevant files, and scope boundaries
- assumptions and decisions already settled
- an ordered implementation checklist using `- [ ]` and `- [x]`
- risks, edge cases, rollback points, and protected dirty state
- exact automated and manual verification
- progress, verification evidence, and review notes kept current

## Assumptions

State every assumption that could change scope, behavior, or validation. Ground
known facts in files or command output. If conflicting evidence or a missing
choice could materially change the result, stop and resolve it before
implementation.

## Checklist And Progress

- [ ] Record the initial state and protected pre-existing work.
- [ ] Define the result and explicit non-goals.
- [ ] List ordered implementation steps with file-level scope.
- [ ] Define RED, GREEN, regression, and manual checks where applicable.
- [ ] Update checkboxes and decisions as work proceeds.
- [ ] Record final evidence and unresolved risks.

Keep the checklist truthful. Do not mark an item complete because work merely
started, and do not continue against a plan invalidated by new evidence; revise
it first.

## Verification Evidence

For each material requirement, record the exact command or manual action, the
expected result, the observed result, and the exit status when available.
Include failing RED evidence before implementation for bugs and behavior
changes, then fresh GREEN and broader regression evidence. Do not substitute
confidence, an earlier run, or an agent report for current evidence.

## Review Notes

Record meaningful decisions, deviations, tradeoffs, remaining concerns, and the
rollback path. Before completion, reconcile these notes with the final diff and
confirm the plan, documentation, and implementation describe the same behavior.

## Commit Boundary

Update the ExecPlan in the same commit as the implementation or documentation
milestone it describes. A multi-commit plan may progress across commits, but
each commit must include its matching checkbox, evidence, and review-note
updates. Never leave relevant plan changes behind as a later cleanup commit.
