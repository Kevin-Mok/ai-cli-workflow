# Phone SSH diagnostic shell startup failure

Date: 2026-10-03

## Symptom and impact

The first read-only diagnostic command could not start: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. SSH investigation was briefly delayed; that command changed no files.

## Evidence and status

The sandboxed command returned exit 1. Approved elevated execution returned exit 0 and captured the initial Git status: only the pre-existing untracked `docs/postmortem/2026-09-30-secret-audit-shell-sandbox-startup.md` was present. It remains untouched.

A delegated search also returned exit 2 because an assumed `dot_ssh` directory does not exist; the subsequent repository-wide search succeeded. A public SSH host-key probe returned no keys for default port 22 within its timeout, so piping that empty result into `ssh-keygen` produced an error. No conclusion about endpoint identity is drawn from that empty probe.

## Root cause and resolution

The shell sandbox could not configure its loopback interface. Approved execution outside that sandbox allowed read-only diagnostics to continue. The empty host-key probe was replaced by probing the documented PC port, 22229, which returned the PC's matching ED25519 host fingerprint.

## Verification and follow-up

Repository reads, service inspection, public-IP lookup, and the public port-22229 fingerprint comparison completed successfully. Sandbox repair is outside this task. Use discovered paths and handle empty probe output explicitly in future diagnostics.
