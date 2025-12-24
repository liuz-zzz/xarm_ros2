from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'yolo_detection'

setup(
    name='yolo-detection',
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # 安装 launch 文件
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
        # 安装配置文件
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),
        # 安装模型文件
        (os.path.join('share', package_name, 'models'),
            glob('models/*.pt')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='liuz',
    maintainer_email='liuz_z@163.com',
    description='YOLO object detection for ROS2',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'yolo_detector = yolo_detection.yolo_detector_node:main',
        ],
    },
)
