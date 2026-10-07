"""Private technical knowledge and deterministic compact projections.

Uses context_store's descriptor-based containment, private files, and common lock.
Project source inspection is separate and never executes project instructions.
"""
from __future__ import annotations
from contextlib import contextmanager
from datetime import datetime, timezone
import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat

c = None  # Injected by the current context_store interface, including its error type.

PROJECT_NAME = 'project-knowledge.json'
CACHE_NAME = 'topic-briefs.json'
FORMAT_VERSION = 1
KNOWLEDGE_MAX_BYTES = 16 * 1024 * 1024


def now():
    return datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00','Z')


def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def empty_projects():
    return {'schema_version':1,'revision':0,'updated_at':None,'projects':[],'findings':[]}


def _strings(value, limit=4096):
    for item in c._array(value):
        c._text(item,limit)


def _path(value):
    path=c._text(value,1024)
    if PurePosixPath(path).is_absolute() or '..' in PurePosixPath(path).parts:
        raise c.StoreError('Project evidence paths must be coding-root-relative without parent traversal.')


def _hash(value):
    if not isinstance(value,str) or len(value)!=64 or any(x not in '0123456789abcdef' for x in value):
        raise c.StoreError('Invalid source hash; expected SHA-256.')


def validate_projects(value):
    record=c._object(value,set(empty_projects()))
    if type(record['schema_version']) is not int or record['schema_version']!=1 or type(record['revision']) is not int or record['revision']<0:
        raise c.StoreError('Unsupported or invalid project store version/revision; preserve it for explicit repair.')
    if record['updated_at'] is not None: c._timestamp(record['updated_at'])
    elif record['revision']!=0: raise c.StoreError('Initialized project storage requires an update timestamp.')
    identifiers=set()
    keys=set()
    project_ids=set()
    for p in c._array(record['projects']):
        c._object(p,{'id','key','topic','relative_path','purpose','technologies','structure','constraints','patterns','sources','unavailable','uninspected','inspected_at','fingerprint','repo_relative_path','provenance_version'}, {'availability'})
        if type(p['provenance_version']) is not int or p['provenance_version']!=1: raise c.StoreError('Project records require versioned example-user Mok commit evidence; rebuild legacy derived knowledge explicitly.')
        _path(p['repo_relative_path'])
        if not PurePosixPath(p['relative_path']).is_relative_to(PurePosixPath(p['repo_relative_path'])): raise c.StoreError('Project must belong to its recorded Git repository.')
        if p.get('availability','available') not in ('available','unavailable'): raise c.StoreError('Invalid project availability.')
        for field in ('id','key','topic'): c._slug(p[field])
        if p['id'] in identifiers or p['key'] in keys: raise c.StoreError('Duplicate project identifiers or keys.')
        identifiers.add(p['id']); keys.add(p['key']); project_ids.add(p['id'])
        _path(p['relative_path']); c._text(p['purpose']); c._timestamp(p['inspected_at']); _hash(p['fingerprint'])
        for field in ('technologies','structure','constraints','patterns','unavailable','uninspected'): _strings(p[field])
        source_paths=set()
        for s in c._array(p['sources']):
            c._object(s,{'path','sha256','inspected_at','kind','observations','author_evidence'})
            author=c._object(s['author_evidence'],{'author','commit','blob_sha256'})
            if author['author']!='example-user Mok' or author['blob_sha256']!=s['sha256'] or not isinstance(author['commit'],str) or len(author['commit']) not in (40,64) or any(x not in '0123456789abcdef' for x in author['commit']):
                raise c.StoreError('Source requires example-user Mok author and matching committed-content evidence.')
            _path(s['path']); _hash(s['sha256']); c._timestamp(s['inspected_at']); c._text(s['kind'],120); _strings(s['observations'])
            if s['path'] in source_paths: raise c.StoreError('Duplicate project evidence paths.')
            source_paths.add(s['path'])
            if not PurePosixPath(s['path']).is_relative_to(PurePosixPath(p['relative_path'])):
                raise c.StoreError('Project evidence must belong to its recorded project.')
    for f in c._array(record['findings']):
        c._object(f,{'id','key','topic','statement','scope','basis','status','implication','evidence','inspected_at'})
        for field in ('id','key','topic'): c._slug(f[field])
        if f['id'] in identifiers or f['key'] in keys: raise c.StoreError('Duplicate knowledge identifiers or keys.')
        identifiers.add(f['id']); keys.add(f['key'])
        for field in ('statement','scope','implication'): c._text(f[field])
        c._timestamp(f['inspected_at'])
        if f['basis']!='observed' or f['status']!='source_backed': raise c.StoreError('Technical findings must remain source-backed observations.')
        if not c._array(f['evidence']): raise c.StoreError('Technical findings require supporting sources.')
        for e in f['evidence']:
            c._object(e,{'project_id','path','sha256','inspected_at'})
            c._slug(e['project_id']); _path(e['path']); _hash(e['sha256']); c._timestamp(e['inspected_at'])
            if e['project_id'] not in project_ids: raise c.StoreError('Finding evidence refers to an unavailable project.')
            p=next(p for p in record['projects'] if p['id']==e['project_id'])
            if not any(s['path']==e['path'] and s['sha256']==e['sha256'] for s in p['sources']):
                raise c.StoreError('Finding evidence must match a validated project source hash.')
    return copy.deepcopy(record)


