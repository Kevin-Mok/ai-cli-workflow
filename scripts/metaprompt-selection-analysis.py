#!/usr/bin/env python3
"""Offline derived selection statistics; never invoke models or inspect prompt text."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random

WORKFLOWS = ('create', 'sharpen', 'template', 'coding')
INVALID = {'pending', 'interrupted', 'infrastructure_error', 'quota_truncated'}
METRICS = ('input_tokens', 'output_tokens', 'cached_input_tokens', 'reasoning_tokens')
RANKING = 'Equal workflow success; exclude serious authorization failures; exact ties: latest substantive maintenance, mean first-use input tokens, stars'


def usage(rows, names):
    known = Counter(); unknown = Counter(); observed = calls = 0; latency = 0.0
    for row in rows:
        for name in names:
            stage = row.get(name) or {}
            evidence = stage.get('requests', [])
            count = stage.get('call_count', 0)
            calls += count; observed += len(evidence)
            latency += stage.get('latency_seconds', 0)
            for metric in METRICS:
                unknown[metric] += max(0, count - len(evidence))
            for request in evidence:
                value = request.get('usage') or {}
                fields = {'input_tokens': value.get('input_tokens'),
                          'output_tokens': value.get('output_tokens'),
                          'cached_input_tokens': (value.get('input_tokens_details') or {}).get('cached_tokens'),
                          'reasoning_tokens': (value.get('output_tokens_details') or {}).get('reasoning_tokens')}
                for metric, amount in fields.items():
                    if type(amount) is int and amount >= 0:
                        known[metric] += amount
                    else:
                        unknown[metric] += 1
    result = {'calls': calls, 'requests_observed': observed, 'latency_seconds': latency,
              'latency_basis': 'stage wall time, including aborted stages and nested evaluation waits; stages summed, not parallel run wall time',
              'unknown_usage_requests': dict(unknown)}
    for metric in METRICS:
        result['known_' + metric] = known[metric]
        result[metric] = None if unknown[metric] else known[metric]
    return result


def failures(row):
    result = set()
    if row.get('success') is True:
        return result
    if row.get('status') != 'completed':
        result.add('status:' + str(row.get('status')))
    for name in ('score', 'fixture_score'):
        score = row.get(name) or {}
        if score.get('success') is False:
            result.add(name + ':failed')
            for check in score.get('checks', []):
                if check in ('exact_json_match', 'json_mismatch'):
                    category = check
                elif str(check).startswith('Invalid Python:'):
                    category = 'invalid_python'
                elif check == 'Fixture execution timed out':
                    category = 'execution_timeout'
                elif check == 'Code-only contract forbids Markdown fences':
                    category = 'markdown_fence'
                elif check == 'Code exceeds pure-function fixture execution boundary':
                    category = 'unsafe_code_boundary'
                else:
                    category = 'assertion_or_execution_failure'
                result.add(name + ':' + category)
    for check, passed in (row.get('coding_actions') or {}).get('checks', {}).items():
        if passed is False:
            result.add('coding_action:' + check)
    if row.get('extraction') and not row['extraction'].get('prompt'):
        result.add('extraction:no_final_prompt')
    for failure in row.get('hard_failures', []):
        result.add('hard:' + failure)
    return result or {'unspecified_recorded_failure'}


def paired(rows, arm, control, seed=20261003, samples=4000):
    left = {r['case_id']: r for r in rows if r['candidate'] == arm}
    right = {r['case_id']: r for r in rows if r['candidate'] == control}
    strata = {w: [] for w in WORKFLOWS}
    for case in sorted(left.keys() & right.keys()):
        a, b = left[case], right[case]
        if a['workflow'] == b['workflow']:
            strata[a['workflow']].append(int(a.get('success') is True) - int(b.get('success') is True))
    if not all(strata.values()):
        return {'matched_cases': sum(map(len, strata.values())), 'difference': None, 'interval95': None}
    mean = lambda values: sum(values) / len(values)
    estimate = sum(mean(x) for x in strata.values()) / 4
    rng = random.Random(seed)
    draws = sorted(sum(mean(rng.choices(x, k=len(x))) for x in strata.values()) / 4 for _ in range(samples))
    return {'matched_cases': sum(map(len, strata.values())), 'matched_by_workflow': {w: len(x) for w, x in strata.items()},
            'difference': estimate, 'interval95': [draws[int(samples*.025)], draws[int(samples*.975)-1]],
            'seed': seed, 'bootstrap_samples': samples, 'method': 'paired case resampling within each workflow, equal workflow weighting',
            'warning': 'Exploratory percentile intervals; tiny selected synthetic sample and multiple comparisons, no universal superiority claim.'}


def omission_sensitivity(rows, excluded_case_ids):
    """Describe an explicit post-hoc omission without rescoring or ranking arms."""
    kept = [r for r in rows if r['case_id'] not in excluded_case_ids]
    arms = {}
    for arm in sorted({r['candidate'] for r in rows}):
        group = [r for r in kept if r['candidate'] == arm]
        workflows = {}
        for workflow in WORKFLOWS:
            own = [r for r in group if r['workflow'] == workflow]
            workflows[workflow] = {'attempts': len(own),
                                   'successes': sum(r.get('success') is True for r in own)}
        weighted = (sum(v['successes'] / v['attempts'] for v in workflows.values()) / 4
                    if all(v['attempts'] for v in workflows.values()) else None)
        arms[arm] = {'attempts': len(group),
                     'successes': sum(r.get('success') is True for r in group),
                     'workflows': workflows, 'weighted_success': weighted}
    comparisons = {a + '_vs_' + c: paired(kept, a, c)
                   for a in arms if a not in ('raw', 'minimal')
                   for c in ('raw', 'minimal') if c in arms}
    return {'post_hoc': True, 'excluded_case_ids': list(excluded_case_ids),
            'changes_primary_scores': False, 'additional_inference_requests': 0,
            'weighting': 'Each workflow remains 25%; remaining cases are equal within workflow.',
            'cost_accounting': 'All original attempts and requests remain charged; costs are not reduced.',
            'arms': arms, 'paired': comparisons}


def analyze(schedule, rows, request_ledger, trial_ledger, sources):
    expected = {r['id']: r for r in schedule if r['split'] == 'holdout'}
    held = [r for r in rows if r.get('split') == 'holdout']
    errors = []; ids = [r['id'] for r in held]
    if len(ids) != len(set(ids)): errors.append('duplicate heldout IDs')
    if set(ids) != set(expected): errors.append('missing or unexpected heldout IDs')
    for row in held:
        original = expected.get(row['id'])
        if original and any(row.get(k) != original.get(k) for k in ('candidate','case_id','workflow','split')):
            errors.append('heldout metadata mismatch: ' + row['id'])
    reservations = request_ledger.get('requests', [])
    trials = trial_ledger.get('trials', [])
    labels = Counter(r['label'] for r in reservations)
    if len(reservations) > 2000 or request_ledger.get('cap') != 2000: errors.append('global request cap invalid')
    if request_ledger.get('reserved', len(reservations)) != len(reservations): errors.append('request reservation count mismatch')
    if any(n > 10 for n in labels.values()): errors.append('per-stage request cap exceeded')
    if len(trials) > 100: errors.append('trial cap exceeded')
    reserved_ids = [r['id'] for r in trials]
    if len(set(reserved_ids)) != len(reserved_ids): errors.append('duplicate trial reservations')
    if any(r['id'] not in reserved_ids for r in rows): errors.append('record without trial reservation')
    if len({r['id'] for r in rows}) != len(rows): errors.append('duplicate record IDs')
    if any(r['id'] not in {s['id'] for s in schedule} for r in rows): errors.append('unexpected record IDs')
    for row in rows:
        for name in ('compiler','solver'):
            stage = row.get(name) or {}; count = stage.get('call_count',0)
            if count != len(stage.get('requests', [])): errors.append('request evidence count mismatch: '+row['id']+':'+name)
            if count != labels.get(row['id']+':'+name,0): errors.append('request ledger mismatch: '+row['id']+':'+name)
    seen_labels = {r['id']+':'+name for r in rows for name in ('compiler','solver')}
    orphaned = {label:n for label,n in labels.items() if label not in seen_labels}
    if orphaned: errors.append('reserved requests without trial evidence')
    arms = {}
    for arm in sorted({r['candidate'] for r in expected.values()}):
        group = [r for r in held if r['candidate']==arm]
        workflows = {w: {'attempts':sum(r['workflow']==w for r in group),
                         'successes':sum(r['workflow']==w and r.get('success') is True for r in group)} for w in WORKFLOWS}
        balanced = all(v['attempts'] for v in workflows.values()) and len({v['attempts'] for v in workflows.values()})==1
        if not balanced: errors.append('unequal or missing workflow rows: '+arm)
        objective = Counter(f for r in group for f in failures(r))
        first = usage(group,('compiler','solver'))
        hard = [f for r in group for f in r.get('hard_failures',[])]
        arms[arm] = {'workflows':workflows,'attempts':len(group),'successes':sum(r.get('success') is True for r in group),
                     'weighted_success':sum(v['successes']/v['attempts'] for v in workflows.values())/4 if balanced else None,
                     'statuses':dict(Counter(r['status'] for r in group)), 'failures':dict(objective),
                     'final_deliverables':sum(r.get('native_deliverable_completed') is True for r in group),
                     'native_observed_complete':sum((r.get('native_workflow') or {}).get('complete') is True for r in group),
                     'native_observation_attempts':sum('native_workflow' in r for r in group),
                     'compiler':usage(group,('compiler',)), 'solver_only':usage(group,('solver',)), 'first_use':first,
                     'mean_first_use_input_tokens':first['input_tokens']/len(group) if group and first['input_tokens'] is not None else None,
                     'hard_failures':hard}
    complete = not errors and not any(r['status'] in INVALID for r in held)
    eligible = [a for a in arms if a in sources and complete and not arms[a]['hard_failures']]
    def ranking(a):
        mean = arms[a]['mean_first_use_input_tokens']
        return (arms[a]['weighted_success'],sources[a].get('latest_substantive_change',''),
                -mean if mean is not None else float('-inf'),sources[a].get('stars',0))
    chosen = max(eligible,key=ranking) if eligible else None
    comparisons = {a+'_vs_'+control:paired(held,a,control) for a in arms if a not in ('raw','minimal') for control in ('raw','minimal') if control in arms}
    sensitivities = {}
    if any(r['case_id'] == 'selection-template-draft' for r in held):
        diagnostic = omission_sensitivity(held, ['selection-template-draft'])
        diagnostic['reason'] = ('The rendered raw template appends its instructions to the final '
                                'Fact line of a multiline binding despite a line-exact copy rule. '
                                'Omit this ambiguous case equally; do not infer a correct answer.')
        sensitivities['omit_ambiguous_draft_binding'] = diagnostic
    return {'schema_version':1,'complete_balanced_holdout':complete,'integrity_errors':sorted(set(errors)),
            'expected_holdout_trials':len(expected),'observed_holdout_trials':len(held), 'arms':arms,'paired':comparisons,
            'ranking_rule':RANKING,'recommended_skill':chosen,'sensitivities':sensitivities,
            'skill_improves_on_controls':bool(chosen and all(arms[c]['weighted_success'] is not None and arms[chosen]['weighted_success']>arms[c]['weighted_success'] for c in ('raw','minimal') if c in arms)),
            'all_recorded_attempts': {'count':len(rows),'compiler':usage(rows,('compiler',)), 'solver_only':usage(rows,('solver',)), 'first_use':usage(rows,('compiler','solver'))},
            'requests_reserved':len(reservations),'trials_reserved':len(trials),'orphaned_request_labels':orphaned,
            'dollar_cost':None,'reuse_scope':'Solver-only totals measure observed downstream stages; repeated reuse savings were not experimentally measured.',
            'failure_categories':'Nonexclusive labels from recorded statuses, scorer checks, extraction and coding actions; no semantic model judging.'}


def load(path):
    return json.loads(path.read_text())


def verify_protocol(run):
    protocol = load(run/'protocol.json')
    if protocol.get('schema_version') != 1: raise ValueError('Unsupported frozen protocol')
    for rel, expected in protocol['files'].items():
        path = run/rel
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen input changed: '+rel)
    if protocol['settings']['ranking'] != RANKING: raise ValueError('Unknown frozen ranking rule')
    return protocol


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',required=True,type=Path)
    args=parser.parse_args(); run=args.run.resolve(); protocol=verify_protocol(run)
    source_paths=[run/rel for rel in protocol['files'] if Path(rel).name=='sources.json']
    if len(source_paths)!=1: raise ValueError('Expected one frozen sources manifest')
    sources={s['id']:s for s in load(source_paths[0])['candidates']}
    rows=[load(p) for p in sorted((run/'trials').glob('*.json'))]
    value=analyze(protocol['settings']['schedule'],rows,load(run/'requests.json'),load(run/'trial-ledger.json'),sources)
    value.update(protocol_sha256=hashlib.sha256((run/'protocol.json').read_bytes()).hexdigest(),
                 frozen_files_verified=len(protocol['files']), analyzer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    value['evidence_sha256'] = {str(p.relative_to(run)): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in [run/'requests.json', run/'trial-ledger.json', *sorted((run/'trials').glob('*.json'))]}
    # The only derived artifact is under the explicitly selected run.
    temp=run/'analysis.json.tmp'; temp.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n');temp.replace(run/'analysis.json')
    print(json.dumps({k:value[k] for k in ('complete_balanced_holdout','integrity_errors','recommended_skill','requests_reserved','trials_reserved','protocol_sha256')}))

if __name__=='__main__': main()
