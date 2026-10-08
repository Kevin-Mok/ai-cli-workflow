"""Incremental private Codex work digest, shared by scheduled and manual runs."""
from __future__ import annotations
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import textwrap
import stat
import tempfile

from .paths import state_root, ensure_private_directory, atomic_write, local_now, LockError, PathError
from .state_private import private_file_bytes
from .session_digest_input import parse, epoch, clean, native_titles
from .session_digest_runtime import infer, InferenceError, validate_summary

VERSION=1
STATE_VERSION=3
MAX_STATE=16*1024*1024
HEX=re.compile(r'[0-9a-f]{64}\Z')
STATUSES={'pending','ready','partial','stale','skipped','failed'}


def directory():
    root=state_root(require_repository=False)
    return root, root/'sessions'


@contextmanager
def lock():
    root,d=directory(); ensure_private_directory(d,require_repository=False)
    fd=os.open(d/'refresh.lock',os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
    try:
        meta=os.fstat(fd)
        if not stat.S_ISREG(meta.st_mode) or meta.st_uid!=os.geteuid() or meta.st_nlink!=1:
            raise PathError('unsafe session digest lock')
        os.fchmod(fd,0o600)
        try: fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: raise LockError('another session digest refresh is running') from None
        yield root,d
    finally: os.close(fd)


def empty():
    return {'schema_version':STATE_VERSION,'refreshed_at':None,'background_refreshed_at':None,'seen':{},'fingerprints':{},'screened':{},'summary_hashes':{},'sessions':{},'queue':[], 'coverage':{'skipped':0,'failed':0,'partial':0,'unknown':0,'stale':0},'error':None}


def load(root,d):
    data=private_file_bytes(root,d/'state.json',max_bytes=MAX_STATE)
    if data is None: return empty()
    try:
        v=json.loads(data)
        if isinstance(v,dict) and type(v.get('schema_version')) is int:
            legacy = set(empty()) - {'screened', 'summary_hashes', 'background_refreshed_at'}
            if v['schema_version'] == 1 and set(v) == legacy - {'fingerprints'}:
                v['fingerprints'] = {}
                v['schema_version'] = 2
            if v['schema_version'] == 2 and set(v) == legacy:
                v['screened'] = {}
                v['background_refreshed_at'] = v['refreshed_at']
                # v2 seen hashes could advance before inference succeeded. Only
                # reuse hashes still tied to a successful saved summary.
                v['summary_hashes'] = {
                    key: entry['hash'] for key, entry in v['sessions'].items()
                    if entry['summary'] is not None and entry['status'] in ('ready', 'partial')
                    and v['seen'].get(key) == entry['hash']
                }
                v['schema_version'] = STATE_VERSION
        if not isinstance(v,dict) or set(v)!=set(empty()) or type(v['schema_version']) is not int or v['schema_version']!=STATE_VERSION: raise ValueError()
        # Parser revisions invalidate only metadata screening, not successful
        # recap hashes or explicit check dispositions.
        if isinstance(v.get('screened'), dict):
            v['screened'] = {key: stamp for key, stamp in v['screened'].items()
                             if not (isinstance(stamp, list) and len(stamp) == 5)}
        for field in ('fingerprints', 'screened'):
            if not isinstance(v[field],dict) or len(v[field])>100000: raise ValueError()
            for key, stamp in v[field].items():
                if not isinstance(key,str) or not HEX.fullmatch(key) or not isinstance(stamp,list) or len(stamp)!=(6 if field == 'screened' else 5) or any(type(n) is not int or n<0 for n in stamp): raise ValueError()
        if not isinstance(v['summary_hashes'],dict) or len(v['summary_hashes'])>20000: raise ValueError()
        for key, digest in v['summary_hashes'].items():
            if not isinstance(key,str) or not HEX.fullmatch(key) or key not in v['sessions'] or not isinstance(digest,str) or not HEX.fullmatch(digest): raise ValueError()
        for field in ('refreshed_at', 'background_refreshed_at'):
            if v[field] is not None and (not isinstance(v[field],str) or not epoch(v[field])): raise ValueError()
        if not isinstance(v['seen'],dict) or not isinstance(v['sessions'],dict) or len(v['seen'])>100000 or len(v['sessions'])>20000: raise ValueError()
        for k,h in v['seen'].items():
            if not HEX.fullmatch(k) or not isinstance(h,str) or len(h)>100: raise ValueError()
        q=v['queue']
        if not isinstance(q,list) or len(q)!=len(set(q)) or any(not isinstance(k,str) or k not in v['sessions'] for k in q): raise ValueError()
        if v['error'] not in (None,'authentication','quota','timeout','isolation','invalid_summary','runtime','scan'): raise ValueError()
        if not isinstance(v['coverage'],dict) or any(type(n) is not int or n<0 for n in v['coverage'].values()): raise ValueError()
        for k,e in v['sessions'].items():
            if not HEX.fullmatch(k) or not isinstance(e,dict): raise ValueError()
            if set(e)!= {'key','source','id','title','cwd','last_activity','status','partial','hash','reason','summary','checks','summarized_at'} or e['key']!=k: raise ValueError()
            if any(not isinstance(e[x],str) or len(e[x])>8192 for x in ('source','id','title','cwd','last_activity','hash','reason')): raise ValueError()
            if e['status'] not in STATUSES or type(e['partial']) is not bool or not isinstance(e['checks'],list): raise ValueError()
            if e['summary'] is not None: e['summary']=validate_summary(e['summary'])
            if e['summarized_at'] is not None and (not isinstance(e['summarized_at'],str) or not epoch(e['summarized_at'])): raise ValueError()
            ids=set()
            for c in e['checks']:
                if not isinstance(c,dict) or set(c)!= {'id','key','text','disposition','resolved_at'}: raise ValueError()
                if not isinstance(c['id'],str) or not HEX.fullmatch(c['id']) or c['id'] in ids or not isinstance(c['key'],str) or not re.fullmatch('[a-z0-9][a-z0-9-]{0,79}',c['key']): raise ValueError()
                if c['id']!=check_id(k,c['key']) or not isinstance(c['text'],str) or len(c['text'])>1000 or c['disposition'] not in ('open','checked','dismissed'): raise ValueError()
                if c['resolved_at'] is not None and (not isinstance(c['resolved_at'],str) or not epoch(c['resolved_at'])): raise ValueError()
                ids.add(c['id']); c['text']=clean(c['text'])
        return v
    except (ValueError,TypeError,KeyError,AttributeError,UnicodeError,RecursionError):
        raise ValueError('invalid session digest state; preserve it and restore a validated backup') from None


def check_id(key,slug):
    return hashlib.sha256((key+'\0'+slug).encode()).hexdigest()


def report(v,calls=0,entries=None):
    if entries is None: entries=sorted(v['sessions'].values(),key=lambda e:(e['cwd'],e['last_activity'],e['key']))
    checks=[{**c,'session_key':e['key'],'session_id':e['id'],'project':e['cwd']} for e in entries for c in e['checks'] if c['disposition']=='open']
    return {'schema_version':VERSION,'refreshed_at':v['refreshed_at'],'pending_count':len(checks),'backlog_count':len(v['queue']),
            'model_calls':calls,'summary_updated_at':max((e['summarized_at'] for e in entries if e['summarized_at']),default=None),'coverage':dict(v['coverage']),'error':v['error'],'sessions':entries,'open_checks':checks}


def save(root,d,v):
    text=json.dumps(v,ensure_ascii=True,indent=2)+'\n'
    if len(text.encode())>=MAX_STATE: raise ValueError('session digest state exceeds limit')
    # Refuse unsafe preexisting files even though atomic replacement would not
    # follow a link; do not silently destroy a different owner's state.
    for name in ('state.json','digest.md'):
        private_file_bytes(root,d/name,max_bytes=MAX_STATE)
    old=private_file_bytes(root,d/'state.json',max_bytes=MAX_STATE)
    backup=None
    if old is not None:
        fd,name=tempfile.mkstemp(prefix='.rollback-',dir=d)
        backup=Path(name)
        with os.fdopen(fd,'wb') as stream:
            stream.write(old); stream.flush(); os.fsync(stream.fileno())
    try:
        atomic_write(d/'state.json',text,mode=0o600)
        try: atomic_write(d/'digest.md',render(report(v)),mode=0o600)
        except BaseException:
            if backup is not None: os.replace(backup,d/'state.json')
            else: (d/'state.json').unlink(missing_ok=True)
            raise
    finally:
        if backup is not None: backup.unlink(missing_ok=True)



def summarize(entry, dialogue):
    """Replace a recap while retaining explicitly recorded check dispositions."""
    key = entry['key']
    summary = validate_summary(infer(dialogue, [{'key': check['key'], 'text': check['text']} for check in entry['checks']]))
    existing = {check['key']: check for check in entry['checks']}
    for check in summary['checks']:
        normalized = ' '.join(check['text'].casefold().split())
        same = next((value for value in existing.values() if ' '.join(value['text'].casefold().split()) == normalized), None)
        if check['key'] not in existing and same is not None:
            check['key'] = same['key']
        if check['key'] in existing:
            existing[check['key']]['text'] = check['text']
        else:
            existing[check['key']] = {'id': check_id(key, check['key']), **check, 'disposition': 'open', 'resolved_at': None}
    summary['checks'] = list({check['key']: check for check in summary['checks']}.values())
    summary = validate_summary(summary)
    entry.update(summary=summary, checks=list(existing.values()), summarized_at=local_now().isoformat(),
                 status='partial' if entry['partial'] else 'ready', reason='')


def refresh(limit=20):
    """Discover metadata first; screen at most twenty queued changed sources."""
    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError('digest limit must be between 1 and 20')
    with lock() as (root, d):
        v = load(root, d)
        now = local_now()
        now_s = now.isoformat()
        cutoff = now.timestamp() - 7 * 86400
        home = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))).expanduser()
        if not home.is_absolute() or home.resolve() != home.absolute():
            raise PathError('CODEX_HOME must be an absolute physical directory')
        titles = native_titles(home)
        paths = {}
        source_keys = {entry['source']: key for key, entry in v['sessions'].items() if entry['source']}
        scan_failed = 0
        for folder in ('sessions', 'archived_sessions'):
            base = home / folder
            if base.is_symlink():
                scan_failed += 1
                continue
            if not base.exists():
                continue
            def onerror(error):
                nonlocal scan_failed
                scan_failed += 1
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
                        scan_failed += 1
                        continue
                    key = source_keys.get(str(path), hashlib.sha256(str(path.relative_to(home)).encode()).hexdigest())
                    fingerprint = [metadata.st_size, metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_dev, metadata.st_ino]
                    previous = v['fingerprints'].get(key)
                    known = key in v['seen'] or previous is not None
                    old = v['sessions'].get(key)
                    v['fingerprints'][key] = fingerprint
                    paths[key] = path
                    if (old is None or not known) and metadata.st_mtime < cutoff and (v['background_refreshed_at'] is None or (known and (previous is None or previous == fingerprint))):
                        continue
                    if old is None:
                        v['sessions'][key] = {
                            'key': key, 'source': clean(str(path)), 'id': '', 'title': '', 'cwd': '',
                            'last_activity': '', 'status': 'pending', 'partial': False, 'hash': '',
                            'reason': f'initial_candidate:{cutoff}' if v['background_refreshed_at'] is None else 'not_screened',
                            'summary': None, 'checks': [], 'summarized_at': None,
                        }
                    if old is None or previous != fingerprint or (old['status'] == 'failed' and key not in v['queue']):
                        if old is not None and old['status'] != 'skipped':
                            old.update(status='stale' if old['summary'] else 'pending', reason='changed_source')
                        if old is not None and not known and v['background_refreshed_at'] is None:
                            old['reason'] = f'initial_candidate:{cutoff}'
                        if key not in v['queue']:
                            v['queue'].append(key)
                    if old is not None and old['id'] and previous == fingerprint:
                        old['title'] = titles.get(old['id'], '')
        v['error'] = 'scan' if scan_failed else None
        for key, entry in v['sessions'].items():
            if key not in paths and entry['status'] != 'skipped':
                entry.update(status='stale', reason='source_unavailable')
        v['queue'] = [key for key in v['queue'] if key in paths]
        calls = 0
        for key in list(v['queue'])[:limit]:
            old = v['sessions'][key]
            v['screened'].pop(key, None)
            try:
                parsed = parse(paths[key], home)
            except (OSError, ValueError):
                old.update(status='failed', reason='scan')
                v['error'] = 'scan'
                v['queue'].remove(key)
                v['queue'].append(key)
                continue
            parsed['key'] = key
            dialogue = parsed.pop('dialogue')
            sid = parsed['id']
            parsed['title'] = titles.get(sid, '') if isinstance(sid, str) else ''
            parsed.update(summary=old['summary'], checks=old['checks'], summarized_at=old['summarized_at'])
            parsed.setdefault('reason', '')
            v['sessions'][key] = parsed
            entry = parsed
            if entry['status'] == 'skipped':
                if entry['reason'] in ('private_context', 'unsafe_source'):
                    entry.update(summary=None, checks=[], summarized_at=None)
                v['seen'][key] = entry['hash']
                v['queue'].remove(key)
                continue
            if old['reason'].startswith('initial_candidate:'):
                initial_cutoff = float(old['reason'].split(':', 1)[1])
                activity = epoch(entry['last_activity'])
                if activity and activity < initial_cutoff:
                    entry.update(status='skipped', reason='outside_initial_window')
                    v['seen'][key] = entry['hash']
                    v['queue'].remove(key)
                    continue
            if v['summary_hashes'].get(key) == entry['hash'] and entry['summary'] is not None and old['status'] != 'failed':
                entry.update(status='partial' if entry['partial'] else 'ready', reason='')
                v['queue'].remove(key)
                continue
            v['seen'][key] = entry['hash']
            calls += 1
            try:
                summarize(entry, dialogue)
                v['summary_hashes'][key] = entry['hash']
                v['queue'].remove(key)
            except (InferenceError, ValueError) as error:
                category = error.category if isinstance(error, InferenceError) else 'invalid_summary'
                entry.update(status='failed', reason=category)
                v['error'] = category
                v['queue'].remove(key)
                v['queue'].append(key)
                if category in ('authentication', 'quota', 'isolation'):
                    break
        v['refreshed_at'] = local_now().isoformat()
        v['background_refreshed_at'] = v['refreshed_at']
        v['coverage'] = {
            'skipped': sum(entry['status'] == 'skipped' for entry in v['sessions'].values()),
            'failed': scan_failed + sum(entry['status'] == 'failed' for entry in v['sessions'].values()),
            'partial': sum(entry['status'] == 'partial' for entry in v['sessions'].values()),
            'unknown': sum(entry['summary'] is None and entry['status'] != 'skipped' for entry in v['sessions'].values()),
            'stale': sum(entry['status'] == 'stale' or (bool(entry['last_activity']) and epoch(entry['last_activity']) < cutoff) for entry in v['sessions'].values()),
        }
        save(root, d, v)
        return report(v, calls)


