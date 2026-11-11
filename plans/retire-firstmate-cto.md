# Retire the Firstmate CTO wrapper

Replace the redundant outer CTO launcher with documented native Firstmate usage:
Codex runs in /home/kevin/coding/firstmate and the owning primary acts as the CTO.

## Scope and decisions

Remove scripts/executable_firstmate-cto, tests/test_firstmate_cto.py and both
custom CTO prompt files. Consolidate useful role guidance in docs/firstmate.md;
leave short redirects at old operator-guide paths so historical links still work.
Update README, smoke checks, feedback and superseded plan banners. No new wrapper,
MCP server, skill, goal, worker or project mutation is requested. The subsequent
commit-session request authorizes a focused commit and push of session-owned work.

Native Firstmate's existing data/captain.md memory workflow owns durable CTO
preferences; documentation alone does not claim those preferences were installed.
Native Codex CLI help and Firstmate README/configuration/supervision sources
support the documented commands. A cwd-filtered picker alone does not identify
an operational home. Preserve human pauses and existing owners.

## Ordered checklist

- [x] Capture both repositories' initial git status; map all references and shortcuts.
- [x] Back up affected uncommitted wrapper files under /tmp before removing them.
- [x] Observe the retirement acceptance check fail while wrapper artifacts exist.
- [x] Remove wrapper source/tests/prompts and rewrite active documentation.
- [x] Mark old plans and external local operator docs as superseded; preserve incident history.
- [x] Remove only the byte-matched installed wrapper and obsolete read-only Fleet monitor.
- [x] Attempt required refresh-config; preserve unrelated MIME-source conflict if still present.
- [x] Verify removal, links, native CLI options, guide and documented read-only protocol.
- [x] Review final scope and record evidence and remaining limitations.

## Protected state and rollback

Main checkout has extensive unrelated modifications and untracked work. Preserve
all unrelated hunks, postmortems, source ledgers, live Firstmate homes, conversations,
worker processes and tmux shells. Do not delete ~/.local/state/firstmate-cto:
it includes saved context and routes. Old plans and postmortems remain historical.
The only runtime removal is a verified dedicated read-only Fleet monitor; never
kill cto-master or the chat just to retire the wrapper. Verify exact command and
single-pane window before closing it; if identity differs, leave it intact.

The installed launcher must byte-match the reviewed source snapshot before removal;
preserve newer local edits instead of deleting them. Backups are outside Git;
their exact directory is recorded in the evidence section. External Firstmate docs
are untracked operator notes; add current guidance without altering upstream code,
private preferences, hooks or project state. No worktree is needed for this cleanup.

## Verification

Use /tmp/verify-firstmate-retirement.py before and after to check source/installed
absence, active docs and native command coverage; expected RED then GREEN. This
one-off acceptance check avoids adding permanent tests for deleted functionality.
Run git diff --check; verify guide Markdown targets and fish command syntax.
Read installed codex --help and resume --help. Render (never run the emitted
monitoring steps) Firstmate's Codex supervision protocol. Review runtime metadata
after monitor cleanup. Do not launch/resume a primary for a documentation check.

Manual: from a shell run codex resume -C /home/kevin/coding/firstmate; choose the
existing owning primary, confirm its home and ask $bearings without resuming paused
work. For a genuinely new fleet, codex -C /home/kevin/coding/firstmate starts native
Firstmate. In chat request durable CTO preferences through its existing memory
workflow. Interactive selection, hook trust, preference persistence and unattended
supervision remain unverified unless observed by the operator.

## Review and delivery

Keep implementation and this plan together if later committed. Suggested subject:
refactor(firstmate): retire outer CTO wrapper. Cursor handoff: read this plan and
docs/firstmate.md; verify native-only setup and preserve historical and private state.
The cleanup initially requested no commit/push; commit-session now authorizes
focused delivery. README claims point to the native guide.

## Evidence

Initial source and external git statuses captured. Read-only mapper found no fish
shortcut for firstmate-cto and no nested AGENTS in the affected source directories.
The ordinary fm directory shortcut is retained. Final verification is recorded below.

Rollback snapshot: /tmp/firstmate-cto-retirement-v89j5fym

