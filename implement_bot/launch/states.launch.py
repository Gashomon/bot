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

# from launch.

import xacro

from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():

    # params
    use_sim_time = LaunchConfiguration('use_sim_time')
    jsp_on = LaunchConfiguration('jsp_on')

    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('implement_bot'))
    xacro_file = os.path.join(pkg_path,'description','main_urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = robot_description_config.toxml()

    # Create a robot_state_publisher node
    rsp_params = {'robot_description': robot_description, 'use_sim_time': use_sim_time}
    robot_state_publisher = Node(
        package = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        output = 'screen',
        parameters = [rsp_params]
    )

    # added joint state publisher gui
    joint_state_publisher = Node(
        package = 'joint_state_publisher_gui', 
        executable = 'joint_state_publisher_gui',
        output = 'screen',
        condition = IfCondition(jsp_on)
        )

    twist_params = os.path.join(pkg_path, 'config', 'twist_mux.yaml')
    twist_remaps = Node(
        package="twist_mux",
        executable="twist_mux",
        parameters=[twist_params, {use_sim_time:True}],
        remappings=[('/cmd_vel_out', '/diff_cont/cmd_vel_unstamped')]
    )
        
    # real robot controller manager
    controller_yaml_file = os.path.join(
        get_package_share_directory('implement_bot'),
        'config',
        'bot_controller_params.yaml'
    )

    robobo = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])
    real_bot_controller = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{'robot_description' :robot_description}, controller_yaml_file],
        output={
          'stdout': 'screen',
          'stderr': 'screen',
          }
     ) 
    
    delayed_controller_manager = TimerAction(period=5.0, actions=[real_bot_controller])

    # delayed_controller_manager = RegisterEventHandler(
    #     event_handler=OnProcessStart(
    #         target_action=delayed_robot_params,
    #         on_start=[real_bot_controller],
    #     )
    # )    
    
    # just controller manager
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
     ) 
    
    #added ROS2 control spawners 
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"]
    )

    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=real_bot_controller,
            on_start=[diff_drive_spawner],
        )
    )

    #added ROS2 control spawners 
    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"]
    )
    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=real_bot_controller,
            on_start=[joint_broad_spawner],
        )
    )

    #added ROS2 control spawners 
    imu_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["imu_broad"]
    )
    delayed_imu_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=real_bot_controller,
            on_start=[imu_broad_spawner],
        )
    )

    left_range_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["left_range_broad"]
    )

    right_range_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["right_range_broad"]
    )

    delayed_range_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=real_bot_controller,
            on_start=[right_range_spawner, left_range_spawner],
        )
    )
    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value = 'false',
            description = 'Use sim time if true'
        ),
        DeclareLaunchArgument(
            'jsp_on',
            default_value = 'false',
            choices = ['true', 'false'],
            description = 'Actviate joint state publisher'
        ),

        robot_state_publisher,
        joint_state_publisher,
        twist_remaps,

        #simulation 
        # controller_manager,
        # diff_drive_spawner,
        # joint_broad_spawner

        # real bot
        delayed_controller_manager,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner,
        delayed_imu_broad_spawner,
        delayed_range_broad_spawner

    ])