def review(limit=None, refresh_limit=None, *, all_sessions=False):
    from .session_review import review as recent_review
    return recent_review(limit, refresh_limit, all_sessions=all_sessions)


def metadata():
    root,d=directory(); r=report(load(root,d))
    return {k:r[k] for k in ('refreshed_at','summary_updated_at','pending_count','backlog_count','coverage','error')}


def resolve(payload):
    if not isinstance(payload,dict) or set(payload)!= {'schema_version','check_id','disposition','confirmed'} or type(payload['schema_version']) is not int or payload['schema_version']!=VERSION or payload['confirmed'] is not True or payload['disposition'] not in ('checked','dismissed') or not isinstance(payload['check_id'],str) or not HEX.fullmatch(payload['check_id']):
        raise ValueError('resolve requires schema_version 1, check_id, checked/dismissed disposition and confirmed true')
    with lock() as (root,d):
        v=load(root,d)
        for e in v['sessions'].values():
            for c in e['checks']:
                if c['id']==payload['check_id']:
                    c.update(disposition=payload['disposition'],resolved_at=local_now().isoformat()); save(root,d,v)
                    return {'schema_version':VERSION,'check_id':c['id'],'disposition':c['disposition'],'pending_count':report(v)['pending_count']}
        raise ValueError('unknown digest check_id')


