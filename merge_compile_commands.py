#!/usr/bin/env python3
"""
Merge all compile_commands.json files from build subdirectories
into a single file at the workspace root for clangd.
"""

import json
import os
from pathlib import Path

def merge_compile_commands(workspace_root):
    """Merge all compile_commands.json files in the build directory."""
    build_dir = Path(workspace_root) / "build"
    output_file = Path(workspace_root) / "compile_commands.json"
    
    all_commands = []
    
    # Find all compile_commands.json files
    for compile_db in build_dir.rglob("compile_commands.json"):
        # Skip the merged one if it exists
        if compile_db == output_file:
            continue
            
        try:
            with open(compile_db, 'r') as f:
                commands = json.load(f)
                all_commands.extend(commands)
                print(f"Added {len(commands)} entries from {compile_db.relative_to(workspace_root)}")
        except Exception as e:
            print(f"Error reading {compile_db}: {e}")
    
    # Write merged compile_commands.json
    with open(output_file, 'w') as f:
        json.dump(all_commands, f, indent=2)
    
    print(f"\nMerged {len(all_commands)} compilation commands to {output_file}")
    print(f"clangd is now configured for code navigation!")

if __name__ == "__main__":
    workspace_root = os.path.dirname(os.path.abspath(__file__))
    merge_compile_commands(workspace_root)
