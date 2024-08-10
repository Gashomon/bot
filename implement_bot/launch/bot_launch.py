# Main Robot launch file

# Combined: sensors, states, & localization launch

# import package path-finding functions
import os
from ament_index_python.packages import get_package_share_directory

# import launch functions
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

# import node structures
from launch_ros.actions import Node


# overall launch function
def generate_launch_description():

    # package variables
    package_name='implement_bot' 
    package_path = get_package_share_directory(package_name)

    #states_publisher parameters
    use_sim_time = LaunchConfiguration('use_sim_time')
    jsp_on = LaunchConfiguration('jsp_on')

    # parameters declarations
    decl_sim_time = DeclareLaunchArgument(
            'use_sim_time',
            default_value = 'false',
            description = 'Use sim time if true'
        )
    decl_jsp_on = DeclareLaunchArgument(
            'jsp_on',
            default_value = 'false',
            choices = ['true', 'false'],
            description = 'Actviate joint state publisher'
        )

    # states_publisher launch file
    states_publisher_path = os.path.join( package_path,'launch','states_launch.py')
    states_publisher = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(states_publisher_path),
                launch_arguments={'use_sim_time': use_sim_time, 'jsp_on': jsp_on}.items()
    )

    # compressed launch description function
    ld = LaunchDescription()

    # add parameters
    ld.add_action(decl_sim_time)
    ld.add_action(decl_jsp_on)

    # add launch files
    ld.add_action(states_publisher)

    # Launch them all!
    return ld
