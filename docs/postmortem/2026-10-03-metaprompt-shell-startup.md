# Metaprompt compilation shell startup failure

- Date: 2026-10-03
- Symptom: Three initial read-only shell calls exited 1 before executing, with
  `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Impact: Repository status and skill/context reads were temporarily blocked;
  those calls made no repository changes.
- Evidence: Retrying the reads with approved elevated execution returned exit 0,
  including `git status --short` before any repository write.
- Root cause: The sandbox could not configure its loopback interface. The
  underlying host restriction was not investigated during prompt compilation.
- Resolution: Used approved elevated execution for the required shell reads.
- Status: Task unblocked; sandbox startup itself remains unresolved.
- Verification: The retried reads returned the canonical instructions, skill
  compilation rules, and pre-existing dirty-file inventory.
- Follow-up: Diagnose the sandbox separately if ordinary execution continues
  to fail; keep retries scoped to the task's authorized operations.
- Execution follow-up: Both read-only research agents encountered the same
  startup error on 2026-10-03. They were directed to the established elevated
  read path; the parent continued using that path successfully.