def load_projects(directory, *, private=True):
    if directory is None: return empty_projects()
    try: descriptor=c._regular_fd(directory,PROJECT_NAME,os.O_RDONLY,private=private)
    except FileNotFoundError: return empty_projects()
    with os.fdopen(descriptor,'rb') as stream:
        return validate_projects(c._decode(stream.read(KNOWLEDGE_MAX_BYTES+1), max_bytes=KNOWLEDGE_MAX_BYTES))


def suppress(projects, personal):
    result=copy.deepcopy(projects)
    forgotten=set(personal['forgotten_keys'])
    result['projects']=[p for p in result['projects'] if p['key'] not in forgotten]
    def forgotten_pattern(pattern):
        return 'technical.'+hashlib.sha256(pattern.encode()).hexdigest()[:16] in forgotten
    for p in result['projects']:
        p['patterns']=[pattern for pattern in p['patterns'] if not forgotten_pattern(pattern)]
        for source in p['sources']:
            source['observations']=[observation for observation in source['observations'] if not (observation.startswith('Technical pattern: ') and forgotten_pattern(observation.removeprefix('Technical pattern: ')))]
    remaining={p['id'] for p in result['projects']}
    # Drop dependent findings entirely; foundation can regenerate qualified evidence.
    result['findings']=[f for f in result['findings'] if f['key'] not in forgotten and all(e['project_id'] in remaining for e in f['evidence'])]
    return result


@contextmanager
def locked(root, *, write):
    directory=lock=None
    try:
        directory=c._directory_fd(root,create=write)
        if directory is not None:
            if write:
                lock=c._regular_fd(directory,c.LOCK_NAME,os.O_RDWR|os.O_CREAT,private=False)
                os.fchmod(lock,0o600)
            else:
                try:
                    lock=c._regular_fd(directory,c.LOCK_NAME,os.O_RDONLY)
                except FileNotFoundError:
                    if not (c._exists_at(directory,c.STORE_NAME) or c._exists_at(directory,PROJECT_NAME)):
                        yield directory
                        return
                    # An existing authoritative store normally has a lock; initialize only if possible.
                    try: lock=c._regular_fd(directory,c.LOCK_NAME,os.O_RDWR|os.O_CREAT)
                    except PermissionError: pass
            if lock is not None: fcntl.flock(lock,fcntl.LOCK_EX)
        yield directory
    except OSError:
        raise c.StoreError('Cannot safely access private knowledge; check ownership, permissions, containment and free space. Re-read before retrying.') from None
    finally:
        if lock is not None: os.close(lock)
        if directory is not None: os.close(directory)


def cache_fd(directory, *, create, repair=False):
    if directory is None: return None
    if create:
        try: os.mkdir('cache',0o700,dir_fd=directory)
        except FileExistsError: pass
    try: child=os.open('cache',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=directory)
    except FileNotFoundError: return None
    try:
        info=os.fstat(child)
        if repair and info.st_uid==os.geteuid(): os.fchmod(child,0o700)
        info=os.fstat(child)
        if info.st_uid!=os.geteuid() or stat.S_IMODE(info.st_mode)!=0o700:
            raise c.StoreError('Private cache directory requires current ownership and 0700 permissions.')
        c._reject_repository(child)
        return child
    except BaseException:
        os.close(child); raise


