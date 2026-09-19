#!/usr/bin/env python3
"""Opt-in network test: download the requested video and verify all media."""
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    for dependency in ('yt-dlp', 'ffmpeg', 'ffprobe'):
        if not shutil.which(dependency):
            raise RuntimeError(f'missing dependency: {dependency}')
    output = Path(tempfile.mkdtemp(prefix='yt-dl-live-'))
    print(f'Artifacts retained in {output}', flush=True)
    script = Path(__file__).resolve().parents[1] / 'scripts' / 'executable_yt-dl'
    result = subprocess.run([str(script), 'https://www.youtube.com/watch?v=oLOzkH0zVZo',
                             '-o', str(output)], capture_output=True, text=True, timeout=900)
    if result.stderr:
        print(result.stderr, file=sys.stderr, end='')
    if result.returncode:
        raise RuntimeError(f'download exited {result.returncode}; media verification not run')
    media = Path(result.stdout.strip())
    if not media.is_file() or media.stat().st_size == 0:
        raise RuntimeError('missing or empty media')
    runtime = ['--js-runtimes', 'node'] if shutil.which('node') else []
    metadata = json.loads(subprocess.run([
        'yt-dlp', '--ignore-config', '--no-playlist', *runtime,
        '--skip-download', '--dump-single-json',
        'https://www.youtube.com/watch?v=oLOzkH0zVZo',
    ], capture_output=True, text=True, check=True, timeout=180).stdout)
    if metadata.get('id') != 'oLOzkH0zVZo':
        raise RuntimeError('downloaded metadata ID does not match requested video')
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                            '-of', 'json', str(media)], capture_output=True, text=True, check=True)
    info = json.loads(probe.stdout)
    kinds = {stream['codec_type'] for stream in info['streams']}
    if not {'audio', 'video'} <= kinds:
        raise RuntimeError(f'missing audio/video streams: {kinds}')
    duration = float(info['format']['duration'])
    expected = float(metadata['duration'])
    if not all(math.isfinite(n) and n > 0 for n in (duration, expected)):
        raise RuntimeError('invalid media/source duration')
    if abs(duration - expected) > max(2, expected * 0.01):
        raise RuntimeError(f'duration mismatch: media={duration}, source={expected}')
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-nostdin', '-i', str(media),
                    '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'], check=True, timeout=900)
    print(json.dumps({'result': 'PASS', 'path': str(media), 'id': metadata['id'],
                      'bytes': media.stat().st_size, 'duration': duration,
                      'source_duration': expected, 'streams': sorted(kinds),
                      'full_decode': 'passed'}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as error:
        print(f'Live verification FAILED: {error}', file=sys.stderr)
        sys.exit(1)
