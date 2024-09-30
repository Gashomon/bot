import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
 
def generate_launch_description():

    # config files unused
    world_name = LaunchConfiguration('world_name')

    rviz_config = LaunchConfiguration('rviz_config')

    # define config file paths
    pkg_path = os.path.join(get_package_share_directory('implement_bot'))
    
    default_rviz = os.path.join(pkg_path,'config/rviz/rviz.rviz')
    # default_rviz = ''
    default_gazebo = os.path.join(pkg_path,'worlds','house.world')

    world_n = 'actual_unfinal.world'
    default_world = os.path.join(pkg_path,'worlds', world_n)

    # gazebo classic launch
    gazebo_cl = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]), 
                    launch_arguments={'world': default_world}.items()
             )

    # creates entity of robot for simulation
    entity_spawner = Node(
        package = 'gazebo_ros', 
        executable = 'spawn_entity.py',
        arguments = ['-topic', 'robot_description', '-entity', 'robot1'],
        output = 'screen',
        name = 'gazebo_spawner'
    )
    
    # rviz launch
    rviz = Node(
        package = 'rviz2', 
        executable = 'rviz2',
        output = 'screen',
        arguments = ['-d', default_rviz],
        name = 'rviz2'
    )

    # Launch!
    return LaunchDescription([
        # DeclareLaunchArgument(
        #     'world_name',
        #     default_value = 'practice.world',
        #     description='loaded world for gazebo'
        # ),
        # DeclareLaunchArgument(
        #     'rviz_config',
        #     default_value = 'rviz.rviz',
        #     description='loaded rviz config'
        # ), 
        
        gazebo_cl,
        entity_spawner,
        rviz    
    ])
