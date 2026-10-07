# Metaprompt runner inspection sandbox startup failure

The restricted command runner failed before repository inspection. Use approved scoped execution for this task; host sandbox repair remains separate.

## Symptom and impact

The first two read-only commands returned `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. Neither shell started; no files changed. Skill inspection and status capture were temporarily blocked.

## Evidence and lookup

Query: `bwrap loopback Failed RTM_NEWADDR`. The tracked memory returned `ext-sandbox-loopback`, verified_workaround. Its execution-environments reference applies: two independent harmless reads failed identically before execution. An approved require_escalated command then ran `pwd`, `git status --short` and required instruction reads successfully (exit 0).

## Root cause and resolution

Restricted runner loopback initialization is denied by the host; repository code is not implicated. Scoped approved execution is a verified workaround, not a repair to default sandbox startup.

## Current status, verification and follow-up

Status: verified_workaround. Repository status and source reads now succeed with scoped escalation. Continue necessary commands on that route; preserve pre-existing dirty files. Host sandbox repair remains outside this skill task. No new reusable learning beyond ext-sandbox-loopback; register this reviewed report without changing existing guidance.
