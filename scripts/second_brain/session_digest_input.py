"""Read native Codex sessions without persisting transcripts or private context."""
from __future__ import annotations
import hashlib
import importlib
import json
from pathlib import Path
import re
import os
import stat
from contextlib import contextmanager
from datetime import datetime

from .content_security import redact

MAX_SOURCE_BYTES = 64 * 1024 * 1024
MAX_LINE_BYTES = 2 * 1024 * 1024
INPUT_BYTES = 32768
PRIVATE_USE = re.compile(r'(?i)(\$personal-context\b|/personal-context\b|\b(?:use|using|invoke|invoking|run|running)\s+(?:the\s+)?(?:`|\$)?personal-context\b)')
PRIVATE_TOOL = re.compile(r'(?i)(personal[-_]context|/coding/personal-context)')


def clean(value: str) -> str:
    return ''.join(c for c in redact(value) if c in '\n\t' or c.isprintable()).encode('utf-8',errors='replace').decode()


def epoch(value: object) -> float:
    try:
        if not isinstance(value,str): return 0
        d=datetime.fromisoformat(value.replace('Z','+00:00'))
        return d.timestamp() if d.tzinfo else 0
    except (ValueError,OverflowError,OSError): return 0


@contextmanager
def source_reader(path: Path, home: Path):
    """Anchor every component; FIFOs, links and replaced parents cannot escape."""
    descriptors=[]
    flags=os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW
    try:
        current=os.open(home,flags); descriptors.append(current)
        parts=path.relative_to(home).parts
        if not parts or any(p in ('.','..') for p in parts): raise OSError('unsafe source path')
        for part in parts[:-1]:
            current=os.open(part,flags,dir_fd=current); descriptors.append(current)
        fd=os.open(parts[-1],os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=current)
        descriptors.append(fd); metadata=os.fstat(fd)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink!=1 or metadata.st_uid!=os.geteuid():
            raise OSError('unsafe source file')
        with os.fdopen(os.dup(fd),'rb') as stream: yield stream,metadata
    finally:
        for fd in reversed(descriptors): os.close(fd)


def helper_origin(payload: dict) -> bool:
    """Recognize native helper origins without consulting conversation text."""
    if payload.get('parent_thread_id') or payload.get('parent_session_id'):
        return True
    def helper(value):
        if isinstance(value, dict):
            return any(helper(key) or helper(item) for key, item in value.items())
        if isinstance(value, (list, tuple)):
            return any(helper(item) for item in value)
        if isinstance(value, str):
            return bool(re.search(r'(^|[^a-z])(subagent|guardian|thread_spawn)([^a-z]|$)', value.casefold()))
        return False
    return any(helper(payload.get(field)) for field in ('source', 'thread_source', 'originator'))


