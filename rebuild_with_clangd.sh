#!/bin/bash
# Rebuild workspace with compile_commands.json for clangd support

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Rebuilding workspace with clangd support"
echo "=========================================="

# Build with compile commands export
echo ""
echo "Step 1: Building workspace..."
colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

# Merge compile_commands.json files
echo ""
echo "Step 2: Merging compile_commands.json..."
python3 merge_compile_commands.py

echo ""
echo "=========================================="
echo "✓ Build complete!"
echo "✓ clangd is configured for code navigation"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Reload your IDE/editor window"
echo "2. Open a C++ file from xarm_ros2"
echo "3. Code navigation (Go to Definition, Find References) should now work!"
echo ""
