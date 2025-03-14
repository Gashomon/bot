import os
from launch import LaunchDescription
from launch_ros.actions import Node

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, LifecycleNode

def generate_launch_description():

    node_name = LaunchConfiguration('node_name')
    # Launch arguments
    declare_node_name_cmd = DeclareLaunchArgument(
        'node_name',
        # default_value='ldlidar_node',
        default_value='ldlidar_node',
        description='Name of the node'
    )

    # Lidar node configuration file
    lidar_config_path = os.path.join(
        get_package_share_directory('implement_bot'),
        'config',
        'ldlidar.yaml'
    )

    # Lifecycle manager configuration file
    lc_mgr_config_path = os.path.join(
        get_package_share_directory('implement_bot'),
        'config',
        'lifecycle_mgr.yaml'
    )

    # Lifecycle manager node
    lc_mgr_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager',
        output='screen',
        parameters=[
            # YAML files
            lc_mgr_config_path  # Parameters
        ]
    )

    # LDLidar lifecycle node
    ldlidar_node = LifecycleNode(
        package='ldlidar_node',
        executable='ldlidar_node',
        name=node_name,
        namespace='',
        output='screen',
        parameters=[
            # YAML files
            lidar_config_path  # Parameters
        ]
    )

    return LaunchDescription([
        declare_node_name_cmd,
        lc_mgr_node,
        ldlidar_node
    ])
