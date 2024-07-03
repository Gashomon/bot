import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro


def generate_launch_description():

    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('bot'))
    
    # added teleop keyboard
    twistkey = Node(package='teleop_twist_keyboard', 
                    executable='teleop_twist_keyboard', 
                    output='screen',
                    arguments=['--ros-agrs', '-r', '/cmd_vel:=/diff_cont/cmd_vel_unstamped'])

    # Launch!
    return LaunchDescription([
        twistkey
        
    ])

    # ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped
