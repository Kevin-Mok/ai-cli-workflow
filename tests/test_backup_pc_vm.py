import importlib.machinery
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import types
import unittest
from unittest import mock

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/backup-pc-vm-check'

class VmTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.exists(),'reusable VM check missing')
        loader=importlib.machinery.SourceFileLoader('vm_check',str(SCRIPT))
        spec=importlib.util.spec_from_loader(loader.name,loader)
        self.vm=importlib.util.module_from_spec(spec);loader.exec_module(self.vm)

    def test_boot_disconnects_source_and_backup_and_only_uses_virtual_images(self):
        state={'iso':'/tmp/live.iso','code':'/tmp/code.fd','vars':'/tmp/vars.fd',
               'source':'/tmp/source.qcow2','backup':'/tmp/backup.qcow2','target':'/tmp/target.raw','stage':'/tmp/stage'}
        boot=' '.join(self.vm.qemu_command(state,'boot'))
        self.assertIn('target.raw',boot);self.assertNotIn('source.qcow2',boot);self.assertNotIn('backup.qcow2',boot);self.assertNotIn('live.iso',boot)
        restore=' '.join(self.vm.qemu_command(state,'restore'))
        self.assertIn('backup.qcow2',restore);self.assertIn('target.raw',restore);self.assertNotIn('source.qcow2',restore)
        backup=' '.join(self.vm.qemu_command(state,'backup'))
        self.assertIn('source.qcow2',backup);self.assertIn('backup.qcow2',backup);self.assertNotIn('target.raw',backup)

    def test_regular_image_guard_rejects_device_and_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'image';p.write_bytes(b'virtual')
            self.assertEqual(self.vm.regular_file(str(p)),str(p))
            link=Path(temp)/'link';link.symlink_to(p)
            for bad in [str(link),'/dev/null',temp]:
                with self.assertRaises(ValueError):self.vm.regular_file(bad)

    def test_init_stages_required_backup_helpers_with_the_entrypoint(self):
        # Omitting either helper makes the disposable tools disk unable to back up.
        # Mock only external image creation; initialize and file copies stay real.
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp)
            for name in ('source.raw','live.iso','code.fd','vars.fd'):
                (base/name).write_bytes(b'fixture')
            args=types.SimpleNamespace(work_dir=str(base/'work'),source_image=str(base/'source.raw'),
                iso=str(base/'live.iso'),firmware_code=str(base/'code.fd'),firmware_vars=str(base/'vars.fd'),
                target_size=70,backup_size=1,dry_run=False)
            with mock.patch.object(self.vm.shutil,'which',return_value='/fixture/qemu'), mock.patch.object(
                    self.vm,'run',return_value='{"format":"raw"}'):
                self.vm.initialize(args)
            stage=base/'work'/'stage'
            for name in ('backup-pc-progress.py','backup-pc-sync.py'):
                self.assertTrue((stage/name).is_file(), 'VM tools disk missing '+name)
                self.assertEqual((stage/name).read_bytes(),(SCRIPT.parent/name).read_bytes())
            result=subprocess.run([str(stage/'backup-pc'),'backup','--help'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)

    def test_help_and_init_dry_run_create_nothing(self):
        result=subprocess.run([str(SCRIPT),'--help'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('boot',result.stdout)
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp)
            for name in ('source.raw','live.iso','code.fd','vars.fd'): (base/name).write_bytes(b'fixture')
            args=types.SimpleNamespace(work_dir=str(base/'work'),source_image=str(base/'source.raw'),
                iso=str(base/'live.iso'),firmware_code=str(base/'code.fd'),firmware_vars=str(base/'vars.fd'),
                target_size=160,backup_size=256,dry_run=True)
            self.vm.initialize(args);self.assertFalse((base/'work').exists())

if __name__=='__main__':unittest.main()
