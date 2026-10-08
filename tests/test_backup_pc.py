"""Real tar fixtures plus mocked hardware boundaries; never format host disks."""
import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import types
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/executable_backup-pc'


def load_tool():
    source = SCRIPT.read_text().split("<<'BACKUP_PC_PY'\n", 1)
    if len(source) != 2:
        raise AssertionError('standalone backup engine is missing')
    module = types.ModuleType('backup_pc')
    module.__file__ = str(SCRIPT)
    exec(compile(source[1].rsplit('\nBACKUP_PC_PY', 1)[0], str(SCRIPT), 'exec'), module.__dict__)
    return module


def fixture(root):
    files = {
        'etc/os-release': 'ID=ubuntu\nVERSION_ID="24.04"\n',
        'etc/fstab': 'UUID=old-root / ext4 defaults 0 1\nUUID=old-home /home ext4 defaults 0 2\nUUID=old-efi /boot/efi vfat umask=0077 0 1\nUUID=old-swap none swap sw 0 0\nUUID=external /media/store ext4 defaults 0 2\n',
        'var/lib/dpkg/status': 'Package: fixture\n',
        'usr/bin/dpkg': 'binary', 'usr/sbin/grub-install': 'binary',
        'usr/sbin/update-initramfs': 'binary', 'usr/sbin/update-grub': 'binary',
        'usr/lib/grub/x86_64-efi/modinfo.sh': 'modules',
        'usr/lib/shim/shimx64.efi.signed': 'signed shim',
        'usr/lib/grub/x86_64-efi-signed/grubx64.efi.signed': 'signed grub',
        'boot/vmlinuz-fixture': 'kernel', 'lib/modules/fixture/modules.dep': 'modules',
        'boot/efi/EFI/ubuntu/shimx64.efi': 'shim',
        'boot/efi/EFI/ubuntu/grubx64.efi': 'grub',
        'home/alice/file with spaces': 'important', 'home/alice/.config/browser/profile': 'profile',
        'home/alice/.android/settings': 'android', 'home/alice/game/save': 'save',
        'opt/app/data': 'app', 'var/lib/docker/overlay2/state': 'docker',
        'var/lib/snapd/snaps/app.snap': 'snap', 'var/lib/dpkg/info/app.list': 'db',
        'var/log/journal/data': 'logs', 'var/crash/report': 'crash',
        'var/tmp/state': 'persistent', 'lost+found/recovered': 'recovered',
        'mnt/local/file': 'local', 'media/local/file': 'local',
        'home/alice/.cache/download': 'cache', 'root/.cache/download': 'cache',
        'var/cache/apt/archives/download': 'cache', 'var/lib/apt/lists/index': 'cache',
        'var/cache/pacman/pkg/download': 'cache', 'var/lib/snapd/cache/download': 'cache',
        'dev/runtime': 'runtime', 'proc/runtime': 'runtime', 'sys/runtime': 'runtime',
        'run/runtime': 'runtime', 'tmp/runtime': 'runtime',
    }
    for name, data in files.items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(data)
    elf = bytearray(20); elf[:4] = b'\x7fELF'; elf[4:6] = b'\x02\x01'; elf[18:20] = (62).to_bytes(2,'little')
    (root/'usr/bin/dpkg').write_bytes(elf)
    (root/'tmp').chmod(0o1777)
    return files


def device(name='/dev/fixture', size=200 * 2**30):
    return {'name': name, 'type': 'disk', 'size': size, 'maj:min': '99:0', 'serial': 'TEST',
            'model': 'Virtual disk', 'wwn': 'test', 'pttype': 'gpt', 'fstype': None,
            'children': [{'name': name+'1', 'type': 'part', 'size': size-2**30,
                          'maj:min': '99:1', 'fstype': 'ext4', 'uuid': 'existing'}]}


class BackupAccessTests(unittest.TestCase):
    def setUp(self):
        self.b=load_tool()
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.bundle=Path(self.tmp.name)/'bundle.incomplete'
        self.bundle.mkdir(mode=0o700)

    def test_generated_files_owned_by_invoker_without_touching_home_or_links(self):
        archive=self.bundle/'system.tar.xz';archive.write_text('fixture');archive.chmod(0o600)
        log=self.bundle/'backup.log';log.write_text('log');log.chmod(0o600)
        home=self.bundle/'home';home.mkdir();private=home/'private';private.write_text('data');private.chmod(0o400)
        before=private.stat()
        outside=Path(self.tmp.name)/'outside';outside.write_text('protected')
        (self.bundle/'warnings.json').symlink_to(outside)
        with patch.object(self.b.os,'chown') as chown:
            self.b.set_bundle_owner(self.bundle,(1234,5678))
        changed={Path(call.args[0]) for call in chown.call_args_list}
        self.assertEqual(changed,{self.bundle,archive,log})
        for call in chown.call_args_list:
            self.assertEqual(call.args[1:],(1234,5678));self.assertFalse(call.kwargs['follow_symlinks'])
        self.assertEqual((private.stat().st_uid,private.stat().st_gid,private.stat().st_mode),(before.st_uid,before.st_gid,before.st_mode))
        self.assertEqual(archive.stat().st_mode & 0o777,0o600)

    def test_repair_requires_bundle_artifacts_and_never_follows_archive_symlink(self):
        args=types.SimpleNamespace(bundle=str(self.bundle),user='example-user')
        with patch.object(self.b,'require_root'),patch.object(self.b,'set_bundle_owner') as repair:
            with self.assertRaises(self.b.BackupError): self.b.repair_access(args)
            outside=Path(self.tmp.name)/'outside';outside.write_text('protected')
            (self.bundle/'system.tar.xz').symlink_to(outside)
            (self.bundle/'backup.log').write_text('log')
            with self.assertRaises(self.b.BackupError): self.b.repair_access(args)
            repair.assert_not_called()

    def test_failed_backup_assigns_created_archive_and_log_to_invoker(self):
        root=Path(self.tmp.name)/'source';root.mkdir();fixture(root)
        dest=Path(self.tmp.name)/'backups'
        args=types.SimpleNamespace(source_root=str(root),destination=str(dest),dry_run=False,live=True)
        meta={'source_disks':[],'swap_bytes':0,'excludes':[],'consistency':'live-nonatomic'}
        def interrupted_archive(source,archive,*args,**kwargs):
            archive.write_bytes(b'partial');archive.chmod(0o600)
            raise self.b.BackupError('fixture interrupted archive')
        with patch.object(self.b,'require_root'),patch.object(self.b,'require_tools'),patch.object(self.b,'source_preflight',return_value=meta),patch.object(self.b,'destination_preflight'),patch.object(self.b,'backup_owner',return_value=(1234,5678)),patch.object(self.b.os,'chown') as chown,patch.object(self.b,'create_archive',side_effect=interrupted_archive),contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(self.b.BackupError,'fixture interrupted'):
                self.b.backup(args)
        bundle=next(dest.iterdir())
        changed={Path(call.args[0]) for call in chown.call_args_list}
        self.assertEqual(changed,{bundle,bundle/'system.tar.xz',bundle/'backup.log'})
        self.assertTrue(bundle.name.endswith('.incomplete'))
        self.assertIsNone(self.b.ACTIVE_PROGRESS)

    def test_owner_uses_account_database_and_root_without_sudo_stays_root(self):
        account=types.SimpleNamespace(pw_uid=1234,pw_gid=5678)
        with patch.dict(self.b.os.environ,{'SUDO_USER':'example-user'},clear=True),patch.object(self.b.pwd,'getpwnam',return_value=account) as lookup:
            self.assertEqual(self.b.backup_owner(),(1234,5678));lookup.assert_called_once_with('example-user')
        with patch.dict(self.b.os.environ,{},clear=True),patch.object(self.b.os,'getuid',return_value=0),patch.object(self.b.os,'getgid',return_value=0):
            self.assertEqual(self.b.backup_owner(),(0,0))


