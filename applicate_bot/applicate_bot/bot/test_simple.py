from enum import Enum
import random
import time
import random

from applicate_bot.modules.modules import Modules as Modules
from applicate_bot.navigation.modded_robot_navigator import BasicNavigator as Navigator
from applicate_bot.gui.gui import UserInterface as UI
from applicate_bot.comms.command_server import ServerSub as Server
from applicate_bot.comms.logger import DataLogger as Logger 
# from applicate_bot.teleop.roller import Controller as Controller

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
    'Dean': (5.0, 0.0, 0.0), 
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

        self.EXPERIMENTAL=True # not used
        
        # audio folders. starting from home/pi
        path_of_audios = '/home/pi/bot/src/bot/applicate_bot/applicate_bot/modules/real_fx/'
        # self.modules = Modules(setlock= -1, setloadin= -1, setloadout = -1, setdoor= -1, soundenable=True, soundpath=path_of_audios)
        self.modules = Modules(setlock= 25, setloadin= 27, setloadout = 22, setdoor= -1, soundenable=True, soundpath=path_of_audios)
        
        print(f"enable modules are: lock({str(self.modules.LOCKENABLE)}), load({str(self.modules.LOADENABLE)})")
        
        # self.navigator = Navigator()
        self.server = Server()
        self.logger = Logger()
        self.ui = UI()

        self.loadbot()

        self.timer = self.create_timer(0.01, self.run_updates)
        # self.foreverlooping() # TEST IT OFF  

    # A BIT OF LOOPING COMPILER STUFFS
    def loadbot(self):
        print(self.server.fk_done())
        self.playfor('loading')
        self.ui.goto('main')
        self.ui.widget.show()
        
        print('initial lock on')
        self.modules.setlock('on')

        # Set initial pose
        # initial_pose = self.create_pose_stamped(0.0, 0.0, 0.0)
        # self.navigator.setInitialPose(initial_pose)

        # Wait for Nav2 to be active
        # self.navigator.waitUntilNav2Active()   
        self.playfor('activated')

        # permanent button assigns
        self.ui.main.pushButton.clicked.connect(self.cmd_btn)
        self.ui.main.introduceButton.clicked.connect(self.playIntro)
        self.ui.control.pushButton_6.clicked.connect(self.lockoff)
        self.ui.control.pushButton_7.clicked.connect(self.modules.toggleKeyboard)

        # self.run_updates()
            
    def run_updates(self, *events):
        # print("updating")
        if events.count("noui"):
            print("dont ui")
            rclpy.spin_once(self.server)
            return
        
        # print(self.server.fk_done())
        self.ui.app.processEvents()

        if events.count("load"):
            # print("loadup")
            self.updateWeight()
            # print(self.modules.curr_weight)
            if not self.loadislighterthan(3000) and self.ui.runEnabled():    
                self.playfor('heavy')       
                self.ui.disableRun()

            if self.loadislighterthan(3000) and not self.ui.runEnabled():
                self.ui.enableRun()

        if events.count('lock'):
            # print("lockup")
            if self.modules.lockstate == 'on' and self.ui.lockEnabled():
                self.ui.enableLock()
            if self.modules.lockstate == 'off' and not self.ui.lockEnabled():
                self.ui.disableLock()

            if self.modules.countlock:
                if time.perf_counter() - self.modules.lockstarttime >= self.modules.locktimer:
                    self.lockon()
        # else:
            # self.ui.enableLock()

        self.ui.app.processEvents()

    def foreverlooping(self):
        self.ui.goto('main')
        while rclpy.ok():
            self.run_updates()
            # pass
    
    def cmd_btn(self):
        print("starting")
        self.waitforcmd()
        print("going back")
    
    # NAVIGATOR STUFF
    def create_pose_stamped(self, position_x, position_y, orientation_z):
        q_x, q_y, q_z, q_w = tf_transformations.quaternion_from_euler(0.0, 0.0, orientation_z)
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        # pose.header.stamp = self.navigator.get_clock().now().to_msg()
        pose.pose.position.x = position_x
        pose.pose.position.y = position_y
        pose.pose.position.z = 0.0
        pose.pose.orientation.x = 0.0
        pose.pose.orientation.y = 0.0
        pose.pose.orientation.z = q_z
        pose.pose.orientation.w = q_w
        return pose

    def goPose(self, goal_pose):
        # self.navigator.clearAllCostmaps()
        # self.navigator.follow_path(goal_pose)
        i = 0
        # while not self.navigator.isTaskComplete():
        #     i = i + 1
        #     feedback = self.navigator.getFeedback()
        #     if feedback and i % 3 == 0:
        #         pass
                # self.get_logger().info('Navigation Feedback: %s' % feedback)
                # self.get_logger().info('Estimated time of arrival: '+ '{0:.0f}'.format(Duration.from_msg(feedback.estimated_time_remaining).nanoseconds/ 1e9)+ ' seconds.\n')
        # result = self.navigator.getResult()
        # self.get_logger().info('Navigation Result: %s' % result)

    # MODULES STUFF
    def lockon(self):
        self.modules.setlock('on')
        # self.playfor('locked')

        self.modules.countlock = False
        self.modules.lockstarttime = -1.0
        self.ui.enableLock()
        
    def lockoff(self):
        self.ui.disableLock()
        self.modules.setlock('off')
        self.playfor('unlocked')

        self.modules.countlock = True
        self.modules.lockstarttime = time.perf_counter()
        
    def playfor(self, situation):
        self.modules.playonce(situation)

    def loadislighterthan(self, limit):
        load = self.modules.getLoad()
        if load > limit: #load is heavy. limit in grams
            return False
        else:
            return True

    def updateWeight(self):
        if self.modules.LOADENABLE:
            self.modules.updateWeight()
            value = self.modules.getLoad()
            print(value)
            self.modules.setload(value)
            # set value to label if ever
            self.ui.displayWeight(self.modules.loadstate)

    def playIntro(self):
        intro = 'hello' + str(random.randint(1,3))
        print(f"intro is {intro}")
        self.playfor(intro)

    # MAIN ROBOT CONTROLLING STUFF    
    def waitforcmd(self):
        self.ui.goto("control") 
        
        t = Transaction()
        self.ui.control.receiver_name.clear()
        self.ui.control.sender_name.clear()
        self.ui.control.pushButton_5.clicked.connect(
            lambda: self.ui.sendcmd(t))
        while t.dest1 is None or t.dest2 is None:
            self.run_updates("load","lock")
        t.password = self.genpass()

        self.playfor('cmd_got')
        self.run(t)
        
        self.ui.goto('main')
        self.run_updates()
        self.playfor('finish')
        return

    def run(self, transaction):
        reset = None
        self.log("robot_begin")
        if transaction.type == 1:
            reset = self.deliver(transaction)
        # if transaction.type == 2:
        #      reset = self.fetch(transaction)
        # if transaction.type == 3:
        #     reset = self.retrieve(transaction)
        
        print(reset)
        if reset:
            self.log("robot_cancel")
            return
        
        print("done")
        
    def deliver(self, transaction):
        t = transaction
        
        # passcode check
        ex = [None]
        q = "This transaction's passcode is: " + t.password + ".\nYes to go, no to abort"
        self.ui.check(q, ex)
        self.playfor('show_pass')
        while ex[0] is not True:
            self.run_updates()
            if ex[0] is False:
                return True

        self.ui.display(mainT ="Robot is Leaving in 5 seconds. Please step aside.")
        self.run_updates()
        self.playfor('leaving')
        time.sleep(5)        

        #turn off screen
        self.ui.display("travelling")
        self.run_updates()
        time.sleep(3)

        # tp = destinationlist.get(t.dest2)
        # pose = self.create_pose_stamped(tp[0], tp[1], tp[2])
        # self.goPose(pose)

        # while not self.server.fk_done():
        # self.run_updates("noui")
        
        #turn on screen

        q = ""
        print(f"sender is {t.sender}\nreceiver is {t.receiver}")
        if t.receiver != "" or t.sender != "":
            q = q + "Delivery"
        if t.receiver != "":
            q = q + " for " + t.receiver
        if t.sender != "":
            q = q +" from " + t.sender + "\n"
        else:
            q = q + "\n"

        print(f"password is {t.password}")
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
                self.playfor('notify')
                self.run_updates()
                time.sleep(1)
                ex = [None]
                self.ui.check(q, ex)
                self.run_updates()
                 #should be on loop
               
        print("safe")
        self.playfor('enter_pass')
        self.ui.verifyuser(t.password, lambda: self.playfor('wrong_pw'))
        # self.run_updates()

        q = "Take everything. Close door if finished."
        ex[0] = None
        self.ui.check(q, ex, 'leave', 'unlock')
        self.playfor('remove_item')
        while ex[0] is not True:
            self.run_updates('lock')
            if ex[0] is False:
                self.lockoff()
                ex = [None]
                self.ui.check(q, ex, 'leave', 'unlock')
                # self.run_updates('lock')

        self.ui.display(mainT ="Robot is Leaving in 5 seconds. Please step aside.")
        self.run_updates()
        self.playfor('leaving')
        time.sleep(5)
        
        #turn off screen
        self.ui.display("travelling")
        self.run_updates()
        time.sleep(3)
        tp = destinationlist.get("Home")
        # pose = self.create_pose_stamped(tp[0], tp[1], tp[2])
        # self.goPose(pose)

        # while not self.server.fk_done():
        # self.run_updates("noui")

        # self.playfor('nothing') 
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
        node.modules.setlock('on')
        node.modules.closegpio()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()