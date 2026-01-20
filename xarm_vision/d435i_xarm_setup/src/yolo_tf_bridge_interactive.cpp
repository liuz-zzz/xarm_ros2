/* Copyright 2025 UFACTORY Inc. All Rights Reserved.
 *
 * Software License Agreement (BSD License)
 *
 * Interactive YOLO TF Bridge with GUI selection
 *
 * Author: AI Assistant
 ============================================================================*/
#include "sensor_msgs/msg/camera_info.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "vision_msgs/msg/detection2_d_array.hpp"
#include <cv_bridge/cv_bridge.h>
#include <opencv2/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <rclcpp/rclcpp.hpp>

rclcpp::Logger logger = rclcpp::get_logger("yolo_tf_bridge_interactive");
std::shared_ptr<rclcpp::Node> node;
std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster;

// 数据缓存
cv::Mat depth_image;
cv::Mat camera_matrix;
cv::Mat display_image;
bool camera_info_received = false;

// 检测结果缓存
std::vector<vision_msgs::msg::Detection2D> cached_detections;
rclcpp::Time cached_timestamp;

// 交互选择
int selected_detection_index = -1; // -1表示自动选择最高置信度
cv::Point mouse_click_point;
bool new_click = false;

// 参数
double min_confidence = 0.5;
std::string object_frame_id = "object_1";
std::string camera_frame_id = "camera_color_optical_frame";
bool enable_gui = true;

// 鼠标回调函数
void mouse_callback(int event, int x, int y, int flags, void *userdata) {
  if (event == cv::EVENT_LBUTTONDOWN) {
    mouse_click_point = cv::Point(x, y);
    new_click = true;
    RCLCPP_INFO(logger, "鼠标点击: (%d, %d)", x, y);
  }
}

