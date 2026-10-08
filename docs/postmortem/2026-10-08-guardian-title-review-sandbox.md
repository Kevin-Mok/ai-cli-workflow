# Guardian title review sandbox could not start

The independent read-only review attempted rg under the default sandbox and
failed before command execution with bwrap loopback Failed RTM_NEWADDR:
Operation not permitted. No file or model request occurred. This matches the
known local-sandbox-loopback-approved-route finding already used by the parent.
Parent instructed the reviewer to use require_escalated for scoped reads;
the reviewer completed the source analysis and reported filtering/selection risks.
Status: verified workaround for read-only review; default sandbox remains broken.
No new reusable learning beyond the established approved-route finding. No
permissions or sandbox configuration were changed. Follow-up: keep authorized
scoped execution separate from any future infrastructure repair.

A later read-only review lookup assumed /usr/share/man/man1/fzf.1.gz and found
the file absent. No files changed. Installed fzf --help and deliberate synthetic
capability checks provided the needed behavior evidence; the general transform
action is unsupported in fzf 0.44.1. This repeats the existing narrow-path lookup
lesson; no new reusable incident finding.
