import json
import os
import pty
import runpy
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
START = '3e898a0f39172d7c30a6b0ae0258209cfe2c7f0c'


class TrimBenchmarkTest(unittest.TestCase):
    def setUp(self):
        self.module = runpy.run_path(str(ROOT / 'scripts/trim-benchmark'))

    def test_utf8_and_frontmatter_accounting(self):
        split = self.module['description_and_body']
        description, body = split('---\nname: x\ndescription: >-\n  Build logos\n  and icons.\n---\n# é\n')
        self.assertEqual(description, 'Build logos and icons.')
        self.assertEqual(body, '# é\n')
        self.assertEqual(self.module['metric'](body), {'lines': 1, 'bytes': 5, 'approx_tokens': 1.25})
        self.assertEqual(split('---\nname: x\ndescription: "Use logos"\n---\nbody')[0], 'Use logos')
        self.assertEqual(split('---\nname: x\ndescription: Use logos\n  and icons\n---\nbody')[0], 'Use logos and icons')
        with self.assertRaises(ValueError):
            split('body without frontmatter')

    def test_inventory_matches_bytes_and_keeps_bodies_separate(self):
        report = self.module['collect'](ROOT)
        for name, value in report['instructions'].items():
            self.assertEqual(value['bytes'], len((ROOT / name).read_bytes()))
        canonical = [s for p, s in report['skills'].items() if p.startswith('dot_agents/')]
        self.assertEqual(report['totals']['skills_count'], len(canonical))
        expected = sum(report['instructions'][p]['bytes'] for p in ('AGENTS.md', 'dot_codex/AGENTS.md'))
        expected += report['developer_instructions']['bytes']
        expected += sum(s['description']['bytes'] for s in canonical)
        self.assertEqual(report['totals']['loaded_bytes'], expected)
        self.assertGreater(report['totals']['body_bytes'], expected)

    def test_committed_inventory_reproduces_original_baseline(self):
        baseline = json.loads((ROOT / 'benchmarks/trim/BASELINE.json').read_text())
        report = self.module['collect'](ROOT, START)
        self.assertEqual(report, baseline)
        self.assertIn('dot_agents/skills/adapt/SKILL.md', report['skills'])
        self.assertNotIn('dot_agents/skills/lean-instructions/SKILL.md', report['skills'])

    def test_ref_cli_reports_blobs_without_current_budget_gate(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/trim-benchmark'),
                                 '--ref', START, '--json'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['totals'], json.loads((ROOT / 'benchmarks/trim/BASELINE.json').read_text())['totals'])
        self.assertEqual(report['comparison']['loaded_bytes']['percent_change'], 0)
        self.assertEqual(report['budget_errors'], [])
        rejected = subprocess.run([sys.executable, str(ROOT / 'scripts/trim-benchmark'),
                                   '--ref', START, '--check'], capture_output=True, text=True)
        self.assertEqual(rejected.returncode, 2)
        self.assertIn('--check requires the working tree', rejected.stderr)

    def test_invalid_ref_is_concise_and_not_an_option(self):
        for ref in ('missing-trim-ref', '--all'):
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/trim-benchmark'),
                                     '--ref=' + ref, '--json'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn('invalid commit ref', result.stderr)
            self.assertNotIn('Traceback', result.stderr)

    def test_cli_json_and_plain_comparisons(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/trim-benchmark'), '--json'], capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        self.assertIn('loaded_bytes', report['comparison'])
        self.assertIn('percent_change', report['comparison']['loaded_bytes'])
        self.assertIn('lines', report['instruction_comparison']['AGENTS.md'])
        self.assertEqual(report['instruction_comparison']['AGENTS.md']['bytes']['new'], len((ROOT / 'AGENTS.md').read_bytes()))
        self.assertIn('approx_tokens', report['developer_comparison'])
        self.assertIn('lines', report['item_comparison']['dot_agents/skills/metaprompt/SKILL.md']['body'])
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/trim-benchmark'), '--plain'], capture_output=True, text=True, check=True)
        self.assertIn('old', result.stdout)
        self.assertIn('new', result.stdout)
        self.assertIn('%', result.stdout)
        self.assertTrue(result.stdout.isascii())

    def test_invalid_snapshot_has_concise_error(self):
        missing_totals = json.loads((ROOT / 'benchmarks/trim/BASELINE.json').read_text())
        missing_totals['totals'] = {}
        huge_value = json.loads((ROOT / 'benchmarks/trim/BASELINE.json').read_text())
        huge_value['totals']['loaded_bytes'] = 10 ** 400
        for invalid in ({'totals': [], 'skills': {}}, [], {'totals': {'loaded_bytes': 'bad'}, 'skills': {}}, missing_totals, huge_value):
            with self.subTest(invalid=invalid):
                result = subprocess.run([sys.executable, str(ROOT / 'scripts/trim-benchmark'), '--baseline', '/dev/stdin'], input=json.dumps(invalid), capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn('Traceback', result.stderr)
                self.assertIn('snapshot schema', result.stderr)

    def test_tty_decoration_and_agent_overrides(self):
        clean_env = {k: v for k, v in os.environ.items() if not k.startswith('CODEX_') and k not in ('CLAUDECODE', 'CLI_PLAIN')}
        for extra, decorated in (({}, True), ({'CODEX_TEST': '1'}, False), ({'CLAUDECODE': '1'}, False), ({'CLI_PLAIN': '1'}, False)):
            with self.subTest(extra=extra):
                master, slave = pty.openpty()
                try:
                    result = subprocess.run([sys.executable, str(ROOT / 'scripts/trim-benchmark')], stdout=slave, stderr=subprocess.PIPE, env={**clean_env, **extra}, check=True)
                    output = os.read(master, 8192).decode()
                    self.assertEqual('📏' in output, decorated)
                finally:
                    os.close(master)
                    os.close(slave)

    def test_budget_rejects_new_oversize_and_growth(self):
        report = self.module['collect'](ROOT)
        budget = json.loads((ROOT / 'benchmarks/trim/BUDGETS.json').read_text())
        self.assertEqual(self.module['budget_errors'](report, budget), [])
        report['skills']['dot_agents/skills/new/SKILL.md'] = {
            'file': {'lines': 301, 'bytes': 100}, 'description': {'bytes': 20}, 'body': {'bytes': 80}}
        self.assertTrue(any('new/SKILL.md' in s for s in self.module['budget_errors'](report, budget)))
        del report['skills']['dot_agents/skills/new/SKILL.md']
        report['totals']['loaded_bytes'] = budget['loaded_bytes'] + 1
        self.assertTrue(any('loaded_bytes' in s for s in self.module['budget_errors'](report, budget)))

    def test_current_size_budgets(self):
        report = self.module['collect'](ROOT)
        budget = json.loads((ROOT / 'benchmarks/trim/BUDGETS.json').read_text())
        self.assertEqual(self.module['budget_errors'](report, budget), [])

    def test_lean_skill_is_discoverable_and_bounded(self):
        path = ROOT / 'dot_agents/skills/lean-instructions/SKILL.md'
        description, body = self.module['description_and_body'](path.read_text())
        self.assertLessEqual(len(description.encode()), 120)
        self.assertLessEqual(len(body.splitlines()), 300)
        canonical = (ROOT / 'dot_codex/AGENTS.md').read_text()
        self.assertEqual(sum('lean-instructions' in line for line in canonical.splitlines()), 1)


class ComparisonDocumentTest(unittest.TestCase):
    def setUp(self):
        self.module = runpy.run_path(str(ROOT / 'benchmarks/trim/update-comparison.py'))

    def test_only_actual_commits_become_pass_rows(self):
        document = self.module['render'](ROOT, START, START)
        self.assertIn('Always-loaded tokens per session: **9,404.75 → 9,404.75**', document)
        self.assertIn('No pass commits exist in the requested range.', document)
        self.assertIn('unavailable', document)
        self.assertNotIn('Uncommitted working draft', document)
        self.assertIn('dot_agents/skills/playwright-interactive/SKILL.md', document)

    def test_working_draft_is_separate_from_committed_results(self):
        document = self.module['render'](ROOT, START, START, include_working=True)
        self.assertIn('No pass commits exist in the requested range.', document)
        self.assertIn('## Uncommitted working draft', document)
        self.assertIn('Excluded from committed pass rows and savings ranking.', document)

    def test_evidence_counts_and_stale_commit_guard(self):
        fields = self.module['evidence_fields']
        valid = {'commit_subject': 'docs(trim): cull', 'pass': 'Cull', 'technique': 'Ranked cull',
                 'tests': {'passed': 7, 'command': 'python3 -m unittest'},
                 'trigger': {'exact_matches': 13, 'case_count': 17,
                             'method': 'lexical proxy', 'scope': 'keep-list'}}
        evidence = fields(valid, 'docs(trim): cull')
        self.assertEqual(evidence['tests'], '7')
        self.assertEqual(evidence['trigger'], '13/17 (76.47%)')
        self.assertEqual(fields(valid, 'docs(trim): later')['tests'], 'unavailable')
        self.assertEqual(fields({}, 'no evidence')['trigger'], 'unavailable')
        valid['tests']['passed'] = True
        valid['trigger']['exact_matches'] = 18
        self.assertEqual(fields(valid, 'docs(trim): cull')['tests'], 'unavailable')
        self.assertEqual(fields(valid, 'docs(trim): cull')['trigger'], 'unavailable')

    def test_commit_loop_uses_each_snapshot_and_matching_evidence(self):
        first, last = 'a' * 40, 'b' * 40
        subjects = {START: 'original', first: 'perf(trim): descriptions', last: 'docs(trim): follow-up'}
        original = json.loads((ROOT / 'benchmarks/trim/BASELINE.json').read_text())
        reduced = json.loads(json.dumps(original))
        reduced['totals']['description_bytes'] -= 400
        reduced['totals']['loaded_bytes'] -= 400
        reduced['totals']['loaded_approx_tokens'] -= 100
        reports = {START: original, first: reduced, last: reduced}
        evidence = {'commit_subject': subjects[first], 'pass': 'Descriptions', 'technique': 'Trigger-first wording',
                    'tests': {'passed': 7, 'command': 'python3 -m unittest'},
                    'trigger': {'exact_matches': 13, 'case_count': 17, 'method': 'lexical proxy', 'scope': 'keep-list'}}

        def git(root, *args):
            if args[0] == 'merge-base':
                return ''
            if args[0] == 'log':
                return f'{first}\t{subjects[first]}\n{last}\t{subjects[last]}\n'
            if args[:3] == ('show', '-s', '--format=%s'):
                return subjects[args[3]]
            if args[0] == 'ls-tree':
                return '' if args[2] == START else 'benchmarks/trim/pass-evidence.json'
            if args[0] == 'show':
                return json.dumps(evidence)
            self.fail(f'unexpected git request: {args}')

        render = self.module['render']
        with patch.dict(render.__globals__, {'BENCHMARK': {'git': git, 'commit_ref': lambda root, ref: ref,
                                                          'collect': lambda root, ref: reports[ref]}}):
            document = render(ROOT, START, last)
        self.assertIn('**9,404.75 → 9,304.75**', document)
        self.assertIn('| aaaaaaa | Descriptions | Trigger-first wording |', document)
        self.assertIn('| bbbbbbb | docs(trim): follow-up | unavailable |', document)
        self.assertIn('| Trigger-first wording | +100.00 |', document)
        self.assertIn('13/17 (76.47%)', document)


if __name__ == '__main__':
    unittest.main()
