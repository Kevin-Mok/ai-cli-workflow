#!/usr/bin/env python3
"""Preview or apply one shortcut request, without evaluating its command."""
from __future__ import annotations

import argparse
import difflib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import shutil
import textwrap
from typing import TypedDict, cast

SOURCES = {'commands': 'key_aliases.tmpl', 'dirs': 'key_dirs.tmpl', 'files': 'key_files.tmpl'}

class Entry(TypedDict):
    index: int
    key: str
    value: str
    section: str
    active: bool


def strip_comment(text: str) -> str:
    quote = ''
    escape = False
    for i, char in enumerate(text):
        if escape:
            escape = False
        elif char == '\\' and quote != "'":
            escape = True
        elif quote:
            if char == quote: quote = ''
        elif char in "\"'": quote = char
        elif char == '#' and (i == 0 or text[i-1].isspace()): return text[:i].rstrip()
    return text.rstrip()


def logical(value: str) -> str:
    value = strip_comment(value)
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return re.sub(r'\\([\\"$])', r'\1', value[1:-1])
    if len(value) >= 2 and value[0] == value[-1] == "'": return value[1:-1]
    return value


def fish_name(kind: str, key: str) -> str:
    return ('n' if kind == 'files' else '') + key


def entries(text: str) -> list[Entry]:
    found: list[Entry] = []
    sections: list[str] = []
    for index, line in enumerate(text.splitlines(keepends=True)):
        start = re.match(r'^\s*#\s*(.*?)\s*\[\[\[', line)
        if start: sections.append(start.group(1).strip())
        if re.match(r'^\s*#\s*\]\]\]', line):
            if sections: _ = sections.pop()
        if not line.strip() or line.lstrip().startswith(('#', '{{')): continue
        match = re.match(r'^\s*(\S+)\s+(.+?)\s*$', line)
        if not match: raise ValueError(f'Unsupported shortcut line {index+1}; inspect it before editing')
        found.append({'index': index, 'key': match[1], 'value': strip_comment(match[2]),
                      'section': sections[-1] if sections else '', 'active': False})
    return found


def activate(text: str, found: list[Entry]) -> None:
    """Render marker lines in the same branches as definitions; no shell evaluation."""
    lines = text.splitlines(keepends=True)
    by_index = {e['index']: e for e in found}
    annotated = ''.join(f'# fish-alias-active:{i}\n' + line if i in by_index else line
                        for i, line in enumerate(lines))
    render = subprocess.run(['chezmoi', 'execute-template'], input=annotated,
                            text=True, capture_output=True, check=False)
    if render.returncode:
        raise ValueError('chezmoi template rendering failed: ' + render.stderr.strip())
    active_indices = {int(m[1]) for m in re.finditer(r'^# fish-alias-active:(\d+)$', render.stdout, re.M)}
    for entry in found: entry['active'] = entry['index'] in active_indices


def path_literal(target: str) -> str:
    # Quoted/escaped shell path expressions are already intentional user text.
    if target.startswith(('"', "'")) or '\\' in target: return target
    return re.sub(r'([\s"\'()&;|<>$`#*?\[\]{}])', r'\\\1', target)


def route(target: str, root: Path, override: str | None) -> str:
    if override:
        if override not in SOURCES: raise ValueError('kind must be commands, dirs or files')
        return override
    # A quoted command is still a command. Only path-shaped single values route as paths.
    plain = target
    words: list[str] = []
    try:
        words = shlex.split(target)
        if len(words) == 1: plain = words[0]
    except ValueError as error:
        raise ValueError('Unbalanced quoting; clarify the intended command/path') from error
    candidate = Path(os.path.expanduser(plain))
    if not candidate.is_absolute(): candidate = root / candidate
    if len(words) > 1 and not candidate.exists():
        return 'commands'
    path_shaped = plain.startswith(('/', '~/', './', '../')) or candidate.exists() or bool(Path(plain).suffix)
    if not path_shaped: return 'commands'
    if candidate.is_dir() or plain.endswith('/'): return 'dirs'
    if candidate.is_file() or Path(plain).suffix: return 'files'
    raise ValueError('Ambiguous path: ask whether this is a directory or file, then pass kind')


def choose_section(kind: str, target: str, found: list[Entry], override: str | None) -> str:
    available = list(dict.fromkeys(e['section'] for e in found if e['section']))
    if override:
        if override not in available: raise ValueError('section must name an existing section')
        return override
    scores = {section: 0 for section in available}
    if kind == 'commands':
        family = target.split()[0]
        for entry in found:
            head = logical(entry['value']).split()[0]
            # codex-time and codex-search belong to the same executable family as codex.
            if head == family or head.split('-')[0] == family.split('-')[0]:
                scores[entry['section']] = scores.get(entry['section'], 0) + 10
    else:
        plain = logical(target)
        for entry in found:
            common = os.path.commonprefix([plain, logical(entry['value'])])
            scores[entry['section']] = max(scores.get(entry['section'], 0), common.rfind('/') + 1)
    if not scores: raise ValueError('No existing sections found; inspect the template before editing')
    # Preserve existing section order when related entries tie. Preview makes the choice reviewable.
    return max(scores, key=lambda section: scores[section])


def insertion(lines: list[str], section: str) -> int:
    stack: list[str] = []
    depth = 0
    for i, line in enumerate(lines):
        start = re.match(r'^\s*#\s*(.*?)\s*\[\[\[', line)
        if start: stack.append(start.group(1).strip())
        if '{{' in line:
            directives = re.finditer(r'{{-?\s*(.*?)\s*-?}}', line)
            for match in directives:
                directive = match[1]
                if directive.startswith(('if ', 'range ', 'with ')): depth += 1
                elif directive == 'end': depth -= 1
            if depth < 0: raise ValueError('Unbalanced template controls')
        if re.match(r'^\s*#\s*\]\]\]', line):
            if stack and stack[-1] == section:
                if depth: raise ValueError('Section ends inside a condition; choose a safe section manually')
                return i
            if stack: _ = stack.pop()
    raise ValueError('No matching section end; inspect markers before editing')


