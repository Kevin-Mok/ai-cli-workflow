"""Observable native workflow evidence, separate from downstream task success.

This checker never executes tools or models. Missing or malformed evidence is
unverified; it cannot be replaced by a claim in the author's report.
"""
import json
import math
import re

SECTIONS = ('Target', 'Success Criteria', 'External Context', 'Optimized Prompt',
            'Adapter Notes', 'Eval Set', 'Optimization Log', 'Residual Risks')


def _json(value):
    if isinstance(value, (dict, list)):
        return value
    if not isinstance(value, str):
        return None
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return None


def _artifact(artifacts, path):
    return artifacts.get(path) if isinstance(path, str) else None


def _trace(compiled):
    trace = compiled.get('tool_trace', [])
    return [event for event in trace if isinstance(event, dict)
            and event.get('status') == 'ok' and isinstance(event.get('arguments'), dict)] if isinstance(trace, list) else []


def _metric(value):
    if not isinstance(value, dict):
        return None
    clarity, tokens = value.get('clarity_score'), value.get('token_count')
    try:
        finite = all(type(number) in (int, float) and math.isfinite(number)
                     for number in (clarity, tokens))
    except OverflowError:
        finite = False
    if not finite or not 0 <= clarity <= 100 or tokens < 0:
        return None
    return {'clarity_score': clarity, 'token_count': tokens}


def _helper_metrics(event, artifacts):
    result = _json(event.get('result'))
    if not isinstance(result, dict) or type(result.get('exit_code')) is not int or result['exit_code'] != 0:
        return None
    path = event['arguments'].get('output_path')
    if isinstance(path, str) and path in artifacts:
        return _metric(_json(artifacts[path]))
    # Native --compare/--output adds prose around its JSON. Decode an actual
    # metrics object, not numbers scraped from the human-readable comparison.
    stdout = result.get('stdout', '')
    if not isinstance(stdout, str):
        return None
    decoder = json.JSONDecoder()
    for position, character in enumerate(stdout):
        if character == '{':
            try:
                value, _ = decoder.raw_decode(stdout[position:])
            except ValueError:
                continue
            metrics = _metric(value)
            if metrics is not None:
                return metrics
    return None


def _sections(output):
    if not isinstance(output, str):
        return {}
    found, current, fenced = {}, None, False
    names = '|'.join(map(re.escape, SECTIONS))
    pattern = re.compile(r'^\s*(?:#{1,6}\s*)?(?:\d+[.)]\s*)?(' + names + r')(?:\s*:\s*(.*)|\s*)$', re.I)
    for line in output.splitlines():
        if line.lstrip().startswith(('```', '~~~')):
            fenced = not fenced
            if current:
                found[current].append(line)
            continue
        match = pattern.fullmatch(line.replace('**', '')) if not fenced else None
        if match:
            current = next(name for name in SECTIONS if name.casefold() == match[1].casefold())
            found.setdefault(current, []).append(match[2] or '')
        elif current:
            found[current].append(line)
    return {name: '\n'.join(line for line in body if not line.lstrip().startswith(('```', '~~~'))).strip()
            for name, body in found.items()}


def _cases(event, artifacts):
    value = _json(_artifact(artifacts, event['arguments'].get('cases_path')))
    if not isinstance(value, list) or not 10 <= len(value) <= 20:
        return None
    by_id = {}
    for case in value:
        if (not isinstance(case, dict) or set(case) != {'id', 'input', 'expected'}
                or not isinstance(case['id'], str) or not case['id'] or case['id'] in by_id):
            return None
        by_id[case['id']] = case
    try:
        return json.dumps(by_id, sort_keys=True, ensure_ascii=False, allow_nan=False), set(by_id)
    except (TypeError, ValueError):
        return None


def _evaluations(trace, artifacts):
    values = []
    for position, event in enumerate(trace):
        if event.get('tool') != 'evaluate_prompt':
            continue
        result, cases = _json(event.get('result')), _cases(event, artifacts)
        if not isinstance(result, dict) or result.get('status') != 'completed' or cases is None:
            continue
        fingerprint, ids = cases
        results = result.get('case_results')
        if type(result.get('total')) is not int or result['total'] != len(ids) or not isinstance(results, list):
            continue
        passing, seen = set(), set()
        for item in results:
            if (not isinstance(item, dict) or not isinstance(item.get('id'), str)
                    or item['id'] in seen or type(item.get('success')) is not bool):
                break
            seen.add(item['id'])
            if item['success']:
                passing.add(item['id'])
        else:
            if seen == ids:
                values.append({'position': position, 'prompt_path': event['arguments'].get('prompt_path'),
                               'fingerprint': fingerprint, 'passing': passing, 'total': len(ids)})
    return values