class BackupDateSyncTests(unittest.TestCase):
    def setUp(self):
        self.b=load_tool()
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)

    def test_readable_local_date_and_no_overwrite_on_same_day(self):
        now=self.b.datetime.datetime(2026,10,6,17,59)
        (self.base/'10-06-26').mkdir()
        (self.base/'10-06-26-02.incomplete').mkdir()
        bundle=self.b.new_bundle(self.base,now)
        self.assertEqual(bundle.name,'10-06-26-03.incomplete')
        self.assertEqual(bundle.stat().st_mode & 0o777,0o700)
        self.assertEqual(self.b.new_bundle(self.base,now).name,'10-06-26-04.incomplete')

    def test_home_sync_preserves_archive_and_history_and_keeps_incomplete(self):
        root=self.base/'source';root.mkdir();fixture(root)
        bundle=self.base/'10-06-26.incomplete';bundle.mkdir()
        archive=bundle/'system.tar.xz';archive.write_bytes(b'untouched archive')
        log=bundle/'backup.log';log.write_text('original history\n')
        old=archive.stat()
        (bundle/'warnings.json').write_text('["old warning"]')
        args=types.SimpleNamespace(source_root=str(root),bundle=str(bundle),live=True,dry_run=False)
        meta={'source_disks':[],'swap_bytes':0,'excludes':[]}
        with patch.object(self.b,'require_root'),patch.object(self.b,'require_tools'),patch.object(self.b,'source_preflight',return_value=meta),patch.object(self.b,'destination_preflight'),patch.object(self.b,'create_archive') as create,contextlib.redirect_stdout(io.StringIO()):
            args.dry_run=True;self.b.sync_home(args)
            self.assertEqual(log.read_text(),'original history\n')
            self.assertFalse((bundle/'home').exists())
            args.dry_run=False;self.b.sync_home(args)
        create.assert_not_called()
        self.assertEqual(archive.read_bytes(),b'untouched archive')
        self.assertEqual((archive.stat().st_ino,archive.stat().st_mtime_ns),(old.st_ino,old.st_mtime_ns))
        self.assertIn('original history',log.read_text())
        self.assertIn('HOME SYNC FINISHED',log.read_text())
        self.assertEqual(json.loads((bundle/'warnings.json').read_text()),['old warning'])
        self.assertFalse((bundle/'COMPLETE').exists())
        self.assertTrue((bundle/'home-index.json').is_file())
        self.assertEqual((bundle/'home/alice/file with spaces').read_text(),'important')

    def test_home_sync_rejects_completed_or_symlinked_bundle_files(self):
        bundle=self.base/'10-06-26.incomplete';bundle.mkdir()
        (bundle/'system.tar.xz').write_text('archive');(bundle/'backup.log').write_text('log')
        args=types.SimpleNamespace(source_root=str(self.base),bundle=str(bundle),live=True,dry_run=False)
        with patch.object(self.b,'require_root'),patch.object(self.b,'require_tools'),patch.object(self.b,'source_preflight') as preflight,patch.object(self.b,'copy_home') as copy:
            for name in ('COMPLETE','home','home-index.json','warnings.json'):
                p=bundle/name
                if name=='COMPLETE':p.write_text('complete')
                else:p.symlink_to(self.base)
                with self.assertRaises(self.b.BackupError):self.b.sync_home(args)
                p.unlink()
            preflight.assert_not_called();copy.assert_not_called()


