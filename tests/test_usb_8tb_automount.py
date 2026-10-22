import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/enable-usb-8tb-automount.py'
UUID = 'e2f4a51f-954a-4168-a1af-2c9645d3f00a'
OLD = f'UUID={UUID} /mnt/usb-8tb ext4 defaults,nofail 0 2\n'


class USBMountTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'USB automount installer is missing')
        spec = importlib.util.spec_from_file_location('usb_mount', SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_upgrade_preserves_other_disks_and_is_idempotent(self):
        other = '# Keep this disk\nUUID=other /other ext4 defaults 0 2\n'
        updated = self.module.configure(other + OLD)
        self.assertTrue(updated.startswith(other))
        self.assertIn('nofail,x-systemd.automount,x-systemd.device-timeout=5s', updated)
        self.assertIn('x-systemd.device-bound=yes', updated)
        self.assertEqual(self.module.configure(updated), updated)

    def test_refuses_missing_duplicate_or_conflicting_entry(self):
        for contents in ('', OLD + OLD, OLD.replace(UUID, 'other'),
                         OLD.replace('/mnt/usb-8tb', '/other'),
                         OLD.replace('ext4', 'ntfs'), OLD.replace('defaults,nofail', 'ro,nofail')):
            with self.subTest(contents=contents), self.assertRaises(ValueError):
                self.module.configure(contents)

    def test_preserves_inline_comment(self):
        updated = self.module.configure(OLD.rstrip() + ' # external drive\n')
        self.assertTrue(updated.endswith(' # external drive\n'))

    def test_hotplug_rule_targets_only_the_uuid_and_mount_unit(self):
        rule = self.module.RULE
        self.assertIn('ACTION=="add"', rule)
        self.assertIn('SUBSYSTEM=="block"', rule)
        self.assertIn(f'ENV{{ID_FS_UUID}}=="{UUID}"', rule)
        self.assertIn('TAG+="systemd"', rule)
        self.assertIn(r'ENV{SYSTEMD_WANTS}+="mnt-usb\\x2d8tb.mount"', rule)
        self.assertNotIn('RUN', rule)

    def test_activation_preserves_already_mounted_disk(self):
        with patch.object(self.module.subprocess, 'check_output', return_value=f'ext4 {UUID}\n'), patch.object(self.module.subprocess, 'run') as run:
            self.module.activate(lambda *args: None)
        self.assertFalse(any('.automount' in str(call) for call in run.call_args_list))

    def test_activation_starts_automount_if_disk_is_absent(self):
        absent = self.module.subprocess.CalledProcessError(1, 'findmnt')
        with patch.object(self.module.subprocess, 'check_output', side_effect=absent), patch.object(self.module.subprocess, 'run') as run, patch.object(self.module.Path, 'exists', return_value=False):
            self.module.activate(lambda *args: None)
        run.assert_called_once_with(['systemctl', 'start', self.module.UNIT + '.automount'], check=True, timeout=30)


if __name__ == '__main__':
    unittest.main()
