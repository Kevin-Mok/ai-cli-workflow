"""Synthetic compact retrieval, cache, refresh and cross-store erasure tests."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'dot_agents/skills/personal-context/scripts/context_store.py'

class KnowledgeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='context-knowledge-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'private'
        self.root.mkdir()
        self.coding = self.base / 'coding'
        self.coding.mkdir()

    def run_cli(self, *args, payload=None, root=None):
        return subprocess.run([sys.executable, '-B', str(SCRIPT), '--root', str(root or self.root), *args], input=json.dumps(payload) if payload is not None else None, capture_output=True, text=True)

    def command(self, *args, payload=None):
        result = self.run_cli(*args, payload=payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def entry(self, n=0, **changes):
        record = dict(id=f'design-{n}', key=f'design.{n}', topic='design', statement='Synthetic preference '+ ('spacious ' * 70), basis='inferred', source={'ref':'synthetic-discussion', 'as_of':'2026-01-01'}, scope='Synthetic prototype decisions only', implication='Compare options with the stated audience requirements.')
        record.update(changes)
        return record

    def project(self, name='app'):
        p = self.coding / name
        p.mkdir()
        (p / 'package.json').write_text(json.dumps({'name':name, 'dependencies':{'react':'1','typescript':'1'}, 'scripts':{'test':'vitest'}}))
        (p / 'README.md').write_text('# Synthetic dashboard\n\nA dashboard for synthetic tasks.\n\nKeep secrets server side.\n')
        (p / 'src').mkdir()
        (p / 'src/main.tsx').write_text('export function App() { return <main>Demo</main>; }')
        self.git(p,'init','-q')
        self.commit(p)
        return p

    def git(self, project, *args):
        result=subprocess.run(['git','-C',str(project),*args],capture_output=True,text=True,env={**os.environ,'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null'})
        self.assertEqual(result.returncode,0,result.stderr)
        return result.stdout

    def commit(self, project, author='example-user Mok'):
        self.git(project,'add','.')
        self.git(project,'-c','user.name='+author,'-c','user.email=synthetic@example.invalid','commit','-qm','Synthetic authored fixture')

    def test_empty_compact_reads_do_not_initialize(self):
        absent = self.base / 'absent'
        for command in ('topics', 'projects', 'brief'):
            result = self.run_cli(command, root=absent)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['records'], [])
        self.assertFalse(absent.exists())

    def test_briefs_are_bounded_keep_qualifications_and_reduce_full_read(self):
        self.command('update','--payload','-',payload={'entries':[self.entry(n) for n in range(25)]})
        output = self.run_cli('brief','--topic','design')
        self.assertEqual(output.returncode,0,output.stderr)
        brief=json.loads(output.stdout)
        self.assertLessEqual(len(output.stdout.rstrip()),6000)
        self.assertLessEqual(len(brief['records']),8)
        self.assertGreater(brief['omitted'],0)
        row=brief['records'][0]
        for field in ('id','statement','scope','basis','status','evidence_dates','implication'):
            self.assertIn(field,row)
        self.assertEqual(row['status'],'unconfirmed')
        full=self.run_cli('read')
        self.assertLess(len(output.stdout),len(full.stdout)*0.5)
        small=self.run_cli('brief','--limit','2','--char-budget','1600')
        self.assertLessEqual(len(small.stdout.rstrip()),1600)
        self.assertLessEqual(len(json.loads(small.stdout)['records']),2)
        detail=self.command('detail','--id',row['id'])
        self.assertEqual(detail['record']['source']['as_of'],'2026-01-01')

    def test_cache_rebuilds_deterministically_and_correction_removes_old_projection(self):
        self.command('update','--payload','-',payload={'entries':[self.entry()]})
        self.command('brief')
        cache=self.root/'ai-context/cache/topic-briefs.json'
        first=cache.read_bytes()
        self.command('brief')
        self.assertEqual(first,cache.read_bytes())
        d=json.loads(first)
        self.assertEqual(d['format_version'],1)
        self.assertIn('sha256',d['inputs']['personal'])
        cache.write_text('{broken'); cache.chmod(0o600)
        self.command('brief'); self.assertEqual(first,cache.read_bytes())
        self.command('update','--payload','-',payload={'entries':[self.entry(id='correction',statement='A corrected synthetic statement',basis='user_stated')]})
        brief=self.command('brief')
        self.assertEqual([x['id'] for x in brief['records']],['correction'])
        self.assertNotIn('spacious',cache.read_text())

    def test_invalid_authoritative_store_is_preserved_and_cache_not_trusted(self):
        self.command('update','--payload','-',payload={'entries':[self.entry()]})
        self.command('brief')
        path=self.root/'ai-context/context.json'
        path.write_text('{broken')
        result=self.run_cli('brief')
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(path.read_text(),'{broken')
        self.assertNotIn('Synthetic',result.stderr)

    def test_project_foundation_refresh_hashes_and_search(self):
        p=self.project()
        result=self.command('foundation','--coding-root',str(self.coding),'--batch-size','1')
        self.assertEqual(result['projects'],1)
        rows=self.command('projects','--query','react')['records']
        self.assertEqual(len(rows),1)
        identifier=rows[0]['id']
        detail=self.command('detail','--id',identifier)['record']
        self.assertTrue(detail['sources'])
        readme=next(x for x in detail['sources'] if x['path'].endswith('README.md'))
        self.assertEqual(readme['sha256'],hashlib.sha256((p/'README.md').read_bytes()).hexdigest())
        before=self.root.joinpath('ai-context/project-knowledge.json').read_bytes()
        self.assertEqual(self.command('foundation','--coding-root',str(self.coding))['changed_projects'],0)
        self.assertEqual(before,self.root.joinpath('ai-context/project-knowledge.json').read_bytes())
        (p/'README.md').write_text('# Synthetic revised dashboard\n\nRevised example architecture.\n')
        self.commit(p)
        refresh=self.command('foundation','--coding-root',str(self.coding),'--project',identifier)
        self.assertEqual(refresh['changed_projects'],1)
        fresh=self.command('detail','--id',identifier)['record']
        self.assertNotEqual(detail['fingerprint'],fresh['fingerprint'])
        self.assertEqual(len(self.command('brief','--project',identifier)['records']),1)

    def test_forgetting_removes_projects_findings_and_cache_and_suppresses_rebuild(self):
        self.project('one'); self.project('two')
        self.command('foundation','--coding-root',str(self.coding))
        catalog=self.command('projects')['records']
        detail=self.command('detail','--id',catalog[0]['id'])['record']
        self.command('brief')
        self.command('update','--payload','-',payload={'forget_keys':[detail['key']]})
        self.assertEqual(len(self.command('projects')['records']),1)
        raw=json.loads((self.root/'ai-context/project-knowledge.json').read_text())
        self.assertNotIn(detail['id'],json.dumps(raw['projects']))
        for finding in raw['findings']:
            self.assertNotIn(detail['id'],json.dumps(finding['evidence']))
        cache=(self.root/'ai-context/cache/topic-briefs.json').read_text()
        self.assertNotIn(detail['id'],cache)
        self.command('foundation','--coding-root',str(self.coding))
        self.assertEqual(len(self.command('projects')['records']),1)
        self.assertNotEqual(self.run_cli('detail','--id',detail['id']).returncode,0)

    def test_cache_symlink_is_not_followed_and_direct_projection_still_works(self):
        self.command('update','--payload','-',payload={'entries':[self.entry()]})
        sentinel=self.base/'sentinel'; sentinel.write_text('unchanged')
        (self.root/'ai-context/cache').symlink_to(self.base,target_is_directory=True)
        result=self.command('brief')
        self.assertEqual(len(result['records']),1)
        self.assertEqual(sentinel.read_text(),'unchanged')
        self.assertFalse((self.base/'topic-briefs.json').exists())

    def test_parallel_foundation_and_updates_preserve_all_records_and_permissions(self):
        self.project()
        def action(n):
            if n%2:
                return self.run_cli('update','--payload','-',payload={'entries':[self.entry(n)]})
            return self.run_cli('foundation','--coding-root',str(self.coding))
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            results=list(executor.map(action,range(12)))
        for result in results:
            self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(len(self.command('read')['entries']),6)
        self.assertEqual(len(self.command('projects')['records']),1)
        self.command('brief')
        for path in self.root.joinpath('ai-context').rglob('*'):
            self.assertEqual(path.stat().st_mode&0o777,0o700 if path.is_dir() else 0o600)

    def test_foundation_repairs_owned_private_modes_on_unchanged_store(self):
        self.project(); self.command('foundation','--coding-root',str(self.coding))
        path=self.root/'ai-context/project-knowledge.json'
        path.chmod(0o644)
        self.command('foundation','--coding-root',str(self.coding))
        self.assertEqual(path.stat().st_mode & 0o777,0o600)
        self.assertEqual(len(self.command('projects')['records']),1)

    def test_forgetting_cleans_private_cache_even_when_directory_mode_drifted(self):
        self.command('update','--payload','-',payload={'entries':[self.entry()]})
        self.command('brief')
        cache=self.root/'ai-context/cache'
        cache.chmod(0o500)
        self.command('update','--payload','-',payload={'forget_keys':['design.0']})
        cache.chmod(0o700)
        self.assertFalse((cache/'topic-briefs.json').exists())
        self.assertEqual(self.command('brief')['records'],[])

    def test_deleted_project_refresh_marks_historical_evidence_unavailable(self):
        p=self.project(); self.command('foundation','--coding-root',str(self.coding))
        identifier=self.command('projects')['records'][0]['id']
        import shutil
        shutil.rmtree(p)
        self.command('foundation','--coding-root',str(self.coding),'--project',identifier)
        row=self.command('brief','--project',identifier)['records'][0]
        self.assertEqual(row['availability'],'unavailable')
        self.assertIn('historical',row['scope'])
        self.assertTrue(self.command('detail','--id',identifier)['record']['unavailable'])

    def test_missing_project_is_not_used_in_current_recurring_findings(self):
        first=self.project('one'); self.project('two')
        self.command('foundation','--coding-root',str(self.coding))
        import shutil
        shutil.rmtree(first)
        self.command('foundation','--coding-root',str(self.coding))
        knowledge=json.loads((self.root/'ai-context/project-knowledge.json').read_text())
        self.assertEqual(knowledge['findings'],[])

    def test_sources_include_verified_example-user_mok_commit_provenance(self):
        p=self.project()
        self.command('foundation','--coding-root',str(self.coding))
        identifier=self.command('projects')['records'][0]['id']
        record=self.command('detail','--id',identifier)['record']
        self.assertIn('provenance_version',record)
        self.assertEqual(record['provenance_version'],1)
        for source in record['sources']:
            evidence=source['author_evidence']
            self.assertEqual(evidence['author'],'example-user Mok')
            self.assertEqual(evidence['blob_sha256'],source['sha256'])
            self.assertEqual(self.git(p,'show','-s','--format=%an',evidence['commit']).strip(),'example-user Mok')
        row=self.command('brief','--project',identifier)['records'][0]
        self.assertIn('example-user Mok',row['evidence_basis'])

    def test_uncommitted_and_other_author_sources_are_not_indexed(self):
        p=self.project()
        (p/'README.md').write_text('# Other author material\n\nDocumentation written by someone else.\n')
        self.commit(p,author='Other Author')
        (p/'src/main.tsx').write_text('export const dirtyPrivatePayload = true;')
        self.command('foundation','--coding-root',str(self.coding))
        rows=self.command('projects')['records']
        if rows:
            record=self.command('detail','--id',rows[0]['id'])['record']
            names=[source['path'] for source in record['sources']]
            self.assertNotIn('app/README.md',names)
            self.assertNotIn('app/src/main.tsx',names)
            self.assertNotIn('Other author material',json.dumps(record))
            self.assertNotIn('dirtyPrivatePayload',json.dumps(record))

    def test_empty_existing_store_directory_is_not_initialized_by_retrieval(self):
        directory=self.root/'ai-context'; directory.mkdir(mode=0o700)
        for command in ('topics','projects','brief'):
            self.assertEqual(self.command(command)['records'],[])
        self.assertEqual(list(directory.iterdir()),[])

    def test_forgetting_a_technical_finding_scrubs_project_patterns_and_cache(self):
        self.project('one'); self.project('two')
        self.command('foundation','--coding-root',str(self.coding))
        path=self.root/'ai-context/project-knowledge.json'
        data=json.loads(path.read_text())
        self.assertTrue(data['findings'])
        finding=data['findings'][0]
        pattern=finding['statement'].removesuffix(' appears in multiple inspected projects.')
        self.command('update','--payload','-',payload={'forget_keys':[finding['key']]})
        self.command('brief')
        self.assertNotIn(pattern,path.read_text())
        self.assertNotIn(pattern,(self.root/'ai-context/cache/topic-briefs.json').read_text())
        self.command('foundation','--coding-root',str(self.coding))
        self.assertNotIn(pattern,path.read_text())

    def test_real_coding_sources_cannot_use_a_synthetic_storage_override(self):
        import importlib.util
        from types import SimpleNamespace
        from unittest import mock
        spec=importlib.util.spec_from_file_location('fixture_store',SCRIPT)
        module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        knowledge=module._knowledge()
        synthetic_sources=SimpleNamespace(discover_projects=lambda _: [], inspect_project=lambda *_: None, recurring_findings=lambda _: [])
        # No actual coding sources are inspected during this boundary reproducer.
        with mock.patch.object(knowledge.c,'_sibling',return_value=synthetic_sources):
            for source_root in (Path('/home/example/coding'),Path('/home/example/coding/../coding'),Path('/home/example/coding/subproject'),Path('/home/example')):
                with self.subTest(source_root=source_root), self.assertRaises(module.StoreError):
                    knowledge.foundation(self.root,source_root)
        self.assertFalse((self.root/'ai-context').exists())

    def test_corrupt_project_store_rejects_updates_without_replacing_evidence(self):
        self.project(); self.command('foundation','--coding-root',str(self.coding))
        path=self.root/'ai-context/project-knowledge.json'
        path.write_text('{broken')
        for args in [('projects',),('foundation','--coding-root',str(self.coding)),('update','--payload','-')]:
            result=self.run_cli(*args,payload={'forget_keys':['project.example']} if args[0]=='update' else None)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(path.read_text(),'{broken')

if __name__=='__main__': unittest.main()
