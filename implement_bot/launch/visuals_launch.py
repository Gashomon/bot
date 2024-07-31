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
    xacro_file = os.path.join(pkg_path,'description','main_urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    world_file = 'meh'
    # Create a robot_state_publisher node
    params = {'topic': robot_description_config.toxml(), 'name': use_sim_time, 'world': world_file}
    
    gazebo = Node(
        package='ros_gz', 
        executable='create',
        output='screen')

    # added state publisher gui
    joint_state_publisher = Node(
        package='rviz2', 
        executable='rviz2',
        output='screen',
        params = ''
        )

    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),

        robot_state_publisher,
        joint_state_publisher 
    ])
