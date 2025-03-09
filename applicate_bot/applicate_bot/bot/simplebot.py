from enum import Enum
import random
import time

from applicate_bot.modules.modules import Modules as Modules
from applicate_bot.navigation.modded_robot_navigator import BasicNavigator as Navigator
from applicate_bot.gui.gui import UserInterface as UI
from applicate_bot.comms.command_server import ServerSub as Server
from applicate_bot.comms.logger import DataLogger as Logger 

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
import sys

from geometry_msgs.msg import PoseStamped
import tf_transformations
import numpy as np
from std_msgs.msg import String

longsituationslist = {}

destinationlist = {
    'Initial': (0.0, 0.0, 0.0),
    'Home': (0.0, 0.0, 0.0),
    'Dean': (2.0, 0.0, 0.0), 
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
        path_of_audios = '/home/pi/bot/src/bot/applicate_bot/applicate_bot/modules/real_fx/'
        self.modules = Modules(setlock= -1, setloadin= -1, setloadout = -1, setdoor= -1, soundenable=True, soundpath=path_of_audios)
        # self.modules = Modules(setlock= 17, setloadin= 23, setloadout = 24, setdoor= -1, soundenable=True, soundpath=path_of_audios)

        self.navigator = Navigator()
        self.server = Server()
        self.logger = Logger()
        self.ui = UI()
        self.timer = self.create_timer(0.1, self.run_updates)
        
        self.loadbot()
        self.foreverlooping()

    # A BIT OF LOOPING COMPILER STUFFS
    def loadbot(self):
        self.playfor('loading')
        self.ui.goto('main')
        self.ui.widget.show()
        self.run_updates()


        # Set initial pose
        initial_pose = self.create_pose_stamped(0.0, 0.0, 0.0)
        self.navigator.setInitialPose(initial_pose)

        # # Wait for Nav2 to be active
        self.navigator.waitUntilNav2Active()
        
        # self.lockon() # deact for simplicity
        self.playfor('activated')

    def run_updates(self, event=None):
        
        if(event == "control"):
            self.ui.enableRun()
            self.updateWeight()
            snd_onc = True
            while not self.loadislighterthan(10000): 
                self.ui.app.processEvents()             
                self.ui.disableRun()
                self.updateWeight()
                if snd_onc:
                    snd_onc = False
                    self.playfor('heavy')
            snd_onc = True 
        self.ui.app.processEvents()
        
    def updateWeight(self):
        value = self.modules.getLoad()
        # set value to label if ever
        self.ui.displayWeight(value)

    def foreverlooping(self):
        self.ui.goto('main')
        self.ui.main.pushButton.clicked.connect(self.cmd_btn)
        while rclpy.ok():
            self.run_updates()
            
    def cmd_btn(self):
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
        pose.pose.orientation.x = 0.0
        pose.pose.orientation.y = 0.0
        pose.pose.orientation.z = q_z
        pose.pose.orientation.w = q_w
        return pose

    def goPose(self, goal_pose):
        self.navigator.clearAllCostmaps()
        self.navigator.goToPose(goal_pose)

        i = 0
        while not self.navigator.isTaskComplete():
            i = i + 1
            feedback = self.navigator.getFeedback()
            if feedback and i % 3 == 0:
                self.get_logger().info('Navigation Feedback: %s' % feedback)
                self.get_logger().info(
                    'Estimated time of arrival: '
                    + '{0:.0f}'.format(
                        Duration.from_msg(feedback.estimated_time_remaining).nanoseconds
                        / 1e9
                    )
                    + ' seconds.\n'
            
                )
        result = self.navigator.getResult()
        self.get_logger().info('Navigation Result: %s' % result)

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
        self.lockoff()
        self.ui.goto("control") 
        
        t = Transaction()
        self.ui.control.receiver_name.clear()
        self.ui.control.sender_name.clear()
        self.ui.control.pushButton_5.clicked.connect(
            lambda: self.ui.sendcmd(t))
        while t.dest1 is None or t.dest2 is None:
            self.run_updates("control")
            
        t.password = self.genpass()

        self.playfor('cmd_got')
        self.run(t)
        
        self.ui.goto('main')
        self.run_updates()
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
            return
        
        print("done")
  
    def deliver(self, transaction):
        t = transaction
        
        # passcode check
        ex = [None]
        q = "This transaction's passcode is: " + t.password + ".\nYes to go, no to abort"
        self.ui.check(q, ex)
        while ex[0] is not True:
            self.run_updates()
            if ex[0] is False:
                return True

        self.ui.display(mainT ="Robot is Leaving in 5 seconds. Please step aside.")
        self.run_updates()
        time.sleep(5)
        self.playfor('leaving')
        
        self.lockon()

        #turn off screen
        # self.ui.display("travelling")

        tp = destinationlist.get(t.dest2)
        # pose = self.create_pose_stamped(tp[0], tp[1], tp[2])
        # self.goPose(pose)

        # while not self.navigator.isTaskComplete():
        #     self.run_updates()
            
        #turn on screen

        q = ""
        print(f"sender is {t.sender}\nreceiver is {t.receiver}")
        if t.receiver != "":
            q = "Delivery for " + t.receiver
        if t.sender != "":
            q = q +" from " + t.sender + "\n"
        else:
            q = q + "\n"

        q = q + "Are you Receiver?"
        ex = [None]
        self.ui.check(q, ex)
        self.playfor('arrived') #should be on loop
        while ex[0] is not True:
            self.run_updates()
            if ex[0] is False:
                print('not user daw')
                self.ui.display(mainT = "Please notify whomever has the passcode")
                self.run_updates()
                time.sleep(1)
                self.ui.display(mainT = "Please notify whomever has the passcode.")
                self.run_updates()
                time.sleep(1)
                self.ui.display(mainT = "Please notify whomever has the passcode..")
                self.run_updates()
                time.sleep(1)
                self.ui.display(mainT = "Please notify whomever has the passcode...")
                self.run_updates()
                time.sleep(1)
                ex = [None]
                self.ui.check(q, ex)
                self.run_updates()
        
        print("safe")
        self.playfor('password')
        self.ui.verifyuser(t.password)
        self.run_updates()
        self.lockoff()

        q = "Take everything. Close door if finished.\n Press Yes to Leave."
        ex[0] = None
        self.ui.check(q, ex)
        self.playfor('remove_item')
        while ex[0] is not True:
            self.run_updates()
        self.lockon()
        
        #turn off screen
        # self.ui.display("travelling")

        # tp = destinationlist.get("Home")
        # pose = self.create_pose_stamped(tp[0], tp[1], tp[2])
        # self.goPose(pose)

        # while not self.navigator.isTaskComplete():
        #     self.run_updates()
            
        self.playfor('nothing') 
        self.log("robot_home")

        return False

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