#!/usr/bin/env python3
"""Bounded benchmark; creates fixtures in /tmp and never writes to scan targets."""
import argparse
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts/executable_directory-sizes'


def probe(command, seconds=20, sort_output=False):
    start=time.monotonic()
    processes=[]
    sel=selectors.DefaultSelector()
    counts={'stdout':0,'stderr':0}
    first={'stdout':None,'stderr':None,'indexing':None}
    tails={'stdout':b'','stderr':b''}
    timeout=False
    try:
        du=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        processes.append(du)
        last=du
        if sort_output:
            last=subprocess.Popen(['sort','-h'],stdin=du.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
            du.stdout.close()
            processes.append(last)
        sel.register(last.stdout,selectors.EVENT_READ,'stdout')
        for p in processes: sel.register(p.stderr,selectors.EVENT_READ,'stderr')
        while sel.get_map():
            now=time.monotonic()
            if now-start>=seconds:
                timeout=True
                break
            for key,_ in sel.select(min(.1,seconds-(now-start))):
                chunk=os.read(key.fileobj.fileno(),65536)
                if not chunk:
                    sel.unregister(key.fileobj);continue
                kind=key.data
                counts[kind]+=len(chunk)
                elapsed=time.monotonic()-start
                if first[kind] is None: first[kind]=elapsed
                if kind=='stderr' and b'Indexing:' in chunk and first['indexing'] is None:
                    first['indexing']=elapsed
                tails[kind]=(tails[kind]+chunk)[-524288:]
    finally:
        for p in processes:
            if p.poll() is None:
                try: os.killpg(p.pid,signal.SIGTERM)
                except ProcessLookupError: pass
        for p in processes:
            try:p.wait(timeout=4)
            except subprocess.TimeoutExpired:
                os.killpg(p.pid,signal.SIGKILL);p.wait()
        sel.close()
        for p in processes:
            if p.stdout:p.stdout.close()
            p.stderr.close()
    stderr=tails['stderr'].decode(errors='replace')
    return {'elapsed_seconds':round(time.monotonic()-start,4),'timeout':timeout,
            'complete':not timeout and all(p.returncode==0 for p in processes),
            'returncodes':[p.returncode for p in processes],
            'stdout_bytes':counts['stdout'],'stderr_bytes':counts['stderr'],
            'first_stdout_seconds':first['stdout'],'first_stderr_seconds':first['stderr'],
            'first_indexing_seconds':first['indexing'],
            'permission_diagnostic':any(s in stderr.lower() for s in ['permission denied','permissions']),
            'vanished_diagnostic':any(s in stderr.lower() for s in ['no such file','not found','file_not_found']),
            'last_indexing':next((s for s in reversed(stderr.splitlines()) if 'Indexing:' in s),None),
            'all_processes_reaped':all(p.poll() is not None for p in processes)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--backend',required=True)
    parser.add_argument('--reference',type=Path,help='optional explicit read-only real target; one 20s probe per command')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    report={'versions':{name:subprocess.check_output(cmd,text=True).splitlines()[0] for name,cmd in [('dust',[args.backend,'--version']),('du',['du','--version']),('sort',['sort','--version'])]},'cache':'Uncontrolled OS cache. Newly created fixture has warm metadata; no cache drops. Commands rotate across three repetitions; real commands run sequentially once each.','fixture':[],'reference':[]}
    with tempfile.TemporaryDirectory(prefix='directory-sizes-benchmark-') as tmp:
        target=Path(tmp)/'nested fixture';target.mkdir()
        for i in range(120):
            d=target/f'group-{i:03d}'/'nested';d.mkdir(parents=True)
            for j in range(250):(d/f'file-{j:03d}').write_bytes(b'x'*1024)
        (target/'empty').mkdir()
        with (target/'sparse').open('wb') as f:f.truncate(512*1024*1024)
        os.link(target/'group-000'/'nested'/'file-000',target/'hardlink')
        os.symlink('group-000',target/'symlink')
        report['fixture_description']='30,000 1KiB files; 120 two-level directory branches, empty directory, 512MiB sparse file, one hardlink and one directory symlink; depth 2.'
        jobs=[('wrapper-8-threads',[str(SCRIPT),'--backend',args.backend,'--threads','8','--depth','2',str(target)],False),('dust-8-threads',[args.backend,'--config',str(Path(tmp)/'empty.toml'),'-P','-D','-d','2','-n','1000000','-T','8','-c','-b','--',str(target)],False),('du-allocated-sort',['du','-d','2','-h','--',str(target)],True)]
        (Path(tmp)/'empty.toml').write_text('')
        for repetition in range(3):
            for name,cmd,sort in jobs[repetition:]+jobs[:repetition]:
                print(f'Fixture repetition {repetition+1}: {name}',file=sys.stderr,flush=True)
                report['fixture'].append({'name':name,'repetition':repetition+1,**probe(cmd,sort_output=sort)})
    if args.reference:
        target=args.reference.absolute()
        report['reference_path']=str(target)
        for name,cmd,sort in [('wrapper-8-threads',[str(SCRIPT),'--backend',args.backend,'--threads','8','--depth','1',str(target)],False),('du-allocated-sort',['du','-d','1','-h','--',str(target)],True),('du-apparent-sort',['du','-d','1','-h','--apparent-size','--',str(target)],True)]:
            print(f'Reference probe (20s max): {name}',file=sys.stderr,flush=True)
            report['reference'].append({'name':name,**probe(cmd,sort_output=sort)})
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
