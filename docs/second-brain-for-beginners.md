# Second Brain: the beginner version

You do not use Second Brain to store every thought or to make the computer think for you.

You use it so that, when you return to work later, you do not have to remember:

- What you were doing
- Why you were doing it
- What you already tried
- What  finished  means
- What to do next

It is a written handoff from your current self to your future self.

## The workflow in one sentence

At the beginning, say what you are doing. During the work, save important context. At the end, write down what happened and what comes next.

~~~text
start work -> remember the context -> do the work -> leave a handoff
~~~

## A real example

Suppose you are fixing a Linux-config script.

Without Second Brain:

- You stop for the day.
- Tomorrow you open the repo.
- You wonder which file you changed.
- You forget why the change was needed.
- You repeat yesterday's investigation.

With Second Brain:

- You record:  The Fish setup command must update the chezmoi source template. 
- You choose one outcome:  Make the command persist XDG_STATE_HOME in Fish. 
- You do the work.
- You record:  Updated the script; next step is chezmoi apply and a Fish check. 
- Tomorrow, the status and daily note remind you where to continue.

That is the whole purpose: less re-discovery and cleaner handoffs.

## What you should do

You only need four actions.

### 1. Start with status

When you begin working in the repo, run:

~~~bash
second-brain status --format text
~~~

Think of this as asking:

>  What was I working on, and what context should I remember before I start? 

Read the output before opening random files.

### 2. Capture important context

When something matters, save it:

~~~bash
second-brain capture --kind raw-session --payload -
~~~

The command waits for a JSON note. The simplest way to understand the note is:

>  What would future me be annoyed to have to rediscover? 

Examples of useful things to capture:

-  The script writes to the live Fish config, but chezmoi will overwrite it. 
-  The timer setup failed because the runtime parent directory was missing. 
-  The user wants raw notes private and only sanitized conclusions tracked. 
-  I tried chezmoi apply; it changed the generated Fish config. 

Raw captures are private. They are your scratchpad, not polished documentation.

Here is one complete capture:

~~~bash
second-brain capture --kind raw-session --payload - <<'JSON'
{
  "schema_version": 1,
  "event_id": "fish-config-20260715-01",
  "source": "terminal",
  "timestamp": "2026-07-15T14:00:00-04:00",
  "session_id": "fish-config-20260715",
  "role": "user",
  "text": "The Fish config is managed by chezmoi. Changes must be made in ~/linux-config/dot_config/fish/config.fish.tmpl and then applied."
}
JSON
~~~

You do not need to capture every command. Capture discoveries, decisions, failures, and useful next steps.

### 3. Choose one outcome with focus

A focus is not a list of everything you might do. It is the one result you want from the session.

Run:

~~~bash
second-brain focus --payload -
~~~

Use it when you are starting a meaningful work session.

Example:

~~~bash
second-brain focus --payload - <<'JSON'
{
  "schema_version": 1,
  "event_id": "example-project-focus-20260715",
  "source": "terminal",
  "timestamp": "2026-07-15T14:05:00-04:00",
  "date": "2026-07-15",
  "project": "ExampleProject",
  "outcome": "Make the Second Brain beginner guide understandable.",
  "done_when": "A new user can explain the purpose and follow the basic commands.",
  "evidence": "The guide contains a plain-language workflow and working examples.",
  "confirmed": true
}
JSON
~~~

Translate the fields like this:

- outcome: What result am I trying to produce?
- done_when: How will I know it is finished?
- evidence: What will prove that I finished it?

If you have ten possible tasks, put the other nine in a private capture. Keep one focus.

### 4. Leave a handoff with closeout

When you stop working, tell your future self what happened:

~~~bash
second-brain closeout --payload -
~~~

Example:

~~~bash
second-brain closeout --payload - <<'JSON'
{
  "schema_version": 1,
  "event_id": "example-project-closeout-20260715",
  "source": "terminal",
  "timestamp": "2026-07-15T16:00:00-04:00",
  "date": "2026-07-15",
  "project": "ExampleProject",
  "planned": "Make the Second Brain beginner guide understandable.",
  "completed": "Rewrote the guide around a normal work session and added command examples.",
  "evidence": "The beginner guide now explains the purpose before the implementation details.",
  "blocker": "",
  "decisions": [],
  "open": [],
  "next": "Read the guide once as a new user and simplify anything still unclear.",
  "confirmed": true
}
JSON
~~~

Important: planned must exactly match the outcome from your focus.

A good closeout answers:

- What did I finish?
- What proof do I have?
- What is still open?
- What should I do next time?

## What happens the next time?

You run:

~~~bash
second-brain status --format text
~~~

Then you read the recent context and continue from the recorded next step instead of starting from a blank page.

That is how Second Brain helps your workflow. It shortens the distance between:

~~~text
 I stopped working yesterday 
~~~

and:

~~~text
 I know exactly where to continue today 
~~~

## Where the information lives

~~~text
~/linux-config/second-brain/
~~~

This is the tracked, reviewable part of the system. It contains durable project context, daily notes, and sanitized decisions.

~~~text
~/second-brain/raw/
~~~

This is private scratch state. It is for raw session captures and details that should not go into Git.

Never put passwords, API keys, tokens, or sensitive personal information in the tracked vault.

## Do I need to use it for everything?

No.

Use it when:

- You are working on something that will continue later.
- You learned something that future you would need again.
- You made a decision and want to remember why.
- You are handing work to another session or person.
- You want a clear record of progress.

Do not use it for:

- A one-line command you will never need again.
- Secrets or credentials.
- Every tiny thought.
- Replacing Taskwarrior for ordinary task tracking.

## If something is broken

Run:

~~~bash
second-brain doctor --format text --check
~~~

This checks the vault's structure, privacy rules, and ownership rules.

For a safe checkpoint preview:

~~~bash
second-brain checkpoint --dry-run
~~~

For the full command reference, see [docs/second-brain.md](second-brain.md).
