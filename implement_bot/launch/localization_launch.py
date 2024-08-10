import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription

from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

from launch_ros.actions import Node

from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():

    # config 
    use_slam = LaunchConfiguration('use_slam')
    decl_use_slam = DeclareLaunchArgument(
            'use_slam',
            default_value = 'false',
            choices = ['true', 'false'],
            description = 'Activate mapping '
        )
    package_path = get_package_share_directory('implement_bot')
    slam_params = os.path.join( package_path, 'config', 'mapper_params_online_async.yaml')

    # slam toolbox classic launch
    slam_toolbox = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')]), 
                    launch_arguments={'params-file': slam_params, 'use_sim_time': 'true'}.items(),condition = IfCondition(use_slam)
             )
    
    
    nav2_localization = LaunchDescription(

    )

    ld = LaunchDescription()
    ld.add_action(decl_use_slam)
    ld.add_action(slam_toolbox)


    # ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=map_save.yaml -p use_sim_time:=true
    # ros2 run nav2_util lifecycle_bringup map_server
    # ros2 run nav2_amcl amcl --ros-args -p use_sim_time:=true
    # ros2 run nav2_util lifecycle_bringup amcl

    # Launch them all!
    return ld