def update(root: Path, request: dict[str, str], apply: bool) -> dict[str, object]:
    raw = request.get('input', '')
    if any(c in raw for c in '\r\n\0'):
        raise ValueError('Provide one single-line abbreviation and command/path')
    match = re.match(r'^\s*(\S+)\s+(.+?)\s*$', raw)
    if not match: raise ValueError('Missing abbreviation or command/path; ask for the missing input')
    key, target = match[1], match[2]
    if '{{' in raw or '}}' in raw:
        raise ValueError('Template delimiters require manual literal escaping; request was not rendered')
    if not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.-]*', key): raise ValueError('Unsafe abbreviation')
    kind = route(target, root, request.get('kind'))
    texts: dict[str, str] = {}
    parsed: dict[str, list[Entry]] = {}
    paths = {k: root / 'aliases' / name for k, name in SOURCES.items()}
    for source_kind, path in paths.items():
        if path.is_symlink() or not path.is_file(): raise ValueError('Shortcut sources must be regular files')
        texts[source_kind] = path.read_text()
        parsed[source_kind] = entries(texts[source_kind])
        activate(texts[source_kind], parsed[source_kind])
    section = choose_section(kind, target, parsed[kind], request.get('section'))
    effective = fish_name(kind, key)
    conflicts = [(k, e) for k, group in parsed.items() for e in group
                 if e['active'] and fish_name(k, e['key']) == effective]
    def normalized(value: str) -> str:
        if kind == 'commands': return logical(value)
        try:
            parts = shlex.split(value)
            return parts[0] if len(parts) == 1 else value
        except ValueError: return value
    identical = next((e for k, e in conflicts if k == kind and normalized(e['value']) == normalized(target)), None)
    after = dict(texts)
    for source_kind, text in texts.items():
        lines = text.splitlines(keepends=True)
        for k, entry in conflicts:
            if k == source_kind and entry is not identical:
                lines[entry['index']] = '# ' + lines[entry['index']]
        if source_kind == kind and identical is None:
            value = target
            if kind == 'commands':
                value = '"' + re.sub(r'([\\"$])', r'\\\1', target) + '"'
            else: value = path_literal(target)
            lines.insert(insertion(lines, section), f'{key} {value}\n')
        after[source_kind] = ''.join(lines)
    # Validate all proposed template structures before any write.
    for source_kind in SOURCES:
        if after[source_kind] != texts[source_kind]: activate(after[source_kind], entries(after[source_kind]))
    diffs = ''.join(''.join(difflib.unified_diff(texts[k].splitlines(True), after[k].splitlines(True),
                   fromfile=str(paths[k]), tofile=str(paths[k]))) for k in SOURCES)
    if apply:
        for k, path in paths.items():
            if path.read_text() != texts[k]: raise ValueError('Sources changed concurrently; rerun preview')
        for k, path in paths.items():
            if after[k] != texts[k]: _ = path.write_text(after[k])
    return {'kind': kind, 'section': identical['section'] if identical else section,
            'fish_name': effective, 'target': target, 'changed': bool(diffs), 'applied': apply,
            'diff': diffs, 'conflicts': len(conflicts) - (1 if identical else 0)}


class Options(argparse.Namespace):
    repo: Path = Path('/home/example/linux-config')
    apply: bool = False
    json: bool = False
    plain: bool = False
    details: bool = False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument('--repo', type=Path, default=Path('/home/example/linux-config'))
    _ = parser.add_argument('--apply', action='store_true', help='Write after validating; default previews only')
    _ = parser.add_argument('--json', action='store_true', help='Export clean JSON including the proposed diff')
    _ = parser.add_argument('--plain', action='store_true', help='Use ASCII output')
    _ = parser.add_argument('--details', action='store_true', help='Include the source diff and error evidence')
    args = parser.parse_args(namespace=Options())
    try:
        decoded: object = cast(object, json.load(sys.stdin))
        if not isinstance(decoded, dict):
            raise ValueError('Expected JSON object with string fields')
        fields = cast(dict[object, object], decoded)
        request: dict[str, str] = {}
        for key, value in fields.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValueError('Expected JSON object with string fields')
            request[key] = value
        result = update(args.repo, request, args.apply)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            title = ('Applied' if args.apply else 'Preview') if result['changed'] else 'Already present'
            print(('' if args.plain else '🐟 ') + 'Fish shortcut — ' + title if not args.plain else 'Fish shortcut - ' + title)
            width = max(20, shutil.get_terminal_size().columns)
            for label, value in [('Source', SOURCES[kind] if isinstance((kind := result['kind']), str) else ''),
                                 ('Section', result['section']), ('Fish name', result['fish_name']),
                                 ('Target', result['target']), ('Conflicts', result['conflicts'])]:
                print(textwrap.fill(f'{label:<10} {value}', width=width, subsequent_indent='           '))
            print('Conditions follow the current host; inactive definitions remain unchanged.')
            if args.details: print(result['diff'])
        return 0
    except (ValueError, OSError) as error:
        print(f'fish-alias: {error}' if args.details else 'fish-alias: cannot safely edit this request; check input/path type or use --details.', file=sys.stderr)
        return 2

if __name__ == '__main__': raise SystemExit(main())
