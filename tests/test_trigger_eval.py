import json
import os
import pty
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/trigger-eval'


class TriggerEvalTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'trigger-eval CLI is not implemented')
        self.module = runpy.run_path(str(SCRIPT))

    def active_paths(self):
        path = ROOT / 'benchmarks/trim/trigger-active.json'
        self.assertTrue(path.is_file(), 'active phase pointer is not implemented')
        selection = json.loads(path.read_text())
        return ROOT / selection['cases'], ROOT / selection['baseline']

    def cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)

    def test_catalog_uses_only_name_and_description(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / 'dot_agents/skills/example/SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('---\nname: "example"\ndescription: >-\n  Render diagrams\n  from text.\n---\nSECRET BODY TOKEN\n')
            self.assertEqual(self.module['load_catalog'](root), {'example': 'Render diagrams from text.'})
            skill.write_text(skill.read_text().replace('SECRET BODY TOKEN', 'different body'))
            self.assertEqual(self.module['load_catalog'](root), {'example': 'Render diagrams from text.'})

    def test_active_keep_list_labels_are_valid_and_cases_unchanged(self):
        cases_path, baseline_path = self.active_paths()
        active = self.module['load_cases'](cases_path)
        archived = {case['id']: case for case in self.module['load_cases'](ROOT / 'benchmarks/trim/trigger-cases.yaml')}
        catalog = self.module['load_catalog'](ROOT)
        self.assertTrue(all(set(case['expected']) <= catalog.keys() for case in active))
        retained = self.module['load_cases'](ROOT / 'benchmarks/trim/cull-keep-cases.yaml')
        self.assertTrue(all(case == archived[case['id']] for case in retained))
        self.assertTrue(all(case in active for case in retained))
        frozen = json.loads(baseline_path.read_text())
        self.assertEqual(frozen['case_count'], 46)
        self.assertEqual(frozen['exact_matches'], 41)
        cull = json.loads((ROOT / 'benchmarks/trim/cull-keep-baseline.json').read_text())
        self.assertEqual((cull['case_count'], cull['exact_matches']), (17, 13))
        self.assertEqual(self.module['digest'](active), frozen['cases_sha256'])

    def test_default_selection_uses_pointer_and_falls_back_to_archive(self):
        self.assertTrue(callable(self.module.get('default_selection')), 'default selection is not implemented')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            selection = self.module['default_selection'](root)
            self.assertEqual(selection['cases'], root / 'benchmarks/trim/trigger-cases.yaml')
            self.assertEqual(selection['baseline'], root / 'benchmarks/trim/trigger-baseline.json')
            pointer = root / 'benchmarks/trim/trigger-active.json'
            pointer.parent.mkdir(parents=True)
            pointer.write_text(json.dumps({'cases': 'keep.yaml', 'baseline': 'keep.json', 'scope': 'approved keep-list subset'}))
            selection = self.module['default_selection'](root)
            self.assertEqual(selection['cases'], root / 'keep.yaml')
            self.assertEqual(selection['baseline'], root / 'keep.json')
            self.assertIn('keep-list', selection['scope'])
            pointer.write_text(json.dumps({'cases': '../outside.yaml', 'baseline': 'keep.json', 'scope': 'invalid'}))
            with self.assertRaises(ValueError):
                self.module['default_selection'](root)

    def test_explicit_cases_and_comparison_override_active_defaults(self):
        cases_path, baseline_path = self.active_paths()
        result = self.cli('--json', '--check', '--cases', str(cases_path), '--baseline', str(baseline_path))
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertIn('Explicit case set', report['scope'])
        result = self.cli('--cases', str(ROOT / 'benchmarks/trim/trigger-cases.yaml'))
        self.assertEqual(result.returncode, 2)
        self.assertIn('expected skill absent from catalog', result.stderr)

    def test_generic_ranker_supports_multilabel_and_abstention(self):
        catalog = {'first': 'alpha', 'second': 'beta'}
        route = self.module['router'](catalog)
        self.assertEqual(route('alpha beta'), ['first', 'second'])
        self.assertEqual(route('unknown words'), [])
        self.assertEqual(route('the and of'), [])
        self.assertEqual(route('ALPHA'), ['first'])

    def test_archived_cases_keep_original_frozen_metadata(self):
        cases = self.module['load_cases'](ROOT / 'benchmarks/trim/trigger-cases.yaml')
        frozen = json.loads((ROOT / 'benchmarks/trim/trigger-baseline.json').read_text())
        self.assertEqual(self.module['digest'](cases), frozen['cases_sha256'])
        self.assertEqual(len(cases), frozen['case_count'])
        self.assertEqual(frozen['exact_matches'], 40)
        self.assertTrue(40 <= len(cases) <= 60)
        self.assertEqual(len({case['id'] for case in cases}), len(cases))
        self.assertTrue(any(not case['expected'] for case in cases))
        self.assertTrue(any(len(case['expected']) > 1 for case in cases))

    def test_cli_json_reproduces_active_comparison_without_prompt_text(self):
        result = self.cli('--json', '--check')
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        cases_path, baseline_path = self.active_paths()
        frozen = json.loads(baseline_path.read_text())
        self.assertIn('keep-list', report['scope'])
        self.assertGreaterEqual(report['exact_match_accuracy'], frozen['exact_match_accuracy'])
        self.assertEqual(report['cases_sha256'], frozen['cases_sha256'])
        self.assertIn('proxy', report['method'])
        self.assertEqual(set(report['per_case'][0]), {'id', 'exact_match'})
        self.assertNotIn('\"prompt\":', result.stdout)
        for case in self.module['load_cases'](cases_path):
            self.assertNotIn(case['prompt'], result.stdout)
        self.assertEqual(report['gate_errors'], [])

    def test_gate_rejects_lower_accuracy(self):
        _, baseline_path = self.active_paths()
        baseline = json.loads(baseline_path.read_text())
        baseline['exact_match_accuracy'] = 1.0
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as file:
            json.dump(baseline, file)
            file.flush()
            result = self.cli('--json', '--check', '--baseline', file.name)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('accuracy below baseline', json.loads(result.stdout)['gate_errors'])

    def test_description_changes_can_improve_but_not_weaken_accuracy(self):
        cases = [{'id': 'first', 'prompt': 'alpha', 'expected': ['first']}]
        baseline = self.module['evaluate']({'first': 'alpha'}, cases)
        changed = self.module['evaluate']({'first': 'alpha alpha'}, cases)
        self.assertNotEqual(baseline['catalog_sha256'], changed['catalog_sha256'])
        self.assertEqual(self.module['gate_errors'](changed, baseline), [])
        weakened = self.module['evaluate']({'first': 'beta'}, cases)
        self.assertEqual(self.module['gate_errors'](weakened, baseline), ['accuracy below baseline'])

    def test_previous_pass_snapshot_catches_decline_above_initial_floor(self):
        initial = {'schema_version': 1, 'algorithm': self.module['ALGORITHM'],
                   'cases_sha256': 'same-cases', 'case_count': 50, 'exact_match_accuracy': 0.80}
        current = {**initial, 'exact_match_accuracy': 0.82}
        previous = {**initial, 'exact_match_accuracy': 0.84}
        self.assertEqual(self.module['gate_errors'](current, initial), [])
        self.assertEqual(self.module['gate_errors'](current, previous), ['accuracy below baseline'])

    def test_malformed_baseline_accuracy_fails_concisely(self):
        _, baseline_path = self.active_paths()
        baseline = json.loads(baseline_path.read_text())
        for accuracy in (10 ** 400, float('inf'), -1, True, 'bad'):
            with self.subTest(accuracy=accuracy), tempfile.NamedTemporaryFile(mode='w', suffix='.json') as file:
                json.dump({**baseline, 'exact_match_accuracy': accuracy}, file)
                file.flush()
                result = self.cli('--json', '--check', '--baseline', file.name)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn('trigger-eval:', result.stderr)
                self.assertNotIn('Traceback', result.stderr)

    def test_comparison_snapshot_is_documented_in_help_and_report(self):
        result = self.cli('--help')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('comparison snapshot', result.stdout)
        self.assertIn('pre-pass', result.stdout)
        result = self.cli('--plain')
        self.assertIn('Comparison snapshot accuracy:', result.stdout)

    def test_gate_rejects_changed_case_set(self):
        cases_path, _ = self.active_paths()
        data = json.loads(cases_path.read_text())
        data['cases'][0]['prompt'] += ' changed'
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml') as file:
            json.dump(data, file)
            file.flush()
            result = self.cli('--json', '--check', '--cases', file.name)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('case set differs from frozen baseline', json.loads(result.stdout)['gate_errors'])

    def test_invalid_cases_fail_concisely(self):
        for data in ({'cases': []}, {'cases': [{'id': 'x', 'prompt': '', 'expected': []}]}, {'cases': [{'id': 'x', 'prompt': 'hello', 'expected': ['missing-skill']}]}):
            with self.subTest(data=data), tempfile.NamedTemporaryFile(mode='w', suffix='.yaml') as file:
                json.dump(data, file)
                file.flush()
                result = self.cli('--cases', file.name)
                self.assertEqual(result.returncode, 2)
                self.assertIn('trigger-eval:', result.stderr)
                self.assertNotIn('Traceback', result.stderr)

    def test_plain_and_tty_agent_output(self):
        result = self.cli('--plain', '--check')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.isascii())
        self.assertIn('deterministic lexical proxy', result.stdout)
        self.assertIn('PASS', result.stdout)
        clean = {k: v for k, v in os.environ.items() if not k.startswith('CODEX_') and k not in ('CLAUDECODE', 'CLI_PLAIN')}
        for extra, decorated in (({}, True), ({'CODEX_TEST': '1'}, False), ({'CLI_PLAIN': '1'}, False)):
            with self.subTest(extra=extra):
                master, slave = pty.openpty()
                try:
                    result = subprocess.run([sys.executable, str(SCRIPT)], stdout=slave, stderr=subprocess.PIPE, env={**clean, **extra})
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual('🎯' in os.read(master, 16384).decode(), decorated)
                finally:
                    os.close(master)
                    os.close(slave)


if __name__ == '__main__':
    unittest.main()
