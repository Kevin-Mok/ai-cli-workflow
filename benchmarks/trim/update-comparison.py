#!/usr/bin/env python3
"""Regenerate committed trim comparisons; optionally show the uncommitted draft."""

import argparse
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[2]
START = '3e898a0f39172d7c30a6b0ae0258209cfe2c7f0c'
BENCHMARK = runpy.run_path(str(ROOT / 'scripts/trim-benchmark'))
EVIDENCE = 'benchmarks/trim/pass-evidence.json'


def number(value):
    return f'{value:,.2f}'.rstrip('0').rstrip('.') if isinstance(value, float) else f'{value:,}'


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def evidence_fields(data, subject=None):
    if not isinstance(data, dict) or (subject is not None and data.get('commit_subject') != subject):
        data = {}
    result = {'pass': data.get('pass', subject or 'unavailable'),
              'technique': data.get('technique', 'unavailable'),
              'tests': 'unavailable', 'trigger': 'unavailable',
              'command': 'unavailable', 'routing_scope': 'unavailable'}
    tests = data.get('tests', {})
    trigger = data.get('trigger', {})
    if (isinstance(tests, dict) and type(tests.get('passed')) is int and tests['passed'] >= 0
            and isinstance(tests.get('command'), str) and tests['command'].strip()):
        result.update(tests=str(tests['passed']), command=tests['command'])
    if (isinstance(trigger, dict) and type(trigger.get('case_count')) is int
            and type(trigger.get('exact_matches')) is int
            and 0 <= trigger['exact_matches'] <= trigger['case_count'] and trigger['case_count'] > 0
            and all(isinstance(trigger.get(k), str) and trigger[k].strip() for k in ('method', 'scope'))):
        result['trigger'] = f"{trigger['exact_matches']}/{trigger['case_count']} ({trigger['exact_matches'] / trigger['case_count']:.2%})"
        result['routing_scope'] = trigger['method'] + '; ' + trigger['scope']
    return result


def load_evidence(root, ref=None, subject=None):
    if ref is None:
        path = root / EVIDENCE
        data = json.loads(path.read_text()) if path.exists() else {}
    else:
        exists = BENCHMARK['git'](root, 'ls-tree', '--name-only', ref, '--', EVIDENCE).strip()
        data = json.loads(BENCHMARK['git'](root, 'show', ref + ':' + EVIDENCE)) if exists else {}
    return evidence_fields(data, subject)


def metrics(report):
    values = {}
    for path in ('AGENTS.md', 'dot_codex/AGENTS.md'):
        for key in ('lines', 'bytes', 'approx_tokens'):
            values[path + ' ' + key] = report['instructions'][path][key]
    values.update({'Developer-instruction tokens': report['developer_instructions']['approx_tokens'],
                   'Skill-description tokens': report['totals']['description_bytes'] / 4,
                   'SKILL.md body bytes': report['totals']['body_bytes'],
                   'Canonical skill count': report['totals']['skills_count'],
                   'Always-loaded tokens/session': report['totals']['loaded_approx_tokens']})
    return values


def largest(report):
    return sorted(((path, value['body']['bytes']) for path, value in report['skills'].items()
                   if path.startswith('dot_agents/')), key=lambda item: (-item[1], item[0]))[:10]


