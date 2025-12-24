# YOLO Detection Package

这是一个用于 ROS2 的 YOLO 物体检测功能包。

## 功能特性

- 支持 YOLOv8 和 YOLOv11 所有模型
- GPU 和 CPU 推理支持
- 发布标准 ROS2 Detection2DArray 消息
- 可视化标注图像输出
- 可配置的置信度和类别过滤

## 依赖安装

```bash
# 安装 ultralytics (YOLOv8/v11)
pip install ultralytics

# 如果使用 GPU
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## 模型下载

**注意**: YOLO模型文件未包含在仓库中。

### 方法1: 自动下载(推荐)

首次运行时,Ultralytics会自动下载模型到 `~/.cache/ultralytics/`

### 方法2: 使用下载脚本

```bash
cd /path/to/yolo_detection
./download_models.sh
```

### 方法3: 手动下载

```bash
cd models/
# 下载YOLOv11n模型
wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt
```

模型会在首次使用时自动下载,无需手动操作。

## 使用方法

### 1. 编译功能包

```bash
cd ~/Work/xarm7_ws
colcon build --packages-select yolo_detection
source install/setup.bash
```

### 2. 启动检测节点

```bash
# 使用默认参数启动
ros2 launch yolo_detection yolo_detection.launch.py

# 指定模型和设备
ros2 launch yolo_detection yolo_detection.launch.py model:=yolov8s.pt device:=cuda:0

# 使用 CPU
ros2 launch yolo_detection yolo_detection.launch.py device:=cpu

# 同时启动相机
ros2 launch yolo_detection yolo_detection.launch.py use_camera:=true
```

### 3. 查看检测结果

```bash
# 查看检测消息
ros2 topic echo /yolo/detections

# 使用 RViz 可视化
ros2 run rqt_image_view rqt_image_view /yolo/image_annotated
```

## 话题说明

### 订阅话题
- `/camera/camera/color/image_raw` (sensor_msgs/Image) - 输入图像

### 发布话题
- `/yolo/detections` (vision_msgs/Detection2DArray) - 检测结果
- `/yolo/image_annotated` (sensor_msgs/Image) - 标注后的图像

## 参数配置

编辑 `config/yolo_params.yaml` 修改参数：

```yaml
yolo_detector:
  ros__parameters:
    model_path: "yolov8n.pt"          # 模型选择
    confidence_threshold: 0.5          # 置信度阈值
    device: "cuda:0"                   # 推理设备
    target_classes: []                 # 目标类别过滤
```

## 模型选择

| 模型 | 速度 | 精度 | 适用场景 |
|------|------|------|----------|
| yolov8n / yolov11n | 最快 | 中等 | 实时应用 |
| yolov8s / yolov11s | 快 | 良好 | 平衡选择 |
| yolov8m / yolov11m | 中等 | 高 | 高精度需求 |
| yolov8l / yolov11l | 慢 | 很高 | 离线处理 |

## COCO 数据集常用类别

```python
["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", 
 "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
 "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
 "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
 "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove",
 "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
 "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
 "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
 "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
 "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
 "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
 "toothbrush"]
```

## 故障排除

### 问题: 找不到 CUDA
```bash
# 检查 CUDA 是否可用
python3 -c "import torch; print(torch.cuda.is_available())"

# 如果不可用，使用 CPU
device: "cpu"
```

### 问题: 模型下载失败
```bash
# 手动下载模型
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

## 作者

liuz <liuz_z@163.com>
