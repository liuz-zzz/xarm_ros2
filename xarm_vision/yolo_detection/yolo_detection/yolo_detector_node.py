#!/usr/bin/env python3
"""
YOLO 物体检测节点
使用 YOLOv8/v11 进行实时物体检测，发布检测结果到 ROS2 话题
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose
from std_msgs.msg import Header
from cv_bridge import CvBridge
import cv2
import numpy as np
# 解析模型路径
import os
from ament_index_python.packages import get_package_share_directory
from ultralytics import YOLO

class YoloDetectorNode(Node):
    """YOLO 物体检测 ROS2 节点"""
    
    def __init__(self):
        super().__init__('yolo_detector')
        
        # 声明参数
        self.declare_parameter('model_path', 'yolov8n.pt')
        self.declare_parameter('confidence_threshold', 0.5)
        self.declare_parameter('iou_threshold', 0.45)
        self.declare_parameter('device', 'cuda:0')
        self.declare_parameter('image_topic', '/camera/camera/color/image_raw')
        self.declare_parameter('publish_annotated', True)
        # 目标类别过滤 - 默认检测人
        self.declare_parameter('target_classes', ['person'])
        
        # 获取参数
        model_path = self.get_parameter('model_path').value
        self.conf_threshold = self.get_parameter('confidence_threshold').value
        self.iou_threshold = self.get_parameter('iou_threshold').value
        device = self.get_parameter('device').value
        image_topic = self.get_parameter('image_topic').value
        self.publish_annotated = self.get_parameter('publish_annotated').value
        self.target_classes = self.get_parameter('target_classes').value

        self.get_logger().info(f'✓ 参数加载成功')
        if self.target_classes:
            self.get_logger().info(f'  - 目标类别: {self.target_classes}')
        else:
            self.get_logger().info(f'  - 检测模式: 所有类别')
        
        
        # 如果是相对路径,在包的share目录中查找
        if not os.path.isabs(model_path):
            try:
                package_share_dir = get_package_share_directory('yolo_detection')
                full_model_path = os.path.join(package_share_dir, model_path)
                if os.path.exists(full_model_path):
                    model_path = full_model_path
                    self.get_logger().info(f'使用包中的模型: {model_path}')
                else:
                    self.get_logger().warn(f'包中未找到模型文件: {full_model_path}')
            except Exception as e:
                self.get_logger().warn(f'无法获取包路径: {e}')
        
        # 初始化 YOLO 模型
        self.get_logger().info(f'加载 YOLO 模型: {model_path}')
        self.get_logger().info(f'使用设备: {device}')
        try:
            self.model = YOLO(model_path)
            self.model.to(device)
            self.get_logger().info('YOLO 模型加载成功')
        except Exception as e:
            self.get_logger().error(f'YOLO 模型加载失败: {e}')
            raise
        
        # CV Bridge
        self.bridge = CvBridge()
        
        # 订阅图像话题
        self.image_sub = self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            10
        )
        
        # 发布检测结果
        self.detection_pub = self.create_publisher(
            Detection2DArray,
            '/yolo/detections',
            10
        )
        
        # 发布标注图像（可选）
        if self.publish_annotated:
            self.annotated_pub = self.create_publisher(
                Image,
                '/yolo/image_annotated',
                10
            )
        
        # 统计信息
        self.frame_count = 0
        self.detection_count = 0
        
        self.get_logger().info('YOLO 检测节点已启动')
        self.get_logger().info(f'订阅图像话题: {image_topic}')
        self.get_logger().info(f'置信度阈值: {self.conf_threshold}')
        
    def image_callback(self, msg: Image):
        """图像回调函数"""
        try:
            # 转换 ROS 图像到 OpenCV 格式
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            # YOLO 推理
            results = self.model(
                cv_image,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                verbose=False
            )
            
            # 处理检测结果
            detections = self.process_detections(results[0], msg.header)
            
            # 发布检测结果
            self.detection_pub.publish(detections)
            
            # 发布标注图像
            if self.publish_annotated and len(detections.detections) > 0:
                # 如果有类别过滤,需要手动绘制只包含目标类别的标注
                if self.target_classes:
                    # 过滤结果,只保留目标类别
                    filtered_indices = []
                    for i, box in enumerate(results[0].boxes):
                        cls_id = int(box.cls[0].cpu().numpy())
                        class_name = self.model.names[cls_id]
                        if class_name in self.target_classes:
                            filtered_indices.append(i)
                    
                    # 使用YOLO的plot方法,但只绘制过滤后的索引
                    if filtered_indices:
                        # 创建过滤后的boxes列表
                        import torch
                        filtered_boxes_data = results[0].boxes.data[filtered_indices]
                        # 临时替换boxes用于绘制
                        original_boxes = results[0].boxes
                        results[0].boxes.data = filtered_boxes_data
                        annotated_image = results[0].plot()
                        # 恢复原始boxes
                        results[0].boxes = original_boxes
                    else:
                        annotated_image = cv_image
                else:
                    # 没有类别过滤,绘制所有检测
                    annotated_image = results[0].plot()
                
                annotated_msg = self.bridge.cv2_to_imgmsg(annotated_image, encoding='bgr8')
                annotated_msg.header = msg.header
                self.annotated_pub.publish(annotated_msg)
            
            # 统计
            self.frame_count += 1
            self.detection_count += len(detections.detections)
            
            if self.frame_count % 30 == 0:
                avg_detections = self.detection_count / self.frame_count
                self.get_logger().info(
                    f'已处理 {self.frame_count} 帧, '
                    f'平均检测数: {avg_detections:.2f}'
                )
                
        except Exception as e:
            self.get_logger().error(f'图像处理错误: {e}')
    
    def process_detections(self, result, header: Header) -> Detection2DArray:
        """将 YOLO 结果转换为 ROS Detection2DArray 消息"""
        detection_array = Detection2DArray()
        detection_array.header = header
        
        # 获取检测框
        boxes = result.boxes
        
        if boxes is None or len(boxes) == 0:
            return detection_array
        
        for box in boxes:
            # 获取边界框坐标 (xyxy 格式)
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            
            # 获取类别和置信度
            cls_id = int(box.cls[0].cpu().numpy())
            confidence = float(box.conf[0].cpu().numpy())
            class_name = self.model.names[cls_id]
            
            # 如果指定了目标类别，过滤
            if self.target_classes and class_name not in self.target_classes:
                continue
            
            # 创建 Detection2D 消息
            detection = Detection2D()
            detection.header = header
            
            # 设置边界框中心和大小
            center_x = float((x1 + x2) / 2.0)
            center_y = float((y1 + y2) / 2.0)
            size_x = float(x2 - x1)
            size_y = float(y2 - y1)
            
            detection.bbox.center.position.x = center_x
            detection.bbox.center.position.y = center_y
            detection.bbox.size_x = size_x
            detection.bbox.size_y = size_y
            
            # 设置类别和置信度
            hypothesis = ObjectHypothesisWithPose()
            hypothesis.hypothesis.class_id = class_name
            hypothesis.hypothesis.score = confidence
            detection.results.append(hypothesis)
            
            # 设置检测ID (格式: class_name_index)
            detection_index = len(detection_array.detections)
            detection.id = f"{class_name}_{detection_index}"
            
            # 添加到数组
            detection_array.detections.append(detection)
        
        return detection_array


def main(args=None):
    rclpy.init(args=args)
    
    try:
        node = YoloDetectorNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f'节点错误: {e}')
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
