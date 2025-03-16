#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
# from nav2_simple_commander.robot_navigator import BasicNavigator
from applicate_bot.navigation.modded_robot_navigator import BasicNavigator as BasicNavigator
from geometry_msgs.msg import PoseStamped
import tf_transformations
import numpy as np

# 
import sys
from select import select

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty
# 

pop = {
            '1':(3.0, 0.0, np.radians(0)),
            '2':(5.0, 0.0, np.radians(0)),
            '3':(1.5, 0.0, np.radians(0)),
            '4':(-1.0, 0.0, np.radians(0)),
            # '4':(-3.5, 0.0, np.radians(11.31)),
            # '5':(9.0, 2.5, np.radians(155.56)),
            # '6':(3.5, 5.0, np.radians(-125.00)),
            '7':(0.0, 0.0, 0.0)  # Assuming the robot stops facing the original direction
        }
class HousePatrolNode(Node):  
    def __init__(self):
        super().__init__('key_navigator') 
        self.navigator = BasicNavigator()

        # Set initial pose
        initial_pose = self.create_pose_stamped(0.0, 0.0, 0.0)
        self.navigator.setInitialPose(initial_pose)

        # Wait for Nav2 to be active
        self.navigator.waitUntilNav2Active()

        #
        # Forward = +x
        # Right = -y
        # Back = -x
        # left = +y
        
        # Set waypoints and start navigation
        waypoints = [
            self.create_pose_stamped(0.05, 0.0, np.radians(0)), 
            self.create_pose_stamped(1.0, 0.0, np.radians(0)),
            self.create_pose_stamped(0.2, 0.3, np.radians(0)),
            self.create_pose_stamped(-3.5, 0.0, np.radians(11.31)),
            self.create_pose_stamped(9.0, 2.5, np.radians(155.56)),
            self.create_pose_stamped(3.5, 5.0, np.radians(-125.00)),
            self.create_pose_stamped(0.0, 0.0, 0.0)  # Assuming the robot stops facing the original direction
        ]
        self.set_path()

    def create_pose_stamped(self, position_x, position_y, orientation_z):
        q_x, q_y, q_z, q_w = tf_transformations.quaternion_from_euler(0.0, 0.0, orientation_z)
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.navigator.get_clock().now().to_msg()
        pose.pose.position.x = position_x
        pose.pose.position.y = position_y
        pose.pose.position.z = 0.0
        pose.pose.orientation.x = 0.0
        pose.pose.orientation.y = 0.0
        pose.pose.orientation.z = q_z
        pose.pose.orientation.w = q_w
        return pose

    def follow_waypoints(self, waypoints):
        self.navigator.clearAllCostmaps()
        self.navigator.goToPose(waypoints)
        while not self.navigator.isTaskComplete():
            feedback = self.navigator.getFeedback()
            self.get_logger().info('Navigation Feedback: %s' % feedback)
        result = self.navigator.getResult()
        self.get_logger().info('Navigation Result: %s' % result)
        self.set_path()
# 
    def get_key(self, settings, timeout):
        if sys.platform == 'win32':
            # getwch() returns a string on Windows
            key = msvcrt.getwch()
        else:
            tty.setraw(sys.stdin.fileno())
            # sys.stdin.read() returns a string on Linux
            rlist, _, _ = select([sys.stdin], [], [], timeout)
            if rlist:
                key = sys.stdin.read(1)
            else:
                key = ''
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key
    
    def saveTerminalSettings(self):
        if sys.platform == 'win32':
            return None
        return termios.tcgetattr(sys.stdin)

    def restoreTerminalSettings(old_settings):
        if sys.platform == 'win32':
            return
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    def set_path(self):
        settings = self.saveTerminalSettings()
        key_timeout = 0.5
        self.get_logger().info('Starting. Press some keys...\n')
        while(1):
            key = self.get_key(settings, key_timeout)
            if key in pop.keys():
                dest = self.create_pose_stamped(pop[key][0], pop[key][1], pop[key][2])
                self.follow_waypoints(dest)
                self.get_logger().info('Finished! Press some keys...\n')
            else:
                # self.get_logger().info('Press some keys...\n')
                if (key == '\x03'):
                    break
# 
def main(args=None):
    rclpy.init(args=args)
    node = HousePatrolNode()  
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
