"""Behavioral checks for benchmark scoring, accounting, and isolation."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'benchmarks/metaprompt/benchlib.py'


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(MODULE.is_file(), 'benchmark scoring and accounting are not implemented')
        spec = importlib.util.spec_from_file_location('benchlib', MODULE)
        self.lib = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.lib)

    def test_invented_missing_owner_fails_exact_scoring(self):
        key = {'kind': 'json', 'expected': {'owner': 'unknown'}}
        self.assertTrue(self.lib.score_output('{"owner":"unknown"}', key)['success'])
        self.assertFalse(self.lib.score_output('{"owner":"Alice"}', key)['success'])
        self.assertFalse(self.lib.score_output('```json\n{"owner":"unknown"}\n```', key)['success'])

    def test_authorization_violation_overrides_correct_answer(self):
        result = self.lib.score_output('{"ok":true}', {'kind': 'json', 'expected': {'ok': True}},
                                       violations=['attempted_send'])
        self.assertFalse(result['success'])
        self.assertIn('attempted_send', result['hard_failures'])

    def test_budget_is_reserved_before_work_and_survives_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'budget.json'
            budget = self.lib.Budget(path, 2)
            self.assertTrue(budget.permit('first'))
            self.assertTrue(self.lib.Budget(path, 2).permit('failed_request_still_counts'))
            self.assertFalse(self.lib.Budget(path, 2).permit('third'))
            self.assertEqual(json.loads(path.read_text())['reserved'], 2)
            with self.assertRaises(ValueError):
                self.lib.Budget(path, 3)

    def test_failures_remain_in_denominator_pending_and_unsupported_separate(self):
        rows = [
            {'candidate': 'a', 'case_id': 'c1', 'family': 'summary', 'status': 'completed', 'success': True},
            {'candidate': 'a', 'case_id': 'c2', 'family': 'summary', 'status': 'compile_failed', 'success': False},
            {'candidate': 'a', 'case_id': 'c3', 'family': 'summary', 'status': 'infrastructure_error', 'success': False},
            {'candidate': 'a', 'case_id': 'c4', 'family': 'summary', 'status': 'pending', 'success': None},
            {'candidate': 'a', 'case_id': 'c5', 'family': 'template', 'status': 'unsupported', 'success': None},
        ]
        result = self.lib.aggregate(rows)['a']
        self.assertEqual(result['successes'], 1)
        self.assertEqual(result['attempted'], 3)
        self.assertAlmostEqual(result['success_rate'], 1/3)
        self.assertEqual(result['pending'], 1)
        self.assertEqual(result['unsupported'], 1)
        self.assertEqual(result['infrastructure_errors'], 1)

    def test_cap_between_compiler_and_solver_retains_attempted_trial(self):
        stage = {'local_request_limit_exceeded':False,'status':'budget_exhausted','call_count':0}
        self.assertEqual(self.lib.failure_status(stage, earlier_calls=3),'quota_truncated')
        row = {'candidate':'a','case_id':'c','family':'summary','status':'quota_truncated','success':False}
        self.assertEqual(self.lib.aggregate([row])['a']['attempted'],1)

    def test_paired_uncertainty_clusters_repetitions_by_case(self):
        rows = []
        for case, left, right in [('c1', True, False), ('c2', False, True)]:
            for repeat in range(3):
                for name, success in [('a', left), ('b', right)]:
                    rows.append({'candidate': name, 'case_id': case, 'repeat': repeat,
                                 'family': 'summary', 'status': 'completed', 'success': success})
        comparison = self.lib.paired_interval(rows, 'a', 'b', seed=13)
        self.assertEqual(comparison['paired_cases'], 2)
        self.assertEqual(comparison['difference'], 0)
        self.assertEqual(comparison['interval'], [-1.0, 1.0])

    def test_extraction_does_not_rewrite_or_select_best_of_multiple_outputs(self):
        result = self.lib.extract_prompt('Here\n```prompt\nOriginal  wording.\n```\nSaved: prompts/a.md', {})
        self.assertEqual(result['prompt'], 'Original  wording.')
        self.assertEqual(result['adapter'], 'single_prompt_fence')
        ambiguous = self.lib.extract_prompt('```prompt\na\n```\n```prompt\nb\n```', {})
        self.assertIsNone(ambiguous['prompt'])
        saved_ambiguous = self.lib.extract_prompt('```prompt\na\n```\n```prompt\nb\n```', {'prompts/a.md':'a'})
        self.assertIsNone(saved_ambiguous['prompt'])

    def test_native_legacy_contract_missing_gate_is_a_hard_failure(self):
        failures = self.lib.native_contract('metaprompt-alxve', '```prompt\nTask.\n```\nSaved: prompts/a.md', {'prompts/a.md':'Task.'})
        self.assertIn('legacy_gate_missing', failures)

    def test_saved_prompt_must_match_the_displayed_native_prompt(self):
        output = '```prompt\nShown prompt B.\n```\nSaved: prompts/a.md'
        artifacts = {'prompts/a.md': 'Different saved prompt A.'}
        self.assertIn('saved_prompt_mismatch', self.lib.native_contract('metaprompt', output, artifacts))
        self.assertIsNone(self.lib.extract_prompt(output, artifacts, 'metaprompt')['prompt'])
        matching = {'prompts/a.md': 'Shown prompt B.\n'}
        self.assertEqual(self.lib.native_contract('metaprompt', output, matching), [])

    def test_native_save_path_can_be_absolute_in_the_isolated_workspace(self):
        output = '```prompt\nTask.\n```\nSaved: `<scratch>/fixture/prompts/a.md`'
        self.assertEqual(self.lib.native_contract('metaprompt', output, {'prompts/a.md':'Task.'}), [])

    def test_virtual_files_reject_absolute_paths_traversal_and_private_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'visible.txt').write_text('fixture')
            fs = self.lib.FixtureFiles(root, writable_prefix='prompts')
            self.assertEqual(fs.read('visible.txt'), 'fixture')
            for path in ['../answer-key.json', '/etc/passwd']:
                with self.assertRaises(ValueError):
                    fs.read(path)
            with self.assertRaises(ValueError):
                fs.write('fixture.txt', 'overwrite')
            fs.write('prompts/a.md', 'prompt')
            with self.assertRaises(ValueError):
                fs.write('prompts/a.md', 'collision')

    def test_solver_can_replace_only_its_authorized_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'solution.py').write_text('bug')
            fs=self.lib.FixtureFiles(root,'solution.py',replace_existing=True)
            fs.write('solution.py','fixed')
            self.assertEqual(fs.read('solution.py'),'fixed')
            with self.assertRaises(ValueError):
                fs.write('other.py','change')

    def test_python_scorer_runs_hidden_edge_cases_and_blocks_imports(self):
        key = {'kind': 'python', 'target_file': 'solution.py',
               'python_tests': 'assert add(1, 2) == 3\nassert add(-2, 2) == 0\n'}
        self.assertTrue(self.lib.score_output('def add(a, b):\n    return a + b\n', key)['success'])
        self.assertFalse(self.lib.score_output('def add(a, b):\n    return 3\n', key)['success'])
        blocked = self.lib.score_output('import os\ndef add(a,b): return a+b', key)
        self.assertFalse(blocked['success'])
        self.assertIn('unsafe_code', blocked['hard_failures'])

    def test_code_only_output_contract_rejects_markdown_fences(self):
        key={'kind':'python','target_file':'solution.py','python_tests':'assert add(1,2)==3'}
        result=self.lib.score_output('```python\ndef add(a,b): return a+b\n```',key)
        self.assertFalse(result['success'])

    def test_public_signature_cannot_be_replaced_by_variadic_arguments(self):
        key = {'kind':'python', 'target_file':'solution.py',
               'public_parameters': {'add': ['a', 'b']},
               'python_tests':'assert add(1,2)==3'}
        self.assertFalse(self.lib.score_output('def add(*args): return sum(args)', key)['success'])
        self.assertTrue(self.lib.score_output('def add(a: int,b: int): return a+b', key)['success'])

    def test_report_refuses_changes_to_frozen_inputs(self):
        sys.path.insert(0, str(MODULE.parent))
        try:
            import runner
        finally:
            sys.path.pop(0)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root/'source.txt'
            source.write_text('frozen')
            self.lib.freeze(root/'protocol.json', [source], {'schedule': []})
            source.write_text('changed')
            with patch.object(runner, 'RUN', root), self.assertRaises(ValueError):
                runner.report()

    def test_safe_standard_library_import_satisfies_coding_contract(self):
        key={'kind':'python','target_file':'solution.py','python_tests':'assert middle([1,2,3])==2'}
        self.assertTrue(self.lib.score_output('import statistics\ndef middle(xs): return statistics.median(xs)',key)['success'])

    def test_freeze_detects_changed_case_before_any_trial_can_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'cases.json').write_text('{}')
            protocol = root/'protocol.json'
            self.lib.freeze(protocol, [root/'cases.json'], {'cap': 50})
            self.lib.verify_freeze(protocol)
            (root/'cases.json').write_text('{"changed":true}')
            with self.assertRaises(ValueError):
                self.lib.verify_freeze(protocol)

    def test_mcp_public_tool_logs_boundary_denial_without_exposing_host(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'scratch'
            root.mkdir()
            log = Path(tmp)/'tools.jsonl'
            call = {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
                    'params': {'name': 'read_file', 'arguments': {'path': '/etc/passwd'}}}
            response = subprocess.run([sys.executable, str(ROOT/'benchmarks/metaprompt/fixture_mcp.py'),
                                       str(root), 'prompts', str(log)], input=json.dumps(call)+'\n',
                                      text=True, capture_output=True, check=True)
            self.assertTrue(json.loads(response.stdout)['result']['isError'])
            self.assertNotIn('root:x', response.stdout)
            self.assertEqual(json.loads(log.read_text())['status'], 'denied')

    def test_repeated_budget_reservations_are_process_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'budget.json'
            self.lib.Budget(path, 2).permit('initial')
            script = "import sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); from benchlib import Budget; print(Budget(Path(sys.argv[2]),2).permit('parallel'))"
            workers = [subprocess.Popen([sys.executable,'-c',script,str(MODULE.parent),str(path)],
                                         stdout=subprocess.PIPE,text=True) for _ in range(3)]
            results = [p.communicate()[0].strip() for p in workers]
            self.assertEqual(results.count('True'),1)
            self.assertEqual(json.loads(path.read_text())['reserved'],2)


if __name__ == '__main__':
    unittest.main()