def invalidate_cache(directory, *, forgetting=False):
    child=None
    try:
        child=cache_fd(directory,create=False,repair=forgetting)
        if child is not None:
            # unlink never follows links; only a rebuildable projection is removed.
            try: os.unlink(CACHE_NAME,dir_fd=child)
            except FileNotFoundError: pass
            os.fsync(child)
    except (OSError,c.StoreError):
        if forgetting:
            raise c.StoreError("Forgetting tombstones are saved, but private cache cleanup failed; repair cache ownership/access and retry the same forget request.") from None
        # Stale caches never authorize retrieval: inputs and projections are validated each read.
        pass
    finally:
        if child is not None: os.close(child)


def projections(personal, projects):
    rows=[]
    for e in personal['entries']:
        if e['status']=='superseded': continue
        rows.append({**{field:e[field] for field in ('id','key','topic','statement','basis','status','scope','implication')},'kind':'personal','evidence_dates':[e['source']['as_of']], 'recorded_at':e['recorded_at'], 'evidence_basis':e['basis']+'; full provenance in detail', 'detail_id':e['id']})
    for p in projects['projects']:
        rows.append({'id':p['id'],'key':p['key'],'topic':'projects','kind':'project','statement':p['purpose'],'relative_path':p['relative_path'],'technologies':p['technologies'],'structure':p['structure'],'constraints':p['constraints'],'availability':p.get('availability','available'),'scope':('Unavailable project; historical inspected evidence only. ' if p.get('availability')=='unavailable' else 'Inspected project sources only. ')+'Ownership, activity and personal preferences are unconfirmed.','basis':'observed','status':'source_backed','evidence_dates':[p['inspected_at']],'evidence_basis':f"example-user Mok latest-author committed evidence for {len(p['sources'])} inspected sources; {len(p['unavailable'])} unavailable; {len(p['uninspected'])} uninspected markers",'implication':p['patterns'],'detail_id':p['id']})
    for f in projects['findings']:
        rows.append({**{field:f[field] for field in ('id','key','topic','statement','scope','basis','status','implication')},'kind':'finding','evidence_dates':sorted({e['inspected_at'] for e in f['evidence']}),'evidence_basis':f"{len({e['project_id'] for e in f['evidence']})} supporting projects",'project_ids':sorted({e['project_id'] for e in f['evidence']}),'detail_id':f['id']})
    return sorted(rows,key=lambda r:(r['topic'],r['kind'],r['id']))


def cached_projection(directory, personal, projects):
    expected={'format_version':FORMAT_VERSION,'inputs':{'personal':{'revision':personal['revision'],'sha256':digest(personal)},'projects':{'revision':projects['revision'],'sha256':digest(projects)}},'records':projections(personal,projects)}
    child=None
    try:
        child=cache_fd(directory,create=False)
        if child is not None:
            try:
                descriptor=c._regular_fd(child,CACHE_NAME,os.O_RDONLY)
                with os.fdopen(descriptor,'rb') as stream: candidate=c._decode(stream.read(KNOWLEDGE_MAX_BYTES+1), max_bytes=KNOWLEDGE_MAX_BYTES)
                # Compare validated direct projections as well as input tags: a tampered cache cannot add records.
                if candidate==expected: return candidate['records']
            except (OSError,c.StoreError): pass
            os.close(child); child=None
        if directory is not None:
            child=cache_fd(directory,create=True)
            if child is not None: c._write(child,expected,name=CACHE_NAME, max_bytes=KNOWLEDGE_MAX_BYTES)
    except (OSError,c.StoreError):
        # Unsafe/unwritable/malformed cache has no authority; use bounded direct projections.
        pass
    finally:
        if child is not None: os.close(child)
    return expected['records']


