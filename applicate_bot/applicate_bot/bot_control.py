# Python file compilation of all control commands

# from std_msgs.msg import String

import navigation.nav_func_basic as Nav
import numpy as np
from modules import lock
from modules import audio
from modules import load
import sampleui.sample_bot_widget_ui as UI

# bot functions
nav = Nav.NavigationNode()
ui = UI.Ui_Form()



# TRAVERSALS (unfinalized data)
destinations = {
    'Initial': (0.0, 0.0, np.radians(0)), 
    'Home': (1.2123, 0.0458, 0.01636), 
    'Dean': (-28.0098, 1.37033, -1.5951), 
    'CE'  : (-19.2221, 0.0, np.radians(0)),
    'ME' : (-3.50651, 1.3341, -0.0429),
    'CpE'  : (-7.8943, 1.4781, -0.0478),
    'EE'  : (0.2, 0.0, np.radians(0)),
    'ECE'  : (-9.3469, 1.4631, -0.04289)
}

# SAMPLE
# 'name_of_waypoint' : (x_coordinate, y,_coordinate, angle_of_position)
# '1':(4.0, 2.5, np.radians(0)), '2':(2.5, 2.5, np.radians(90)) #use np.radians if angle is initially degrees

class BotCommands():

    def simpleDrive(self, dest): #only destination points
        if destinations.get(dest) is not None:
            station = {
                nav.create_pose_stamped(destinations[dest][0], destinations[dest][1], destinations[dest][2])
            }
            nav.follow_waypoints(station)
            return 'success'
        else:
            return 'wrong points'
    
    # def complexDrive(self, dest[]) #inputting many points
    
    def sound(self, situation):
        audio.playfor(situation)
    
    def lock(self, state):
        if state == 'open':
            lock.lock('off')
        elif state == 'close':
            lock.lock('on')
               
    


