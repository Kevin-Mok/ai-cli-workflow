# Diagnose phone SSH access

## Purpose and observable outcome

Identify the correct phone-to-PC endpoint and distinguish account-password fallback from a local SSH-key passphrase. Success requires a Termux login from cellular data; local probes alone do not establish that result.

## Context and scope

Relevant files: `docs/phone-ssh-public-ip.md`, `docs/smoke-tests.md`, `dot_config/fish/config.fish.tmpl`, and `aliases/key_aliases.tmpl`. Investigate live SSH read-only. Do not change SSH service settings, keys, router rules, or shortcuts without evidence that they need fixing.

## Assumptions and decisions

The user uses Termux and can test on cellular data or Wi-Fi. The supplied command uses 192.0.2.10 on default port 22; repository shortcut `scu` instead uses 192.0.2.10:22229. Public-IP lookup currently agrees with the latter. The identity of 192.0.2.10 remains unverified.

## Checklist

- [x] Capture initial Git status and inspect relevant instructions and SSH docs.
- [x] Inspect PC listeners, authorized-key fingerprint, permissions, and configuration.
- [x] Compare the public endpoint host fingerprint with the local PC.
- [x] Record endpoint and prompt troubleshooting in docs and smoke tests.
- [ ] Obtain the user's cellular Termux login result and exact prompt if unsuccessful.
- [ ] Make an evidence-backed fix only if the corrected endpoint still fails.

## Risks and rollback

The public IP can change. Cellular and other Wi-Fi networks may impose different connectivity restrictions. No promise of access on every network is implied. Never disclose private keys or accept a changed host key without verification. Preserve the initial untracked September 30 postmortem. Only documentation changes are planned; rollback is removal of this session's documentation additions.

## Verification evidence

- `curl -4 --connect-timeout 5 --max-time 10 -fsS https://api.ipify.org`: exit 0, public IPv4 99.237.218.221.
- `ss -ltn 'sport = :22229'`: exit 0, IPv4 and IPv6 listeners present. SSH service is running.
- `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub`: exit 0, fingerprint `SHA256:Ga9LbSmPJsQ5+XRk4hmMsakRzuLzCHuBtczD7jNIXdQ`.
- `ssh-keyscan -T 5 -p 22229 -t ed25519 192.0.2.10 2>/dev/null | ssh-keygen -lf -`: exit 0, matching fingerprint. This verifies the endpoint from the PC's network, not from cellular.
- `ssh-keygen -lf /home/example/.ssh/authorized_keys`: exit 0, one ED25519 key labeled `u0_a417@termux`, fingerprint `SHA256:zyK3ixHEmEVfW8HMzFZ6mYTjRB9h2ZaJWnuIVnsCCKc`; directory/file permissions 700/600.
- Readable SSH drop-ins require `AuthenticationMethods publickey` and disable password authentication. Effective root-only `sshd -T` was not run because interactive sudo is needed.
- Pending manual check: disable phone Wi-Fi, run `ssh -p 22229 user@192.0.2.10`, compare host fingerprint if prompted, and report login or exact prompt.

## Review notes

`git diff --check` passed (exit 0) for the documentation changes. Git status
confirmed no tracked configuration files changed and the initial untracked
postmortem remains untouched.

No live configuration changes, private-key reads, or login attempts were performed. Root-cause diagnosis remains provisional until the phone test confirms whether the wrong endpoint explains the reported prompt. Keep this plan with its matching documentation if committed.
