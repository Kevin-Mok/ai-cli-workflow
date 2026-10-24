"""Keep the public admission precedents complete without the private audit input."""

import re
import json
import io
import runpy
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / 'dot_agents/skills/lean-instructions/references/vetted-skills.md'
EXISTING = set('''smoke-test-capture ai-workflow-doctor postmortem-memory
context-handoff playwright morning metaprompt feedback-memory night
readme-recruiter-sync second-brain-session commit-dirty fish-alias commit-plan-push
cto-jarvis metaprompt-run commit-session personal-context next-tasks
brand-system-designer impeccable frontend-design teach-impeccable paper-shaders
trickle-ui no-comments pstack gh-fix-ci long-task-harness motion-primitives open-pr
leetcode-init ui-ux-pro-max screenshot last30days transcribe pdf commit-plan
find-skills design-taste-frontend playwright-interactive ui-styling typeset slides
scroll-world review-animations redesign-existing-projects quieter polish overdrive
optimize openai-docs onboard normalize minimalist-ui metaprompt-alxve imagegen
high-end-visual-design harden full-output-enforcement extract distill design-system
design delight critique colorize clarify brand bolder banner-design audit arrange
animate adapt 21st-registry 21st-design-sync 21st-cli-use 21st-ai'''.split())
PROPOSED = {
    'pr-12:grok-cli-handoff', 'pr-16:caveman', 'pr-25:canvas-ui',
    'pr-33:skill-eval', 'pr-34:anthropic-frontend-design',
    'pr-35:stitch-design-md', 'pr-36:ui-ux-pro-max',
    'pr-37:feedback-memory', 'pr-38:impeccable',
    'pr-39:vercel-react-best-practices', 'pr-46:shadcn',
    'pr-53:motion-prompt', 'pr-54:huashu-art-motion',
}
VERDICTS = {'KEEP', 'CULL', 'ADD', 'REJECT', 'MERGED-INTO'}


def entries(source):
    """Read the documented table shape, retaining verdict groups for validation."""
    verdict = None
    result = []
    for line in source.splitlines():
        if re.match(r'^#{2,3} (KEEP|CULL|ADD|REJECT|MERGED-INTO)$', line):
            verdict = line.split()[-1]
        if not re.match(r'\| (?:existing:|pr-\d+:)', line):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if len(cells) != 10:
            raise ValueError(f'{cells[0]}: expected ten calibration columns')
        result.append(dict(zip(('id', 'value', 'uniqueness', 'description_chars',
                                'body_bytes', 'cost_tokens', 'score', 'why',
                                'evidence', 'survivor'), cells), verdict=verdict))
    return result


