# Postmortem-memory shell sandbox startup failure

Repository inspection could not start through the default sandbox. Use the reviewed execution path for this task and retain the host restriction as unresolved.

## Symptom and impact

The first read-only `pwd && git status --short` invocation failed before any command ran: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. No repository changes occurred.

## Evidence and current status

The identical inspection through `require_escalated` completed with exit 0 and captured the initial dirty state. This establishes a verified task-local workaround; it does not fix or activate the sandbox.

## Root cause and resolution

The failure occurs during bubblewrap network namespace setup. The underlying host permission cause is unconfirmed. Approved execution outside the failing sandbox permits inspection.

## Verification and next steps

The reviewed command returned the working directory, git status, and skill text. Continue through the reviewed path, add this report to shared memory, and do not claim that sandbox runtime behavior has been repaired.

## Inspection correction

A catalog lookup used `dot_agents/README.md`, which does not exist. The catalog is `dot_agents/skills/README.md`; the subsequent search identified it. This was an inspection path mistake, not a repository runtime defect.

The evaluation agent also observed the same startup error, then used the reviewed command path. Both observations belong to this task-local incident, not two independent recurrence counts.

A second guessed fish-function snapshot path was absent; discovery located the actual `scripts/executable_snapshot-codex-config` entrypoint. Future reads should locate files before assuming shell-helper placement.

Refresh preflight also guessed `dot_gitconfig`, which is not the chezmoi Git source path. Snapshot dry-run passed; a following metadata comparison raised FileNotFoundError before any refresh or config mutation. Resolve managed paths with `chezmoi source-path` rather than guessed dotfile names.
