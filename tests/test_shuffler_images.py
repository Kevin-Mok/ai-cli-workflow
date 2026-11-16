"""Exercise image-only wallpaper cycles and the actual i3 shell arguments."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SHUFFLER = ROOT / 'scripts/executable_shuffler'

class WallpaperSelectionTest(unittest.TestCase):
    def test_image_cycle_rejects_stale_metadata_and_handles_nested_space_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wanted = [root/'root.png', root/'dim/non-editing/with space.JPG', root/'4k/number.jpg.1']
            for path in wanted + [root/'README.md', root/'download.jpg.crdownload', root/'.git/hidden.png']:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('fixture')
            (root/'shuffle.txt').write_text(str(root/'README.md')+'\n'+str(root/'deleted.png')+'\n')
            actual = []
            for _ in wanted:
                result = subprocess.run(['bash',str(SHUFFLER),'-i',str(root)],capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr)
                actual.append(result.stdout.strip())
            self.assertEqual(set(actual),set(map(str,wanted)))
            self.assertEqual(len(set(actual)),len(wanted))

    def test_empty_image_collection_fails_without_a_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp)/'notes.txt').write_text('not an image')
            result = subprocess.run(['bash',str(SHUFFLER),'-i',tmp],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(result.stdout,'')
            self.assertIn('No wallpaper images',result.stderr)

    def test_generic_mode_still_accepts_nonimages(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'notes.txt';path.write_text('generic selection')
            result = subprocess.run(['bash',str(SHUFFLER),tmp],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(result.stdout.strip(),str(path))

    def test_each_wallpaper_binding_uses_all_images_and_passes_spaces_as_one_argument(self):
        config=(ROOT/'dot_config/i3/config.tmpl').read_text()
        bindings=[line.split(' exec ',1)[1] for line in config.splitlines()
                  if line.startswith('bindsym ') and 'apply-pywal-theme' in line and 'shuffler' in line]
        self.assertEqual(len(bindings),6)
        with tempfile.TemporaryDirectory() as tmp:
            home=Path(tmp);scripts=home/'scripts';scripts.mkdir()
            selected=home/'Pictures/Backgrounds/non editing/space name.png'
            (scripts/'shuffler').write_text('#!/bin/bash\n[ "$1" = -i ] && [ "$2" = "$HOME/Pictures/Backgrounds" ] || exit 9\nprintf "%s\\n" "$HOME/Pictures/Backgrounds/non editing/space name.png"\n')
            (scripts/'apply-pywal-theme').write_text('#!/bin/bash\n[ "$#" = 1 ] && [ "$1" = "$HOME/Pictures/Backgrounds/non editing/space name.png" ]\n')
            for p in scripts.iterdir():p.chmod(0o755)
            env={**os.environ,'HOME':tmp,'scripts_path':str(scripts),'make_st_script':'true'}
            for command in bindings:
                with self.subTest(command=command):
                    result=subprocess.run(['bash','-c',command.replace('/home/example',tmp)],env=env,capture_output=True,text=True)
                    self.assertEqual(result.returncode,0,result.stderr)
