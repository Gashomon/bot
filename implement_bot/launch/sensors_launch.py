import os
from launch import LaunchDescription
# from launch_ros.actions import Node

from launch_ros.actions import Node, LifecycleNode
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    lidar_sensor = Node(
        package='rplidar_ros',
        executable='rplidar_composition',
        output='screen',
        parameters=[{
            'serial_port': '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.3:1.0-port0',
            'frame_id': 'laser_frame',
            'angle_compensate': True,
            'scan_mode': 'Standard'
        }],
        name = 'lidar'
    )

    lidar_pkg_dir = "/home/asho/path_bot/src/ldrobot-lidar-ros2"
    node_name = 'ldlidar_node'

    lidar_config_path = os.path.join(
        get_package_share_directory('implement_bot'),
        'config',
        'ldlidar.yaml'
    )

    ldlidar_node = LifecycleNode(
        package='ldlidar_node',
        executable='ldlidar_node',
        name=node_name,
        namespace='',
        output='screen',
        parameters=[
            # YAML files
            lidar_config_path  # Parameters
        ]
    )

    return LaunchDescription([
        # lidar_sensor,
        ldlidar_node
    ])
