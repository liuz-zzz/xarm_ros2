#!/usr/bin/env python3
"""
YOLO 检测启动文件
启动 YOLO 检测节点和相机（可选）
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # 声明启动参数
    use_camera_arg = DeclareLaunchArgument(
        'use_camera',
        default_value='true',
        description='是否启动 RealSense 相机'
    )
    
    # 获取配置文件路径
    config_file = PathJoinSubstitution([
        FindPackageShare('yolo_detection'),
        'config',
        'yolo_params.yaml'
    ])
    
    # YOLO 检测节点
    yolo_node = Node(
        package='yolo_detection',
        executable='yolo_detector',
        name='yolo_detector',
        output='screen',
        parameters=[config_file],  # 只使用 YAML 配置文件
        emulate_tty=True,
    )
    
    # RealSense 相机启动（可选）
    camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('realsense2_camera'),
                'launch',
                'rs_launch.py'
            ])
        ),
        launch_arguments={
            'publish_tf': 'false',
            'align_depth.enable': 'true',
        }.items(),
        condition=IfCondition(LaunchConfiguration('use_camera'))
    )
    
    return LaunchDescription([
        use_camera_arg,
        camera_launch,
        yolo_node,
    ])
