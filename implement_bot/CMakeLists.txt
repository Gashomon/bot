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
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

# CODE dependencies
# find_package(applicate_bot REQUIRED)

# ROBOT dependencies
# find_package(robot_description REQUIRED)
find_package(nav2_bringup REQUIRED)
find_package(nav2_amcl REQUIRED)
find_package(nav2_map_server REQUIRED)
find_package(ros2_control REQUIRED)
find_package(slam_toolbox REQUIRED)

# HARDWARE dependencies
find_package(hardware_interface REQUIRED)
# find_package(python3-serial REQUIRED)

# SENSOR dependencies
# find_package(imu_sensor_broadcaster REQUIRED)
# find_package(rplidar_ros REQUIRED)
# find_package(ldlidar-robot-ros2 REQUIRED)

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
  DIRECTORY config description hardware import launch maps worlds   
  DESTINATION share/${PROJECT_NAME}
)

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
