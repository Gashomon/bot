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

# from launch

import xacro

from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():

    # Create a server node
    
    server = Node(
        package="implement_bot",
        executable="server"
    )
    
    # Launch!
    return LaunchDescription([
       server

    ])
