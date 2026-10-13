# tmux scrolling investigation sandbox startup

The default command runner failed before reading the saved prompt. Use the approved scoped execution route to continue; host sandbox repair is separate.

## Symptom and impact

On 2026-10-13 the initial read returned exit 1: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. No shell body ran and no repository changes occurred.

## Lookup and evidence

Query: `bwrap loopback Failed RTM_NEWADDR`. Matching reviewed finding: `local-sandbox-loopback-approved-route` in execution-environments.md. Applicable because the wrapper failed before command execution. Approved require_escalated reads returned exit 0, including current instructions, prompt and Git status. A read-only investigation agent encountered the same startup error.

## Status, resolution and limits

Verified workaround: approved scoped shell execution permits this task. The default Bubblewrap startup remains broken; no host security settings were changed. No new reusable learning beyond the existing finding. Next steps: use the scoped route for necessary task commands and keep host repair out of this task.

## Resume title transport

On authorized continuation, native set_thread_title failed with an HTTP transport error to its local MCP endpoint. No title update occurred; kept the existing title and continued from the authoritative plan. No transport retry or host changes. This is separate from tmux behavior; the environment limitation does not invalidate configuration or scrolling verification.
