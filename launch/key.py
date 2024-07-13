import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():

    #added keyboard tele operation
    key_teleop = Node(  package="teleop_twist_keyboard", 
                        executable="teleop_twist_keyboard",
                        output='screen',
                        prefix='xterm -e',
                        arguments=['/cmd_vel:=/diff_cont/cmd_vel_unstamped'])
    
    # Launch them all!
    return LaunchDescription([
        key_teleop
    ])
