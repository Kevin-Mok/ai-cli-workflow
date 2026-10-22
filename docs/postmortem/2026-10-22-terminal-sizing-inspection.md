# Terminal sizing inspection path assumption

Use the existing fish refresh function when activating terminal configuration.
Discover its location before reading it; do not assume a scripts entry exists.

## Symptom, impact and evidence

During read-only terminal sizing diagnosis, `cat scripts/executable_refresh-config`
reported that the path does not exist. Other inspection output was unaffected;
no configuration, terminal placement or live state changed.

## Lookup and diagnosis

Lookup `terminal font size tmux monitor 4k` matched the monitor-font runtime
finding and existing sandbox access guidance. Its relevant lesson is to discover
actual installed/source paths, rather than assume a scripts entry. The refresh
command is a fish function; inspect the discovered source before activation.

## Status and next steps

Resolved diagnostic path assumption; no runtime repair needed. Discover refresh
source, inspect its conflict behavior, and preserve unrelated dirty/live files.
No new reusable learning: existing path-discovery guidance covers this mistake.

## Activation follow-up

Required `fish -c refresh-config` exited1; private diagnostics are in
`/tmp/refresh-config.IDhiOUHy.log`. The wrapper reported an apply conflict and
adopted no files. Preserve unrelated local/source divergence. Inspect the
conflicting target, then apply only the reviewed Kitty config; do not force a
whole refresh or reload i3. Activation verification continued with scoped deployment.

Scoped `chezmoi apply` for `~/.config/kitty/kitty.conf` exited0 and source/live
bytes match. The default was already applied before the full refresh reached
the unrelated adapter conflict. New processes read19pt; existing OS-window
sizes were not reset and i3 was not reloaded. Isolated default/scaling fixture
passed19/14.123/11.310pt; existing isolated runtime smoke passed. The full
refresh conflict remains; no new remedy beyond the existing scoped-apply
workaround is claimed. Status: verified scoped activation, global conflict open.
