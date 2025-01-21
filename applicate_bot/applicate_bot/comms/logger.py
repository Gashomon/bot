import rclpy
from rclpy.clock import Clock
from rclpy.node import Node
from rclpy.serialization import serialize_message

from std_msgs.msg import String
from sensor_msgs.msg import LaserScan, Range, Imu
from costmap_msgs.msg import CostMap
from geometry_msgs.msg import Twist

import rosbag2_py
import datetime

class DataLogger(Node):

    def _init_(self):

        # ros2 bag & writer
        self.writer = rosbag2_py.SequentialWriter()
        currTime = datetime.datetime.now()

        bag_name = "data" + currTime.year +""+ currTime.day +""+ currTime.hour +""+ currTime.minute +""+ currTime.second
        storage_options = rosbag2_py._storage.StorageOptions(
            uri=bag_name,
            storage_id='sqlite3')
        converter_options = rosbag2_py._storage.ConverterOptions('', '')
        self.writer.open(storage_options, converter_options)

        # Make logger publisher
        self.logger = self.create_publisher(String, 'botLogger', 10)

        # obstacle detection
        lidar_topic = rosbag2_py._storage.TopicMetadata(
            name='ldlidar_node/scan',
            type='sensor_msgs/msg/LaserScan',
            serialization_format='cdr')
        self.writer.create_topic(lidar_topic)

        leftRange_topic = rosbag2_py._storage.TopicMetadata(
            name='left_range_broad/range',
            type='sensor_msgs/msgg/Range',
            serialization_format='cdr')
        self.writer.create_topic(leftRange_topic)

        rightRange_topic = rosbag2_py._storage.TopicMetadata(
            name='right_range_broad/range',
            type='sensor_msgs/msg/Range',
            serialization_format='cdr')
        self.writer.create_topic(rightRange_topic)

        costmap_topic = rosbag2_py._storage.TopicMetadata(
            name='local_costmap/raw',
            type='cost_map_msgs/CostMap',
            serialization_format='cdr')
        self.writer.create_topic(costmap_topic)

        # velocity reader
        imu_topic = rosbag2_py._storage.TopicMetadata(
            name='imu_broad/imu',
            type='sensor_msgs/msg/Imu',
            serialization_format='cdr')
        self.writer.create_topic(imu_topic)

        vel_topic = rosbag2_py._storage.TopicMetadata(
            name='/diff_cont/cmd_vel_unstamped',
            type='geometry_msgs/msg/Twist',
            serialization_format='cdr')
        self.writer.create_topic(vel_topic)

        # pose reader
        # tf_topic = rosbag2_py._storage.TopicMetadata(
        #     name='/tf',
        #     type='geometry_msgs/msg/Twist',
        #     serialization_format='cdr')
        # self.writer.create_topic(tf_topic)
        # 
        # ekf_topic = rosbag2_py._storage.TopicMetadata(
        #     name='/ekf_filter_node/odometry/local',
        #     type='nav_msgs/Odometry)',
        #     serialization_format='cdr')
        # self.writer.create_topic(ekf_topic)
        # 
        # diffcont_topic = rosbag2_py._storage.TopicMetadata(
        #     name='/diff_cont/odom',
        #     type='nav_msgs/Odometry)',
        #     serialization_format='cdr')
        # self.writer.create_topic(diffcont_topic)

        # success reader
        bot_topic = rosbag2_py._storage.TopicMetadata(
            name='botLogger',
            type='std_msgs/msg/String',
            serialization_format='cdr')
        self.writer.create_topic(bot_topic)

        # subscribers
        self.bot_subscriber = self.create_subscription( 
            String,
            'botLogger',
            self.bot_callback,
            10)
        self.bot_subscriber

        self.lidar_timer = self.create_timer(1, self.lidar_callback)
        self.leftRange_timer = self.create_timer(1,self.leftRange_callback)
        self.rightRange_timer = self.create_timer(1,self.rightRange_callback)
        self.costmap_timer = self.create_timer(1, self.costmap_callback)
        self.imu_timer = self.create_timer(1,self.imu_callback)

    # logger function
    def logwrite(self, msg):
            self.msg = String
            self.msg.data = msg
            self.logger.publish(msg)
            self.get_logger().info('[botlogger]: "%s"' % msg.data)

    # writers
    def lidar_callback(self, msg):
        self.writer.write(
            'ldlidar_node/scan',
            serialize_message(msg),
            Clock().now().nanoseconds)

    def leftRange_callback(self, msg):
        self.writer.write(
            'left_range_broad/range',
            serialize_message(msg),
            Clock().now().nanoseconds)
        
    def rightRange_callback(self, msg):
        self.writer.write(
            'right_range_broad/range',
            serialize_message(msg),
            Clock().now().nanoseconds)
    
    def costmap_callback(self, msg):
        self.writer.write(
            'local_costmap/raw',
            serialize_message(msg),
            Clock().now().nanoseconds)
        
    def imu_callback(self, msg):
        self.writer.write(
            'imu_broad/imu',
            serialize_message(msg),
            Clock().now().nanoseconds)
    
    # def vel_callback(self, msg):
    #     self.writer.write(
    #         '/diff_cont/cmd_vel_unstamped',
    #         serialize_message(msg),
    #         Clock().now().nanoseconds)

    # def tf_callback(self, msg):
    #     self.writer.write(
    #         '/tf',
    #         serialize_message(msg),
    #         Clock().now().nanoseconds)
    
    # def ekf_callback(self, msg):
    #     self.writer.write(
    #         '/ekf_filter_node/odometry/local',
    #         serialize_message(msg),
    #         Clock().now().nanoseconds)
    
    # def diffcont_callback(self, msg):
    #     self.writer.write(
    #         'diff_cont/odom',
    #         serialize_message(msg),
    #         Clock().now().nanoseconds)
   
    def bot_callback(self, msg):
        self.writer.write(
            'botLogger',
            serialize_message(msg),
            Clock().now().nanoseconds)
        
def main(args=None):
    rclpy.init(args=args)
    dl = DataLogger()
    rclpy.spin(dl)
    rclpy.shutdown()


if __name__ == '__main__':
    main()