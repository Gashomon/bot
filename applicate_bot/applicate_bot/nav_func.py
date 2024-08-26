#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
import tf_transformations
import numpy as np

import sys
from select import select

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty

# Set waypoints and start navigation
waypoints = {
            '1':(4.0, 2.5, np.radians(0)),
            '2':(2.5, 2.5, np.radians(90)),
            '3':(2.5, 7.0, np.radians(-130.60)),
            '4':(-3.5, 0.0, np.radians(11.31)),
            '5':(9.0, 2.5, np.radians(155.56)),
            '6':(3.5, 5.0, np.radians(-125.00)),
            '7':(0.0, 0.0, 0.0)  # Assuming the robot stops facing the original direction
}

def getKey(settings, timeout):
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

def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)

def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

class NavigationNode(Node):  
    def __init__(self):
        super().__init__('nav_func') 
        self.navigator = BasicNavigator()

        # Set initial pose
        initial_pose = self.create_pose_stamped(0.0, 0.0, 0.0)
        self.navigator.setInitialPose(initial_pose)

        # Wait for Nav2 to be active
        self.navigator.waitUntilNav2Active()

    def create_pose_stamped(self, position_x, position_y, orientation_z):
        q_x, q_y, q_z, q_w = tf_transformations.quaternion_from_euler(0.0, 0.0, orientation_z)
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.navigator.get_clock().now().to_msg()
        pose.pose.position.x = position_x
        pose.pose.position.y = position_y
        pose.pose.position.z = 0.0
        pose.pose.orientation.x = q_x
        pose.pose.orientation.y = q_y
        pose.pose.orientation.z = q_z
        pose.pose.orientation.w = q_w
        return pose

    def follow_waypoints(self, waypoints):
        self.navigator.followWaypoints(waypoints)
        while not self.navigator.isTaskComplete():
            feedback = self.navigator.getFeedback()
            self.get_logger().info('Navigation Feedback: %s' % feedback)
        result = self.navigator.getResult()
        self.get_logger().info('Navigation Result: %s' % result)

def main(args=None):
    rclpy.init(args=args)
    node = NavigationNode() 
    settings = saveTerminalSettings()
    key_timeout = 0.5
    for i in waypoints.keys():
        node.create_pose_stamped(waypoints[i][0], waypoints[i][1], waypoints[i][2])

    try:
        rclpy.spin(node)
        
        while(1):
            key = getKey(settings, key_timeout)
            if key in waypoints.keys():
                curr_way = node.create_pose_stamped(waypoints[key][0], waypoints[key][1], waypoints[key][2])
                node.follow_waypoints(curr_way)
            else:
                self.get_logger().info('bing chilling...\n')
                if (key == '\x03'):
                    break

    except Exception as e:
        print(e)
    finally:
        restoreTerminalSettings(settings) 
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
