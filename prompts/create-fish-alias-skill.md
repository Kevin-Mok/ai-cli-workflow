# Create a fish shortcut skill

Create and install a reusable Codex skill in /home/example/linux-config that lets the user provide only an abbreviation followed by its command or path. Choose a concise descriptive skill name using existing repo conventions. This is a request to create the skill, not to modify metaprompt-run.

## User contract

Example future invocation: `$fish-alias cbn codex-time burn day` (replace the illustrative skill name with the final name). It must add `cbn "codex-time burn day"` to the appropriate existing section of aliases/key_aliases.tmpl. Treat cbn as the abbreviation and preserve the complete remainder as the command; do not require the user to name the template or section. Use this example in documentation and validation; do not install the example into live aliases solely because it was supplied as an example.

Support the repository's three shortcut sources: aliases/key_aliases.tmpl for commands, aliases/key_dirs.tmpl for directory shortcuts, and aliases/key_files.tmpl for file shortcuts. Inspect their actual format and generator behavior before defining routing. Infer the best existing section from nearby related entries. Ask only when missing command/path or genuinely ambiguous intent prevents a correct change.

For the requested abbreviation, find active conflicting definitions across relevant shortcut sources and account for how generation and template conditions affect fish conflicts. Preserve conflicting entries in place by inserting exactly `# ` at the start of their lines; never delete them. Leave already commented entries and unrelated abbreviations untouched. An identical active mapping is a no-op, with no duplicate or extra comment. Preserve quoting, shell metacharacters, paths with spaces, template directives, and section markers. Do not execute the supplied command to test it.

## Implementation and verification

Read AGENTS.md and dot_codex/AGENTS.md, relevant nested instructions, .agent/PLANS.md, tasks/lessons.md, and canonical feedback before changes. Use the skill-creator workflow and tracked dot_agents/skills sources, and follow the existing installation and refresh conventions. Inspect the shortcut generator and tests to ground behavior. There is substantial pre-existing dirty work, including aliases/key_aliases.tmpl, aliases/key_dirs.tmpl, README.md, docs/smoke-tests.md, tasks/lessons.md, and postmortem memory; capture current status and preserve unrelated hunks.

Implement the smallest complete skill and only supporting helpers that materially improve safety. Record a decision-complete plan for non-trivial work. Verify the defining behavior with isolated fixtures before implementation, then run focused checks for command, directory, and file routing; section selection; cross-source abbreviation conflicts; exact '# ' preservation; identical mapping idempotence; missing inputs; quoting; template conditions; and unrelated content preservation. Validate the skill and generated fish syntax using existing repo checks, without running user commands. Update docs/smoke-tests.md with concrete Action/Expected examples, and keep relevant README and plan documentation accurate. Run refresh-config for tracked configuration changes and verify installation as applicable. No commit, push, or worktree was requested.

Report the final skill name, canonical source link, paste-ready usage for cbn and codex-time burn day, verified results, and any actual limitations. Complete the implementation in this conversation; do not invoke metaprompt-run again.
