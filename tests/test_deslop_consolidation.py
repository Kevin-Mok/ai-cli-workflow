"""Keep the useful de-slop checks in the automatic frontend workflow."""

import json
import runpy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DeslopConsolidationTest(unittest.TestCase):
    def test_duplicate_skill_is_removed_from_the_source_catalog(self):
        self.assertFalse((ROOT / 'dot_agents/skills/ai-ux-deslop').exists())
        catalog = runpy.run_path(str(ROOT / 'scripts/trigger-eval'))['load_catalog'](ROOT)
        self.assertNotIn('ai-ux-deslop', catalog)
        self.assertIn('frontend-design', catalog)

    def test_automatic_frontend_review_keeps_the_two_useful_checks_and_safeguards(self):
        source = (ROOT / 'dot_agents/skills/frontend-design/SKILL.md').read_text().lower()
        self.assertTrue('inventory' in source, 'Frontend review must retain: inventory')
        self.assertTrue('secondary text' in source, 'Frontend review must retain: secondary text')
        self.assertTrue('reviewer' in source, 'Frontend review must retain: reviewer')
        self.assertTrue('without explanation' in source, 'Frontend review must retain: without explanation')
        self.assertTrue('persistent labels' in source, 'Frontend review must retain: persistent labels')
        self.assertTrue('required' in source, 'Frontend review must retain: required')
        self.assertNotIn('repeat until clean', source)
        self.assertNotIn('at most one short line', source)

    def test_survivor_corpus_does_not_relabel_retired_skill_cases(self):
        old = json.loads((ROOT / 'benchmarks/trim/overnight-cases.yaml').read_text())['cases']
        current = json.loads((ROOT / 'benchmarks/trim/deslop-survivor-cases.yaml').read_text())['cases']
        survivors = [case for case in old if not case['id'].startswith('overnight-ai-ux-')]
        self.assertEqual(current, survivors)
        self.assertEqual(len(old), 54)
        self.assertEqual(len(current), 51)

    def test_survivor_routing_keeps_every_previously_correct_case(self):
        api = runpy.run_path(str(ROOT / 'scripts/trigger-eval'))
        cases = api['load_cases'](ROOT / 'benchmarks/trim/deslop-survivor-cases.yaml')
        before = json.loads((ROOT / 'benchmarks/trim/deslop-survivor-before.json').read_text())
        after = api['evaluate'](api['load_catalog'](ROOT), cases)
        correct_before = {case['id'] for case in before['per_case'] if case['exact_match']}
        correct_after = {case['id'] for case in after['per_case'] if case['exact_match']}
        self.assertLessEqual(correct_before, correct_after)
        self.assertEqual(api['gate_errors'](after, before), [])


if __name__ == '__main__':
    unittest.main()
