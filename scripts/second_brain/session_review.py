"""Discover recent safe conversations independently of the background queue."""
from __future__ import annotations

from datetime import datetime
import hashlib
import os
from pathlib import Path
import re
import shutil
import stat
import shlex
import unicodedata
from zoneinfo import ZoneInfo

from . import sessions
from .session_digest_input import clean, epoch, native_titles, parse
from .paths import PathError, local_now
from .session_digest_runtime import InferenceError

TORONTO = ZoneInfo('America/Toronto')
LEGACY_HELPER = re.compile(r'^(?:guardian\s+review\b|(?:spawned\s+)?(?:subagent|helper)(?:\s+session|\s+agent)?\s*(?:$|[:/—-]))', re.I)


def fingerprint(metadata):
    return [2, metadata.st_size, metadata.st_mtime_ns, metadata.st_ctime_ns,
            metadata.st_dev, metadata.st_ino]


def source_paths(home, v):
    """Inventory physical owned files; the parser anchors subsequent reads."""
    paths = {}
    source_keys = {entry['source']: key for key, entry in v['sessions'].items() if entry['source']}
    failed = 0
    def onerror(error):
        nonlocal failed
        failed += 1
    for folder in ('sessions', 'archived_sessions'):
        base = home / folder
        if base.is_symlink():
            failed += 1
            continue
        if not base.exists():
            continue
        for dirname, dirs, files in os.walk(base, followlinks=False, onerror=onerror):
            dirs[:] = [name for name in dirs if not (Path(dirname) / name).is_symlink()]
            for name in sorted(files):
                if not name.endswith('.jsonl'):
                    continue
                path = Path(dirname) / name
                try:
                    metadata = path.lstat()
                    if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1 or metadata.st_uid != os.geteuid():
                        raise OSError('unsafe source')
                except OSError:
                    failed += 1
                    continue
                key = source_keys.get(str(path), hashlib.sha256(str(path.relative_to(home)).encode()).hexdigest())
                paths[key] = (path, fingerprint(metadata))
    return paths, failed


def discard_queue(v, key):
    if key in v['queue']:
        v['queue'].remove(key)


def screen(v, key, path, stamp, home, titles, current_sources=None):
    """Refresh metadata without asserting that an older recap is fresh."""
    old = v['sessions'].get(key)
    entry = parse(path, home, exclude_helpers=True)
    if old is None and entry['id'] and current_sources is not None:
        # Archiving changes the source pathname, not conversation identity.
        # Keep the original state key so persisted check IDs remain valid.
        prior = next((value for value in v['sessions'].values()
                      if value['id'] == entry['id'] and value['source'] not in current_sources), None)
        if prior is not None:
            key, old = prior['key'], prior
    entry['key'] = key
    dialogue = entry.pop('dialogue')
    entry.update(title='', summary=None, checks=[], summarized_at=None)
    entry.setdefault('reason', '')
    if entry['status'] == 'skipped':
        # Unscreenable sources must not display a cached title/recap. Keep old
        # dispositions privately for transient size/read failures only.
        if old and entry['reason'] not in ('private_context', 'unsafe_source', 'helper_session'):
            entry.update(summary=old['summary'], checks=old['checks'], summarized_at=old['summarized_at'])
        else:
            v['summary_hashes'].pop(key, None)
        discard_queue(v, key)
    else:
        entry['title'] = titles.get(entry['id'], '')
        if old:
            entry.update(summary=old['summary'], checks=old['checks'], summarized_at=old['summarized_at'])
        fresh = entry['summary'] is not None and v['summary_hashes'].get(key) == entry['hash']
        entry.update(status=('partial' if entry['partial'] else 'ready') if fresh else ('stale' if entry['summary'] else 'pending'),
                     reason='' if fresh else ('changed_source' if entry['summary'] else 'not_summarized'))
        if fresh:
            discard_queue(v, key)
    v['sessions'][key] = entry
    # The complete signature catches same-size rewrites with restored mtime.
    # Never cache a parse if its pathname changed while it was being read.
    try:
        stable = stamp == fingerprint(path.lstat()) and entry['reason'] != 'changed_during_read'
    except OSError:
        stable = False
    if stable:
        v['screened'][key] = stamp
    else:
        v['screened'].pop(key, None)
        entry.update(status='stale' if entry['summary'] else 'pending', reason='changed_during_read')
    return entry, dialogue


