# xArm7 ROS2 接口完整文档

本文档详细列出了 xArm7 机械臂在 ROS2 环境下的所有接口，包括话题(Topics)、服务(Services)和动作(Actions)。

## 目录
- [1. 话题接口 (Topics)](#1-话题接口-topics)
- [2. 服务接口 (Services)](#2-服务接口-services)
- [3. 动作接口 (Actions)](#3-动作接口-actions)
- [4. 消息类型说明](#4-消息类型说明)

---

## 1. 话题接口 (Topics)

### 1.1 发布的话题 (Published Topics)

#### `/joint_states`
- **消息类型**: `sensor_msgs/msg/JointState`
- **功能**: 发布机械臂关节状态信息
- **内容**: 
  - `position`: 关节位置（弧度）
  - `velocity`: 关节速度（弧度/秒）
  - `effort`: 关节力矩/电流估计值
- **频率**: 默认 5Hz（可配置）

#### `/robot_states`
- **消息类型**: `xarm_msgs/msg/RobotMsg`
- **功能**: 发布机械臂完整状态信息
- **内容**:
  - `state`: 机器人状态（1=运行中, 2=待命, 3=暂停, 4=停止, 5=配置改变）
  - `mode`: 控制模式（0=位置模式, 1=伺服模式, 2=示教模式）
  - `cmdnum`: 命令缓冲区中等待的命令数
  - `mt_brake`: 制动器状态（二进制位表示各轴）
  - `mt_able`: 伺服使能状态（二进制位表示各轴）
  - `err`: 错误代码
  - `warn`: 警告代码
  - `angle`: 当前关节角度（弧度）
  - `pose`: TCP笛卡尔位置 [X(mm), Y(mm), Z(mm), Roll(rad), Pitch(rad), Yaw(rad)]
  - `offset`: TCP相对于法兰中心的偏移
- **频率**: 默认 5Hz（可配置）

#### `/xarm_cgpio_states`
- **消息类型**: `xarm_msgs/msg/CIOState`
- **功能**: 发布控制器GPIO状态
- **内容**:
  - `state`: GPIO模块状态
  - `code`: GPIO模块错误代码
  - `input_digitals`: 数字输入状态（CI0-CI7, DI0-DI7）
  - `output_digitals`: 数字输出状态（CO0-CO7, DO0-DO7）
  - `input_analogs`: 模拟输入值（AI0, AI1）
  - `output_analogs`: 模拟输出值（AO0, AO1）
- **频率**: 默认 5Hz（可配置）

#### `/uf_ftsensor_ext_states`
- **消息类型**: `geometry_msgs/msg/WrenchStamped`
- **功能**: 发布力矩传感器外部力数据
- **内容**: 力和力矩的六维向量

#### `/uf_ftsensor_raw_states`
- **消息类型**: `geometry_msgs/msg/WrenchStamped`
- **功能**: 发布力矩传感器原始数据
- **内容**: 未经处理的力和力矩数据

### 1.2 订阅的话题 (Subscribed Topics)

#### `/vc_set_joint_velocity`
- **消息类型**: `xarm_msgs/msg/MoveVelocity`
- **功能**: 接收关节空间速度控制命令
- **需要启用**: 在配置文件中设置 `services.vc_set_joint_velocity: true`

#### `/vc_set_cartesian_velocity`
- **消息类型**: `xarm_msgs/msg/MoveVelocity`
- **功能**: 接收笛卡尔空间速度控制命令
- **需要启用**: 在配置文件中设置 `services.vc_set_cartesian_velocity: true`

---

## 2. 服务接口 (Services)

### 2.1 基础控制服务

#### `/xarm/clean_error`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 清除错误状态
- **参数**: 无
- **返回**: `ret` (0表示成功)

#### `/xarm/clean_warn`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 清除警告状态
- **参数**: 无
- **返回**: `ret` (0表示成功)

#### `/xarm/clean_conf`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 清除配置
- **参数**: 无
- **返回**: `ret` (0表示成功)

#### `/xarm/save_conf`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 保存当前配置
- **参数**: 无
- **返回**: `ret` (0表示成功)

#### `/xarm/reload_dynamics`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 重新加载动力学参数
- **参数**: 无
- **返回**: `ret` (0表示成功)

### 2.2 状态查询服务

#### `/xarm/get_state`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取机器人状态
- **参数**: 无
- **返回**: `data` (状态值)

#### `/xarm/get_cmdnum`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取命令缓冲区中的命令数
- **参数**: 无
- **返回**: `data` (命令数量)

#### `/xarm/get_err_warn_code`
- **服务类型**: `xarm_msgs/srv/GetInt16List`
- **功能**: 获取错误和警告代码
- **参数**: 无
- **返回**: `datas` (错误和警告代码列表)

#### `/xarm/get_position`
- **服务类型**: `xarm_msgs/srv/GetFloat32List`
- **功能**: 获取当前TCP笛卡尔位置
- **参数**: 无
- **返回**: `datas` [X, Y, Z, Roll, Pitch, Yaw]

#### `/xarm/get_servo_angle`
- **服务类型**: `xarm_msgs/srv/GetFloat32List`
- **功能**: 获取当前关节角度
- **参数**: 无
- **返回**: `datas` (7个关节角度，弧度)

#### `/xarm/get_position_aa`
- **服务类型**: `xarm_msgs/srv/GetFloat32List`
- **功能**: 获取当前TCP位置（轴角表示）
- **参数**: 无
- **返回**: `datas` [X, Y, Z, Rx, Ry, Rz]

### 2.3 模式和状态设置服务

#### `/xarm/set_mode`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置控制模式
- **参数**: `data` (0=位置模式, 1=伺服模式, 2=示教模式)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_state`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置机器人状态
- **参数**: `data` (0=待命, 3=暂停, 4=停止)
- **返回**: `ret` (0表示成功)

#### `/xarm/motion_enable`
- **服务类型**: `xarm_msgs/srv/SetInt16ById`
- **功能**: 使能/失能指定关节的运动
- **参数**: `id` (关节ID), `data` (1=使能, 0=失能)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_servo_attach`
- **服务类型**: `xarm_msgs/srv/SetInt16ById`
- **功能**: 连接指定伺服电机
- **参数**: `id` (伺服ID), `data` (1=连接)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_servo_detach`
- **服务类型**: `xarm_msgs/srv/SetInt16ById`
- **功能**: 断开指定伺服电机
- **参数**: `id` (伺服ID), `data` (1=断开)
- **返回**: `ret` (0表示成功)

### 2.4 运动控制服务

#### `/xarm/set_position`
- **服务类型**: `xarm_msgs/srv/MoveCartesian`
- **功能**: 设置TCP目标位置（笛卡尔空间）
- **参数**: 
  - `pose`: [X(mm), Y(mm), Z(mm), Roll(rad), Pitch(rad), Yaw(rad)]
  - `mvvelo`: 速度 (mm/s)
  - `mvacc`: 加速度 (mm/s²)
  - `mvtime`: 运动时间 (s)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_tool_position`
- **服务类型**: `xarm_msgs/srv/MoveCartesian`
- **功能**: 设置工具坐标系下的目标位置
- **参数**: 同 `set_position`
- **返回**: `ret` (0表示成功)

#### `/xarm/set_position_aa`
- **服务类型**: `xarm_msgs/srv/MoveCartesian`
- **功能**: 设置TCP目标位置（轴角表示）
- **参数**: `pose`: [X, Y, Z, Rx, Ry, Rz]
- **返回**: `ret` (0表示成功)

#### `/xarm/set_servo_angle`
- **服务类型**: `xarm_msgs/srv/MoveJoint`
- **功能**: 设置关节目标角度
- **参数**: 
  - `angles`: 7个关节角度（弧度）
  - `mvvelo`: 速度 (rad/s)
  - `mvacc`: 加速度 (rad/s²)
  - `mvtime`: 运动时间 (s)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_servo_angle_j`
- **服务类型**: `xarm_msgs/srv/MoveJoint`
- **功能**: 关节空间伺服运动（模式1）
- **参数**: `angles`: 7个关节角度（弧度）
- **返回**: `ret` (0表示成功)
- **注意**: 用于高频率小步长运动，需在模式1下使用

#### `/xarm/set_servo_cartesian`
- **服务类型**: `xarm_msgs/srv/MoveCartesian`
- **功能**: 笛卡尔空间伺服运动（模式1）
- **参数**: 
  - `pose`: [X, Y, Z, Roll, Pitch, Yaw]
  - `is_tool_coord`: 是否使用工具坐标系
- **返回**: `ret` (0表示成功)
- **注意**: 用于高频率小步长运动，需在模式1下使用

#### `/xarm/set_servo_cartesian_aa`
- **服务类型**: `xarm_msgs/srv/MoveCartesian`
- **功能**: 笛卡尔空间伺服运动（轴角表示，模式1）
- **参数**: `pose`: [X, Y, Z, Rx, Ry, Rz]
- **返回**: `ret` (0表示成功)

#### `/xarm/move_circle`
- **服务类型**: `xarm_msgs/srv/MoveCircle`
- **功能**: 圆弧运动
- **参数**: 
  - `pose1`: 圆弧中间点
  - `pose2`: 圆弧终点
  - `mvvelo`: 速度
  - `mvacc`: 加速度
  - `percent`: 圆弧百分比
- **返回**: `ret` (0表示成功)

#### `/xarm/move_gohome`
- **服务类型**: `xarm_msgs/srv/MoveHome`
- **功能**: 回到零位
- **参数**: 
  - `mvvelo`: 速度
  - `mvacc`: 加速度
  - `mvtime`: 运动时间
- **返回**: `ret` (0表示成功)

### 2.5 速度控制服务

#### `/xarm/vc_set_joint_velocity`
- **服务类型**: `xarm_msgs/srv/MoveVelocity`
- **功能**: 设置关节速度（服务方式）
- **参数**: `velocities`: 7个关节速度
- **返回**: `ret` (0表示成功)

#### `/xarm/vc_set_cartesian_velocity`
- **服务类型**: `xarm_msgs/srv/MoveVelocity`
- **功能**: 设置笛卡尔速度（服务方式）
- **参数**: `velocities`: [vx, vy, vz, ωx, ωy, ωz]
- **返回**: `ret` (0表示成功)

### 2.6 运动参数设置服务

#### `/xarm/set_tcp_jerk`
- **服务类型**: `xarm_msgs/srv/SetFloat32`
- **功能**: 设置TCP加加速度
- **参数**: `data` (mm/s³)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_tcp_maxacc`
- **服务类型**: `xarm_msgs/srv/SetFloat32`
- **功能**: 设置TCP最大加速度
- **参数**: `data` (mm/s²)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_joint_jerk`
- **服务类型**: `xarm_msgs/srv/SetFloat32`
- **功能**: 设置关节加加速度
- **参数**: `data` (rad/s³)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_joint_maxacc`
- **服务类型**: `xarm_msgs/srv/SetFloat32`
- **功能**: 设置关节最大加速度
- **参数**: `data` (rad/s²)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_pause_time`
- **服务类型**: `xarm_msgs/srv/SetFloat32`
- **功能**: 设置暂停时间
- **参数**: `data` (秒)
- **返回**: `ret` (0表示成功)

### 2.7 TCP和负载配置服务

#### `/xarm/set_tcp_offset`
- **服务类型**: `xarm_msgs/srv/SetFloat32List`
- **功能**: 设置TCP偏移
- **参数**: `datas`: [X, Y, Z, Roll, Pitch, Yaw]
- **返回**: `ret` (0表示成功)

#### `/xarm/set_tcp_load`
- **服务类型**: `xarm_msgs/srv/SetTcpLoad`
- **功能**: 设置TCP负载
- **参数**: 
  - `mass`: 质量 (kg)
  - `center_of_gravity`: 重心位置 [X, Y, Z]
- **返回**: `ret` (0表示成功)

#### `/xarm/set_gravity_direction`
- **服务类型**: `xarm_msgs/srv/SetFloat32List`
- **功能**: 设置重力方向
- **参数**: `datas`: [X, Y, Z] (单位向量)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_world_offset`
- **服务类型**: `xarm_msgs/srv/SetFloat32List`
- **功能**: 设置世界坐标系偏移
- **参数**: `datas`: [X, Y, Z, Roll, Pitch, Yaw]
- **返回**: `ret` (0表示成功)

#### `/xarm/iden_tcp_load`
- **服务类型**: `xarm_msgs/srv/IdenLoad`
- **功能**: 识别TCP负载
- **参数**: 识别参数
- **返回**: `ret`, 识别结果

### 2.8 安全和限制设置服务

#### `/xarm/set_collision_sensitivity`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置碰撞灵敏度
- **参数**: `data` (0-5, 0最不敏感)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_teach_sensitivity`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置示教灵敏度
- **参数**: `data` (1-5)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_collision_rebound`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置碰撞后回弹
- **参数**: `data` (1=启用, 0=禁用)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_fence_mode`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置围栏模式
- **参数**: `data` (1=启用, 0=禁用)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_reduced_mode`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置缩减模式
- **参数**: `data` (1=启用, 0=禁用)
- **返回**: `ret` (0表示成功)

#### `/xarm/get_reduced_mode`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取缩减模式状态
- **参数**: 无
- **返回**: `data` (1=启用, 0=禁用)

#### `/xarm/set_reduced_tcp_boundary`
- **服务类型**: `xarm_msgs/srv/SetInt16List`
- **功能**: 设置TCP边界限制
- **参数**: `datas`: 边界参数
- **返回**: `ret` (0表示成功)

#### `/xarm/set_reduced_joint_range`
- **服务类型**: `xarm_msgs/srv/SetFloat32List`
- **功能**: 设置关节范围限制
- **参数**: `datas`: 关节范围
- **返回**: `ret` (0表示成功)

#### `/xarm/set_reduced_max_tcp_speed`
- **服务类型**: `xarm_msgs/srv/SetFloat32`
- **功能**: 设置最大TCP速度限制
- **参数**: `data` (mm/s)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_reduced_max_joint_speed`
- **服务类型**: `xarm_msgs/srv/SetFloat32`
- **功能**: 设置最大关节速度限制
- **参数**: `data` (rad/s)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_self_collision_detection`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置自碰撞检测
- **参数**: `data` (1=启用, 0=禁用)
- **返回**: `ret` (0表示成功)

### 2.9 工具端IO服务

#### `/xarm/get_tgpio_digital`
- **服务类型**: `xarm_msgs/srv/GetDigitalIO`
- **功能**: 获取工具端数字输入状态
- **参数**: 无
- **返回**: `digitals`: 2个数字输入状态

#### `/xarm/set_tgpio_digital`
- **服务类型**: `xarm_msgs/srv/SetDigitalIO`
- **功能**: 设置工具端数字输出
- **参数**: 
  - `ionum`: IO编号 (0或1)
  - `value`: 值 (0或1)
- **返回**: `ret` (0表示成功)

#### `/xarm/get_tgpio_analog`
- **服务类型**: `xarm_msgs/srv/GetAnalogIO`
- **功能**: 获取工具端模拟输入
- **参数**: `ionum`: IO编号 (0或1)
- **返回**: `value`: 模拟值

#### `/xarm/set_tgpio_digital_with_xyz`
- **服务类型**: `xarm_msgs/srv/SetDigitalIO`
- **功能**: 在指定位置设置工具端数字输出
- **参数**: IO编号、值和位置
- **返回**: `ret` (0表示成功)

### 2.10 控制器IO服务

#### `/xarm/get_cgpio_digital`
- **服务类型**: `xarm_msgs/srv/GetDigitalIO`
- **功能**: 获取控制器数字输入状态
- **参数**: 无
- **返回**: `digitals`: 数字输入状态（CI0-CI7, DI0-DI7）

#### `/xarm/set_cgpio_digital`
- **服务类型**: `xarm_msgs/srv/SetDigitalIO`
- **功能**: 设置控制器数字输出
- **参数**: 
  - `ionum`: IO编号 (0-15)
  - `value`: 值 (0或1)
- **返回**: `ret` (0表示成功)

#### `/xarm/get_cgpio_analog`
- **服务类型**: `xarm_msgs/srv/GetAnalogIO`
- **功能**: 获取控制器模拟输入
- **参数**: `ionum`: IO编号 (0或1)
- **返回**: `value`: 模拟值

#### `/xarm/set_cgpio_analog`
- **服务类型**: `xarm_msgs/srv/SetAnalogIO`
- **功能**: 设置控制器模拟输出
- **参数**: 
  - `ionum`: IO编号 (0或1)
  - `value`: 目标值 (0-10V)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_cgpio_digital_with_xyz`
- **服务类型**: `xarm_msgs/srv/SetDigitalIO`
- **功能**: 在指定位置设置控制器数字输出
- **参数**: IO编号、值和位置
- **返回**: `ret` (0表示成功)

#### `/xarm/set_cgpio_analog_with_xyz`
- **服务类型**: `xarm_msgs/srv/SetAnalogIO`
- **功能**: 在指定位置设置控制器模拟输出
- **参数**: IO编号、值和位置
- **返回**: `ret` (0表示成功)

#### `/xarm/config_tgpio_reset_when_stop`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 配置停止时工具端GPIO复位
- **参数**: `data` (1=启用, 0=禁用)
- **返回**: `ret` (0表示成功)

#### `/xarm/config_cgpio_reset_when_stop`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 配置停止时控制器GPIO复位
- **参数**: `data` (1=启用, 0=禁用)
- **返回**: `ret` (0表示成功)

### 2.11 夹爪控制服务

#### 2.11.1 xArm夹爪

##### `/xarm/set_gripper_enable`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 使能/失能夹爪
- **参数**: `data` (1=使能, 0=失能)
- **返回**: `ret` (0表示成功)

##### `/xarm/set_gripper_mode`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置夹爪模式
- **参数**: `data` (0=位置模式)
- **返回**: `ret` (0表示成功)

##### `/xarm/set_gripper_speed`
- **服务类型**: `xarm_msgs/srv/SetFloat32`
- **功能**: 设置夹爪速度
- **参数**: `data` (1-5000)
- **返回**: `ret` (0表示成功)

##### `/xarm/set_gripper_position`
- **服务类型**: `xarm_msgs/srv/GripperMove`
- **功能**: 设置夹爪位置
- **参数**: `pos` (0-850, 0=闭合, 850=完全打开)
- **返回**: `ret` (0表示成功)

##### `/xarm/get_gripper_position`
- **服务类型**: `xarm_msgs/srv/GetFloat32`
- **功能**: 获取夹爪当前位置
- **参数**: 无
- **返回**: `data`: 当前位置

##### `/xarm/get_gripper_err_code`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取夹爪错误代码
- **参数**: 无
- **返回**: `data`: 错误代码

##### `/xarm/clean_gripper_error`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 清除夹爪错误
- **参数**: 无
- **返回**: `ret` (0表示成功)

#### 2.11.2 真空夹爪

##### `/xarm/set_vacuum_gripper`
- **服务类型**: `xarm_msgs/srv/VacuumGripperCtrl`
- **功能**: 控制真空夹爪
- **参数**: 
  - `on`: 开关 (true=开, false=关)
  - `wait`: 是否等待完成
  - `timeout`: 超时时间
- **返回**: `ret` (0表示成功)

##### `/xarm/get_vacuum_gripper`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取真空夹爪状态
- **参数**: 无
- **返回**: `data`: 状态值

#### 2.11.3 BIO夹爪

##### `/xarm/set_bio_gripper_enable`
- **服务类型**: `xarm_msgs/srv/BioGripperEnable`
- **功能**: 使能BIO夹爪
- **参数**: `enable`: true/false
- **返回**: `ret` (0表示成功)

##### `/xarm/set_bio_gripper_speed`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置BIO夹爪速度
- **参数**: `data`: 速度值
- **返回**: `ret` (0表示成功)

##### `/xarm/open_bio_gripper`
- **服务类型**: `xarm_msgs/srv/BioGripperCtrl`
- **功能**: 打开BIO夹爪
- **参数**: 控制参数
- **返回**: `ret` (0表示成功)

##### `/xarm/close_bio_gripper`
- **服务类型**: `xarm_msgs/srv/BioGripperCtrl`
- **功能**: 关闭BIO夹爪
- **参数**: 控制参数
- **返回**: `ret` (0表示成功)

##### `/xarm/get_bio_gripper_status`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取BIO夹爪状态
- **参数**: 无
- **返回**: `data`: 状态值

##### `/xarm/get_bio_gripper_error`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取BIO夹爪错误
- **参数**: 无
- **返回**: `data`: 错误代码

##### `/xarm/clean_bio_gripper_error`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 清除BIO夹爪错误
- **参数**: 无
- **返回**: `ret` (0表示成功)

#### 2.11.4 Lite6夹爪

##### `/xarm/open_lite6_gripper`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 打开Lite6夹爪
- **参数**: 无
- **返回**: `ret` (0表示成功)

##### `/xarm/close_lite6_gripper`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 关闭Lite6夹爪
- **参数**: 无
- **返回**: `ret` (0表示成功)

##### `/xarm/stop_lite6_gripper`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 停止Lite6夹爪
- **参数**: 无
- **返回**: `ret` (0表示成功)

#### 2.11.5 Robotiq夹爪

##### `/xarm/robotiq_reset`
- **服务类型**: `xarm_msgs/srv/RobotiqReset`
- **功能**: 复位Robotiq夹爪
- **参数**: 复位参数
- **返回**: `ret` (0表示成功)

##### `/xarm/robotiq_set_activate`
- **服务类型**: `xarm_msgs/srv/RobotiqActivate`
- **功能**: 激活Robotiq夹爪
- **参数**: 激活参数
- **返回**: `ret` (0表示成功)

##### `/xarm/robotiq_set_position`
- **服务类型**: `xarm_msgs/srv/RobotiqMove`
- **功能**: 设置Robotiq夹爪位置
- **参数**: 位置和速度参数
- **返回**: `ret` (0表示成功)

##### `/xarm/robotiq_open`
- **服务类型**: `xarm_msgs/srv/RobotiqMove`
- **功能**: 打开Robotiq夹爪
- **参数**: 速度参数
- **返回**: `ret` (0表示成功)

##### `/xarm/robotiq_close`
- **服务类型**: `xarm_msgs/srv/RobotiqMove`
- **功能**: 关闭Robotiq夹爪
- **参数**: 速度参数
- **返回**: `ret` (0表示成功)

##### `/xarm/robotiq_get_status`
- **服务类型**: `xarm_msgs/srv/RobotiqGetStatus`
- **功能**: 获取Robotiq夹爪状态
- **参数**: 无
- **返回**: 完整状态信息

### 2.12 力控传感器服务

#### `/xarm/set_ft_sensor_enable`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 使能力控传感器
- **参数**: `data` (1=使能, 0=失能)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_ft_sensor_mode`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置力控传感器模式
- **参数**: `data` (模式值)
- **返回**: `ret` (0表示成功)

#### `/xarm/get_ft_sensor_mode`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取力控传感器模式
- **参数**: 无
- **返回**: `data`: 当前模式

#### `/xarm/get_ft_sensor_error`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取力控传感器错误
- **参数**: 无
- **返回**: `data`: 错误代码

#### `/xarm/get_ft_sensor_data`
- **服务类型**: `xarm_msgs/srv/GetFloat32List`
- **功能**: 获取力控传感器数据
- **参数**: 无
- **返回**: `datas`: [Fx, Fy, Fz, Mx, My, Mz]

#### `/xarm/set_ft_sensor_zero`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 设置力控传感器零点
- **参数**: 无
- **返回**: `ret` (0表示成功)

#### `/xarm/iden_ft_sensor_load_offset`
- **服务类型**: `xarm_msgs/srv/IdenLoad`
- **功能**: 识别力控传感器负载偏移
- **参数**: 识别参数
- **返回**: `ret`, 识别结果

#### `/xarm/set_ft_sensor_load_offset`
- **服务类型**: `xarm_msgs/srv/FtCaliLoad`
- **功能**: 设置力控传感器负载偏移
- **参数**: 负载参数
- **返回**: `ret` (0表示成功)

#### `/xarm/set_ft_sensor_force_parameters`
- **服务类型**: `xarm_msgs/srv/FtForceParams`
- **功能**: 设置力控参数
- **参数**: 力控参数
- **返回**: `ret` (0表示成功)

#### `/xarm/set_ft_sensor_admittance_parameters`
- **服务类型**: `xarm_msgs/srv/FtAdmittanceParams`
- **功能**: 设置导纳控制参数
- **参数**: 导纳参数
- **返回**: `ret` (0表示成功)

### 2.13 轨迹记录和回放服务

#### `/xarm/start_record_trajectory`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 开始记录轨迹
- **参数**: 无
- **返回**: `ret` (0表示成功)

#### `/xarm/stop_record_trajectory`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 停止记录轨迹
- **参数**: 无
- **返回**: `ret` (0表示成功)

#### `/xarm/save_record_trajectory`
- **服务类型**: `xarm_msgs/srv/TrajCtrl`
- **功能**: 保存记录的轨迹
- **参数**: 
  - `filename`: 文件名
- **返回**: `ret` (0表示成功)

#### `/xarm/load_trajectory`
- **服务类型**: `xarm_msgs/srv/TrajCtrl`
- **功能**: 加载轨迹文件
- **参数**: 
  - `filename`: 文件名
- **返回**: `ret` (0表示成功)

#### `/xarm/playback_trajectory`
- **服务类型**: `xarm_msgs/srv/TrajPlay`
- **功能**: 回放轨迹
- **参数**: 
  - `times`: 回放次数
  - `wait`: 是否等待完成
- **返回**: `ret` (0表示成功)

#### `/xarm/get_trajectory_rw_status`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取轨迹读写状态
- **参数**: 无
- **返回**: `data`: 状态值

### 2.14 直线电机/滑轨服务

#### `/xarm/set_linear_motor_enable`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 使能直线电机
- **参数**: `data` (1=使能, 0=失能)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_linear_motor_speed`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置直线电机速度
- **参数**: `data`: 速度值
- **返回**: `ret` (0表示成功)

#### `/xarm/set_linear_motor_pos`
- **服务类型**: `xarm_msgs/srv/LinearMotorSetPos`
- **功能**: 设置直线电机位置
- **参数**: 位置参数
- **返回**: `ret` (0表示成功)

#### `/xarm/set_linear_motor_stop`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 停止直线电机
- **参数**: 无
- **返回**: `ret` (0表示成功)

#### `/xarm/set_linear_motor_back_origin`
- **服务类型**: `xarm_msgs/srv/LinearMotorBackOrigin`
- **功能**: 直线电机回零
- **参数**: 回零参数
- **返回**: `ret` (0表示成功)

#### `/xarm/get_linear_motor_pos`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取直线电机位置
- **参数**: 无
- **返回**: `data`: 位置值

#### `/xarm/get_linear_motor_status`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取直线电机状态
- **参数**: 无
- **返回**: `data`: 状态值

#### `/xarm/get_linear_motor_error`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取直线电机错误
- **参数**: 无
- **返回**: `data`: 错误代码

#### `/xarm/get_linear_motor_is_enabled`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取直线电机使能状态
- **参数**: 无
- **返回**: `data`: 使能状态

#### `/xarm/get_linear_motor_on_zero`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取直线电机是否在零点
- **参数**: 无
- **返回**: `data`: 零点状态

#### `/xarm/get_linear_motor_sci`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取直线电机SCI状态
- **参数**: 无
- **返回**: `data`: SCI值

#### `/xarm/get_linear_motor_sco`
- **服务类型**: `xarm_msgs/srv/GetInt16List`
- **功能**: 获取直线电机SCO状态
- **参数**: 无
- **返回**: `datas`: SCO值列表

#### `/xarm/clean_linear_motor_error`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 清除直线电机错误
- **参数**: 无
- **返回**: `ret` (0表示成功)

### 2.15 Modbus通信服务

#### `/xarm/get_tgpio_modbus_baudrate`
- **服务类型**: `xarm_msgs/srv/GetInt32`
- **功能**: 获取工具端Modbus波特率
- **参数**: 无
- **返回**: `data`: 波特率

#### `/xarm/set_tgpio_modbus_baudrate`
- **服务类型**: `xarm_msgs/srv/SetInt32`
- **功能**: 设置工具端Modbus波特率
- **参数**: `data`: 波特率
- **返回**: `ret` (0表示成功)

#### `/xarm/set_tgpio_modbus_timeout`
- **服务类型**: `xarm_msgs/srv/SetModbusTimeout`
- **功能**: 设置工具端Modbus超时
- **参数**: 超时参数
- **返回**: `ret` (0表示成功)

#### `/xarm/getset_tgpio_modbus_data`
- **服务类型**: `xarm_msgs/srv/GetSetModbusData`
- **功能**: 读写工具端Modbus数据
- **参数**: Modbus命令参数
- **返回**: `ret`, 读取的数据

### 2.16 高级配置服务

#### `/xarm/set_simulation_robot`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置仿真模式
- **参数**: `data` (1=仿真, 0=实际)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_baud_checkset_enable`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 使能波特率检查设置
- **参数**: `data` (1=使能, 0=禁用)
- **返回**: `ret` (0表示成功)

#### `/xarm/get_checkset_default_baud`
- **服务类型**: `xarm_msgs/srv/GetInt32ByType`
- **功能**: 获取默认波特率检查设置
- **参数**: `type`: 类型
- **返回**: `data`: 波特率

#### `/xarm/set_checkset_default_baud`
- **服务类型**: `xarm_msgs/srv/SetInt32ByType`
- **功能**: 设置默认波特率检查设置
- **参数**: `type`: 类型, `data`: 波特率
- **返回**: `ret` (0表示成功)

#### `/xarm/set_report_tau_or_i`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置报告力矩或电流
- **参数**: `data` (0=力矩, 1=电流)
- **返回**: `ret` (0表示成功)

#### `/xarm/get_report_tau_or_i`
- **服务类型**: `xarm_msgs/srv/GetInt16`
- **功能**: 获取报告类型
- **参数**: 无
- **返回**: `data` (0=力矩, 1=电流)

#### `/xarm/set_cartesian_velo_continuous`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置笛卡尔速度连续模式
- **参数**: `data` (1=启用, 0=禁用)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_allow_approx_motion`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 允许近似运动
- **参数**: `data` (1=允许, 0=不允许)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_only_check_type`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置仅检查类型
- **参数**: `data`: 检查类型
- **返回**: `ret` (0表示成功)

#### `/xarm/set_counter_reset`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 复位计数器
- **参数**: 无
- **返回**: `ret` (0表示成功)

#### `/xarm/set_counter_increase`
- **服务类型**: `xarm_msgs/srv/Call`
- **功能**: 增加计数器
- **参数**: 无
- **返回**: `ret` (0表示成功)

#### `/xarm/set_rs485_use_503_port`
- **服务类型**: `xarm_msgs/srv/SetInt16`
- **功能**: 设置RS485使用503端口
- **参数**: `data` (1=使用, 0=不使用)
- **返回**: `ret` (0表示成功)

#### `/xarm/set_external_device_monitor_params`
- **服务类型**: `xarm_msgs/srv/SetInt16List`
- **功能**: 设置外部设备监控参数
- **参数**: `datas`: 监控参数列表
- **返回**: `ret` (0表示成功)

---

## 3. 动作接口 (Actions)

### 3.1 xArm夹爪动作

#### `xarm_gripper/gripper_action`
- **动作类型**: `control_msgs/action/GripperCommand`
- **功能**: 控制xArm夹爪运动
- **目标参数**:
  - `command.position`: 目标位置（0-0.86弧度，0=完全打开，0.86=完全闭合）
  - `command.max_effort`: 最大力（当前未使用）
- **反馈**: 
  - `position`: 当前位置
  - `effort`: 当前力
  - `stalled`: 是否停滞
  - `reached_goal`: 是否到达目标
- **结果**:
  - `position`: 最终位置
  - `effort`: 最终力
  - `stalled`: 是否停滞
  - `reached_goal`: 是否成功到达目标

### 3.2 BIO夹爪动作

#### `bio_gripper/gripper_action`
- **动作类型**: `control_msgs/action/GripperCommand`
- **功能**: 控制BIO夹爪运动
- **参数**: 同xArm夹爪动作

---

## 4. 消息类型说明

### 4.1 自定义消息类型

#### `xarm_msgs/msg/RobotMsg`
机器人完整状态消息，包含：
- `state`: 机器人状态
- `mode`: 控制模式
- `cmdnum`: 命令缓冲数量
- `mt_brake`: 制动器状态
- `mt_able`: 伺服使能状态
- `err`: 错误代码
- `warn`: 警告代码
- `angle`: 关节角度数组
- `pose`: TCP位姿 [X, Y, Z, Roll, Pitch, Yaw]
- `offset`: TCP偏移

#### `xarm_msgs/msg/CIOState`
控制器IO状态消息，包含：
- `state`: GPIO模块状态
- `code`: 错误代码
- `input_digitals`: 数字输入状态数组
- `output_digitals`: 数字输出状态数组
- `input_analogs`: 模拟输入值数组
- `output_analogs`: 模拟输出值数组
- `input_conf`: 输入配置
- `output_conf`: 输出配置

#### `xarm_msgs/msg/MoveVelocity`
速度控制消息，用于速度控制话题订阅

### 4.2 标准ROS2消息类型

- `sensor_msgs/msg/JointState`: 关节状态
- `geometry_msgs/msg/WrenchStamped`: 力和力矩数据
- `control_msgs/action/GripperCommand`: 夹爪控制动作

---

## 5. 使用示例

### 5.1 启动xArm7驱动
```bash
ros2 launch xarm_api xarm7_driver.launch.py robot_ip:=192.168.1.xxx
```

### 5.2 查看机器人状态
```bash
# 订阅关节状态
ros2 topic echo /joint_states

# 订阅机器人状态
ros2 topic echo /robot_states
```

### 5.3 基础运动控制
```bash
# 设置模式为0（位置模式）
ros2 service call /xarm/set_mode xarm_msgs/srv/SetInt16 "{data: 0}"

# 设置状态为0（待命）
ros2 service call /xarm/set_state xarm_msgs/srv/SetInt16 "{data: 0}"

# 移动到指定关节角度
ros2 service call /xarm/set_servo_angle xarm_msgs/srv/MoveJoint "{angles: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}"

# 移动到指定笛卡尔位置
ros2 service call /xarm/set_position xarm_msgs/srv/MoveCartesian "{pose: [300, 0, 300, 3.14, 0, 0]}"
```

### 5.4 伺服运动（高频小步长）
```bash
# 设置模式为1（伺服模式）
ros2 service call /xarm/set_mode xarm_msgs/srv/SetInt16 "{data: 1}"

# 设置状态为0（待命）
ros2 service call /xarm/set_state xarm_msgs/srv/SetInt16 "{data: 0}"

# 笛卡尔伺服运动（需要循环调用，每次小步长）
ros2 service call /xarm/set_servo_cartesian xarm_msgs/srv/MoveCartesian "{pose: [302, 0, 300, 3.14, 0, 0]}"
```

### 5.5 夹爪控制
```bash
# 使能夹爪
ros2 service call /xarm/set_gripper_enable xarm_msgs/srv/SetInt16 "{data: 1}"

# 设置夹爪模式
ros2 service call /xarm/set_gripper_mode xarm_msgs/srv/SetInt16 "{data: 0}"

# 设置夹爪速度
ros2 service call /xarm/set_gripper_speed xarm_msgs/srv/SetFloat32 "{data: 1500}"

# 设置夹爪位置（服务方式）
ros2 service call /xarm/set_gripper_position xarm_msgs/srv/GripperMove "{pos: 500}"

# 使用动作控制夹爪
ros2 action send_goal /xarm_gripper/gripper_action control_msgs/action/GripperCommand "{command: {position: 0.5, max_effort: 0}}"
```

### 5.6 IO控制
```bash
# 读取工具端数字输入
ros2 service call /xarm/get_tgpio_digital xarm_msgs/srv/GetDigitalIO

# 设置控制器数字输出
ros2 service call /xarm/set_cgpio_digital xarm_msgs/srv/SetDigitalIO "{ionum: 0, value: 1}"

# 读取控制器模拟输入
ros2 service call /xarm/get_cgpio_analog xarm_msgs/srv/GetAnalogIO "{ionum: 0}"

# 设置控制器模拟输出
ros2 service call /xarm/set_cgpio_analog xarm_msgs/srv/SetAnalogIO "{ionum: 0, value: 5.0}"
```

### 5.7 错误处理
```bash
# 查看错误代码
ros2 topic echo /robot_states --field err

# 清除错误
ros2 service call /xarm/clean_error xarm_msgs/srv/Call

# 重新设置状态为待命
ros2 service call /xarm/set_state xarm_msgs/srv/SetInt16 "{data: 0}"
```

---

## 6. 注意事项

1. **服务启用配置**: 大部分服务默认是禁用的，需要在配置文件 `xarm_params.yaml` 或 `xarm_user_params.yaml` 中启用相应服务，或者设置 `services.debug: true` 启用所有服务。

2. **模式切换**: 
   - 模式0（位置模式）：用于标准运动命令
   - 模式1（伺服模式）：用于高频率小步长运动（servo_cartesian, servo_angle_j）
   - 模式2（示教模式）：重力补偿，便于手动示教

3. **状态管理**: 
   - 状态0（待命）：准备接收运动命令
   - 状态3（暂停）：运动暂停
   - 状态4（停止）：不接受运动命令
   - 发生错误后需要清除错误并重新设置状态

4. **伺服运动**: 使用 `set_servo_cartesian` 或 `set_servo_angle_j` 时：
   - 必须在模式1下使用
   - 需要高频率调用（100-250Hz）
   - 每次步长必须小于10mm或对应的关节角度
   - 路径必须从当前位置开始

5. **坐标系**: 
   - 位置单位：毫米(mm)
   - 角度单位：弧度(rad)
   - 笛卡尔姿态：[X, Y, Z, Roll, Pitch, Yaw]

6. **返回值**: 所有服务调用返回 `ret` 字段，0表示成功，非0表示失败（参考用户手册查看具体错误码）。

7. **夹爪位置**: 
   - 服务调用：0-850（0=闭合，850=完全打开）
   - 动作调用：0-0.86弧度（0=完全打开，0.86=完全闭合）

8. **话题频率**: 默认发布频率为5Hz，可通过 `joint_states.rate` 参数配置。

---

## 7. 参考资源

- [xArm ROS2 GitHub仓库](https://github.com/xArm-Developer/xarm_ros2)
- [xArm用户手册](https://www.ufactory.cc/docs/)
- [xArm SDK文档](https://github.com/xArm-Developer/xArm-Python-SDK)
- ROS2官方文档: https://docs.ros.org/

---

**文档版本**: 1.0  
**最后更新**: 2024  
**适用于**: xArm7, xArm6, xArm5, Lite6, UF850 (接口通用)
