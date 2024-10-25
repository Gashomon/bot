# ROS COMMANDS
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/cmd_vel_key
rqt_graph
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=./src/bot/implement_bot/config/mapper_params_online_async.yaml use_sim_time:=true
ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=map_save.yaml -p use_sim_time:=true
ros2 run nav2_util lifecycle_bringup map_server
ros2 run nav2_amcl amcl --ros-args -p use_sim_time:=true
ros2 run nav2_util lifecycle_bringup amcl
ros2 launch bot launch_sim.launch.py

# ROS2 CONTROL
ros2 topic pub /diff_cont/cmd_vel_unstamped geometry_msgs/msg/Twist "{linear: {x: -1.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" --rate 10

# Gazebo Classic

# RVIZ

# LIDAR
ros2 run ldlidar_node ldlidar_node # <--- not recommended. Better using the launch file 
ros2 lifecycle set /lidar_node configure
ros2 lifecycle set /lidar_node activate
ros2 launch ldlidar_node ldlidar.launch.py
ros2 launch ldlidar_node ldlidar_with_mgr.launch.py
ros2 launch ldlidar_node ldlidar_rviz2.launch.py

# SERIAL
ros2 run applicate_bot motor_driver --ros-args -p serial_port:=/dev/ttyUSB0 -p baud_rate:=57600 -p loop_rate:=30 -p encoder_cpr:=2000