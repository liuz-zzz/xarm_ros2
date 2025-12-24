#!/bin/bash
# YOLO模型下载脚本
# 下载YOLOv11n模型文件到models目录

set -e  # 遇到错误立即退出

echo "开始下载YOLO模型文件..."
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MODELS_DIR="$SCRIPT_DIR/models"

# 创建models目录(如果不存在)
mkdir -p "$MODELS_DIR"
cd "$MODELS_DIR"

# 下载yolov11n.pt
echo "下载 yolov11n.pt (约6MB)..."
if [ -f "yolov11n.pt" ]; then
    echo "  文件已存在,跳过下载"
else
    # YOLOv11模型会在首次使用时自动下载
    # 这里使用Python脚本预先下载
    python3 << 'EOF'
from ultralytics import YOLO
import os

print("  正在下载YOLOv11n模型...")
model = YOLO('yolov11n.pt')
print("  ✓ yolov11n.pt 下载完成")

# 移动到当前目录
import shutil
home_dir = os.path.expanduser('~')
source = os.path.join(home_dir, '.cache', 'ultralytics', 'yolov11n.pt')
if os.path.exists(source):
    shutil.copy(source, 'yolov11n.pt')
    print(f"  模型已复制到 models/yolov11n.pt")
EOF
fi
echo ""

echo "========================================="
echo "模型下载完成!"
echo "========================================="
echo ""
ls -lh "$MODELS_DIR"/*.pt 2>/dev/null || echo "注意: 模型文件可能在 ~/.cache/ultralytics/ 目录中"
echo ""
echo "模型文件位置: $MODELS_DIR"
echo ""
echo "提示: 如果模型不在此目录,Ultralytics会在首次运行时自动下载"
