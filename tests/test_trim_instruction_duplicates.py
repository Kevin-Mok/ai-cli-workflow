"""Remove only the repeated developer block while retaining canonical controls."""

import re
import runpy
import subprocess
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = 'dot_codex/config.toml'
BEFORE = '4296498e'
ORIGINAL = '3e898a0f39172d7c30a6b0ae0258209cfe2c7f0c'


def committed(ref):
    return subprocess.check_output(['git', 'show', f'{ref}:{CONFIG}'], cwd=ROOT).decode()


class InstructionDuplicateTest(unittest.TestCase):
    def test_only_duplicated_developer_block_is_removed(self):
        before_text = committed(BEFORE)
        current_text = (ROOT / CONFIG).read_text()
        block = re.compile(r'^developer_instructions = """\n.*?^"""\n', re.M | re.S)
        self.assertEqual(len(block.findall(before_text)), 1)
        self.assertEqual(current_text, block.sub('', before_text))
        before, current = tomllib.loads(before_text), tomllib.loads(current_text)
        self.assertNotIn('developer_instructions', current)
        before.pop('developer_instructions')
        self.assertEqual(current, before, 'every unrelated TOML setting must remain unchanged')

    def test_models_and_efforts_keep_original_values_and_lines(self):
        original = committed(ORIGINAL)
        current = (ROOT / CONFIG).read_text()
        for key in ('model', 'model_reasoning_effort', 'plan_mode_reasoning_effort'):
            with self.subTest(setting=key):
                self.assertEqual(tomllib.loads(current)[key], tomllib.loads(original)[key])
                self.assertEqual(re.search(rf'^{key} = .*$', current, re.M)[0],
                                 re.search(rf'^{key} = .*$', original, re.M)[0])

    def test_all_three_controls_remain_in_standing_canonical_policy(self):
        core = ' '.join((ROOT / 'dot_codex/AGENTS.md').read_text().split())
        for rule in (
            'Keep relevant documentation and ExecPlan updates in the same commit as their implementation.',
            'Use concise Conventional Commit subjects and minimal bodies with only concrete bullets.',
            'Before the first modifying command in a Git repo, capture `git status --short`.',
        ):
            self.assertIn(rule, core)

    def test_benchmark_no_longer_charges_the_repeated_block(self):
        collect = runpy.run_path(str(ROOT / 'scripts/trim-benchmark'))['collect']
        before, current = collect(ROOT, BEFORE), collect(ROOT)
        self.assertEqual(before['developer_instructions']['bytes'], 717)
        self.assertEqual(current['developer_instructions']['bytes'], 0)
        self.assertEqual(before['totals']['loaded_bytes'] - current['totals']['loaded_bytes'], 717)
        for key in ('skills_count', 'description_bytes'):
            self.assertEqual(current['totals'][key], before['totals'][key])


if __name__ == '__main__':
    unittest.main()
