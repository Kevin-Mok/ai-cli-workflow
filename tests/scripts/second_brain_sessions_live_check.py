#!/usr/bin/env python3
"""Prove native unchanged summarized sessions require no inference.

Read the live digest and native sources without changing them. Copy only
structured, redacted digest state into a private temporary directory, restrict
discovery to already summarized sources, and fail if inference is attempted.
The real backlog remains untouched and raw transcripts are never copied.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from second_brain import sessions
from second_brain.paths import ensure_private_directory, atomic_write


def main():
    root, directory = sessions.directory()
    state = sessions.load(root, directory)
    entries = {key: entry for key, entry in state['sessions'].items()
               if entry['status'] in ('ready', 'partial') and entry['summary'] is not None}
    if not entries:
        print('No successfully summarized source is available for the unchanged-input check.')
        return 1
    allowed = {entry['source'] for entry in entries.values()}
    walk = os.walk
    def selected_walk(*args, **kwargs):
        for dirname, dirs, files in walk(*args, **kwargs):
            selected = [name for name in files if str(Path(dirname) / name) in allowed]
            yield dirname, dirs, selected
    with tempfile.TemporaryDirectory(prefix='second-brain-digest-check-') as temporary:
        with patch.dict(os.environ, {'XDG_STATE_HOME': temporary}):
            fixture_root, fixture_directory = sessions.directory()
            ensure_private_directory(fixture_directory, require_repository=False)
            clone = {**state, 'sessions': entries, 'queue': []}
            atomic_write(fixture_directory / 'state.json', json.dumps(clone), mode=0o600)
            with patch.object(sessions.os, 'walk', selected_walk):
                with patch.object(sessions, 'infer', side_effect=AssertionError('unchanged input attempted inference')) as inference:
                    result = sessions.refresh()
                    inference.assert_not_called()
            assert result['model_calls'] == 0
            assert any(entry['status'] in ('ready', 'partial') for entry in result['sessions'])
            print(json.dumps({'verified_unchanged_sessions': len(entries), 'model_calls': 0,
                              'live_state_modified': False, 'raw_transcripts_copied': False}))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
