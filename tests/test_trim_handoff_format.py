"""Keep shared handoff safeguards while disclosing only its artifact template."""

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'dot_agents/skills/context-handoff'
BASE = 'f9930fc8'
DIRECTIVE = 'Return only the handoff, at most 600 words, using the eight headings below in order.\n\n'
ROUTER = 'Before creating or returning a handoff artifact, MUST read [the handoff format](references/handoff-format.md). Long-task setup and resume do not load the template.\n\n'


class HandoffFormatTest(unittest.TestCase):
    def test_only_format_payload_moves_with_every_original_paragraph_preserved(self):
        original = subprocess.check_output(['git', 'show', BASE + ':dot_agents/skills/context-handoff/SKILL.md'], cwd=ROOT, text=True)
        template = re.search(r'```markdown\n.*?```\n\n', original, re.S)[0]
        reference = SKILL / 'references/handoff-format.md'
        self.assertTrue(reference.is_file(), 'on-demand handoff format is not implemented')
        main, detail = (SKILL / 'SKILL.md').read_text(), reference.read_text()
        self.assertEqual(main, original.replace(DIRECTIVE, ROUTER, 1).replace(template, '', 1))
        self.assertIn(DIRECTIVE, detail)
        self.assertIn(template, detail)
        self.assertEqual(main.split('---', 2)[:2], original.split('---', 2)[:2])
        for block in original.strip().split('\n\n'):
            self.assertEqual(main.count(block) + detail.count(block), 1, block[:80])
        self.assertLess(len(main.encode()), len(original.encode()) - 400)
        self.assertLess(len(detail.encode()), 20000)
        self.assertFalse(detail.endswith('\n\n'))
        for paragraph in original.split('\n\n'):
            if paragraph not in (DIRECTIVE.rstrip('\n'),) and paragraph not in template and not paragraph.startswith('```'):
                self.assertIn(paragraph, main)
        for guard in ('## Long-task procedure', 'Create a goal only when the user requested one',
                      'Do not publish, push, send, or deploy', 'Assign `DC#` IDs',
                      'Use None only after an explicit check', 'Group repeated failures',
                      'Every next action includes', 'Never use anaphora'):
            self.assertIn(guard, main)
        for path in (SKILL / 'SKILL.md', reference):
            unfenced = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
            for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', unfenced):
                self.assertTrue((path.parent / target).is_file(), target)


if __name__ == '__main__':
    unittest.main()
