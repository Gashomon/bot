cmake_minimum_required(VERSION 3.5)
project(implement_bot)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(pluginlib REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

# ALL CODE dependencies
# find_package(applicate_bot REQUIRED)

# Navigation dependencies
# find_package(robot_description REQUIRED)
find_package(nav2_bringup REQUIRED)
find_package(nav2_amcl REQUIRED)
find_package(nav2_map_server REQUIRED)
find_package(slam_toolbox REQUIRED)

# HARDWARE dependencies
find_package(hardware_interface REQUIRED)
# find_package(python3-serial REQUIRED)

# SENSOR dependencies
# find_package(imu_sensor_broadcaster REQUIRED)
# find_package(rplidar_ros REQUIRED)
# find_package(ldlidar-robot-ros2 REQUIRED)
find_package(ros2_control REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(controller_manager REQUIRED)
find_package(backward_ros REQUIRED)

# SENSOR dependencies
find_package(imu_sensor_broadcaster REQUIRED)
find_package(rplidar_ros REQUIRED)


# ROS2CONTROl dependencies

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(
  DIRECTORY 
    config
    description
    hardware
    import 
    launch
    maps
    worlds
  DESTINATION share/${PROJECT_NAME}
)

## COMPILE ROS2 Libraries
add_library(
  diffbot_system
  SHARED
  hardware/diffbot_system.cpp
)
target_compile_features(diffbot_system PUBLIC cxx_std_17)
target_include_directories(diffbot_system PUBLIC
$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/hardware/include>
$<INSTALL_INTERFACE:include/diffbot_system>
)
ament_target_dependencies(
  diffbot_system PUBLIC
  hardware_interface
  pluginlib
  rclcpp
  rclcpp_lifecycle
  rclcpp_components
  # serial
  
)
target_link_libraries(diffbot_system PUBLIC serial)

# Export hardware plugins
pluginlib_export_plugin_description_file(hardware_interface diffbot_system.xml)

# INSTALL
install(
  DIRECTORY hardware/include/
  DESTINATION include/
)

install(TARGETS diffbot_system
  EXPORT export_diffbot_system
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

ament_export_targets(export_diffbot_system HAS_LIBRARY_TARGET)
ament_export_dependencies(
  hardware_interface
  pluginlib
  rclcpp
  rclcpp_lifecycle
  rclcpp_components
  # serial
)

  # install(TARGETS implement_bot
  #   EXPORT implement_bot
  #   ARCHIVE DESTINATION lib
  #   LIBRARY DESTINATION lib
  #   RUNTIME DESTINATION bin
  # )
# SETTING EXECUTABLES

# launch directory
# set(launch_dir "src/bot/implement_bot/launch/")

# # To record launch files as executables
# add_executable(visuals ${launch_dir}visuals.launch.py)

# # To add dependencies specifially for each executable
# # ament_target_dependencies()

# # To enable all recorded executables to the computer
# install(
#   TARGETS
#   visuals
#   DESTINATION lib/${PROJECT_NAME}
# )

ament_package()
