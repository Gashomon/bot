#ROS COMMANDS
# ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped
# rqt_graph
# ros2 launch slam_toolbox online_async_launch.py slam_params_file:=./src/bot/config/mapper_params_online_async.yaml use_sim_time:=true
# ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=map_save.yaml -p use_sim_time:=true
# ros2 run nav2_util lifecycle_bringup map_server
# ros2 run nav2_amcl amcl --ros-args -p use_sim_time:=true
# ros2 run nav2_util lifecycle_bringup amcl
# ros2 launch bot launch_sim.launch.py

# ROS CONTROL
# ros2 topic pub /diff_cont/cmd_vel_unstamped geometry_msgs/msg/Twist "{linear: {x: -1.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" --rate 10


