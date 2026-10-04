#!/usr/bin/env python3
"""Derive request-level costs from frozen pilot evidence; never invokes models."""
from collections import Counter
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / 'benchmarks/metaprompt'
RUN = ROOT / 'runs/pilot-2026-10-03'


def stage_metrics(stage: dict | None) -> dict:
    result = dict(episodes=0, requests=0, measured_requests=0,
                  requests_with_unknown_usage=0, input_tokens=0,
                  cached_input_tokens=0, output_tokens=0,
                  reasoning_output_tokens=0, latency_seconds=0.0)
    if not stage:
        return result
    result.update(episodes=1, requests=stage['call_count'],
                  latency_seconds=stage['latency_seconds'])
    # Clarification requests are already flattened by the frozen runner.
    # CLI turn totals are absent on episode-limit failures; per-request usage
    # still records the inference that actually occurred.
    for request in stage.get('requests', []):
        usage = request.get('usage')
        if not usage:
            continue
        result['measured_requests'] += 1
        result['input_tokens'] += usage['input_tokens']
        result['output_tokens'] += usage['output_tokens']
        result['cached_input_tokens'] += usage.get('input_tokens_details', {}).get('cached_tokens', 0)
        result['reasoning_output_tokens'] += usage.get('output_tokens_details', {}).get('reasoning_tokens', 0)
    result['requests_with_unknown_usage'] = result['requests'] - result['measured_requests']
    return result


def sum_stages(stages: list[dict | None]) -> dict:
    total = Counter(stage_metrics(None))
    for stage in stages:
        total.update(stage_metrics(stage))
    return dict(total)


def analyze(results: dict, budget: dict) -> dict:
    rows = results['trials']
    archive = results['archived_failed_attempts']
    all_rows = rows + archive
    total = sum_stages([r.get(s) for r in all_rows for s in ('compiler', 'solver')])
    setup = sum(r['label'].startswith('setup:') for r in budget['requests'])
    if total['requests'] + setup != budget['reserved']:
        raise ValueError('Saved stage requests plus setup do not reconcile with the quota ledger')
    candidates = {}
    for name in sorted({r['candidate'] for r in rows if r['split'] == 'holdout'}):
        own = [r for r in rows if r['split'] == 'holdout' and r['candidate'] == name]
        solvers = [r['solver'] for r in own if r.get('solver')]
        candidates[name] = {
            'scheduled_pairs': len(own),
            'statuses': dict(Counter(r['status'] for r in own)),
            'successes': sum(r['success'] is True for r in own),
            'first_use_attempt_totals': sum_stages([r.get(s) for r in own for s in ('compiler', 'solver')]),
            'compiler_totals': sum_stages([r.get('compiler') for r in own]),
            'observed_solver_component_totals': sum_stages(solvers),
            'clarification_turns': sum(r.get('clarification_turns', 0) for r in own),
            'loaded_reference_reads': sum(len((r.get('compiler') or {}).get('loaded_references', [])) for r in own),
            'observed_tool_boundary_violations': sum(len((r.get(s) or {}).get('hard_failures', [])) for r in own for s in ('compiler', 'solver')),
            'per_case': [{
                'case_id':r['case_id'], 'status':r['status'], 'success':r['success'],
                'compiler':stage_metrics(r.get('compiler')) if r.get('compiler') else None,
                'solver':stage_metrics(r.get('solver')) if r.get('solver') else None,
            } for r in own],
        }
    models = sorted({q['served_model'] for r in all_rows for s in ('compiler','solver')
                     for q in (r.get(s) or {}).get('requests',[]) if q.get('served_model')})
    return {
        'schema_version':1, 'usage_source':'Recorded per-request response metadata, including aborted episodes',
        'reserved_requests':budget['reserved'], 'cap':budget['cap'],
        'setup_requests_with_unknown_usage':setup,
        'all_stage_totals_including_archived_attempts':total,
        'served_models':models, 'candidates':candidates,
        'grading_model_calls':0, 'preparation_model_usage':None, 'actual_usd_cost':None,
        'measured_grading_latency_seconds':results['measured_grading_latency_seconds'],
        'reuse_caveat':'Solver component only; repeated reuse/cache behavior was not executed. Aborted costs are not costs per successful completion.',
    }


def main() -> None:
    sys.path.insert(0, str(ROOT))
    from benchlib import digest, save_json, verify_freeze
    verify_freeze(RUN/'protocol.json')
    results = json.loads((RUN/'results.json').read_text())
    budget = json.loads((RUN/'budget.json').read_text())
    result = analyze(results, budget)
    result['frozen_protocol_sha256'] = digest(RUN/'protocol.json')
    result['results_sha256'] = digest(RUN/'results.json')
    result['analysis_script_sha256'] = digest(Path(__file__))
    save_json(RUN/'analysis.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
