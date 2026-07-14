#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import importlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))


class SecondBrainPathSafetyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.boundary = self.root / "vault"
        self.boundary.mkdir()
        self.paths = importlib.import_module("second_brain.paths")
        self.safe_create = importlib.import_module("second_brain.safe_create")
        self.safe_files = importlib.import_module("second_brain.safe_files")

    def test_atomic_create_never_overwrites_existing_target(self) -> None:
        target = self.boundary / "imports" / "note.md"
        target.parent.mkdir()
        target.write_bytes(b"RACE_SENTINEL\n")

        with self.assertRaises(self.paths.TargetExistsError):
            self.paths.atomic_create(
                self.boundary,
                target,
                b"APPROVED_IMPORT\n",
            )

        self.assertEqual(target.read_bytes(), b"RACE_SENTINEL\n")

    def test_atomic_create_rejects_symlinked_parent_without_outside_write(
        self,
    ) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        (self.boundary / "imports").symlink_to(outside, target_is_directory=True)
        target = self.boundary / "imports" / "note.md"

        with self.assertRaises(self.paths.PathError):
            self.paths.atomic_create(
                self.boundary,
                target,
                b"DO_NOT_WRITE_OUTSIDE\n",
            )

        self.assertEqual(list(outside.iterdir()), [])

    def test_regular_file_bytes_rejects_hardlinks_and_symlinks(self) -> None:
        target = self.boundary / "protected.md"
        target.write_bytes(b"protected\n")
        hardlink = self.boundary / "hardlink.md"
        os.link(target, hardlink)

        with self.assertRaises(self.paths.PathError):
            self.paths.regular_file_bytes(self.boundary, target)

        hardlink.unlink()
        outside = self.root / "outside.md"
        outside.write_bytes(b"outside\n")
        target.unlink()
        target.symlink_to(outside)
        with self.assertRaises(self.paths.PathError):
            self.paths.regular_file_bytes(self.boundary, target)

    def test_atomic_replace_rejects_stale_expected_content(self) -> None:
        target = self.boundary / "protected.md"
        target.write_bytes(b"changed-after-preview\n")
        expected_sha = hashlib.sha256(b"previewed\n").hexdigest()

        with self.assertRaises(self.paths.PathError):
            self.paths.atomic_replace_if_unchanged(
                self.boundary,
                target,
                expected_sha,
                b"upgraded\n",
            )

        self.assertEqual(target.read_bytes(), b"changed-after-preview\n")

    def test_atomic_replace_preserves_edit_injected_after_identity_check(self) -> None:
        original = b"previewed\n"
        manual = b"MANUAL_EDIT_SENTINEL\n"
        target = self.boundary / "protected.md"
        backup = self.boundary / "protected-before-stat.md"
        manual_candidate = self.boundary / "manual-candidate.md"
        target.write_bytes(original)
        manual_candidate.write_bytes(manual)
        expected_sha = hashlib.sha256(original).hexdigest()
        real_stat = self.paths.os.stat
        injected = False

        def inject_after_stat(path, *args, **kwargs):
            nonlocal injected
            result = real_stat(path, *args, **kwargs)
            if (
                path == target.name
                and kwargs.get("dir_fd") is not None
                and not injected
            ):
                injected = True
                os.replace(target, backup)
                os.replace(manual_candidate, target)
            return result

        with mock.patch.object(
            self.paths.os,
            "stat",
            side_effect=inject_after_stat,
        ):
            with self.assertRaises(self.paths.PathError):
                self.paths.atomic_replace_if_unchanged(
                    self.boundary,
                    target,
                    expected_sha,
                    b"AUTOMATED_UPDATE\n",
                )

        self.assertTrue(injected)
        self.assertEqual(target.read_bytes(), b"AUTOMATED_UPDATE\n")
        self.assertEqual(backup.read_bytes(), original)
        recovery = list(self.boundary.glob(".protected.md.*.tmp"))
        self.assertEqual(len(recovery), 1)
        self.assertEqual(recovery[0].read_bytes(), manual)

    def test_portable_create_rejects_casefold_sibling(self) -> None:
        parent = self.boundary / "imports"
        parent.mkdir()
        sibling = parent / "NOTE.md"
        sibling.write_bytes(b"LATE_SIBLING_SENTINEL\n")
        target = parent / "note.md"

        with self.assertRaises(self.paths.TargetExistsError):
            self.paths.atomic_create(
                self.boundary,
                target,
                b"APPROVED_IMPORT\n",
                portable_unique=True,
            )

        self.assertFalse(target.exists())
        self.assertEqual(sibling.read_bytes(), b"LATE_SIBLING_SENTINEL\n")

    def test_portable_create_rejects_casefold_parent_sibling(self) -> None:
        imports = self.boundary / "imports"
        imports.mkdir()
        existing = imports / "PRIVATE-SOURCE"
        existing.mkdir()
        target = imports / "private-source" / "note.md"

        with self.assertRaises(self.paths.TargetExistsError):
            self.paths.atomic_create(
                self.boundary,
                target,
                b"APPROVED_IMPORT\n",
                portable_unique=True,
            )

        self.assertFalse(target.parent.exists())
        self.assertTrue(existing.is_dir())

    def test_portable_create_rolls_back_after_late_ancestor_collision(self) -> None:
        imports = self.boundary / "imports"
        imports.mkdir()
        target = imports / "private-source" / "note.md"
        collision = imports / "PRIVATE-SOURCE"
        real_link = self.safe_create.os.link
        injected = False

        def inject_ancestor_collision(*args, **kwargs):
            nonlocal injected
            result = real_link(*args, **kwargs)
            collision.mkdir()
            injected = True
            return result

        with mock.patch.object(
            self.safe_create.os,
            "link",
            side_effect=inject_ancestor_collision,
        ):
            with self.assertRaises(self.paths.TargetExistsError):
                self.paths.atomic_create(
                    self.boundary,
                    target,
                    b"APPROVED_IMPORT\n",
                    portable_unique=True,
                )

        self.assertTrue(injected)
        self.assertFalse(target.exists())
        self.assertFalse(target.parent.exists())
        self.assertTrue(collision.is_dir())

    def test_portable_create_never_deletes_late_manual_target_on_rollback(
        self,
    ) -> None:
        parent = self.boundary / "imports"
        parent.mkdir()
        target = parent / "note.md"
        sibling = parent / "NOTE.md"
        manual_candidate = parent / "manual-candidate.md"
        manual = b"LATE_MANUAL_TARGET\n"
        manual_candidate.write_bytes(manual)
        real_link = self.safe_create.os.link

        def inject_manual_target_and_collision(*args, **kwargs):
            result = real_link(*args, **kwargs)
            os.replace(manual_candidate, target)
            sibling.write_bytes(b"LATE_PORTABLE_SIBLING\n")
            return result

        with mock.patch.object(
            self.safe_create.os,
            "link",
            side_effect=inject_manual_target_and_collision,
        ):
            with self.assertRaises(self.paths.PathError):
                self.paths.atomic_create(
                    self.boundary,
                    target,
                    b"APPROVED_IMPORT\n",
                    portable_unique=True,
                )

        self.assertEqual(target.read_bytes(), manual)
        self.assertEqual(sibling.read_bytes(), b"LATE_PORTABLE_SIBLING\n")

    def test_atomic_create_rejects_late_target_replacement_before_success(
        self,
    ) -> None:
        parent = self.boundary / "imports"
        parent.mkdir()
        target = parent / "note.md"
        manual_candidate = parent / "manual-candidate.md"
        manual = b"LATE_MANUAL_TARGET\n"
        manual_candidate.write_bytes(manual)
        real_link = self.safe_create.os.link

        def inject_manual_target(*args, **kwargs):
            result = real_link(*args, **kwargs)
            os.replace(manual_candidate, target)
            return result

        with mock.patch.object(
            self.safe_create.os,
            "link",
            side_effect=inject_manual_target,
        ):
            with self.assertRaises(self.paths.PathError):
                self.paths.atomic_create(
                    self.boundary,
                    target,
                    b"APPROVED_IMPORT\n",
                    portable_unique=True,
                )

        self.assertEqual(target.read_bytes(), manual)

    def test_atomic_replace_fails_closed_while_another_process_has_file_open(
        self,
    ) -> None:
        original = b"previewed\n"
        manual = b"MANUAL_OPEN_WRITER_SENTINEL\n"
        target = self.boundary / "protected.md"
        target.write_bytes(original)
        child_code = (
            "import os,sys\n"
            "fd=os.open(sys.argv[1], os.O_RDWR)\n"
            "print('ready', flush=True)\n"
            "sys.stdin.readline()\n"
            "os.lseek(fd, 0, os.SEEK_SET)\n"
            "os.ftruncate(fd, 0)\n"
            f"os.write(fd, {manual!r})\n"
            "os.fsync(fd)\n"
            "os.close(fd)\n"
        )
        process = subprocess.Popen(
            [sys.executable, "-B", "-c", child_code, str(target)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            assert process.stdout is not None
            self.assertEqual(process.stdout.readline().strip(), "ready")
            with self.assertRaises(self.paths.PathError):
                self.paths.atomic_replace_if_unchanged(
                    self.boundary,
                    target,
                    hashlib.sha256(original).hexdigest(),
                    b"AUTOMATED_UPDATE\n",
                )
        finally:
            assert process.stdin is not None
            process.stdin.write("continue\n")
            process.stdin.flush()
            stdout, stderr = process.communicate(timeout=10)
            self.assertEqual(process.returncode, 0, stdout + stderr)

        self.assertEqual(target.read_bytes(), manual)

    def test_atomic_replace_detects_target_replaced_after_exchange(self) -> None:
        original = b"previewed\n"
        manual = b"MANUAL_NEW_TARGET_SENTINEL\n"
        target = self.boundary / "protected.md"
        target.write_bytes(original)
        manual_candidate = self.boundary / "manual-new-target.md"
        manual_candidate.write_bytes(manual)
        real_read = self.safe_files._read_descriptor
        injected = False
        reads = 0

        def inject_after_displaced_read(descriptor):
            nonlocal injected, reads
            result = real_read(descriptor)
            reads += 1
            if reads == 2 and not injected:
                injected = True
                os.replace(manual_candidate, target)
            return result

        with mock.patch.object(
            self.safe_files,
            "_read_descriptor",
            side_effect=inject_after_displaced_read,
        ):
            with self.assertRaises(self.paths.PathError):
                self.paths.atomic_replace_if_unchanged(
                    self.boundary,
                    target,
                    hashlib.sha256(original).hexdigest(),
                    b"AUTOMATED_UPDATE\n",
                )

        self.assertTrue(injected)
        self.assertEqual(target.read_bytes(), manual)
        recovery = list(self.boundary.glob(".protected.md.*.tmp"))
        self.assertEqual(len(recovery), 1)
        self.assertEqual(recovery[0].read_bytes(), original)

    def test_atomic_replace_leases_installed_inode_until_finalization(self) -> None:
        original = b"previewed\n"
        target = self.boundary / "protected.md"
        target.write_bytes(original)
        real_read = self.safe_files._read_installed_prepared
        writer_returncode: int | None = None
        writer_code = (
            "import os,sys\n"
            "try:\n"
            " fd=os.open(sys.argv[1],os.O_WRONLY|os.O_NONBLOCK)\n"
            "except BlockingIOError:\n"
            " raise SystemExit(3)\n"
            "os.ftruncate(fd,0)\n"
            "os.write(fd,b'EXTERNAL_WRITER_SENTINEL\\n')\n"
            "os.fsync(fd)\n"
            "os.close(fd)\n"
        )

        def inject_external_writer(
            parent_fd,
            target_name,
            descriptor,
            prepared,
        ):
            nonlocal writer_returncode
            result = real_read(parent_fd, target_name, descriptor, prepared)
            completed = subprocess.run(
                [sys.executable, "-B", "-c", writer_code, str(target)],
                check=False,
                capture_output=True,
                text=True,
            )
            writer_returncode = completed.returncode
            return result

        with mock.patch.object(
            self.safe_files,
            "_read_installed_prepared",
            side_effect=inject_external_writer,
        ):
            with self.assertRaises(self.paths.PathError):
                self.paths.atomic_replace_if_unchanged(
                    self.boundary,
                    target,
                    hashlib.sha256(original).hexdigest(),
                    b"AUTOMATED_UPDATE\n",
                )

        self.assertEqual(writer_returncode, 3)
        self.assertEqual(target.read_bytes(), b"AUTOMATED_UPDATE\n")
        recovery = list(self.boundary.glob(".protected.md.*.tmp"))
        self.assertEqual(len(recovery), 1)
        self.assertEqual(recovery[0].read_bytes(), original)

    def test_atomic_replace_preserves_atomic_save_that_renamed_leased_inode(
        self,
    ) -> None:
        original = b"previewed\n"
        manual = b"MANUAL_ATOMIC_SAVE_WITH_BACKUP\n"
        target = self.boundary / "protected.md"
        backup = self.boundary / "protected.md~"
        target.write_bytes(original)
        real_exchange = self.safe_files._rename_exchange_at
        injected = False

        def inject_atomic_save(parent_fd, first, second):
            nonlocal injected
            if not injected:
                injected = True
                os.replace(target, backup)
                target.write_bytes(manual)
            return real_exchange(parent_fd, first, second)

        with mock.patch.object(
            self.safe_files,
            "_rename_exchange_at",
            side_effect=inject_atomic_save,
        ):
            with self.assertRaises(self.paths.PathError):
                self.paths.atomic_replace_if_unchanged(
                    self.boundary,
                    target,
                    hashlib.sha256(original).hexdigest(),
                    b"AUTOMATED_UPDATE\n",
                )

        self.assertTrue(injected)
        self.assertEqual(target.read_bytes(), b"AUTOMATED_UPDATE\n")
        self.assertEqual(backup.read_bytes(), original)
        recovery = list(self.boundary.glob(".protected.md.*.tmp"))
        self.assertEqual(len(recovery), 1)
        self.assertEqual(recovery[0].read_bytes(), manual)


if __name__ == "__main__":
    unittest.main()
