# Commit Plan Push Design

## Purpose

Provide a global `commit-plan-push` skill for explicit requests to turn the
current intended dirty Git worktree into a safe, chronological commit series
and push it.

## Decision

The skill is a companion to `commit-plan` and `commit-dirty`, installed at
`/home/example/.agents/skills/commit-plan-push/SKILL.md`. It performs the
planning work before any Git write, stops on ambiguous mixed changes, verifies
the intended work, runs the mandatory README gate, creates each reviewed
commit oldest-to-newest, and pushes the configured upstream only after the
whole verified series succeeds. Once those safety checks pass, it executes the
inferred commit series and final push without requesting a second user
confirmation.

## Scope

The skill describes a Git workflow only. It does not add a command, modify
repository configuration, rewrite history, or push partial multi-commit work.

## Validation

Use a temporary contract test: it must fail before the skill exists, then
confirm the completed skill exposes the required trigger wording, planning,
safety stops, verification, commit ordering, delayed push cadence, and result
reporting, including automatic execution after the safety checks pass.
