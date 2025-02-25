from enum import Enum
import random
import time

from applicate_bot.modules.modules import Modules as Modules
# import applicate_bot.navigation.nav_func as Nav
from applicate_bot.navigation.modded_robot_navigator import BasicNavigator as Navigator
# import applicate_bot.gui.guiros as UI
from applicate_bot.gui.gui import UserInterface as UI
from applicate_bot.comms.command_server import ServerSub as Server
from applicate_bot.comms.logger import DataLogger as Logger 

import rclpy
from rclpy.node import Node
import sys

from geometry_msgs.msg import PoseStamped
import tf_transformations
import numpy as np
from std_msgs.msg import String

longsituationslist = {}
# shortsituationslist = {'load'} # unneeded list

destinationlist = {
    'Initial': (0.0, 0.0, 0.0), 
    'Home': (0.0, 0.0, 0.0), 
    'Dean': (1.0, 0.0, 0.0), 
    'CE'  : (0.3, 0.0, 0.0),
    'EE' : (0.3, 0.0, 0.0),
    'CpE'  : (0.3, 0.0, 0.0),
    'ME'  : (0.3, 0.0, 0,0),
    'ECE'  : (0.3, 0.0, 0.0)
}

class TransacType(Enum):
    DELIVER = '1'
    FETCH = '2'
    RETRIEVE = '3'

class Transaction():
    sender = ""
    receiver = ""
    password = ""
    type = None
    dest1 = None
    dest2 = None
    
