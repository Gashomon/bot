# Just some code (the orginal before restructure)

import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='implement_bot' #<--- CHANGE ME

    gazebo_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'gazebo_params.yaml')

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','states.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'jsp_on' : 'false'}.items()
    )
    
    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]), 
                    launch_arguments={'extra_gazebo_args': '--ros-args --params-file' + gazebo_params_file, 'world': './src/bot/implement_bot/worlds/practice.world'}.items()
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')

    # added state publisher
    state_publisher = Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui')

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

    #added keyboard tele operation
    key_teleop = Node(package="teleop_twist_keyboard", executable="teleop_twist_keyboard",
                      arguments=['/cmd_vel:=/diff_cont/cmd_vel'])
    
    twist_stamper = Node(
        package='twist_stamper',
        executable='twist_stamper',
        remappings=[('/cmd_vel_in','/diff_cont/cmd_vel_unstamped'),
                    ('/cmd_vel_out','/diff_cont/cmd_vel')]
      )

    # Launch them all!
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        diff_drive_spawner,
        joint_broad_spawner,
        # twist_stamper
        # key_teleop
    ])
