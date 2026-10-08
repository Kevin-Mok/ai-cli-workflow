# Picker layout manual-page path was absent

A read-only gzip lookup assumed /usr/share/man/man1/fzf.1.gz and raised
FileNotFoundError. No files changed and subsequent source reads succeeded.
The installed fzf --help already provided the required responsive preview syntax.
Cause: assumed documentation path without discovery. Resolution: use observed
fzf --help and real-terminal verification instead of retrying guessed paths.
Postmortem-memory was read in this task series; prior narrow-path/schema incident
applies to unverified path assumptions. No new reusable learning; register this
report with an explicit no-new-learning decision. Lookup workaround is verified by the previously observed fzf --help output; feature verification is recorded separately in the task plan.
