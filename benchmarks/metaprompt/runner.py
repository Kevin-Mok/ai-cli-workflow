"""Reproducible pilot orchestration; all inference crosses the durable quota gate."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import random
import shutil
import sys
import tempfile
import time

from benchlib import (Budget, MINIMAL, aggregate, bind_template, digest, extract_prompt,
                      failure_status, freeze, native_contract, paired_interval, save_json, score_output, verify_freeze)
from runtime import run_codex

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
RUN = ROOT / 'runs' / 'pilot-2026-10-03'
CAP = 50
SEED = 20261003
PILOT_CASES = ['hold-summary-partial', 'hold-coding-window']
MODEL = 'gpt-6.1-sol'
CLARIFICATION = ('No additional facts are available. Preserve the supplied intent and constraints; '
                 'leave unknown facts unknown. Author the prompt using the skill\'s native contract. '
                 'This reply supplies no authorization to execute its downstream task.')


def load_inputs() -> tuple[list[dict], dict, dict]:
    cases = json.loads((ROOT/'cases.json').read_text())
    sources = json.loads((ROOT/'sources.json').read_text())
    keys = json.loads((ROOT/'answer-key.json').read_text())
    for value in (cases, sources, keys):
        if value.get('schema_version') != 1:
            raise ValueError('Unsupported benchmark data schema')
    return cases['cases'], {c['id']: c for c in sources['candidates']}, keys['cases']


def verify() -> dict:
    cases, sources, keys = load_inputs()
    if len({c['id'] for c in cases}) != len(cases) or set(keys) != {c['id'] for c in cases}:
        raise ValueError('Case IDs and answer keys do not match uniquely')
    count = 0
    for candidate in sources.values():
        for name, expected in candidate['files'].items():
            path = ROOT/name
            if not path.resolve().is_relative_to(ROOT) or not path.is_file() or digest(path) != expected:
                raise ValueError('Candidate integrity mismatch: ' + name)
            count += 1
    for case in cases:
        if case['split'] not in {'development', 'holdout'}:
            raise ValueError('Unknown split')
        for name in case.get('files', {}):
            if Path(name).is_absolute() or '..' in Path(name).parts:
                raise ValueError('Unsafe fixture path')
        if case.get('bindings'):
            bind_template(case['task_prompt'], case['bindings'])
    return {'cases': len(cases), 'splits': dict(Counter(c['split'] for c in cases)),
            'heldout_families': dict(Counter(c['family'] for c in cases if c['split'] == 'holdout')),
            'candidates': len(sources)+2, 'pinned_files': count, 'status': 'verified'}


def schedule() -> list[dict]:
    cases, sources, _ = load_inputs()
    families = {c['id']: c['family'] for c in cases}
    rows = [dict(candidate='raw', case_id='dev-extract-inventory', split='development', repeat=0),
            dict(candidate='metaprompt', case_id='dev-guide-summary', split='development', repeat=0)]
    rng = random.Random(SEED)
    for case in PILOT_CASES:
        names = list(sources) + ['raw', 'minimal']
        rng.shuffle(names)
        rows.extend(dict(candidate=name, case_id=case, split='holdout', repeat=0) for name in names)
    for row in rows:
        row.update(id=f"{row['case_id']}--{row['candidate']}--r{row['repeat']}", family=families[row['case_id']],
                   status='pending', success=None)
    return rows


def dry_run() -> dict:
    rows = schedule()
    return {'status': 'dry_run_no_model_calls', 'runtime': {'model': MODEL, 'reasoning': 'medium',
            'billing': 'Codex subscription', 'monetary_cost': None},
            'cap': CAP, 'setup_request_reservation': 1,
            'available_after_setup': CAP-1, 'scheduled_trials': len(rows),
            'minimum_calls': 1 + sum(1 if r['candidate'] in {'raw','minimal'} else 2 for r in rows),
            'upper_bound_attempts': CAP, 'compiler_request_limit': 4, 'solver_request_limit': 2,
            'compiler_timeout_seconds': 180, 'solver_timeout_seconds': 180,
            'native_reference_reads_and_saves': 'additional inference requests count toward the cap',
            'heldout_repetitions': 1, 'full_suite_repetitions_prepared': 3,
            'scope': '2 of 6 families; pilot cannot establish an overall winner',
            'schedule': rows}


def freeze_inputs(refreeze: bool = False) -> None:
    verify()
    RUN.mkdir(parents=True, exist_ok=True)
    protocol = RUN/'protocol.json'
    if protocol.exists():
        if not refreeze:
            verify_freeze(protocol)
            return
        if any(json.loads(p.read_text()).get('split') == 'holdout' and
               json.loads(p.read_text()).get('status') != 'pending' for p in (RUN/'trials').glob('*.json')):
            raise ValueError('Cannot revise the protocol after held-out execution')
        history = RUN/'protocol-history'
        history.mkdir(exist_ok=True)
        shutil.move(protocol, history/f'protocol-{time.time_ns()}.json')
    files = [p for p in ROOT.rglob('*') if p.is_file() and 'runs' not in p.relative_to(ROOT).parts
             and '__pycache__' not in p.parts and p.suffix != '.pyc']
    settings = dry_run()
    settings.update(minimal_baseline=MINIMAL, clarification_reply=CLARIFICATION,
                    retries='No automatic stage retries; transport retries disabled; all attempts retained',
                    selection='No winner unless coverage complete, no hard failures, paired improvement >=0.10 and interval excludes zero; pilot remains provisional',
                    uncertainty='Family-stratified bootstrap of paired case means; repetitions clustered',
                    workflow_track='Static supported-scope audit; dynamic creation/template coverage prepared, not run')
    freeze(protocol, files, settings)
    budget = Budget(RUN/'budget.json', CAP)
    if budget.used == 0:
        budget.permit('setup:unauthenticated-runtime-test-http401')


def _stage(prompt: str, files: dict[str, str], stage: str, trial_id: str, budget: Budget,
           invoke=run_codex, target_file: str | None = None) -> dict:
    limit = 4 if stage == 'compiler' else 2
    calls = 0
    exceeded = False
    def permit() -> bool:
        nonlocal calls, exceeded
        if calls >= limit:
            exceeded = True
            return False
        if not budget.permit(trial_id + ':' + stage):
            return False
        calls += 1
        return True
    with tempfile.TemporaryDirectory(prefix='metaprompt-trial-') as tmp:
        base = Path(tmp)
        scratch = base/'fixture'
        scratch.mkdir()
        for name, content in files.items():
            path = scratch/name
            if not path.resolve().is_relative_to(scratch):
                raise ValueError('Unsafe stage input path')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        log = base/'tools.jsonl'
        # MCP is the only tool surface; its process sees the scratch directory
        # but neither the answer key nor the repository is exposed as a tool.
        prefix = 'prompts' if stage == 'compiler' else target_file or 'artifacts'
        mcp = [sys.executable, str(ROOT/'fixture_mcp.py'), str(scratch), prefix, str(log)]
        if target_file:
            mcp.append('--replace-target')
        result = invoke(prompt, scratch, permit, model=MODEL, effort='medium', timeout=180, mcp_command=mcp)
        result['clarification_turns'] = 0
        if (stage == 'compiler' and result['status'] == 'ok' and '?' in result['output']
                and '```' not in result['output'] and not list((scratch/'prompts').glob('*.md'))):
            initial = result
            continuation = prompt + '\n\nPrevious compiler reply:\n' + initial['output'] + '\n\nUser reply:\n' + CLARIFICATION
            result = invoke(continuation, scratch, permit, model=MODEL, effort='medium', timeout=180, mcp_command=mcp)
            result['prior_reply'] = initial
            result['clarification_turns'] = 1
            result['latency_seconds'] += initial['latency_seconds']
            result['call_count'] += initial['call_count']
            result['requests'] = initial.get('requests',[]) + result.get('requests',[])
            if initial.get('usage') and result.get('usage'):
                result['usage'] = dict(Counter(initial['usage']) + Counter(result['usage']))
            else:
                result['usage'] = None
        trace = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
        artifacts = {str(p.relative_to(scratch)): p.read_text()
                     for p in (scratch/('prompts' if stage == 'compiler' else 'artifacts')).rglob('*') if p.is_file()}
        if target_file and any(e['tool']=='write_file' and e['status']=='ok' and e['arguments'].get('path')==target_file for e in trace):
            artifacts[target_file] = (scratch/target_file).read_text()
        result.update(input_prompt=prompt, fixture_files=files, tool_trace=trace, artifacts=artifacts,
                      loaded_references=[e['arguments']['path'] for e in trace if e['tool'] == 'read_file' and e['status'] == 'ok'],
                      hard_failures=['unauthorized_tool_access' for e in trace if e['status'] == 'denied'],
                      local_request_limit_exceeded=exceeded)
    # Replace ephemeral locations in stored runtime metadata; never save auth.
    serialized = json.dumps(result).replace(str(base), '<scratch>')
    return json.loads(serialized)


def execute_trial(row: dict, case: dict, source: dict | None, key: dict, budget: Budget,
                  invoke=run_codex) -> dict:
    record = dict(row, started_at=time.time(), compiler=None, solver=None, clarification_turns=0)
    prompt = case['task_prompt']
    if row['candidate'] == 'minimal':
        prompt = MINIMAL + prompt
    elif source:
        root = (ROOT/source['entrypoint']).parent
        files = {}
        for filename in source['files']:
            path = ROOT/filename
            if path.is_relative_to(root) and path.suffix not in {'.svg'}:
                files[str(path.relative_to(root))] = path.read_text()
        request = ('Apply the supplied skill to this prompt-authoring request. You are in an isolated '
                   'workspace. The supplied skill is the only skill active here. References use paths '
                   'relative to this workspace. Read needed references with the fixture MCP tools. '
                   'Save new prompts under prompts/ when the skill requires it. Shell, network, '
                   'external messages and deployment tools are unavailable. Follow the skill\'s native '
                   'interaction and output contract.\n\nSkill entrypoint:\n' + files['SKILL.md'] +
                   '\n\nRequest: Sharpen this existing task prompt:\n\n' + prompt +
                   '\n\nCompiler context:\n' + case.get('compiler_context',''))
        record['compiler'] = _stage(request, files, 'compiler', row['id'], budget, invoke)
        compiled = record['compiler']
        extracted = extract_prompt(compiled['output'], compiled['artifacts'], row['candidate'])
        # A single scripted clarification uses remaining stage/global budget.
        # This pilot does not authorize a standalone legacy `go` or hidden extra
        # optimization pass. Questions without a usable prompt remain visible.
        record['clarification_requested'] = extracted['prompt'] is None and '?' in compiled['output']
        record['clarification_turns'] = compiled['clarification_turns']
        record['clarification_policy_executed'] = bool(compiled['clarification_turns'])
        record['extraction'] = extracted
        must_save = row['candidate'] in {'metaprompt', 'metaprompt-alxve'}
        record['artifact_contract_satisfied'] = bool(compiled['artifacts']) if must_save else None
        record['native_contract_failures'] = native_contract(row['candidate'], compiled['output'], compiled['artifacts'])
        if compiled['status'] != 'ok':
            record.update(status=failure_status(compiled), success=False)
            return record
        if not extracted['prompt'] or record['native_contract_failures'] or compiled['hard_failures']:
            record.update(status='compile_failed', success=False)
            return record
        prompt = extracted['prompt']
    try:
        if case.get('bindings'):
            prompt = bind_template(prompt, case['bindings'])
    except ValueError as exc:
        record.update(status='compile_failed', success=False, error=str(exc))
        return record
    record['compiled_prompt'] = prompt
    request = prompt + '\n\nSupplied task inputs:\n' + case.get('solver_context','')
    record['solver'] = _stage(request, case.get('files', {}), 'solver', row['id'], budget, invoke, key.get('target_file'))
    solver = record['solver']
    if solver['status'] != 'ok':
        record.update(status=failure_status(solver, (record.get('compiler') or {}).get('call_count',0)), success=False)
        return record
    output = solver['output']
    if key['kind'] == 'python' and 'artifacts/'+key['target_file'] in solver['artifacts']:
        output = solver['artifacts']['artifacts/'+key['target_file']]
    grading_started = time.monotonic()
    record['score'] = score_output(output, key, solver['hard_failures'])
    if key['kind'] == 'python' and key['target_file'] in solver['artifacts']:
        record['fixture_score'] = score_output(solver['artifacts'][key['target_file']],key,solver['hard_failures'])
        record['score']['success'] = record['score']['success'] and record['fixture_score']['success']
    record['grading_latency_seconds'] = time.monotonic() - grading_started
    record.update(status='completed', success=record['score']['success'], finished_at=time.time())
    return record


def execute(phase: str, retry_infrastructure: bool = False) -> dict:
    freeze_inputs()
    protocol = verify_freeze(RUN/'protocol.json')
    cases, sources, keys = load_inputs()
    case_map = {c['id']: c for c in cases}
    budget = Budget(RUN/'budget.json', CAP)
    trials = RUN/'trials'
    trials.mkdir(exist_ok=True)
    if phase == 'holdout':
        dev = [trials/(r['id']+'.json') for r in schedule() if r['split']=='development']
        valid_development = {'completed', 'compile_failed', 'solver_failed', 'episode_limit'}
        if not all(p.is_file() and json.loads(p.read_text())['status'] in valid_development for p in dev):
            raise ValueError('Complete development transport/scoring pilot before holdout')
    for row in protocol['settings']['schedule']:
        if row['split'] != phase or budget.used >= CAP:
            continue
        path = trials/(row['id']+'.json')
        if path.exists():
            previous = json.loads(path.read_text())
            if not retry_infrastructure or previous['status'] != 'infrastructure_error' or phase != 'development':
                continue
            archive = RUN/'failed-attempts'
            archive.mkdir(exist_ok=True)
            shutil.move(path, archive/(row['id']+f'-{time.time_ns()}.json'))
        save_json(path, dict(row, status='interrupted', success=False))
        result = execute_trial(row, case_map[row['case_id']], sources.get(row['candidate']), keys[row['case_id']], budget)
        save_json(path, result)
        print(json.dumps({'trial': row['id'], 'status': result['status'], 'success': result['success'],
                          'budget_used': budget.used}), flush=True)
        if result['status'] == 'infrastructure_error':
            incident = REPO/'docs/postmortem/2026-10-03-metaprompt-benchmark-trial-infrastructure.md'
            if not incident.exists():
                incident.write_text('# Benchmark trial infrastructure failure\n\n'
                                    'Date: 2026-10-03. Trials stop on infrastructure errors; retain all attempts.\n\n')
            with incident.open('a') as handle:
                stage = result.get('solver') or result.get('compiler') or {}
                handle.write(f"- Trial `{row['id']}`: {stage.get('error')}. Impact: trial unscored; "
                             f"{budget.used}/{CAP} total requests reserved. Evidence retained in the run JSON. "
                             'Status: investigation required before further model execution.\n')
            break
    summary = report()
    return {k:summary[k] for k in ['reserved_requests','cap','recommendation_status']}


def report() -> dict:
    rows = []
    protocol = RUN/'protocol.json'
    frozen_rows = verify_freeze(protocol)['settings']['schedule'] if protocol.exists() else schedule()
    for row in frozen_rows:
        path = RUN/'trials'/(row['id']+'.json')
        rows.append(json.loads(path.read_text()) if path.exists() else row)
    heldout = [r for r in rows if r['split']=='holdout']
    total_usage = Counter()
    usage_unknown = 1  # unauthenticated setup attempt has no token measurement
    latency = 0.0
    archive = [json.loads(p.read_text()) for p in (RUN/'failed-attempts').glob('*.json')]
    for row in rows + archive:
        for stage in ['compiler','solver']:
            data = row.get(stage)
            if data:
                latency += data['latency_seconds']
                if data.get('usage'):
                    total_usage.update({k:v for k,v in data['usage'].items() if isinstance(v,int)})
                else:
                    usage_unknown += 1
    sources = load_inputs()[1]
    result = {'schema_version': 1, 'label': 'budget-constrained exploratory pilot',
              'model': MODEL, 'reasoning': 'medium', 'cap': CAP,
              'reserved_requests': Budget(RUN/'budget.json', CAP).used,
              'measured_usage': dict(total_usage), 'stages_with_unknown_usage_including_setup': usage_unknown,
              'measured_latency_seconds': latency, 'monetary_cost': None,
              'billing': 'subscription usage; USD billing not exposed',
              'preparation_model_usage': None, 'grading_model_calls': 0,
              'measured_grading_latency_seconds': sum(r.get('grading_latency_seconds',0) for r in rows + archive),
              'completed_trials_with_unmeasured_grading_latency': sum(r['status']=='completed' and 'grading_latency_seconds' not in r for r in rows + archive),
              'workflow_coverage': {k:v['supported_workflows'] for k,v in sources.items()},
              'dynamic_workflow_coverage': 'not executed; shared sharpening track only',
              'heldout_summary': aggregate(heldout),
              'paired_vs_raw': {name:paired_interval(heldout,name,'raw') for name in sources},
              'paired_vs_minimal': {name:paired_interval(heldout,name,'minimal') for name in sources},
              'trials': rows, 'archived_failed_attempts': archive,
              'recommendation_status': 'insufficient_coverage_for_overall_winner'}
    if RUN.exists():
        save_json(RUN/'results.json', result)
    return {k:v for k,v in result.items() if k not in {'trials','archived_failed_attempts'}}


def main() -> None:
    parser = argparse.ArgumentParser(description=('' if os.environ.get('CLI_PLAIN') == '1' else '📖 ') + __doc__)
    parser.add_argument('command', choices=['verify','dry-run','freeze','refreeze-development','run','report'])
    parser.add_argument('--phase', choices=['development','holdout'], default='development')
    parser.add_argument('--retry-infrastructure', action='store_true', help='Retain failed development attempt and retry after a diagnosed fix; consumes existing budget')
    args = parser.parse_args()
    try:
        if args.command == 'verify':
            result = verify()
        elif args.command == 'dry-run':
            result = dry_run()
        elif args.command in {'freeze','refreeze-development'}:
            freeze_inputs(args.command == 'refreeze-development')
            result = {'status':'frozen','path':str(RUN/'protocol.json')}
        elif args.command == 'run':
            result = execute(args.phase,args.retry_infrastructure)
        else:
            result = report()
        print(json.dumps(result, indent=2))
    except (ValueError,OSError,KeyError) as exc:
        parser.exit(2, f'Benchmark stopped: {exc}\n')


if __name__ == '__main__':
    main()
