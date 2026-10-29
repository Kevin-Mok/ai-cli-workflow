# Hallmark source record

This package vendors Hallmark v2 for explicit invocation. Review the pinned source and license before updating; preserve the local invocation policy.

- Repository: https://github.com/nutlope/hallmark
- Version: 2.0.0.
- Fixed commit: [7ec868225c6caa040558c321ee0fefa0e73f83a8](https://github.com/nutlope/hallmark/tree/7ec868225c6caa040558c321ee0fefa0e73f83a8).
- Source directory: `skills/hallmark/`, copied in full including references, themes, scripts and fixtures.
- License: MIT, copyright 2026 Hallmark contributors; LICENSE copied verbatim. Redistribution is permitted with the copyright and permission notice retained.
- Local changes: added `disable-model-invocation: true` to SKILL.md and set `policy.allow_implicit_invocation: false` in agents/openai.yaml. Added a source-record link in SKILL.md. In references/brand-truth.md, replaced numeric private-network examples with equivalent range names to pass the public privacy gate while retaining the fetch restrictions. All other upstream files are byte-identical.

Invoke with `$hallmark` in Codex or `/hallmark` in Claude Code. Copying this package does not run its installers or install hooks. Run scripts only when needed: image generation sends prompts to Together AI using `TOGETHER_API_KEY`; saving photo suggestions downloads external images. Generated files and logs belong in the target project. Review external asset licenses before redistribution; the MIT notice covers this package, not downloaded assets or fonts.

Update by selecting an immutable upstream commit, reviewing its license and diff, copying the same directory, reapplying the two invocation settings, updating this record and rerunning the upstream reference checks plus the repository privacy gate. Do not run the upstream installer to update this vendored source.
