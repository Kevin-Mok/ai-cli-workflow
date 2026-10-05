#!/usr/bin/env python3
"""Exercise cross-repository retrieval and synthetic learning in a temporary fixture."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / 'dot_agents/skills/postmortem-memory'
HELPER = SKILL / 'scripts/postmortem_memory.py'


def main():
    with tempfile.TemporaryDirectory(prefix='postmortem-memory-smoke-') as temp:
        base = Path(temp)
        project = base / 'another-repository'
        project.mkdir()
        def run(*args, expected=0):
            result = subprocess.run(['python3', '-B', str(HELPER), *args], cwd=project,
                                    capture_output=True, text=True)
            if result.returncode != expected:
                raise RuntimeError(f'Expected {expected}, got {result.returncode}: {result.stdout}{result.stderr}')
            return json.loads(result.stdout)
        known = run('search', 'bwrap loopback')
        assert any(hit['status'] == 'verified_workaround' for hit in known['matches'])
        assert Path(known['knowledge']) == SKILL
        knowledge = base / 'fixture-knowledge'
        (knowledge / 'references').mkdir(parents=True)
        (knowledge / 'SKILL.md').write_text('# Fixture memory\n')
        (knowledge / 'references/execution.md').write_text('# Execution\n\n## synthetic-retry\n\nFixture only.\n')
        report = project / 'docs/postmortem/synthetic.md'
        report.parent.mkdir(parents=True)
        report.write_text('# Synthetic retry failure\n\nDiagnosis remains unverified.\n')
        digest = hashlib.sha256(report.read_bytes()).hexdigest()
        finding = dict(id='synthetic-retry', reference='references/execution.md#synthetic-retry',
                       status='unresolved', symptoms=['synthetic retry failure'],
                       applicability='Temporary fixture only', diagnostics=['Reproduce the fixture'],
                       confidence='hypothesis', remedy='Test the candidate remedy',
                       verification='No remedy verified yet', verification_scope='none',
                       limitations='No production or runtime claim', sources=[digest])
        entry = dict(sha256=digest, aliases=[str(report)], reviewed_on='2026-10-05', findings=[finding['id']])
        ledger = dict(schema_version=1, roots=[str(project)], reports=[entry], findings=[finding])
        def save():
            (knowledge / 'sources.json').write_text(json.dumps(ledger))
        save()
        run('check', '--knowledge', str(knowledge), '--postmortem', str(report))
        report.write_text('# Synthetic retry failure\n\nFixture code check passed; live activation pending.\n')
        stale = run('check', '--knowledge', str(knowledge), '--postmortem', str(report), expected=1)
        assert stale['changed'] == [str(report)]
        # Simulate Codex's explicit review/update, not a helper mutation command.
        digest = hashlib.sha256(report.read_bytes()).hexdigest()
        entry['sha256'] = digest
        finding.update(status='activation_pending', confidence='confirmed', verification_scope='code',
                       verification='Synthetic fixture code check passed; no runtime observation',
                       remedy='Activate the fixture runtime when authorized', sources=[digest])
        save()
        run('check', '--knowledge', str(knowledge), '--postmortem', str(report))
        updated = run('search', 'synthetic retry', '--knowledge', str(knowledge))
        assert updated['matches'][0]['status'] == 'activation_pending'
        assert updated['matches'][0]['verification_scope'] == 'code'
    print('PASS: cross-repo tracked lookup; stale hash rejected; reviewed learning updated; activation remains pending; fixture removed.')


if __name__ == '__main__':
    main()
