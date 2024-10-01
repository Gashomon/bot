# Python file compilation of all control commands

from std_msgs.msg import String

import nav_func_basic
import motor_driver

import numpy as np

nav = nav_func_basic.NavigationNode()
mot = motor_driver.MotorDriver()

# TRAVERSALS (unfinalized data)
destinations = {
    'Home': (0.0, 0.0, 0.0), 
    'Dean': (0.5, 0.0, 0.0), 
    'CE'  : (0.4, 0.0, 0.0),
    'CpE' : (0.3, 0.0, 0.0),
    'ME'  : (0.2, 0.0, 0.0)
}
mainpath = (
    (1.0, 1.0, 0.0),
    (1.2, 1.0, 0.0),
    (1.3, 1.0, 0.0),
    (1.4, 1.0, 0.0),
    (1.5, 1.0, 0.0)
)
paths = {
    'Home->MainPath':
        {
            (0.0, 0.0, 0.0),
            (0.2, 0.2, 0.0),
            (0.4, 0.4, 0.0),
            (0.6, 0.6, 0.0),
            (0.8, 0.8, 0.0),
            (1.0, 1.0, 0.0)
        },
    'MainPath->Dean':
        {
            (),
        }
}

            # SAMPLE
# Set waypoints and start navigation
# waypoints = {
#             '0':(0.0, 0.0, 0.0),  # Assuming the robot stops facing the original direction
#             '1':(4.0, 2.5, np.radians(0)),
#             '2':(2.5, 2.5, np.radians(90)),
#             '3':(2.5, 7.0, np.radians(-130.60)),
#             '4':(-3.5, 0.0, np.radians(11.31)),
#             '5':(9.0, 2.5, np.radians(155.56)),
#             '6':(3.5, 5.0, np.radians(-125.00)),
# }

class BotCommands():

    def travel(self, dest):
        if destinations.get(dest) is not None:
            station = {
                nav.create_pose_stamped(destinations[dest][0], destinations[dest][1], destinations[dest][2])
            }
            nav.follow_waypoints(station)
            return 'success'
        else:
            return 'wrong points'
    
    def sound(self, snd):
        return
    
    def lock(self, state, passcode):
        return
    

    # def goDest(self, arr):
    #     dest = arr[0]
    #     x = float(arr[1])
    #     y = float(arr[2])
    #     a = np.radians(float(arr[3]))
    #     if dest == "error":
    #         self.err("wrong input")
    #     else:
    #         self.response_lbl.setText("Going to " + dest)
    #         bot.follow_waypoints([bot.create_pose_stamped(x, y, a)])
    
    # def getDest(self):
    #     x = self.x_pos_in.text()
    #     y = self.y_pos_in.text()
    #     a = self.angle_in.text()
    #     xneg = False
    #     yneg = False
    #     aneg = False
    #     if x[0]== '-':
    #         x = self.rmchars(x, 1, 'left')
    #         xneg = True
    #     if y[0]== '-':
    #         y = self.rmchars(y, 1, 'left')
    #         yneg = True
    #     if a[0]== '-':
    #         a = self.rmchars(a, 1, 'left')
    #         aneg = True
    #     if x.isnumeric() and y.isnumeric() and a.isnumeric():
    #         if xneg:
    #             x= '-'+x
    #         if yneg:
    #             y='-'+y
    #         if aneg:
    #             a='-'+a 
    #         txt = "pos: " + x + ", " + y + ": " + a + "°" 
    #         arr = [txt, x, y, a]
    #         return arr
    #     else:
            
    #         return ["error", 0,0,0]
    
    # def err(self, msg):
    #     self.response_lbl.setText("Error: " + msg)
    #     return
    
    # def rmchars(self, word, n, dir):
    #     new =''
    #     for i in range(len(word)):
    #         if dir == 'left' and i < n+i:
    #             n-=1
    #             continue
    #         elif dir == 'right' and i> len(word)-n:
    #             n-=1
    #             continue
    #         new+=word[i]
    #     return new