class VettedSkillsTest(unittest.TestCase):
    def source(self):
        self.assertTrue(REFERENCE.is_file(), 'complete on-demand calibration reference is missing')
        return REFERENCE.read_text()

    def test_every_ranked_candidate_has_one_distinct_public_id(self):
        rows = entries(self.source())
        expected = {f'existing:{name}' for name in EXISTING} | PROPOSED | {'pr-55:file-size-guard'}
        self.assertEqual(len(EXISTING), 79)
        self.assertEqual(len(PROPOSED), 13)
        self.assertEqual(len(rows), 93)
        self.assertEqual({row['id'] for row in rows}, expected)
        self.assertEqual(len({row['id'] for row in rows}), len(rows))
        self.assertEqual({row['verdict'] for row in rows}, VERDICTS)

    def test_scores_are_audit_estimates_with_explicit_unscored_exceptions(self):
        source = self.source()
        rows = entries(source)
        self.assertIn('description chars/4 + body bytes/40', source)
        self.assertIn('10% body-load assumption', source)
        self.assertIn('not current measurements', source)
        unscored = {'pr-37:feedback-memory', 'pr-55:file-size-guard'}
        for row in rows:
            with self.subTest(candidate=row['id']):
                self.assertTrue(row['why'])
                self.assertTrue(row['evidence'])
                if row['id'] in unscored:
                    for key in ('value', 'uniqueness', 'cost_tokens', 'score'):
                        self.assertEqual(row[key], 'unknown')
                    self.assertIn('not scored', row['evidence'])
                    continue
                self.assertIn(int(row['value']), range(6))
                self.assertIn(int(row['uniqueness']), range(3))
                cost = int(row['description_chars']) / 4 + int(row['body_bytes']) / 40
                self.assertAlmostEqual(float(row['cost_tokens']), cost, delta=1)
                expected_score = (2 * int(row['value']) + int(row['uniqueness'])) / (cost / 100)
                self.assertAlmostEqual(float(row['score']), expected_score, delta=0.02)

    def test_overrides_merges_swap_and_approved_roster_remain_explicit(self):
        source = self.source()
        rows = {row['id']: row for row in entries(source)}
        self.assertEqual(rows['existing:last30days']['verdict'], 'KEEP')
        self.assertLess(float(rows['existing:last30days']['score']), 1)
        self.assertIn('user override', rows['existing:last30days']['why'])
        for loser, survivor in (('long-task-harness', 'context-handoff'),
                                ('commit-plan', 'commit-plan-push')):
            self.assertEqual(rows[f'existing:{loser}']['verdict'], 'MERGED-INTO')
            self.assertEqual(rows[f'existing:{loser}']['survivor'], f'existing:{survivor}')
        self.assertEqual(rows['existing:impeccable']['survivor'], 'pr-38:impeccable')
        self.assertIn('same-slot swap', source)
        approved = {row['id'] for row in rows.values() if row['verdict'] == 'ADD'}
        self.assertEqual(approved, {
            'pr-12:grok-cli-handoff', 'pr-33:skill-eval', 'pr-37:feedback-memory',
            'pr-38:impeccable', 'pr-39:vercel-react-best-practices',
            'pr-46:shadcn', 'pr-55:file-size-guard',
        })
        rejected = {row['id'] for row in rows.values() if row['verdict'] == 'REJECT'}
        self.assertEqual(rejected, PROPOSED - (approved & PROPOSED))
        self.assertIn('20668', source)
        self.assertIn('8000', rows['pr-46:shadcn']['body_bytes'])
        self.assertIn('zero recurring tokens', rows['pr-55:file-size-guard']['evidence'])
        known = set(rows) | {'system:imagegen', 'system:openai-docs'}
        for row in rows.values():
            for survivor in row['survivor'].split(', '):
                self.assertIn(survivor, known | {'none'})

    def test_evidence_stays_aggregate_and_reference_stays_on_demand(self):
        source = self.source()
        self.assertIn('heuristic', source)
        self.assertIn('all-cwd', source)
        self.assertIn('Patterns', source)
        self.assertNotRegex(source, r'(?:/home/|~/|session[_-]id|session_meta|github\.com[:/])')
        self.assertNotRegex(source, r'(?m)^>')
        self.assertNotRegex(source, r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f-]{23}\b')

    def sync_api(self):
        path = ROOT / 'scripts/sync-vetted-skills'
        self.assertTrue(path.is_file(), 'inventory and drift CLI is missing')
        return runpy.run_path(str(path))

    def test_live_inventory_and_current_active_snapshot_do_not_drift(self):
        api = self.sync_api()
        report = api['audit'](ROOT, Path.home())
        self.assertEqual(report['errors'], [])
        self.assertTrue(report['installed_only'])
        self.assertTrue(any(row['kind'] == 'builtin' for row in report['skills']))
        self.assertTrue(any(row['verdict'] == 'CULL' for row in report['installed_only']))
        self.assertFalse(any(row['active'] for row in report['installed_only']))

    def test_inventory_detects_add_remove_trigger_drift_and_installed_collisions(self):
        api = self.sync_api()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'repo'
            home = Path(directory) / 'host'
            root.mkdir()
            home.mkdir()
            skill = root / 'dot_agents/skills/example/SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('---\nname: example\ndescription: Use for example tasks.\n---\nJob.\n')
            (root / '.chezmoiexternal.toml.tmpl').write_text('')
            report = api['collect'](root, home)
            self.assertEqual(len(report), 1)
            record = report[0]
            snapshot = {record['id']: {'candidate': 'existing:example',
                                      'description_sha256': record['description_sha256'],
                                      'description': 'Use for example tasks.',
                                      'scopes': record['scopes'], 'job': 'Example tasks'}}
            known = {'existing:example': 'KEEP'}
            self.assertEqual(api['drift_errors'](report, snapshot, {}, known), [])
            self.assertTrue(api['drift_errors']([], snapshot, {}, known))
            changed = dict(record, description_sha256='changed')
            self.assertTrue(api['drift_errors']([changed], snapshot, {}, known))
            changed = dict(record, description='An unrelated trigger despite an unchanged hash.')
            self.assertTrue(api['drift_errors']([changed], snapshot, {}, known))
            extra = dict(record, id='repo:unexpected', name='unexpected')
            self.assertTrue(api['drift_errors']([record, extra], snapshot, {}, known))
            builtin = dict(record, id='builtin:example', kind='builtin', active=False)
            self.assertTrue(api['drift_errors']([record, builtin], snapshot, {}, known),
                            'same slug in a different origin needs its own entry')
            self.assertTrue(any('contradicts CULL' in error for error in
                                api['drift_errors']([record], snapshot, {}, {'existing:example': 'CULL'})))

    def test_external_installer_and_builtin_exports_are_read_without_running_installers(self):
        api = self.sync_api()
        with tempfile.TemporaryDirectory() as directory:
            root, home = Path(directory) / 'repo', Path(directory) / 'host'
            root.mkdir()
            home.mkdir()
            (root / '.chezmoiexternal.toml.tmpl').write_text(
                '{{ if true }}\n[".codex/skills/upstreams/sample"]\n'
                'type = "git-repo"\nurl = "unused"\n{{ end }}\n')
            (root / 'run_after_install-test.sh').write_text('exit 99\ncodex plugin add widget@market\n')
            paths = (
                '.codex/skills/upstreams/sample/skills/external-job/SKILL.md',
                '.codex/plugins/cache/market/widget/1.2.3/skills/plugin-job/SKILL.md',
                '.codex/skills/.system/system-job/SKILL.md',
            )
            for relative in paths:
                path = home / relative
                path.parent.mkdir(parents=True)
                path.write_text('---\nname: fixture\ndescription: Use for fixture tasks.\n---\nJob.\n')
            records = {row['id']: row for row in api['collect'](root, home)}
            self.assertTrue(records['external:sample:external-job']['active'])
            self.assertTrue(records['plugin:market:widget:plugin-job']['active'])
            self.assertFalse(records['builtin:system-job']['active'])
            self.assertEqual(records['builtin:system-job']['kind'], 'builtin')
            self.assertEqual(records['external:sample:external-job']['description'], 'Use for fixture tasks.')
            (home / paths[0]).unlink()
            with self.assertRaisesRegex(ValueError, 'configured source unavailable'):
                api['collect'](root, home)

    def test_overlap_search_has_real_trigger_text_and_meaningful_jobs(self):
        api = self.sync_api()
        _, data = api['load_reference'](REFERENCE)
        records = {row['id']: row for row in api['collect'](ROOT, Path.home())}
        for identity, entry in data['active'].items():
            with self.subTest(identity=identity):
                self.assertEqual(entry['description'], records[identity]['description'])
                self.assertNotEqual(entry['job'], records[identity]['name'].replace('-', ' ') + ' workflow.')
        for identity, entry in data['unranked'].items():
            with self.subTest(precedent=identity):
                self.assertEqual(entry['description'], records[identity]['description'])
                self.assertEqual(entry['description_basis'], 'detected public skill frontmatter')
                self.assertTrue(entry['job'])

    def test_source_read_errors_hide_raw_host_diagnostics(self):
        api = self.sync_api()
        output = io.StringIO()

        def unreadable(*args):
            raise OSError('hidden-host-path')

        with patch.dict(api['main'].__globals__, {'audit': unreadable}), patch('sys.argv', ['sync-vetted-skills', '--plain']), redirect_stderr(output):
            self.assertEqual(api['main'](), 2)
        self.assertIn('check source availability and file permissions', output.getvalue())
        self.assertNotIn('hidden-host-path', output.getvalue())

    def test_culled_history_preserves_exact_removals_without_fabricating_a_sha(self):
        api = self.sync_api()
        data = api['load_reference'](REFERENCE)[1]
        manifest = json.loads((ROOT / 'benchmarks/trim/CULL.json').read_text())
        expected = {f'existing:{row["name"]}' for row in manifest['local_removed']}
        local = {row['candidate'] for row in data['history'] if row['scope'] == 'repo source removed'}
        self.assertEqual(local, expected)
        self.assertIn('## Culled', self.source())
        for row in data['history']:
            self.assertEqual(row['date'], '2026-10-22')
            self.assertTrue(row['reason'])
            self.assertTrue(row['evidence'])
            self.assertTrue(row['survivor'])
            self.assertRegex(row['commit'], r'^(?:pending: .+|[0-9a-f]{40})$')
        retired = {row['candidate'] for row in data['history'] if row['scope'].startswith('config retired')}
        self.assertTrue({f'existing:{name}' for name in (
            '21st-ai', '21st-cli-use', '21st-design-sync', '21st-registry',
            'review-animations', 'scroll-world')} <= retired)
        self.assertTrue(any(name.startswith('external:superpowers:') for name in retired))
        for row in data['unranked'].values():
            self.assertIn(row['verdict'], ('UNSCORED', 'CULL'))
            self.assertTrue(row['job'])


if __name__ == '__main__':
    unittest.main()
