import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.actions import DeclareLaunchArgument, LogInfo
from launch_ros.actions import Node

# from launch.

import xacro

from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():

    # params
    use_sim_time = LaunchConfiguration('use_sim_time')
    jsp_on = LaunchConfiguration('jsp_on')

    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('implement_bot'))
    xacro_file = os.path.join(pkg_path,'description','main_urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    
    # Create a robot_state_publisher node
    rsp_params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': use_sim_time}
    robot_state_publisher = Node(
        package = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        output = 'screen',
        parameters = [rsp_params]
    )

    # added joint state publisher gui
    joint_state_publisher = Node(
        package = 'joint_state_publisher_gui', 
        executable = 'joint_state_publisher_gui',
        output = 'screen',
        condition = IfCondition(jsp_on)
        )

    twist_params = os.path.join(pkg_path, 'config', 'twist_mux.yaml')
    twist_remaps = Node(
        package="twist_mux",
        executable="twist_mux",
        parameters=[twist_params, {use_sim_time:True}],
        remappings=[('/cmd_vel_out', '/diff_cont/cmd_vel_unstamped')]
    )
    #added ROS2 control spawners 
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
        name = 'diff_drive_controller'
    )

    #added ROS2 control spawners 
    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
        name = 'joint_broad_controller'
    )

    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value = 'false',
            description = 'Use sim time if true'
        ),
        DeclareLaunchArgument(
            'jsp_on',
            default_value = 'false',
            choices = ['true', 'false'],
            description = 'Actviate joint state publisher'
        ),

        robot_state_publisher,
        joint_state_publisher,
        twist_remaps,
        diff_drive_spawner,
        joint_broad_spawner

    ])
