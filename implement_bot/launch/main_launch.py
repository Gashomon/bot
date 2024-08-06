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

# import node structures
from launch_ros.actions import Node


# overall launch function
def generate_launch_description():

    package_name='bot' #<--- CHANGE ME

    # path finding method 1
    package_path = get_package_share_directory(package_name)
    states_publisher_path = os.path.join( package_path,'launch','states.launch.py')

    #path finding method 2
    # package_path = FindPackageShare(package_name)
    # states_publisher_path = PathJoinSubstitution([package_path, 'launch', 'states.launch.py'])

    states_publisher = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(states_publisher_path),
                launch_arguments={'use_sim_time': 'true'}.items()
    )
    
    # Include the Gazebo launch file, provided by the gazebo_ros package
    visuals_launch = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(states_publisher_path),
                launch_arguments={'use_sim_time': 'true'}.items()
    )
    gazebo = Node(package='ros_gz', executable='create',
                        arguments=['-topic', 'robot_description',
                                   '-name', 'robot', '-world', 'default'],
                        output='screen')
    
    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='ros_gz_bridge', executable='parameter_bridge',
                        arguments=['/TOPIC@ROS_MSG@IGN_MSG'],
                        output='screen')

    #added ROS2 control spawners 
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    #added ROS2 control spawners 
    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    ld = LaunchDescription()

    # parameters
    ld.add_action()

    #launch files
    ld.add_action(states_publisher)

    # Launch them all!
    return LaunchDescription([
        states_publisher,
        gazebo,
        # spawn_entity,
        # diff_drive_spawner,
        # joint_broad_spawner
    ])
