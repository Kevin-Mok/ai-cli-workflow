"""Usage accounting must retain aborted requests without double counting."""
import importlib.util
from pathlib import Path
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'scripts/metaprompt-benchmark-analysis.py'


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(MODULE.is_file(), 'request-level report is not implemented')
        spec = importlib.util.spec_from_file_location('benchmark_analysis', MODULE)
        self.analysis = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.analysis)

    def test_aborted_episode_keeps_request_usage_when_cli_total_is_missing(self):
        stage = {'usage': None, 'call_count': 2, 'latency_seconds': 4,
                 'requests': [{'usage': {'input_tokens':100, 'output_tokens':10,
                      'input_tokens_details':{'cached_tokens':40},
                      'output_tokens_details':{'reasoning_tokens':3}}}, {'usage':None}]}
        result = self.analysis.stage_metrics(stage)
        self.assertEqual(result['input_tokens'], 100)
        self.assertEqual(result['cached_input_tokens'], 40)
        self.assertEqual(result['output_tokens'], 10)
        self.assertEqual(result['requests_with_unknown_usage'], 1)

    def test_flattened_clarification_requests_are_not_counted_twice(self):
        request = {'usage': {'input_tokens':100, 'output_tokens':10}}
        stage = {'call_count':2, 'requests':[request,request], 'latency_seconds':4,
                 'prior_reply': {'call_count':1,'requests':[request]}}
        result = self.analysis.stage_metrics(stage)
        self.assertEqual(result['requests'], 2)
        self.assertEqual(result['input_tokens'], 200)


if __name__ == '__main__':
    unittest.main()
