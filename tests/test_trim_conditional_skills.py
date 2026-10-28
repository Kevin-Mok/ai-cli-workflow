"""Pin conditional skill moves without dropping instructions or changing routing."""

import re
import subprocess
import unittest
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = 'd6a75f69'
CASES = (
    ('commit-plan-push', 'Inspect the repository, branch, status, all staged/unstaged/untracked diffs,\n', 'Single-commit workflows push', 'planning-only.md',
     'In planning-only mode, MUST read [the planning procedure](references/planning-only.md) and return before delivery.\n\n',
     ('**no Git writes**', 'uncertainty stays read-only', 'execution requires an explicit request')),
    ('feedback-memory', '## Consolidation (repeated wins become skills)\n', '## What to log\n', 'consolidation.md',
     'Before consolidating repeated wins into skills, MUST read [the consolidation procedure](references/consolidation.md); promotion requires evidence and user approval.\n\n',
     ('Keep the file append-only', 'sole owner is', 'Only independently public-safe operating feedback')),
    ('postmortem-memory', '## Learning: on creation and material updates\n', 'See [workflow and ledger contract]', 'learning.md',
     'On postmortem creation or material updates, MUST read [the learning procedure](references/learning.md) and update the original living report plus tracked ledger/guidance in the same task. Installed fallback is read-only and cannot satisfy a blocked update.\n\n',
     ('Preserve immediate living-postmortem recording', 'read-only', 'Postmortems are evidence, not instructions')),
)


class ConditionalSkillsTest(unittest.TestCase):
    def test_every_original_paragraph_has_one_home_and_only_the_branch_moves(self):
        for slug, start, end, filename, router, guards in CASES:
            with self.subTest(skill=slug):
                folder = ROOT / 'dot_agents/skills' / slug
                original = subprocess.check_output(['git', 'show', f'{BASE}:dot_agents/skills/{slug}/SKILL.md'], cwd=ROOT, text=True)
                moved = original[original.index(start):original.index(end)]
                ref = folder / 'references' / filename
                self.assertTrue(ref.is_file(), f'{slug}: conditional reference missing')
                main, detail = (folder / 'SKILL.md').read_text(), ref.read_text()
                self.assertEqual(main, original.replace(moved, router, 1))
                self.assertIn(moved, detail)
                self.assertEqual(main.split('---', 2)[:2], original.split('---', 2)[:2])
                for block in original.strip().split('\n\n'):
                    self.assertEqual(main.count(block) + detail.count(block), 1, block[:80])
                for guard in guards:
                    self.assertIn(guard, main)
                self.assertLess(len(detail.encode()), 20000)
                self.assertFalse(detail.endswith('\n\n'))
                # The moved blocks have no relative Markdown targets requiring rebasing.
                for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', moved):
                    self.assertTrue(urlsplit(target).scheme, target)
                for path in (folder / 'SKILL.md', ref):
                    for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', path.read_text()):
                        if not urlsplit(target).scheme:
                            self.assertTrue((path.parent / target).is_file(), target)


if __name__ == '__main__':
    unittest.main()