class Bot(Node):

    def __init__(self):
        super().__init__('appbot') 

        self.EXPERIMENTAL=True
        
        # audio folders. starting from home/pi
        path_of_audios = '/home/pi/bot/src/bot/applicate_bot/applicate_bot/modules/sounds/'
        self.modules = Modules(setlock= -1, setloadin= -1, setloadout = -1, setdoor= -1, soundenable=True, soundpath=path_of_audios)

        self.navigator = Navigator()
        self.server = Server()
        self.logger = Logger()
        self.ui = UI()
        self.timer = self.create_timer(0.1, self.run_updates)
        
        self.loadbot()
        self.waitforcmd()
        
        
    # def __init__(self, modules, nav, server, ui, logger) -> None:
    #     self.EXPERIMENTAL = True
    #     self.modules = modules
    #     self.nav = nav
    #     self.server = server
    #     self.ui = ui
    #     self.logger = logger

    # A BIT OF LOOPING COMPILER STUFFS
    def loadbot(self):
        self.playfor('loading')
        self.ui.widget.show()

        # Set initial pose
        initial_pose = self.create_pose_stamped(0.0, 0.0, 0.0)
        self.navigator.setInitialPose(initial_pose)

        # Wait for Nav2 to be active
        self.navigator.waitUntilNav2Active()
        
        self.lockon()
        self.playfor('activated')

    def run_updates(self):
        self.ui.app.processEvents()
    
    def foreverlooping(self):
        while rclpy.ok():
            self.waitforcmd()

    # NAVIGATOR STUFF
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
            feedback = self.getFeedback()
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
    
    def goPose(self, pose):
        self.navigator.goToPose(pose)

    # MODULES STUFF
    def lockon(self):
        self.modules.setlock('on')
        self.playfor('locked')
    
    def lockoff(self):
        self.modules.setlock('off')
        self.playfor('unlocked')
    
    def dooropen(self): # unimplemented door stuff
        door = self.modules.getdoorstate()
        if door == 'open':
            return True
        if door == 'close':
            return False
    
    def doorlocked(self): # unimplemented door stuff
        lock = self.modules.getlockstate()
        if lock == 'on':
            return True
        if lock == 'off':
            return False
        
    def playfor(self, situation):
        if longsituationslist.get(situation) is not None:
            self.modules.playloop(situation)
        else:
        # if shortsituationslist.get(situation) is not None:
            self.modules.playonce(situation)

    def loadislighterthan(self, limit):
        load = self.modules.getLoad()
        if load > limit: #load is heavy
            self.playfor('heavy')
            return False
        else:
            return True

    # MAIN ROBOT CONTROLLING STUFF    
    def waitforcmd(self):
        if self.EXPERIMENTAL:
            self.ui.goto("control") 
            t = Transaction()
            self.ui.control.pushButton_5.clicked.connect(
                lambda: self.ui.sendcmd(t, 'del'))
            self.ui.control.pushButton_6.clicked.connect(
                lambda: self.ui.sendcmd(t, 'fet'))
            self.ui.control.pushButton_7.clicked.connect(
                lambda: self.ui.sendcmd(t, 'ret'))
            while t.dest1 is None or t.dest2 is None:
                self.run_updates()
            t.password = self.genpass()
            self.playfor('cmd_got')
            
            self.run(t)
        else:
            t = self.server.waitforcmd(t)
            self.playfor('cmd_got')
            self.run(t)
    
    def run(self, transaction):
        
        self.log("robot_begin")
        if transaction.type == TransacType.DELIVER:
            self.deliver(transaction)
        if transaction.type == TransacType.FETCH:
            self.fetch(transaction)
        if transaction.type == TransacType.RETRIEVE:
            self.retrieve(transaction)
    
        while not self.readydrive():
            self.ui.display("Not yet Ready")
        
        pose = self.nav.create_pose_stamped(destinationlist.get("Home"))
        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.nav.goPose(pose)
        self.playfor('running')
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        self.playfor('nothing') 
        self.logger.logwrite("robot_home")
    
    def deliver(self, transaction):
        t = transaction

        pose = self.nav.create_pose_stamped(t.dest1)
        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.nav.goPose(pose)
        self.playfor('running')
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        
        self.playfor('arrived')
        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        self.playfor('password')
        while not self.ui.verifyuser(t.password):
            pass
        
        self.lockoff()
        self.playfor('put_in')
        while True:
            while not self.loadislighterthan(20000):
                self.ui.display("Load too heavy")
                self.playfor('heavy')

            q = "ready to go? close door"
            self.playfor('leaving')
            if self.ui.check(q):
                break

        pose = self.nav.create_pose_stamped(t.dest2)
        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.nav.goPose(pose)
        self.playfor('runinng')
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")

        self.playfor('arrived')
        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        self.playfor('password')
        while not self.ui.verifyuser(t.password):
            pass

        self.lockoff()

        self.playfor('remove_item')
        while True:
            q = "ready to go?"
            self.playfor('leaving')
            if self.ui.check(q):
                break

    def fetch(self, transaction):
        t = transaction

        pose = self.nav.create_pose_stamped(t.dest1)
        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.nav.goPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        
        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        while not self.ui.verifyuser(t.password):
            pass
        
        self.lockoff()

        while True:
            while not self.loadislighterthan(20000):
                self.ui.display("Load too heavy")

            q = "ready to go?"
            if self.ui.check(q):
                break

        pose = self.nav.create_pose_stamped(t.dest2)
        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.nav.goPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")

        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        while not self.ui.verifyuser(t.password):
            pass

        self.lockoff()

        while True:

            q = "ready to go?"
            if self.ui.check(q):
                break
    
        pose = self.nav.create_pose_stamped(t.dest1)
        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.nav.goPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        
        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        while not self.ui.verifyuser(t.password):
            pass
        
        self.lockoff()

        while True:

            q = "ready to go?"
            if self.ui.check(q):
                break

    def retrieve(self, transaction):
        t = transaction

        pose = self.nav.create_pose_stamped(t.dest2)
        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.nav.goPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        
        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        while not self.ui.verifyuser(t.password):
            pass
        
        self.lockoff()

        while True:
            while not self.loadislighterthan(20000):
                self.ui.display("Load too heavy")

            q = "ready to go?"
            if self.ui.check(q):
                break
                    
        while not self.readydrive():
            self.ui.display("Not yet Ready")

        pose = self.nav.create_pose_stamped(t.dest1)
        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.nav.goPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")

        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        while not self.ui.verifyuser(t.password):
            pass

        self.lockoff()

        while True:

            q = "ready to go?"
            if self.ui.check(q):
                break    
        
    def readydrive(self, limit=100):
        # if self.dooropen():
        #     return False
        # if not self.loadislighterthan(limit):
        #     return False
        self.playfor('locked')
        self.lockon()
        return True

    def genpass(self):
        password = ""
        for i in range(4):
            password = password + str(random.randint(0,9))
        return password
    
    def log(self, msg):
        log_msg = String()
        log_msg.data = msg
        return log_msg

def main(args=None):
    rclpy.init(args=args)
    node = Bot() 
    try:
        rclpy.spin(node)
    except Exception as e:
        print(e)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()