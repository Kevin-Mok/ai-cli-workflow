"""Isolated shortcut edits and real generator checks; never execute mapped commands."""
import json
from pathlib import Path
import os
import shlex
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
HELPER = REPO / 'dot_agents/skills/fish-alias/scripts/fish_alias.py'

class FishAliasTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'aliases').mkdir()
        self.original = {
            'commands': '# basic [[[ #\nls "lsd"\n# ]]] basic #\n# work [[[ #\nc "codex"\ncr "codex resume"\n# ]]] work #\n',
            'dirs': '# sys [[[ #\nlc ~/linux-config\n# ]]] sys #\n# cdn [[[ #\ncn ~/coding\n# ]]] cdn #\n',
            'files': '# sys [[[ #\na ~/linux-config/aliases/key_aliases.tmpl\n# ]]] sys #\n# cdn [[[ #\nre README.md\n# ]]] cdn #\n',
        }
        for kind, text in self.original.items(): self.path(kind).write_text(text)

    def path(self, kind):
        return self.root / 'aliases' / {'commands':'key_aliases.tmpl','dirs':'key_dirs.tmpl','files':'key_files.tmpl'}[kind]

    def call(self, value, apply=True, **extra):
        payload = {'input': value, **extra}
        args = ['python3', '-B', str(HELPER), '--repo', str(self.root), '--json', '--details']
        if apply: args.append('--apply')
        return subprocess.run(args, input=json.dumps(payload), text=True, capture_output=True)

    def success(self, value, **extra):
        result = self.call(value, **extra)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_command_section_and_complete_remainder(self):
        result = self.success('cbn codex-time burn day')
        self.assertEqual(result['kind'], 'commands')
        self.assertEqual(result['section'], 'work')
        self.assertIn('cbn "codex-time burn day"\n# ]]] work', self.path('commands').read_text())
        self.assertEqual(self.path('dirs').read_text(), self.original['dirs'])

    def test_readable_default_and_details(self):
        payload = json.dumps({'input':'cbn codex-time burn day'})
        base = ['python3','-B',str(HELPER),'--repo',str(self.root),'--plain']
        preview = subprocess.run(base,input=payload,text=True,capture_output=True)
        self.assertEqual(preview.returncode,0,preview.stderr)
        self.assertIn('Preview',preview.stdout)
        self.assertIn('Source',preview.stdout)
        self.assertNotIn('+++',preview.stdout)
        details = subprocess.run(base+['--details'],input=payload,text=True,capture_output=True)
        self.assertEqual(details.returncode,0,details.stderr)
        self.assertIn('+++',details.stdout)

    def test_preview_does_not_write(self):
        result = self.success('cbn codex-time burn day', apply=False)
        self.assertTrue(result['changed'])
        self.assertEqual(self.path('commands').read_text(), self.original['commands'])

    def test_directory_and_file_routing(self):
        directory = self.root / 'my project'; directory.mkdir()
        file = directory / 'notes.md'; file.touch()
        self.assertEqual(self.success('pj ' + str(directory))['kind'], 'dirs')
        result = self.success('nt ' + str(file))
        self.assertEqual(result['kind'], 'files')
        self.assertEqual(result['fish_name'], 'nnt')
        self.assertIn('my\\ project', self.path('files').read_text())
        self.assertFalse(self.success('nt ' + str(file))['changed'])

    def test_example-user_home_directory_normalization(self):
        for target in ('/home/example', '/home/example/coding/project/',
                       '"/home/example/coding/my project/"',
                       '/home/example/coding/my\\ project/'):
            with self.subTest(target=target):
                section = 'cdn' if 'coding' in target else 'sys'
                result = self.success('pj ' + target, kind='dirs', section=section)
                self.assertTrue(result['target'].startswith('~'), result)
                self.assertNotIn('/home/example', result['target'])
                self.assertEqual(result['section'], 'cdn' if 'coding' in target else 'sys')
                self.assertFalse(self.success('pj ' + target, kind='dirs', section=section)['changed'])
        generated = self.generate()
        self.assertIn('~/coding/my', generated)

    def test_home_normalization_is_directory_prefix_only(self):
        for target in ('/home/example/project/', '/tmp/home/example-user/project/'):
            with self.subTest(target=target):
                self.assertEqual(self.success('pj ' + target, kind='dirs')['target'], target)
        command = 'echo /home/example/coding/project'
        self.assertEqual(self.success('zz ' + command, section='work')['target'], command)
        file = '/home/example/notes.md'
        self.assertEqual(self.success('nt ' + file, kind='files')['target'], file)

    def test_conflicts_and_exact_comment_preservation(self):
        self.path('commands').write_text(self.original['commands'] + '  cbn "old" # retain\n# cbn "older"\nuntouched "yes"\n')
        self.path('dirs').write_text(self.original['dirs'] + 'cbn ~/old\n')
        self.path('files').write_text(self.original['files'] + 'bn ~/old.txt\ncbn ~/other.txt\n')
        self.success('cbn codex-time burn day')
        self.assertIn('#   cbn "old" # retain\n# cbn "older"\nuntouched "yes"\n', self.path('commands').read_text())
        self.assertIn('# cbn ~/old\n', self.path('dirs').read_text())
        self.assertIn('bn ~/old.txt\ncbn ~/other.txt\n', self.path('files').read_text())
        self.success('nbn codex-time burn day')
        self.assertIn('# bn ~/old.txt\ncbn ~/other.txt\n', self.path('files').read_text())

    def test_file_effective_name_conflicts(self):
        self.path('commands').write_text(self.original['commands'] + 'nre "old"\nre "unrelated"\n')
        self.success('re docs/new.md')
        self.assertIn('# nre "old"\nre "unrelated"', self.path('commands').read_text())
        self.assertIn('# re README.md', self.path('files').read_text())

    def test_identical_noop(self):
        self.success('cbn codex-time burn day')
        before = {k: self.path(k).read_bytes() for k in self.original}
        self.assertFalse(self.success('cbn codex-time burn day')['changed'])
        self.assertEqual(before, {k: self.path(k).read_bytes() for k in self.original})

    def test_conditions_only_active_conflicts_and_unconditional_insert(self):
        extra = '{{ if eq .chezmoi.hostname "impossible-fish-alias-test-host" }}\ncbn "inactive"\n{{ else }}\ncbn "active"\n{{ end }}\n'
        self.path('commands').write_text(self.original['commands'].replace('# ]]] work #', extra + '# ]]] work #'))
        self.success('cbn codex-time burn day')
        after = self.path('commands').read_text()
        self.assertIn('cbn "inactive"\n{{ else }}\n# cbn "active"\n{{ end }}', after)
        self.assertIn('{{ end }}\ncbn "codex-time burn day"', after)

    def test_missing_and_ambiguous_inputs_leave_all_bytes(self):
        before = {k: self.path(k).read_bytes() for k in self.original}
        for value in ('', 'cbn', 'zz /nonexistent/ambiguous', 'zz echo one\necho two'):
            with self.subTest(value=value):
                self.assertNotEqual(self.call(value).returncode, 0)
                self.assertEqual(before, {k: self.path(k).read_bytes() for k in self.original})

    def test_request_cannot_inject_template_code(self):
        before = {k: self.path(k).read_bytes() for k in self.original}
        result = self.call('zz echo {{ .chezmoi.hostname }}', section='work')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(before, {k: self.path(k).read_bytes() for k in self.original})

    def test_quoting_hash_metacharacters_idempotence(self):
        command = 'printf "%s # tag" "$HOME" && echo \'it works\' | cat > /tmp/not-executed'
        result = self.success('zz ' + command, section='work')
        self.assertEqual(result['target'], command)
        self.assertFalse(self.success('zz ' + command, section='work')['changed'])
        self.generate()

    def test_executable_path_with_arguments_is_command(self):
        self.assertEqual(self.success('zz /bin/echo notes.md', section='work')['kind'], 'commands')

    def test_command_with_file_argument_routes_to_commands(self):
        self.assertEqual(self.success('zz echo notes.md', section='work')['kind'], 'commands')

    def test_absolute_executable_with_arguments_is_a_command(self):
        for target in ('/bin/echo notes.md', '/bin/echo hello', '~/bin/tool notes.md'):
            with self.subTest(target=target):
                result = self.success('zz ' + target, section='work')
                self.assertEqual(result['kind'], 'commands')
                self.assertEqual(result['target'], target)

    def test_template_request_rejection_reason(self):
        before = {k: self.path(k).read_bytes() for k in self.original}
        result = self.call('zz echo {{ .chezmoi.hostname }}', section='work')
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn('Template delimiters', result.stderr)
        self.assertEqual(before, {k: self.path(k).read_bytes() for k in self.original})

    def test_backticks_preserved_in_stored_abbreviation(self):
        command = 'echo `date`'
        self.success('zz ' + command, section='work')
        self.generate()
        result = subprocess.run(['fish', '--no-config', '-c',
            'source "$argv[1]"; abbr --show zz',
            str(self.root / 'home/.config/fish/key_abbr.fish')],
            text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(shlex.split(result.stdout)[-1], command)

    def test_quoted_path_roundtrip(self):
        path = self.root / 'quoted path.md'; path.touch()
        value = 'zz "' + str(path) + '"'
        self.assertEqual(self.success(value)['kind'], 'files')
        self.assertFalse(self.success(value)['changed'])
        self.generate()

    def test_unrelated_sections_and_commented_entries_preserved(self):
        self.success('cbn codex-time burn day')
        self.assertTrue(self.path('commands').read_text().startswith('# basic [[[ #\nls "lsd"\n# ]]] basic #\n'))

    def generate(self):
        home = self.root / 'home'
        for sub in ('aliases', '.config/fish', '.config/ranger'): (home / sub).mkdir(parents=True, exist_ok=True)
        for kind in self.original:
            render = subprocess.run(['chezmoi', 'execute-template'], input=self.path(kind).read_text(), text=True, capture_output=True)
            self.assertEqual(render.returncode, 0, render.stderr)
            (home / 'aliases' / self.path(kind).stem).write_text(render.stdout)
        generated = subprocess.run(['bash', str(REPO / 'scripts/executable_sync-shortcuts')], env={**os.environ,'HOME':str(home)}, text=True, capture_output=True)
        self.assertEqual(generated.returncode, 0, generated.stderr)
        syntax = subprocess.run(['fish','-n',str(home / '.config/fish/key_abbr.fish')], text=True, capture_output=True)
        self.assertEqual(syntax.returncode, 0, syntax.stderr)
        return (home / '.config/fish/key_abbr.fish').read_text()

    def test_generator_paths_with_spaces_and_quoted_hash(self):
        self.path('commands').write_text('zz "printf \'# keep\'"\n')
        self.path('dirs').write_text('pj /tmp/my\\ project\n')
        self.path('files').write_text('nt /tmp/my\\ project/notes.md\n')
        generated = self.generate()
        self.assertIn('# keep', generated)
        self.assertIn('my\\\\ project', generated)
        self.assertIn('notes.md', generated)

if __name__ == '__main__': unittest.main()
