#!/usr/bin/env python3
"""Behavioral contracts for shared incident discovery, retrieval and review coverage."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / 'dot_agents/skills/postmortem-memory'
HELPER = SKILL / 'scripts/postmortem_memory.py'


class MemoryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'projects'
        self.root.mkdir()
        self.knowledge = self.base / 'knowledge'
        (self.knowledge / 'references').mkdir(parents=True)
        (self.knowledge / 'SKILL.md').write_text('# Fixture memory\n')
        self.source = self.report('app/docs/postmortem/one.md', 'Sandbox loopback failed. Approved path works.\n')
        self.digest = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.finding = dict(id='sandbox', reference='references/execution.md#sandbox',
                            status='verified_workaround', symptoms=['bwrap loopback failed'],
                            applicability='Command fails before shell execution',
                            diagnostics=['Check whether the shell started'], confidence='supported',
                            remedy='Use an approved narrow execution path',
                            verification='Approved read-only command exited zero',
                            verification_scope='workaround', limitations='Host sandbox remains broken',
                            sources=[self.digest])
        self.report_entry = dict(sha256=self.digest, aliases=[str(self.source)],
                                 reviewed_on='2026-10-05', findings=['sandbox'])
        self.ledger = dict(schema_version=1, roots=[str(self.root)],
                           reports=[self.report_entry], findings=[self.finding])
        (self.knowledge / 'references/execution.md').write_text('# Execution\n\n## sandbox\n\nFixture.\n')
        self.save()

    def report(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def save(self):
        (self.knowledge / 'sources.json').write_text(json.dumps(self.ledger))

    def cli(self, *args, expected=0):
        result = subprocess.run(['python3', '-B', str(HELPER), *args,
                                 '--knowledge', str(self.knowledge)], capture_output=True, text=True,
                                cwd=self.base)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_scan_deduplicates_copies_retaining_aliases_and_ignored_sources(self):
        copy = self.report('ignored/archive/docs/postmortems/copied.md', self.source.read_text())
        (self.root / '.gitignore').write_text('ignored/\n')
        data = self.cli('scan', '--root', str(self.root))
        self.assertEqual(len(data['documents']), 1)
        self.assertEqual(data['documents'][0]['aliases'], sorted([str(copy), str(self.source)]))
        self.assertIn(str(copy), data['unregistered_aliases'])
        self.assertEqual(data['unique_reports'], 1)

    def test_scan_new_and_changed_hashes(self):
        self.source.write_text('Different diagnosis\n')
        new = self.report('app/docs/incidents/two.md', '# Incident\nNew failure\n')
        data = self.cli('scan', '--root', str(self.root))
        self.assertEqual(data['changed'], [str(self.source)])
        self.assertIn(str(new), data['new'])

    def test_singular_plural_and_named_reports(self):
        for folder in ['incident', 'incidents', 'postmortem', 'postmortems', 'incident-reports']:
            self.report(f'other/{folder}/one.md', f'{folder} distinct report\n')
        self.report('other/docs/2026-incident-report.md', 'Named report\n')
        data = self.cli('scan', '--root', str(self.root))
        self.assertEqual(data['unique_reports'], 7)

    def test_private_and_build_paths_pruned_before_reads_and_symlinks_skipped(self):
        for folder in ['personal-context', 'private', '.private', 'node_modules', '.git', 'dist', '.next', 'venv']:
            self.report(f'{folder}/docs/postmortem/secret.md', 'DO NOT READ\n')
        self.report('app/docs/postmortem/personal-context-secret.md', 'DO NOT READ\n')
        self.report('app/docs/postmortem/template.md', 'Not a report\n')
        os.symlink(self.source, self.root / 'linked-incident.md')
        os.symlink(self.source.parent, self.root / 'postmortems')
        data = self.cli('scan', '--root', str(self.root))
        self.assertEqual(data['unique_reports'], 1)
        self.assertTrue(data['excluded'])

    def test_named_plan_prompt_and_skill_narratives_are_not_reports(self):
        for folder in ['plans', 'prompts', 'skills', 'tasks', 'benchmarks']:
            self.report(f'app/{folder}/postmortem-memory.md', 'Guidance, not an incident.\n')
        data = self.cli('scan', '--root', str(self.root))
        self.assertEqual(data['unique_reports'], 1)

    def test_genuine_report_about_template_failure_is_discovered(self):
        report = self.report('app/docs/postmortem/2026-10-05-template-substitution-failure.md',
                             '# Incident\n\n## Symptom\nTemplate substitution failed.\n')
        data = self.cli('scan', '--root', str(self.root))
        self.assertIn(str(report), data['new'])

    def test_missing_registered_source_is_incomplete_but_search_remains_available(self):
        self.source.unlink()
        data = self.cli('check', '--root', str(self.root), expected=1)
        self.assertIn(str(self.source), data['missing_sources'])
        self.assertTrue(self.cli('search', 'loopback')['matches'])

    def test_repeatable_roots_and_missing_root_are_explicit(self):
        data = self.cli('scan', '--root', str(self.root), '--root', str(self.root / 'app'))
        self.assertEqual(data['unique_reports'], 1)
        data = self.cli('scan', '--root', str(self.base / 'missing'), expected=1)
        self.assertIn('missing', str(data['errors']).lower())

    def test_unreadable_file_reports_incomplete_coverage(self):
        self.source.chmod(0)
        self.addCleanup(self.source.chmod, 0o600)
        data = self.cli('check', '--root', str(self.root), expected=1)
        self.assertIn('unreadable', str(data['errors']).lower())

    def test_unreadable_directory_reports_incomplete_coverage(self):
        self.source.parent.chmod(0)
        self.addCleanup(self.source.parent.chmod, 0o700)
        data = self.cli('scan', '--root', str(self.root), expected=1)
        self.assertIn('unreadable', str(data['errors']).lower())

    def test_scan_walk_error_is_reported(self):
        spec = importlib.util.spec_from_file_location('memory', HELPER)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        def broken_walk(root, **kwargs):
            kwargs['onerror'](PermissionError(13, 'Denied', str(root)))
            return iter(())
        with mock.patch.object(module.os, 'walk', broken_walk):
            data = module.discover([self.root])
        self.assertTrue(data['errors'])

    def test_search_returns_status_reference_applicability_sources(self):
        data = self.cli('search', 'bwrap loopback')
        hit = data['matches'][0]
        self.assertEqual(hit['status'], 'verified_workaround')
        self.assertEqual(hit['reference'], 'references/execution.md#sandbox')
        self.assertIn(str(self.source), str(hit['sources']))
        self.assertIn('shell', hit['applicability'])

    def test_search_miss_is_success_and_has_next_step(self):
        data = self.cli('search', 'unknown-holdout-error')
        self.assertEqual(data['matches'], [])
        self.assertTrue(data['next_step'])

    def test_check_fails_new_alias_until_registered(self):
        copy = self.report('copy/docs/incident/copy.md', self.source.read_text())
        data = self.cli('check', '--root', str(self.root), expected=1)
        self.assertIn(str(copy), str(data['errors']))
        self.report_entry['aliases'].append(str(copy))
        self.save()
        self.cli('check', '--root', str(self.root))

    def test_targeted_check_detects_changed_report_without_scanning_other_roots(self):
        self.ledger['roots'] = [str(self.base / 'missing')]
        self.save()
        self.cli('check', '--postmortem', str(self.source))
        self.source.write_text('Material update\n')
        data = self.cli('check', '--postmortem', str(self.source), expected=1)
        self.assertIn('changed', str(data['errors']).lower())

    def test_targeted_check_rejects_private_symlink_and_unrelated_document(self):
        private = self.report('personal-context/docs/postmortem/one.md', 'Private\n')
        ordinary = self.report('app/README.md', 'Narrative\n')
        link = self.root / 'incident-link.md'
        link.symlink_to(self.source)
        for path in [private, ordinary, link]:
            data = self.cli('check', '--postmortem', str(path), expected=1)
            self.assertTrue(data['errors'])

    def test_no_new_learning_requires_reason(self):
        self.report_entry['findings'] = []
        self.ledger['findings'] = []
        self.save()
        self.cli('check', '--root', str(self.root), expected=2)
        self.report_entry['decision'] = 'Reviewed; isolated typo provides no additional reusable guidance.'
        self.save()
        self.cli('check', '--root', str(self.root))

    def test_broken_reference_and_one_way_source_links_fail(self):
        self.finding['reference'] = 'references/missing.md#sandbox'
        self.save()
        self.cli('check', '--root', str(self.root), expected=2)
        self.finding['reference'] = 'references/execution.md#sandbox'
        self.finding['sources'] = []
        self.save()
        self.cli('check', '--root', str(self.root), expected=2)

    def test_reference_traversal_and_missing_anchor_fail(self):
        for reference in ['../outside.md#sandbox', 'references/execution.md#absent']:
            self.finding['reference'] = reference
            self.save()
            self.cli('check', '--root', str(self.root), expected=2)

    def test_status_and_evidence_scope_are_distinct(self):
        self.finding['status'] = 'unresolved'
        self.finding['confidence'] = 'hypothesis'
        self.finding['verification_scope'] = 'none'
        self.save()
        self.cli('check', '--root', str(self.root))
        self.finding['status'] = 'verified_fix'
        self.save()
        self.cli('check', '--root', str(self.root), expected=2)
        self.finding.update(status='activation_pending', confidence='confirmed', verification_scope='code')
        self.save()
        data = self.cli('search', 'bwrap')
        self.assertEqual(data['matches'][0]['status'], 'activation_pending')
        self.cli('check', '--root', str(self.root))

    def test_verified_remedy_can_have_supported_not_confirmed_root_cause(self):
        self.finding.update(status='verified_fix', confidence='supported', verification_scope='runtime')
        self.save()
        self.cli('check', '--root', str(self.root))

    def test_invalid_json_and_duplicate_ids_actionable(self):
        (self.knowledge / 'sources.json').write_text('{')
        data = self.cli('scan', '--root', str(self.root), expected=2)
        self.assertTrue(data['errors'])
        self.ledger['findings'].append(dict(self.finding))
        self.save()
        self.cli('check', '--root', str(self.root), expected=2)

    def test_malformed_links_report_the_invalid_field(self):
        self.finding['sources'] = None
        self.save()
        data = self.cli('check', '--root', str(self.root), expected=2)
        self.assertIn('sandbox', str(data['errors']))
        self.assertIn('sources', str(data['errors']))

    def test_read_only_commands_do_not_mutate_sources_or_knowledge(self):
        before = {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
        self.cli('scan', '--root', str(self.root))
        self.cli('search', 'loopback')
        self.cli('check', '--root', str(self.root))
        after = {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
        self.assertEqual(before, after)


class WorkflowTest(unittest.TestCase):
    def test_compact_skill_metadata_and_mandatory_lookup_learning(self):
        text = (SKILL / 'SKILL.md').read_text()
        self.assertIn('name: postmortem-memory', text)
        self.assertLess(len(text.split()), 650)
        self.assertIn('before', text.lower())
        self.assertIn('read-only', text)
        policy = (REPO / 'dot_codex/AGENTS.md').read_text()
        self.assertIn('postmortem-memory', policy)
        self.assertIn('--postmortem', policy)
        self.assertTrue((SKILL / 'agents/openai.yaml').is_file())
        for file in ['README.md', 'dot_agents/skills/README.md', 'docs/smoke-tests.md']:
            self.assertIn('postmortem-memory', (REPO / file).read_text())

    def test_actual_ledger_reference_status_and_coverage(self):
        result = subprocess.run(['python3', '-B', str(HELPER), 'check'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertGreater(data['unique_reports'], 150)
        self.assertGreater(data['finding_count'], 15)


if __name__ == '__main__':
    unittest.main()
