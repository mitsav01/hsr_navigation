cmake_minimum_required(VERSION 3.5)
project(hsr_navigation)

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)

# Install directories (if there are specific resources to install)
install(DIRECTORY launch map src
  DESTINATION share/${PROJECT_NAME}
)

# Install Python script
install(PROGRAMS
  src/global_pose_publisher.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()