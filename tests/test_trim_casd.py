"""Prove conditional policy relocation preserves every pre-pass block verbatim."""

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = '6e9934c7'


def blocks(text):
    lines = text.splitlines()
    result = []
    index = 0
    section = ''
    while index < len(lines):
        if not lines[index].strip():
            index += 1
            continue
        start = index
        if lines[index].startswith('#'):
            section = lines[index]
            index += 1
        else:
            index += 1
            while index < len(lines) and lines[index].strip() and not re.match(r'^(?:- |#{1,6} )', lines[index]):
                index += 1
        result.append({'start_line': start + 1, 'section': section,
                       'text': '\n'.join(lines[start:index])})
    return result


class TrimCasdTest(unittest.TestCase):
    def test_all_original_policy_blocks_have_one_verbatim_home(self):
        path = ROOT / 'benchmarks/trim/casd-map.json'
        self.assertTrue(path.is_file(), 'CASD preservation map is not implemented')
        mapping = json.loads(path.read_text())
        self.assertEqual(mapping['base_commit'], BASE)
        original = subprocess.run(['git', 'show', BASE + ':dot_codex/AGENTS.md'],
                                  cwd=ROOT, capture_output=True, text=True, check=True).stdout
        self.assertEqual(mapping['source_sha256'], hashlib.sha256(original.encode()).hexdigest())
        source = blocks(original)
        self.assertEqual(len(mapping['blocks']), len(source))
        homes = {'dot_codex/AGENTS.md'} | {row['home'] for row in mapping['blocks']}
        content = {home: (ROOT / home).read_text() for home in homes}
        for prior, record in zip(source, mapping['blocks']):
            with self.subTest(line=prior['start_line']):
                self.assertEqual(record['start_line'], prior['start_line'])
                self.assertEqual(record['section'], prior['section'])
                self.assertEqual(record['sha256'], hashlib.sha256(prior['text'].encode()).hexdigest())
                self.assertIn(prior['text'], content[record['home']])
                self.assertEqual(sum(text.count(prior['text']) for text in content.values()), 1)
        self.assertGreater(len(homes), 4)

    def test_core_budget_and_mandatory_conditional_routes(self):
        core = (ROOT / 'dot_codex/AGENTS.md').read_text()
        self.assertLessEqual(len(core.encode()), 9000)
        self.assertLessEqual(len(core.splitlines()), 150)
        targets = re.findall(r'\]\((references/[^)#]+\.md)(?:#[^)]*)?\)', core)
        self.assertGreaterEqual(len(set(targets)), 6)
        for target in set(targets):
            path = ROOT / 'dot_codex' / target
            self.assertTrue(path.is_file(), target)
            self.assertLess(len(path.read_bytes()), 20000)
            line = next(line for line in core.splitlines() if f']({target})' in line)
            self.assertIn('MUST read', line)
        docs_route = next(line for line in core.splitlines() if '](references/documentation-and-config.md)' in line)
        self.assertIn('commits or pushes', docs_route)
        memory_route = next(line for line in core.splitlines() if '](references/session-memory.md)' in line)
        self.assertIn('personal-context, project/session context', memory_route)
        for retained in ('Evidence precedes every completion claim', 'Before the first modifying command',
                         'Never stage secrets', 'Active user and developer instructions',
                         'failing test or executable reproducer', 'standalone raw fish lines'):
            self.assertIn(retained, core)


if __name__ == '__main__':
    unittest.main()
