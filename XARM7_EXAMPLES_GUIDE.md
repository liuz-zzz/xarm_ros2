# xArm7 开发示例程序完整指南

本文档汇总了 xArm7 ROS2 工作空间中所有可用的示例程序、测试代码和开发资源，方便您快速开始开发。

## 目录
- [1. 快速启动示例](#1-快速启动示例)
- [2. MoveIt 运动规划示例](#2-moveit-运动规划示例)
- [3. xArm Planner API 示例](#3-xarm-planner-api-示例)
- [4. xArm SDK C++ 示例](#4-xarm-sdk-c-示例)
- [5. 视觉抓取示例](#5-视觉抓取示例)
- [6. Gazebo 仿真示例](#6-gazebo-仿真示例)
- [7. 控制器示例](#7-控制器示例)
- [8. 移动底盘集成示例](#8-移动底盘集成示例)

---

## 1. 快速启动示例

### 1.1 启动真实机械臂驱动

```bash
# 启动 xArm7 驱动（替换为您的机械臂IP）
ros2 launch xarm_api xarm7_driver.launch.py robot_ip:=192.168.1.xxx

# 启动 xArm6 驱动
ros2 launch xarm_api xarm6_driver.launch.py robot_ip:=192.168.1.xxx

# 启动 xArm5 驱动
ros2 launch xarm_api xarm5_driver.launch.py robot_ip:=192.168.1.xxx

# 启动 Lite6 驱动
ros2 launch xarm_api lite6_driver.launch.py robot_ip:=192.168.1.xxx

# 启动 UF850 驱动
ros2 launch xarm_api uf850_driver.launch.py robot_ip:=192.168.1.xxx
```

**可用参数**：
- `robot_ip`: 机械臂IP地址（必需）
- `report_type`: 报告类型（默认: normal）
- `dof`: 自由度（xArm7默认为7）
- `add_gripper`: 是否添加夹爪（默认: false）
- `add_vacuum_gripper`: 是否添加真空夹爪（默认: false）
- `add_bio_gripper`: 是否添加BIO夹爪（默认: false）

### 1.2 可视化显示

```bash
# 仅显示机械臂模型（不连接真机）
ros2 launch xarm_description xarm7_rviz_display.launch.py

# 使用 ros2_control 控制并显示
ros2 launch xarm_controller xarm7_control_rviz_display.launch.py
```

---

## 2. MoveIt 运动规划示例

### 2.1 MoveIt 仿真模式（Fake模式）

```bash
# xArm7 MoveIt 仿真
ros2 launch xarm_moveit_config xarm7_moveit_fake.launch.py

# 带夹爪的 MoveIt 仿真
ros2 launch xarm_moveit_config xarm7_moveit_fake.launch.py add_gripper:=true

# 双臂 MoveIt 仿真
ros2 launch xarm_moveit_config dual_xarm7_moveit_fake.launch.py
```

### 2.2 MoveIt 控制真实机械臂

```bash
# xArm7 MoveIt 真机控制
ros2 launch xarm_moveit_config xarm7_moveit_realmove.launch.py \
  robot_ip:=192.168.1.xxx

# 带夹爪的真机控制
ros2 launch xarm_moveit_config xarm7_moveit_realmove.launch.py \
  robot_ip:=192.168.1.xxx \
  add_gripper:=true

# 双臂真机控制
ros2 launch xarm_moveit_config dual_xarm7_moveit_realmove.launch.py \
  robot_ip_1:=192.168.1.xxx \
  robot_ip_2:=192.168.1.yyy
```

### 2.3 MoveIt Servo 实时控制

```bash
# 启动 MoveIt Servo（实时笛卡尔控制）
ros2 launch xarm_moveit_servo xarm_moveit_servo_realmove.launch.py \
  robot_ip:=192.168.1.xxx \
  dof:=7
```

### 2.4 MoveIt 演示启动文件

位置：`src/xarm_ros2/xarm_moveit_config/launch/demo/`

```bash
# 仿真模式演示
ros2 launch xarm_moveit_config demo_fake.launch.py

# 真机模式演示
ros2 launch xarm_moveit_config demo_realmove.launch.py robot_ip:=192.168.1.xxx

# 双臂仿真演示
ros2 launch xarm_moveit_config demo_dual_fake.launch.py

# 双臂真机演示
ros2 launch xarm_moveit_config demo_dual_realmove.launch.py \
  robot_ip_1:=192.168.1.xxx \
  robot_ip_2:=192.168.1.yyy
```

---

## 3. xArm Planner API 示例

### 3.1 测试程序列表

位置：`src/xarm_ros2/xarm_planner/test/`

#### 3.1.1 单臂关节空间规划

**文件**: `test_xarm_planner_api_joint.cpp`

```bash
# 编译后运行
ros2 run xarm_planner test_xarm_planner_api_joint
```

**功能**：
- 使用 xArm Planner API 进行关节空间运动规划
- 示例代码展示如何设置目标关节角度
- 执行规划并控制机械臂运动

**关键代码片段**：
```cpp
// 设置目标关节角度
std::vector<double> target_joint = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
// 执行规划
planner->planJointTarget(target_joint);
```

#### 3.1.2 单臂笛卡尔空间规划

**文件**: `test_xarm_planner_api_pose.cpp`

```bash
ros2 run xarm_planner test_xarm_planner_api_pose
```

**功能**：
- 笛卡尔空间目标位姿规划
- 位置和姿态控制示例

#### 3.1.3 使用 Service Client 的关节规划

**文件**: `test_xarm_planner_client_joint.cpp`

```bash
ros2 run xarm_planner test_xarm_planner_client_joint
```

**功能**：
- 通过 ROS2 服务调用进行运动规划
- 异步规划和执行

#### 3.1.4 使用 Service Client 的位姿规划

**文件**: `test_xarm_planner_client_pose.cpp`

```bash
ros2 run xarm_planner test_xarm_planner_client_pose
```

#### 3.1.5 带夹爪的规划示例

**文件**: `test_xarm_gripper_planner_api_joint.cpp`

```bash
ros2 run xarm_planner test_xarm_gripper_planner_api_joint
```

**功能**：
- 机械臂运动 + 夹爪控制
- 抓取和放置动作示例

**文件**: `test_xarm_gripper_planner_client_joint.cpp`

```bash
ros2 run xarm_planner test_xarm_gripper_planner_client_joint
```

#### 3.1.6 Lite6 夹爪真机控制

**文件**: `test_lite_gripper_realmove.cpp`

```bash
ros2 run xarm_planner test_lite_gripper_realmove
```

**功能**：
- Lite6 机械臂夹爪控制示例
- 真机运动测试

#### 3.1.7 双臂协同规划

**文件**: `test_dual_xarm_planner_api_joint.cpp`

```bash
ros2 run xarm_planner test_dual_xarm_planner_api_joint
```

**功能**：
- 双臂协同运动规划
- 左右臂独立控制
- 同步运动示例

---

## 4. xArm SDK C++ 示例

位置：`src/xarm_ros2/xarm_sdk/cxx/example/`

这些是底层 SDK 的示例程序，展示了如何直接使用 xArm C++ API。

### 4.1 基础功能示例

#### 事件注册和属性获取

```bash
# 0001 - 事件注册示例
./0001-event_register <robot_ip>

# 0002 - 获取机械臂属性
./0002-get_property <robot_ip>

# 0003 - API 获取示例
./0003-api_get <robot_ip>

# 0004 - 伺服电机连接/断开
./0004-servo_attach_detach <robot_ip>
```

### 4.2 直线运动示例

```bash
# 1001 - 直线运动
./1001-move_line <robot_ip>

# 1004 - 圆弧+直线组合运动
./1004-move_arc_line <robot_ip>

# 1006 - 工具坐标系直线运动
./1006-move_tool_line <robot_ip>

# 1008 - 轴角表示的直线运动
./1008-move_line_aa <robot_ip>
```

### 4.3 速度控制示例

```bash
# 1009 - 笛卡尔速度控制
./1009-cartesian_velocity_control <robot_ip>

# 2000 - 关节速度控制
./2000-joint_velocity_control <robot_ip>
```

### 4.4 关节运动示例

```bash
# 2001 - 关节运动
./2001-move_joint <robot_ip>
```

### 4.5 圆弧运动示例

```bash
# 3001 - 圆弧运动
./3001-move_circle <robot_ip>
```

### 4.6 轨迹记录和回放

```bash
# 3002 - 记录轨迹
./3002-record_trajectory <robot_ip>

# 3003 - 回放轨迹
./3003-playback_trajectory <robot_ip>
```

### 4.7 数据获取和反馈

```bash
# 3004 - 获取报告数据
./3004-get_report_data <robot_ip>

# 3005 - 任务反馈
./3005-task_feedback <robot_ip>
```

### 4.8 IO 控制示例

```bash
# 5001 - 获取工具端数字IO
./5001-get_tgpio_digital <robot_ip>

# 5002 - 获取工具端模拟IO
./5002-get_tgpio_analog <robot_ip>

# 5003 - 设置工具端数字IO
./5003-set_tgpio_digital <robot_ip>

# 5005 - 获取控制器GPIO数字和模拟IO
./5005-get_cgpio_digital_analog <robot_ip>

# 5006 - 设置控制器GPIO数字和模拟IO
./5006-set_cgpio_digital_analog <robot_ip>

# 5008 - 获取控制器GPIO状态
./5008-get_cgpio_state <robot_ip>
```

### 4.9 夹爪控制示例

```bash
# 5004 - xArm 夹爪控制
./5004-set_gripper <robot_ip>

# 5009 - BIO 夹爪控制
./5009-set_bio_gripper <robot_ip>

# Robotiq 夹爪控制
./thirdparty-set_robotiq_gripper <robot_ip>

# 因时夹爪控制
./thirdparty-set_yinshi_gripper <robot_ip>
```

### 4.10 安全功能示例

```bash
# 6001 - 设置缩减模式
./6001-set_reduced_mode <robot_ip>

# 6002 - 设置围栏模式
./6002-set_fense_mode <robot_ip>
```

### 4.11 伺服运动示例

```bash
# 7001 - 关节伺服运动
./7001-servo_j <robot_ip>

# 7002 - 笛卡尔伺服运动
./7002-servo_cartesian <robot_ip>

# 7003 - 轴角表示的笛卡尔伺服
./7003-servo_cartesian_aa <robot_ip>
```

### 4.12 力控功能示例

```bash
# 8000 - 负载识别（电流法）
./8000-load_identify_current <robot_ip>

# 8001 - 力控技术
./8001-force_tech <robot_ip>

# 8002 - 导纳控制
./8002-admittance_control <robot_ip>

# 8003 - 力控制
./8003-force_control <robot_ip>

# 8004 - 负载识别
./8004-load_identify <robot_ip>

# 8005 - 读取力传感器数据
./8005-read_force_data <robot_ip>

# 8006 - 保存力传感器零点
./8006-save_force_zero <robot_ip>

# 8010 - 获取力传感器配置
./8010-get_ft_sensor_config <robot_ip>
```

### 4.13 直线电机/滑轨示例

```bash
# 9000 - 直线电机控制
./9000-set_linear_motor <robot_ip>
```

### 4.14 Modbus 通信示例

```bash
# 3006 - 标准 Modbus TCP
./3006-standard_modbus_tcp <robot_ip>

# 5000 - 设置工具端 Modbus
./5000-set_tgpio_modbus <robot_ip>
```

### 4.15 其他功能

```bash
# 1007 - 计数器
./1007-counter <robot_ip>

# 10086 - 校准偏移
./10086-cali_offset <robot_ip>
```

---

## 5. 视觉抓取示例

位置：`src/xarm_ros2/xarm_vision/d435i_xarm_setup/`

### 5.1 RealSense D435i 相机集成

#### 5.1.1 2D 物体识别和抓取（使用 xArm API）

```bash
# 启动 2D 物体识别
ros2 launch d435i_xarm_setup d435i_findobj2d_robot_api.launch.py \
  robot_ip:=192.168.1.xxx \
  dof:=7

# 或使用独立节点
ros2 launch d435i_xarm_setup start_find_obj_2d.launch.py
ros2 launch d435i_xarm_setup grasp_node_robot_api.launch.py \
  robot_ip:=192.168.1.xxx
```

**功能**：
- 使用 RealSense D435i 相机进行 2D 物体检测
- 自动计算抓取位置
- 使用 xArm API 执行抓取动作

**源码**: `src/findobj_grasp_xarm_api.cpp`

#### 5.1.2 2D 物体识别和抓取（使用 MoveIt Planner）

```bash
ros2 launch d435i_xarm_setup d435i_findobj2d_robot_moveit_planner.launch.py \
  robot_ip:=192.168.1.xxx \
  dof:=7

# 或使用独立节点
ros2 launch d435i_xarm_setup grasp_node_robot_moveit_planner.launch.py \
  robot_ip:=192.168.1.xxx
```

**功能**：
- 2D 物体检测
- 使用 MoveIt 进行运动规划
- 避障抓取

**源码**: `src/findobj_grasp_moveit_planner.cpp`

#### 5.1.3 ORK Linemod 3D 物体识别

```bash
ros2 launch d435i_xarm_setup d435i_robot_ork_linemod.launch.py \
  robot_ip:=192.168.1.xxx \
  dof:=7
```

**功能**：
- 使用 ORK (Object Recognition Kitchen) 进行 3D 物体识别
- Linemod 算法
- 6D 位姿估计

#### 5.1.4 手眼标定

```bash
# 自动手眼标定
ros2 launch d435i_xarm_setup d435i_robot_auto_calib.launch.py \
  robot_ip:=192.168.1.xxx \
  dof:=7

# 发布手眼标定 TF
ros2 launch d435i_xarm_setup publish_handeye_tf.launch.py
```

**功能**：
- 自动执行手眼标定流程
- 计算相机到机械臂基座的变换
- 保存标定结果

#### 5.1.5 TF 变换工具

**源码**: `src/tf_object_to_base.cpp`

**功能**：
- 将物体坐标从相机坐标系转换到机械臂基座坐标系
- 用于抓取位置计算

---

## 6. Gazebo 仿真示例

### 6.1 基础 Gazebo 仿真

```bash
# xArm7 Gazebo 仿真
ros2 launch xarm_gazebo xarm7_beside_table_gazebo.launch.py

# 带夹爪的 Gazebo 仿真
ros2 launch xarm_gazebo xarm7_beside_table_gazebo.launch.py add_gripper:=true

# 双臂 Gazebo 仿真
ros2 launch xarm_gazebo dual_xarm7_beside_table_gazebo.launch.py
```

### 6.2 Gazebo + MoveIt 仿真

```bash
# xArm7 Gazebo + MoveIt
ros2 launch xarm_moveit_config xarm7_moveit_gazebo.launch.py

# 双臂 Gazebo + MoveIt
ros2 launch xarm_moveit_config dual_xarm7_moveit_gazebo.launch.py
```

### 6.3 其他机型 Gazebo 仿真

```bash
# Lite6
ros2 launch xarm_gazebo lite6_beside_table_gazebo.launch.py

# xArm6
ros2 launch xarm_gazebo xarm6_beside_table_gazebo.launch.py

# xArm5
ros2 launch xarm_gazebo xarm5_beside_table_gazebo.launch.py

# UF850
ros2 launch xarm_gazebo uf850_beside_table_gazebo.launch.py
```

---

## 7. 控制器示例

### 7.1 ros2_control 控制器

```bash
# xArm7 控制器 + RViz
ros2 launch xarm_controller xarm7_control_rviz_display.launch.py

# 双臂控制器
ros2 launch xarm_controller dual_xarm7_control_rviz_display.launch.py
```

### 7.2 可用的控制器类型

- **位置控制器** (position_controllers)
- **速度控制器** (velocity_controllers)
- **轨迹控制器** (joint_trajectory_controller)

---

## 8. 移动底盘集成示例

位置：`src/xarm_ros2/demo/mbot_demo/`

### 8.1 移动底盘 + 机械臂仿真

```bash
# Gazebo 仿真
ros2 launch mbot_demo mbot_moveit_gazebo.launch.py

# Fake 模式
ros2 launch mbot_demo mbot_moveit_fake.launch.py

# 真机模式
ros2 launch mbot_demo mbot_moveit_realmove.launch.py robot_ip:=192.168.1.xxx
```

**功能**：
- 展示如何将 xArm 机械臂安装在移动底盘上
- 底盘 + 机械臂联合控制
- MoveIt 全身规划

**文档**: `src/xarm_ros2/demo/mbot_demo/readme.md`

---

## 9. 开发工具和库

### 9.1 uf_ros_lib 工具库

位置：`src/xarm_ros2/uf_ros_lib/`

**功能**：
- `MoveItConfigsBuilder`: MoveIt 配置构建器
- 参数描述工具
- 机器人工具函数

**文档**: `src/xarm_ros2/uf_ros_lib/Readme.md`

**使用示例**：
```python
from uf_ros_lib.moveit_configs_builder import MoveItConfigsBuilder

# 构建 MoveIt 配置
moveit_config = MoveItConfigsBuilder(
    robot_type='xarm',
    dof=7,
    robot_ip='192.168.1.xxx'
).to_moveit_configs()
```

---

## 10. 快速开发模板

### 10.1 Python 服务调用模板

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from xarm_msgs.srv import MoveCartesian, SetInt16

class XArmController(Node):
    def __init__(self):
        super().__init__('xarm_controller')
        
        # 创建服务客户端
        self.set_mode_client = self.create_client(SetInt16, '/xarm/set_mode')
        self.set_state_client = self.create_client(SetInt16, '/xarm/set_state')
        self.move_client = self.create_client(MoveCartesian, '/xarm/set_position')
        
    def set_mode(self, mode):
        """设置控制模式"""
        request = SetInt16.Request()
        request.data = mode
        future = self.set_mode_client.call_async(request)
        return future
        
    def move_to_position(self, x, y, z, roll, pitch, yaw, speed=100, acc=500):
        """移动到指定位置"""
        request = MoveCartesian.Request()
        request.pose = [x, y, z, roll, pitch, yaw]
        request.mvvelo = speed
        request.mvacc = acc
        future = self.move_client.call_async(request)
        return future

def main():
    rclpy.init()
    controller = XArmController()
    
    # 设置模式为0（位置模式）
    future = controller.set_mode(0)
    rclpy.spin_until_future_complete(controller, future)
    
    # 移动到目标位置
    future = controller.move_to_position(300, 0, 300, 3.14, 0, 0)
    rclpy.spin_until_future_complete(controller, future)
    
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 10.2 C++ MoveIt 规划模板

```cpp
#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>

int main(int argc, char** argv)
{
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("xarm_moveit_example");
    
    // 创建 MoveGroup 接口
    moveit::planning_interface::MoveGroupInterface move_group(node, "xarm7");
    
    // 设置目标位姿
    geometry_msgs::msg::Pose target_pose;
    target_pose.position.x = 0.3;
    target_pose.position.y = 0.0;
    target_pose.position.z = 0.3;
    target_pose.orientation.w = 1.0;
    
    move_group.setPoseTarget(target_pose);
    
    // 规划并执行
    moveit::planning_interface::MoveGroupInterface::Plan plan;
    bool success = (move_group.plan(plan) == moveit::core::MoveItErrorCode::SUCCESS);
    
    if (success) {
        move_group.execute(plan);
        RCLCPP_INFO(node->get_logger(), "Motion executed successfully!");
    }
    
    rclcpp::shutdown();
    return 0;
}
```

### 10.3 C++ xArm Planner API 模板

```cpp
#include <rclcpp/rclcpp.hpp>
#include "xarm_planner/xarm_planner.h"

int main(int argc, char** argv)
{
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("xarm_planner_example");
    
    // 创建 Planner
    auto planner = std::make_shared<xarm_planner::XArmPlanner>(node, "xarm7");
    
    // 设置目标关节角度
    std::vector<double> target_joint = {0.0, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0};
    
    // 执行规划
    if (planner->planJointTarget(target_joint)) {
        RCLCPP_INFO(node->get_logger(), "Planning succeeded!");
        planner->execute();
    }
    
    rclcpp::shutdown();
    return 0;
}
```

---

## 11. 常用开发场景

### 11.1 场景1: 简单的抓取和放置

```bash
# 1. 启动驱动
ros2 launch xarm_api xarm7_driver.launch.py robot_ip:=192.168.1.xxx add_gripper:=true

# 2. 在另一个终端运行您的抓取程序
ros2 run your_package grasp_and_place_node
```

### 11.2 场景2: 视觉引导抓取

```bash
# 启动相机 + 机械臂 + 视觉抓取
ros2 launch d435i_xarm_setup d435i_findobj2d_robot_moveit_planner.launch.py \
  robot_ip:=192.168.1.xxx \
  dof:=7 \
  add_gripper:=true
```

### 11.3 场景3: 仿真测试

```bash
# 1. 启动 Gazebo 仿真
ros2 launch xarm_gazebo xarm7_beside_table_gazebo.launch.py add_gripper:=true

# 2. 启动 MoveIt
ros2 launch xarm_moveit_config xarm7_moveit_gazebo.launch.py

# 3. 运行您的测试程序
ros2 run your_package test_node
```

### 11.4 场景4: 双臂协同

```bash
# 启动双臂 MoveIt
ros2 launch xarm_moveit_config dual_xarm7_moveit_realmove.launch.py \
  robot_ip_1:=192.168.1.xxx \
  robot_ip_2:=192.168.1.yyy

# 运行双臂协同程序
ros2 run xarm_planner test_dual_xarm_planner_api_joint
```

---

## 12. 编译和运行示例

### 12.1 编译所有包

```bash
cd ~/dev_ws
colcon build --symlink-install
source install/setup.bash
```

### 12.2 编译特定包

```bash
# 只编译 xarm_planner
colcon build --packages-select xarm_planner

# 编译 xarm_planner 及其依赖
colcon build --packages-up-to xarm_planner
```

### 12.3 运行测试程序

```bash
# 方法1: 直接运行可执行文件
ros2 run xarm_planner test_xarm_planner_api_joint

# 方法2: 使用 launch 文件
ros2 launch xarm_planner test_planner.launch.py

# 方法3: 运行 SDK 示例（需要先编译）
cd src/xarm_ros2/xarm_sdk/cxx/example
./build.sh
./1001-move_line 192.168.1.xxx
```

---

## 13. 参考文档

### 13.1 主要文档

- **主 README**: `src/xarm_ros2/ReadMe.md`
- **xArm API 文档**: `src/xarm_ros2/xarm_api/ReadMe.md`
- **xArm SDK 文档**: `src/xarm_ros2/xarm_sdk/cxx/ReadMe.md`
- **uf_ros_lib 文档**: `src/xarm_ros2/uf_ros_lib/Readme.md`
- **mbot_demo 文档**: `src/xarm_ros2/demo/mbot_demo/readme.md`

### 13.2 接口文档

- **ROS2 接口完整文档**: `/home/liuz/Work/dev_ws/XARM7_ROS2_INTERFACES.md`

### 13.3 在线资源

- [xArm ROS2 GitHub](https://github.com/xArm-Developer/xarm_ros2)
- [xArm 用户手册](https://www.ufactory.cc/docs/)
- [xArm Python SDK](https://github.com/xArm-Developer/xArm-Python-SDK)
- [MoveIt 2 文档](https://moveit.picknik.ai/main/index.html)

---

## 14. 示例程序索引

### 按功能分类

| 功能类别 | 示例数量 | 位置 |
|---------|---------|------|
| MoveIt 规划 | 8个测试 | `xarm_planner/test/` |
| SDK 底层控制 | 44个示例 | `xarm_sdk/cxx/example/` |
| 视觉抓取 | 3个程序 | `xarm_vision/d435i_xarm_setup/src/` |
| Gazebo 仿真 | 多个 launch | `xarm_gazebo/launch/` |
| MoveIt Demo | 4个 launch | `xarm_moveit_config/launch/demo/` |
| 移动底盘集成 | 3个 launch | `demo/mbot_demo/launch/` |

### 按难度分类

#### 入门级
- `xarm7_driver.launch.py` - 启动驱动
- `xarm7_rviz_display.launch.py` - 可视化
- `xarm7_moveit_fake.launch.py` - MoveIt 仿真
- `1001-move_line.cc` - 简单直线运动

#### 中级
- `test_xarm_planner_api_joint.cpp` - Planner API 使用
- `test_xarm_gripper_planner_api_joint.cpp` - 带夹爪规划
- `findobj_grasp_xarm_api.cpp` - 视觉抓取
- `7001-servo_j.cc` - 伺服运动

#### 高级
- `test_dual_xarm_planner_api_joint.cpp` - 双臂协同
- `findobj_grasp_moveit_planner.cpp` - MoveIt 视觉抓取
- `8002-admittance_control.cc` - 导纳控制
- `mbot_moveit_realmove.launch.py` - 移动底盘集成

---

## 15. 快速查找

### 我想要...

- **控制真实机械臂** → 第1节 快速启动示例
- **使用 MoveIt 规划** → 第2节 MoveIt 运动规划示例
- **编写 C++ 程序** → 第3节 xArm Planner API 示例
- **使用底层 SDK** → 第4节 xArm SDK C++ 示例
- **实现视觉抓取** → 第5节 视觉抓取示例
- **在仿真中测试** → 第6节 Gazebo 仿真示例
- **控制夹爪** → 第4.9节 夹爪控制示例
- **使用力控** → 第4.12节 力控功能示例
- **双臂协同** → 第3.1.7节 双臂协同规划
- **快速开始编程** → 第10节 快速开发模板

---

**文档版本**: 1.0  
**最后更新**: 2024-12-11  
**包含示例数**: 60+ 个示例程序和 launch 文件  
**适用机型**: xArm7, xArm6, xArm5, Lite6, UF850
