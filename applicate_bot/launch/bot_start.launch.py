# Main Robot launch file

# Combined: sensors, states, & localization launch w/ starting the app

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
    bot_pkg_name='implement_bot' 
    bot_pkg_path = get_package_share_directory(bot_pkg_name)
    map_path = os.path.join(bot_pkg_name, 'maps')

    #states_publisher parameters
    use_sim_time = LaunchConfiguration('use_sim_time')
    jsp_on = LaunchConfiguration('jsp_on')
    map_file_path = LaunchConfiguration('map_file_path')

    # parameters declarations
    declare_sim_time = DeclareLaunchArgument(
            'use_sim_time',
            default_value = 'false',
            description = 'Use sim time if true'
        )
    declare_jsp_on = DeclareLaunchArgument(
            'jsp_on',
            default_value = 'false',
            choices = ['true', 'false'],
            description = 'Actviate joint state publisher'
        )
    declare_map_file_path = DeclareLaunchArgument(
        name='map_file_path',
        default_value= os.path.join(map_path, 'modded_actual.yaml'),
        description='Path to the map file')

    # bot launch file
    bot_path = os.path.join(bot_pkg_path,'launch','bot.launch.py')
    publish_bot = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(bot_path),
                launch_arguments={'use_sim_time': use_sim_time, 'jsp_on': jsp_on}.items()
    )

    # navigation and localization launch file
    navloc_path = os.path.join(bot_pkg_path,'launch','full_navloc.launch.py')
    publish_navloc = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(navloc_path),
                launch_arguments={'use_sim_time': use_sim_time, 'map_file_path': map_file_path}.items()
    )

    # application launch file
    publish_app = Node(
        package = 'applicate_bot',
        executable = 'test',
        output = 'screen',
        parameters = []
    )
    # compressed launch description function
    ld = LaunchDescription()

    # add parameters
    ld.add_action(declare_sim_time)
    ld.add_action(declare_jsp_on)
    ld.add_action(declare_map_file_path)

    # add launch files
    ld.add_action(publish_bot)
    ld.add_action(publish_navloc)
    ld.add_action(publish_app)

    # Launch them all!
    return ld
