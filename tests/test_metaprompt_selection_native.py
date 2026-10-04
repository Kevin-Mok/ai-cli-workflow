"""Native observation checks; entirely local fixtures, no model/runtime imports."""
import importlib.util
import json
from pathlib import Path
import unittest

PATH = Path(__file__).resolve().parents[1] / 'benchmarks/metaprompt-selection/selection_native.py'
spec = importlib.util.spec_from_file_location('selection_native', PATH)
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)


def event(tool, args, result):
    return {'tool': tool, 'arguments': args, 'status': 'ok', 'result': json.dumps(result)}


def senior_fixture():
    cases = [{'id': str(i), 'input': {'value': i}, 'expected': i} for i in range(10)]
    artifacts = {'prompts/current.txt': 'Original prompt', 'prompts/revised.txt': 'Final prompt',
        'prompts/cases.json': json.dumps(cases),
        'artifacts/baseline.json': json.dumps({'clarity_score': 70, 'token_count': 100}),
        'artifacts/revision.json': json.dumps({'clarity_score': 75, 'token_count': 110})}
    trace = [event('run_skill_check', {'prompt_path':'prompts/current.txt', 'output_path':'artifacts/baseline.json'}, {'exit_code':0, 'stdout':'{}'}),
        event('run_skill_check', {'prompt_path':'prompts/revised.txt', 'baseline_path':'artifacts/baseline.json', 'output_path':'artifacts/revision.json'}, {'exit_code':0, 'stdout':'{}'})]
    for prompt in ('prompts/current.txt', 'prompts/revised.txt'):
        trace.append(event('evaluate_prompt', {'prompt_path':prompt, 'cases_path':'prompts/cases.json'},
            {'status':'completed', 'total':10, 'success':False,
             'case_results':[{'id':str(i), 'success':i != 9} for i in range(10)]}))
    return {'output':'Final prompt', 'tool_trace':trace, 'artifacts':artifacts}