def render(r):
    lines=['# Private Codex work digest','', 'Conversation reports are not independent proof of implementation or completion.',
           f"Refreshed: {r.get('refreshed_at') or 'never'} | Open checks: {r.get('pending_count',0)} | Backlog: {r.get('backlog_count',0)}",'']
    if 'coverage' in r: lines.append('Coverage: '+', '.join(f'{k}={n}' for k,n in r['coverage'].items()))
    if r.get('error'): lines.append('Refresh issue: '+r['error'])
    cwd=None
    for e in r.get('sessions',[]):
        if cwd!=e['cwd']:
            cwd=e['cwd']; lines.extend(['', '## '+(cwd or 'Unknown project')])
        summary=e['summary']; lines.extend(['', '### '+(e['title'] or (summary['title']+' (inferred title)' if summary else 'Untitled session')),
           f"Session: {e['id'] or 'excluded'} | Last activity: {e['last_activity'] or 'unknown'} | Coverage: {e['status']} | Summarized: {e['summarized_at'] or 'never'}" ])
        if e['reason']: lines.append('Reason: '+e['reason'])
        if e['source']: lines.append('Source: '+e['source'])
        if e['id'] and re.fullmatch(r'[0-9a-fA-F-]{36}',e['id']) and isinstance(cwd,str) and cwd.startswith('/'):
            lines.append('Resume: '+shlex.join(['codex','-C',cwd,'resume',e['id']]))
        if summary:
            lines.append('Goal: '+summary['goal'])
            for field,label in (('intentions','Intentions'),('accomplishments','Reported accomplishments'),('remaining','Remaining work'),('blockers','Blockers'),('verification','Recorded verification reports')):
                lines.append(label+': '+('; '.join(summary[field]) or 'unknown / none reported'))
        for c in e['checks']:
            if c['disposition']=='open': lines.append(f"- Check [{c['id']}]: {c['text']}")
    if r.get('pending_count'): lines.extend(['','Which outstanding check would you like to handle?'])
    return '\n'.join(lines)+'\n'


def render_terminal(r, width=None, *, plain=False):
    from .session_review import render_terminal as render_recent
    return render_recent(r, width, plain=plain)
