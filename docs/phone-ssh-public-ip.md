# SSH From Your Phone Over Public IP

Use `scripts/executable_setup-phone-ssh.sh` to set up key-based SSH access
from your phone over a public IP. Prepare the phone's key, configure SSH,
forward the router port when needed, then test from cellular data. Add Mosh
and extra hardening after SSH works.

What it changes:

- moves SSH to a non-default port
- disables password and keyboard-interactive login
- keeps public-key login enabled
- opens the chosen port in `ufw` or `firewalld` when one is active

What it does not change:

- router port forwarding
- ISP or carrier NAT restrictions
- dynamic DNS

## Prerequisites

- `sshd` is installed on the target machine
- your phone SSH client has a public/private keypair
- the target login user has that public key in `~/.ssh/authorized_keys`, or you
  will pass `--public-key /path/to/phone.pub`
- your router forwards a TCP port to this machine, or the machine already has a
  directly reachable public IP

If your ISP uses CGNAT and does not give you a real inbound public IP, raw SSH
by public IPv4 address will not work until you solve that upstream.

## Setup

Run the setup script normally. It will prompt for `sudo` and re-exec itself as
root. Replace `22229`, `example-user`, and the public-key path with your real values:

```bash
./scripts/executable_setup-phone-ssh.sh \
  --port 22229 \
  --user example-user \
  --public-key /path/to/phone.pub
```

Safer cutover if you want to keep `22` open while testing:

```bash
./scripts/executable_setup-phone-ssh.sh \
  --port 22229 \
  --user example-user \
  --public-key /path/to/phone.pub \
  --keep-port-22
```

The script writes:

- `/etc/ssh/sshd_config.d/80-phone-remote-access.conf`
- `/etc/systemd/system/ssh.socket.d/listen.conf` when `ssh.socket` is enabled or active

It validates the resulting config with `sshd -t` before reloading the SSH
service, and it creates `/run/sshd` first when that runtime directory is
missing. On systems using `ssh.socket`, it also updates the systemd
`ListenStream` entries so the custom port actually opens. On systems not using
socket activation, it enables and starts `ssh.service` if that service was
inactive.

## Router Step

Forward the same external TCP port on your router to this machine's LAN IP and
the same internal port.

Example:

- external `22229/tcp` -> `192.0.2.10:22229`

## Verify

1. Turn off Wi-Fi on your phone so you are not testing from inside the LAN.
2. Connect over cellular data with the public IP:

```bash
ssh -p 22229 example-user@PUBLIC_IP
```

3. Confirm the login succeeds without any password prompt.
4. If you used `--keep-port-22`, rerun the script without that flag after the
   custom port works.

## Wrong Endpoint Or Password Prompt

As verified on October 3, 2026, the PC endpoint is:

```bash
ssh -p 22229 user@192.0.2.10
```

The fish shortcut `scu` uses this endpoint. The `sso` and `ssop` shortcuts use
`192.0.2.10` on port 22; do not assume those reach this PC. The PC's public
IP can change, so recheck it with the host-side doctor when an old endpoint
stops working.

For a new connection, compare the ED25519 host fingerprint against the PC's
local `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub` output. The verified
fingerprint on that date is
`SHA256:Ga9LbSmPJsQ5+XRk4hmMsakRzuLzCHuBtczD7jNIXdQ`.

Test from cellular data with phone Wi-Fi disabled, then repeat on Wi-Fi.
`Enter passphrase for key ...` asks to unlock the phone's private key locally;
`example-user@HOST's password:` asks for the remote account password. A key installed
on one server does not automatically authorize it on another. If the corrected
endpoint still prompts, report the exact prompt before changing server settings.
Never share the private key. This PC currently has one authorized ED25519 key
labeled `u0_a417@termux`; its public fingerprint is
`SHA256:zyK3ixHEmEVfW8HMzFZ6mYTjRB9h2ZaJWnuIVnsCCKc`.

## Mosh From Termux

Mosh uses the existing SSH connection only to start a session. After that,
the terminal session uses UDP, so it remains usable when the phone changes
between Wi-Fi and cellular data. It is not a file-transfer protocol; use the
included SSH helpers for `scp` and `rsync` transfers.

