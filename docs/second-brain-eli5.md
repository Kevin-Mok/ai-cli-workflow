# Second Brain, explained like you are five

Second Brain is a little notebook that helps future-you pick up where
present-you stopped.

It is not a place to save everything. It is a place to save the few things
that would be annoying to rediscover: what you were trying to do, what you
learned, and what should happen next.

## The whole idea

Think of a work session like leaving a trail through the woods:

```text
start -> choose one destination -> leave useful trail markers -> leave a sign for tomorrow
```

Second Brain keeps those trail markers and the final sign in a predictable
place, so you or Codex do not have to guess next time.

## The easiest way to use it

Tell Codex when you are starting meaningful work:

> Help me start a Second Brain session for this task.

Codex checks the small amount of context that matters, then suggests **one
finish line** for today. For example:

> Today: make the Fish configuration change persist.
>
> Done when: the tracked template and a verification check show the setting
> survives chezmoi.

Say yes only if that is really the one result you want. Once you confirm it,
it becomes the focus for the day. You do not need a huge to-do list here.

## While you work

Tell Codex about discoveries that future-you would otherwise need to find
again. Good examples:

- "This file is generated; edit the template instead."
- "I tried this command and it failed because the parent folder was missing."
- "The next person needs to run this check after changing the config."

Codex can capture those rough notes privately. They are scratchpad notes, not
Git-tracked documentation.

You can also look at the short current-state summary yourself:

```bash
second-brain status --format text
```

Use it when you want the answer to: "What was I working on?"

## When you stop

Tell Codex:

> Help me close out my Second Brain session.

Codex will show you a short handoff before saving it:

- Planned: the focus you approved at the start.
- Completed: what actually happened.
- Evidence: the file, link, or other thing that proves it.
- Blocker: what is still in the way, or "none."

Confirm that summary only when it is accurate. Tomorrow, that handoff is your
answer to: "Where do I continue?"

## Two kinds of notes: keep these separate

| Kind | Where it lives | What it is for |
| --- | --- | --- |
| Rough session capture | Private computer state, outside Git | Messy discoveries and temporary context |
| Durable Second Brain note | `second-brain/`, tracked in Git | Clean, safe context worth reusing or reviewing |

Never put passwords, API keys, tokens, proprietary code, raw journal entries,
or sensitive personal details in `second-brain/`.

## Where things go

You do not need to memorize every folder. This small map is enough:

- `00 Context`: stable information about you, decisions, and how the system
  should remember things.
- `01 Inbox`: a safe note that needs sorting later.
- `02 Projects`: work with a finish line.
- `03 Areas`: responsibilities you keep doing, such as work or teaching.
- `04 Resources`: useful reference material.
- `05 Daily Notes`: what happened on a particular day.

The [vault front door](../second-brain/README.md) links to the rest when you
need it.

## If something feels wrong

Run the safe health check:

```bash
second-brain doctor --format text --check
```

It checks the vault's structure and safety rules without changing anything.
If it reports a problem, stop and fix that problem before trusting a
checkpoint.

## The tiny daily routine

1. Start: ask Codex to begin a Second Brain session.
2. Pick one finish line and confirm it.
3. Share important discoveries as you work.
4. Stop: ask Codex for a closeout, check the summary, and confirm it.

That is all. Second Brain is not extra homework; it is a note to make tomorrow
less confusing.

For the command-level reference, see the [operator guide](second-brain.md).
