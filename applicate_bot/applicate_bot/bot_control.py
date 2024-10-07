# Python file compilation of all control commands

# from std_msgs.msg import String

import navigation.nav_func_basic as Nav
import numpy as np
from modules import lock
from modules import audio

# bot functions
nav = Nav.NavigationNode()

# TRAVERSALS (unfinalized data)
destinations = {
    'Home': (0.0, 0.0, np.radians(0)), 
    'Dean': (0.5, 0.0, np.radians(0)), 
    'CE'  : (0.4, 0.0, np.radians(0)),
    'CpE' : (0.3, 0.0, np.radians(0)),
    'ME'  : (0.2, 0.0, np.radians(0))
}
# SAMPLE
# 'name_of_waypoint' : (x_coordinate, y,_coordinate, angle_of_position)
# '1':(4.0, 2.5, np.radians(0)), '2':(2.5, 2.5, np.radians(90))

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
    
    def sound(self, situation):
        audio.playfor(situation)
    
    def lock(self, state):
        if state == 'open':
            lock.lock('off')
        elif state == 'close':
            lock.lock('on')
            
            
    

