# Postmortem: Design Skills Timer Copy-Rename Residue

**Incident date:** 2026-08-19
**Severity:** Low — command help text only
**Status:** Resolved

## Symptom and impact

The new setup utility ran correctly but advertised
`setup-design-skills-release-timer` instead of its installed command,
`setup-design-skills-timer`. This could mislead an operator; no timer,
source, credential, or generated media behavior was affected.

## Evidence and root cause

The exact-name regression test failed against the copied utility's `--help`
output. The original Superpowers setup script was adapted with broad token
replacement, which did not rewrite the compound command name.

## Resolution and verification

Added an assertion for `usage: setup-design-skills-timer`, then replaced the
two residual source strings, deployed the exact managed target, and reran the
test. The test passed and the installed `--help` output now uses the correct
name.

## Follow-up

When adapting named utilities, test both their behavior and their public
command identity; broad text substitution is not sufficient evidence.
