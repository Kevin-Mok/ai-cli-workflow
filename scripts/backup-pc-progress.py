"""Live backup copy display, metadata sizing, activity log and pipe draining.

No disk-layout operations live here. Recovery remains in the standalone Bash
script; this helper is shipped and checksummed for future backup invocations.
"""
import codecs
import datetime
import fnmatch
import os
from pathlib import Path
import re
import selectors
import signal
import stat
import subprocess
import sys
import time
import unicodedata


def safe_text(text):
    return ''.join(c if c.isprintable() else f'\\x{ord(c):02x}' for c in str(text))


def duration(seconds):
    if seconds is None: return '--:--:--'
    seconds=max(0,int(seconds))
    return f'{seconds//3600:02d}:{seconds//60%60:02d}:{seconds%60:02d}'


def estimate_root(root, excludes, dynamic, live=False, callback=None):
    """Estimate tar input, not compressed bytes; never read file contents."""
    excludes=tuple(excludes)+('./home/*',)
    seen=set()
    total=0
    def excluded(relative):
        return any(fnmatch.fnmatchcase(relative,p) for p in excludes) or any(
            relative==p or relative.startswith(p.rstrip('/')+'/') for p in dynamic)
    def visit(path,relative):
        nonlocal total
        if excluded(relative): return
        try:
            st=path.lstat()
            total+=1024  # Approximate headers/PAX metadata; percentage is an estimate.
            if callback: callback(relative)
            if stat.S_ISDIR(st.st_mode):
                if any(p.endswith('/*') and fnmatch.fnmatchcase(relative,p[:-2]) for p in excludes): return
                with os.scandir(path) as entries:
                    for entry in entries: visit(Path(entry.path),relative.rstrip('/')+'/'+entry.name)
            elif stat.S_ISREG(st.st_mode):
                inode=(st.st_dev,st.st_ino)
                if inode not in seen:
                    seen.add(inode)
                    payload=min(st.st_size,st.st_blocks*512)
                    total+=(payload+511)//512*512
        except FileNotFoundError:
            if not live: raise
    visit(Path(root),'.')
    return max(10240,total)


def fit_columns(text,width):
    result=[]
    used=0
    for c in text:
        cells=0 if unicodedata.combining(c) else (2 if unicodedata.east_asian_width(c) in ('W','F') else 1)
        if used+cells>width: break
        result.append(c);used+=cells
    return ''.join(result)


