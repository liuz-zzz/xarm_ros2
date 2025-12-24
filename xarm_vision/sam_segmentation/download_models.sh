#!/bin/bash
# SAM模型下载脚本
# 下载所有3个SAM模型文件到models目录

set -e  # 遇到错误立即退出

echo "开始下载SAM模型文件..."
echo "总大小约 4GB,请确保有足够的磁盘空间和网络带宽"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MODELS_DIR="$SCRIPT_DIR/models"

# 创建models目录(如果不存在)
mkdir -p "$MODELS_DIR"
cd "$MODELS_DIR"

# 下载sam_vit_b (358MB)
echo "[1/3] 下载 sam_vit_b.pth (358MB)..."
if [ -f "sam_vit_b.pth" ]; then
    echo "  文件已存在,跳过下载"
else
    wget -c https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth -O sam_vit_b.pth
    echo "  ✓ sam_vit_b.pth 下载完成"
fi
echo ""

# 下载sam_vit_l (1.2GB)
echo "[2/3] 下载 sam_vit_l.pth (1.2GB)..."
if [ -f "sam_vit_l.pth" ]; then
    echo "  文件已存在,跳过下载"
else
    wget -c https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth -O sam_vit_l.pth
    echo "  ✓ sam_vit_l.pth 下载完成"
fi
echo ""

# 下载sam_vit_h (2.4GB)
echo "[3/3] 下载 sam_vit_h.pth (2.4GB)..."
if [ -f "sam_vit_h.pth" ]; then
    echo "  文件已存在,跳过下载"
else
    wget -c https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -O sam_vit_h.pth
    echo "  ✓ sam_vit_h.pth 下载完成"
fi
echo ""

echo "========================================="
echo "所有模型下载完成!"
echo "========================================="
echo ""
ls -lh "$MODELS_DIR"/*.pth
echo ""
echo "模型文件位置: $MODELS_DIR"
