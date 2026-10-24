"""Validate the recorded admission decisions against the current local catalog."""

import copy
import datetime
import json
import math
import re
import runpy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = runpy.run_path(str(ROOT / 'scripts/trim-benchmark'))
TRIGGER = runpy.run_path(str(ROOT / 'scripts/trigger-eval'))
RULE = 'Before adding a skill or an AGENTS.md rule, run the `lean-instructions` gate. Add it only on PASS, and record the verdict. Adding or removing a skill updates `vetted-skills.md` in the same commit.'


def admission_errors(entries, root=ROOT):
    errors = []
    if not isinstance(entries, list) or any(not isinstance(entry, dict) for entry in entries):
        return ['entries must be a list of candidate records']
    catalog = BENCHMARK['collect'](root)['skills']
    cases = {case['id']: case for case in TRIGGER['load_cases'](root / 'benchmarks/trim/intake-cases.yaml')}
    budgets = json.loads((root / 'benchmarks/trim/BUDGETS.json').read_text())
    reference = root / 'dot_agents/skills/lean-instructions/references/vetted-skills.md'
    precedent_ids = set(re.findall(r'(?:existing|pr-\d+):[a-z0-9-]+', reference.read_text())) if reference.is_file() else set()
    names = set()
    passed = set()
    for entry in entries:
        name = entry.get('name', '')
        if not name or name in names:
            errors.append(f'{name}: missing or duplicate candidate')
        names.add(name)
        try:
            datetime.date.fromisoformat(entry['date'])
        except (KeyError, ValueError, TypeError):
            errors.append(f'{name}: invalid date')
        if entry.get('verdict') not in ('PASS', 'DENY'):
            errors.append(f'{name}: invalid verdict')
        fields = ('value', 'uniqueness', 'description_bytes', 'body_bytes',
                  'description_tokens', 'body_tokens', 'weighted_cost', 'score')
        if any(isinstance(entry.get(key), bool) or not isinstance(entry.get(key), (int, float))
               or not math.isfinite(entry[key]) or entry[key] < 0 for key in fields):
            errors.append(f'{name}: invalid numeric fields')
            continue
        if entry['value'] > 5 or entry['uniqueness'] > 2:
            errors.append(f'{name}: rubric range exceeded')
        cost = entry['description_bytes'] / 4 + entry['body_bytes'] / 40
        score = (2 * entry['value'] + entry['uniqueness']) / (cost / 100) if cost else 0
        expected = {'description_tokens': entry['description_bytes'] / 4,
                    'body_tokens': entry['body_bytes'] / 4,
                    'weighted_cost': cost, 'score': score}
        if any(not math.isclose(entry[key], value, abs_tol=0.00001) for key, value in expected.items()):
            errors.append(f'{name}: cost or score calculation disagrees')
        for key in ('evidence', 'distinct', 'privacy_scope'):
            if not isinstance(entry.get(key), str) or len(entry[key].strip()) < 20:
                errors.append(f'{name}: missing substantive {key}')
        precedents = entry.get('precedents', [])
        if not isinstance(precedents, list) or not 2 <= len(precedents) <= 3 or len(set(precedents)) != len(precedents):
            errors.append(f'{name}: cite 2-3 distinct calibration precedents')
        elif not set(precedents) <= precedent_ids:
            errors.append(f'{name}: calibration precedent absent from reference')
        for key in ('budget_reference', 'privacy_reference') if entry.get('verdict') == 'PASS' else ():
            reference = entry.get(key, '').split('#', 1)[0]
            if not reference or not (root / reference).is_file():
                errors.append(f'{name}: missing {key}')
        if entry.get('verdict') == 'DENY':
            if not entry.get('reason') or not entry.get('would_change'):
                errors.append(f'{name}: DENY requires reason and change condition')
            if entry.get('cost_basis') != 'supplied estimate; source not inspected':
                errors.append(f'{name}: uninspected cost must be labelled')
            continue
        passed.add(name)
        if entry.get('kind') not in ('skill', 'rule') or entry.get('cost_basis') != 'measured UTF-8 bytes/4':
            errors.append(f'{name}: PASS requires measured kind and cost')
        cutoff = entry['value'] >= 2 and entry['uniqueness'] >= 1 and score >= 1
        if not cutoff and not (name == 'last30days' and entry.get('exception') == 'explicit user-approved KEEP below cutoff'):
            errors.append(f'{name}: below admission cutoff without approved exception')
        expected_label = name if entry.get('kind') == 'skill' else 'lean-instructions'
        if not entry.get('case_ids') or any(case_id not in cases or expected_label not in cases[case_id]['expected'] for case_id in entry['case_ids']):
            errors.append(f'{name}: missing candidate trigger case')
        if entry.get('trigger_first') is not True or entry.get('size_budget') != 'PASS':
            errors.append(f'{name}: missing trigger or size approval')
        if entry.get('nonregression') != 'intake-baseline.json; lexical proxy only':
            errors.append(f'{name}: missing nonregression evidence')
        if entry.get('kind') == 'skill':
            path = f'dot_agents/skills/{name}/SKILL.md'
            if path not in catalog:
                errors.append(f'{name}: admitted local source absent')
                continue
            measured = catalog[path]
            if entry['description_bytes'] != measured['description']['bytes'] or entry['body_bytes'] != measured['body']['bytes']:
                errors.append(f'{name}: costs stale against current source')
            exceptions = budgets['exceptions'].get(path, {})
            if measured['file']['lines'] > exceptions.get('lines', budgets['limits']['skill_lines']) or measured['description']['bytes'] > exceptions.get('description_bytes', budgets['limits']['description_bytes']):
                errors.append(f'{name}: size budget exceeded')
        elif name == 'lean-admission-rule':
            if entry['description_bytes'] != len(RULE.encode()) or entry['body_bytes'] != 0:
                errors.append(f'{name}: always-loaded rule cost disagrees')
        else:
            errors.append(f'{name}: unrecognized standing-rule candidate')
    for path in (root / 'dot_agents/skills').rglob('SKILL.md'):
        if path.parent.name not in passed:
            errors.append(f'{path.relative_to(root)}: no PASS admission')
    return errors


