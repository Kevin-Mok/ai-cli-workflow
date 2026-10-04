#!/usr/bin/env python3
"""Run the maintained-skill selection benchmark without changing installed skills."""
from pathlib import Path
import runpy
import sys

root = Path(__file__).resolve().parents[1] / 'benchmarks/metaprompt-selection'
sys.path.insert(0, str(root))
runpy.run_path(str(root / 'selection.py'), run_name='__main__')
