Create a reusable Bash script in /home/example/linux-config that I can run locally to repair Codex CLI updates on my VPS.

Context:
- SSH target from my screenshot: example-user@51.222.111.61. Allow overriding it.
- My existing SSH key provides passwordless login; this does not establish passwordless sudo.
- Codex runs `npm install -g @openai/codex`, which fails with EACCES while renaming /usr/lib/node_modules/@openai/codex.
- I suspect outdated Node/npm, but investigate permissions and installation ownership before deciding that versions need upgrading.

Deliver scripts/executable_fix-vps-codex.sh with:
1. --host, --port, --identity, --dry-run, and --help options. Use existing SSH configuration and host-key verification. Dry run must perform diagnostics without remote changes.
2. Remote diagnostics for OS, architecture, login shell, Node/npm versions, executable paths, npm global prefix, and relevant ownership/permissions. Avoid printing credentials.
3. A minimal, repeatable repair that gives example-user a writable Codex installation and makes future normal updates work without sudo. Reuse an existing suitable user-managed runtime where possible. Upgrade Node/npm only when compatibility requires it, using verified current requirements and official sources.
4. Persistent PATH setup for the detected login shell, including fish if present. Back up changed configuration and avoid duplicate entries on reruns.
5. Clear errors, meaningful exit codes, and rollback instructions. Preserve Codex authentication/configuration, existing applications, and system-managed Node packages. Do not recursively change ownership of /usr or run Codex as root.
6. Verification that a fresh SSH login resolves the intended Codex executable, `codex --version` succeeds, and the ordinary npm update command succeeds as example-user.

Follow repository instructions and preserve pre-existing dirty work. Inspect the existing local fnm repair helper for useful conventions without assuming it applies to the VPS. Add focused regression coverage for permissions, shell/PATH handling, repeat runs, SSH failures, and a genuinely non-mutating dry run. Update the ExecPlan, relevant usage docs, and smoke checks.

Deliver the script, exact local invocation, test results, and any remaining manual verification. State whether sudo is needed and why. Build and validate the script locally; leave running the remote repair to me.

When you choose an approach, commit; revisit only on directly contradictory evidence. Before delivering, identify and fix the draft’s biggest weakness internally. Show only the final result.
