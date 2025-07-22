#!/usr/bin/env python3
"""
Wrapper script to run main.py with correct Python path setup.
This script should be run from the project root directory.
"""
import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')

sys.path.insert(0, project_root)
sys.path.insert(0, src_path)

if __name__ == "__main__":
    from src.main import main
    main()
