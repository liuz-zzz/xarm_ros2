#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2025, UFACTORY, Inc.
# All rights reserved.
#
# YOLO Interactive Grasping System Launch File
# Author: AI Assistant

from launch import LaunchDescription
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def launch_setup(context, *args, **kwargs):
    robot_ip = LaunchConfiguration('robot_ip')
    robot_type = LaunchConfiguration('robot_type')
    dof = LaunchConfiguration('dof', default=6)
    hw_ns = LaunchConfiguration('hw_ns', default='')
    calib_filename = LaunchConfiguration('calib_filename', default='')
    yolo_target_class = LaunchConfiguration('yolo_target_class', default='apple')
    yolo_confidence = LaunchConfiguration('yolo_confidence', default='0.5')

    robot_type = robot_type.perform(context)
    dof = dof.perform(context)
    hw_ns = hw_ns.perform(context)
    
    if hw_ns == '':
        hw_ns = 'xarm' if robot_type == 'xarm' else 'ufactory'
    if robot_type == 'lite' or robot_type == 'uf850':
        dof = '6'
    calib_filename = calib_filename.perform(context)
    if calib_filename == '':
        calib_filename = '{}_rs_on_hand_calibration'.format(robot_type)
    else:
        calib_filename = PathJoinSubstitution([FindPackageShare('d435i_xarm_setup'), 'config', calib_filename])

    # 1. RealSense 相机
    rs_camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([FindPackageShare('realsense2_camera'), 'launch', 'rs_launch.py'])),
        launch_arguments={
            'publish_tf': 'false',
            'align_depth.enable': 'true',
        }.items(),
    )
    
    # 2. YOLO 检测节点
    yolo_config_file = PathJoinSubstitution([
        FindPackageShare('yolo_detection'),
        'config',
        'yolo_params.yaml'
    ])
    
    yolo_detector_node = Node(
        package='yolo_detection',
        executable='yolo_detector',
        name='yolo_detector',
        output='screen',
        parameters=[
            yolo_config_file,
            {
                'target_classes': [],  # 空列表表示检测所有类别
                'confidence_threshold': float(yolo_confidence.perform(context)),
            }
        ],
        emulate_tty=True,
    )
    
    # 3. YOLO TF 桥接节点 (交互式版本)
    yolo_tf_bridge_node = Node(
        package='d435i_xarm_setup',
        executable='yolo_tf_bridge_interactive',  # 使用交互式版本
        name='yolo_tf_bridge_interactive',
        output='screen',
        parameters=[{
            'object_frame_id': 'object_1',
            'camera_frame_id': 'camera_color_optical_frame',
            'min_confidence': float(yolo_confidence.perform(context)),
            'enable_gui': True,  # 启用GUI
        }]
    )

    # 4. 机械臂驱动
    extra_robot_api_params_path = PathJoinSubstitution([FindPackageShare('d435i_xarm_setup'), 'config', 'extra_robot_api_params.yaml'])
    robot_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([FindPackageShare('xarm_api'), 'launch', '_robot_driver.launch.py'])),
        launch_arguments={
            'robot_ip': robot_ip,
            'robot_type': robot_type,
            'dof': dof,
            'hw_ns': hw_ns,
            'add_gripper': 'true' if robot_type != 'lite' else 'false',
            'add_vacuum_gripper': 'true' if robot_type == 'lite' else 'false',
            'extra_robot_api_params_path': extra_robot_api_params_path
        }.items(),
    )

    # 5. RViz 可视化
    rviz_display_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([FindPackageShare('xarm_description'), 'launch', '_robot_rviz_display.launch.py'])),
        launch_arguments={
            'robot_type': robot_type,
            'dof': dof,
            'hw_ns': hw_ns,
            'add_gripper': 'true' if robot_type != 'lite' else 'false',
            'add_vacuum_gripper': 'true' if robot_type == 'lite' else 'false',
            'limited': 'false',
        }.items(),
    )

    # 6. 手眼标定 TF
    publish_handeye_tf_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([FindPackageShare('d435i_xarm_setup'), 'launch', 'publish_handeye_tf.launch.py'])),
        launch_arguments={
            'calib_filename': calib_filename,
        }.items(),
    )
    
    # 7. 抓取节点 (立即启动,内部等待TF最多15秒)
    grasp_node = Node(
        package='d435i_xarm_setup',
        executable='findobj_grasp_xarm_api',
        parameters=[{
            'robot_type': robot_type,
            'dof': int(dof),
            'hw_ns': hw_ns,
        }],
        output='screen'
    )

    return [
        rs_camera_launch,
        yolo_detector_node,
        yolo_tf_bridge_node,
        robot_driver_launch,
        rviz_display_launch,
        publish_handeye_tf_launch,
        grasp_node,  # 立即启动,等待用户点击选择(15秒内)
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('robot_ip', description='机械臂IP地址'),
        DeclareLaunchArgument('robot_type', default_value='xarm', description='机器人类型'),
        DeclareLaunchArgument('dof', default_value='7', description='机械臂自由度'),
        DeclareLaunchArgument('hw_ns', default_value='', description='硬件命名空间'),
        DeclareLaunchArgument('calib_filename', default_value='', description='标定文件名'),
        DeclareLaunchArgument('yolo_target_class', default_value='apple', description='YOLO目标类别(交互式模式忽略)'),
        DeclareLaunchArgument('yolo_confidence', default_value='0.5', description='YOLO置信度阈值'),
        OpaqueFunction(function=launch_setup)
    ])
