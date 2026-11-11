# Use Firstmate natively with Codex

Kevin uses Codex in `/home/kevin/coding/firstmate` as the native Firstmate
coordinator. Open or resume that conversation, describe the project outcome,
and let Firstmate delegate and supervise Codex workers. This guide covers
startup, everyday requests, the CTO role, and returning to existing work.

## The setup

**You → Firstmate acting as CTO → Codex workers**

Firstmate is the directory of instructions, skills and helper scripts that
Codex reads when it starts there. Its primary conversation already coordinates
multiple projects. It is not an MCP server or a separate program to install.
The separate `firstmate-cto` launcher, outer chat, custom prompts and Fleet
monitor have been retired; they are not part of Kevin's current setup.

- Firstmate source and instructions: `/home/kevin/coding/firstmate`.
- Machine policy and this operator guide: `/home/kevin/linux-config`.
- Durable coordinator preferences: the owning home's private `data/captain.md`.
- Project implementation: workers assigned by Firstmate, not the coordinator.

## Open your existing Firstmate

From any shell directory, no sudo is needed:

codex resume -C /home/kevin/coding/firstmate

`-C` (uppercase) is short for `--cd`: it sets Codex's working root to the
Firstmate directory even when your terminal is in another directory. It does not
change your terminal shell's directory. `resume` opens the saved-conversation picker.

**Expected:**

```text
Codex shows saved conversations for the Firstmate working directory.
Select the existing primary Firstmate conversation and press Enter.
Type requests at the Codex input prompt.
```

Choose the owning primary, not a ship worker, review, or retired outer CTO
conversation. A title or directory filter alone does not prove ownership.
If the primary is already open, return to its existing terminal instead of
opening another client for the same conversation. For a custom `FM_HOME`,
reuse that home's established launch environment; do not substitute the default
home or guess one from a screenshot.

As your first message, ask for identity and status without changing the run:

```text
Confirm your Firstmate operational home and which work you own. Report current
priorities, verified results, human pauses, blockers and the next checkpoint.
Do not start or resume paused work from this status request.
```

If startup reports a conflicting session owner, stop and return to the existing
primary. Do not clear its ownership record, run startup twice or kill another
session to make a new one open.

## Start a genuinely new Firstmate session

Use this only when you are establishing a new primary, not replacing the owner
of an existing fleet. No sudo is needed:

codex -C /home/kevin/coding/firstmate

**Expected:**

```text
Codex opens with Firstmate as its working directory and reads its instructions.
The primary runs or verifies its normal startup and reports its context.
Any normal folder or hook approval still requires review in Codex.
```

Do not type shell commands into an agent message box. Codex reads Firstmate's
`AGENTS.md`; the primary follows its startup contract and confirms its home.
There is no need to manually run the internal startup or worker-spawn scripts.
Do not bypass hook trust or change the model or permission settings to launch it.

## Give Firstmate the CTO role

The CTO is the existing primary, not another supervisor above it. Send this
ordinary chat message in the owning Firstmate conversation:

```text
Act as my CTO within your existing Firstmate role. Maintain my stated priorities,
delegate implementation to Codex workers, make routine reversible decisions,
and report verified outcomes, blockers and decisions that need me.

Save these durable operating preferences in this home's data/captain.md through
your normal memory workflow, preserving existing preferences. Keep one owning
coordinator. Preserve human pauses and task-specific permissions. This setup
message does not authorize starting or resuming work. Confirm what you saved.
```

Firstmate's existing memory workflow owns that private preference file. The
file is included in its normal startup context. This guide records Kevin's
chosen setup; it does not claim those preferences have already been saved in
any live Firstmate home. Shared preferences for existing secondmates belong
in the primary's `data/captain-shared.md` through Firstmate's native procedure.
You do not need to create a secondmate merely to use the CTO title.

## Ask for work

Name the repository, outcome, acceptance checks and delivery permission. The
primary onboards projects through its project-management workflow and assigns
isolated workers. Example chat message:

```text
For ChartClutch, fix drawings disappearing after a page reload. Preserve existing
saved drawings. Verify with regression tests and a browser reload. Use Codex
workers and the project's established validation workflow. Commit the verified
change locally; do not push or merge. Report the commit, checks and remaining risks.
```

For a bounded unattended run, also provide an explicit duration or deadline,
ordered scope, push destination if authorized, and restart permission. Preserve
existing human pauses; opening Codex is not permission to resume them. Merge
permission and push permission are separate from permission to implement.

Useful messages typed into the Firstmate Codex input (not the shell):

| Input | Purpose |
| --- | --- |
| `$bearings` | Ask for Firstmate's fresh status digest. |
| `$afk` with a bounded assignment | Invoke its native away-mode procedure; confirm the accepted scope and deadline. |
| `Pause this run and confirm what has stopped.` | Request an explicit pause and wait for acknowledgment. |
| `Report the completed changes, commit, checks and remaining work.` | Check the actual outcome rather than inferring it from a quiet terminal. |

## Leave and return

When the primary is hosted in tmux, **Alt+D** detaches with Kevin's existing
bindings; **Ctrl+Space**, then **w** selects a window by its current name.
Those keys apply only inside tmux. Running Codex directly does not itself create
a tmux session. Detaching preserves the running process; exiting Codex does not
prove workers have stopped. Ask the primary to pause first when that is wanted.
Resume through the saved-conversation picker above, and reconcile status before
assigning work. The computer must stay awake and connected for local work.

Codex's native Firstmate supervision uses bounded foreground checkpoints.
A live process, an idle input prompt or a native goal alone does not prove
supervision is active. Have the primary confirm its current monitoring and next
checkpoint; it follows the protocol emitted by its own startup.

## Reference and migration notes

- [Installed Firstmate overview](/home/kevin/coding/firstmate/README.md).
- [Native primary contract](/home/kevin/coding/firstmate/AGENTS.md).
- [Captain preferences](/home/kevin/coding/firstmate/docs/configuration.md#captain-preferences-datacaptainmd--datacaptain-sharedmd).
- [Codex supervision protocol](/home/kevin/coding/firstmate/docs/supervision-protocols/codex.md).
- [Shared smoke checks](smoke-tests.md#native-firstmate-with-codex).

Old CTO plans and incident reports remain historical evidence. Saved conversations,
private routes and runtime notes were retained; do not treat their former tmux
window numbers, owner IDs or deadlines as current startup instructions. The
obsolete read-only Fleet monitor can be removed without stopping Firstmate workers.
