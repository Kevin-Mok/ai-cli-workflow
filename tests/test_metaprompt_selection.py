"""Executable contracts for the replacement selection benchmark."""
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'benchmarks/metaprompt-selection'
sys.path.insert(0, str(ROOT))


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((ROOT / 'selection.py').exists(), 'New selection harness is not implemented')
        self.selection = importlib.import_module('selection')
        self.core = importlib.import_module('selection_core')

    def test_allocation_balances_workflows_without_spending_over_100_trials(self):
        self.assertEqual(self.selection.allocation(7), {'development_per_arm': 2, 'holdout_per_arm': 12, 'total': 98})
        self.assertEqual(self.selection.allocation(5), {'development_per_arm': 2, 'holdout_per_arm': 16, 'total': 90})
        self.assertEqual(self.selection.allocation(4), {'development_per_arm': 2, 'holdout_per_arm': 20, 'total': 88})
        with self.assertRaises(ValueError):
            self.selection.allocation(8)

    def test_request_reservations_survive_reopen_and_cannot_raise_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'requests.json'
            budget = self.core.Budget(path, 2000)
            self.assertTrue(budget.permit('first'))
            self.assertEqual(self.core.Budget(path, 2000).used, 1)
            with self.assertRaises(ValueError):
                self.core.Budget(path, 2001)
            with self.assertRaises(ValueError):
                self.core.Budget(path, 1999)
            small = self.core.Budget(Path(tmp) / 'small.json', 2)
            self.assertTrue(small.permit('failed transport'))
            self.assertTrue(small.permit('success'))
            self.assertFalse(small.permit('over cap'))
            self.assertEqual(small.used, 2)

    def test_trial_reservation_never_replays_an_interrupted_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = self.selection.TrialLedger(Path(tmp) / 'trials.json')
            self.assertTrue(ledger.reserve('one'))
            self.assertFalse(ledger.reserve('one'))
            for index in range(99):
                self.assertTrue(ledger.reserve(str(index)))
            self.assertFalse(ledger.reserve('101st'))
            self.assertEqual(ledger.used, 100)

    def test_stage_ceiling_includes_continuations_without_refunds(self):
        with tempfile.TemporaryDirectory() as tmp:
            budget = self.core.Budget(Path(tmp) / 'requests.json', 2000)
            gate = self.selection.StageGate(budget, 'trial:compiler')
            for _ in range(10):
                self.assertTrue(gate.permit())
            self.assertFalse(gate.permit())
            self.assertTrue(gate.exceeded)
            self.assertEqual(budget.used, 10)

    def test_public_checks_run_real_code_and_cannot_select_hidden_tests(self):
        mcp = importlib.import_module('selection_mcp')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'fixture'
            root.mkdir()
            (root / 'target.py').write_text('def double(value):\n    return value\n')
            (root / 'public_tests.py').write_text('from target import double\nassert double(3) == 6\n')
            fs = self.core.FixtureFiles(root, 'target.py', replace_existing=True)
            log = Path(tmp) / 'tools.jsonl'
            def call(name, args):
                return mcp.respond({'id': 1, 'method': 'tools/call', 'params': {'name': name, 'arguments': args}}, fs, log)['result']
            self.assertFalse(json.loads(call('run_tests', {})['content'][0]['text'])['success'])
            call('write_file', {'path': 'target.py', 'content': 'def double(value):\n    return value * 2\n'})
            self.assertTrue(json.loads(call('run_tests', {})['content'][0]['text'])['success'])
            self.assertTrue(call('run_tests', {'path': '../answer-key.json'})['isError'])
            self.assertTrue(call('write_file', {'path': 'public_tests.py', 'content': ''})['isError'])

    def test_batch_files_reduce_roundtrips_without_widening_access(self):
        mcp = importlib.import_module('selection_mcp')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'fixture'
            root.mkdir()
            fs = self.core.FixtureFiles(root, 'prompts')
            log = Path(tmp) / 'tools.jsonl'
            def call(name, args):
                return mcp.respond({'id': 1, 'method': 'tools/call', 'params': {'name': name, 'arguments': args}}, fs, log)['result']
            result = call('write_files', {'files': [{'path': 'prompts/a.txt', 'content': 'a'}, {'path': 'prompts/b.txt', 'content': 'b'}]})
            self.assertFalse(result.get('isError', False))
            read = call('read_files', {'paths': ['prompts/a.txt', 'prompts/b.txt']})
            self.assertEqual(json.loads(read['content'][0]['text']), {'prompts/a.txt': 'a', 'prompts/b.txt': 'b'})
            denied = call('write_files', {'files': [{'path': 'prompts/new.txt', 'content': 'new'}, {'path': '../outside.txt', 'content': 'bad'}]})
            self.assertTrue(denied['isError'])
            self.assertFalse((root / 'prompts/new.txt').exists())
            collision = call('write_file', {'path': 'prompts/a.txt', 'content': 'replacement'})
            self.assertTrue(collision['isError'])
            self.assertEqual(json.loads(log.read_text().splitlines()[-1])['status'], 'error')
            self.assertEqual(json.loads(log.read_text().splitlines()[-2])['status'], 'denied')

    def test_template_binding_rejects_lost_slots_and_does_not_rebind_input(self):
        self.assertEqual(self.core.bind_template('Use {{packet}}', {'packet': '{{other}}'}), 'Use {{other}}')
        with self.assertRaises(ValueError):
            self.core.bind_template('Use fixed example', {'packet': 'data'})

    def test_recommendation_uses_equal_workflows_and_excludes_unsafe_skill(self):
        sources = {'safe': {'latest_substantive_change': '2026-09-01', 'stars': 1001},
                   'unsafe': {'latest_substantive_change': '2026-10-01', 'stars': 99999}}
        rows = []
        for name in ['safe', 'unsafe', 'raw', 'minimal']:
            for workflow in self.selection.WORKFLOWS:
                rows.append({'candidate': name, 'workflow': workflow, 'status': 'completed',
                             'split': 'holdout', 'success': True, 'first_use_input_tokens': 100,
                             'hard_failures': ['unauthorized_tool_access'] if name == 'unsafe' else []})
        result = self.selection.summarize(rows, sources)
        self.assertEqual(result['recommended_skill'], 'safe')
        self.assertEqual(result['arms']['safe']['weighted_success'], 1)
        self.assertFalse(result['skill_improves_on_controls'])
        self.assertFalse(result['arms']['unsafe']['eligible_for_default'])

    def test_infrastructure_coverage_cannot_establish_a_recommendation(self):
        rows = [{'candidate': 'skill', 'workflow': w, 'status': 'quota_truncated',
                 'split': 'holdout', 'success': False, 'hard_failures': []} for w in self.selection.WORKFLOWS]
        result = self.selection.summarize(rows, {'skill': {'stars': 1001, 'latest_substantive_change': '2026-09-01'}})
        self.assertIsNone(result['recommended_skill'])

    def test_coding_must_stop_after_successful_verification(self):
        trace = [{'tool': 'read_file', 'arguments': {'path': 'target.py'}, 'status': 'ok'},
                 {'tool': 'read_file', 'arguments': {'path': 'public_tests.py'}, 'status': 'ok'},
                 {'tool': 'run_tests', 'arguments': {}, 'status': 'ok', 'result': '{"success":false}'},
                 {'tool': 'write_file', 'arguments': {'path': 'target.py'}, 'status': 'ok'},
                 {'tool': 'run_tests', 'arguments': {}, 'status': 'ok', 'result': '{"success":true}'},
                 {'tool': 'write_file', 'arguments': {'path': 'target.py'}, 'status': 'ok'},
                 {'tool': 'run_tests', 'arguments': {}, 'status': 'ok', 'result': '{"success":true}'}]
        self.assertFalse(self.selection.coding_actions(trace, 'target.py')['success'])

    def test_native_completion_distinguishes_prompt_from_required_report(self):
        self.assertTrue(hasattr(self.selection, 'native_observations'), 'Native completion audit missing')
        stage = {'output': '## Optimized Prompt\nReturn JSON.', 'tool_trace': [], 'artifacts': {}}
        observed = self.selection.native_observations(stage, {'id': 'sentry-prompt-optimizer'}, 'create')
        self.assertFalse(observed['complete'])
        self.assertIn('missing_section:Target', observed['failures'])
        self.assertTrue(self.selection.native_observations(stage, {'id': 'wshobson-patterns'}, 'create')['complete'])

    def test_compilation_extracts_final_section_without_rewriting(self):
        self.assertTrue(hasattr(self.selection, 'extract_compilation'), 'Native deliverable extraction missing')
        result = self.selection.extract_compilation('Notes\n## Revised Prompt\n```text\nKeep {{packet}} exactly.\n```\n## Changes\nKept inputs.', {}, {})
        self.assertEqual(result['prompt'], 'Keep {{packet}} exactly.')

    def test_draft_artifact_does_not_end_native_refinement(self):
        result = self.selection.extract_compilation('Here is a draft; shall I refine it?', {'prompts/draft.md': 'Draft text'}, {})
        self.assertIsNone(result['prompt'])

    def test_native_final_markdown_link_selects_its_exact_saved_artifact(self):
        output = 'Optimization Complete!\n\n**FINAL PROMPT:** [prompts/final_prompt.txt](<scratch>/fixture/prompts/final_prompt.txt)\n\nPublic cases passed.'
        result = self.selection.extract_compilation(output, {'prompts/current_prompt.txt': 'baseline', 'prompts/final_prompt.txt': 'final exact bytes\n'}, {})
        self.assertEqual(result['prompt'], 'final exact bytes\n')
        output = '**Best Prompt — FINAL:** [prompts/final_prompt.txt](<scratch>/fixture/prompts/final_prompt.txt)'
        result = self.selection.extract_compilation(output, {'prompts/final_prompt.txt': 'final exact bytes\n'}, {})
        self.assertEqual(result['prompt'], 'final exact bytes\n')

    def test_safe_iterator_exhaustion_preserves_standard_python_behavior(self):
        code = 'def first(values):\n    try:\n        return next(iter(values))\n    except StopIteration:\n        raise ValueError("empty") from None\n'
        key = {'kind': 'python', 'target_file': 'target.py', 'python_tests': 'assert first([4]) == 4\ntry:\n    first([])\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError("empty must raise")'}
        self.assertTrue(self.core.score_output(code, key)['success'])

    def test_development_recovery_uses_first_complete_reply_and_never_replays_solver(self):
        self.assertTrue(hasattr(self.selection, 'recovery_author_output'), 'Development extraction recovery missing')
        record = {'split': 'development', 'solver': None, 'compiler': {'status': 'episode_limit', 'output': 'unfinished',
                  'artifacts': {}, 'prior_replies': [{'status': 'ok', 'output': '```prompt\nfirst final\n```'},
                                                   {'status': 'ok', 'output': '```prompt\nlater final\n```'}]}}
        self.assertIn('first final', self.selection.recovery_author_output(record, {}))
        with self.assertRaises(ValueError):
            self.selection.recovery_author_output(dict(record, split='holdout'), {})
        with self.assertRaises(ValueError):
            self.selection.recovery_author_output(dict(record, solver={'status': 'infrastructure_error'}), {})

    def test_pure_typing_and_string_helpers_remain_valid_python(self):
        key = {'kind': 'python', 'target_file': 'target.py', 'python_tests': 'assert clean(" x\\ny ") == ["x", "y"]'}
        code = 'from typing import List\ndef clean(text: str) -> List[str]:\n    return [line.strip() for line in text.splitlines()]\n'
        self.assertTrue(self.core.score_output(code, key)['success'])

    def test_trial_keeps_private_keys_out_of_both_model_stages(self):
        self.assertTrue(hasattr(self.selection, 'execute_trial'), 'Compile-and-solve execution missing')
        seen = []
        def invoke(prompt, scratch, permit, **kwargs):
            self.assertTrue(permit())
            seen.append(prompt)
            text = '```prompt\nReturn JSON with value from supplied input.\n```' if len(seen) == 1 else '{"value":"secret-expected-answer"}'
            return {'status': 'ok', 'output': text, 'requests': [], 'latency_seconds': 0, 'call_count': 1}
        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / 'candidate'
            package.mkdir()
            (package / 'SKILL.md').write_text('Author useful prompts.')
            source = {'id': 'sample', 'entrypoint': str(package / 'SKILL.md'), 'files': {str(package / 'SKILL.md'): ''}}
            case = {'id': 'test', 'workflow': 'create', 'split': 'development', 'authoring_request': 'Create a JSON prompt.',
                    'task_prompt': 'Return JSON.', 'files': {}, 'solver_context': 'value is supplied here'}
            row = {'id': 'test--sample', 'candidate': 'sample', 'case_id': 'test', 'workflow': 'create', 'split': 'development'}
            result = self.selection.execute_trial(row, case, source, {'kind': 'json', 'expected': {'value': 'secret-expected-answer'}},
                                                   self.core.Budget(Path(tmp) / 'budget.json', 2000), invoke)
            self.assertTrue(result['success'])
            self.assertEqual(len(seen), 2)
            self.assertTrue(all('secret-expected-answer' not in prompt for prompt in seen))

    def test_coding_action_grading_requires_observed_red_fix_green(self):
        self.assertTrue(hasattr(self.selection, 'coding_actions'), 'Coding action grading missing')
        trace = [{'tool': 'read_file', 'arguments': {'path': 'target.py'}, 'status': 'ok'},
                 {'tool': 'read_file', 'arguments': {'path': 'public_tests.py'}, 'status': 'ok'},
                 {'tool': 'run_tests', 'arguments': {}, 'status': 'ok', 'result': '{"success":false}'},
                 {'tool': 'write_file', 'arguments': {'path': 'target.py'}, 'status': 'ok'},
                 {'tool': 'run_tests', 'arguments': {}, 'status': 'ok', 'result': '{"success":true}'}]
        self.assertTrue(self.selection.coding_actions(trace, 'target.py')['success'])
        self.assertFalse(self.selection.coding_actions(trace[0:2] + trace[3:], 'target.py')['success'])
        self.assertFalse(self.selection.coding_actions([], 'target.py')['success'])

    def test_schedule_is_paired_and_balanced_with_development_separate(self):
        self.assertTrue(hasattr(self.selection, 'build_schedule'), 'Balanced schedule missing')
        cases = [{'id': 'dev1', 'workflow': 'create', 'split': 'development'},
                 {'id': 'dev2', 'workflow': 'coding', 'split': 'development'}]
        for workflow in self.selection.WORKFLOWS:
            cases.extend({'id': workflow + str(i), 'workflow': workflow, 'split': 'holdout'} for i in range(6))
        rows = self.selection.build_schedule(cases, {'a': {}, 'b': {}, 'c': {}})
        self.assertEqual(len(rows), 90)
        for arm in ['a', 'b', 'c', 'raw', 'minimal']:
            own = [r for r in rows if r['candidate'] == arm]
            self.assertEqual(sum(r['split'] == 'development' for r in own), 2)
            for workflow in self.selection.WORKFLOWS:
                self.assertEqual(sum(r['split'] == 'holdout' and r['workflow'] == workflow for r in own), 4)
        case_sets = [{r['case_id'] for r in rows if r['candidate'] == name} for name in ['a', 'b', 'raw']]
        self.assertEqual(case_sets[0], case_sets[1])
        self.assertEqual(case_sets[1], case_sets[2])

    def test_development_gate_does_not_require_correct_candidate_answers(self):
        self.assertTrue(hasattr(self.selection, 'development_readiness'), 'Infrastructure readiness gate missing')
        rows = [{'id': 'control', 'workflow': 'coding', 'status': 'completed', 'success': True, 'coding_actions': {'success': True}},
                {'id': 'skill', 'workflow': 'coding', 'status': 'completed', 'success': False, 'coding_actions': {'success': False}}]
        self.assertTrue(self.selection.development_readiness(rows, ['control', 'skill'])['ready'])
        rows[1]['status'] = 'infrastructure_error'
        self.assertFalse(self.selection.development_readiness(rows, ['control', 'skill'])['ready'])


if __name__ == '__main__':
    unittest.main()
