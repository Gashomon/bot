#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
# from nav2_simple_commander.robot_navigator import BasicNavigator
from applicate_bot.navigation.robot_navigator import BasicNavigator as BasicNavigator
from geometry_msgs.msg import PoseStamped
import tf_transformations

import sys
from select import select

import os
if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty

class NavigationNode(Node):  
    def __init__(self):
        super().__init__('NavigationNode') 
        self.navigator = BasicNavigator()

        # Set initial pose
        initial_pose = self.create_pose_stamped(0.0, 0.0, 0.0)
        self.navigator.setInitialPose(initial_pose)
        print("pop")
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
    
    def simpleDrive(self, destinations, dest): #only destination points
        if destinations.get(dest) is not None:
            station = [
                # self.create_pose_stamped(0.0, 0.0, 0.0),
                self.create_pose_stamped(destinations[dest][0], destinations[dest][1], destinations[dest][2])  
            ]
            self.follow_waypoints(station)
        else:
            print('wrong points')
        return
    
    # def complexDrive(self, dest[]) #inputting many points


def main(args=None):
    rclpy.init(args=args)
    node = NavigationNode() 
    try:
        rclpy.spin(node)
    
    except Exception as e:
        print(e)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
