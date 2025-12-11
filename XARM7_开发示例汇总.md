# xArm7 开发示例汇总

本文档汇总了 xarm_ros2 中所有可用的示例程序和启动文件，供开发参考使用。

## 目录
- [1. 基础功能示例](#1-基础功能示例)
- [2. MoveIt 控制示例](#2-moveit-控制示例)
- [3. Planner API 示例](#3-planner-api-示例)
- [4. Gazebo 仿真示例](#4-gazebo-仿真示例)
- [5. MoveIt Servo 控制示例](#5-moveit-servo-控制示例)
- [6. 视觉应用示例](#6-视觉应用示例)
- [7. 双臂控制示例](#7-双臂控制示例)

---

## 1. 基础功能示例

### 1.1 xarm_description - 模型显示

在 RViz 中显示机械臂模型：

```bash
# 基础模型显示
ros2 launch xarm_description xarm7_rviz_display.launch.py

# 带夹爪模型
ros2 launch xarm_description xarm7_rviz_display.launch.py add_gripper:=true

# 带真空吸头模型
ros2 launch xarm_description xarm7_rviz_display.launch.py add_vacuum_gripper:=true

# 带 RealSense D435i 相机模型
ros2 launch xarm_description xarm7_rviz_display.launch.py add_realsense_d435i:=true
```

**相关文件位置：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_description/launch/xarm7_rviz_display.launch.py`

---

### 1.2 xarm_api - 驱动节点与服务测试

启动机械臂驱动节点并测试基础服务：

```bash
# 启动驱动节点
ros2 launch xarm_api xarm7_driver.launch.py robot_ip:=192.168.1.117

# 测试 service（在另一个终端）
ros2 run xarm_api test_xarm_ros_client

# 测试 topic
ros2 run xarm_api test_robot_states
```

**常用服务命令示例：**

```bash
# 使能所有关节
ros2 service call /xarm/motion_enable xarm_msgs/srv/SetInt16ById "{id: 8, data: 1}"

# 设置模式和状态
ros2 service call /xarm/set_mode xarm_msgs/srv/SetInt16 "{data: 0}"
ros2 service call /xarm/set_state xarm_msgs/srv/SetInt16 "{data: 0}"

# 笛卡尔直线运动 (单位: mm, rad)
ros2 service call /xarm/set_position xarm_msgs/srv/MoveCartesian "{pose: [300, 0, 250, 3.14, 0, 0], speed: 50, acc: 500, mvtime: 0}"

# 关节运动 (单位: rad)
ros2 service call /xarm/set_servo_angle xarm_msgs/srv/MoveJoint "{angles: [0, 0, 0, 0, 0, 0, 0], speed: 0.35, acc: 10, mvtime: 0}"
```

**相关文件位置：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_api/launch/xarm7_driver.launch.py`

---

### 1.3 xarm_controller - ROS2 Control 接口

使用 ros2_control 控制机械臂：

```bash
# 启动控制器并在 RViz 中显示
ros2 launch xarm_controller xarm7_control_rviz_display.launch.py robot_ip:=192.168.1.117

# 带夹爪
ros2 launch xarm_controller xarm7_control_rviz_display.launch.py robot_ip:=192.168.1.117 add_gripper:=true
```

**相关文件位置：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_controller/launch/`

---

## 2. MoveIt 控制示例

### 2.1 虚拟环境（Fake）

在虚拟环境中使用 MoveIt 控制：

```bash
# 基础虚拟控制
ros2 launch xarm_moveit_config xarm7_moveit_fake.launch.py

# 带夹爪
ros2 launch xarm_moveit_config xarm7_moveit_fake.launch.py add_gripper:=true

# 带真空吸头
ros2 launch xarm_moveit_config xarm7_moveit_fake.launch.py add_vacuum_gripper:=true

# 带 RealSense D435i
ros2 launch xarm_moveit_config xarm7_moveit_fake.launch.py add_realsense_d435i:=true
```

**相关文件位置：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_moveit_config/launch/xarm7_moveit_fake.launch.py`

---

### 2.2 真机控制（Realmove）

连接真实机械臂使用 MoveIt 控制：

```bash
# 基础真机控制
ros2 launch xarm_moveit_config xarm7_moveit_realmove.launch.py robot_ip:=192.168.1.117

# 带夹爪
ros2 launch xarm_moveit_config xarm7_moveit_realmove.launch.py robot_ip:=192.168.1.117 add_gripper:=true

# 带真空吸头
ros2 launch xarm_moveit_config xarm7_moveit_realmove.launch.py robot_ip:=192.168.1.117 add_vacuum_gripper:=true

# 使用运动学校准参数（2023年8月后生产的机械臂）
ros2 launch xarm_moveit_config xarm7_moveit_realmove.launch.py robot_ip:=192.168.1.117 kinematics_suffix:=AAA
```

**相关文件位置：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_moveit_config/launch/xarm7_moveit_realmove.launch.py`

---

### 2.3 MoveIt Demo 示例

交互式 MoveIt 演示：

```bash
# 虚拟环境 Demo
ros2 launch xarm_moveit_config demo/demo_fake.launch.py

# 真机 Demo
ros2 launch xarm_moveit_config demo/demo_realmove.launch.py robot_ip:=192.168.1.117
```

**相关文件位置：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_moveit_config/launch/demo/demo_fake.launch.py`
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_moveit_config/launch/demo/demo_realmove.launch.py`

---

## 3. Planner API 示例

### 3.1 虚拟环境 Planner

```bash
# 启动虚拟 planner 节点
ros2 launch xarm_planner xarm7_planner_fake.launch.py

# 带夹爪
ros2 launch xarm_planner xarm7_planner_fake.launch.py add_gripper:=true
```

---

### 3.2 真机 Planner

```bash
# 启动真机 planner 节点
ros2 launch xarm_planner xarm7_planner_realmove.launch.py robot_ip:=192.168.1.117

# 带夹爪
ros2 launch xarm_planner xarm7_planner_realmove.launch.py robot_ip:=192.168.1.117 add_gripper:=true
```

**相关文件位置：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_planner/launch/xarm7_planner_fake.launch.py`
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_planner/launch/xarm7_planner_realmove.launch.py`

---

### 3.3 Planner 测试示例

启动 planner 后，在另一个终端运行测试：

```bash
# 通过 API 控制关节运动
ros2 launch xarm_planner test_xarm_planner_api_joint.launch.py dof:=7 robot_type:=xarm

# 通过 API 控制笛卡尔运动
ros2 launch xarm_planner test_xarm_planner_api_pose.launch.py dof:=7 robot_type:=xarm

# 通过 service 控制关节运动
ros2 launch xarm_planner test_xarm_planner_client_joint.launch.py dof:=7

# 通过 service 控制笛卡尔运动
ros2 launch xarm_planner test_xarm_planner_client_pose.launch.py dof:=7

# 测试夹爪控制（API）
ros2 launch xarm_planner test_xarm_gripper_planner_api_joint.launch.py dof:=7

# 测试夹爪控制（service）
ros2 launch xarm_planner test_xarm_gripper_planner_client_joint.launch.py dof:=7
```

**相关文件位置：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_planner/launch/test_xarm_planner_api_joint.launch.py`
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_planner/launch/test_xarm_planner_api_pose.launch.py`
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_planner/launch/test_xarm_planner_client_joint.launch.py`
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_planner/launch/test_xarm_planner_client_pose.launch.py`
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_planner/launch/test_xarm_gripper_planner_api_joint.launch.py`
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_planner/launch/test_xarm_gripper_planner_client_joint.launch.py`

---

## 4. Gazebo 仿真示例

### 4.1 单独 Gazebo 显示

```bash
# 基础 Gazebo 仿真
ros2 launch xarm_gazebo xarm7_beside_table_gazebo.launch.py

# 带夹爪
ros2 launch xarm_gazebo xarm7_beside_table_gazebo.launch.py add_gripper:=true

# 带自定义末端工具（圆柱体示例）
ros2 launch xarm_gazebo xarm7_beside_table_gazebo.launch.py add_other_geometry:=true geometry_type:=cylinder geometry_height:=0.075 geometry_radius:=0.045
```

**相关文件位置：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_gazebo/launch/xarm7_beside_table_gazebo.launch.py`

---

### 4.2 MoveIt + Gazebo 联合控制

```bash
# 基础联合控制
ros2 launch xarm_moveit_config xarm7_moveit_gazebo.launch.py

# 带夹爪
ros2 launch xarm_moveit_config xarm7_moveit_gazebo.launch.py add_gripper:=true

# 带真空吸头
ros2 launch xarm_moveit_config xarm7_moveit_gazebo.launch.py add_vacuum_gripper:=true
```

**相关文件位置：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_moveit_config/launch/xarm7_moveit_gazebo.launch.py`

---

## 5. MoveIt Servo 控制示例

基于 MoveIt Servo 的实时控制，支持多种输入设备。

### 5.1 键盘控制

```bash
# 虚拟环境
ros2 launch xarm_moveit_servo xarm_moveit_servo_fake.launch.py dof:=7

# 真机
ros2 launch xarm_moveit_servo xarm_moveit_servo_realmove.launch.py robot_ip:=192.168.1.117 dof:=7

# 在另一个终端启动键盘输入节点
ros2 run xarm_moveit_servo xarm_keyboard_input
```

**键盘控制说明：**
- 按照终端提示使用键盘控制 TCP 位置和姿态

---

### 5.2 XBOX 手柄控制

```bash
# 虚拟环境（有线手柄）
ros2 launch xarm_moveit_servo xarm_moveit_servo_fake.launch.py dof:=7 joystick_type:=1

# 虚拟环境（无线手柄）
ros2 launch xarm_moveit_servo xarm_moveit_servo_fake.launch.py dof:=7 joystick_type:=2

# 真机（有线手柄）
ros2 launch xarm_moveit_servo xarm_moveit_servo_realmove.launch.py robot_ip:=192.168.1.117 dof:=7 joystick_type:=1

# 真机（无线手柄）
ros2 launch xarm_moveit_servo xarm_moveit_servo_realmove.launch.py robot_ip:=192.168.1.117 dof:=7 joystick_type:=2
```

**XBOX 手柄控制说明：**
- 左摇杆：控制 TCP 的 X 和 Y
- 右摇杆：控制 TCP 的 ROLL 和 PITCH
- 左右触发器：控制 TCP 的 Z
- 左右缓冲器：控制 TCP 的 YAW
- 十字键：控制关节 1 和关节 2
- 按键 X 和 B：控制最后一个关节
- 按键 Y 和 A：控制倒数第二个关节

---

### 5.3 SpaceMouse 六维鼠标控制

```bash
# 虚拟环境
ros2 launch xarm_moveit_servo xarm_moveit_servo_fake.launch.py dof:=7 joystick_type:=3

# 真机
ros2 launch xarm_moveit_servo xarm_moveit_servo_realmove.launch.py robot_ip:=192.168.1.117 dof:=7 joystick_type:=3
```

**SpaceMouse 控制说明：**
- 六个维度对应控制 TCP 的 X/Y/Z/ROLL/PITCH/YAW
- 左键：单独控制 XYZ
- 右键：单独控制 ROLL/PITCH/YAW

**相关文件位置：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_moveit_servo/launch/xarm_moveit_servo_fake.launch.py`
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_moveit_servo/launch/xarm_moveit_servo_realmove.launch.py`

---

## 6. 视觉应用示例

### 6.1 手眼标定

使用 RealSense D435i 进行手眼标定（眼在手上）：

```bash
# xArm7 手眼标定
ros2 launch d435i_xarm_setup d435i_robot_auto_calib.launch.py robot_type:=xarm dof:=7 robot_ip:=192.168.1.117

# 使用运动学校准参数（2023年8月后生产）
ros2 launch d435i_xarm_setup d435i_robot_auto_calib.launch.py robot_type:=xarm dof:=7 robot_ip:=192.168.1.117 kinematics_suffix:=AAA
```

**标定步骤：**
1. 准备 ArUco 标定板（可从 https://chev.me/arucogen/ 下载）
2. 启动标定程序
3. 通过拖动示教或 xArm Studio 移动机械臂到不同位置
4. 在标定窗口点击 "Take Sample" 采集数据（建议采集 17 个样本）
5. 点击 "Save" 保存标定结果（保存在 `~/.ros2/easy_handeye2/calibrations/`）

**相关文件位置：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_vision/d435i_xarm_setup/`

---

### 6.2 3D 视觉抓取示例

基于 find_object_2d 的物体识别和抓取。

#### 方法 1：使用 MoveIt 驱动（推荐）

```bash
# 启动视觉识别和 MoveIt 规划
ros2 launch d435i_xarm_setup d435i_findobj2d_robot_moveit_planner.launch.py robot_type:=xarm dof:=7 robot_ip:=192.168.1.117

# 使用自定义标定文件
ros2 launch d435i_xarm_setup d435i_findobj2d_robot_moveit_planner.launch.py robot_type:=xarm dof:=7 robot_ip:=192.168.1.117 calib_filename:=my_calibration

# 在另一个终端启动抓取节点
ros2 launch d435i_xarm_setup grasp_node_robot_moveit_planner.launch.py robot_type:=xarm dof:=7
```

**代码参考：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_vision/d435i_xarm_setup/src/findobj_grasp_moveit_planner.cpp`

---

#### 方法 2：使用 xarm_api 服务驱动

```bash
# 启动视觉识别和 API 控制
ros2 launch d435i_xarm_setup d435i_findobj2d_robot_api.launch.py robot_type:=xarm dof:=7 robot_ip:=192.168.1.117

# 使用自定义标定文件
ros2 launch d435i_xarm_setup d435i_findobj2d_robot_api.launch.py robot_type:=xarm dof:=7 robot_ip:=192.168.1.117 calib_filename:=my_calibration

# 在另一个终端启动抓取节点
ros2 launch d435i_xarm_setup grasp_node_robot_api.launch.py robot_type:=xarm dof:=7
```

**代码参考：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_vision/d435i_xarm_setup/src/findobj_grasp_xarm_api.cpp`

**注意事项：**
- 实际应用前请仔细阅读代码并根据场景修改
- 需要调整的参数：抓取准备位置、姿态、抓取深度、移动速度等
- 识别目标名称默认为 "object_1"，对应 `/objects/1.png`
- 背景应尽量干净，与目标物体有明显区分度
- 目标物体纹理越丰富，识别率越高

---

## 7. 双臂控制示例

### 7.1 双臂虚拟控制

```bash
# 双 xArm7 虚拟控制
ros2 launch xarm_moveit_config dual_xarm7_moveit_fake.launch.py

# 双臂带夹爪
ros2 launch xarm_moveit_config dual_xarm7_moveit_fake.launch.py add_gripper:=true

# 单独指定左右臂配置
ros2 launch xarm_moveit_config dual_xarm7_moveit_fake.launch.py add_gripper_1:=true add_gripper_2:=false dof_1:=7 dof_2:=6
```

---

### 7.2 双臂真机控制

```bash
# 双 xArm7 真机控制
ros2 launch xarm_moveit_config dual_xarm7_moveit_realmove.launch.py robot_ip_1:=192.168.1.117 robot_ip_2:=192.168.1.203

# 双臂带夹爪
ros2 launch xarm_moveit_config dual_xarm7_moveit_realmove.launch.py robot_ip_1:=192.168.1.117 robot_ip_2:=192.168.1.203 add_gripper:=true

# 单独指定左右臂配置
ros2 launch xarm_moveit_config dual_xarm7_moveit_realmove.launch.py robot_ip_1:=192.168.1.117 robot_ip_2:=192.168.1.203 add_gripper_1:=true add_gripper_2:=false dof_1:=7 dof_2:=6
```

**相关文件位置：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_moveit_config/launch/dual_xarm7_moveit_fake.launch.py`
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_moveit_config/launch/dual_xarm7_moveit_realmove.launch.py`

---

### 7.3 双臂 Demo

```bash
# 双臂虚拟 Demo
ros2 launch xarm_moveit_config demo/demo_dual_fake.launch.py

# 双臂真机 Demo
ros2 launch xarm_moveit_config demo/demo_dual_realmove.launch.py robot_ip_1:=192.168.1.117 robot_ip_2:=192.168.1.203
```

**相关文件位置：**
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_moveit_config/launch/demo/demo_dual_fake.launch.py`
- `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_moveit_config/launch/demo/demo_dual_realmove.launch.py`

---

## 8. 其他型号机械臂

本文档以 xArm7 为例，其他型号机械臂（xArm5、xArm6、Lite6、UF850、xArm7_mirror）的使用方法类似，只需将启动文件名中的 `xarm7` 替换为对应型号即可。

### 可用型号列表：
- **xArm5**: `xarm5_*.launch.py`
- **xArm6**: `xarm6_*.launch.py`
- **xArm7**: `xarm7_*.launch.py`
- **xArm7 Mirror**: `xarm7_mirror_*.launch.py`
- **Lite6**: `lite6_*.launch.py`
- **UF850**: `uf850_*.launch.py`

---

## 9. 常用启动参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `robot_ip` | - | 机械臂 IP 地址（真机必需） |
| `dof` | 7 | 机械臂轴数 |
| `add_gripper` | false | 是否添加 xArm 夹爪 |
| `add_vacuum_gripper` | false | 是否添加真空吸头 |
| `add_bio_gripper` | false | 是否添加 BIO 夹爪 |
| `add_realsense_d435i` | false | 是否添加 RealSense D435i 相机 |
| `add_d435i_links` | false | 是否添加 D435i 各摄像头间的连杆关系 |
| `velocity_control` | false | 是否使用速度控制 |
| `report_type` | normal | 上报类型（normal/rich/dev） |
| `kinematics_suffix` | - | 运动学校准参数文件后缀 |
| `add_other_geometry` | false | 是否添加自定义几何模型 |
| `geometry_type` | box | 几何模型类型（box/cylinder/sphere/mesh） |

**双臂参数：**
- `robot_ip_1` / `robot_ip_2`: 左右臂 IP
- `dof_1` / `dof_2`: 左右臂轴数
- `add_gripper_1` / `add_gripper_2`: 左右臂夹爪配置
- 其他参数类似，添加 `_1` 或 `_2` 后缀

---

## 10. 开发资源

### 10.1 源码位置
- **xarm_ros2**: `/home/liuz/Work/dev_ws/src/xarm_ros2/`
- **xarm_api**: `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_api/`
- **xarm_planner**: `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_planner/`
- **xarm_moveit_config**: `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_moveit_config/`
- **xarm_vision**: `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_vision/`

### 10.2 参考文档
- **xarm_api 详细说明**: `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_api/ReadMe.md`
- **xarm_msgs 消息格式**: `/home/liuz/Work/dev_ws/src/xarm_ros2/xarm_msgs/ReadMe.md`
- **uf_ros_lib 工具库**: `/home/liuz/Work/dev_ws/src/xarm_ros2/uf_ros_lib/Readme.md`
- **官方中文文档**: `/home/liuz/Work/dev_ws/src/xarm_ros2/ReadMe_cn.md`
- **官方英文文档**: `/home/liuz/Work/dev_ws/src/xarm_ros2/ReadMe.md`

### 10.3 在线资源
- **GitHub**: https://github.com/xArm-Developer/xarm_ros2
- **xArm SDK**: https://github.com/xArm-Developer/xArm-CPLUS-SDK

---

## 11. 快速开始

### 11.1 环境准备

```bash
# 进入工作区
cd ~/dev_ws/

# source 环境
source install/setup.bash

# 如果局域网有多人使用 ROS2，设置 DOMAIN ID 避免干扰
export ROS_DOMAIN_ID=42  # 选择 0-101 之间的数字
```

### 11.2 第一个示例

```bash
# 1. 虚拟环境测试（无需真机）
ros2 launch xarm_moveit_config xarm7_moveit_fake.launch.py

# 2. 真机测试（需要连接机械臂）
ros2 launch xarm_moveit_config xarm7_moveit_realmove.launch.py robot_ip:=192.168.1.117

# 3. Gazebo 仿真测试
ros2 launch xarm_moveit_config xarm7_moveit_gazebo.launch.py
```

---

## 12. 注意事项

1. **运行前务必 source 环境**：
   ```bash
   cd ~/dev_ws/
   source install/setup.bash
   ```

2. **真机测试前请仔细了解**：
   - Mode（模式）的含义和切换
   - State（状态）的含义和设置
   - 运动指令的安全使用

3. **命名空间**：
   - xArm 系列默认命名空间：`/xarm/`
   - Lite6 和 UF850 默认命名空间：`/ufactory/`

4. **多人使用 ROS2**：
   - 设置不同的 `ROS_DOMAIN_ID` 避免干扰

5. **运动学校准**：
   - 2023年8月后生产的机械臂建议使用 `kinematics_suffix` 参数
   - 需先生成校准参数文件

6. **视觉应用**：
   - 需要额外安装依赖包（RealSense SDK、aruco_ros、easy_handeye2 等）
   - 实际应用前务必理解并修改示例代码

---

## 13. 故障排查

### 13.1 编译问题
```bash
# 清理编译缓存
cd ~/dev_ws/
rm -rf build/ install/ log/

# 重新编译
colcon build
```

### 13.2 连接问题
```bash
# 检查网络连接
ping 192.168.1.117

# 检查机械臂状态
ros2 topic echo /xarm/robot_states
```

### 13.3 权限问题
```bash
# USB 设备权限（手柄、相机等）
sudo chmod 666 /dev/ttyUSB0
sudo chmod 666 /dev/video0
```

---

**文档生成时间**: 2025-12-11  
**适用版本**: ROS2 Humble  
**工作区路径**: `/home/liuz/Work/dev_ws/`
