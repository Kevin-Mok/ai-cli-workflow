# Compile the VPS and AWS bootstrap implementation prompt

## Purpose and observable outcome

Save the approved, paste-ready implementation prompt at
[prompts/bootstrap-vps-aws.md](../prompts/bootstrap-vps-aws.md). A later coding
session can use it to build a one-command server installer and a standalone
AWS Terraform setup. This task saves the prompt; it does not execute it.

## Context and scope

The user invoked `metaprompt`, chose the scope through six planning answers,
and approved the proposed prompt with `go` after Plan Mode ended.
Repository and current official documentation were inspected during planning.

The original three deliverables are the compiled prompt, this ExecPlan, and the
[deferred sandbox incident record](../docs/postmortem/2026-10-04-vps-bootstrap-prompt-sandbox-startup.md).
The saved prompt contains only the approved prompt text, without the
surrounding metaprompt report. No public API, configuration, installation,
or infrastructure behavior changes in this task.

The subsequent `commit-session` request authorizes a commit and push on a new
worktree branch. Two required delivery records are included with the original
artifacts: the [scope attribution incident](../docs/postmortem/2026-10-04-vps-prompt-session-scope-attribution.md)
and the [documentation patch incident](../docs/postmortem/2026-10-04-vps-prompt-delivery-patch-context.md).
A related entry in `tasks/lessons.md` records the repo-specific attribution
limitation, making six paths in the final delivery scope.

## Assumptions and settled decisions

- Deliverable: save the implementation prompt for a later coding session.
- Cloud scope: full AWS provisioning code, with a standalone network.
- Installation: shell essentials plus Codex, Claude Code, and shared skills.
- AI scope: CLI tools and skills; Graphiti/Neo4j are not required on the VPS.
- Linux scope: Ubuntu/Debian; the approved prompt specifies Ubuntu 24.04 LTS,
  Ubuntu 26.04 LTS, and Debian 13 on x86_64.
- Implementation direction: Bash bootstrap and chezmoi, reused by cloud-init;
  Terraform owns AWS resources.
- AWS starter defaults: Ubuntu 26.04, configurable t3.medium, encrypted
  20 GiB root disk. Region, SSH public key, and allowed CIDR are caller inputs.
- Authentication remains manual. The future implementation prompt authorizes
  code creation and validation, not AWS deployment or account sign-in.
- Preserve the exact approved prompt rather than expanding its scope while
  saving it. Technical versions and official guidance must be rechecked by
  the future implementing agent.

## Ordered checklist

- [x] Read relevant instructions, prompt-authoring references, feedback, and lessons.
- [x] Inspect the repo and official documentation; confirm the six scope choices.
- [x] Capture the current Git status and fingerprint protected dirty files.
- [x] Confirm artifact paths are unused and applicable nested rules are absent.
- [x] Save the exact approved prompt and deferred failure record.
- [x] Read back all three documents; check fidelity, links, whitespace, and scope.
- [x] Confirm existing files are unchanged and record final evidence.
- [x] Prepare the saved-prompt handoff and distinguish prepared evaluations from execution.
- [x] Run the scope helper and establish the documented direct-write fallback.
- [x] Create the requested worktree branch and transfer only the session documents.
- [x] Run the required README gate; it passes without changes.
- [x] Resolve the documentation patch context mismatch without changing prompt text.
- [x] Verify the final six-path scope and prepare the reviewed commit.

## Protected dirty state, risks, and rollback

The pre-write status contains modified `aliases/key_dirs.tmpl`,
`docs/phone-ssh-public-ip.md`, and `docs/smoke-tests.md`, plus:

- `docs/postmortem/2026-09-30-secret-audit-shell-sandbox-startup.md`
- `docs/postmortem/2026-10-03-benchmark-prompt-sandbox-startup.md`
- `docs/postmortem/2026-10-03-phone-ssh-diagnostic-shell-startup.md`
- `docs/postmortem/2026-10-04-terminal-prompt-sandbox-startup.md`
- `plans/compile-metaprompt-benchmark.md`
- `plans/compile-terminal-workflow-prompt.md`
- `plans/diagnose-phone-ssh-access.md`
- `prompts/benchmark-metaprompt-skills.md`
- `prompts/choose-terminal-workflow-2.md`
- `prompts/choose-terminal-workflow.md`

Preserve all of them. On a prompt-name collision, choose a new suffix rather
than overwrite. Before writing, SHA-256 fingerprints were captured for all
13 pre-existing changed files. Rollback before committing removes only this
task's five new documents and the appended lesson after checking for subsequent
user edits. After
committing, preserve history and use a separately authorized follow-up change.

