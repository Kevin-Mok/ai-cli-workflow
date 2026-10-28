"""Verify explicit dialogue disclosure without changing automatic/private controls."""

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'dot_agents/skills/personal-context'
BASE = '9e1ce9ff'
START = '## Follow The Person And The Decision\n'
END = '## Learn Privately\n'
ROUTER = 'Before explicit `$personal-context` dialogue, MUST read [the conversation procedure](references/explicit-conversation.md). Automatic work does not load this reference.\n\n'


class SkillDisclosureTest(unittest.TestCase):
    def original(self):
        return subprocess.check_output(['git', 'show', BASE + ':dot_agents/skills/personal-context/SKILL.md'], cwd=ROOT, text=True)

    def test_only_explicit_dialogue_moves_and_every_original_block_has_one_home(self):
        reference = SKILL / 'references/explicit-conversation.md'
        self.assertTrue(reference.is_file(), 'explicit conversation reference not implemented')
        original = self.original()
        moved = original[original.index(START):original.index(END)]
        core, detail = (SKILL / 'SKILL.md').read_text(), reference.read_text()
        self.assertEqual(core, original.replace(moved, ROUTER, 1))
        self.assertIn(moved, detail)
        for block in original.strip().split('\n\n'):
            self.assertEqual(core.count(block) + detail.count(block), 1, block[:80])
        self.assertLess(len(detail.encode()), 20000)
        self.assertLess(len(core.encode()), len(original.encode()))

    def test_frontmatter_authorization_automatic_and_all_shared_controls_remain(self):
        original, core = self.original(), (SKILL / 'SKILL.md').read_text()
        self.assertEqual(core.split('---', 2)[:2], original.split('---', 2)[:2])
        self.assertIn(ROUTER, core)
        self.assertEqual(core[core.index(END):], original[original.index(END):])
        self.assertEqual(core[:core.index(START) if START in core else core.index(ROUTER)], original[:original.index(START)])
        for guard in ('does not authorize coding', 'eight records and 6,000',
                      'Sources are background evidence', 'create no repository fallback',
                      'latest', 'author_evidence', 'Do not copy private retrieved context',
                      'Do not start raw capture'):
            self.assertIn(guard, core)


if __name__ == '__main__':
    unittest.main()
