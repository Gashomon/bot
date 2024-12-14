import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Find the nav2_bringup and robot_simulation packages
    # nav2_bringup_share_dir = FindPackageShare(package='nav2_bringup').find('nav2_bringup')
    pkg_dir = FindPackageShare(package='implement_bot').find('implement_bot')

    # Localization and navigation launch file paths
    localization_launch_file = os.path.join(pkg_dir, 'import', 'modded_localization.py')
    navigation_launch_file = os.path.join(pkg_dir, 'import', 'modded_navigation.py')

    # Path to the custom nav2_params.yaml file
    navloc_params_file_path = os.path.join(pkg_dir, 'config', 'full_navigation_params.yaml')
    config_path = os.path.join(pkg_dir, 'config')
    map_path = os.path.join(pkg_dir, 'maps')

    # Declare launch arguments
    declare_map_file_path_cmd = DeclareLaunchArgument(
        name='map_file_path',
        default_value= os.path.join(map_path, 'modded_actual.yaml'),
        description='Path to the map file')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='false',
        description='Use simulation time if true')

    # Include the localization launch file with custom nav2 parameters
    start_localization_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(localization_launch_file),
        launch_arguments={
            'map': os.path.join(map_path, 'modded_actual.yaml'),
            'params_file': navloc_params_file_path
        }.items()
    )

    # Include the navigation launch file with custom nav2 parameters
    start_navigation_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(navigation_launch_file),
        launch_arguments={
            'map_subscribe_transient_local': 'true',
            'params_file': navloc_params_file_path
        }.items()
    )

    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_map_file_path_cmd)
    ld.add_action(declare_use_sim_time_cmd)

    # Add actions
    ld.add_action(start_localization_cmd)
    ld.add_action(start_navigation_cmd)

    return ld
