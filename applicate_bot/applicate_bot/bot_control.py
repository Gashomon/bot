# Python file compilation of all control commands

from std_msgs.msg import String

import nav_func_basic
import motor_driver

nav = nav_func_basic.NavigationNode()
mot = motor_driver.MotorDriver()

class BotControl():

    def command(self, cmd, sprm1, sprm2, iprm1, fprm1, fprm2):
        if cmd == 'travel':
            nav.follow_waypoints
        elif cmd == 'display':
            if sprm1 == '':
                return
        elif cmd == 'sound':
            if sprm1 == '':
                return
        elif cmd == 'lock':
            if sprm1 == '':
                return
        elif cmd == '':
            if sprm1 == '':
                return
        elif cmd == '':
            if sprm1 == '':
                return
        elif cmd == '':
            if sprm1 == '':
                return
        else:
            return
        
            
