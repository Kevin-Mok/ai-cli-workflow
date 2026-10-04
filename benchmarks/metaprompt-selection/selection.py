"""Balanced skill selection; all trial and inference reservations are durable."""
import argparse
from collections import Counter
import fcntl
import json
import os
from pathlib import Path
import random
import re
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor

from selection_core import (Budget, MINIMAL, bind_template, digest, extract_prompt,
                            freeze, save_json, score_output, verify_freeze)
from selection_runtime import run_codex
from selection_eval import StageBudget
from selection_native import native_observations

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
RUN = ROOT / 'runs' / 'selection-2026-10-03'
WORKFLOWS = ('create', 'sharpen', 'template', 'coding')
MODEL = 'gpt-6.1-sol'
SEED = 20261003
CLARIFICATION = ('Use only supplied facts. No additional facts are available; preserve unknowns. '
                 'Please complete your native prompt-authoring workflow now, including any required '
                 'refinement step. This authorizes prompt creation only, not the downstream task. '
                 'Keep canonical template slots when requested. Supply a single final prompt deliverable.')


def allocation(arms: int) -> dict:
    if type(arms) is not int or not 2 <= arms <= 7:
        raise ValueError('Expected two controls and at most five finalists')
    held = 4 * ((100 // arms - 2) // 4)
    return {'development_per_arm': 2, 'holdout_per_arm': held, 'total': arms * (2 + held)}


class TrialLedger:
    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)

    def reserve(self, ident: str) -> bool:
        with self.path.open('a+') as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            handle.seek(0)
            data = handle.read()
            state = json.loads(data) if data else {'cap': 100, 'trials': []}
            if state['cap'] != 100:
                raise ValueError('Trial cap changed')
            if len(state['trials']) >= 100 or ident in {r['id'] for r in state['trials']}:
                return False
            state['trials'].append({'id': ident, 'reserved_at': time.time()})
            handle.seek(0)
            handle.truncate()
            json.dump(state, handle, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
            return True

    @property
    def used(self) -> int:
        if not self.path.exists():
            return 0
        with self.path.open() as handle:
            fcntl.flock(handle, fcntl.LOCK_SH)
            return len(json.load(handle)['trials'])


class StageGate:
    def __init__(self, budget: Budget, label: str):
        self.budget, self.label = budget, label
        self.shared = StageBudget(budget.path, label, cap=budget.cap)

    @property
    def calls(self) -> int:
        return self.shared.used

    @property
    def exceeded(self) -> bool:
        return self.shared.stage_exhausted

    def permit(self) -> bool:
        return self.shared.permit()


def request_usage(stage: dict | None) -> dict:
    total = Counter()
    for request in (stage or {}).get('requests', []):
        usage = request.get('usage') or {}
        total.update(input_tokens=usage.get('input_tokens', 0), output_tokens=usage.get('output_tokens', 0),
                     cached_input_tokens=usage.get('input_tokens_details', {}).get('cached_tokens', 0),
                     reasoning_tokens=usage.get('output_tokens_details', {}).get('reasoning_tokens', 0))
    return dict(total)


def summarize(rows: list[dict], sources: dict) -> dict:
    arms = {}
    for name in sorted({row['candidate'] for row in rows}):
        group = [r for r in rows if r['candidate'] == name and r['split'] == 'holdout']
        workflows = {}
        for workflow in WORKFLOWS:
            subset = [r for r in group if r['workflow'] == workflow]
            workflows[workflow] = {'successes': sum(r.get('success') is True for r in subset), 'attempts': len(subset)}
        complete = (all(v['attempts'] for v in workflows.values()) and
                    len({v['attempts'] for v in workflows.values()}) == 1 and
                    not any(r['status'] in {'pending', 'interrupted', 'infrastructure_error', 'quota_truncated'} for r in group))
        weighted = sum(v['successes'] / v['attempts'] for v in workflows.values()) / 4 if complete else None
        hard = [f for r in group for f in r.get('hard_failures', [])]
        usage_complete = all(r.get('usage_complete', True) and r.get('first_use_input_tokens') is not None for r in group)
        total_input = sum(r.get('first_use_input_tokens') or 0 for r in group)
        arms[name] = {'workflows': workflows, 'weighted_success': weighted,
                      'successes': sum(r.get('success') is True for r in group), 'attempts': len(group),
                      'statuses': dict(Counter(r['status'] for r in group)), 'hard_failures': hard,
                      'eligible_for_default': name in sources and complete and not hard,
                      'usage_complete': usage_complete,
                      'mean_first_use_input_tokens': total_input / len(group) if group and usage_complete else None}
    choices = [name for name, value in arms.items() if value['eligible_for_default']]
    def order(name):
        source, arm = sources[name], arms[name]
        return (arm['weighted_success'], source.get('latest_substantive_change', ''),
                -(arm['mean_first_use_input_tokens'] if arm['mean_first_use_input_tokens'] is not None else float('inf')), source.get('stars', 0))
    chosen = max(choices, key=order) if choices else None
    controls = [arms[name]['weighted_success'] for name in ('raw', 'minimal') if name in arms and arms[name]['weighted_success'] is not None]
    return {'arms': arms, 'recommended_skill': chosen,
            'skill_improves_on_controls': bool(chosen and controls and arms[chosen]['weighted_success'] > max(controls)),
            'interpretation': 'Practical choice from a small balanced synthetic sample; no claim of universal superiority.'}


def extract_compilation(output: str, artifacts: dict[str, str], source: dict) -> dict:
    prompts = {name: value for name, value in artifacts.items() if name.endswith(('.md', '.txt'))
               and not re.search(r'(?:^|/)(?:current_prompt|baseline|eval|draft)[^/]*$', name)}
    for line in output.splitlines():
        prefix = line.split('[', 1)[0]
        if not (re.search(r'\b(final|revised|optimized)\b', prefix, re.I) and re.search(r'\bprompt\b', prefix, re.I)):
            continue
        links = re.findall(r'\[([^\]]+)\]\(([^\n]+)\)', line)
        choices = {value.removeprefix('<scratch>/fixture/').removeprefix('./') for link in links for value in link}
        matches = [name for name in prompts if name in choices]
        if len(matches) == 1:
            return {'prompt': prompts[matches[0]], 'adapter': 'explicit_final_markdown_link'}
    for pattern in (r'(?im)^(?:Final|Revised|Optimized) prompt(?: file)?:\s*`?([^`\n]+)`?\s*$',):
        named = re.search(pattern, output)
        if named and named.group(1) in prompts:
            return {'prompt': prompts[named.group(1)], 'adapter': 'explicit_final_artifact'}
    result = extract_prompt(output, prompts, source.get('adapter', ''))
    if result['adapter'] == 'only_saved_artifact':
        # An intermediate saved file is not evidence that native authoring ended.
        result = {'prompt': None, 'adapter': 'final_artifact_not_identified'}
    if result['prompt'] is not None or result['adapter'] in {'saved_prompt_mismatch', 'ambiguous_prompt_fences'}:
        return result
    section = re.search(r'(?ims)^#{1,4}\s*(?:\d+[.)]?\s*)?(?:Final|Revised|Optimized) Prompt\s*\n(.*?)(?=^#{1,4}\s|\Z)', output)
    if section:
        raw = section.group(1).strip()
        match = re.fullmatch(r'```[^\n]*\n(.*?)\n```', raw, re.S)
        return {'prompt': match.group(1) if match else raw, 'adapter': 'explicit_final_section'}
    fences = re.findall(r'```(?:text|markdown|md)?\s*\n(.*?)\n```', output, re.S)
    if len(fences) == 1:
        return {'prompt': fences[0], 'adapter': 'single_native_text_fence'}
    return {'prompt': None, 'adapter': 'no_unambiguous_final_prompt'}


def coding_actions(trace: list[dict], target: str) -> dict:
    good = expanded_trace(trace)
    reads = {event['arguments'].get('path') for event in good if event['tool'] == 'read_file'}
    writes = [i for i, event in enumerate(good) if event['tool'] == 'write_file' and event['arguments'].get('path') == target]
    tests = [(i, json.loads(event['result']).get('success')) for i, event in enumerate(good) if event['tool'] == 'run_tests']
    checks = {'read_target': target in reads, 'read_public_tests': 'public_tests.py' in reads,
              'wrote_target': bool(writes),
              'public_red_before_fix': bool(writes and any(i < writes[0] and passed is False for i, passed in tests)),
              'public_green_after_fix': bool(writes and any(i > writes[-1] and passed is True for i, passed in tests)),
              'stopped_after_green': not any(passed is True and any(j > i for j in writes) for i, passed in tests)}
    return {'success': all(checks.values()), 'checks': checks}


def expanded_trace(trace: list[dict]) -> list[dict]:
    result = []
    for event in trace:
        if event['status'] != 'ok':
            continue
        if event['tool'] == 'read_files':
            result.extend(dict(event, tool='read_file', arguments={'path': path}) for path in event['arguments']['paths'])
        elif event['tool'] == 'write_files':
            result.extend(dict(event, tool='write_file', arguments=item) for item in event['arguments']['files'])
        else:
            result.append(event)
    return result


def stage(prompt: str, files: dict[str, str], name: str, trial_id: str, budget: Budget,
          invoke=run_codex, target: str | None = None, source: dict | None = None) -> dict:
    gate = StageGate(budget, trial_id + ':' + name)
    with tempfile.TemporaryDirectory(prefix='metaprompt-selection-') as tmp:
        base = Path(tmp)
        scratch = base / 'fixture'
        scratch.mkdir()
        for filename, content in files.items():
            path = scratch / filename
            if not path.resolve().is_relative_to(scratch):
                raise ValueError('Unsafe stage input path')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        log = base / 'tools.jsonl'
        command = [sys.executable, str(ROOT / 'selection_mcp.py'), str(scratch),
                   'prompts' if name == 'compiler' else target or 'artifacts', str(log)]
        if target:
            command.append('--replace-target')
        if source and source.get('approved_helper'):
            command.extend(['--skill-check', source['approved_helper']])
        if name == 'compiler':
            command.extend(['--budget', str(budget.path.resolve()), '--stage-label', trial_id + ':compiler'])
        replies, current = [], prompt
        for continuation in range(3):
            result = invoke(current, scratch, gate.permit, model=MODEL, effort='medium', timeout=600, mcp_command=command)
            replies.append(result)
            artifacts = {str(p.relative_to(scratch)): p.read_text() for area in ('prompts', 'artifacts')
                         for p in (scratch / area).rglob('*') if p.is_file()}
            if target and (scratch / target).exists():
                artifacts[target] = (scratch / target).read_text()
            if (name != 'compiler' or result['status'] != 'ok' or
                    extract_compilation(result['output'].replace(str(base), '<scratch>'), artifacts, source or {})['prompt'] is not None or
                    gate.calls >= 10):
                break
            current += '\n\nPrevious author reply:\n' + result['output'] + '\n\nUser reply:\n' + CLARIFICATION
        trace = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
        combined = dict(replies[-1])
        combined.update(input_prompt=prompt, fixture_files=files, tool_trace=trace, artifacts=artifacts,
                        clarification_turns=len(replies) - 1, prior_replies=replies[:-1],
                        latency_seconds=sum(r['latency_seconds'] for r in replies), call_count=gate.calls,
                        requests=([request for r in replies for request in r.get('requests', [])] +
                                  [request for event in trace for request in event.get('native_runtime', {}).get('requests', [])]),
                        hard_failures=['unauthorized_tool_access' for event in trace if event['status'] == 'denied'],
                        local_request_limit_exceeded=gate.exceeded)
        if gate.exceeded:
            combined['status'] = 'episode_limit'
        elif combined['status'] == 'budget_exhausted':
            combined['status'] = 'quota_truncated'
    return json.loads(json.dumps(combined).replace(str(base), '<scratch>'))


def execute_trial(row: dict, case: dict, source: dict | None, key: dict, budget: Budget,
                  invoke=run_codex, compiler_override: dict | None = None) -> dict:
    record = dict(row, started_at=time.time(), compiler=None, solver=None, hard_failures=[], case_input_version=case.get('input_version', 1))
    prompt = case['task_prompt']
    if row['candidate'] == 'minimal':
        prompt = MINIMAL + prompt
    elif source:
        package = (ROOT / source['entrypoint']).parent
        files = {}
        for filename in source['files']:
            path = ROOT / filename
            if path.is_relative_to(package) and path.suffix not in {'.svg', '.png', '.jpg', '.pyc'}:
                files[str(path.relative_to(package))] = path.read_text()
        request = ('Apply the supplied native skill to the prompt-authoring request. It is the only active skill. '
                   'Complete its authoring/refinement workflow, not the downstream task. Native references and '
                   'scripts are relative to this isolated workspace. Use read_files to load needed references '
                   'together and write_files to save related prompt/eval files together, conserving inference turns. '
                   'Save prompt inputs/drafts/finals under prompts/ when files are needed; baseline input can be '
                   'prompts/current_prompt.txt. ' +
                   ('Native static analysis is available through run_skill_check (fixed prompt_optimizer.py, '
                    '--analyze --json, optional baseline comparison/output). ' if source.get('approved_helper') else '') +
                   'Helper and evaluation outputs belong under artifacts/. No shell, external messages or deployment. '
                   'Label the final prompt unambiguously for mechanical handoff; preserve the native report format. '
                   'Public model evaluations are available through evaluate_prompt(prompt_path,cases_path,output_path). '
                   'First write your own representative public cases under prompts/ as a JSON array of '
                   '{"id":string,"input":JSON,"expected":JSON}. It supports 1-20 cases, batched in one fresh '
                   'no-tools model context and compared by exact typed JSON; code/text outputs are strings. '
                   'No hidden inputs or keys are available. Expected values stay in the checker, not the evaluator prompt. '
                   'These evals share your compiler allowance of ten total inference requests; tool calls may be grouped. '
                   'Reserve a request for your final deliverable. If the allowance prevents more evaluation, '
                   'return the best authored prompt and state which native checks remain unverified; do not claim it passed them. '
                   'Do not claim an evaluation ran unless its tool result confirms it. '
                   'Target downstream runtime is Codex gpt-6.1-sol, medium reasoning.\n\n'
                   'Available relative files:\n' + '\n'.join(sorted(files)) +
                   '\n\nSkill entrypoint:\n' + files['SKILL.md'] +
                   '\n\nPrompt-authoring request:\n' + case['authoring_request'] +
                   '\n\nCompiler context:\n' + case.get('compiler_context', ''))
        if case.get('files'):
            request += '\n\nPublic task files available to the downstream solver (read-only authoring context):\n' + json.dumps(case['files'])
        if compiler_override is not None and row['split'] != 'development':
            raise ValueError('Compiler recovery is permitted only before held-out execution')
        compiled = compiler_override if compiler_override is not None else stage(request, files, 'compiler', row['id'], budget, invoke, source=source)
        record['compiler'] = compiled
        record['hard_failures'].extend(compiled['hard_failures'])
        effective_output = compiled.get('recovered_author_output', compiled['output'])
        extracted = extract_compilation(effective_output, compiled['artifacts'], source)
        record['extraction'] = extracted
        record['native_deliverable_completed'] = extracted['prompt'] is not None
        record['native_workflow'] = native_observations(dict(compiled, output=effective_output), source, case['workflow'], final_prompt=extracted['prompt'])
        if ((compiled['status'] != 'ok' and compiler_override is None) or extracted['prompt'] is None or compiled['hard_failures']):
            record.update(status=compiled['status'] if compiled['status'] != 'ok' else 'compile_failed', success=False)
            return finish_record(record)
        prompt = extracted['prompt']
    try:
        if case.get('bindings'):
            prompt = bind_template(prompt, case['bindings'])
    except ValueError as exc:
        record.update(status='compile_failed', success=False, error=str(exc))
        return finish_record(record)
    record['compiled_prompt'] = prompt
    request = (prompt + '\n\nSupplied task inputs:\n' + case.get('solver_context', '') +
               '\n\nRuntime: only fixture read_file, write_file, list_files, and run_tests tools are available. '
               'run_tests executes the supplied public tests; no arguments. Do not claim unobserved actions.\n'
               'Available relative files:\n' + '\n'.join(sorted(case.get('files', {}))))
    solver = stage(request, case.get('files', {}), 'solver', row['id'], budget, invoke, target=case.get('target_file'))
    record['solver'] = solver
    record['hard_failures'].extend(solver['hard_failures'])
    if solver['status'] != 'ok':
        record.update(status=solver['status'], success=False)
        return finish_record(record)
    record['score'] = score_output(solver['output'], key, record['hard_failures'])
    if key['kind'] == 'python':
        record['fixture_score'] = score_output(solver['artifacts'].get(key['target_file'], ''), key, record['hard_failures'])
        record['coding_actions'] = coding_actions(solver['tool_trace'], key['target_file'])
        record['score']['success'] = (record['score']['success'] and record['fixture_score']['success']
                                      and record['coding_actions']['success'])
    record['hard_failures'].extend(record['score']['hard_failures'])
    record.update(status='completed', success=record['score']['success'])
    record['downstream_success'] = record['success']
    return finish_record(record)


def finish_record(record: dict) -> dict:
    compiler, solver = request_usage(record.get('compiler')), request_usage(record.get('solver'))
    stages = [record[name] for name in ('compiler', 'solver') if record.get(name)]
    complete = all(len(s.get('requests', [])) == s.get('call_count', 0) and
                   all(r.get('usage') is not None for r in s.get('requests', [])) for s in stages)
    record.update(finished_at=time.time(), compiler_usage=compiler, solver_usage=solver,
                  usage_complete=complete,
                  first_use_input_tokens=(compiler.get('input_tokens', 0) + solver.get('input_tokens', 0)) if complete else None,
                  first_use_output_tokens=(compiler.get('output_tokens', 0) + solver.get('output_tokens', 0)) if complete else None)
    return record


def recovery_author_output(record: dict, source: dict) -> str | None:
    if record['split'] != 'development' or record.get('solver') is not None:
        raise ValueError('Only an unused development solver stage can be continued')
    compiled = record.get('compiler') or {}
    for reply in compiled.get('prior_replies', []) + [compiled]:
        if reply.get('status') == 'ok' and extract_compilation(reply.get('output', ''), compiled.get('artifacts', {}), source)['prompt'] is not None:
            return reply['output']
    return None


def recover_development() -> dict:
    if (RUN / 'protocol.json').exists():
        raise ValueError('Development recovery is closed after freeze')
    cases, sources, keys = load_inputs()
    by_id = {case['id']: case for case in cases}
    recovered = []
    budget = Budget(RUN / 'requests.json', 2000)
    for path in sorted((RUN / 'trials').glob('*--d2.json')):
        record = json.loads(path.read_text())
        if record.get('solver') is not None or not record.get('compiler'):
            continue
        source = sources.get(record['candidate'])
        output = recovery_author_output(record, source or {})
        if output is None or record['compiler'].get('hard_failures'):
            continue
        archive = RUN / 'development-recovery' / path.name
        if archive.exists():
            continue
        save_json(archive, record)
        compiled = dict(record['compiler'], recovered_author_output=output)
        row = {key: record[key] for key in ('id', 'candidate', 'case_id', 'split', 'workflow', 'family', 'status', 'success')}
        resumed = execute_trial(row, by_id[row['case_id']], source, keys[row['case_id']], budget, compiler_override=compiled)
        resumed['recovery'] = {'reason': 'Development adapter missed explicit native final artifact link',
                               'original_trial': '../development-recovery/' + path.name,
                               'new_compiler_requests': 0, 'additional_trial_reservations': 0}
        save_json(path, resumed)
        recovered.append({'id': row['id'], 'status': resumed['status'], 'success': resumed['success']})
        print(json.dumps(recovered[-1]), flush=True)
    return {'recovered': recovered, 'requests_reserved': budget.used, 'development_gate': development_gate()}


def load_inputs() -> tuple[list[dict], dict, dict]:
    values = [json.loads((ROOT / name).read_text()) for name in ('cases.json', 'sources.json', 'answer-key.json')]
    if any(value.get('schema_version') != 1 for value in values):
        raise ValueError('Unsupported input schema')
    return values[0]['cases'], {c['id']: c for c in values[1]['candidates']}, values[2]['cases']


def build_schedule(cases: list[dict], sources: dict) -> list[dict]:
    names = list(sources) + ['raw', 'minimal']
    counts, rng = allocation(len(names)), random.Random(SEED)
    development = [case for case in cases if case['split'] == 'development']
    if len(development) != 2:
        raise ValueError('Exactly two development cases required')
    selected = development[:]
    for workflow in WORKFLOWS:
        choices = [case for case in cases if case['split'] == 'holdout' and case['workflow'] == workflow]
        needed = counts['holdout_per_arm'] // 4
        if len(choices) < needed:
            raise ValueError('Insufficient fresh cases for workflow ' + workflow)
        rng.shuffle(choices)
        selected.extend(choices[:needed])
    rows = []
    for case in selected:
        order = names[:]
        rng.shuffle(order)
        for name in order:
            rows.append({'id': case['id'] + '--' + name, 'candidate': name, 'case_id': case['id'],
                         'split': case['split'], 'workflow': case['workflow'], 'family': case.get('family', case['workflow']),
                         'status': 'pending', 'success': None})
    return rows


def verify() -> dict:
    cases, sources, keys = load_inputs()
    if len({c['id'] for c in cases}) != len(cases) or set(keys) != {c['id'] for c in cases}:
        raise ValueError('Case IDs and keys must match uniquely')
    references = json.loads((ROOT / 'reference-solutions.json').read_text())['cases']
    files, checked, red = 0, 0, 0
    for source in sources.values():
        if not source.get('eligible'):
            raise ValueError('An ineligible candidate entered the finalist manifest')
        for name, expected in source['files'].items():
            path = ROOT / name
            if not path.resolve().is_relative_to(ROOT) or not path.is_file() or digest(path) != expected:
                raise ValueError('Source integrity failure: ' + name)
            files += 1
    for case in cases:
        if case['workflow'] not in WORKFLOWS or case['split'] not in {'development', 'holdout'}:
            raise ValueError('Unsupported workflow or split')
        for name in case.get('files', {}):
            if Path(name).is_absolute() or '..' in Path(name).parts:
                raise ValueError('Unsafe fixture path')
        key = keys[case['id']]
        if not score_output(references[case['id']], key)['success']:
            raise ValueError('Reference answer does not pass: ' + case['id'])
        checked += 1
        if key['kind'] == 'python':
            original = case['files'][key['target_file']]
            public = dict(key, python_tests=case['files']['public_tests.py'])
            if score_output(original, key)['success'] or score_output(original, public)['success']:
                raise ValueError('Buggy fixture must fail public and hidden checks: ' + case['id'])
            if not score_output(references[case['id']], public)['success']:
                raise ValueError('Reference must pass public checks: ' + case['id'])
            red += 1
        if case.get('bindings'):
            bind_template(case['task_prompt'], case['bindings'])
    schedule = settings()['schedule']
    if len(schedule) > 100:
        raise ValueError('Selected development and held-out schedule exceeds 100 attempts')
    return {'status': 'verified', 'cases': len(cases), 'finalists': len(sources), 'pinned_files': files,
            'reference_answers_passed': checked, 'coding_red_green_pairs': red, 'scheduled_trials': len(schedule)}


def settings() -> dict:
    cases, sources, _ = load_inputs()
    base = build_schedule(cases, sources)
    second = [dict(row, id=row['id'] + '--d2', development_round=2) for row in base if row['split'] == 'development']
    return {'model': MODEL, 'reasoning': 'medium', 'billing': 'Codex subscription', 'dollar_cost': None,
            'trial_cap': 100, 'request_cap': 2000, 'compiler_requests_per_trial': 10, 'solver_requests_per_trial': 10,
            'stage_timeout_seconds': 600, 'allocation': allocation(len(sources) + 2), 'seed': SEED,
            'second_development_round': len(second), 'total_planned_trials': len(base) + len(second),
            'minimal_contract': MINIMAL, 'clarification_reply': CLARIFICATION, 'max_clarification_replies': 2,
            'schedule': base + second,
            'ranking': 'Equal workflow success; exclude serious authorization failures; exact ties: latest substantive maintenance, mean first-use input tokens, stars',
            'cost': 'Request-level input/output/cache/reasoning tokens, including unsuccessful episodes; no invented subscription dollar price',
            'native_adaptation': 'Isolated fixture tools; public batch evaluations share compiler quota; reviewed native static helper where required; final-prompt handoff label',
            'inference_retries': 'None; every reserved failed attempt counts; interrupted trials never replay automatically'}


def development_gate() -> dict:
    cases, sources, _ = load_inputs()
    needed = [row for row in settings()['schedule'] if row.get('development_round') == 2]
    rows = []
    for row in needed:
        path = RUN / 'trials' / (row['id'] + '.json')
        if path.exists():
            rows.append(json.loads(path.read_text()))
    return development_readiness(rows, [row['id'] for row in needed])


def development_readiness(rows: list[dict], expected_ids: list[str]) -> dict:
    by_id = {row['id']: row for row in rows}
    problems = []
    for ident in expected_ids:
        if ident not in by_id:
            problems.append(ident + ': missing')
            continue
        trial = by_id[ident]
        if trial['status'] != 'completed':
            problems.append(ident + ': ' + trial['status'])
    if not any(row['workflow'] == 'coding' and row.get('coding_actions', {}).get('success') for row in rows):
        problems.append('Shared coding runtime has not demonstrated a complete read/RED/edit/GREEN workflow')
    return {'ready': not problems, 'problems': problems}


def freeze_inputs() -> dict:
    verified = verify()
    gate = development_gate()
    if not gate['ready']:
        raise ValueError('Development gate incomplete: ' + '; '.join(gate['problems']))
    protocol = RUN / 'protocol.json'
    if protocol.exists():
        verify_freeze(protocol)
        return {'status': 'already_frozen', **verified}
    files = [path for path in ROOT.rglob('*') if path.is_file() and 'runs' not in path.relative_to(ROOT).parts
             and '__pycache__' not in path.parts and path.suffix != '.pyc']
    files += list((REPO / 'scripts').glob('metaprompt-selection*.py'))
    files += list((REPO / 'tests').glob('test_metaprompt_selection*.py'))
    freeze(protocol, files, settings())
    return {'status': 'frozen', 'protocol_sha256': digest(protocol), **verified}


def execute(phase: str, jobs: int = 2, development_round: int = 1) -> dict:
    if phase not in {'development', 'holdout'} or jobs not in {1, 2, 3}:
        raise ValueError('Unsupported phase or parallelism')
    cases, sources, keys = load_inputs()
    by_id = {case['id']: case for case in cases}
    if phase == 'holdout':
        frozen = verify_freeze(RUN / 'protocol.json')
        rows = frozen['settings']['schedule']
    else:
        verify()
        rows = [row for row in settings()['schedule'] if row.get('development_round', 1) == development_round]
        version = RUN / ('development-settings' + ('-round2' if development_round == 2 else '') + '.json')
        if not version.exists():
            save_json(version, settings())
    budget, ledger = Budget(RUN / 'requests.json', 2000), TrialLedger(RUN / 'trial-ledger.json')
    pending = [row for row in rows if row['split'] == phase and not (RUN / 'trials' / (row['id'] + '.json')).exists()]
    def run_one(row):
        if not ledger.reserve(row['id']):
            return dict(row, status='previously_reserved_or_trial_cap', success=False)
        path = RUN / 'trials' / (row['id'] + '.json')
        save_json(path, dict(row, status='interrupted', success=False, error='Reserved before model invocation; completion not yet persisted'))
        trial = execute_trial(row, by_id[row['case_id']], sources.get(row['candidate']), keys[row['case_id']], budget)
        save_json(path, trial)
        print(json.dumps({'trial': row['id'], 'status': trial['status'], 'success': trial['success'],
                          'requests_used': budget.used, 'trials_reserved': ledger.used}), flush=True)
        return trial
    results = []
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        # Submit bounded batches so an infrastructure fault cannot launch the whole schedule.
        for offset in range(0, len(pending), jobs):
            batch = list(pool.map(run_one, pending[offset:offset + jobs]))
            results.extend(batch)
            incidents = [r for r in batch if r['status'] in {'infrastructure_error', 'interrupted', 'quota_truncated', 'previously_reserved_or_trial_cap'}]
            if incidents:
                save_json(RUN / 'incident.json', {'phase': phase, 'trials': [{'id': r['id'], 'status': r['status']} for r in incidents]})
                break
    return {'phase': phase, 'new_trials': len(results), 'requests_reserved': budget.used,
            'trials_reserved': ledger.used, 'development_gate': development_gate() if phase == 'development' else None}


def report() -> dict:
    _, sources, _ = load_inputs()
    rows = [json.loads(path.read_text()) for path in sorted((RUN / 'trials').glob('*.json'))]
    expected = [r for r in settings()['schedule'] if r['split'] == 'holdout']
    held = [r for r in rows if r['split'] == 'holdout']
    complete = ({r['id'] for r in expected} == {r['id'] for r in held} and
                all(r['status'] not in {'pending', 'interrupted', 'infrastructure_error', 'quota_truncated'} for r in held))
    value = summarize(rows, sources)
    if not complete:
        value['recommended_skill'] = None
        value['skill_improves_on_controls'] = False
    usage = Counter()
    requests = 0
    unknown_usage = 0
    for row in rows:
        for name in ('compiler', 'solver'):
            usage.update(request_usage(row.get(name)))
            for request in (row.get(name) or {}).get('requests', []):
                requests += 1
                unknown_usage += request.get('usage') is None
    value.update(complete_balanced_holdout=complete, usage=dict(usage), inference_requests_observed=requests,
                 requests_missing_usage=unknown_usage, requests_reserved=Budget(RUN / 'requests.json', 2000).used,
                 trials_reserved=TrialLedger(RUN / 'trial-ledger.json').used, development_gate=development_gate(),
                 dollar_cost=None, sources='../../sources.json', rows=rows)
    save_json(RUN / 'results.json', value)
    return {k: v for k, v in value.items() if k != 'rows'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['verify', 'dry-run', 'develop', 'recover-development', 'freeze', 'run', 'report'])
    parser.add_argument('--jobs', type=int, choices=[1, 2, 3], default=2)
    parser.add_argument('--development-round', type=int, choices=[1, 2], default=1)
    args = parser.parse_args()
    if args.action == 'verify':
        result = verify()
    elif args.action == 'dry-run':
        result = {'status': 'no_model_calls', **settings()}
    elif args.action == 'develop':
        result = execute('development', args.jobs, args.development_round)
    elif args.action == 'recover-development':
        result = recover_development()
    elif args.action == 'freeze':
        result = freeze_inputs()
    elif args.action == 'run':
        result = execute('holdout', args.jobs)
    else:
        result = report()
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