During delivery, two additional unrelated files appeared in the original
checkout: `docs/postmortem/2026-10-04-kitty-scrollbar-inspection.md` and
`plans/kitty-codex-scrollback.md`. They are excluded as unattributed work.
All 13 baseline files still match their captured SHA-256 fingerprints.

AWS readiness and installation correctness are future verification work.
No model comparison, installation test, Terraform test, or cloud deployment
was performed as part of prompt authoring.

## Exact verification plan

This is documentation-only work; behavioral RED/GREEN tests are not applicable.

1. Read all new files back with Python and compare the saved prompt
   byte-for-byte with the approved prompt held in session context.
2. Check UTF-8 readability, a final newline, absence of trailing whitespace,
   absence of the surrounding report in the prompt, and existence of every
   local Markdown link in the plan and incident record.
3. Run `git diff --check`; before committing, also run
   `git diff --cached --check` and inspect the complete staged diff.
4. Run `git status --short`; compare pre-existing files' SHA-256 fingerprints
   with the captured baseline and confirm only the intended files were added:
   three during authoring, then two incident records and one lesson during delivery.
5. Manually compare the prompt with all six user choices and the approved plan.
   Expected: the one-command VPS workflow, AI scope, AWS starter, tests,
   documentation, and execution limits remain intact.

## Progress and verification evidence

- Planning inspection and current save-path checks completed successfully
  through the reviewed read-only execution route.
- Pre-write status was captured; all three intended paths were available.
- The read-back Python check exited 0. Comparison with the approved prompt
  held in session context returned `exact_approved_prompt: true`.
- All three documents passed UTF-8, final-newline, and trailing-whitespace
  checks. All four relative Markdown links resolved.
- SHA-256 comparisons confirmed all 13 pre-existing changed files were
  unchanged. The only additions were the three intended artifacts.
- `git diff --check` produced no diagnostics; `git status --short` showed the
  expected three additions alongside the protected pre-existing work.
- Manual review confirmed all six scope selections and the approved text were
  preserved. The evaluation scenarios are prepared, not executed comparisons.

Delivery checks:

- The prompt SHA-256 remains
  `22633969f23ee537f5710ab5ebf1e4f459d41e36b74601328da272598e1d5ca0`.
- The worktree contains exactly the six intended paths. UTF-8, final-newline,
  trailing-whitespace, and seven relative-link checks passed, exit 0.
- `git diff --check` passed, exit 0.
- `./scripts/executable_readme-recruiter-sync` returned
  `pass_no_change`, exit 0, in both the original checkout and the new worktree.
- All 13 protected original files are unchanged. A size-only comparison of the
  dirty set also noticed two concurrent, unrelated additions; both stay out
  of scope.

Official sources consulted during planning:

- [Chezmoi setup](https://www.chezmoi.io/user-guide/setup/)
- [Ansible pull mode](https://docs.ansible.com/projects/ansible/latest/cli/ansible-pull.html)
- [Codex CLI installation](https://learn.chatgpt.com/docs/codex/cli)
- [Claude Code setup and memory requirements](https://code.claude.com/docs/en/setup)
- [Terraform with cloud-init](https://developer.hashicorp.com/terraform/tutorials/provision/cloud-init)
- [Ubuntu release list](https://ubuntu.com/project/docs/release-team/list-of-releases/)
- [Debian releases](https://www.debian.org/releases/index)

## Review notes and commit boundary

Repository instructions, installed configuration, and reusable manual
procedures are unchanged. README and smoke-test documentation remain accurate;
`refresh-config` is not applicable to these documentation artifacts.
The future implementation prompt explicitly requires those updates when
behavior changes.

The original save-only request did not authorize commit or push. The later
`commit-session` request explicitly authorizes both on a new worktree branch.
Keep all six session paths in the same commit, using subject
`docs: add VPS and AWS bootstrap implementation prompt`.

Delivery context:

- Session: `01a1086d-ab77-7991-ab48-c505183de525`.
- Worktree: `/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt`.
- Branch: `docs/vps-aws-bootstrap-prompt`, created from `672cacd`.
- Push target: `origin/docs/vps-aws-bootstrap-prompt`; `origin` is the
  original checkout's configured remote.
- Ownership: directly observed document writes. The scope helper cannot parse
  this session's wrapped tool events; its attribution failure is documented.
- The worktree directory is ignored through local `.git/info/exclude`.
  This keeps worktree metadata out of Git without an unrelated commit on main
  or a tracked configuration change.
- The original checkout retains all 13 pre-existing dirty files plus the two
  concurrent unrelated additions identified above. No worktree
  merge, AWS deployment, or installer execution is part of this delivery.
- Final commit SHA, push result, and clean-worktree evidence are reported in
  the session handoff after execution, rather than predicted here.
