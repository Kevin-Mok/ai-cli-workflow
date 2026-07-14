"""Static paths and patterns that define the tracked vault health contract."""

from __future__ import annotations

import re


REQUIRED_PATHS = (
    "README.md",
    ".obsidian/.gitignore",
    ".obsidian/app.json",
    ".obsidian/appearance.json",
    ".obsidian/snippets/example-user.css",
    "00 Context/About Me.md",
    "00 Context/Writing Style.md",
    "00 Context/Memory Map.md",
    "00 Context/Decisions.md",
    "00 Context/Learnings.md",
    "00 Context/AI Workflow.md",
    "00 Context/Audience and Privacy.md",
    "00 Context/External Locations.md",
    "01 Inbox/Brain Dump.md",
    "02 Projects/Linux Config AI Workflow.md",
    "02 Projects/ExampleProject.md",
    "02 Projects/Beginner Python Teaching Sites.md",
    "03 Areas/Work and Career.md",
    "03 Areas/AI Workflow.md",
    "03 Areas/Teaching.md",
    "03 Areas/Wellbeing.md",
    "03 Areas/Relationship.md",
    "04 Resources/AI Agents and Prompting.md",
    "04 Resources/Education Product Design.md",
    "04 Resources/CEMC Math Contest Prep.md",
    "04 Resources/Beginner Programming Pedagogy.md",
    "04 Resources/Software Architecture and UX.md",
    "04 Resources/Linux Automation.md",
    "04 Resources/Parent Facing Sales and Marketing.md",
    "04 Resources/CBT and Wellbeing.md",
    "05 Daily Notes/2026-07-14.md",
    "06 Archive/README.md",
    "06 Archive/backups/README.md",
    "07 Attachments/README.md",
    "07 Attachments/External Media Index.md",
)
PLACEHOLDER_RE = re.compile(
    r"\{\{[^}\n]+\}\}|(?i:\b(?:TBD|TODO)\b|replace with|your name here)"
)
STATUS_PREFIXES = (
    "01 Inbox/",
    "02 Projects/",
    "03 Areas/",
    "04 Resources/",
    "05 Daily Notes/",
)
IMPORT_PREFIX = "06 Archive/Imports/"
RECOVERY_NAME_RE = re.compile(r"^\..+\.[0-9a-f]{24}\.tmp$")
CANONICAL_OWNERS = (
    "dot_agents/skills/feedback-memory/feedback.log",
    "tasks/lessons.md",
)
