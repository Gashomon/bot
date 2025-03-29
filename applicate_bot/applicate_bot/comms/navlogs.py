import rclpy
from rclpy.clock import Clock
from rclpy.node import Node
from rclpy.serialization import serialize_message

from std_msgs.msg import String
from sensor_msgs.msg import LaserScan, Range, Imu
from nav2_msgs.msg import Costmap
from geometry_msgs.msg import Twist
from tf2_msgs.msg import TFMessage

import rosbag2_py
import datetime

class SimpleBagRecorder(Node):
    def __init__(self):
        super().__init__('simple_bag_recorder')
        self.writer = rosbag2_py.SequentialWriter()
        currTime = datetime.datetime.now()

        bag_name = "trial" + str(currTime.year) +"."+ str(currTime.month) +"."+ str(currTime.day) +"."+ str(currTime.hour) +"."+ str(currTime.minute) +"."+ str(currTime.second)
        storage_options = rosbag2_py.StorageOptions(
            uri='/home/pi/data_gather/bags/nav_logs/' + bag_name,
            storage_id='sqlite3')

        converter_options = rosbag2_py.ConverterOptions('', '')
        self.writer.open(storage_options, converter_options)

        # TF
        tf_topic = rosbag2_py.TopicMetadata(
            name='tf',
            type='std_msgs/msg/String',
            serialization_format='cdr')
        self.writer.create_topic(tf_topic)

        self.tf_sub = self.create_subscription(
            TFMessage,
            'tf',
            self.tf_callback,
            10)
        self.tf_sub

        # Joint_States
        joint_topic = rosbag2_py.TopicMetadata(
            name='joint_states',
            type='std_msgs/msg/String',
            serialization_format='cdr')
        self.writer.create_topic(tf_topic)

        self.tf_sub = self.create_subscription(
            TFMessage,
            'joint_states',
            self.tf_callback,
            10)
        self.tf_sub

        # Scan
        tf_topic = rosbag2_py.TopicMetadata(
            name='tf',
            type='std_msgs/msg/String',
            serialization_format='cdr')
        self.writer.create_topic(tf_topic)

        self.tf_sub = self.create_subscription(
            TFMessage,
            'tf',
            self.tf_callback,
            10)
        self.tf_sub

        # Cmd Vel

        # Global Costmap

        # Global Costmap Updates

        # Global Path

        # Goal Pose

        # Odom

        # AMCL

    def tf_callback(self, msg):
        self.writer.write(
            'tf',
            serialize_message(msg),
            self.get_clock().now().nanoseconds)
    
    def joint_callback(self, msg):
        self.writer.write(
            'joint_states',
            serialize_message(msg),
            self.get_clock().now().nanoseconds)


def main(args=None):
    rclpy.init(args=args)
    sbr = SimpleBagRecorder()
    rclpy.spin(sbr)
    rclpy.shutdown()


if __name__ == '__main__':
    main()