def _senior(trace, artifacts, final_prompt, failures, checks):
    helpers = [(i, event) for i, event in enumerate(trace) if event.get('tool') == 'run_skill_check']
    comparisons = [(i, event) for i, event in helpers if event['arguments'].get('baseline_path')]
    if final_prompt is not None:
        comparisons = [(i, event) for i, event in comparisons
                       if _artifact(artifacts, event['arguments'].get('prompt_path')) == final_prompt]
        checks['final_prompt_static_analysis'] = bool(comparisons)
        if not comparisons:
            failures.append('final_prompt_static_analysis_not_observed')
    if not comparisons:
        failures.append('native_baseline_revision_pair_not_observed')
        return
    position, revised = comparisons[-1]
    baseline_path = revised['arguments'].get('baseline_path')
    earlier = [(i, event) for i, event in helpers if i < position
               and event['arguments'].get('output_path') == baseline_path
               and _helper_metrics(event, artifacts) is not None]
    baseline_metrics = _metric(_json(_artifact(artifacts, baseline_path)))
    revised_metrics = _helper_metrics(revised, artifacts)
    if not earlier or baseline_metrics is None or revised_metrics is None:
        failures.append('native_baseline_revision_metrics_unverified')
        return
    _, baseline = earlier[-1]
    checks['static_clarity_no_regression'] = revised_metrics['clarity_score'] >= baseline_metrics['clarity_score']
    checks['static_token_limit'] = revised_metrics['token_count'] <= baseline_metrics['token_count'] * 1.10
    if not checks['static_clarity_no_regression']:
        failures.append('static_clarity_regression')
    if not checks['static_token_limit']:
        failures.append('static_token_regression')
    evaluations = _evaluations(trace, artifacts)
    base_path, revision_path = baseline['arguments'].get('prompt_path'), revised['arguments'].get('prompt_path')
    pairs = [(b, r) for b in evaluations for r in evaluations
             if b['position'] < r['position'] and b['prompt_path'] == base_path
             and r['prompt_path'] == revision_path and b['fingerprint'] == r['fingerprint']]
    if not pairs:
        failures.append('same_case_public_eval_pair_not_observed')
        return
    baseline_eval, revision_eval = max(pairs, key=lambda pair: (pair[1]['position'], pair[0]['position']))
    checks['public_eval_case_count'] = revision_eval['total']
    checks['baseline_passing_cases'] = len(baseline_eval['passing'])
    checks['public_no_regression'] = baseline_eval['passing'] <= revision_eval['passing']
    if not checks['public_no_regression']:
        failures.append('public_eval_regression')


def native_observations(compiled, source, workflow, final_prompt=None):
    """Check supported observable contracts; usable-prompt extraction is separate."""
    compiled = compiled if isinstance(compiled, dict) else {}
    source = source if isinstance(source, dict) else {}
    trace = _trace(compiled)
    artifacts = compiled.get('artifacts', {})
    artifacts = artifacts if isinstance(artifacts, dict) else {}
    references = set()
    for event in trace:
        args = event['arguments']
        if event.get('tool') == 'read_file' and isinstance(args.get('path'), str):
            references.add(args['path'])
        elif event.get('tool') == 'read_files' and isinstance(args.get('paths'), list):
            references.update(path for path in args['paths'] if isinstance(path, str))
    failures, checks = [], {}
    if source.get('id') == 'sentry-prompt-optimizer':
        sections = _sections(compiled.get('output'))
        for name in SECTIONS:
            if name not in sections:
                failures.append('missing_section:' + name)
            elif not sections[name]:
                failures.append('empty_section:' + name)
        needed = {'references/core-patterns.md', 'references/model-family-notes.md',
                  'references/meta-optimization-loop.md' if workflow == 'sharpen'
                  else 'references/transformed-examples.md'}
        failures.extend('unread_required_reference:' + path for path in sorted(needed - references))
    elif source.get('id') == 'alireza-senior':
        _senior(trace, artifacts, final_prompt, failures, checks)
    elif source.get('id') != 'wshobson-patterns':
        failures.append('unsupported_native_contract')
    return {'complete': not failures, 'failures': failures, 'checks': checks,
            'loaded_references': sorted(references),
            'scope': 'Observable native report/reference/static/public-eval evidence; separate from downstream success and semantic quality.'}
