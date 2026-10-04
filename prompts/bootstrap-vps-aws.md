Implement a plug-and-play server installation workflow for this repository:
https://github.com/example-user/dotfiles.git

The owner wants one command on a fresh VPS that installs their Linux
configuration, makes fish and shared aliases immediately usable, and installs
Codex, Claude Code, and shared skills. Also provide beginner-friendly Terraform
for creating an AWS server with the same setup.

Read the repository's AGENTS.md instruction chain and .agent/PLANS.md.
Create and maintain plans/bootstrap-vps-aws.md. Preserve pre-existing work.

Context inspected during prompt preparation; recheck before implementation:
- README.md: current installation instructions.
- dot_config/chezmoi/chezmoi-template.toml.tmpl: desktop-oriented defaults
  and the expected ~/linux-config source directory.
- .chezmoiignore: headless mode excludes most helper scripts.
- dot_config/fish/config.fish.tmpl: hardcoded home paths, desktop startup,
  and shortcut generation during shell startup.
- scripts/executable_sync-shortcuts: canonical alias generation.
- .chezmoiexternal.toml.tmpl and the root run_* hooks: external skills
  and installation dependencies.
- scripts/executable_codex: currently requires a local Graphiti sidecar.
Reference docs/smoke-tests.md when documenting the new verification steps.

Architecture
Use a small Bash bootstrap plus chezmoi for server configuration.
Cloud-init must invoke that same bootstrap. Terraform owns AWS resources.
Explain briefly why this meets the original Ansible-style automation goal.
Verify current official installation guidance before choosing commands and
dependency versions.

Support Ubuntu 24.04 LTS, Ubuntu 26.04 LTS, and Debian 13 on x86_64.
Keep distribution and architecture limitations explicit.

Implement in this order:

1. Server profile and regression coverage
Create a persistent VPS profile that installs the intended shell and AI
configuration while preserving existing desktop behavior. Correct home/user
assumptions, missing-directory handling, and headless script/hook exclusions.
Keep desktop startup and optional services out of the VPS startup path.
Core shared skills must work without desktop/design bootstrapping dependencies.

Fish must start cleanly for arbitrary usernames, including noninteractive SSH
commands. Generate shortcuts after configuration changes, and load them during
interactive startup. Preserve the existing canonical alias sources.

2. One-command bootstrap
Add scripts/executable_bootstrap-vps.sh and document a downloadable one-line
invocation plus execution from a checkout.

Install Git, curl/CA certificates, chezmoi, fish, tmux, ripgrep, fzf, Neovim,
and lsd. Install Codex and Claude using their supported native installers.
Use ~/linux-config for the checkout and configure chezmoi noninteractively.

Support an existing sudo-capable login account and root execution with an
explicit target user. Keep user files and CLI installations owned by that user.
Make fish the target account's login shell after validation.

Provide --help, --user, --repo, --ref, and a read-only --check mode.
Handle existing checkouts and configuration without destructive resets or
silent overwrites. Repeated successful runs must converge without duplicate
PATH entries, aliases, shell changes, or unnecessary reinstalls.

Report failures with actionable diagnostics and print a clear completion line
only after verification. Document the actual sudo requirements.

3. AI tools and configuration
Install Codex, Claude Code, and the repo's shared skills.
Provide VPS-compatible configuration so both CLIs launch without Graphiti,
Neo4j, a local model, or workstation-only paths and MCP services.
Preserve the existing workstation configuration.

Authentication remains a separate user action. Do not copy credentials or
place tokens in Git, cloud-init, Terraform variables, or state.

4. AWS provisioning
Add a standalone Terraform configuration under infra/aws/:
one EC2 instance, a dedicated VPC/public subnet, internet gateway, routing,
and SSH access restricted to a required caller-supplied CIDR.

Require AWS region and SSH public key inputs. Default to Ubuntu 26.04,
x86_64, a configurable t3.medium instance, and an encrypted 20 GiB root disk.
Use official Canonical images, IMDSv2, and an explicitly selected repository
revision for cloud-init.

Use local Terraform state for this single-operator starter; exclude state,
plan files, credentials, and real tfvars from Git. Commit the provider lockfile.
Provide outputs for the IP address and SSH command.

Create a reusable helper for plan, apply, status, and destroy. Explain AWS
authentication, required inputs, ongoing instance/storage/public-IP costs,
state backup, bootstrap logs, readiness checks, and teardown.
Creating an EC2 instance alone must not be reported as successful bootstrap.

Build and validate this code without launching or destroying AWS resources.

5. Verification and documentation
Start behavior changes with failing tests or executable reproductions.
Add a reusable test runner for fresh installs in disposable environments.
Cover all supported releases, a non-example-user account, root/sudo handling,
repeated runs, an existing dirty checkout, unsupported systems, download
failure, and interrupted installation recovery.

Verify fish syntax and quiet noninteractive startup; confirm a representative
abbreviation such as lc, required commands, correct ownership, and the login
shell. Check codex --version and claude --version without signing in or
making inference requests.

Run the relevant existing shell, shortcut, skill-link, and configuration
regressions. Run Terraform fmt -check, init -backend=false, validate, and
mocked-provider tests. Validate rendered cloud-init.

Provide a manual fresh-SSH-login check and cloud-init status/log checks.
Clearly distinguish disposable local verification from unexecuted AWS checks.

Update README.md, docs/smoke-tests.md, and the ExecPlan together.
Follow repository refresh-config requirements while protecting existing work;
do not use refresh-config as the fresh-server bootstrap.

Return the exact one-command installer invocation, AWS helper usage, automated
and manual test results, remaining limitations, and a suggested Conventional
Commit subject. Do not commit, push, authenticate accounts, or deploy.
