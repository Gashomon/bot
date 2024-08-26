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
    use_sim_time = LaunchConfiguration('use_sim_time')
    decl_use_sim_time = DeclareLaunchArgument(
            'use_sim_time',
            default_value = 'true',
            choices = ['true', 'false'],
            description = 'Use sim time if true'
        )
    package_path = get_package_share_directory('implement_bot')
    slam_params = os.path.join( package_path, 'config', 'mapper_params_online_async.yaml')
    robot_localization_file_path = os.path.join(package_path, 'config/ekf.yaml') 
    # slam_params = "/src/bot/implement_bot/config/mapper_params_online_async.yaml"

    # slam toolbox classic launch
    slam_toolbox = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')]), 
                    launch_arguments={'slam_params_file': slam_params, 'use_sim_time': use_sim_time}.items(),condition = IfCondition(use_slam)
             )
    
    # Start robot localization using an Extended Kalman filter
    robot_loc = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[robot_localization_file_path, 
        {'use_sim_time': use_sim_time}])

    # NAV2 STUFF
    nav2_lifecycle_amcl = Node(
        package = "nav2_util",
        executable = "lifecycle_bringup",
        arguments=["amcl"],
    )
    nav2_lifecycle_map = Node(
        package = "nav2_util",
        executable = "lifecycle_bringup",
        arguments=["map_server"]
    )
    nav2_amcl = Node(
        package = "nav2_amcl",
        executable = "amcl",
        arguments = ['p', 'use_sim_time:=true'],
    )
    nav2_map = Node(
        package = "nav2_map_server",
        executable = "map_server",
        arguments=['--ros-args', '-p','yaml_filename:=src/bot/implement_bot/maps/map_save.yaml', '-p', 'use_sim_time:=true'],
    )
    ld = LaunchDescription()
    ld.add_action(decl_use_slam)
    ld.add_action(decl_use_sim_time)
    
    ld.add_action(slam_toolbox)
    # ld.add_action(robot_loc) 
    #  
    # ld.add_action(nav2_lifecycle_amcl)
    # ld.add_action(nav2_lifecycle_map)
    # ld.add_action(nav2_amcl)
    # ld.add_action(nav2_map)

    # ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=src/bot/implement_bot/maps/map_save.yaml -p use_sim_time:=true
    # ros2 run nav2_util lifecycle_bringup map_server --ros-args __node:='hello'
    # ros2 run nav2_amcl amcl --ros-args -p use_sim_time:=true -r __node='hello'
    # ros2 run nav2_util lifecycle_bringup amcl

    # Launch them all!
    return ld