def eligible(entry):
    summary = entry['summary']
    title = entry['title'] or (summary['title'] if summary else '')
    return bool(entry['id']) and entry['status'] != 'skipped' and not LEGACY_HELPER.search(' '.join(title.split()))


def select(v, paths, limit):
    entries = [entry for key, entry in v['sessions'].items()
               if key in paths and v['screened'].get(key) == paths[key][1] and eligible(entry)]
    entries.sort(key=lambda entry: (-epoch(entry['last_activity']), entry['id'], entry['key']))
    unique = {}
    for entry in entries:
        unique.setdefault(entry['id'], entry)
    directories = {}
    for entry in unique.values():
        directories.setdefault(entry['cwd'], []).append(entry)
    selected = list(directories.values())[:limit]
    # --all preserves complete eligible history. Ordinary review caps each
    # directory at three sessions; insertion order follows its latest activity.
    return [entry for group in selected for entry in (group if limit is None else group[:3])]


def discover(v, home, titles):
    paths, scan_failed = source_paths(home, v)
    current_sources = {str(path) for path, stamp in paths.values()}
    for key, (path, stamp) in list(paths.items()):
        entry = v['sessions'].get(key)
        if entry is not None and v['screened'].get(key) == stamp:
            if entry['status'] != 'skipped':
                entry['title'] = titles.get(entry['id'], '')
            continue
        try:
            screened, _ = screen(v, key, path, stamp, home, titles, current_sources)
            if screened['key'] != key:
                paths[screened['key']] = paths.pop(key)
        except (OSError, ValueError):
            scan_failed += 1
            v['screened'].pop(key, None)
            if entry is not None:
                entry.update(status='failed', reason='scan')
    for key, entry in v['sessions'].items():
        if key not in paths:
            v['screened'].pop(key, None)
            if entry['status'] != 'skipped':
                entry.update(status='stale', reason='source_unavailable')
    v['queue'] = [key for key in v['queue'] if key in paths]
    return paths, scan_failed


def review(limit=None, refresh_limit=None, *, all_sessions=False):
    if limit is not None and (type(limit) is not int or not 1 <= limit <= 20):
        raise ValueError('review limit must be between 1 and 20')
    if type(all_sessions) is not bool or (all_sessions and limit is not None):
        raise ValueError('--all cannot be combined with an explicit display limit')
    display_limit = None if all_sessions else (5 if limit is None else limit)
    budget = refresh_limit if refresh_limit is not None else min((display_limit or 20) * 3, 20)
    if type(budget) is not int or not 0 <= budget <= 20:
        raise ValueError('review refresh limit must be between 0 and 20')
    with sessions.lock() as (root, directory):
        v = sessions.load(root, directory)
        home = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))).expanduser()
        if not home.is_absolute() or home.resolve() != home.absolute():
            raise PathError('CODEX_HOME must be an absolute physical directory')
        titles = native_titles(home)
        paths, scan_failed = discover(v, home, titles)
        v['error'] = 'scan' if scan_failed else None
        selected = select(v, paths, display_limit)
        calls = 0
        for entry in sorted(selected, key=lambda entry: (-epoch(entry['last_activity']), entry['id'], entry['key'])):
            key = entry['key']
            if entry['summary'] is not None and v['summary_hashes'].get(key) == entry['hash']:
                continue
            if calls >= budget:
                break
            path, stamp = paths[key]
            try:
                # No transcript is retained in the metadata cache. Re-screen
                # selected input before inference, including privacy changes.
                entry, dialogue = screen(v, key, path, stamp, home, titles)
                if not eligible(entry) or v['screened'].get(key) != stamp:
                    continue
                calls += 1
                sessions.summarize(entry, dialogue)
                v['summary_hashes'][key] = entry['hash']
                v['seen'][key] = entry['hash']
                discard_queue(v, key)
            except (InferenceError, ValueError, OSError) as error:
                category = error.category if isinstance(error, InferenceError) else ('scan' if isinstance(error, OSError) else 'invalid_summary')
                entry.update(status='failed', reason=category)
                v['error'] = category
                if category in ('authentication', 'quota', 'isolation'):
                    break
        # Model calls can take minutes. Revalidate cached entries before they
        # enter any output: a conversation may have become private meanwhile.
        paths, final_scan_failed = discover(v, home, native_titles(home))
        scan_failed = max(scan_failed, final_scan_failed)
        if scan_failed and v['error'] is None:
            v['error'] = 'scan'
        selected = select(v, paths, display_limit)
        v['refreshed_at'] = local_now().isoformat()
        all_entries = list(v['sessions'].values())
        v['coverage'] = {
            'skipped': sum(entry['status'] == 'skipped' for entry in all_entries),
            'failed': scan_failed + sum(entry['status'] == 'failed' for entry in all_entries),
            'partial': sum(entry['status'] == 'partial' for entry in all_entries),
            'unknown': sum(entry['summary'] is None and entry['status'] != 'skipped' for entry in all_entries),
            'stale': sum(entry['status'] == 'stale' for entry in all_entries),
            'hidden': len(all_entries) - len(selected),
            'restricted': sum(entry['reason'] == 'private_context' for entry in all_entries),
        }
        sessions.save(root, directory, v)
        return sessions.report(v, calls, entries=selected)