class BackupTests(unittest.TestCase):
    def setUp(self):
        self.b = load_tool()
        self.tmp = tempfile.TemporaryDirectory(prefix='backup-pc-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'source'
        self.root.mkdir()
        self.files = fixture(self.root)
        self.archive = Path(self.tmp.name) / 'system.tar.xz'

    def make_archive(self):
        self.b.create_archive(self.root, self.archive, [])
        return self.b.inspect_archive(self.archive)

    def test_help_and_excludes(self):
        result = subprocess.run(['bash', str(SCRIPT), '--help'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--target-disk', result.stdout)
        result = subprocess.run(['bash', str(SCRIPT), 'excludes'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('./var/lib/snapd/cache/*', result.stdout)

    def test_tar_roundtrip_retains_state_and_omits_only_cache_runtime(self):
        os.link(self.root/'home/alice/file with spaces', self.root/'home/alice/hardlink')
        os.setxattr(self.root/'home/alice/file with spaces', 'user.backup-test', b'xattr')
        subprocess.run(['setfacl', '-m', 'u:65534:r--', str(self.root/'home/alice/file with spaces')], check=True)
        sparse = self.root/'home/alice/sparse'
        with sparse.open('wb') as f:
            f.seek(64*2**20); f.write(b'end')
        self.make_archive()
        out = Path(self.tmp.name)/'restored'; out.mkdir()
        self.b.extract_archive(self.archive, out)
        self.b.copy_home(self.root/'home',out/'home',[])
        for name in self.files:
            omitted = '/.cache/' in name or name.startswith(('dev/', 'proc/', 'sys/', 'run/', 'tmp/', 'var/cache/apt/archives/', 'var/lib/apt/lists/', 'var/cache/pacman/pkg/', 'var/lib/snapd/cache/'))
            self.assertEqual((out/name).exists(), not omitted, name)
        p = out/'home/alice/file with spaces'
        self.assertEqual(p.read_text(), 'important')
        self.assertEqual(p.stat().st_ino, (out/'home/alice/hardlink').stat().st_ino)
        self.assertEqual(p.stat().st_uid, (self.root/'home/alice/file with spaces').stat().st_uid)
        self.assertEqual(os.getxattr(p, 'user.backup-test'), b'xattr')
        self.assertIn('user:65534:r--', subprocess.check_output(['getfacl', '-cnp', str(p)], text=True))
        self.assertLess((out/'home/alice/sparse').stat().st_blocks*512, 2**20)
        self.assertEqual((out/'tmp').stat().st_mode & 0o7777, 0o1777)
        self.assertFalse((out/'home/home').exists())

    def test_dynamic_exclusion_preserves_other_mountpoint_files(self):
        (self.root/'mnt/unrelated').mkdir(); (self.root/'mnt/unrelated/data').write_text('external')
        self.b.create_archive(self.root, self.archive, ['./mnt/unrelated'])
        with tarfile.open(self.archive) as tf:
            names = tf.getnames()
        self.assertNotIn('./mnt/unrelated/data', names)
        self.assertIn('./mnt/local/file', names)

    def test_capacity_counts_sparse_extents_and_hardlinks_once(self):
        p = self.root/'home/alice/sparse'
        with p.open('wb') as f:
            f.seek(100*2**30); f.write(b'x')
        os.link(p, self.root/'home/alice/sparse-link')
        info = self.make_archive()
        home=self.b.inspect_home(self.root/'home',excludes=[])
        info['home_bytes']=home['bytes']
        self.assertLess(info['home_bytes'], 2**20)
        layout = self.b.layout_for(info, 2**30, 200*2**30, None)
        self.assertEqual(layout['root_gib'], 64)
        self.assertEqual(layout['swap_bytes'], 2**30)
        for capacity, override in [(60*2**30,None), (200*2**30,1)]:
            with self.assertRaises(self.b.BackupError):
                self.b.layout_for(info, 2**30, capacity, override)

    def test_partial_and_unsafe_archives_rejected(self):
        for names in [('home/alice/data',), ('../escape',), ('/absolute',)]:
            with tarfile.open(self.archive, 'w:xz') as tf:
                for name in names:
                    t = tarfile.TarInfo(name); t.size=1; tf.addfile(t, io.BytesIO(b'x'))
            with self.assertRaises(self.b.BackupError): self.b.inspect_archive(self.archive)

    def test_missing_kernel_modules_and_signed_boot_rejected(self):
        for name in ['var/lib/dpkg/status','usr/lib/shim/shimx64.efi.signed', 'lib/modules/fixture/modules.dep']:
            p=self.root/name; original=p.read_bytes(); p.unlink()
            self.b.create_archive(self.root,self.archive,[])
            with self.assertRaises(self.b.BackupError): self.b.inspect_archive(self.archive)
            p.write_bytes(original)

    def test_verify_bundle_rejects_corruption_and_incomplete(self):
        info = self.make_archive()
        bundle = Path(self.tmp.name)/'bundle'; bundle.mkdir()
        shutil.move(self.archive, bundle/'system.tar.xz')
        shutil.copy2(SCRIPT, bundle/'backup-pc')
        (bundle/'RECOVERY.md').write_text('instructions')
        (bundle/'warnings.json').write_text('[]\n')
        self.b.copy_home(self.root/'home',bundle/'home',[])
        home=self.b.inspect_home(bundle/'home',excludes=[])
        (bundle/'home-index.json').write_text(json.dumps(home))
        manifest = {'schema':2, 'consistency':'offline', 'storage':'compressed-system+browsable-home', 'home_bytes':home['bytes'], 'coverage':'full-system', 'architecture':'amd64', 'os':'ubuntu',
                    'version':'24.04', 'boot':'uefi', 'swap_bytes':0, 'source_disks':[], 'archive':info}
        (bundle/'manifest.json').write_text(json.dumps(manifest))
        self.b.write_checksums(bundle)
        (bundle/'COMPLETE').write_text('complete\n')
        self.assertEqual(self.b.verify_bundle(bundle/'system.tar.xz')['swap_bytes'],0)
        (bundle/'system.tar.xz').write_bytes(b'corrupted')
        with self.assertRaises(self.b.BackupError): self.b.verify_bundle(bundle/'system.tar.xz')
        (bundle/'COMPLETE').unlink()
        with self.assertRaises(self.b.BackupError): self.b.verify_bundle(bundle/'system.tar.xz')

    def test_source_requires_read_only_root_home_efi_and_offline(self):
        mounts=[{'target':str(self.root/suffix), 'source':'/dev/source'+str(i), 'fstype':fs,
                 'options':'ro', 'maj:min':'88:'+str(i), 'fsroot':'/'}
                for i,(suffix,fs) in enumerate([('', 'ext4'),('home','ext4'),('boot/efi','vfat')],1)]
        source=device('/dev/source'); source['maj:min']='88:0'
        source['children']=[{'name':'/dev/source'+str(i),'type':'part','size':2**30,'maj:min':'88:'+str(i),'uuid':'old-'+name} for i,name in enumerate(['root','home','efi'],1)]
        # Remove swap: this fixture tests mounts, not swap discovery.
        (self.root/'etc/fstab').write_text((self.root/'etc/fstab').read_text().replace('UUID=old-swap none swap sw 0 0\n',''))
        with patch.object(self.b,'mounts',return_value=mounts), patch.object(self.b,'block_devices',return_value=[source]), patch.object(self.b,'holders',return_value=[]):
            self.b.source_preflight(self.root, Path(self.tmp.name)/'dest')
            for bad in [mounts[:1], [dict(m,options='rw') for m in mounts], mounts+[dict(mounts[0],target='/')]]:
                with patch.object(self.b,'mounts',return_value=bad):
                    with self.assertRaises(self.b.BackupError): self.b.source_preflight(self.root,Path(self.tmp.name)/'dest')

    def test_standard_ubuntu_os_release_symlink_is_complete(self):
        p=self.root/'etc/os-release'; data=p.read_text(); p.unlink()
        (self.root/'usr/lib/os-release').write_text(data)
        p.symlink_to('../usr/lib/os-release')
        self.make_archive()

    def test_archive_architecture_encryption_and_essential_mounts_rejected(self):
        cases=[('usr/bin/dpkg',b'ARM binary'), ('etc/crypttab',b'crypt UUID=x none luks\n'),
               ('etc/fstab',(self.root/'etc/fstab').read_bytes()+b'UUID=x /usr ext4 defaults 0 2\n')]
        for name,data in cases:
            p=self.root/name; old=p.read_bytes() if p.exists() else None; p.write_bytes(data)
            self.b.create_archive(self.root,self.archive,[])
            with self.assertRaises(self.b.BackupError): self.b.inspect_archive(self.archive)
            if old is None: p.unlink()
            else: p.write_bytes(old)

    def test_script_managed_symlinks_rejected_before_restore(self):
        for name,target in [('dev','/dev'),('tmp','/tmp'),('etc/initramfs-tools/conf.d','/etc'),
                            ('etc/default/grub.d','/etc'),('etc/fstab','/etc/fstab')]:
            p=self.root/name
            if p.exists():
                if p.is_dir(): shutil.rmtree(p)
                else: p.unlink()
            p.parent.mkdir(parents=True,exist_ok=True); p.symlink_to(target)
            self.b.create_archive(self.root,self.archive,[])
            with self.assertRaises(self.b.BackupError): self.b.inspect_archive(self.archive)
            p.unlink()
            fixture(self.root)

    def test_backup_publication_is_standalone_and_failures_incomplete(self):
        dest=Path(self.tmp.name)/'bundles'
        args=types.SimpleNamespace(source_root=str(self.root),destination=str(dest),dry_run=True)
        meta={'source_disks':[], 'swap_bytes':0,'excludes':[]}
        with patch.object(self.b,'require_root'),patch.object(self.b,'require_tools'),patch.object(self.b,'source_preflight',return_value=meta),patch.object(self.b,'destination_preflight'),contextlib.redirect_stdout(io.StringIO()):
            self.b.backup(args); self.assertFalse(dest.exists())
            args.dry_run=False; self.b.backup(args)
            complete=list(dest.iterdir()); self.assertEqual(len(complete),1)
            bundle=complete[0]; self.b.verify_bundle(bundle/'system.tar.xz')
            self.assertEqual((bundle/'home/alice/file with spaces').read_text(),'important')
            self.assertEqual(bundle.stat().st_mode & 0o777,0o755)
            self.assertEqual((bundle/'system.tar.xz').stat().st_mode & 0o777,0o600)
            with tarfile.open(bundle/'system.tar.xz') as tf:
                self.assertNotIn('./home/example/file with spaces',tf.getnames())
            (bundle/'home/alice/file with spaces').write_text('changed')
            with self.assertRaises(self.b.BackupError): self.b.verify_bundle(bundle/'system.tar.xz')
            result=subprocess.run(['bash',str(bundle/'backup-pc'),'excludes'],capture_output=True,text=True,cwd='/tmp')
            self.assertEqual(result.returncode,0,result.stderr)
            with patch.object(self.b,'create_archive',side_effect=self.b.BackupError('fixture write failure')):
                with self.assertRaises(self.b.BackupError): self.b.backup(args)
            self.assertEqual(len(list(dest.glob('*.incomplete'))),1)

    def test_signed_boot_symlinks_are_resolved_inside_restored_tree(self):
        p=self.root/'usr/lib/shim/shimx64.efi.signed'; data=p.read_bytes();p.unlink()
        target=p.with_name('shimx64.efi.signed.latest');target.write_bytes(data)
        p.symlink_to('/etc/alternatives/shimx64.efi.signed')
        alt=self.root/'etc/alternatives/shimx64.efi.signed';alt.parent.mkdir(parents=True)
        alt.symlink_to('/usr/lib/shim/shimx64.efi.signed.latest')
        self.make_archive()
        with patch.object(self.b,'run') as commands:
            self.b.install_boot(self.root,{'root':'NEW'})
        self.assertEqual((self.root/'boot/efi/EFI/BOOT/BOOTX64.EFI').read_bytes(),data)
        self.assertTrue(any('--no-nvram' in call.args for call in commands.call_args_list))
        self.assertNotIn('--force',str(commands.call_args_list))

    def test_efi_links_and_managed_boot_dirs_rejected(self):
        for name in ['boot/efi/EFI/BOOT','boot/efi/EFI/ubuntu/grub.cfg']:
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to('/etc')
            self.b.create_archive(self.root,self.archive,[])
            with self.assertRaises(self.b.BackupError): self.b.inspect_archive(self.archive)
            p.unlink()

    def test_resume_removes_old_swap_and_offsets(self):
        p=self.root/'etc/default/grub';p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text('GRUB_CMDLINE_LINUX_DEFAULT="quiet resume=UUID=OLD resume_offset=42"\n')
        self.b.update_resume(self.root,'NEW')
        self.assertIn('resume=UUID=NEW',p.read_text()); self.assertNotIn('resume_offset=',p.read_text())
        self.assertEqual((self.root/'etc/initramfs-tools/conf.d/resume').read_text(),'RESUME=UUID=NEW\n')

    def test_home_copy_inventory_exclusion_parity_and_literal_mount_names(self):
        for name in ['alice/project/.cache/keep','alice/mounted [disk]/skip']:
            p=self.root/'home'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(name)
        dest=Path(self.tmp.name)/'home-copy'
        dynamic=['./home/example/mounted [disk]']
        self.b.copy_home(self.root/'home',dest,dynamic)
        self.assertTrue((dest/'alice/project/.cache/keep').is_file())
        self.assertFalse((dest/'alice/mounted [disk]/skip').exists())
        a=self.b.inspect_home(self.root/'home',dynamic)
        b=self.b.inspect_home(dest,[])
        self.assertEqual(a['entries'],b['entries'])

    def test_home_capacity_counts_canonical_data_blocks_and_missing_home_rejected(self):
        p=self.root/'home/alice/zero';p.write_bytes(bytes(64*1024))
        a=self.b.inspect_home(self.root/'home',[])
        p.write_bytes(b'x'*(64*1024))
        b=self.b.inspect_home(self.root/'home',[])
        self.assertEqual(b['bytes']-a['bytes'],64*1024)
        with self.assertRaises(self.b.BackupError):self.b.inspect_home(self.root/'missing',[])

    def test_destination_filesystem_rejects_nonlinux_readonly_before_copy(self):
        dest=Path(self.tmp.name)/'destination'
        base={'target':self.tmp.name,'fstype':'ext4','options':'rw'}
        with patch.object(self.b,'mounts',return_value=[base]):self.b.destination_preflight(dest)
        for fs,opts in [('vfat','rw'),('exfat','rw'),('ntfs','rw'),('ext4','ro')]:
            with patch.object(self.b,'mounts',return_value=[dict(base,fstype=fs,options=opts)]):
                with self.assertRaises(self.b.BackupError):self.b.destination_preflight(dest)
        self.assertFalse(dest.exists())

    def test_home_hardlinks_sparse_hash_and_symlinks_verified(self):
        p=self.root/'home/alice/data';p.write_bytes(bytes(8192)+b'bytes')
        linked=self.root/'home/alice/link';os.link(p,linked)
        (self.root/'home/alice/outside').symlink_to('/etc/passwd')
        before=self.b.inspect_home(self.root/'home',[])
        linked.unlink();shutil.copy2(p,linked)
        self.assertNotEqual(before['entries'],self.b.inspect_home(self.root/'home',[])['entries'])
        digest=self.b.sparse_digest(p,p.stat().st_size)
        with p.open('r+b') as f:f.write(b'changed')
        self.assertNotEqual(digest,self.b.sparse_digest(p,p.stat().st_size))

    def test_exclusion_lists_match_standalone_policy(self):
        for name in ['txt/exclude-dirs-backup.txt.tmpl','txt/exclude-dirs-backup-full.txt']:
            lines=(SCRIPT.parents[1]/name).read_text().splitlines()
            patterns=[line for line in lines if line.strip() and not line.startswith('#')]
            self.assertEqual(set(patterns),set(self.b.EXCLUDES))

    def test_fstab_rewrites_and_external_mounts_gain_nofail(self):
        text=(self.root/'etc/fstab').read_text()
        new=self.b.rewrite_fstab(text, {'root':'new-root','home':'new-home','efi':'new-efi','swap':'new-swap'})
        self.assertNotIn('old-',new)
        self.assertIn('UUID=new-home /home ext4',new)
        self.assertIn('UUID=external /media/store ext4 defaults,nofail',new)
        self.assertEqual(new.count('UUID=new-swap'),1)


class WriterTests(unittest.TestCase):
    def test_restore_command_order_owns_mounts_and_never_writes_firmware(self):
        b=load_tool()
        with tempfile.TemporaryDirectory(prefix='backup-pc-writer-') as temp:
            work=Path(temp)/'work'; work.mkdir()
            commands=[]; saved={}
            def boundary(*args,capture=False):
                commands.append(tuple(str(x) for x in args))
                if args[0]=='mount' and len(args)==3 and args[-1]==work:
                    fixture(work)
                if args[0]=='blkid': return 'new-'+str(args[-1]).rsplit('/',1)[-1]+'\n'
                if args[0]=='umount' and args[-1]==work:
                    saved['fstab']=(work/'etc/fstab').read_text()
                    for child in work.iterdir():
                        if child.is_dir(): shutil.rmtree(child)
                        else: child.unlink()
                return ''
            with patch.object(b.tempfile,'mkdtemp',return_value=str(work)),patch.object(b,'run',side_effect=boundary),patch.object(b,'partition_paths',return_value={i:'/dev/virtual'+str(i) for i in range(1,5)}):
                b.perform_restore(Path('/fixture/system.tar.xz'),device('/dev/virtual'),{'root_gib':64,'swap_bytes':2**30,'home_bytes':100*2**30})
            dev_mount=('mount','--bind','/dev',str(work/'dev'))
            private=('mount','--make-private',str(work/'dev'))
            pts=('mount','-t','devpts','devpts',str(work/'dev/pts'))
            self.assertIn(private,commands)
            self.assertLess(commands.index(dev_mount),commands.index(private));self.assertLess(commands.index(private),commands.index(pts))
            self.assertTrue(any(c[:2]==('mkfs.ext4','-F') and '-i' in c and c[c.index('-i')+1]=='4096' for c in commands))
            self.assertNotIn('old-',saved['fstab'])
            self.assertIn(('umount',str(work)),commands)
            self.assertEqual(commands[-1],('umount',str(work)))
            self.assertFalse(any('efivarfs' in c for c in commands))
            self.assertTrue(any('--no-nvram' in c for c in commands))


    def test_failure_cleans_only_successful_script_mounts_and_marks_incomplete(self):
        b=load_tool()
        with tempfile.TemporaryDirectory(prefix='backup-pc-failure-') as temp:
            work=Path(temp)/'work';work.mkdir(); commands=[]
            def boundary(*args,capture=False):
                commands.append(tuple(str(x) for x in args))
                if args[0]=='blkid':return str(args[-1])+'-UUID'
                if args[0]=='mount' and args[-1]==work/'boot/efi':
                    raise subprocess.CalledProcessError(1,['mount'])
                if args[0]=='umount' and args[-1]==work:
                    shutil.rmtree(work/'home');shutil.rmtree(work/'boot')
                return ''
            out=io.StringIO()
            with patch.object(b.tempfile,'mkdtemp',return_value=str(work)),patch.object(b,'run',side_effect=boundary),patch.object(b,'partition_paths',return_value={1:'/dev/virtual1',2:'/dev/virtual2',3:'/dev/virtual3'}),contextlib.redirect_stdout(out):
                with self.assertRaises(subprocess.CalledProcessError):b.perform_restore(Path('/fixture/system.tar.xz'),device('/dev/virtual'),{'root_gib':64,'swap_bytes':0,'home_bytes':100*2**30})
            unmounts=[c for c in commands if c[0]=='umount']
            self.assertEqual(unmounts,[('umount',str(work/'home')),('umount',str(work))])
            self.assertIn('TARGET INCOMPLETE',out.getvalue());self.assertFalse(work.exists())


class LiveTests(unittest.TestCase):
    setUp=BackupTests.setUp
    def test_live_source_requires_opt_in_and_preserves_mount_dirs(self):
        mounts=[{'target':target,'source':'/dev/source'+str(i),'fstype':fs,'options':'rw','maj:min':'88:'+str(i),'fsroot':'/'}
                for i,(target,fs) in enumerate([('/','ext4'),('/home','ext4'),('/boot/efi','vfat')],1)]
        mounts += [{'target':'/proc','source':'proc','fstype':'proc','options':'rw','maj:min':'0:1','fsroot':'/'},
                   {'target':'/mnt/usb-8tb','source':'/dev/backup1','fstype':'ext4','options':'rw','maj:min':'89:1','fsroot':'/'}]
        source=device('/dev/source');source['maj:min']='88:0'
        source['children']=[{'name':'/dev/source'+str(i),'type':'part','size':2**30,'maj:min':'88:'+str(i),'uuid':'old-'+name}
                            for i,name in enumerate(['root','home','efi'],1)]
        p=self.root/'etc/fstab';p.write_text(p.read_text().replace('UUID=old-swap none swap sw 0 0\n',''))
        def confined(root,name):return self.root/name
        with patch.object(self.b,'mounts',return_value=mounts),patch.object(self.b,'block_devices',return_value=[source]),patch.object(self.b,'holders',return_value=[]),patch.object(self.b,'confined_path',side_effect=confined):
            with self.assertRaises(self.b.BackupError):self.b.source_preflight(Path('/'),Path('/mnt/usb-8tb/sys-backup'))
            meta=self.b.source_preflight(Path('/'),Path('/mnt/usb-8tb/sys-backup'),live=True)
            self.assertIn('./mnt/usb-8tb',meta['excludes']);self.assertNotIn('./proc',meta['excludes'])
            self.assertEqual(meta['consistency'],'live-nonatomic')
            with patch.object(self.b,'mounts',return_value=[m for m in mounts if m['target']!='/mnt/usb-8tb']):
                with self.assertRaises(self.b.BackupError):self.b.source_preflight(Path('/'),Path('/mnt/usb-8tb/sys-backup'),live=True)
            with self.assertRaises(self.b.BackupError):self.b.source_preflight(self.root,Path('/backup'),live=True)

    def test_swap_device_alias_resolves_to_conventional_source_partition(self):
        table=[{'target':str(self.root/suffix),'source':'/dev/source'+str(i),'fstype':fs,'options':'ro','maj:min':'88:'+str(i),'fsroot':'/'}
               for i,(suffix,fs) in enumerate([('','ext4'),('home','ext4'),('boot/efi','vfat')],1)]
        source=device('/dev/source');source['maj:min']='88:0'
        source['children']=[{'name':'/dev/source'+str(i),'type':'part','size':2**30,'maj:min':'88:'+str(i),'uuid':'old-'+name}
                           for i,name in enumerate(['root','home','efi','swap'],1)]
        alias=Path(self.tmp.name)/'swap-link';alias.symlink_to('/dev/source4')
        p=self.root/'etc/fstab';p.write_text(p.read_text().replace('UUID=old-swap',str(alias)))
        with patch.object(self.b,'mounts',return_value=table),patch.object(self.b,'block_devices',return_value=[source]),patch.object(self.b,'holders',return_value=[]):
            self.assertEqual(self.b.source_preflight(self.root,Path(self.tmp.name)/'dest')['swap_bytes'],2**30)

    def test_filename_warning_text_never_hides_a_real_tar_read_error(self):
        for line in ['tar: ./opt/socket ignored/data: Warning: Cannot open: Permission denied',
                     'tar: ./opt/file changed as we read it: Warning: Cannot open: Input/output error']:
            with patch.object(self.b.subprocess,'run',return_value=subprocess.CompletedProcess([],0,'',line+'\n')):
                with self.assertRaises(self.b.BackupError):self.b.create_archive(self.root,self.archive,[],live=True)

    def test_live_tar_records_changes_but_rejects_real_read_errors(self):
        result=subprocess.CompletedProcess([],1,'','tar: ./var/log/log: file changed as we read it\n')
        with patch.object(self.b.subprocess,'run',return_value=result):
            warnings=self.b.create_archive(self.root,self.archive,[],live=True)
            self.assertIn('file changed',str(warnings))
            with self.assertRaises(self.b.BackupError):self.b.create_archive(self.root,self.archive,[])
        for error in ['tar: ./private: Warning: Cannot open: Permission denied\n', 'tar: ./disk: Warning: Read error: Input/output error\n']:
            with patch.object(self.b.subprocess,'run',return_value=subprocess.CompletedProcess([],0,'',error)):
                with self.assertRaises(self.b.BackupError):self.b.create_archive(self.root,self.archive,[],live=True)

    def test_live_copy_accepts_vanished_files_once_and_fails_other_errors(self):
        dest=Path(self.tmp.name)/'live-home'
        results=[subprocess.CompletedProcess([],24,'','file has vanished: fixture\n'),subprocess.CompletedProcess([],0,'','')]
        with patch.object(self.b.subprocess,'run',side_effect=results) as calls,patch.object(self.b.os,'utime') as timestamps:
            warnings=self.b.copy_home(self.root/'home',dest,[],live=True)
            self.assertEqual(calls.call_count,1);self.assertIn('vanished',str(warnings));timestamps.assert_not_called()
        with patch.object(self.b.subprocess,'run',return_value=subprocess.CompletedProcess([],23,'','permission denied')):
            with self.assertRaises(self.b.BackupError):self.b.copy_home(self.root/'home',dest,[],live=True)

    def test_live_copy_progress_accepts_vanished_files_but_offline_rejects(self):
        result=subprocess.CompletedProcess([],24,'','file has vanished: fixture\n')
        progress=unittest.mock.Mock()
        progress.command.return_value=result
        with patch.object(self.b,'ACTIVE_PROGRESS',progress):
            warnings=self.b.copy_home(self.root/'home',Path(self.tmp.name)/'progress-home',[],live=True)
            self.assertEqual(warnings,result.stderr.splitlines())
            progress.command.assert_called_once()
            with self.assertRaises(self.b.BackupError):
                self.b.copy_home(self.root/'home',Path(self.tmp.name)/'offline-home',[],live=False)

    def test_live_tar_shrinking_file_is_reported_and_offline_is_rejected(self):
        result=subprocess.CompletedProcess([],0,'','tar: ./var/log/log: File shrank by 4096 bytes; padding with zeros\n')
        with patch.object(self.b.subprocess,'run',return_value=result):
            self.assertIn('File shrank',str(self.b.create_archive(self.root,self.archive,[],live=True)))
            with self.assertRaises(self.b.BackupError):self.b.create_archive(self.root,self.archive,[])

    def test_live_publication_uses_copied_home_inventory_and_protects_warnings(self):
        dest=Path(self.tmp.name)/'live-bundles'
        args=types.SimpleNamespace(source_root=str(self.root),destination=str(dest),dry_run=False,live=True)
        meta={'source_disks':[],'swap_bytes':0,'excludes':[],'consistency':'live-nonatomic'}
        original_copy=self.b.copy_home
        def vanished_copy(*args, **kwargs):
            original_command=self.b.ACTIVE_PROGRESS.command
            def vanished_result(*command_args):
                result=original_command(*command_args)
                self.assertEqual(result.returncode,0)
                result.returncode=24
                result.stderr+='file has vanished: fixture\n'
                return result
            with patch.object(self.b.ACTIVE_PROGRESS,'command',side_effect=vanished_result) as calls:
                warnings=original_copy(*args,**kwargs)
                self.assertEqual(calls.call_count,1)
                return warnings
        with patch.object(self.b,'require_root'),patch.object(self.b,'require_tools'),patch.object(self.b,'source_preflight',return_value=meta),patch.object(self.b,'destination_preflight'),patch.object(self.b,'copy_home',side_effect=vanished_copy),patch.object(self.b,'set_bundle_owner',wraps=self.b.set_bundle_owner) as ownership,contextlib.redirect_stdout(io.StringIO()):
            self.b.backup(args)
        bundle=next(dest.iterdir());manifest=self.b.verify_bundle(bundle/'system.tar.xz')
        self.assertFalse(bundle.name.endswith('.incomplete'))
        self.assertEqual(ownership.call_count,4)
        self.assertEqual(ownership.call_args.args[0],bundle)
        self.assertIn('file has vanished: fixture',json.loads((bundle/'warnings.json').read_text()))
        self.assertEqual(manifest['consistency'],'live-nonatomic')
        self.assertTrue((bundle/'warnings.json').is_file())
        self.assertIn('warnings.json',(bundle/'SHA256SUMS').read_text())
        (bundle/'warnings.json').write_text('tampered')
        with self.assertRaises(self.b.BackupError):self.b.verify_bundle(bundle/'system.tar.xz')



class CompressionResourceTests(unittest.TestCase):
    def setUp(self):
        self.b=load_tool()

    def budget(self, cpus=12, available_kib=40*1024*1024, percent=75):
        memory=f'MemTotal:       65011712 kB\nMemAvailable:   {available_kib} kB\n'
        with patch.object(self.b.os,'sched_getaffinity',return_value=set(range(cpus))),patch.object(self.b.Path,'read_text',return_value=memory):
            return self.b.compression_resources(percent)

    def test_budget_respects_affinity_and_available_memory(self):
        budget=self.budget()
        self.assertEqual(budget['threads'],9)
        self.assertEqual(budget['memory_bytes'],30*2**30)
        self.assertEqual(self.budget(cpus=4)['threads'],3)
        self.assertEqual(self.budget(cpus=1)['threads'],1)
        self.assertEqual(self.budget(available_kib=80*1024*1024)['memory_bytes'],47616*2**20)

    def test_low_memory_keeps_maximum_preset_with_single_thread_or_rejects(self):
        self.assertEqual(self.budget(available_kib=1024*1024)['threads'],1)
        with self.assertRaises(self.b.BackupError): self.budget(available_kib=800*1024)
        for percent in (0,101,-1):
            with self.assertRaises(self.b.BackupError): self.budget(percent=percent)

    def test_missing_available_memory_refuses_unbounded_compression(self):
        with patch.object(self.b.os,'sched_getaffinity',return_value={0,1}),patch.object(self.b.Path,'read_text',return_value='MemTotal: 65011712 kB\n'):
            with self.assertRaises(self.b.BackupError):self.b.compression_resources()

    def test_archive_passes_budget_to_xz_without_lowering_preset(self):
        with tempfile.TemporaryDirectory() as td:
            archive=Path(td)/'system.tar.xz'
            budget={'percent':75,'threads':9,'memory_bytes':30*2**30,'cpu_count':12}
            with patch.object(self.b,'copy_command',return_value=[]) as call:
                self.b.create_archive(Path(td),archive,[],resources=budget)
            command=call.call_args.args[0]
            compressor=next(x for x in command if x.startswith('--use-compress-program='))
            self.assertIn('--threads=9',compressor)
            self.assertIn('--memlimit-compress=32212254720',compressor)
            self.assertIn('--no-adjust',compressor)
            self.assertIn('-9e',compressor)

    def test_real_memory_limited_thread_reduction_records_notice_and_completes(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'root';root.mkdir();fixture(root)
            archive=Path(td)/'system.tar.xz'
            budget={'percent':75,'threads':9,'memory_bytes':2*2**30,'cpu_count':12}
            warnings=self.b.create_archive(root,archive,[],resources=budget)
            self.assertIn('Reduced the number of threads',str(warnings))
            self.assertGreater(self.b.inspect_archive(archive)['root_bytes'],0)

    def test_cli_validates_percentage_before_any_backup(self):
        for percent in ('0','101','abc','75.5'):
            result=subprocess.run(['bash',str(SCRIPT),'backup','--source-root','/','--destination','/unused','--resource-percent',percent],capture_output=True,text=True)
            self.assertEqual(result.returncode,2)
            self.assertIn('1 to 100',result.stderr)
        help_result=subprocess.run(['bash',str(SCRIPT),'backup','--help'],capture_output=True,text=True)
        self.assertEqual(help_result.returncode,0)
        self.assertIn('--resource-percent',help_result.stdout)

    def test_inherited_xz_options_cannot_override_compression(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'root';root.mkdir();fixture(root);(root/'file').write_text('fixture')
            archive=Path(td)/'system.tar.xz'
            with patch.dict(os.environ,{'XZ_OPT':'--invalid-backup-fixture-option','XZ_DEFAULTS':'--invalid-backup-fixture-default'}):
                self.b.create_archive(root,archive,[])
                self.assertGreater(self.b.inspect_archive(archive)['root_bytes'],0)
                restored=Path(td)/'restored';restored.mkdir()
                self.b.extract_archive(archive,restored)
                self.assertEqual((restored/'file').read_text(),'fixture')
            with tarfile.open(archive) as tf:
                self.assertEqual(tf.extractfile('./file').read(),b'fixture')

class GuardTests(unittest.TestCase):
    def setUp(self):
        self.b=load_tool(); self.disk=device()
        self.manifest={'source_disks': [{'serial':'SOURCE','wwn':'source','name':'/dev/source'}],
                       'archive':{'root_bytes':1000,'home_bytes':0},'home_bytes':1000,'swap_bytes':0}

    def test_disk_guards_mounted_swap_holders_backup_running_source(self):
        with patch.object(self.b,'block_devices',return_value=[self.disk]), patch.object(self.b,'mounts',return_value=[]), patch.object(self.b,'swap_devices',return_value=[]), patch.object(self.b,'holders',return_value=[]), patch.object(self.b,'path_disks',return_value=set()), patch.object(self.b,'is_block',return_value=True):
            self.b.target_preflight('/dev/fixture',Path('/backup/system.tar.xz'),self.manifest)
            scenarios=[('mounts',[{'maj:min':'99:1','target':'/mnt/other'}]),('swap_devices',['99:1']),('holders',['dm-0']),('path_disks',{'/dev/fixture'})]
            for method,value in scenarios:
                with patch.object(self.b,method,return_value=value):
                    with self.assertRaises(self.b.BackupError): self.b.target_preflight('/dev/fixture',Path('/backup/system.tar.xz'),self.manifest)
            same=copy.deepcopy(self.manifest); same['source_disks']=[dict(self.disk)]
            with self.assertRaises(self.b.BackupError): self.b.target_preflight('/dev/fixture',Path('/backup/system.tar.xz'),same)
            with self.assertRaises(self.b.BackupError): self.b.target_preflight('/dev/fixture1',Path('/backup/system.tar.xz'),self.manifest)

    def test_zero_writes_until_verification_capacity_confirmation_and_identity(self):
        args=types.SimpleNamespace(archive='/backup/system.tar.xz',target_disk='/dev/fixture',root_size=None,dry_run=False)
        with patch.object(self.b,'require_root'), patch.object(self.b,'require_tools'), patch.object(self.b,'run',return_value='{"signatures":[]}'), patch.object(self.b,'verify_bundle',return_value=self.manifest), patch.object(self.b,'target_preflight',return_value=self.disk), patch.object(self.b,'perform_restore') as writes, patch.object(self.b,'input',create=True,return_value='NO'), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(self.b.BackupError): self.b.restore(args)
            writes.assert_not_called()
            args.dry_run=True; self.b.restore(args); writes.assert_not_called(); args.dry_run=False
            with patch.object(self.b,'input',create=True,side_effect=EOFError):
                with self.assertRaises(self.b.BackupError): self.b.restore(args)
            changed=dict(self.disk,serial='CHANGED')
            with patch.object(self.b,'input',create=True,return_value='ERASE /dev/fixture'), patch.object(self.b,'target_preflight',side_effect=[self.disk,changed]):
                with self.assertRaises(self.b.BackupError): self.b.restore(args)
            with patch.object(self.b,'verify_bundle',side_effect=self.b.BackupError('checksum')):
                with self.assertRaises(self.b.BackupError): self.b.restore(args)
            with patch.object(self.b,'target_preflight',return_value=device(size=10*2**30)):
                with self.assertRaises(self.b.BackupError): self.b.restore(args)
            writes.assert_not_called()

    def test_successful_confirmation_rechecks_then_calls_writer(self):
        args=types.SimpleNamespace(archive='/backup/system.tar.xz',target_disk='/dev/fixture',root_size=None,dry_run=False)
        with patch.object(self.b,'require_root'), patch.object(self.b,'require_tools'), patch.object(self.b,'run',return_value='{"signatures":[]}'), patch.object(self.b,'verify_bundle',return_value=self.manifest), patch.object(self.b,'target_preflight',return_value=self.disk) as preflight, patch.object(self.b,'perform_restore') as writes, patch.object(self.b,'input',create=True,return_value='ERASE /dev/fixture'), contextlib.redirect_stdout(io.StringIO()):
            self.b.restore(args)
            self.assertEqual(preflight.call_count,2); writes.assert_called_once()


if __name__=='__main__': unittest.main()
