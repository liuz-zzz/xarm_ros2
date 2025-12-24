# SAM Segmentation for ROS2

基于Meta的Segment Anything Model (SAM)的ROS2图像分割包,与YOLO检测系统集成。

## 功能特性

- 支持SAM所有模型版本 (vit_b, vit_l, vit_h)
- GPU和CPU推理支持
- 与YOLO检测结果集成
- 发布分割掩码和可视化图像
- 实时性能优化

## 依赖安装

```bash
# 安装segment-anything
pip install segment-anything

# 安装其他依赖
pip install opencv-python numpy
```

## 模型下载

**重要**: 模型文件未包含在仓库中(文件太大,超过GitHub限制)。

### 方法1: 使用下载脚本(推荐)

```bash
cd /path/to/sam_segmentation
./download_models.sh
```

### 方法2: 手动下载

```bash
cd models/
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth -O sam_vit_b.pth
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth -O sam_vit_l.pth
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -O sam_vit_h.pth
```

**注意**: 总下载大小约4GB,请确保有足够的磁盘空间和网络带宽。

## 模型文件

包中已包含3个SAM模型:
- `sam_vit_b.pth` (358MB) - 最快,适合实时应用
- `sam_vit_l.pth` (1.2GB) - 平衡速度和精度
- `sam_vit_h.pth` (2.4GB) - 最高精度,需要强大GPU

## 使用方法

### 启动SAM分割节点(包含YOLO和相机)

```bash
ros2 launch sam_segmentation sam_segmentation.launch.py
```

### 只启动SAM节点(假设YOLO已运行)

```bash
ros2 launch sam_segmentation sam_segmentation.launch.py use_yolo:=false use_camera:=false
```

### 单独运行SAM节点

```bash
ros2 run sam_segmentation sam_segmenter
```

## 话题说明

### 订阅话题
- `/camera/camera/color/image_raw` (sensor_msgs/Image) - 相机图像
- `/yolo/detections` (vision_msgs/Detection2DArray) - YOLO检测结果

### 发布话题
- `/sam/segmentation_masks` (sensor_msgs/Image) - 分割掩码(单通道)
- `/sam/annotated_image` (sensor_msgs/Image) - 带分割结果的可视化图像

## 配置参数

编辑 `config/sam_params.yaml`:

```yaml
sam_segmenter:
  ros__parameters:
    model_path: "models/sam_vit_b.pth"  # 模型路径
    model_type: "vit_b"                  # 模型类型
    device: "cuda:0"                     # 推理设备
    publish_annotated: true              # 发布可视化图像
```

## 可视化

查看分割掩码:
```bash
ros2 run rqt_image_view rqt_image_view /sam/segmentation_masks
```

查看标注图像:
```bash
ros2 run rqt_image_view rqt_image_view /sam/annotated_image
```

## 性能建议

- **实时应用**: 使用 `vit_b` 模型
- **高精度应用**: 使用 `vit_h` 模型(需要强大GPU)
- **平衡选择**: 使用 `vit_l` 模型

## 工作流程

1. 订阅YOLO检测结果获取目标边界框
2. 订阅相机图像
3. 使用SAM对每个检测框进行精细分割
4. 发布分割掩码和可视化结果

## 许可证

Apache-2.0