def activity_label(value):
    timestamp = epoch(value)
    if not timestamp:
        return 'Activity unknown'
    local = datetime.fromtimestamp(timestamp, TORONTO)
    return f"{local:%b} {local.day}, {local.year} at {local.strftime('%I:%M %p %Z').lstrip('0')}"


def next_step(entry):
    summary = entry['summary']
    if not summary:
        return ''
    remaining = summary.get('remaining', [])
    if remaining:
        return remaining[0]
    current = {check['key'] for check in summary.get('checks', [])}
    return next((check['text'] for check in entry['checks']
                 if check['key'] in current and check['disposition'] == 'open'), '')


def render_terminal(report, width=None, *, plain=False):
    """Render the complete selected report for a terminal, without Markdown."""
    plain = plain or os.environ.get("CLI_PLAIN") == "1"
    width = max(40, min(88, width if width is not None else shutil.get_terminal_size((88, 24)).columns))
    lines = []

    def cells(text):
        total = 0
        previous = 0
        for char in text:
            if char == '\ufe0f':
                # VS16 promotes a text-width symbol (e.g. sun) to emoji width.
                total += int(previous == 1)
            elif unicodedata.combining(char) or char == '\ufe0e':
                continue
            else:
                previous = 2 if unicodedata.east_asian_width(char) in ('W', 'F') else 1
                total += previous
        return total

    def add(text, prefix=''):
        # Preserve spaces in quoted paths/commands while removing terminal controls.
        text = re.sub(r'[\n\t\r]', ' ', clean(str(text))).strip()
        if plain:
            text = text.encode('ascii', errors='backslashreplace').decode()
        continuation = ' ' * cells(prefix)
        line = prefix
        spacing = ''
        for token in re.findall(r' +|[^ ]+', text):
            if token.isspace():
                spacing = token
                continue
            if cells(line + spacing + token) <= width:
                line += spacing + token
            else:
                if line != prefix and line != continuation:
                    lines.append(line.rstrip())
                    line = continuation
                for char in re.findall(r'.[\ufe0e\ufe0f]?', token):
                    if cells(line + char) > width:
                        lines.append(line)
                        line = continuation
                    line += char
            spacing = ''
        lines.append(line.rstrip())

    def section(label, emoji):
        lines.append('')
        add(label + ':', prefix='      ' + ('' if plain else emoji + ' '))

    def field(label, value):
        add(value, prefix=f'      {label + ":":<15} ')

    def items(label, emoji, values):
        section(label, emoji)
        for value in values or ['None reported.']:
            add(value, prefix='        - ' if plain else '        • ')

    def checks(label, values):
        if not values:
            return
        section(label, '☑')
        for check in values:
            disposition = check['disposition'].capitalize()
            add(disposition + ' · ' + check['text'] if not plain else
                disposition + ' - ' + check['text'], prefix='        ')
            add(check['id'], prefix='          ID: ')
            if check.get('resolved_at'):
                add(activity_label(check['resolved_at']), prefix='          Resolved: ')

    add('Recent work directories' if plain else '🗂️ Recent work directories')
    add('Conversation reports; not independently verified.')
    coverage = report.get('coverage', {})
    if coverage.get('restricted'):
        add('Private or uncertain sessions are excluded; recent work may be incomplete.',
            prefix='' if plain else '⚠ ')

    def render_entry(number, entry):
        summary = entry['summary']
        title = entry['title'] or (summary['title'] if summary else 'Untitled session')
        add(title, prefix=f'   {number}. ' + ('' if plain else '💬 '))
        add(activity_label(entry['last_activity']), prefix='      ' + ('' if plain else '🕒 '))
        if entry['status'] in ('failed', 'stale'):
            label = 'Recap stale' if summary else 'Recap unavailable'
            add(label + ': ' + (entry['reason'] or entry['status']).replace('_', ' '),
                prefix='      ' if plain else '      ⚠ ')
        if entry.get('partial', entry['status'] == 'partial'):
            add('Recap based on partial conversation.', prefix='      ' if plain else '      ⚠ ')
        if summary:
            section('Goal', '🎯')
            add(summary['goal'], prefix='        ')
            items('Intentions', '🧭', summary.get('intentions', []))
            items('Recap', '📝', summary.get('accomplishments', []))
            step = next_step(entry)
            if step:
                lines.append('')
                add(step, prefix='      Next: ' if plain else '      🔜 Next: ')
            items('Remaining work', '📌', summary.get('remaining', []))
            items('Blockers', '🚧', summary.get('blockers', []))
            items('Verification reports', '🧪', summary.get('verification', []))
        else:
            lines.append('')
            add('Recap not generated.', prefix='      ' if plain else '      📝 ')

        current = {check['key'] for check in summary.get('checks', [])} if summary else set()
        checks('Current checks', [check for check in entry['checks'] if check['key'] in current])
        checks('Earlier checks', [check for check in entry['checks'] if check['key'] not in current])
        if not entry['checks']:
            section('Checks', '☑')
            add('None reported.', prefix='        ')
        section('Session details', '🔎')
        statuses = {'ready': 'Recap current', 'partial': 'Partial conversation',
                    'pending': 'Recap pending', 'stale': 'Recap stale',
                    'failed': 'Refresh failed'}
        field('Status', statuses.get(entry['status'], entry['status'].replace('_', ' ')))
        field('Summarized', activity_label(entry['summarized_at']) if entry.get('summarized_at') else 'Never')
        if summary and summary['title'] != title:
            field('Recap title', summary['title'])
        field('Session', entry['id'] or 'Unavailable')
        if entry.get('reason'):
            field('Reason', entry['reason'].replace('_', ' '))
        field('Source', entry.get('source') or 'Unavailable')
        cwd = entry['cwd']
        if entry['id'] and re.fullmatch(r'[0-9a-fA-F-]{36}', entry['id']) and isinstance(cwd, str) and cwd.startswith('/'):
            field('Resume', shlex.join(['codex', '-C', cwd, 'resume', entry['id']]))

    groups = {}
    for entry in report.get('sessions', []):
        groups.setdefault(entry['cwd'], []).append(entry)
    for directory_number, (cwd, entries) in enumerate(groups.items(), 1):
        lines.extend(['', ('-' if plain else '─') * width])
        add(cwd or 'Unknown directory', prefix=f'{directory_number}. ' + ('' if plain else '📁 '))
        lines.append('')
        for number, entry in enumerate(entries, 1):
            if number > 1:
                lines.extend(['', '   ' + ('-' if plain else '─') * (width - 3), ''])
            render_entry(number, entry)
    if not report.get('sessions'):
        lines.append('')
        add('No work sessions available.')
    lines.extend(['', ('-' if plain else '─') * width])
    add('Review coverage' if plain else '📊 Review coverage')
    field('Displayed', f"{len(groups)} directories · {len(report.get('sessions', []))} sessions" if not plain else
          f"{len(groups)} directories / {len(report.get('sessions', []))} sessions")
    field('Reviewed', activity_label(report['refreshed_at']) if report.get('refreshed_at') else 'Never')
    field('Latest recap', activity_label(report['summary_updated_at']) if report.get('summary_updated_at') else 'Never')
    field('Open checks', report.get('pending_count', 0))
    field('Queued', report.get('backlog_count', 0))
    field('Model calls', report.get('model_calls', 0))
    for key, count in coverage.items():
        field(key.replace('_', ' ').capitalize(), count)
    if report.get('error'):
        field('Refresh issue', report['error'].replace('_', ' '))
    return '\n'.join(lines) + '\n'
