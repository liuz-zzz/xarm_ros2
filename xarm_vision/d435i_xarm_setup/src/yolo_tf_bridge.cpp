/* Copyright 2025 UFACTORY Inc. All Rights Reserved.
 *
 * Software License Agreement (BSD License)
 *
 * Modified to work with YOLO detections instead of find_object_2d
 *
 * Author: Jason Peng <jason@ufactory.cc>
 * Author: Vinman <vinman@ufactory.cc>
 * Modified by: AI Assistant
 ============================================================================*/
#include "sensor_msgs/msg/camera_info.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "vision_msgs/msg/detection2_d_array.hpp"
#include <cv_bridge/cv_bridge.h>
#include <opencv2/opencv.hpp>
#include <rclcpp/rclcpp.hpp>

rclcpp::Logger logger = rclcpp::get_logger("yolo_tf_bridge");
std::shared_ptr<rclcpp::Node> node;
std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster;

// 数据缓存
cv::Mat depth_image;
cv::Mat camera_matrix;
bool camera_info_received = false;

// 参数
double min_confidence = 0.5;
std::string object_frame_id = "object_1";
std::string camera_frame_id = "camera_color_optical_frame";

void camera_info_callback(const sensor_msgs::msg::CameraInfo::SharedPtr msg) {
  if (!camera_info_received) {
    // 提取相机内参矩阵
    camera_matrix = cv::Mat::eye(3, 3, CV_64F);
    camera_matrix.at<double>(0, 0) = msg->k[0]; // fx
    camera_matrix.at<double>(1, 1) = msg->k[4]; // fy
    camera_matrix.at<double>(0, 2) = msg->k[2]; // cx
    camera_matrix.at<double>(1, 2) = msg->k[5]; // cy

    camera_info_received = true;
    RCLCPP_INFO(logger, "相机内参已接收: fx=%.2f, fy=%.2f, cx=%.2f, cy=%.2f",
                msg->k[0], msg->k[4], msg->k[2], msg->k[5]);
  }
}

void depth_callback(const sensor_msgs::msg::Image::SharedPtr msg) {
  try {
    cv_bridge::CvImagePtr cv_ptr =
        cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::TYPE_16UC1);
    depth_image = cv_ptr->image.clone();
  } catch (cv_bridge::Exception &e) {
    RCLCPP_ERROR(logger, "深度图转换错误: %s", e.what());
  }
}

