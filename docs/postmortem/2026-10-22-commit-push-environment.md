# Commit delivery environment restrictions

Review and ship safe dirty work while preserving desktop state. Record unavailable
integration checks separately from passing unit checks and retain local commits
if pushing is blocked.

## Symptom, impact and evidence

The native title tool failed with an HTTP transport error contacting the local
MCP endpoint. No title changed. The isolated Kitty smoke command exited 1 during
Xvfb startup before creating Kitty fixtures; 18 unit tests and the desktop-layout
shell check passed. No desktop windows moved and no i3 reload occurred.

## Lookup and applicability

Read the tracked postmortem-memory skill. Queries `title tool transport HTTP
request failed` and `Xvfb sandbox X11 access` returned adjacent environment/access
guidance. Existing restricted-display guidance applies to the graphical probe;
the title transport remains unavailable. Neither result proves a product defect.

## Current status and next steps

Title update skipped under the documented unavailable-tool fallback. Obtain
smoke diagnostics, run safe checks, then attempt privacy-gated commits and one
upstream push. No repair or passing graphical check is claimed yet.

## Diagnostic follow-up

Smoke --details confirmed Xvfb could not bind local/unix listeners and supplied
no display; disposable fixtures were cleaned up. This matches restricted X11
access guidance. Required `fish -c refresh-config` exited 1: read-only runtime,
Fish variable and alias paths, followed by an apply stop. No force deployment
was attempted. Continue safe delivery and request scoped host smoke access.

Scoped host smoke passed both12/19pt fixtures, round trips, restart, zoom,
restore and cross-window/instance isolation (exit0). The sandbox remains
restricted; host execution is a verified workaround. Physical review is manual.

An isolated-index git add failed because object insertion still needs .git
writes, even with GIT_INDEX_FILE under /tmp. No commit attempted. Use scoped
host Git writes; a temporary index alone does not bypass repository permissions.

Host refresh also stopped safely on existing local/source conflicts (exit1;
private diagnostics under /tmp). No force apply or i3 reload. The first reviewed
documentation candidate was blocked by the mandatory privacy gate with eight
home_path findings. No commit attempted. Preserve local path overlays and stage
only sanitized public candidates; path-only reversals add no publishable change.
The initial staging failure left no partial commit. Existing active hooks remain
unchanged; explicit privacy checks are mandatory even if hooks report inactive.

The broader memory suite completed25 passing tests and one coverage failure:
its default roots are sanitized /home/example paths absent on this host.
This is a configured-source availability failure; do not claim full corpus
coverage. Validate public candidate contracts against an explicit empty root
and check changed local reports by hash separately. No source-policy rewrite.

A contract-check invocation initially named an absent empty temporary root and
exited1; creating that intended fixture directory allowed both reviewed candidate
contract checks to pass (233/234 findings respectively, no contract errors).
This is check setup only, not a product change. Concurrent new memory edits
appeared during delivery; retain them outside this initial reviewed scope and
construct candidate ledgers from HEAD plus explicitly reviewed records.
