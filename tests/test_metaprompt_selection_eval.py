"""Public eval behavior; injected runtimes never reach a model endpoint."""
import importlib
import json
import multiprocessing
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'benchmarks/metaprompt-selection'


def reserve_worker(path, label, queue):
    sys.path.insert(0, str(PACKAGE))
    from selection_eval import StageBudget
    queue.put(StageBudget(Path(path), label).permit())


class PublicEvalTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((PACKAGE/'selection_eval.py').is_file(), 'public eval module not implemented')
        sys.path.insert(0, str(PACKAGE))
        self.mod = importlib.import_module('selection_eval')
        from selection_core import FixtureFiles
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.scratch = self.root/'scratch'
        self.scratch.mkdir()
        self.fs = FixtureFiles(self.scratch, 'prompts')
        (self.scratch/'prompt.txt').write_text('Return the supplied value.')
        self.cases = [{'id':'one','input':{'value':1},'expected':1},
                      {'id':'two','input':{'value':False},'expected':False}]
        (self.scratch/'public.json').write_text(json.dumps(self.cases))
        self.args = dict(prompt_path='prompt.txt',cases_path='public.json',output_path='artifacts/eval.json')
        self.budget = self.root/'budget.json'
        self.label = 'trial-id:compiler'

    def fake(self, output, status='ok'):
        def invoke(prompt, scratch, permit, **kwargs):
            self.assertEqual(kwargs['mcp_command'], None)
            self.assertEqual(kwargs['model'], 'gpt-6.1-sol')
            self.assertEqual(kwargs['effort'], 'medium')
            self.assertEqual(list(scratch.iterdir()), [])
            self.sent = prompt
            if not permit():
                return dict(status='budget_exhausted',call_count=0,requests=[],output='',error='Budget exhausted',usage=None,latency_seconds=0)
            return dict(status=status,call_count=1,requests=[{'payload':{'model':'gpt-6.1-sol'},'usage':{'input_tokens':3,'output_tokens':2},'served_model':'gpt-6.1-sol','headers':{'Authorization':'test-secret'}}],output=output,error=None if status=='ok' else 'transport failed',usage={'input_tokens':3,'output_tokens':2},latency_seconds=0.2)
        return invoke

    def evaluate(self, output, status='ok'):
        return self.mod.evaluate_prompt(self.fs,self.args,self.budget,self.label,invoke=self.fake(output,status))

    def test_batch_real_outputs_typed_compare_without_sending_expected_values(self):
        self.cases[0]['expected'] = {'public_expected_marker': 1}
        (self.scratch/'public.json').write_text(json.dumps(self.cases))
        result = self.evaluate('[{"id":"one","output":{"public_expected_marker":1}},{"id":"two","output":false}]')
        self.assertTrue(result['success'])
        self.assertEqual(result['passed'],2)
        self.assertNotIn('public_expected_marker',self.sent)
        self.assertEqual(result['runtime']['call_count'],1)
        self.assertEqual(json.loads(self.budget.read_text())['requests'][0]['label'],self.label)
        saved=(self.scratch/self.args['output_path']).read_text()
        self.assertNotIn('Authorization',saved)
        self.assertNotIn('test-secret',saved)
        self.assertEqual(json.loads(saved),result)

    def test_boolean_is_not_a_number_and_wrong_answer_is_not_infrastructure(self):
        result=self.evaluate('[{"id":"one","output":true},{"id":"two","output":0}]')
        self.assertEqual(result['status'],'completed')
        self.assertFalse(result['success'])
        self.assertEqual(result['passed'],0)

    def test_bad_result_ids_or_shape_fail_instead_of_dropping_cases(self):
        for output in ['[]','[{"id":"one","output":1},{"id":"one","output":1}]','```json\n[]\n```','[{"id":"one","output":1,"extra":1}]']:
            with self.subTest(output=output):
                self.args['output_path']='artifacts/eval-'+str(len(list((self.scratch/'artifacts').glob('*'))))+'.json'
                result=self.evaluate(output)
                self.assertEqual(result['status'],'invalid_output')
                self.assertFalse(result['success'])
                self.assertEqual(result['total'],2)

    def test_invalid_paths_cases_or_collision_cost_zero(self):
        calls=[]
        def never(*a,**k):calls.append(1);raise AssertionError('No runtime on invalid input')
        for updates in [dict(prompt_path='/etc/passwd'),dict(cases_path='../key.json'),dict(output_path='prompts/eval.json'),dict(extra='ignored')]:
            with self.subTest(updates=updates):
                with self.assertRaises(ValueError):self.mod.evaluate_prompt(self.fs,{**self.args,**updates},self.budget,self.label,invoke=never)
        (self.scratch/'artifacts').mkdir()
        (self.scratch/'artifacts/eval.json').write_text('original')
        with self.assertRaises(ValueError):self.mod.evaluate_prompt(self.fs,self.args,self.budget,self.label,invoke=never)
        self.assertEqual((self.scratch/'artifacts/eval.json').read_text(),'original')
        self.args['output_path']='artifacts/new.json'
        for cases in [[],self.cases*11,[{'id':'x','input':1}],self.cases+self.cases]:
            (self.scratch/'public.json').write_text(json.dumps(cases))
            with self.assertRaises(ValueError):self.mod.evaluate_prompt(self.fs,self.args,self.budget,self.label,invoke=never)
        self.assertEqual(calls,[])
        self.assertFalse(self.budget.exists())

    def test_global_and_compiler_quota_share_existing_ledger(self):
        from selection_core import Budget
        budget=Budget(self.budget,2000)
        for _ in range(9):self.assertTrue(budget.permit(self.label))
        self.assertTrue(self.evaluate('[{"id":"one","output":1},{"id":"two","output":false}]')['success'])
        self.args['output_path']='artifacts/second.json'
        result=self.evaluate('[]')
        self.assertEqual(result['status'],'episode_limit')
        self.assertEqual(result['runtime']['call_count'],0)
        self.assertEqual(Budget(self.budget,2000).used,10)
        other=self.root/'global.json'
        limited=self.mod.StageBudget(other,'other:compiler',cap=1)
        self.assertTrue(limited.permit())
        self.assertFalse(self.mod.StageBudget(other,'next:compiler',cap=1).permit())

    def test_atomic_stage_cap_survives_parallel_processes(self):
        context=multiprocessing.get_context('fork')
        queue=context.Queue()
        processes=[context.Process(target=reserve_worker,args=(str(self.budget),self.label,queue)) for _ in range(16)]
        for p in processes:p.start()
        for p in processes:p.join(10);self.assertEqual(p.exitcode,0)
        results=[queue.get(timeout=2) for _ in processes]
        self.assertEqual(sum(results),10)
        self.assertEqual(json.loads(self.budget.read_text())['reserved'],10)

    def test_runtime_error_keeps_attempt_and_safe_trace(self):
        result=self.evaluate('',status='infrastructure_error')
        self.assertEqual(result['status'],'infrastructure_error')
        self.assertFalse(result['success'])
        self.assertEqual(result['runtime']['call_count'],1)
        self.assertEqual(json.loads(self.budget.read_text())['reserved'],1)


if __name__=='__main__':
    unittest.main()
