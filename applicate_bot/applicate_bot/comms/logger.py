import rclpy
from rclpy.clock import Clock
from rclpy.node import Node
from rclpy.serialization import serialize_message

from std_msgs.msg import String
from sensor_msgs.msg import LaserScan, Range, Imu
from nav2_msgs.msg import Costmap
from geometry_msgs.msg import Twist

import rosbag2_py
import datetime

class DataLogger(Node):

    def __init__(self):

        super().__init__('logger') # node name 
        # ros2 bag & writer
        self.writer = rosbag2_py.SequentialWriter()
        currTime = datetime.datetime.now()

        bag_name = "data" + str(currTime.year) +""+ str(currTime.month) +""+ str(currTime.day) +""+ str(currTime.hour) +""+ str(currTime.minute) +""+ str(currTime.second)
        storage_options = rosbag2_py._storage.StorageOptions(
            uri="bags/" +bag_name,
            storage_id='sqlite3')
        converter_options = rosbag2_py._storage.ConverterOptions('', '')
        self.writer.open(storage_options, converter_options)

        # Make logger publisher
        self.logger = self.create_publisher(String, 'botLogger', 10)

        # timered messages
        self.lidar_msg = ""
        self.leftRange_msg = ""
        self.rightRange_msg = ""
        self.costmap_msg = ""
        self.imu_msg = ""
        self.vel_msg = ""
        
        # new message marks
        self.new_lidar_msg = False
        self.new_leftRange_msg = False
        self.new_rightRange_msg = False
        self.new_costmap_msg = False
        self.new_imu_msg = False
        self.new_vel_msg = False

        # obstacle detection
        lidar_topic = rosbag2_py._storage.TopicMetadata(
            name='ldlidar_node/scan',
            type='sensor_msgs/msg/LaserScan',
            serialization_format='cdr')
        self.writer.create_topic(lidar_topic)

        leftRange_topic = rosbag2_py._storage.TopicMetadata(
            name='left_range_broad/range',
            type='sensor_msgs/msg/Range',
            serialization_format='cdr')
        self.writer.create_topic(leftRange_topic)

        rightRange_topic = rosbag2_py._storage.TopicMetadata(
            name='right_range_broad/range',
            type='sensor_msgs/msg/Range',
            serialization_format='cdr')
        self.writer.create_topic(rightRange_topic)

        costmap_topic = rosbag2_py._storage.TopicMetadata(
            name='local_costmap/raw',
            type='nav2_msgs/msg/CostMap',
            serialization_format='cdr')
        self.writer.create_topic(costmap_topic)

        # velocity reader
        imu_topic = rosbag2_py._storage.TopicMetadata(
            name='imu_broad/imu',
            type='sensor_msgs/msg/Imu',
            serialization_format='cdr')
        self.writer.create_topic(imu_topic)

        vel_topic = rosbag2_py._storage.TopicMetadata(
            name='diff_cont/cmd_vel_unstamped',
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

        self.lidar_subscriber = self.create_subscription( 
            LaserScan,
            'ldlidar_node/scan',
            self.lidar_callback,
            10)
        self.lidar_subscriber

        self.leftRange_subscriber = self.create_subscription( 
            Range,
            'left_range_broad/range',
            self.leftRange_callback,
            10)
        self.bot_subscriber

        self.rightRange_subscriber = self.create_subscription( 
            Range,
            'right_range_broad/range',
            self.rightRange_callback,
            10)
        self.rightRange_subscriber

        self.costmap_subscriber = self.create_subscription( 
            Costmap,
            'local_costmap/raw',
            self.costmap_callback,
            10)
        self.costmap_subscriber

        self.imu_subscriber = self.create_subscription( 
            Imu,
            'imu_broad/imu',
            self.imu_callback,
            10)
        self.imu_subscriber

        self.vel_subscriber = self.create_subscription( 
            Twist,
            'diff_cont/vel_unstampedr',
            self.vel_callback,
            10)
        self.vel_subscriber

        # timered writers
        self.timer = self.create_timer(1, self.lidar_writer)
        # self.leftRange_timer = self.create_timer(1,self.leftRange_writer())
        # self.rightRange_timer = self.create_timer(1,self.rightRange_writer())
        # self.costmap_timer = self.create_timer(1, self.costmap_writer())
        # self.imu_timer = self.create_timer(1,self.imu_writer())

    # logger function
    def logwrite(self, msg):
            self.msg = String
            self.msg.data = msg
            self.logger.publish(msg)
            self.get_logger().info('[botlogger]: "%s"' % msg.data)

    # callbacks
    def lidar_callback(self, msg):
        self.lidar_msg = serialize_message(msg)
        self.new_lidar_msg = True

    def leftRange_callback(self, msg):
        self.leftRange_msg = serialize_message(msg)
        self.new_leftRange_msg = True
        
    def rightRange_callback(self, msg):
        self.rightRange_msg = serialize_message(msg)
        self.new_rightRange_msg = True
    
    def costmap_callback(self, msg):
        self.costmap_msg = serialize_message(msg)
        self.new_costmap_msg = True
        
    def imu_callback(self, msg):
        self.imu_msg = serialize_message(msg)
        self.new_imu_msg = True
    
    def vel_callback(self, msg):
        self.vel_msg = serialize_message(msg)
        self.new_vel_msg = True

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
   
    # writers
    def lidar_writer(self):
        if self.new_lidar_msg:
            self.writer.write(
                'ldlidar_node/scan',
                self.lidar_msg,
                Clock().now().nanoseconds)
            self.new_lidar_msg = False

    def leftRange_writer(self):
        if self.new_leftRange_msg:
            self.writer.write(
                'left_range_broad/range',
                self.leftRange_msg,
                Clock().now().nanoseconds)
            self.new_leftRange_msg = False
        
    def rightRange_writer(self):
        if self.new_rightRange_msg:
            self.writer.write(
                'right_range_broad/range',
                self.rightRange_msg,
                Clock().now().nanoseconds)
            self.new_rightRange_msg = False
    
    def costmap_writer(self):
        if self.new_costmap_msg:
            self.writer.write(
                'local_costmap/raw',
                self.costmap_msg,
                Clock().now().nanoseconds)
            self.new_costmap_msg = False
        
    def imu_writer(self):
        if self.new_imu_msg:
            self.writer.write(
                'imu_broad/imu',
                self.imu_msg,
                Clock().now().nanoseconds)
            self.new_imu_msg = False
    
    def vel_writer(self):
        if self.new_vel_msg:
            self.writer.write(
                'diffcont/vel_unstamped',
                self.vel_msg,
                Clock().now().nanoseconds)
            self.new_vel_msg = False

    # bot writer & callback
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