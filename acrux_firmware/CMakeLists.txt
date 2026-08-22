cmake_minimum_required(VERSION 3.8)
project(acrux_firmware)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(action_msgs REQUIRED)


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)

  ament_lint_auto_find_test_dependencies()
endif()

# Install Python modules
ament_python_install_package(${PROJECT_NAME})

add_executable(network_status_publisher_node src/network_status_publisher.cpp)
ament_target_dependencies(network_status_publisher_node rclcpp std_msgs)

add_executable(goal_status_publisher src/goal_status_publisher.cpp)
ament_target_dependencies(goal_status_publisher rclcpp std_msgs action_msgs)


install(TARGETS
  goal_status_publisher
  network_status_publisher_node
  DESTINATION lib/${PROJECT_NAME}
)


install(
  DIRECTORY launch config src
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
