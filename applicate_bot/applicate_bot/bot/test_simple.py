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
    'Dean': (0.3, 0.0, 0.0), 
    'CE'  : (0.0, 0.0, 0.0),
    'EE' : (0.0, 0.0, 0.0),
    'CpE'  : (0.0, 0.0, 0.0),
    'ME'  : (0.0, 0.0, 0,0),
    'ECE'  : (0.0, 0.0, 0.0)
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
        # self.waitforcmd()
        self.foreverlooping()
        
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

        # # Wait for Nav2 to be active
        self.navigator.waitUntilNav2Active()
        
        self.lockon()
        self.playfor('activated')

    def run_updates(self):
        self.ui.app.processEvents()
    
    def foreverlooping(self):
        while rclpy.ok():
            print("starting")
            self.waitforcmd()
            print("going back")

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
    
    def playfor(self, situation):
        self.modules.playonce(situation)

    def loadislighterthan(self, limit):
        load = self.modules.getLoad()
        if load > limit: #load is heavy. limit in grams
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
            # self.playfor('cmd_got')
            self.run(t)
        else:
            t = self.server.waitforcmd(t)
            self.playfor('cmd_got')
            self.run(t)
        print("ultra done")
        return

    def run(self, transaction):
        
        reset = None
        self.log("robot_begin")
        if transaction.type == 1:
            reset = self.deliver(transaction)
        if transaction.type == 2:
             reset = self.fetch(transaction)
        if transaction.type == 3:
            reset = self.retrieve(transaction)
        
        print(reset)
        if reset:
            self.log("robot_cancel")
            self.lockon()
        
        print("done")
  
    def deliver(self, transaction):
        t = transaction
        ex = [None]
        
        self.lockoff()
        self.playfor('put_item')
        
        # loop of confirmation
        while True:
            self.run_updates()
            
            # weight check
            snd_onc = True
            while not self.loadislighterthan(10000):
                self.run_updates()
                self.ui.display(mainT="Load too heavy")
                ex[0] = None
                if snd_onc:
                    snd_onc = False
                    self.playfor('heavy')
            snd_onc = True

            # item in check
            q = "Put in your items and close door if finished.\nClick yes if you are done. No to cancel"
            self.ui.check(q, ex)
            if ex[0] is False:
                print("popo")
                return False

            if ex[0] is True:
                self.lockon()
                self.playfor('password')
                print("3")
                # passcode check
                ex = [None]
                q = "This transaction's passcode is: " + t.password + ".\nYes to go, no to abort"
                self.ui.check(q, ex)
                while ex[0] is not True:
                    self.run_updates()
                    if ex[0] is False:
                        print("passcode wrong")
                        ex = [None]
                        break

            # true exit check
            if ex[0] is True:
                break
            if ex[0] is False:
                return False

        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.playfor('leaving')
        
        tp = destinationlist.get(t.dest2)
        pose = self.create_pose_stamped(tp[0], tp[1], tp[2])
        self.goPose(pose)
        # self.playfor('runinng')
        self.ui.display("travelling")
        while not self.navigator.isTaskComplete():
            self.run_updates()
            
        q = "r u user?"
        ex[0] = [None]
        self.ui.check(q, ex)
        self.playfor('arrived') #should be on loop
        while ex[0] is not True:
            self.run_updates()
        
        self.playfor('password')
        ui.verifyuser(t.password)
        self.lockoff()

        q = "Close door. Yes to leave"
        ex[0] = None
        self.ui.check(q, ex)
        self.playfor('remove_item')
        while ex[0] is not True:
            self.run_updates()
        self.lockon()
        
        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.playfor('leaving')

        tp = destinationlist.get("Home")
        pose = self.create_pose_stamped(tp[0], tp[1], tp[2])
        self.goPose(pose)
        # self.playfor('running')

        self.ui.display("travelling")
        while not self.navigator.isTaskComplete():
            self.run_updates()
            
        self.playfor('nothing') 
        self.logger.logwrite("robot_home")

        return False

    def fetch(self, transaction):
        t = transaction

        pose = self.create_pose_stamped(t.dest1)
        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.goPose(pose)
        while not self.navigator.isTaskComplete():
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

        pose = self.create_pose_stamped(t.dest2)
        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.goPose(pose)
        while not self.navigator.isTaskComplete():
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
    
        pose = self.create_pose_stamped(t.dest1)
        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.goPose(pose)
        while not self.navigator.isTaskComplete():
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

        pose = self.create_pose_stamped(t.dest2)
        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.goPose(pose)
        while not self.navigator.isTaskComplete():
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

        pose = self.create_pose_stamped(t.dest1)
        self.ui.display("OTW. step aside. 3 secs")
        time.sleep(3)
        self.goPose(pose)
        while not self.navigator.isTaskComplete():
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