def parse(path: Path, home: Path, *, exclude_helpers=False) -> dict[str, object]:
    """Screen every record before building bounded, redacted inference input.

    Incomplete/oversized sources cannot be safely screened and are skipped.
    Tool text is used only for exclusion, never passed to the model. Tool checks
    in the digest therefore remain reports from the conversation.
    """
    index = importlib.import_module('codex_search_index')
    conversation_text, session_id, tool_strings = index.conversation_text, index.session_id, index.tool_strings
    tool_events = index.TOOL_EVENTS
    with source_reader(path,home) as (f,st):
        key=hashlib.sha256(str(path.relative_to(home)).encode()).hexdigest()
        result: dict[str, object]={'key':key,'source':clean(str(path)), 'id':'', 'cwd':'',
                'last_activity':'', 'status':'pending','partial':False,'dialogue':'','hash':''}
        if st.st_size > MAX_SOURCE_BYTES:
            return {**result,'status':'skipped','reason':'oversized_source','hash':f'{st.st_size}:{st.st_mtime_ns}'}
        messages=[]; mirrored=set(); h=hashlib.sha256(); malformed=0; privacy=False
        while raw:=f.readline(MAX_LINE_BYTES+1):
            h.update(raw)
            if len(raw)>MAX_LINE_BYTES:
                return {**result,'status':'skipped','reason':'oversized_record','hash':f'{st.st_size}:{st.st_mtime_ns}'}
            try:
                row=json.loads(raw)
                if not isinstance(row,dict): raise ValueError()
                kind=row.get('type'); p=row.get('payload')
                if not isinstance(p,dict) or not isinstance(kind,str): raise ValueError()
                date=row.get('timestamp')
                if isinstance(date,str) and epoch(date)>epoch(result['last_activity']): result['last_activity']=date
                if kind=='session_meta':
                    if exclude_helpers and helper_origin(p):
                        # No helper content or metadata is exposed. Early exclusion
                        # also avoids screening large spawned-agent transcripts.
                        return {**result, 'id':'', 'cwd':'', 'source':'',
                                'status':'skipped', 'reason':'helper_session'}
                    sid=session_id(p.get('id'))
                    if result['id'] and sid and sid!=result['id']: raise ValueError()
                    result['id']=sid or result['id']
                    if isinstance(p.get('cwd'),str): result['cwd']=clean(p['cwd'])
                    if epoch(p.get('timestamp'))>epoch(result['last_activity']): result['last_activity']=p['timestamp']
                role=''; text=''; response=False
                if kind=='response_item' and p.get('type')=='message':
                    role=p.get('role'); response=True
                    content=p.get('content')
                    if not isinstance(content,list): raise ValueError()
                    text='\n'.join(x['text'] for x in content if isinstance(x,dict) and x.get('type') in ('input_text','output_text') and isinstance(x.get('text'),str))
                elif kind=='event_msg' and p.get('type') in ('user_message','agent_message'):
                    role='user' if p['type']=='user_message' else 'assistant'; text=p.get('message')
                elif kind=='response_item' and p.get('type') not in ('message','reasoning'):
                    # Tool arguments or retrieval output from the private store.
                    if PRIVATE_TOOL.search(str(p.get('name',''))) or any(PRIVATE_TOOL.search(x) for x in tool_strings(p)):
                        privacy=True
                elif kind=='event_msg' and p.get('type') in tool_events:
                    if any(PRIVATE_TOOL.search(x) for x in tool_strings(p)): privacy=True
                if role in ('user','assistant'):
                    text=conversation_text(role,text)
                    if text:
                        if PRIVATE_USE.search(text): privacy=True
                        safe=clean(text)
                        digest=hashlib.sha256((role+'\0'+safe).encode()).hexdigest()
                        if response: mirrored.add(digest)
                        messages.append((response,digest,role,safe))
            except (ValueError,TypeError,UnicodeError,RecursionError): malformed+=1
        if os.fstat(f.fileno()).st_mtime_ns!=st.st_mtime_ns or os.fstat(f.fileno()).st_size!=st.st_size:
            return {**result,'status':'skipped','reason':'changed_during_read','hash':h.hexdigest()}
        result['hash']=h.hexdigest()
        if malformed:
            return {**result,'status':'skipped','reason':'unsafe_source','id':'','cwd':'','source':''}
        if privacy: return {**result,'status':'skipped','reason':'private_context','id':'','cwd':'','source':''}
        if not result['id']:
            return {**result,'status':'skipped','reason':'missing_session_id'}
        lines=[json.dumps({'role':role,'text':text},ensure_ascii=True) for response,digest,role,text in messages if response or digest not in mirrored]
        data='\n'.join(lines).encode()
        result['partial']=len(data)>INPUT_BYTES
        if len(data)>INPUT_BYTES:
            data=data[:INPUT_BYTES//2]+b'\n[... omitted middle; partial ...]\n'+data[-INPUT_BYTES//2:]
        result['hash']=hashlib.sha256(('\n'.join(lines)).encode()).hexdigest()
        result['dialogue']=data.decode('utf-8',errors='replace')
        if not lines: result.update(status='skipped',reason='no_dialogue')
        return result


def native_titles(home: Path) -> dict[str, str]:
    """Read the native title index only; no summaries or private cache imports."""
    session_id = importlib.import_module('codex_search_index').session_id
    titles = {}
    path = home / 'session_index.jsonl'
    try:
        with source_reader(path, home) as (stream, metadata):
            if metadata.st_size > 4 * 1024 * 1024:
                return titles
            for raw in stream:
                try:
                    row = json.loads(raw)
                    if not isinstance(row, dict):
                        continue
                    sid = session_id(row.get('id'))
                    title = row.get('thread_name')
                    if sid and isinstance(title, str) and len(title) <= 1000:
                        titles[sid] = clean(title)
                except (ValueError, UnicodeError):
                    continue
    except OSError:
        pass
    return titles
