#!/usr/bin/env python3
"""
YOLO 检测测试脚本
用于测试 YOLO 检测节点是否正常工作
"""

import rclpy
from rclpy.node import Node
from vision_msgs.msg import Detection2DArray


class YoloTestNode(Node):
    """测试节点：订阅并打印 YOLO 检测结果"""
    
    def __init__(self):
        super().__init__('yolo_test')
        
        self.subscription = self.create_subscription(
            Detection2DArray,
            '/yolo/detections',
            self.detection_callback,
            10
        )
        
        self.get_logger().info('YOLO 测试节点已启动，等待检测结果...')
    
    def detection_callback(self, msg: Detection2DArray):
        """打印检测结果"""
        num_detections = len(msg.detections)
        
        if num_detections == 0:
            self.get_logger().info('未检测到物体')
            return
        
        self.get_logger().info(f'检测到 {num_detections} 个物体:')
        
        for i, detection in enumerate(msg.detections):
            if detection.results:
                class_id = detection.results[0].hypothesis.class_id
                score = detection.results[0].hypothesis.score
                
                bbox = detection.bbox
                center_x = bbox.center.position.x
                center_y = bbox.center.position.y
                size_x = bbox.size_x
                size_y = bbox.size_y
                
                self.get_logger().info(
                    f'  [{i+1}] {class_id}: {score:.2f} | '
                    f'中心=({center_x:.1f}, {center_y:.1f}) | '
                    f'大小=({size_x:.1f}x{size_y:.1f})'
                )


def main(args=None):
    rclpy.init(args=args)
    node = YoloTestNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