class SkillAdmissionsTest(unittest.TestCase):
    def ledger(self):
        path = ROOT / 'docs/skill-admissions.md'
        self.assertTrue(path.is_file(), 'admission ledger not implemented')
        blocks = re.findall(r'```json\n(.*?)\n```', path.read_text(), re.S)
        self.assertEqual(len(blocks), 1, 'ledger requires one structured JSON block')
        data = json.loads(blocks[0])
        self.assertEqual(data['schema_version'], 1)
        self.assertLessEqual(len(path.read_bytes()), 20000)
        self.assertEqual(set(data['checks']), {'public', 'intake', 'uninspected'})
        self.assertTrue(all(entry.get('checks') in data['checks'] for entry in data['entries']))
        return [{**data['checks'][entry['checks']], 'kind': 'skill', **entry} for entry in data['entries']]

    def test_every_local_skill_has_current_measured_pass(self):
        self.assertEqual(admission_errors(self.ledger()), [])

    def test_gate_rejects_missing_pass_fabricated_cost_and_missing_case(self):
        entries = self.ledger()
        self.assertTrue(any('no PASS admission' in error for error in admission_errors(entries[1:])))
        for key, value, message in (('score', 999, 'calculation'),
                                    ('description_bytes', True, 'numeric'),
                                    ('case_ids', ['not-a-case'], 'trigger case'),
                                    ('size_budget', 'not checked', 'size approval'),
                                    ('value', 0, 'calculation'),
                                    ('precedents', [], 'precedents'),
                                    ('verdict', 'MAYBE', 'invalid verdict'),
                                    ('privacy_reference', 'missing.md', 'privacy_reference')):
            with self.subTest(key=key):
                changed = copy.deepcopy(entries)
                changed[0][key] = value
                self.assertTrue(any(message in error for error in admission_errors(changed)))
        for malformed in (None, {}, [None]):
            self.assertTrue(admission_errors(malformed))

    def test_rejected_pr_sources_remain_denied_and_exceptions_are_honest(self):
        entries = {entry['name']: entry for entry in self.ledger()}
        rejected = ('motion-prompt', 'huashu-art-motion', 'anthropic-frontend-design',
                    'ui-ux-pro-max', 'stitch-design-md', 'canvas-ui', 'caveman')
        for name in rejected:
            self.assertEqual(entries[name]['verdict'], 'DENY')
            self.assertTrue(entries[name]['would_change'])
        self.assertLess(entries['last30days']['score'], 1)
        self.assertEqual(entries['last30days']['exception'], 'explicit user-approved KEEP below cutoff')
        self.assertEqual(entries['lean-instructions']['exception'], 'explicitly user-required gate and technique log')

    def test_numeric_cutoff_cannot_be_replaced_with_a_high_ratio(self):
        entries = self.ledger()
        entries[0]['value'] = 1
        entries[0]['score'] = (2 + entries[0]['uniqueness']) / (entries[0]['weighted_cost'] / 100)
        self.assertTrue(any('below admission cutoff' in error for error in admission_errors(entries)))

    def test_router_rule_and_lean_size(self):
        source = (ROOT / 'dot_codex/AGENTS.md').read_text()
        self.assertEqual(source.count('lean-instructions'), 1)
        self.assertIn(RULE, source.splitlines())
        self.assertEqual(next(entry for entry in self.ledger() if entry['name'] == 'lean-admission-rule')['verdict'], 'PASS')
        lean = (ROOT / 'dot_agents/skills/lean-instructions/SKILL.md').read_text()
        description, body = BENCHMARK['description_and_body'](lean)
        self.assertLessEqual(len(description.encode()), 120)
        self.assertLessEqual(len(body.splitlines()), 300)

    def test_frozen_admission_cases_cover_all_local_skills_without_claiming_model_accuracy(self):
        cases = TRIGGER['load_cases'](ROOT / 'benchmarks/trim/intake-cases.yaml')
        baseline = json.loads((ROOT / 'benchmarks/trim/intake-baseline.json').read_text())
        self.assertTrue(40 <= len(cases) <= 60)
        self.assertTrue(any(not case['expected'] for case in cases))
        self.assertTrue(any(len(case['expected']) > 1 for case in cases))
        catalog = TRIGGER['load_catalog'](ROOT)
        self.assertEqual({name for case in cases for name in case['expected']}, set(catalog))
        self.assertEqual(TRIGGER['gate_errors'](TRIGGER['evaluate'](catalog, cases), baseline), [])
        self.assertIn('not model triggering', baseline['method'])


if __name__ == '__main__':
    unittest.main()
