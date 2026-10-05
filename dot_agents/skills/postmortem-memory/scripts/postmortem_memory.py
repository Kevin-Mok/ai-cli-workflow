#!/usr/bin/env python3
"""Read-only discovery, retrieval and coverage checks for human-reviewed incident memory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

TRACKED = Path('/home/example/linux-config/dot_agents/skills/postmortem-memory')
DEFAULT_ROOTS = [Path('/home/example/coding'), Path('/home/example/linux-config')]
PRUNED = {'.git', '.hg', '.svn', 'node_modules', 'bower_components', 'vendor',
          '.venv', 'venv', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache',
          'dist', 'build', '.next', '.nuxt', '.cache', 'coverage', 'target', '.tox',
          'site-packages', 'templates', '.superpowers', 'personal-context', 'private', '.private', 'personal'}
REPORT_DIRS = {'postmortem', 'postmortems', 'incident', 'incidents',
               'incident-report', 'incident-reports', 'incident_reports'}
STATUSES = {'verified_fix', 'verified_workaround', 'unresolved', 'activation_pending'}
SCOPES = {'runtime', 'code', 'workaround', 'none'}


def excluded(path):
    """Check lexical names before resolution, traversal or reads."""
    return any(p.lower() in PRUNED or 'personal-context' in p.lower() for p in path.parts)


def template_artifact(path):
    stem = path.stem.lower()
    return stem == 'template' or stem.endswith(('-template', '_template', '.template')) or stem.startswith(('template-', 'template_'))


def eligible(path):
    name = path.name.lower()
    return (not excluded(path) and path.suffix.lower() in {'.md', '.txt', '.rst'}
            and not template_artifact(path) and name not in {'readme.md', 'index.md'}
            and (any(p.lower() in REPORT_DIRS for p in path.parts[:-1])
                 or (not any(p.lower() in {'plans', 'prompts', 'skills', 'tasks', 'benchmarks'} for p in path.parts[:-1])
                     and ('postmortem' in name or re.search(r'(^|[-_])incident([-_.]|$)', name)))))


def readable(path, directory=False):
    mode = path.stat().st_mode
    # Mode check also makes denied sources explicit for privileged readers.
    return bool(mode & (stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)) and (
        not directory or bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)))


def symlink_component(path):
    return any(p.is_symlink() for p in [path, *path.parents])


def read_report(path):
    if not eligible(path) or symlink_component(path):
        raise ValueError(f'Excluded, symlinked or ineligible postmortem: {path}')
    if not path.is_file() or not readable(path) or any(
            not readable(p, directory=True) for p in path.parents):
        raise OSError(f'Unreadable postmortem: {path}')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def discover(roots):
    """Walk all physical sources, ignoring gitignore; return errors rather than silence."""
    hashes = {}
    errors = []
    exclusions = []
    seen = set()
    for value in roots:
        root = Path(os.path.abspath(value))
        if excluded(root) or symlink_component(root):
            exclusions.append({'path': str(root), 'reason': 'private/build/symlink root'})
            continue
        if not root.is_dir():
            errors.append(f'Missing or non-directory root: {root}')
            continue
        if not readable(root, directory=True):
            errors.append(f'Unreadable directory: {root}')
            continue
        for current, dirs, files in os.walk(root, followlinks=False,
                                           onerror=lambda error: errors.append(str(error))):
            base = Path(current)
            kept = []
            for name in sorted(dirs):
                path = base / name
                if excluded(path) or path.is_symlink():
                    exclusions.append({'path': str(path), 'reason': 'private/build/symlink directory'})
                elif not readable(path, directory=True):
                    errors.append(f'Unreadable directory: {path}')
                else:
                    kept.append(name)
            dirs[:] = kept
            for name in sorted(files):
                path = base / name
                if str(path) in seen:
                    continue
                seen.add(str(path))
                if path.is_symlink() or excluded(path) or template_artifact(path):
                    if path.suffix.lower() in {'.md', '.rst', '.txt'}:
                        exclusions.append({'path': str(path), 'reason': 'private/template/symlink file'})
                    continue
                if not eligible(path):
                    continue
                try:
                    digest = read_report(path)
                    hashes.setdefault(digest, []).append(str(path))
                except (OSError, ValueError) as error:
                    errors.append(str(error))
    return {'documents': [{'sha256': h, 'aliases': sorted(set(a))}
                          for h, a in sorted(hashes.items())],
            'unique_reports': len(hashes),
            'document_count': sum(len(set(a)) for a in hashes.values()),
            'errors': sorted(set(errors)), 'excluded': exclusions}


def load_ledger(knowledge):
    try:
        ledger = json.loads((knowledge / 'sources.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        raise ValueError(f'Cannot load sources.json at {knowledge}: {error}') from error
    errors = []
    if not isinstance(ledger, dict) or ledger.get('schema_version') != 1:
        raise ValueError('sources.json: expected object with schema_version 1')
    reports = ledger.get('reports')
    findings = ledger.get('findings')
    if not isinstance(reports, list) or not isinstance(findings, list):
        raise ValueError('sources.json: reports and findings must be lists')
    by_hash = {}
    by_id = {}
    aliases = {}
    for report in reports:
        if not isinstance(report, dict):
            errors.append('Report must be an object')
            continue
        digest = report.get('sha256', '')
        if not isinstance(digest, str) or not re.fullmatch(r'[a-f0-9]{64}', digest):
            errors.append('Report requires SHA256 hex digest')
            continue
        if digest in by_hash:
            errors.append(f'Duplicate report hash: {digest}')
        by_hash[digest] = report
        paths = report.get('aliases', [])
        links = report.get('findings', [])
        if not isinstance(paths, list) or not paths or not all(isinstance(p, str) and Path(p).is_absolute() for p in paths):
            errors.append(f'Report {digest}: aliases must be absolute source paths')
        else:
            for path in paths:
                if excluded(Path(path)):
                    errors.append(f'Private source alias prohibited: {path}')
                if path in aliases and aliases[path] != digest:
                    errors.append(f'Alias registered at multiple hashes: {path}')
                aliases[path] = digest
        if not isinstance(links, list) or not all(isinstance(i, str) for i in links):
            errors.append(f'Report {digest}: findings must be a list of IDs')
        elif not links and not isinstance(report.get('decision'), str):
            errors.append(f'Report {digest}: explicit no-new-learning decision required')
        elif not links and not report.get('decision', '').strip():
            errors.append(f'Report {digest}: empty no-new-learning decision')
        if not isinstance(report.get('reviewed_on'), str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', report['reviewed_on']):
            errors.append(f'Report {digest}: reviewed_on date required')
    text_fields = ['id', 'reference', 'status', 'applicability', 'confidence', 'remedy',
                   'verification', 'verification_scope', 'limitations']
    for finding in findings:
        if not isinstance(finding, dict):
            errors.append('Finding must be an object')
            continue
        identity = finding.get('id', '<missing>')
        if not isinstance(identity, str):
            errors.append('Finding ID must be a string')
            continue
        if identity in by_id:
            errors.append(f'Duplicate finding ID: {identity}')
        by_id[identity] = finding
        if any(not isinstance(finding.get(key), str) or not finding[key].strip() for key in text_fields):
            errors.append(f'Finding {identity}: nonempty evidence, applicability and reference fields required')
            continue
        for key in ['symptoms', 'diagnostics', 'sources']:
            if not isinstance(finding.get(key), list) or not finding[key] or not all(isinstance(s, str) and s.strip() for s in finding[key]):
                errors.append(f'Finding {identity}: nonempty {key} list required')
        status = finding['status']
        scope = finding['verification_scope']
        confidence = finding['confidence']
        if status not in STATUSES or scope not in SCOPES or confidence not in {'confirmed', 'supported', 'hypothesis'}:
            errors.append(f'Finding {identity}: invalid status, confidence or verification_scope')
        if status == 'verified_fix' and (confidence == 'hypothesis' or scope not in {'code', 'runtime'}):
            errors.append(f'Finding {identity}: verified fix requires supported/confirmed cause and code/runtime evidence')
        if status == 'verified_workaround' and (confidence == 'hypothesis' or scope == 'none'):
            errors.append(f'Finding {identity}: workaround requires observed evidence')
        if status == 'activation_pending' and scope not in {'code', 'none'}:
            errors.append(f'Finding {identity}: pending activation cannot assert live runtime verification')
        reference, marker, anchor = finding['reference'].partition('#')
        target = knowledge / reference
        if (not marker or not anchor or not reference.startswith('references/')
                or '..' in Path(reference).parts or not target.is_file()
                or not target.resolve().is_relative_to(knowledge.resolve())):
            errors.append(f'Finding {identity}: invalid or missing reference {finding["reference"]}')
        else:
            try:
                content = target.read_text(encoding='utf-8')
                headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.M)
                anchors = {re.sub(r'[^\w -]', '', h.lower()).replace(' ', '-') for h in headings}
                if anchor not in anchors and f'id="{anchor}"' not in content:
                    errors.append(f'Finding {identity}: missing reference anchor {anchor}')
            except (OSError, UnicodeError) as error:
                errors.append(f'Finding {identity}: unreadable reference: {error}')
    for digest, report in by_hash.items():
        for identity in report.get('findings', []) if isinstance(report.get('findings'), list) else []:
            linked = by_id.get(identity, {}).get('sources') if isinstance(identity, str) else None
            if not isinstance(linked, list) or digest not in linked:
                errors.append(f'Report {digest}: missing reciprocal finding link {identity}')
    for identity, finding in by_id.items():
        for digest in finding.get('sources', []) if isinstance(finding.get('sources'), list) else []:
            linked = by_hash.get(digest, {}).get('findings') if isinstance(digest, str) else None
            if not isinstance(linked, list) or identity not in linked:
                errors.append(f'Finding {identity}: missing reciprocal source link {digest}')
    if errors:
        raise ValueError('\n'.join(errors))
    return ledger


def coverage(data, ledger, roots=None):
    reviewed = {r['sha256']: r for r in ledger['reports']}
    aliases = {a: r['sha256'] for r in ledger['reports'] for a in r['aliases']}
    new, changed, unregistered = [], [], []
    for report in data['documents']:
        for path in report['aliases']:
            if path in aliases and aliases[path] != report['sha256']:
                changed.append(path)
            elif report['sha256'] not in reviewed:
                new.append(path)
            elif path not in aliases:
                unregistered.append(path)
    data.update(new=sorted(new), changed=sorted(changed),
                unregistered_aliases=sorted(unregistered))
    observed = {a for r in data['documents'] for a in r['aliases']}
    selected = [Path(os.path.abspath(r)) for r in roots or []]
    data['missing_sources'] = sorted(a for a in aliases if a not in observed and
                                     any(Path(a).is_relative_to(root) for root in selected))
    return data


def search(query, ledger):
    tokens = set(re.findall(r'[a-z0-9]+', query.lower())) - {'a', 'an', 'the', 'and', 'or', 'to', 'of', 'in', 'is'}
    matches = []
    reports = {r['sha256']: r for r in ledger['reports']}
    for finding in ledger['findings']:
        haystack = ' '.join(str(finding[k]) for k in ['id', 'symptoms', 'applicability', 'diagnostics', 'remedy', 'limitations']).lower()
        words = set(re.findall(r'[a-z0-9]+', haystack))
        score = len(tokens & words)
        if not score:
            continue
        score += 3 if query.lower() in haystack else 0
        match = {k: finding[k] for k in ['id', 'reference', 'status', 'applicability', 'confidence', 'remedy', 'verification', 'verification_scope', 'limitations']}
        match['sources'] = [{'sha256': h, 'aliases': reports[h]['aliases']} for h in finding['sources']]
        match['score'] = score
        matches.append(match)
    matches.sort(key=lambda hit: (-hit['score'], hit['id']))
    return {'query': query, 'matches': matches[:20],
            'next_step': 'Read matching reference and source evidence before remediation.' if matches else
                         'No matching learning. Broaden symptom terms, then reproduce and diagnose; record the new postmortem and review decision.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ['scan', 'search', 'check']:
        child = sub.add_parser(command)
        child.add_argument('--knowledge', type=Path, help='Explicit knowledge directory (fixtures or alternate checkout)')
        if command == 'search':
            child.add_argument('query')
        else:
            child.add_argument('--root', action='append', type=Path, help='Repeatable scan roots; defaults to coding and linux-config')
        if command == 'check':
            child.add_argument('--postmortem', type=Path, help='Check only this report, plus all ledger/reference contracts')
    args = parser.parse_args(argv)
    knowledge = args.knowledge or (TRACKED if (TRACKED / 'SKILL.md').is_file() else Path(__file__).resolve().parents[1])
    try:
        ledger = load_ledger(knowledge)
        if args.command == 'search':
            data = search(args.query, ledger)
        else:
            if args.command == 'check' and args.postmortem:
                path = Path(os.path.abspath(args.postmortem))
                try:
                    digest = read_report(path)
                    data = {'documents': [{'sha256': digest, 'aliases': [str(path)]}],
                            'unique_reports': 1, 'document_count': 1, 'errors': [], 'excluded': []}
                except (OSError, ValueError) as error:
                    data = {'documents': [], 'unique_reports': 0, 'document_count': 0, 'errors': [str(error)], 'excluded': []}
            else:
                data = discover(args.root or DEFAULT_ROOTS)
            coverage(data, ledger, None if args.command == 'check' and args.postmortem else args.root or DEFAULT_ROOTS)
            if args.command == 'check':
                for kind in ['new', 'changed', 'unregistered_aliases', 'missing_sources']:
                    data['errors'].extend(f'{kind}: {path}' for path in data[kind])
                data['finding_count'] = len(ledger['findings'])
        data['knowledge'] = str(knowledge)
        print(json.dumps(data, indent=2, sort_keys=True))
        return 1 if data.get('errors') else 0
    except (ValueError, OSError, TypeError, KeyError) as error:
        print(json.dumps({'errors': str(error).splitlines(), 'knowledge': str(knowledge)}, indent=2))
        return 2


if __name__ == '__main__':
    sys.exit(main())