class NativeObservationTests(unittest.TestCase):
    def observe(self, compiled, **kwargs):
        return native.native_observations(compiled, {'id':'alireza-senior'}, 'sharpen', **kwargs)

    def test_no_regression_allows_previously_failing_public_case(self):
        result = self.observe(senior_fixture(), final_prompt='Final prompt')
        self.assertTrue(result['complete'], result)
        self.assertTrue(result['checks']['public_no_regression'])

    def test_new_failure_in_previously_passing_case_rejected(self):
        compiled = senior_fixture()
        value = json.loads(compiled['tool_trace'][-1]['result'])
        value['case_results'][0]['success'] = False
        compiled['tool_trace'][-1]['result'] = json.dumps(value)
        self.assertIn('public_eval_regression', self.observe(compiled)['failures'])

    def test_ids_same_but_inputs_or_expected_changed_cannot_pair(self):
        for field in ('input', 'expected'):
            with self.subTest(field=field):
                compiled = senior_fixture()
                cases = json.loads(compiled['artifacts']['prompts/cases.json'])
                cases[0][field] = 'changed'
                compiled['artifacts']['prompts/other.json'] = json.dumps(cases)
                compiled['tool_trace'][-1]['arguments']['cases_path'] = 'prompts/other.json'
                self.assertIn('same_case_public_eval_pair_not_observed', self.observe(compiled)['failures'])

    def test_public_eval_without_baseline_or_ten_cases_unverified(self):
        for change in ('baseline', 'count'):
            with self.subTest(change=change):
                compiled = senior_fixture()
                if change == 'baseline':
                    del compiled['tool_trace'][2]
                else:
                    cases = json.loads(compiled['artifacts']['prompts/cases.json'])[:9]
                    compiled['artifacts']['prompts/cases.json'] = json.dumps(cases)
                self.assertFalse(self.observe(compiled)['complete'])

    def test_actual_static_gate_and_final_bytes_required(self):
        for metrics, final, failure in [({'clarity_score':69, 'token_count':100}, 'Final prompt', 'static_clarity_regression'),
            ({'clarity_score':75, 'token_count':111}, 'Final prompt', 'static_token_regression'),
            ({'clarity_score':75, 'token_count':110}, 'Another prompt', 'final_prompt_static_analysis_not_observed')]:
            with self.subTest(metrics=metrics, final=final):
                compiled = senior_fixture()
                compiled['artifacts']['artifacts/revision.json'] = json.dumps(metrics)
                self.assertIn(failure, self.observe(compiled, final_prompt=final)['failures'])

    def test_static_helper_stdout_mixed_prose_json_supported(self):
        compiled = senior_fixture()
        del compiled['artifacts']['artifacts/revision.json']
        del compiled['tool_trace'][1]['arguments']['output_path']
        compiled['tool_trace'][1]['result'] = json.dumps({'exit_code':0,
            'stdout':'COMPARISON WITH BASELINE\nTokens 100 -> 110\n'+json.dumps({'clarity_score':75, 'token_count':110})+'\nAnalysis saved'})
        self.assertTrue(self.observe(compiled, final_prompt='Final prompt')['complete'])

    def test_invalid_unknown_or_boolean_metrics_never_raise_or_pass(self):
        for metrics in ({'clarity_score':True, 'token_count':100}, {'clarity_score':float('nan'), 'token_count':100}, {}, 'bad json'):
            with self.subTest(metrics=metrics):
                compiled = senior_fixture()
                compiled['artifacts']['artifacts/revision.json'] = json.dumps(metrics)
                self.assertFalse(self.observe(compiled)['complete'])
        for compiled in ({}, {'tool_trace':[None, {'result':'bad'}], 'artifacts':None, 'output':None}):
            self.assertFalse(self.observe(compiled)['complete'])

    def test_malformed_nested_paths_and_oversized_numbers_are_unknown(self):
        for tool_index, key in ((1, 'baseline_path'), (1, 'prompt_path'), (3, 'cases_path')):
            with self.subTest(tool_index=tool_index, key=key):
                compiled = senior_fixture()
                compiled['tool_trace'][tool_index]['arguments'][key] = {'not':'a path'}
                self.assertFalse(self.observe(compiled, final_prompt='Final prompt')['complete'])
        compiled = senior_fixture()
        compiled['artifacts']['artifacts/revision.json'] = json.dumps({'clarity_score':75, 'token_count':10**1000})
        self.assertFalse(self.observe(compiled)['complete'])

    def test_final_eval_must_evaluate_actual_revision(self):
        compiled = senior_fixture()
        compiled['tool_trace'][-1]['arguments']['prompt_path'] = 'prompts/current.txt'
        self.assertFalse(self.observe(compiled, final_prompt='Final prompt')['complete'])

    def test_baseline_metric_artifact_needs_earlier_successful_helper(self):
        compiled = senior_fixture()
        compiled['tool_trace'][0]['result'] = json.dumps({'exit_code':1, 'stdout':''})
        self.assertFalse(self.observe(compiled)['complete'])

    def test_sentry_sections_and_batch_reference_reads(self):
        names = ('Target','Success Criteria','External Context','Optimized Prompt','Adapter Notes','Eval Set','Optimization Log','Residual Risks')
        compiled = {'output':'\n'.join('## '+name+'\nConcrete content.' for name in names),
            'tool_trace':[event('read_files', {'paths':['references/core-patterns.md', 'references/model-family-notes.md', 'references/transformed-examples.md']}, {})]}
        result = native.native_observations(compiled, {'id':'sentry-prompt-optimizer'}, 'coding')
        self.assertTrue(result['complete'], result)
        sharpen = native.native_observations(compiled, {'id':'sentry-prompt-optimizer'}, 'sharpen')
        self.assertIn('unread_required_reference:references/meta-optimization-loop.md', sharpen['failures'])
        compiled['output'] = '\n'.join(str(i+1)+'. **'+name+':** Concrete content.' for i,name in enumerate(names))
        self.assertTrue(native.native_observations(compiled, {'id':'sentry-prompt-optimizer'}, 'create')['complete'])

    def test_section_mentions_inside_prompt_or_empty_sections_not_complete(self):
        compiled = {'output':'```text\nTarget Success Criteria External Context Optimized Prompt Adapter Notes Eval Set Optimization Log Residual Risks\n```', 'tool_trace':[]}
        result = native.native_observations(compiled, {'id':'sentry-prompt-optimizer'}, 'create')
        self.assertIn('missing_section:Target', result['failures'])
        compiled['output'] = '## Target\n\n## Optimized Prompt\nPrompt.'
        self.assertIn('empty_section:Target', native.native_observations(compiled, {'id':'sentry-prompt-optimizer'}, 'create')['failures'])

    def test_wshobson_adds_no_invented_ceremony(self):
        self.assertTrue(native.native_observations({}, {'id':'wshobson-patterns'}, 'create')['complete'])


if __name__ == '__main__':
    unittest.main()