On the PC, prepare Mosh and the host firewall:

```bash
sudo ./scripts/executable_setup-mosh.sh
```

On the router, forward the default Mosh range to this PC's stable LAN address:

- external `60000:61000/udp` -> `PC_LAN_IP:60000:61000/udp`

From Termux, copy this repo's bootstrap over the already-working key-based SSH
connection. Replace the sample connection values with your existing public SSH
endpoint:

```bash
scp -P 22229 example-user@PUBLIC_IP:/home/example/linux-config/scripts/executable_setup-termux-mosh.sh .
chmod +x executable_setup-termux-mosh.sh
./executable_setup-termux-mosh.sh \
  --host PUBLIC_IP \
  --user example-user \
  --ssh-port 22229
```

The bootstrap installs `mosh`, `openssh`, and `rsync`, then creates the
`pc-mosh`, `pc-push`, `pc-pull`, `pc-sync-to-pc`, and `pc-sync-from-pc`
commands. `pc-mosh` uses the named SSH configuration rather than exposing an
SSH or Mosh server from Android. The two sync commands are deliberately
one-way; they do not attempt an unsafe bidirectional merge.

From cellular data, verify the route:

```bash
ssh pc-remote true
pc-mosh
```

If `pc-mosh` is not found after the bootstrap, make its default helper path
available in the current shell:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Extra Hardening Against SSH Spam

After the basic remote-access setup is working, apply the stricter SSH
hardening layer:

```bash
./scripts/executable_harden-phone-ssh.sh --port 22229
```

This writes:

- `/etc/ssh/sshd_config.d/81-phone-ssh-hardening.conf`

What it tightens:

- restricts SSH login to the chosen user with `AllowUsers`
- forces `AuthenticationMethods publickey`
- keeps password and keyboard-interactive auth disabled
- refuses to apply if the chosen user has no valid public key in
  `~/.ssh/authorized_keys`
- lowers `MaxAuthTries`
- shortens `LoginGraceTime`
- limits unauthenticated connection bursts with `MaxStartups`

Tradeoff:

- if you use SSH for any user other than the chosen one, this script will block
  those other SSH logins until you widen the rule
- agent forwarding is disabled by this hardening layer

If you need a different SSH login user, pass it explicitly:

```bash
./scripts/executable_harden-phone-ssh.sh --user example-user --port 22229
```

Quick verification:

```bash
sudo sshd -T | grep -E '^(allowusers|authenticationmethods|passwordauthentication|kbdinteractiveauthentication|maxauthtries|logingracetime|maxstartups) '
```

## If You Still Get `Connection refused`

Run the host-side doctor:

```bash
./scripts/executable_doctor-phone-ssh.sh --port 22229
```

What it tells you:

- whether `sshd` is effectively configured for `22229`
- whether key-only authentication is active in effective `sshd` settings
- whether `ssh.socket` is still forcing the listener to port `22`
- whether the host is actually listening on `22229`
- whether `ufw` or `firewalld` appears to allow the port

Interpretation:

- if the doctor says nothing is listening on `22229`, the problem is still on
  the host
- if the doctor says the host is listening on `22229`, the remaining likely
  causes are router forwarding, wrong LAN target IP, or CGNAT

## Risks And Notes

- Changing the SSH port reduces background scans and log noise. It is not the
  main security control.
- The actual hardening comes from disabling password login and using SSH keys.
- If another `sshd` config file still defines a different `Port`, SSH may keep
  listening there too. Check `sudo sshd -T | grep '^port '` if needed.
- If your distro uses `ssh.socket`, the actual listening ports come from
  systemd socket activation. This workflow now writes a drop-in so the custom
  port is applied there too.
- If your public IP changes often, add dynamic DNS or use the current IP each
  time.

## Rollback

Remove the managed config and reload SSH:

```bash
sudo rm /etc/ssh/sshd_config.d/80-phone-remote-access.conf
sudo rm -f /etc/systemd/system/ssh.socket.d/listen.conf
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket 2>/dev/null || true
sudo systemctl reload ssh || sudo systemctl reload sshd
```