void camera_info_callback(const sensor_msgs::msg::CameraInfo::SharedPtr msg) {
  if (!camera_info_received) {
    camera_matrix = cv::Mat::eye(3, 3, CV_64F);
    camera_matrix.at<double>(0, 0) = msg->k[0];
    camera_matrix.at<double>(1, 1) = msg->k[4];
    camera_matrix.at<double>(0, 2) = msg->k[2];
    camera_matrix.at<double>(1, 2) = msg->k[5];

    camera_info_received = true;
    RCLCPP_INFO(logger, "相机内参已接收");
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

void image_callback(const sensor_msgs::msg::Image::SharedPtr msg) {
  if (!enable_gui)
    return;

  try {
    cv_bridge::CvImagePtr cv_ptr =
        cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
    display_image = cv_ptr->image.clone();
  } catch (cv_bridge::Exception &e) {
    RCLCPP_ERROR(logger, "图像转换错误: %s", e.what());
  }
}

// 检查点是否在边界框内
bool point_in_bbox(const cv::Point &pt,
                   const vision_msgs::msg::Detection2D &detection) {
  double cx = detection.bbox.center.position.x;
  double cy = detection.bbox.center.position.y;
  double w = detection.bbox.size_x;
  double h = detection.bbox.size_y;

  double x1 = cx - w / 2;
  double y1 = cy - h / 2;
  double x2 = cx + w / 2;
  double y2 = cy + h / 2;

  return (pt.x >= x1 && pt.x <= x2 && pt.y >= y1 && pt.y <= y2);
}

// 绘制检测结果
void draw_detections(
    cv::Mat &img, const std::vector<vision_msgs::msg::Detection2D> &detections,
    int selected_idx) {
  for (size_t i = 0; i < detections.size(); i++) {
    const auto &det = detections[i];

    if (det.results.empty())
      continue;

    double confidence = det.results[0].hypothesis.score;
    if (confidence < min_confidence)
      continue;

    // 边界框坐标
    double cx = det.bbox.center.position.x;
    double cy = det.bbox.center.position.y;
    double w = det.bbox.size_x;
    double h = det.bbox.size_y;

    cv::Point pt1(cx - w / 2, cy - h / 2);
    cv::Point pt2(cx + w / 2, cy + h / 2);

    // 选中的用绿色,其他用蓝色
    cv::Scalar color =
        (i == selected_idx) ? cv::Scalar(0, 255, 0) : cv::Scalar(255, 0, 0);
    int thickness = (i == selected_idx) ? 3 : 2;

    // 绘制边界框
    cv::rectangle(img, pt1, pt2, color, thickness);

    // 绘制标签
    std::string class_name = det.results[0].hypothesis.class_id;
    std::string label =
        class_name + " " + std::to_string((int)(confidence * 100)) + "%";

    if (i == selected_idx) {
      label = "[选中] " + label;
    }

    int baseline = 0;
    cv::Size text_size =
        cv::getTextSize(label, cv::FONT_HERSHEY_SIMPLEX, 0.6, 2, &baseline);

    cv::Point text_org(pt1.x, pt1.y - 10);
    cv::rectangle(img, text_org + cv::Point(0, baseline),
                  text_org + cv::Point(text_size.width, -text_size.height),
                  color, cv::FILLED);
    cv::putText(img, label, text_org, cv::FONT_HERSHEY_SIMPLEX, 0.6,
                cv::Scalar(255, 255, 255), 2);
  }

  // 显示提示信息
  std::string hint = "点击物体选择抓取目标 | 按ESC退出";
  cv::putText(img, hint, cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX, 0.7,
              cv::Scalar(0, 255, 255), 2);
}

void detection_callback(
    const vision_msgs::msg::Detection2DArray::SharedPtr msg) {
  if (!camera_info_received || depth_image.empty()) {
    return;
  }

  // 缓存检测结果
  cached_detections.clear();
  for (const auto &det : msg->detections) {
    if (!det.results.empty() &&
        det.results[0].hypothesis.score >= min_confidence) {
      cached_detections.push_back(det);
    }
  }
  cached_timestamp = msg->header.stamp;

  if (cached_detections.empty()) {
    return;
  }

  // 处理鼠标点击
  if (new_click && enable_gui) {
    new_click = false;
    selected_detection_index = -1;

    // 查找点击的检测框
    for (size_t i = 0; i < cached_detections.size(); i++) {
      if (point_in_bbox(mouse_click_point, cached_detections[i])) {
        selected_detection_index = i;
        std::string class_name =
            cached_detections[i].results[0].hypothesis.class_id;
        double conf = cached_detections[i].results[0].hypothesis.score;
        RCLCPP_INFO(logger, "选中物体: %s (置信度: %.2f)", class_name.c_str(),
                    conf);
        break;
      }
    }

    if (selected_detection_index == -1) {
      RCLCPP_WARN(logger, "未点击到任何检测框,将自动选择最高置信度");
    }
  }

  // 确定要发布的检测
  const vision_msgs::msg::Detection2D *target_detection = nullptr;

  if (selected_detection_index >= 0 &&
      selected_detection_index < (int)cached_detections.size()) {
    // 使用手动选择的
    target_detection = &cached_detections[selected_detection_index];
  } else {
    // 自动选择置信度最高的
    double best_conf = 0.0;
    for (const auto &det : cached_detections) {
      double conf = det.results[0].hypothesis.score;
      if (conf > best_conf) {
        best_conf = conf;
        target_detection = &det;
        selected_detection_index = &det - &cached_detections[0];
      }
    }
  }

  if (target_detection == nullptr)
    return;

  // 计算3D坐标并发布TF (与原代码相同)
  int u = static_cast<int>(target_detection->bbox.center.position.x);
  int v = static_cast<int>(target_detection->bbox.center.position.y);

  if (u < 0 || u >= depth_image.cols || v < 0 || v >= depth_image.rows) {
    return;
  }

  // 获取深度值
  int region_size = 5;
  int y_start = std::max(0, v - region_size);
  int y_end = std::min(depth_image.rows, v + region_size);
  int x_start = std::max(0, u - region_size);
  int x_end = std::min(depth_image.cols, u + region_size);

  cv::Mat depth_region =
      depth_image(cv::Range(y_start, y_end), cv::Range(x_start, x_end));

  std::vector<uint16_t> valid_depths;
  for (int i = 0; i < depth_region.rows; i++) {
    for (int j = 0; j < depth_region.cols; j++) {
      uint16_t d = depth_region.at<uint16_t>(i, j);
      if (d > 0)
        valid_depths.push_back(d);
    }
  }

  if (valid_depths.empty())
    return;

  std::sort(valid_depths.begin(), valid_depths.end());
  double depth = valid_depths[valid_depths.size() / 2] * 0.001;

  if (depth < 0.1 || depth > 2.0)
    return;

  // 计算3D坐标
  double fx = camera_matrix.at<double>(0, 0);
  double fy = camera_matrix.at<double>(1, 1);
  double cx = camera_matrix.at<double>(0, 2);
  double cy = camera_matrix.at<double>(1, 2);

  double x_cam = (u - cx) * depth / fx;
  double y_cam = (v - cy) * depth / fy;
  double z_cam = depth;

  // 持续发布TF (抓取节点只读一次,所以持续发布没问题)
  geometry_msgs::msg::TransformStamped transformstamped;
  transformstamped.header.stamp = cached_timestamp;
  transformstamped.header.frame_id = camera_frame_id;
  transformstamped.child_frame_id = object_frame_id;

  transformstamped.transform.translation.x = z_cam;
  transformstamped.transform.translation.y = -x_cam;
  transformstamped.transform.translation.z = -y_cam;

  transformstamped.transform.rotation.x = 0.0;
  transformstamped.transform.rotation.y = 0.0;
  transformstamped.transform.rotation.z = 0.0;
  transformstamped.transform.rotation.w = 1.0;

  tf_broadcaster->sendTransform(transformstamped);

  std::string class_name = target_detection->results[0].hypothesis.class_id;
  double confidence = target_detection->results[0].hypothesis.score;
  RCLCPP_INFO_THROTTLE(logger, *node->get_clock(), 1000,
                       "发布TF: %s (置信度: %.2f), 位置: (%.3f, %.3f, %.3f)m",
                       class_name.c_str(), confidence, x_cam, y_cam, z_cam);

  // 更新显示
  if (enable_gui && !display_image.empty()) {
    cv::Mat display_clone = display_image.clone();
    draw_detections(display_clone, cached_detections, selected_detection_index);
    cv::imshow("YOLO Detection - Click to Select", display_clone);
    cv::waitKey(1);
  }
}

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::NodeOptions node_options;
  node_options.automatically_declare_parameters_from_overrides(true);
  node = rclcpp::Node::make_shared("yolo_tf_bridge_interactive", node_options);

  node->declare_parameter("min_confidence", 0.5);
  node->declare_parameter("object_frame_id", "object_1");
  node->declare_parameter("camera_frame_id", "camera_color_optical_frame");
  node->declare_parameter("enable_gui", true);

  min_confidence = node->get_parameter("min_confidence").as_double();
  object_frame_id = node->get_parameter("object_frame_id").as_string();
  camera_frame_id = node->get_parameter("camera_frame_id").as_string();
  enable_gui = node->get_parameter("enable_gui").as_bool();

  RCLCPP_INFO(logger, "YOLO TF Bridge (交互式) 已启动");
  RCLCPP_INFO(logger, "GUI模式: %s", enable_gui ? "启用" : "禁用");

  tf_broadcaster = std::make_unique<tf2_ros::TransformBroadcaster>(node);

  // 创建GUI窗口
  if (enable_gui) {
    cv::namedWindow("YOLO Detection - Click to Select", cv::WINDOW_NORMAL);
    cv::setMouseCallback("YOLO Detection - Click to Select", mouse_callback,
                         nullptr);
    RCLCPP_INFO(logger, "点击检测框选择抓取目标");
  }

  // 订阅话题
  auto detection_sub =
      node->create_subscription<vision_msgs::msg::Detection2DArray>(
          "/yolo/detections", 10, detection_callback);

  auto depth_sub = node->create_subscription<sensor_msgs::msg::Image>(
      "/camera/camera/aligned_depth_to_color/image_raw", 10, depth_callback);

  auto camera_info_sub =
      node->create_subscription<sensor_msgs::msg::CameraInfo>(
          "/camera/camera/color/camera_info", 10, camera_info_callback);

  auto image_sub = node->create_subscription<sensor_msgs::msg::Image>(
      "/camera/camera/color/image_raw", 10, image_callback);

  rclcpp::spin(node);

  if (enable_gui) {
    cv::destroyAllWindows();
  }

  rclcpp::shutdown();
  return 0;
}
