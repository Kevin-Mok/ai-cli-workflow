# Codex search broad-query output readability

Make broad conversation searches readable in a terminal by bounding the list,
showing one short matched excerpt, and giving project/date information a clear
hierarchy. Preserve full metadata through details and plain piped output.

## Symptom and impact

The user reported that codex-search "root" was unreadable and pasted many old
sessions, repeated untitled labels, raw ISO timestamps, UUIDs, long excerpts and
resume commands. They interrupted the output. Matching itself was correct, but
printing every full block made broad queries impractical to scan.

## Lookup and applicability

Read tracked postmortem-memory and systematic-debugging. Query terminal report
readability color found local-terminal-color-test-environment and
local-terminal-report-readable-projection; their controlled
NO_COLOR fixtures and responsive/progressive terminal views apply. Current
durable feedback requests hierarchy, human-readable dates and
readable terminal reports. Source confirms unbounded print_results with five
240-character snippets per session, regardless of terminal width.

## Status, hypothesis and next steps

Verified code and installed runtime fix. Defining synthetic TTY tests observed
RED: 24 results exceeded the 20-result cap, matching text was unhighlighted, and
details/limit flags were unavailable. Render terminal results as compact numbered
directory/date headers, one excerpt and complete resume commands. Carry rg's
UTF-8 byte match offsets into display spans; escape private text before color
insertion and clip by Unicode terminal cells. Full blocks remain available via
--details and default pipes; --limit affects printing, never picker candidates.
All 29 focused tests pass, including 54-column Unicode, literal/case matches,
NO_COLOR and unchanged source/resume/cache contracts. Independent review and
installed terminal checks are complete; evidence is recorded below.
Original sessions and the cache format need no changes. Keep private content out
of fixtures and reports.

## Review: dense-match highlighting performance

Independent read-only review found that the new span loop converts every rg
submatch using encoded-prefix decoding, even beyond the displayed 240-character
window. Synthetic warm one-line queries for x took 0.191s at 20,000 characters,
1.393s at 80,000 and 16.689s at 160,000 while printing the same small block.
This is an Important quadratic rendering regression. Original matching and
cache behavior are unaffected. Bound offset work to ordered submatches that
overlap the excerpt, with a defining timeout regression before the correction.
Record verified learning after focused GREEN and repeat review/runtime checks.

## Resolution and verification

Bound highlighting to rg's ordered byte ranges inside the excerpt and decode
only relative slices within that window. The defining 160,000-match warm search
timed out at 5s before the fix; afterward it took 0.392s (independent reviewer:
0.354s). Smaller 20,000/80,000 cases took 0.130s/0.217s, with the same 553-byte
output. Preserve a matched trailing carriage return and escape it visibly;
its defining assertion also observed RED then GREEN. At very narrow widths,
move the date to a second clipped line; 20-column header regression observed
28-column RED before correction.

Full focused suite: 29 tests in 9.525s, exit 0. Reviewer independently passed
29 tests in 9.171s and found no remaining Critical/Important issues. Launcher
regression, README gate and diff checks pass. Real fzf Enter on disposable
history returned the exact UUID/directory to the stub, exit 0; original fixture
source bytes were unchanged. Scoped refresh-config returned 0/REFRESH COMPLETE;
installed/source bytes match. Six installed-executable PTY/option/performance
contracts pass in 1.742s. The real colored display showed the numbered project,
date/title hierarchy and highlighted match; real fzf Esc returned 0/no launch
and left the synthetic source unchanged. Learned boundary: limiting visible results does not bound
CPU work unless hidden match spans are excluded before prefix decoding.
