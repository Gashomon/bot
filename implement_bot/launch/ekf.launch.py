import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.actions import DeclareLaunchArgument, LogInfo, TimerAction
from launch_ros.actions import Node

from launch.substitutions import Command
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.actions import TimerAction

# from launch.

import xacro

from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():

    # params
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('implement_bot'))
    
    twist_params = os.path.join(pkg_path, 'config', 'twist_mux.yaml')
    twist_remaps = Node(
        package="twist_mux",
        executable="twist_mux",
        parameters=[twist_params, {use_sim_time:True}],
        remappings=[('/cmd_vel_out', '/diff_cont/cmd_vel_unstamped')]
    )

    ekf_params = os.path.join(pkg_path, 'config', 'ekf_params.yaml')
    ekf = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_node",
        output="log",
        respawn = True,
        respawn_delay=2.0,
        parameters=[ekf_params],
        remappings=[("odometry/filtered", "ekf/odom")],
    )

    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value = 'false',
            description = 'Use sim time if true'
        ),
       
        twist_remaps,
        ekf

    ])
