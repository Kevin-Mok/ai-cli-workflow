import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/enable-ubs-boot-mount.py'


class BootMountTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'boot mount installer is missing')
        spec = importlib.util.spec_from_file_location('boot_mount', SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_adds_stable_nonblocking_mount_and_preserves_existing_entries(self):
        original = '# existing\nUUID=root / ext4 defaults 0 1\n'
        result = self.module.configure(original, 'data-uuid')
        self.assertTrue(result.startswith(original))
        self.assertIn('UUID=data-uuid /mnt/linux-files-3 ext4 defaults,nofail,x-systemd.automount,x-systemd.device-timeout=5s 0 2\n', result)
        self.assertEqual(self.module.configure(result, 'data-uuid'), result)

    def test_refuses_conflicting_target_or_duplicate_device(self):
        for entry in ('UUID=other /mnt/linux-files-3 ext4 defaults 0 2\n',
                      'UUID=data-uuid /other ext4 defaults 0 2\n',
                      'UUID=data-uuid /mnt/linux-files-3 ext4 noauto 0 2\n'):
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                self.module.configure(entry, 'data-uuid')


if __name__ == '__main__':
    unittest.main()
