"""Digest inference failure and schema contracts, using local fake processes."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from second_brain import session_digest_runtime as digest
import codex_search_runtime

SUMMARY={'title':'Work','goal':'Feature','intentions':[],'accomplishments':['reported done'],
    'remaining':[],'blockers':[],'verification':[],'checks':[{'key':'check','text':'api_key=<redacted>'}]}

class FakeRuntime:
    def __init__(self,*args): self.deadline=None
    def set_deadline(self,value): self.deadline=value
    def prepare(self): return 'configured-model'
    def command(self,d,schema,out):
        code='import pathlib,sys; sys.stdin.read(); pathlib.Path(sys.argv[1]).write_text(sys.argv[2])'
        return [sys.executable,'-c',code,str(out),json.dumps(SUMMARY)],dict(__import__('os').environ)

class DigestRuntimeTests(unittest.TestCase):
    def test_valid_result_redacted_before_return(self):
        with patch.object(codex_search_runtime,'IsolatedCodex',FakeRuntime): result=digest.infer('inert dialogue',[])
        self.assertNotIn('secretvalue',json.dumps(result))
    def test_isolation_failure_prevents_process(self):
        with patch.object(codex_search_runtime,'IsolatedCodex') as runtime:
            runtime.return_value.prepare.side_effect=codex_search_runtime.RuntimeUnavailable('private path')
            with patch.object(digest.subprocess,'Popen') as spawn:
                with self.assertRaises(digest.InferenceError) as error: digest.infer('inert',[])
                self.assertEqual(error.exception.category,'isolation'); spawn.assert_not_called()
    def test_auth_and_quota_only_safe_classification(self):
        class Failure(FakeRuntime):
            def command(self,d,schema,out):
                return [sys.executable,'-c',"import sys; sys.stdin.read(); sys.stderr.write(sys.argv[1]); sys.exit(1)",Failure.message],dict(__import__('os').environ)
        for message,category in [('authentication failed: secret','authentication'),('quota limit: secret','quota'),('unplanned provider fault: secret','runtime')]:
            Failure.message=message
            with patch.object(codex_search_runtime,'IsolatedCodex',Failure):
                with self.assertRaises(digest.InferenceError) as error: digest.infer('inert',[])
            self.assertEqual(str(error.exception),category)
    def test_schema_rejects_extra_fields_and_duplicate_check_keys(self):
        with self.assertRaises(ValueError): digest.validate_summary({**SUMMARY,'tool':'exec'})
        with self.assertRaises(ValueError): digest.validate_summary({**SUMMARY,'checks':SUMMARY['checks']*2})
    def test_provider_schema_excludes_invalid_check_keys_before_generation(self):
        import re
        observed=[]
        class SchemaRuntime(FakeRuntime):
            def command(self,d,schema,out):
                observed.append(json.loads(schema.read_text()))
                return super().command(d,schema,out)
        with patch.object(codex_search_runtime,'IsolatedCodex',SchemaRuntime):
            digest.infer('inert fixture',[])
        key_schema=observed[0]['properties']['checks']['items']['properties']['key']
        def accepted(key):
            pattern=key_schema.get('pattern')
            return pattern is None or re.search(pattern,key) is not None
        for invalid in ('UI Check','verify_output','','a'*81):
            self.assertFalse(accepted(invalid),f'provider can generate invalid key: {invalid!r}')
        self.assertTrue(accepted('verify-playlist'))
        self.assertTrue(accepted('a'*80))

    def test_timeout_kills_and_reaps_process(self):
        class Timeout(FakeRuntime):
            def command(self,d,schema,out):
                return [sys.executable,'-c','import sys,time; sys.stdin.read(); time.sleep(60)'],dict(__import__('os').environ)
        with patch.object(codex_search_runtime,'IsolatedCodex',Timeout), patch.object(digest.time,'monotonic',side_effect=[0,119.9]):
            with self.assertRaises(digest.InferenceError) as error: digest.infer('inert',[])
        self.assertEqual(error.exception.category,'timeout')

if __name__=='__main__': unittest.main()
