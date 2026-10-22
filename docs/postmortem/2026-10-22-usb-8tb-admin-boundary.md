# USB 8 TB automount administration boundary

The drive setup needs host systemd access and administrator authentication. Prepare and validate an installer, then apply it from an authenticated terminal.

## Symptom and impact

A sandboxed systemctl inspection returned `Failed to connect to bus: Operation not permitted`. A scoped elevated read succeeded, but `sudo -n -l` reported that a password is required. No host configuration was changed. Candidate fstab validation inside the sandbox also reported unreachable device UUID paths (0 parse errors); validate on the host instead, because the sandbox omits device links.

## Evidence and diagnosis

The host has UUID=e2f4a51f-954a-4168-a1af-2c9645d3f00a mounted at /mnt/usb-8tb. Its fstab entry has defaults,nofail but no automount or hotplug activation. The restricted mount view is read-only; this does not establish a host filesystem fault.

## Prior knowledge lookup

Searched `systemctl Failed to connect to bus Operation not permitted` using the tracked postmortem-memory helper. Execution-environment findings describe approved host access as a workaround; applicable to the access boundary, not a disk failure. Elevated systemctl successfully showed the active mount. Passwordless sudo is unavailable, so do not retry privileged writes without authentication.

## Status and next steps

Activation pending. The UUID-specific installer is prepared: six new tests and two existing boot-mount tests pass; udev rule validation passes. Host fstab validation exits 0 with zero errors and six unprivileged raw-device probe warnings. The sandbox missing-device result is an inspection limitation, not a host disk failure. Run it with sudo in a terminal, then verify mount activation and a safely unmounted power cycle. Do not unplug a mounted filesystem.

## Learning

No new reusable learning: the existing execution-environment and administrator-authentication boundaries explain these results. Installer checks cannot prove live hotplug activation.

## Commit privacy validation

The first candidate privacy check blocked a machine-specific home-path alias in the new ledger record. Public commits use the existing /home/example convention; the working ledger retains its real local alias for targeted lookup. No finding content or unrelated ledger updates are included. Rerun the exact-candidate privacy gate before committing.