void detection_callback(
    const vision_msgs::msg::Detection2DArray::SharedPtr msg) {
  // 检查必要数据是否就绪
  if (!camera_info_received) {
    RCLCPP_WARN_THROTTLE(logger, *node->get_clock(), 2000, "等待相机内参...");
    return;
  }

  if (depth_image.empty()) {
    RCLCPP_WARN_THROTTLE(logger, *node->get_clock(), 2000, "等待深度图像...");
    return;
  }

  if (msg->detections.empty()) {
    return;
  }

  // 选择置信度最高的检测
  const vision_msgs::msg::Detection2D *best_detection = nullptr;
  double best_confidence = 0.0;

  for (const auto &detection : msg->detections) {
    if (!detection.results.empty()) {
      double confidence = detection.results[0].hypothesis.score;
      if (confidence > best_confidence && confidence >= min_confidence) {
        best_confidence = confidence;
        best_detection = &detection;
      }
    }
  }

  if (best_detection == nullptr) {
    return;
  }

  // 获取边界框中心点 (像素坐标)
  int u = static_cast<int>(best_detection->bbox.center.position.x);
  int v = static_cast<int>(best_detection->bbox.center.position.y);

  // 边界检查
  if (u < 0 || u >= depth_image.cols || v < 0 || v >= depth_image.rows) {
    RCLCPP_WARN(logger, "检测中心超出图像范围");
    return;
  }

  // 获取深度值 (使用小区域的中值提高鲁棒性)
  int region_size = 5;
  int y_start = std::max(0, v - region_size);
  int y_end = std::min(depth_image.rows, v + region_size);
  int x_start = std::max(0, u - region_size);
  int x_end = std::min(depth_image.cols, u + region_size);

  cv::Mat depth_region =
      depth_image(cv::Range(y_start, y_end), cv::Range(x_start, x_end));

  // 收集非零深度值
  std::vector<uint16_t> valid_depths;
  for (int i = 0; i < depth_region.rows; i++) {
    for (int j = 0; j < depth_region.cols; j++) {
      uint16_t d = depth_region.at<uint16_t>(i, j);
      if (d > 0) {
        valid_depths.push_back(d);
      }
    }
  }

  if (valid_depths.empty()) {
    RCLCPP_WARN(logger, "检测中心无有效深度值");
    return;
  }

  // 使用中值
  std::sort(valid_depths.begin(), valid_depths.end());
  uint16_t median_depth = valid_depths[valid_depths.size() / 2];
  double depth = median_depth * 0.001; // mm -> m

  // 深度合理性检查
  if (depth < 0.1 || depth > 2.0) {
    RCLCPP_WARN(logger, "深度值异常: %.3f m", depth);
    return;
  }

  // 提取相机内参
  double fx = camera_matrix.at<double>(0, 0);
  double fy = camera_matrix.at<double>(1, 1);
  double cx = camera_matrix.at<double>(0, 2);
  double cy = camera_matrix.at<double>(1, 2);

  // 像素坐标反投影到相机坐标系 (与find_object_2d相同的方法)
  double x_cam = (u - cx) * depth / fx;
  double y_cam = (v - cy) * depth / fy;
  double z_cam = depth;

  // 创建TF变换
  geometry_msgs::msg::TransformStamped transformstamped;
  transformstamped.header.stamp = msg->header.stamp;
  transformstamped.header.frame_id = camera_frame_id;
  transformstamped.child_frame_id = object_frame_id;

  // RealSense相机坐标系: X右, Y下, Z前
  // 转换为标准坐标系
  transformstamped.transform.translation.x = z_cam;  // Z轴是深度
  transformstamped.transform.translation.y = -x_cam; // X轴向右,取负
  transformstamped.transform.translation.z = -y_cam; // Y轴向下,取负

  // 姿态: 单位四元数 (YOLO不提供旋转信息)
  transformstamped.transform.rotation.x = 0.0;
  transformstamped.transform.rotation.y = 0.0;
  transformstamped.transform.rotation.z = 0.0;
  transformstamped.transform.rotation.w = 1.0;

  // 发布TF
  tf_broadcaster->sendTransform(transformstamped);

  // 获取类别名称
  std::string class_name = "unknown";
  if (!best_detection->results.empty()) {
    class_name = best_detection->results[0].hypothesis.class_id;
  }

  RCLCPP_INFO_THROTTLE(logger, *node->get_clock(), 1000,
                       "检测到 %s (置信度: %.2f), 位置: (%.3f, %.3f, %.3f)m",
                       class_name.c_str(), best_confidence, x_cam, y_cam,
                       z_cam);
}

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::NodeOptions node_options;
  node_options.automatically_declare_parameters_from_overrides(true);
  node = rclcpp::Node::make_shared("yolo_tf_bridge", node_options);

  // 声明参数
  node->declare_parameter("min_confidence", 0.5);
  node->declare_parameter("object_frame_id", "object_1");
  node->declare_parameter("camera_frame_id", "camera_color_optical_frame");

  // 获取参数
  min_confidence = node->get_parameter("min_confidence").as_double();
  object_frame_id = node->get_parameter("object_frame_id").as_string();
  camera_frame_id = node->get_parameter("camera_frame_id").as_string();

  RCLCPP_INFO(logger, "YOLO TF Bridge 节点已启动");
  RCLCPP_INFO(logger, "发布TF: %s -> %s", camera_frame_id.c_str(),
              object_frame_id.c_str());
  RCLCPP_INFO(logger, "最小置信度: %.2f", min_confidence);

  // 创建TF广播器
  tf_broadcaster = std::make_unique<tf2_ros::TransformBroadcaster>(node);

  // 订阅话题
  auto detection_sub =
      node->create_subscription<vision_msgs::msg::Detection2DArray>(
          "/yolo/detections", 10, detection_callback);

  auto depth_sub = node->create_subscription<sensor_msgs::msg::Image>(
      "/camera/camera/aligned_depth_to_color/image_raw", 10, depth_callback);

  auto camera_info_sub =
      node->create_subscription<sensor_msgs::msg::CameraInfo>(
          "/camera/camera/color/camera_info", 10, camera_info_callback);

  rclcpp::spin(node);
  rclcpp::shutdown();

  return 0;
}