Intentional RED: python3 /tmp/verify-firstmate-retirement.py exited 1, reporting
all four source artifacts plus installed wrapper, missing native guide and three
active documentation references. Source artifacts then removed and docs updated.
Installed wrapper byte-matched the backed-up source and was removed after saving
its own backup. External Firstmate operator and replacement docs now begin with
native setup and clearly label retained prior content as historical.
Live host metadata confirmed @33 had one pane with exactly
/usr/bin/python3 /home/kevin/scripts/firstmate-cto status --watch 20.
Only that read-only window was closed; cto-master chats and shells were retained.

Fresh GREEN: python3 /tmp/verify-firstmate-retirement.py exited 0. It verifies
absence of four retired source artifacts and installed command, guide command
coverage and link targets, and no active wrapper references in README, smoke
checks or operator pointer. Parent independently reran it successfully.
git diff --check exited 0. Test agent checked Fish syntax for both standalone
native Codex commands, exit 0; codex --help and codex resume --help exited 0,
confirming -C and the default picker (sandbox PATH-alias warning only).
Native Codex supervision instructions rendered successfully, exit 0, without
executing emitted controls. No new permanent code/test was added for removal.

Required fish -c refresh-config exited 1 as expected for the known duplicate
.config/mimeapps.list source mapping. Private log:
/tmp/refresh-config.wV1WBBfo.log. Lookup refresh-config duplicate mimeapps
inconsistent state found local-mime-drift-reconcile and
local-refresh-snapshot-ownership; pre-existing competing source ownership remains
outside this cleanup. Exact-target retirement is verified; broad refresh is not.
This deliberately checked known failure path introduced no new incident/remedy.

Final live host metadata: cto-master retains @77 fish and @79 cto. Only @33 Fleet
was removed. Private routes, saved conversations, firstmate workers and homes
were not deleted, interrupted, steered or resumed. Documentation-only Firstmate
role persistence and interactive resume remain manual checks. No new native
primary was launched, no model/permissions/hooks changed, no commit/push made.
README/guide/native smoke checks/feedback and two external operator-note headers
now reflect the chosen setup; old plans and incident reports are historical.
Final independent evidence review confirmed removal, native guide claims, links,
README/smoke/feedback updates and historical banners. No material implementation
finding. Reviewer noted the then-pending plan update and required accurate reporting
of blocked full refresh; both are now recorded. Live adoption remains unverified.

## Commit-session delivery milestone

Milestone: docs(firstmate): adopt native Codex workflow.
Completed: native guide, compatibility pointers, native README/smoke section,
durable native-use preference, retirement/superseded plans and three incident records.
Runtime retirement was already verified; removed wrapper artifacts were untracked
at the session baseline, so there is no tracked wrapper deletion to publish.

Scope session: 01a1cbfa-0b02-7df3-a75e-57a6471a9478. session_scope returned unsafe
with no recognized successful writes; use direct-write evidence from this conversation.
Mixed-file candidate content starts at HEAD and adds only native Firstmate README
and smoke sections, this session's preference and lessons, and this session's report-ledger
entries. The recovery plan was created in this session and is included. Only this session's
superseded banner and follow-up are published from the older untracked supervisor
plan; its extensive earlier history remains untouched and uncommitted locally.
No unrelated historical postmortems are needed for that reduced candidate.
External Firstmate operator-note edits belong to another checkout and are not
included in this repository's commit. No external repository commit is requested.

Verification: retirement verifier and documentation target checks passed; git diff
--check passed. Explicitly invoked README gate returned pass_no_change. Native
CLI help, Fish syntax and protocol rendering were verified without launching a
primary. Privacy and immutable staged-tree checks run immediately before commit;
Git hooks remain enabled. Interactive adoption and full configuration refresh
remain unverified/blocked as documented above. Unrelated dirty work is preserved.

Delivery target: current branch main, configured origin/main at
Kevin-Mok/ai-cli-workflow. Best-effort focused commit and ordinary push; no history
rewrite. Report the resulting SHA and actual push outcome in the task handoff.

Candidate validation note: the test runner initially used the changed-file overlay
instead of the exported full tree. Its missing-reference results are verification
root errors; see docs/postmortem/2026-11-11-firstmate-candidate-verification.md.
Correct full-tree checks passed. Link review also found baseline absent audio-file
links and a malformed documentation fragment in README. Safely separable repairs
point those readers to the existing sound-configuration document; they introduce
no runtime behavior. Repeat full-tree checks on the final candidate before commit.