def bounded(records, *, limit=8, char_budget=6000):
    if type(limit) is not int or limit<1 or limit>10000 or type(char_budget) is not int or char_budget<256 or char_budget>c.MAX_BYTES:
        raise c.StoreError('Use a limit of 1–10000 and a character budget of 256–2097152.')
    def envelope(rows):
        return {'records':rows,'total':len(records),'omitted':len(records)-len(rows),'detail_ids':[r['id'] for r in records[len(rows):len(rows)+min(limit,3)] if r.get('detail_id')]}
    selected=[]
    for row in records[:limit]:
        candidate=envelope(selected+[row])
        if len(json.dumps(candidate,ensure_ascii=False,separators=(',',':')))>char_budget: break
        selected.append(row)
    result=envelope(selected)
    while len(json.dumps(result,ensure_ascii=False,separators=(',',':')))>char_budget and result['detail_ids']:
        result['detail_ids'].pop()
    return result


def retrieve(root, command, *, topic=None, project=None, query=None, identifier=None, limit=8, char_budget=6000):
    if topic is not None: c._slug(topic)
    if project is not None: c._slug(project)
    with locked(root,write=False) as directory:
        personal=c._load(directory,required=False)
        projects=suppress(load_projects(directory),personal)
        if command=='detail':
            c._slug(identifier)
            for kind,records in [('personal',personal['entries']),('question',personal['questions']),('project',projects['projects']),('finding',projects['findings'])]:
                for row in records:
                    if row['id']==identifier: return {'kind':kind,'record':row}
            raise c.StoreError('No matching managed record; it may be absent or forgotten.')
        has_stores=directory is not None and (c._exists_at(directory,c.STORE_NAME) or c._exists_at(directory,PROJECT_NAME))
        rows=cached_projection(directory,personal,projects) if has_stores else []
        if command=='topics':
            categories=sorted({r['topic'] for r in rows}|{q['topic'] for q in personal['questions']})
            rows=[{'id':t,'topic':t,'records':sum(r['topic']==t for r in rows),'open_questions':sum(q['topic']==t and q['status']=='open' for q in personal['questions']),'question_ids':[q['id'] for q in personal['questions'] if q['topic']==t and q['status']=='open'][:3]} for t in categories]
        elif command=='projects':
            rows=[r for r in rows if r['kind']=='project']
            if query:
                terms=query.casefold().split()
                rows=[r for r in rows if all(term in json.dumps(r,ensure_ascii=False).casefold() for term in terms)]
        else:
            rows=[r for r in rows if (topic is None or r['topic']==topic) and (project is None or r['id']==project or project in r.get('project_ids',[]) or project in r['scope'])]
        return bounded(rows,limit=limit,char_budget=char_budget)


def validate_all(directory):
    return load_projects(directory)


def after_personal_update(directory, personal, projects):
    filtered=suppress(projects,personal)
    if filtered!=projects:
        filtered['revision']=projects['revision']+1; filtered['updated_at']=now()
        c._write(directory,validate_projects(filtered),name=PROJECT_NAME, max_bytes=KNOWLEDGE_MAX_BYTES)
    invalidate_cache(directory, forgetting=bool(personal['forgotten_keys'] or personal['forgotten_question_ids']))


