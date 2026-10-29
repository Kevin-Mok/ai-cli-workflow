# Right bar font activation restrictions

The right-screen font adjustment needs scoped host access because the sandbox blocks i3 IPC and chezmoi excludes the live i3 config.

- Symptom: restricted i3-msg returned Operation not permitted. Optional-path probes found absent script paths; chezmoi cat returned no managed content.
- Impact: initial inspection failed; no live changes occurred.
- Lookup: searched i3 IPC Operation not permitted; existing execution-environments scoped sandbox guidance and workspace-padding activation report apply.
- Evidence: approved IPC identifies HDMI-0 at x5888 as right screen, bar-0 font50; xrdb reports135DPI. chezmoi reports live config not managed.
- Resolution: approved read-only IPC succeeded. Preserve all local settings and apply only the same font change to source and live config, run refresh-config, validate and reload once.
- Status: activated. refresh-config exited0 with REFRESH COMPLETE; i3 validation exited0 with existing wheel-command deprecations; reload returned success true. After successive requested reductions, live bar-0 reports35.6pt, which reduces rendered size by27px from the original50pt at135DPI. Left and middle bars remain30pt and50pt. Screenshot pixel measurement was not performed.
- Learning: no new learning; existing scoped sandbox and unmanaged-target guidance covers this incident.