def render(root, start=START, head='HEAD', include_working=False, progress=None):
    git = BENCHMARK['git']
    start = BENCHMARK['commit_ref'](root, start)
    head = BENCHMARK['commit_ref'](root, head)
    git(root, 'merge-base', '--is-ancestor', start, head)
    commits = [line.split('\t', 1) for line in git(root, 'log', '--reverse', '--format=%H%x09%s', start + '..' + head).splitlines()]
    reports = {}
    for index, sha in enumerate(dict.fromkeys([start, *[sha for sha, _ in commits], head]), 1):
        if progress:
            progress(index, sha)
        reports[sha] = BENCHMARK['collect'](root, sha)
    old, new = reports[start], reports[head]
    old_tokens, new_tokens = old['totals']['loaded_approx_tokens'], new['totals']['loaded_approx_tokens']
    old_evidence, new_evidence = load_evidence(root, start, git(root, 'show', '-s', '--format=%s', start).strip()), load_evidence(root, head, git(root, 'show', '-s', '--format=%s', head).strip())
    delta = new_tokens - old_tokens
    lines = ['# Trim comparison', '',
             'Reproduce instruction costs from committed Git blobs, compare the original with HEAD,',
             'then inspect real pass commits and their recorded verification. An optional working',
             'draft is reported separately and never counts as a committed pass.', '',
             f'Always-loaded tokens per session: **{number(old_tokens)} → {number(new_tokens)}**',
             f'({delta:+,.2f} tokens, {delta / old_tokens:+.2%}).', '',
             f'Original: `{start}`. HEAD: `{head}`.', '',
             'Estimates use UTF-8 bytes / 4, not model tokenizer usage. The headline includes',
             'root AGENTS.md + canonical dot_codex/AGENTS.md + config developer_instructions +',
             'canonical dot_agents skill descriptions. Skill bodies are on-demand. Skill names,',
             'paths, runtime wrappers, external installs and the duplicate .agents catalog are',
             'excluded from the headline. External install changes require separate evidence.', '',
             '## Original versus HEAD', '', '| Metric | Original | HEAD | Change |', '| --- | ---: | ---: | ---: |']
    for key, value in metrics(old).items():
        current = metrics(new)[key]
        lines.append(f'| {key} | {number(value)} | {number(current)} | {current - value:+,.2f} |')
    for label, key in (('Trigger exact-set accuracy', 'trigger'), ('Automated tests passed', 'tests')):
        lines.append(f'| {label} | {old_evidence[key]} | {new_evidence[key]} | unavailable |')
    lines += ['', 'Trigger and test counts are unavailable without matching committed evidence.',
              'Routing scores from different corpora are not comparable; lexical proxy scores',
              'do not establish actual model routing. Test counts cover only their recorded command.', '',
              '## Pass commits', '',
              'Every row comes from `git log --reverse ORIGINAL..HEAD`; no draft, planned pass',
              'or inferred test result is promoted to a commit. L/B/T means lines/bytes/tokens.',
              'The two delta columns measure always-loaded tokens.', '',
              '| Commit | Pass | Technique | Root AGENTS L/B/T | Canonical AGENTS L/B/T | Developer T | Description T | Body B | Skills | Largest body B | Trigger | Tests | Loaded T | Δ previous | Δ original |',
              '| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |']
    previous = old
    savings = {}
    provenance = []
    for sha, subject in commits:
        report = reports[sha]
        evidence = load_evidence(root, sha, subject)
        tokens = report['totals']['loaded_approx_tokens']
        diff = tokens - previous['totals']['loaded_approx_tokens']
        instruction = ['/'.join(number(report['instructions'][path][k]) for k in ('lines', 'bytes', 'approx_tokens'))
                       for path in ('AGENTS.md', 'dot_codex/AGENTS.md')]
        biggest = largest(report)[0] if largest(report) else ('none', 0)
        row = [sha[:7], evidence['pass'], evidence['technique'], *instruction,
               number(report['developer_instructions']['approx_tokens']), number(report['totals']['description_bytes'] / 4),
               number(report['totals']['body_bytes']), report['totals']['skills_count'], f'{biggest[0]}: {number(biggest[1])}',
               evidence['trigger'], evidence['tests'], number(tokens), f'{diff:+,.2f}', f'{tokens - old_tokens:+,.2f}']
        lines.append('| ' + ' | '.join(cell(value) for value in row) + ' |')
        technique = evidence['technique'] if evidence['technique'] != 'unavailable' else subject + ' (technique unavailable)'
        savings[technique] = savings.get(technique, 0) - diff
        provenance.append((sha[:7], evidence))
        previous = report
    if not commits:
        lines += ['', 'No pass commits exist in the requested range.']
    lines += ['', '## Always-loaded cost by commit', '', '```text']
    chart = [('Original', old_tokens), *[(sha[:7], reports[sha]['totals']['loaded_approx_tokens']) for sha, _ in commits]]
    maximum = max(value for _, value in chart) or 1
    for label, value in chart:
        lines.append(f'{label:10} {"#" * round(value / maximum * 40):40} {number(value)} tokens')
    lines += ['```', '', '## Largest canonical skill bodies', '',
              '| Rank | Original skill | Body bytes | HEAD skill | Body bytes |', '| ---: | --- | ---: | --- | ---: |']
    old_largest, new_largest = largest(old), largest(new)
    for index in range(max(len(old_largest), len(new_largest))):
        before = old_largest[index] if index < len(old_largest) else ('none', 0)
        after = new_largest[index] if index < len(new_largest) else ('none', 0)
        lines.append(f'| {index + 1} | {before[0]} | {number(before[1])} | {after[0]} | {number(after[1])} |')
    lines += ['', '## What moved the needle', '']
    if savings:
        lines += ['| Rank | Technique | Net loaded tokens saved |', '| ---: | --- | ---: |']
        for index, (technique, saved) in enumerate(sorted(savings.items(), key=lambda item: (-item[1], item[0])), 1):
            lines.append(f'| {index} | {cell(technique)} | {saved:+,.2f} |')
    else:
        lines += ['No committed technique savings yet. Uncommitted reductions cannot establish a completed pass.']
    lines += ['', '## Verification provenance', '',
              'Optional `benchmarks/trim/pass-evidence.json` records `pass`, `technique`,',
              '`commit_subject`, `tests: {passed, command}`, and',
              '`trigger: {exact_matches, case_count, method, scope}`. The subject must match',
              'the commit; absent, stale or invalid counts are unavailable. Store only safe',
              'aggregate evidence here, never raw session logs or private data.', '',
              '| Commit | Trigger method and corpus | Automated command |', '| --- | --- | --- |']
    for sha, evidence in provenance or [(head[:7], new_evidence)]:
        lines.append(f'| {sha} | {cell(evidence["routing_scope"])} | {cell(evidence["command"])} |')
    if include_working:
        working = BENCHMARK['collect'](root)
        evidence = load_evidence(root)
        lines += ['', '## Uncommitted working draft', '',
                  'Excluded from committed pass rows and savings ranking. These measurements',
                  'come from current files and may change during parallel edits; they do not',
                  'prove that pass commits, privacy gates or required checks have completed.', '',
                  '| Metric | Working draft | Change versus original |', '| --- | ---: | ---: |']
        for key, value in metrics(working).items():
            lines.append(f'| {key} | {number(value)} | {value - metrics(old)[key]:+,.2f} |')
        lines += [f'| Trigger exact-set accuracy | {evidence["trigger"]} | corpus-dependent |',
                  f'| Automated tests passed | {evidence["tests"]} | unavailable |', '',
                  f'Trigger scope: {cell(evidence["routing_scope"])}.',
                  f'Automated command: {cell(evidence["command"])}.']
    lines += ['', '## Regeneration', '',
              'From the repository root, run `python3 benchmarks/trim/update-comparison.py`',
              'after inspecting actual commits. Add `--include-working` only to show a',
              'separately labeled draft. `scripts/trim-benchmark --ref REF --json` exposes',
              'the full inventory for any commit; `--ref` skips current working-tree budgets',
              'and cannot be combined with `--check`. The original immutable BASELINE.json',
              'supplies comparisons and is never rewritten.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--start', default=START)
    parser.add_argument('--head', default='HEAD')
    parser.add_argument('--include-working', action='store_true')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--plain', action='store_true')
    args = parser.parse_args()
    try:
        root = args.repo.resolve()
        def progress(index, sha):
            print(('' if args.plain else '📊 ') + f'Measuring committed snapshot {index}: {sha[:7]}', file=sys.stderr, flush=True)
        document = render(root, args.start, args.head, args.include_working, progress)
        target = args.output or root / 'benchmarks/trim/COMPARISON.md'
        target.write_text(document)
        print(('' if args.plain else '✅ ') + f'Updated {target}')
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(('' if args.plain else '⚠️ ') + f'Comparison not generated: {error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
