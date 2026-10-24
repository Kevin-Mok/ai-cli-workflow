#!/usr/bin/env python3
"""Read native logs in place; emit aggregate candidate counts, never excerpts."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from codex_search_index import conversation_text, session_id, tool_strings, TOOL_EVENTS
from second_brain.session_digest_input import (
    MAX_LINE_BYTES, MAX_SOURCE_BYTES, PRIVATE_TOOL, PRIVATE_TOOL_NAME, PRIVATE_USE,
    epoch, helper_origin, private_tool, source_reader,
)


# Predeclared proxies: do not tune these expressions after inspecting the counts.
COMPLAINTS = {
    'repeated_approval': r"\b(?:why (?:do|are) you (?:keep )?ask(?:ing)?|stop asking|don'?t ask(?: me)?|do not ask(?: me)?)\b.{0,90}\b(?:permission|approval|confirm(?:ation)?)\b",
    'incomplete_scope': r"\byou (?:didn'?t|did not|haven'?t|have not|forgot to|missed|skipped|left out)\b.{0,80}\b(?:finish|complete|implement|fix|include|rest|all|whole|requirement|scope|step)\b|\b(?:finish|implement|do) (?:the rest|everything|all of it|the whole task)\b",
    'unsupported_completion': r"\byou (?:said|claimed|reported|called)\b.{0,70}\b(?:done|complete|fixed|passing|verified)\b.{0,100}\b(?:but|still|without|not)\b|\b(?:it'?s|it is|this is) (?:still )?(?:not|isn'?t) (?:fixed|working|complete)\b",
    'excessive_verbosity_or_cost': r"\b(?:your (?:reply|response|answer)|this|that|it) (?:is )?too (?:long|verbose|wordy|expensive)\b|\bwhy\b.{0,60}\b(?:so many tokens|so expensive|taking so long)\b|\bwast(?:e|ing)\b.{0,40}\b(?:tokens|time|money)\b",
    'overwritten_work': r"\byou (?:overwrote|deleted|discarded|reverted|lost|removed) (?:my|our|the existing|unrelated)\b|\b(?:my|our) (?:changes|work|edits)\b.{0,50}\b(?:gone|lost|overwritten|reverted)\b",
    'copy_paste': r"\bi (?:can'?t|cannot)\b.{0,30}\b(?:copy|paste)\b|\b(?:copy|paste)\b.{0,50}\b(?:broken|doesn'?t work|does not work|fails|extra line|wrap|newline)\b",
    'stale_context': r"\byou(?:'re| are) (?:still )?(?:using|following|working on)\b.{0,60}\b(?:old|stale|previous|wrong)\b.{0,30}\b(?:task|context|instructions|plan|request)\b|\b(?:that'?s|that is|this is) (?:the )?(?:old|previous|wrong) (?:task|context|request|plan)\b",
}
PATTERNS = {key: re.compile(value, re.I) for key, value in COMPLAINTS.items()}
CONTEXT = re.compile(r'(?im)^\s*(?:#\s*AGENTS(?:\.md)?\b|<(?:codex_internal_context|environment_context|user_instructions|developer_instructions|system_instructions|skills_instructions)\b)')
INSTRUCTION = re.compile(r'(?i)^\s*(?:add|write|create|record|use|include|update|make)\b.{0,70}\b(?:rule|instruction|policy|prompt|skill|test|example)\b')
TOOL_TAXONOMY = {
    'permission_or_read_only': r'permission denied|read.only file system|operation not permitted|access denied',
    'missing_resource': r'no such file|not found|does not exist|cannot find',
    'timeout': r'timed?\s*out|timeout',
    'network': r'connection refused|could not resolve|network (?:is )?unreachable|connection reset',
    'validation_or_assertion': r'assertionerror|syntaxerror|validationerror|failed? (?:test|assertion)|tests? failed|failures?=',
}
TOOL_PATTERNS = {key: re.compile(value, re.I) for key, value in TOOL_TAXONOMY.items()}
NONZERO = re.compile(r'(?i)(?:process exited with code|exit code\s*:|exit_code["\s:]+|exited with (?:status|code))\s*(-?\d+)')


def complaint_text(text):
    """Reject policy blobs; remove quoted/code spans before candidate matching."""
    if len(text) > 4000 or len(text.splitlines()) > 40 or CONTEXT.search(text) or INSTRUCTION.search(text):
        return ''
    text = re.sub(r'(?ms)^[ \t]*(```|~~~).*?(?:^[ \t]*\1[^\n]*(?:\n|$)|\Z)', '', text)
    text = re.sub(r'`[^`\n]*`|"[^"\n]*"|“[^”\n]*”', '', text)
    return '\n'.join(line for line in text.splitlines()
                     if not line.lstrip().startswith('>') and not line.startswith(('    ', '\t'))
                     and not (line.strip().startswith(("'", '‘')) and line.strip().endswith(("'", '’')))).strip()


def status_failure(value, depth=0):
    if depth > 24:
        return False
    if isinstance(value, str) and value.lstrip().startswith(('{', '[')):
        try:
            return status_failure(json.loads(value), depth + 1)
        except (ValueError, RecursionError):
            return False
    if isinstance(value, list):
        return any(status_failure(item, depth + 1) for item in value)
    if isinstance(value, dict):
        return (type(value.get('exit_code')) is int and value['exit_code'] != 0
                or value.get('isError') is True or value.get('is_error') is True
                or bool(value.get('error')) or bool(value.get('Err'))
                or any(status_failure(item, depth + 1) for item in value.values()))
    return False


def failed_tool(payload):
    """Recognize completion status; classify only into fixed, generic buckets."""
    text = '\n'.join(tool_strings(payload))
    failed = status_failure(payload) or any(int(match) != 0 for match in NONZERO.findall(text))
    if not failed:
        return None
    return next((key for key, expression in TOOL_PATTERNS.items() if expression.search(text)), 'other_or_unclassified')


def signature(metadata):
    return (metadata.st_dev, metadata.st_ino, metadata.st_size, metadata.st_mtime_ns, metadata.st_ctime_ns)


def scan_session(path, home, cutoff, end, progress):
    """Keep local tallies provisional until every source record is screened."""
    messages = defaultdict(lambda: {'event_msg': [], 'response_item': []})
    tools = []
    coverage = Counter()
    identity = None
    privacy = False
    with source_reader(path, home) as (stream, initial):
        if initial.st_size > MAX_SOURCE_BYTES:
            return {'excluded': 'oversized_source'}
        while raw := stream.readline(MAX_LINE_BYTES + 1):
            progress()
            if len(raw) > MAX_LINE_BYTES:
                return {'excluded': 'oversized_record'}
            if not raw.endswith(b'\n'):
                return {'excluded': 'incomplete_source'}
            if not raw.strip():
                continue
            try:
                record = json.loads(raw)
                if not isinstance(record, dict):
                    raise ValueError()
                kind, payload = record.get('type'), record.get('payload')
                if not isinstance(kind, str) or not isinstance(payload, dict):
                    raise ValueError()
                if kind in ('response_item', 'event_msg') and not isinstance(payload.get('type'), str):
                    raise ValueError()
            except (ValueError, TypeError, UnicodeError, RecursionError):
                return {'excluded': 'incomplete_source'}
            coverage['records'] += 1
            if kind == 'session_meta':
                if helper_origin(payload):
                    return {'excluded': 'helper_session'}
                current = session_id(payload.get('id'))
                if not current or identity and current != identity:
                    return {'excluded': 'invalid_session_metadata'}
                identity = current
            if kind in ('session_meta', 'turn_context') and PRIVATE_TOOL.search(str(payload.get('cwd', ''))):
                privacy = True
            ptype = payload.get('type')
            if kind == 'response_item' and ptype in ('function_call', 'custom_tool_call', 'local_shell_call', 'mcp_tool_call'):
                privacy |= private_tool(payload, tool_strings)
            if kind == 'event_msg' and ptype in TOOL_EVENTS:
                invocation = payload.get('invocation')
                identities = (payload, invocation) if isinstance(invocation, dict) else (payload,)
                privacy |= any(PRIVATE_TOOL_NAME.search(str(item.get(field, '')))
                               for item in identities for field in ('name', 'server', 'tool'))
                if ptype in ('exec_command_begin', 'mcp_tool_call_begin'):
                    privacy |= private_tool(payload, tool_strings)
            stamp = epoch(record.get('timestamp'))
            role, text = '', ''
            if kind == 'event_msg' and ptype in ('user_message', 'agent_message'):
                role = 'user' if ptype == 'user_message' else 'assistant'
                text = payload.get('message')
            elif kind == 'response_item' and ptype in ('message', 'agent_message'):
                role = payload.get('role') if ptype == 'message' else ('assistant' if payload.get('author') == '/root' else '')
                content = payload.get('content')
                if not isinstance(content, list):
                    return {'excluded': 'incomplete_source'}
                text = '\n'.join(item['text'] for item in content if isinstance(item, dict)
                                 and item.get('type') in ('input_text', 'output_text') and isinstance(item.get('text'), str))
            if isinstance(text, str) and PRIVATE_USE.search(conversation_text(role, text)):
                privacy = True
            if role == 'user' and isinstance(text, str):
                # Hashes and dates remain memory-only; use representation counts to
                # remove event/response mirrors while preserving actual repeats.
                digest = hashlib.sha256(text.encode()).digest()
                if not cutoff <= stamp <= end:
                    value = ('outside_window_user_messages', (), '')
                else:
                    cleaned = complaint_text(conversation_text(role, text))
                    matches = tuple(key for key, pattern in PATTERNS.items() if cleaned and pattern.search(cleaned))
                    value = ('eligible_user_messages' if cleaned else 'filtered_user_messages', matches,
                             datetime.fromtimestamp(stamp, timezone.utc).date().isoformat())
                messages[digest][kind].append(value)
            if cutoff <= stamp <= end and ((kind == 'event_msg' and ptype in ('exec_command_end', 'mcp_tool_call_end'))
                                          or (kind == 'response_item' and ptype in ('function_call_output', 'custom_tool_call_output', 'mcp_tool_call_output'))):
                if category := failed_tool(payload):
                    tools.append((category, datetime.fromtimestamp(stamp, timezone.utc).date().isoformat()))
        if signature(os.fstat(stream.fileno())) != signature(initial):
            return {'excluded': 'changed_during_read'}
        try:
            if signature(path.lstat()) != signature(initial):
                return {'excluded': 'changed_during_read'}
        except OSError:
            return {'excluded': 'changed_during_read'}
    if not identity:
        return {'excluded': 'invalid_session_metadata'}
    if privacy:
        return {'excluded': 'private_context'}
    complaints = defaultdict(list)
    for representations in messages.values():
        selected = max(representations.values(), key=len)
        coverage['mirrored_user_messages_removed'] += sum(map(len, representations.values())) - len(selected)
        for status, categories, date in selected:
            coverage[status] += 1
            for category in categories:
                complaints[category].append(date)
    return {'identity': identity, 'coverage': coverage, 'complaints': complaints, 'tools': tools}


def scan(home, *, now, days=60, progress=lambda: None):
    cutoff = (now - timedelta(days=days)).timestamp()
    end = now.timestamp()
    coverage = Counter({key: 0 for key in (
        'inventory_files', 'outside_window_files', 'candidate_files', 'screened_files',
        'eligible_sessions', 'records', 'eligible_user_messages', 'filtered_user_messages',
        'outside_window_user_messages', 'mirrored_user_messages_removed')})
    exclusions = Counter()
    seen = set()
    counts = Counter()
    sessions = Counter()
    dates = defaultdict(set)
    tools = Counter()
    tool_dates = defaultdict(set)
    tool_category_sessions = Counter()
    tool_sessions = 0
    source = home / 'sessions'
    if not source.is_dir():
        raise OSError('source unavailable')
    for path in sorted(source.rglob('*.jsonl')):
        progress()
        coverage['inventory_files'] += 1
        try:
            if path.lstat().st_mtime < cutoff:
                coverage['outside_window_files'] += 1
                continue
            coverage['candidate_files'] += 1
            result = scan_session(path, home, cutoff, end, progress)
        except (OSError, ValueError, RecursionError):
            result = {'excluded': 'unsafe_source'}
        coverage['screened_files'] += 1
        if reason := result.get('excluded'):
            exclusions[reason] += 1
            continue
        identity = result['identity']
        if identity in seen:
            exclusions['duplicate_session'] += 1
            continue
        seen.add(identity)
        coverage['eligible_sessions'] += 1
        coverage.update(result['coverage'])
        for category, occurrences in result['complaints'].items():
            counts[category] += len(occurrences)
            sessions[category] += 1
            dates[category].update(occurrences)
        for category, date in result['tools']:
            tools[category] += 1
            tool_dates[category].add(date)
        tool_category_sessions.update({category for category, _ in result['tools']})
        tool_sessions += bool(result['tools'])
    return {
        'schema_version': 1,
        'window': {'start_utc': datetime.fromtimestamp(cutoff, timezone.utc).isoformat(), 'end_utc': now.isoformat(), 'days': days},
        'coverage': dict(sorted(coverage.items())), 'exclusions': dict(sorted(exclusions.items())),
        'complaints': {category: {'messages': counts[category], 'sessions': sessions[category], 'dates': len(dates[category]),
                                 'frequent': sessions[category] >= 3 and len(dates[category]) >= 2} for category in COMPLAINTS},
        'tool_failures': {'candidates': sum(tools.values()), 'sessions': tool_sessions,
                          'taxonomy': {category: {'candidates': count, 'sessions': tool_category_sessions[category],
                                                  'dates': len(tool_dates[category])} for category, count in sorted(tools.items())}},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path.home() / '.codex', help='native Codex home; read-only')
    parser.add_argument('--days', type=int, default=60)
    parser.add_argument('--now', help='fixed UTC ISO timestamp for repeatable window bounds')
    parser.add_argument('--plain', action='store_true', help='ASCII progress output')
    args = parser.parse_args()
    try:
        now = datetime.fromisoformat(args.now.replace('Z', '+00:00')) if args.now else datetime.now(timezone.utc)
        if now.tzinfo is None or not 1 <= args.days <= 366:
            raise ValueError()
        now = now.astimezone(timezone.utc)
    except (ValueError, OverflowError):
        parser.error('use a timezone-aware --now and --days between 1 and 366')
    start = time.monotonic()
    last = start - 10

    def progress():
        nonlocal last
        current = time.monotonic()
        if current - last >= 10:
            prefix = '' if args.plain else '🔎 '
            print(f'{prefix}Screening native sessions in place; elapsed {current - start:.0f}s. No source text is exported.', file=sys.stderr, flush=True)
            last = current

    try:
        progress()
        report = scan(args.home, now=now, days=args.days, progress=progress)
    except (OSError, ValueError):
        print(('' if args.plain else '⚠️ ') + 'Scan unavailable; verify the native source directory and read access.', file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    print(('' if args.plain else '✅ ') + f"Screening complete: {report['coverage'].get('eligible_sessions', 0)} eligible sessions; elapsed {time.monotonic() - start:.0f}s.", file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
