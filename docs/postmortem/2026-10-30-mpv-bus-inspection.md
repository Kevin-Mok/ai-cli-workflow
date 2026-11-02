# mpv session-bus inspection denied

Live desktop inspection required scoped host permission; the application was unchanged.

- Symptom: sandboxed busctl returned “Failed to connect to bus: Operation not permitted”. Optional directory/package probes also found no mpv scripts/plugin installed.
- Impact: initial live verification blocked, no playback changes.
- Lookup: searched `D-Bus Operation not permitted`; ext-sandbox-loopback applies to denied local IPC. Inspected its execution-environments guidance before remedy.
- Cause: restricted session-bus access; absence of mpv-mpris is separately confirmed by apt-cache policy and the live name list.
- Resolution: scoped require_escalated bus inspection succeeded and showed Chrome/Spotify but no mpv MPRIS name.
- Verification: host busctl list exit 0, filtered names inspected. The compound optional-file probe ended 1 because absent directories are normal on this installation.
- Status: resolved inspection blockage; default sandbox access remains restricted. Next: use approved host execution for runtime media verification.
- Learning: no new reusable learning; existing local IPC sandbox guidance covers this workaround.

- Package setup: sudo -n apt-get install -y mpv-mpris returned password required; no package changes. Lookup `sudo password required` matched ext-interactive-sudo-boundary: privileged install needs the operator. Resolution: apt-get download fetched Ubuntu 0.7.1-1build2; dpkg-deb extracted it, ldd resolved all libraries, and install placed mpris.so in ~/.config/mpv/scripts without system writes. Existing video was left running and requires reopening. No new learning beyond the existing sudo boundary and scoped IPC guidance.

- Refresh: full refresh-config stopped at chezmoi apply (exit 1), private log /tmp/refresh-config.bfvLjBvn.log. No adoption attempted. Inspecting the exact conflict before a targeted apply; full refresh remains blocked.

- Refresh diagnosis: private log names .config/mimeapps.list changed-since-write prompt/EOF. Search `refresh-config chezmoi conflict` matched local-mime-drift-reconcile and local-refresh-snapshot-ownership; reviewed both. This is unrelated live MIME ownership, so no reconciliation was attempted. Source/live music helper cmp exit 0 proves the helper was applied before the later conflict.
- Runtime verification: silent headless mpv with installed plugin published the actual cigarette-smoke filename; installed block rendered it, click paused its unique owner, resume restored Playing, closing the test process restored FlaviBot. Full refresh remains blocked by unrelated MIME drift, current original mpv still needs reopening. No new general learning beyond reviewed IPC/sudo/refresh boundaries.

- Follow-up refresh reproduced the known MIME conflict (private log /tmp/refresh-config.pExPN3le.log); installed 4k_status still matches the updated source. Existing lookup/remedy applies; preserve unrelated MIME drift. Live Pango filename-tail/short/song checks passed and i3 was restarted in place. No new reusable learning.
