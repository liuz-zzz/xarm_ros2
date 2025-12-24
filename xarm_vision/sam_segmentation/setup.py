from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'sam_segmentation'

setup(
    name='sam-segmentation',
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
            glob('models/*.pth')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='liuz',
    maintainer_email='liuz_z@163.com',
    description='SAM (Segment Anything Model) image segmentation for ROS2',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'sam_segmenter = sam_segmentation.sam_segmenter_node:main',
        ],
    },
)
