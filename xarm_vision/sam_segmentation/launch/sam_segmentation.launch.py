from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # 声明启动参数
    use_yolo_arg = DeclareLaunchArgument(
        'use_yolo',
        default_value='true',
        description='是否启动 YOLO 检测节点'
    )
    
    use_camera_arg = DeclareLaunchArgument(
        'use_camera',
        default_value='true',
        description='是否启动 RealSense 相机'
    )
    
    # 获取配置文件路径
    config_file = PathJoinSubstitution([
        FindPackageShare('sam_segmentation'),
        'config',
        'sam_params.yaml'
    ])
    
    # SAM 分割节点
    sam_node = Node(
        package='sam_segmentation',
        executable='sam_segmenter',
        name='sam_segmenter',
        output='screen',
        parameters=[config_file],
        emulate_tty=True,
    )
    
    # YOLO 检测启动（可选）
    yolo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('yolo_detection'),
                'launch',
                'yolo_detection.launch.py'
            ])
        ),
        launch_arguments={
            'use_camera': LaunchConfiguration('use_camera'),
        }.items(),
        condition=IfCondition(LaunchConfiguration('use_yolo'))
    )
    
    return LaunchDescription([
        use_yolo_arg,
        use_camera_arg,
        yolo_launch,
        sam_node,
    ])
