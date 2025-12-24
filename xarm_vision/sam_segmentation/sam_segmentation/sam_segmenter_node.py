#!/usr/bin/env python3
"""
SAM (Segment Anything Model) 图像分割 ROS2 节点

订阅YOLO检测结果和相机图像,对检测到的目标进行精细分割
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray
from cv_bridge import CvBridge
import cv2
import numpy as np
import os
from ament_index_python.packages import get_package_share_directory
import message_filters  # 添加时间同步

try:
    from segment_anything import sam_model_registry, SamPredictor
except ImportError:
    print("错误: 未安装 segment-anything 包")
    print("请运行: pip install segment-anything")
    raise


class SamSegmenterNode(Node):
    """SAM图像分割ROS2节点"""
    
    def __init__(self):
        super().__init__('sam_segmenter')
        
        # 声明参数
        self.declare_parameter('model_path', 'models/sam_vit_b.pth')
        self.declare_parameter('model_type', 'vit_b')
        self.declare_parameter('device', 'cuda:0')
        self.declare_parameter('image_topic', '/camera/camera/color/image_raw')
        self.declare_parameter('detection_topic', '/yolo/detections')
        self.declare_parameter('publish_annotated', True)
        self.declare_parameter('sync_slop', 0.1)  # 时间同步容差(秒)
        
        # 获取参数
        model_path = self.get_parameter('model_path').value
        model_type = self.get_parameter('model_type').value
        device = self.get_parameter('device').value
        image_topic = self.get_parameter('image_topic').value
        detection_topic = self.get_parameter('detection_topic').value
        self.publish_annotated = self.get_parameter('publish_annotated').value
        sync_slop = self.get_parameter('sync_slop').value
        
        self.get_logger().info(f'✓ 参数加载成功')
        self.get_logger().info(f'  - 时间同步容差: {sync_slop}秒')
        
        # 解析模型路径
        if not os.path.isabs(model_path):
            try:
                package_share_dir = get_package_share_directory('sam_segmentation')
                full_model_path = os.path.join(package_share_dir, model_path)
                if os.path.exists(full_model_path):
                    model_path = full_model_path
                    self.get_logger().info(f'使用包中的模型: {model_path}')
                else:
                    self.get_logger().warn(f'包中未找到模型文件: {full_model_path}')
            except Exception as e:
                self.get_logger().warn(f'无法获取包路径: {e}')
        
        # 初始化SAM模型
        self.get_logger().info(f'加载 SAM 模型: {model_path}')
        self.get_logger().info(f'模型类型: {model_type}')
        self.get_logger().info(f'使用设备: {device}')
        
        try:
            sam = sam_model_registry[model_type](checkpoint=model_path)
            sam.to(device=device)
            self.predictor = SamPredictor(sam)
            self.get_logger().info('SAM 模型加载成功')
        except Exception as e:
            self.get_logger().error(f'SAM 模型加载失败: {e}')
            raise
        
        # CV Bridge
        self.bridge = CvBridge()
        
        # 使用message_filters进行时间同步
        self.image_sub = message_filters.Subscriber(
            self,
            Image,
            image_topic
        )
        
        self.detection_sub = message_filters.Subscriber(
            self,
            Detection2DArray,
            detection_topic
        )
        
        # 近似时间同步器
        self.ts = message_filters.ApproximateTimeSynchronizer(
            [self.image_sub, self.detection_sub],
            queue_size=10,
            slop=sync_slop  # 允许的时间差
        )
        self.ts.registerCallback(self.synchronized_callback)
        
        # 发布分割掩码
        self.mask_pub = self.create_publisher(
            Image,
            '/sam/segmentation_masks',
            10
        )
        
        # 发布标注图像
        if self.publish_annotated:
            self.annotated_pub = self.create_publisher(
                Image,
                '/sam/annotated_image',
                10
            )
        
        # 统计信息
        self.frame_count = 0
        self.segmentation_count = 0
        
        self.get_logger().info('SAM 分割节点已启动')
        self.get_logger().info(f'订阅图像话题: {image_topic}')
        self.get_logger().info(f'订阅检测话题: {detection_topic}')
        self.get_logger().info('✓ 已启用时间戳同步')
        
    def synchronized_callback(self, image_msg: Image, detection_msg: Detection2DArray):
        """同步回调函数 - 确保图像和检测结果时间戳匹配"""
        try:
            # 转换ROS图像到OpenCV格式
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, desired_encoding='bgr8')
            
            # 检查时间戳差异(用于调试)
            time_diff = abs(
                image_msg.header.stamp.sec - detection_msg.header.stamp.sec +
                (image_msg.header.stamp.nanosec - detection_msg.header.stamp.nanosec) / 1e9
            )
            
            if time_diff > 0.05:  # 如果时间差超过50ms,记录警告
                self.get_logger().warn(f'时间戳差异: {time_diff:.3f}秒')
            
            # 处理分割
            if len(detection_msg.detections) > 0:
                self.process_segmentation(cv_image, detection_msg, image_msg.header)
                
        except Exception as e:
            self.get_logger().error(f'同步回调错误: {e}')
    
    def process_segmentation(self, image, detections: Detection2DArray, header):
        """处理分割"""
        if len(detections.detections) == 0:
            return
        
        # 设置图像
        self.predictor.set_image(image)
        
        # 创建掩码图像
        h, w = image.shape[:2] # 获取图像高度和宽度，只取前两个维度，第3个维度是通道数，不要
        combined_mask = np.zeros((h, w), dtype=np.uint8) # 创建一个与图像大小相同的掩码，类型为uint8
        annotated_image = image.copy() # 复制图像
        
        # 为每个检测框生成分割掩码
        for detection in detections.detections:
            bbox = detection.bbox
            
            # 提取边界框坐标
            cx = bbox.center.position.x
            cy = bbox.center.position.y
            w_box = bbox.size_x
            h_box = bbox.size_y
            
            # 转换为xyxy格式
            x1 = int(cx - w_box / 2)
            y1 = int(cy - h_box / 2)
            x2 = int(cx + w_box / 2)
            y2 = int(cy + h_box / 2)
            
            # 使用边界框作为提示进行分割
            input_box = np.array([x1, y1, x2, y2])
            
            try:
                masks, scores, logits = self.predictor.predict(
                    box=input_box,
                    multimask_output=False
                )
                
                # 使用第一个掩码
                mask = masks[0]
                
                # 合并到总掩码
                combined_mask[mask] = 255
                
                # 在标注图像上绘制掩码
                color_mask = np.zeros_like(image)
                color = np.random.randint(0, 255, 3).tolist()
                color_mask[mask] = color
                annotated_image = cv2.addWeighted(annotated_image, 1, color_mask, 0.5, 0)
                
                # 绘制边界框
                cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 2)
                
                self.segmentation_count += 1
                
            except Exception as e:
                self.get_logger().warn(f'分割失败: {e}')
        
        # 发布掩码图像
        mask_msg = self.bridge.cv2_to_imgmsg(combined_mask, encoding='mono8')
        mask_msg.header = header
        self.mask_pub.publish(mask_msg)
        
        # 发布标注图像
        if self.publish_annotated:
            annotated_msg = self.bridge.cv2_to_imgmsg(annotated_image, encoding='bgr8')
            annotated_msg.header = header
            self.annotated_pub.publish(annotated_msg)
        
        # 统计
        self.frame_count += 1
        if self.frame_count % 30 == 0:
            avg_segments = self.segmentation_count / self.frame_count
            self.get_logger().info(
                f'已处理 {self.frame_count} 帧, '
                f'平均分割数: {avg_segments:.2f}'
            )


def main(args=None):
    rclpy.init(args=args)
    
    try:
        node = SamSegmenterNode()
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