def foundation(root, coding_root, *, batch_size=8, project=None):
    sources = c._sibling("project_sources")
    discover_projects, inspect_project, recurring_findings = sources.discover_projects, sources.inspect_project, sources.recurring_findings
    if type(batch_size) is not int or not 1<=batch_size<=128:
        raise c.StoreError('Use a foundation batch size from 1 to 128.')
    if coding_root.anchor!='/' or '..' in coding_root.parts:
        raise c.StoreError('Use an absolute coding source root without parent traversal or alternate root anchors.')
    if root==c.DEFAULT_ROOT and coding_root!=Path('/home/example/coding'):
        raise c.StoreError('Real project evidence must come from the designated coding directory.')
    real_coding=Path('/home/example/coding')
    if root!=c.DEFAULT_ROOT and (coding_root.is_relative_to(real_coding) or real_coding.is_relative_to(coding_root)):
        raise c.StoreError('Real coding project knowledge must stay in the designated private root; storage overrides are for synthetic sources only.')
    try:
        roots=[p for p in discover_projects(coding_root) if p!=root and not p.is_relative_to(root)]
    except (OSError,ValueError):
        raise c.StoreError('Cannot safely discover coding sources; check root access and symlink containment.') from None
    discovered_ids={'project-'+hashlib.sha256(p.relative_to(coding_root).as_posix().encode()).hexdigest()[:16] for p in roots}
    if project:
        c._slug(project)
        # IDs are stable relative-path hashes; select without inspecting every unrelated project.
        roots=[p for p in roots if 'project-'+hashlib.sha256(p.relative_to(coding_root).as_posix().encode()).hexdigest()[:16]==project]
        if not roots:
            with locked(root,write=False) as directory:
                known=suppress(load_projects(directory),c._load(directory,required=False))
            if not any(p['id']==project for p in known['projects']):
                raise c.StoreError('Requested project is neither discovered nor in the private catalog.')
    changed_count=inspected_count=suppressed_count=0
    for offset in range(0,len(roots),batch_size):
        batch=[inspect_project(p,coding_root) for p in roots[offset:offset+batch_size]]
        inspected_count+=len(batch)
        with locked(root,write=True) as directory:
            if directory is None: raise c.StoreError('Private root must exist before building a foundation.')
            personal=c._load(directory,required=False,private=False)
            if c._exists_at(directory,c.STORE_NAME):
                descriptor=c._regular_fd(directory,c.STORE_NAME,os.O_RDONLY,private=False)
                try: os.fchmod(descriptor,0o600)
                finally: os.close(descriptor)
            old=load_projects(directory,private=False)
            result=suppress(old,personal)
            indexed={p['id']:p for p in result['projects']}
            for p in batch:
                p['availability']='available'
                if p['key'] in personal['forgotten_keys']:
                    suppressed_count+=1; continue
                previous=indexed.get(p['id'])
                if previous is None or previous['fingerprint']!=p['fingerprint'] or previous.get('availability')=='unavailable':
                    indexed[p['id']]=p; changed_count+=1
            result['projects']=sorted(indexed.values(),key=lambda p:p['id'])
            # Reuse stable dates on unchanged findings; no artificial revision churn.
            previous_findings={f['id']:f for f in result['findings']}
            findings=recurring_findings([p for p in result['projects'] if p.get('availability','available')=='available'])
            for f in findings:
                old_f=previous_findings.get(f['id'])
                if old_f is not None and {k:v for k,v in f.items() if k!='inspected_at'}=={k:v for k,v in old_f.items() if k!='inspected_at'}:
                    f['inspected_at']=old_f['inspected_at']
            result['findings']=[f for f in findings if f['key'] not in personal['forgotten_keys']]
            result=suppress(result,personal)
            validate_projects(result)
            if result!=old:
                result['revision']=old['revision']+1; result['updated_at']=now()
                c._write(directory,result,name=PROJECT_NAME, max_bytes=KNOWLEDGE_MAX_BYTES); invalidate_cache(directory)
            elif c._exists_at(directory,PROJECT_NAME):
                descriptor=c._regular_fd(directory,PROJECT_NAME,os.O_RDONLY,private=False)
                try: os.fchmod(descriptor,0o600)
                finally: os.close(descriptor)
    # Reconcile availability even when discovery is empty; preserve historical evidence.
    with locked(root,write=True) as directory:
        personal=c._load(directory,required=False,private=False)
        old=load_projects(directory,private=False)
        result=suppress(old,personal)
        changed_availability=False
        for p in result['projects']:
            if (project is None or p['id']==project) and p['id'] not in discovered_ids and p.get('availability')!='unavailable':
                p['availability']='unavailable'
                p['unavailable'].append('Project absent, excluded, or unreadable at the latest discovery; retained evidence is historical.')
                changed_availability=True
        if changed_availability:
            result['findings']=[f for f in recurring_findings([p for p in result['projects'] if p.get('availability','available')=='available']) if f['key'] not in personal['forgotten_keys']]
            result['revision']=old['revision']+1; result['updated_at']=now()
            c._write(directory,validate_projects(result),name=PROJECT_NAME,max_bytes=KNOWLEDGE_MAX_BYTES)
            invalidate_cache(directory)
    with locked(root,write=False) as directory:
        personal=c._load(directory,required=False)
        stored=suppress(load_projects(directory),personal)
    return {'ok':True,'discovered':len(roots),'inspected':inspected_count,'changed_projects':changed_count,'suppressed_projects':suppressed_count,'projects':len(stored['projects']),'findings':len(stored['findings']),'revision':stored['revision'],'sources':sum(len(p['sources']) for p in stored['projects']),'unavailable':sum(len(p['unavailable']) for p in stored['projects']),'uninspected_markers':sum(len(p['uninspected']) for p in stored['projects'])}
