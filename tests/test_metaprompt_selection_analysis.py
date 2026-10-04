import importlib.util
import unittest
import tempfile
import hashlib
import json
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / 'scripts/metaprompt-selection-analysis.py'

class AnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('selection_analysis', PATH)
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def fixture(self):
        schedule=[]; rows=[]; requests=[]
        for arm in ('raw','minimal','skill'):
            for workflow in ('create','sharpen','template','coding'):
                ident=arm+'--'+workflow
                base=dict(id=ident,candidate=arm,case_id=workflow,workflow=workflow,split='holdout')
                schedule.append(base)
                rows.append(dict(base,status='completed',success=arm=='skill',hard_failures=[],
                    native_deliverable_completed=True,native_workflow={'complete':False},
                    solver={'call_count':1,'latency_seconds':2,'requests':[{'usage':{'input_tokens':10,'output_tokens':3,'input_tokens_details':{'cached_tokens':2},'output_tokens_details':{'reasoning_tokens':1}}}]}))
                requests.append({'label':ident+':solver'})
        return schedule,rows,{'cap':2000,'requests':requests},{'trials':[{'id':r['id']} for r in rows]}

    def test_known_cost_and_paired_result(self):
        s,r,q,t=self.fixture();v=self.module.analyze(s,r,q,t,{'skill':{'latest_substantive_change':'2026-01-01','stars':2}})
        self.assertEqual(v['recommended_skill'],'skill')
        self.assertEqual(v['arms']['skill']['weighted_success'],1)
        self.assertEqual(v['arms']['skill']['native_observed_complete'],0)
        self.assertEqual(v['arms']['skill']['final_deliverables'],4)
        self.assertEqual(v['arms']['skill']['first_use']['input_tokens'],40)
        self.assertEqual(v['arms']['skill']['solver_only']['cached_input_tokens'],8)
        self.assertEqual(v['paired']['skill_vs_raw']['interval95'],[1,1])

    def test_missing_or_duplicate_never_recommends(self):
        s,r,q,t=self.fixture()
        for rows in (r[:-1],r+[r[0]]):
            v=self.module.analyze(s,rows,q,t,{'skill':{}})
            self.assertIsNone(v['recommended_skill'])
            self.assertFalse(v['complete_balanced_holdout'])

    def test_unknown_failed_usage_not_zero(self):
        s,r,q,t=self.fixture();r[-1]['solver']['requests'][0]['usage']=None
        r[-1].update(status='episode_limit',success=False)
        v=self.module.analyze(s,r,q,t,{'skill':{}})
        self.assertIsNone(v['arms']['skill']['first_use']['input_tokens'])
        self.assertEqual(v['arms']['skill']['first_use']['known_input_tokens'],30)
        self.assertEqual(v['arms']['skill']['first_use']['latency_seconds'],8)
        self.assertEqual(v['arms']['skill']['failures']['status:episode_limit'],1)

    def test_caps_and_metadata_mismatch(self):
        s,r,q,t=self.fixture();q['requests'] += [{'label':'skill--coding:solver'}]*10
        r[0]['workflow']='coding'
        v=self.module.analyze(s,r,q,t,{'skill':{}})
        self.assertIsNone(v['recommended_skill'])
        self.assertTrue(any('cap' in x for x in v['integrity_errors']))
        self.assertTrue(any('metadata' in x for x in v['integrity_errors']))

    def test_frozen_bytes_checked_and_ranking_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'input').write_text('original')
            protocol={'schema_version':1,'files':{'input':hashlib.sha256(b'original').hexdigest()},
                      'settings':{'ranking':self.module.RANKING}}
            (root/'protocol.json').write_text(json.dumps(protocol))
            self.assertEqual(self.module.verify_protocol(root),protocol)
            (root/'input').write_text('changed')
            with self.assertRaisesRegex(ValueError,'Frozen input changed'):
                self.module.verify_protocol(root)

    def test_native_failed_output_keeps_attempt_and_safe_failure_labels(self):
        s,r,q,t=self.fixture();r[-1].update(success=False,
            score={'success':False,'checks':['Traceback\nprivate submitted content']},
            coding_actions={'checks':{'public_red_before_fix':False}})
        v=self.module.analyze(s,r,q,t,{'skill':{}})
        self.assertEqual(v['arms']['skill']['attempts'],4)
        self.assertEqual(v['arms']['skill']['final_deliverables'],4)
        self.assertEqual(v['arms']['skill']['native_observed_complete'],0)
        self.assertIn('score:assertion_or_execution_failure',v['arms']['skill']['failures'])
        self.assertNotIn('private submitted content',json.dumps(v))

    def test_omission_sensitivity_is_balanced_and_never_changes_primary_rows(self):
        _, rows, _, _ = self.fixture()
        for row in rows:
            row['success'] = True
        for arm in ('raw', 'minimal', 'skill'):
            row = dict(next(r for r in rows if r['candidate'] == arm and r['workflow'] == 'template'))
            row.update(id=arm+'--ambiguous', case_id='ambiguous', success=arm=='skill')
            rows.append(row)
        before = json.dumps(rows, sort_keys=True)
        value = self.module.omission_sensitivity(rows, ['ambiguous'])
        self.assertEqual(value['excluded_case_ids'], ['ambiguous'])
        self.assertEqual(value['arms']['raw']['weighted_success'], 1)
        self.assertEqual(value['arms']['raw']['attempts'], 4)
        self.assertEqual(value['arms']['skill']['weighted_success'], 1)
        self.assertEqual(value['paired']['skill_vs_raw']['difference'], 0)
        self.assertEqual(before, json.dumps(rows, sort_keys=True))

if __name__ == '__main__': unittest.main()
