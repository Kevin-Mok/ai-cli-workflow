#!/usr/bin/env python3
"""Run the isolated prompt-skill benchmark without changing installed config."""
from pathlib import Path
import runpy
import sys

root = Path(__file__).resolve().parents[1]/'benchmarks/metaprompt'
sys.path.insert(0, str(root))
runpy.run_path(str(root/'runner.py'), run_name='__main__')
