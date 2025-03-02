# Main launch file with simulations & gui

# Combined Bot & visuals launch 

# import package path-finding method1
import os
from ament_index_python.packages import get_package_share_directory

# # import package path-finding method2
# from launch_ros.substitutions import FindPackageShare
# from launch.substitutions import PathJoinSubstitution

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

    package_name='implement_bot' #<--- CHANGE ME
    package_path = get_package_share_directory(package_name)

    # Visuals Launcher Args
    default_rviz = os.path.join(package_path,'config/rviz/nav2_config.rviz')
    world_n = 'botworld.world'
    default_world = os.path.join(package_path,'worlds', world_n)

    # Bot Launcher Args
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
    # path finding method 1
    package_path = get_package_share_directory(package_name)
    visuals_launch_path = os.path.join( package_path,'launch','visuals.launch.py')
    bot_launch_path = os.path.join( package_path,'launch','bot.launch.py')

    # path finding method 2
    # package_path = FindPackageShare(package_name)
    # states_publisher_path = PathJoinSubstitution([package_path, 'launch', 'states.launch.py'])

    # Include the Gazebo launch file, provided by the gazebo_ros package
    visuals_launch = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(visuals_launch_path),
                launch_arguments={'default_rviz' : default_rviz, 'default_world' : default_world}.items()
    ) 

    # Include the Gazebo launch file, provided by the gazebo_ros package
    bot_launch = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(bot_launch_path),
                launch_arguments={'use_sim_time' : use_sim_time, 'jsp_on' : jsp_on}.items()
    )
    
    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
                        arguments=['/TOPIC@ROS_MSG@IGN_MSG'],
                        output='screen')

    
    ld = LaunchDescription()

    # parameters
    ld.add_action(decl_sim_time)
    ld.add_action(decl_jsp_on)

    #launch files
    ld.add_action(visuals_launch)
    # ld.add_action(spawn_bridge)
    ld.add_action(bot_launch)

    # Launch them all!
    return ld
