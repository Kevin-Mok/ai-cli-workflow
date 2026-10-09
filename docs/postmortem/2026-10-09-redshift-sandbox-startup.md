# Redshift task sandbox startup failure

The initial read-only shell command failed before execution; approved host-shell execution allowed the task to proceed.

## Symptom and impact

bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted. No repository command ran in the failed attempt and no files were changed by it.

## Evidence and lookup

Query: bwrap loopback Failed RTM_NEWADDR. Matching finding ext-sandbox-loopback applies to runner initialization, not Redshift. Approved require_escalated shell commands successfully read repository status and configuration with exit 0. The default runner remains unresolved; host execution is a verified workaround.

## Resolution and follow-up

Use approved host-shell execution for this task. No OS sandbox policy changed. No new learning beyond ext-sandbox-loopback; this recurrence does not establish a repair of sandbox startup.
