"""Home-only resync for incomplete recovery bundles; never publish or recreate root."""
import importlib.util
import json
from pathlib import Path
import types


def sync_home(args, engine):
    b=types.SimpleNamespace(**engine)
    b.require_root()
    b.require_tools(['rsync','findmnt','lsblk','findfs'])
    bundle=Path(args.bundle)
    if bundle.is_symlink() or not bundle.is_dir() or not bundle.name.endswith('.incomplete'):
        b.fail('Home sync requires an ordinary .incomplete backup directory.')
    bundle=bundle.resolve(strict=True)
    if (bundle/'COMPLETE').exists() or (bundle/'COMPLETE').is_symlink():
        b.fail('Refusing to change a published backup.')
    for name in ('system.tar.xz','backup.log'):
        path=bundle/name
        if path.is_symlink() or not path.is_file():
            b.fail('Home sync requires ordinary '+name)
    for name in ('home','home-index.json','warnings.json'):
        path=bundle/name
        if path.is_symlink() or (path.exists() and (not path.is_dir() if name=='home' else not path.is_file())):
            b.fail('Unsafe home sync destination: '+name)
    warnings=[]
    if (bundle/'warnings.json').exists():
        warnings=json.loads((bundle/'warnings.json').read_text())
        if not isinstance(warnings,list) or not all(isinstance(item,str) for item in warnings):
            b.fail('Existing warnings.json must contain a list of warning strings.')
    root=Path(args.source_root).resolve(strict=True)
    meta=b.source_preflight(root,bundle,live=args.live)
    b.destination_preflight(bundle)
    owner=b.backup_owner()
    if args.dry_run:
        b.phase('Dry run: home-only sync into '+str(bundle)+'; root archive unchanged')
        for pattern in b.home_excludes(meta['excludes']): print('  exclude '+pattern)
        return
    spec=importlib.util.spec_from_file_location('backup_progress',Path(__file__).with_name('backup-pc-progress.py'))
    progress=importlib.util.module_from_spec(spec);spec.loader.exec_module(progress)
    engine['ACTIVE_PROGRESS']=progress.Session(bundle,append=True)
    try:
        b.set_bundle_owner(bundle,owner)
        b.phase('HOME SYNC START: '+str(bundle)+'; existing root archive unchanged')
        engine['ACTIVE_PROGRESS'].start('home')
        warnings+=b.copy_home(root/'home',bundle/'home',meta['excludes'],live=args.live)
        engine['ACTIVE_PROGRESS'].finish('home')
        b.phase('Verifying copied home inventory; bundle remains incomplete')
        home=b.inspect_home(bundle/'home',excludes=[],exclude_caches=False)
        (bundle/'home-index.json').write_text(json.dumps(home,indent=2)+'\n')
        (bundle/'home-index.json').chmod(0o600)
        (bundle/'warnings.json').write_text(json.dumps(warnings,indent=2)+'\n')
        (bundle/'warnings.json').chmod(0o600)
        b.phase('HOME SYNC FINISHED: '+str(bundle)+'; full recovery bundle remains incomplete')
    except BaseException as exc:
        b.phase('HOME SYNC FAILED: '+str(exc))
        raise
    finally:
        try:
            try: b.set_bundle_owner(bundle,owner)
            finally: engine['ACTIVE_PROGRESS'].close()
        finally: engine['ACTIVE_PROGRESS']=None
