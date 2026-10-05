# Incident review artifact exceeded command argument limit

An external review agent attempted to serialize its reviewed JSON through one oversized command argument. Write large artifacts in bounded chunks or through a file stream, then parse the complete result before relying on it.

## Symptom and impact

The execution tool rejected the serialization command with `Argument list too long (os error 7)`. The reviewed output was delayed; no file was changed by the rejected command.

## Evidence and current status

The agent reported the rejection before execution and is rewriting its authorized temporary JSON in bounded chunks. The completed artifact now parses successfully and reconciles all 76 external hashes/87 aliases against independent discovery. Bounded serialization is a verified workaround.

## Root cause and resolution

The full review JSON exceeded an operating-system argument limit. This is a confirmed transport limit, not an incident-review content failure. Candidate remedy: bounded writes followed by JSON parse and source-coverage reconciliation.

## Verification and next steps

The final 112,282-byte file was written in eight bounded chunks. JSON parsing and reciprocal source/finding validation passed; independent discovery matched every external alias and hash. Preserve original sources and avoid printing raw incident contents.