class Session:
    def __init__(self,bundle,stream=None,clock=None,append=False):
        self.stream=sys.stdout if stream is None else stream
        self.clock=time.monotonic if clock is None else clock
        self.log_path=Path(bundle)/'backup.log'
        flags=os.O_WRONLY|os.O_CREAT|os.O_NOFOLLOW|(os.O_APPEND if append else os.O_EXCL)
        fd=os.open(self.log_path,flags,0o600)
        self.log_file=os.fdopen(fd,'w',buffering=1,encoding='utf-8',errors='backslashreplace')
        self.began=self.clock()
        self.active=None
        self.current='waiting'
        self.last_display=-float('inf')
        self.last_log=-float('inf')
        self.closed=False
        self.tty_rows=0
        self.states={name:{'total':0,'bytes':0,'percent':0.0,'started':self.began,
                           'advanced':self.began,'eta':None,'finished':False,'started_copy':False}
                     for name in ('root','home')}

    def log(self,text):
        stamp=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
        self.log_file.write(stamp+' '+safe_text(text)+'\n')

    def clear_display(self):
        if not self.stream.isatty(): return
        self.stream.write('\r\033[K')
        for _ in range(max(0,self.tty_rows-1)):self.stream.write('\033[1A\r\033[K')
        self.tty_rows=0

    def message(self,text):
        self.clear_display()
        print(('' if os.environ.get('CLI_PLAIN') == '1' else '💾 ')+'[backup-pc] '+safe_text(text),file=self.stream,flush=True)
        self.log('[phase] '+text)
        self.current=text

    def start(self,stage,total=0):
        self.active=stage
        self.states[stage].update(total=total,bytes=0,percent=0.0,started=self.clock(),
                                  advanced=self.clock(),eta=None,finished=False,finishing=False,started_copy=True)
        self.current='starting '+stage
        self.render(force=True)

    def finish(self,stage):
        self.states[stage].update(percent=100.0,finished=True,eta=0)
        self.render(force=True)

    def sizing(self,name):
        self.current='Sizing root: '+name
        self.render()

    def record(self,stage,line,channel):
        if not line.strip(): return None
        st=self.states[stage]
        if stage=='root' and channel=='stderr':
            match=re.fullmatch(r'tar: BACKUP_PC_ROOT_RECORD=([0-9]+)',line)
            if match:
                amount=int(match[1])*10240  # Explicit GNU tar blocking factor=20.
                if amount>st['bytes']: st['advanced']=self.clock()
                st['bytes']=amount
                return None
        if stage=='home' and channel=='stdout':
            match=re.match(r'^\s*([0-9,]+)\s+([0-9]+)%\s+\S+\s+([0-9]+):([0-9]+):([0-9]+)',line)
            if match:
                amount=int(match[1].replace(',',''))
                if amount>st['bytes']: st['advanced']=self.clock()
                percent=float(match[2])
                elapsed=self.clock()-st['started']
                # rsync summary timestamps are elapsed, not remaining time.
                eta=(100-percent)*elapsed/percent if 0<percent<100 and elapsed>=2 else None
                st.update(bytes=amount,percent=min(99.0,percent),eta=eta,finishing=percent>=100)
                return None
        self.log('['+stage+'/'+channel+'] '+line)
        if channel=='stdout':
            self.current=line.removeprefix('BACKUP_PC_FILE:')
            return None
        # Real diagnostics remain visible and available to the original validator.
        self.clear_display()
        print(safe_text(line),file=sys.stderr,flush=True)
        return line

    def render(self,force=False):
        now=self.clock()
        interval=1 if self.stream.isatty() else 5
        if not force and now-self.last_display<interval: return
        parts=[]
        for name,st in self.states.items():
            percent=st['percent']
            eta=st['eta']
            note=''
            if not st['started_copy']: note='waiting';eta=None
            elif not st['finished'] and name=='root':
                percent=min(99.0,100*st['bytes']/max(1,st['total']))
                elapsed=now-st['started']
                eta=(st['total']-st['bytes'])*elapsed/st['bytes'] if st['bytes']>0 and elapsed>=2 else None
                if st['bytes']>=st['total']: note='finishing';eta=None
                elif now-st['advanced']>=10: note='working / rate uncertain';eta=None
            elif not st['finished'] and st.get('finishing'):
                note='finishing';eta=None
            elif not st['finished'] and now-st['advanced']>=10:
                note='working / rate uncertain';eta=None
            filled=int(percent/10)
            bar='='*filled+'-'*(10-filled)
            prefix='~' if name=='root' and not st['finished'] else ''
            parts.append(f'{name.title()} [{bar}] {prefix}{percent:5.1f}% ETA {duration(eta)} {note}'.rstrip())
        text=' | '.join(parts)+f' | elapsed {duration(now-self.began)} | '+safe_text(self.current)[:140]
        if self.stream.isatty():
            self.clear_display()
            try: width=os.get_terminal_size(self.stream.fileno()).columns or 120
            except OSError: width=120
            icon='' if os.environ.get('CLI_PLAIN') == '1' else '💾 '
            rows=[icon+part for part in parts]+[f'elapsed {duration(now-self.began)} | '+safe_text(self.current)]
            self.stream.write('\n'.join(fit_columns(row,max(1,width-1)) for row in rows))
            self.stream.flush();self.tty_rows=len(rows)
        else: print(('' if os.environ.get('CLI_PLAIN') == '1' else '💾 ')+'[backup-pc] '+text,file=self.stream,flush=True)
        self.last_display=now
        if force or now-self.last_log>=10:
            self.log('[progress] '+text)
            self.last_log=now

    def command(self,args,stage,env):
        """Stream separate pipes; return only diagnostics for the existing guards."""
        if stage=='home' or stage!=self.active: self.start(stage)
        selector=selectors.DefaultSelector()
        proc=None
        handlers={}
        buffers={}
        decoders={}
        warnings=[]
        def interrupt(signum,frame):
            raise KeyboardInterrupt('signal '+signal.Signals(signum).name)
        try:
            for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):
                handlers[sig]=signal.signal(sig,interrupt)
            proc=subprocess.Popen([str(a) for a in args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                  env=env,start_new_session=True,bufsize=0)
            for pipe,channel in ((proc.stdout,'stdout'),(proc.stderr,'stderr')):
                selector.register(pipe,selectors.EVENT_READ,channel)
                buffers[channel]=''
                decoders[channel]=codecs.getincrementaldecoder('utf-8')(errors='replace')
            while selector.get_map():
                self.render()
                for key,_ in selector.select(timeout=1):
                    channel=key.data
                    chunk=os.read(key.fileobj.fileno(),65536)
                    buffers[channel]+=decoders[channel].decode(chunk,final=not chunk)
                    pieces=re.split('[\r\n]',buffers[channel])
                    buffers[channel]=pieces.pop()
                    if not chunk:
                        pieces.append(buffers[channel]);buffers[channel]=''
                        selector.unregister(key.fileobj)
                    for line in pieces:
                        diagnostic=self.record(stage,line,channel)
                        if diagnostic is not None: warnings.append(diagnostic)
                    # Bound an unterminated diagnostic/name line without losing error text.
                    if len(buffers[channel])>65536:
                        diagnostic=self.record(stage,buffers[channel],channel)
                        if diagnostic is not None: warnings.append(diagnostic)
                        buffers[channel]=''
            return subprocess.CompletedProcess(args,proc.wait(),'',('\n'.join(warnings)+'\n') if warnings else '')
        except BaseException:
            try: self.log('[error] copy interrupted; terminating its process group')
            except OSError: pass  # Log failure must never bypass child cleanup.
            for sig in handlers: signal.signal(sig,signal.SIG_IGN)
            if proc is not None:
                try: os.killpg(proc.pid,signal.SIGTERM)
                except ProcessLookupError: pass
                try: proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    try: os.killpg(proc.pid,signal.SIGKILL)
                    except ProcessLookupError: pass
                    proc.wait()
            raise
        finally:
            selector.close()
            if proc is not None: proc.stdout.close();proc.stderr.close()
            for sig,handler in handlers.items(): signal.signal(sig,handler)

    def close(self):
        if self.closed: return
        if self.stream.isatty(): self.stream.write('\n');self.stream.flush()
        self.log_file.close()
        self.closed=True
