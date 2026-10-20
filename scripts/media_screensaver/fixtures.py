"""Disposable synthetic media for the documented desktop acceptance run."""
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw


def generate(root):
    root = Path(root)
    formats = root / 'formats'
    conveyor = root / 'conveyor'
    formats.mkdir(parents=True)
    conveyor.mkdir()
    portrait = Image.new('RGB', (300, 600), '#4477aa')
    ImageDraw.Draw(portrait).text((30, 250), 'PORTRAIT', fill='white')
    for ext in ('jpg', 'jpeg', 'png', 'webp'):
        portrait.save(formats / ('portrait.' + ext))
    long = conveyor / 'long.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'testsrc2=size=640x360:rate=20',
                    '-t', '60', '-c:v', 'libx264', '-threads', '2', '-preset', 'ultrafast', '-y', str(long)], check=True)
    for ext in ('mp4', 'mov', 'mkv'):
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(long), '-t', '1', '-c', 'copy', '-y', str(formats / ('short.' + ext))], check=True)
    (formats / 'corrupt.mp4').write_bytes(b'not a video')
    (formats / 'unrelated.txt').write_text('ignored')
    return formats, conveyor


def demo(args):
    from .main import output, preview, probe
    with tempfile.TemporaryDirectory(prefix='media-screensaver-demo-') as directory:
        output(args, 'progress', 'Generating synthetic photos and short/long videos...')
        formats, conveyor = generate(directory)
        args.media = formats
        if probe(args): return 1
        args.media = conveyor
        if not args.seconds: args.seconds = 35
        output(args, 'info', 'Watch item #1 move left, middle, right and exit. Any keyboard/mouse activity dismisses.')
        return preview(args) or 0
