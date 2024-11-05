# Python file compilation of all control commands

# from std_msgs.msg import String

import navigation.nav_func as Nav
import numpy as np
from modules import lock
from modules import audio
from modules import load

IN_TRIAL_MODE = True
if IN_TRIAL_MODE:
    import gui.pre_ui.ui_func as UI
else:
    import applicate_bot.applicate_bot.gui.pre_ui.ui_func as UI

import time
from enum import Enum

# bot imported functions
nav = Nav.NavigationNode()
ui = UI.UserInterface()

# TRAVERSALS (simple data)
destinationList = {
    'Initial': (0.0, 0.0, np.radians(0)), 
    'Home': (1.2123, 0.0458, 0.01636), 
    'Dean': (-28.0098, 1.37033, -1.5951), 
    'CE'  : (-19.2221, 1.4609, -0.5951),
    'EE' : (-3.50651, 1.3341, -0.0429),
    'CpE'  : (-7.8943, 1.4781, -0.0478),
    'ME'  : (-14.9598, 1.3366, -0.0428),
    'ECE'  : (-9.3469, 1.4631, -0.04289)
}

# SAMPLE
# 'name_of_waypoint' : (x_coordinate, y,_coordinate, angle_of_position)
# '1':(4.0, 2.5, np.radians(0)), '2':(2.5, 2.5, np.radians(90)) #use np.radians if angle is initially degrees

class BotStatus(Enum):
    STARTUP = 0
    SHUTDOWN = 0

    WAITING = 0
    TRAVELLING = 0
    ATHOME = 0
    ATCMD = 0

    BEGINTASK = 0
    ATTASK = 0
    FINISHEDTASK = 0
    
    CRITICAL = 0
    LOST = 0

class BotCommands():
    
    # STARTUPS
    def __init__(self):
        self.botStatus = None

        self.currentStation = None
        self.currentPass = None

        self.task = None
        self.taskStep = None
        
    def startUp(self):
        self.goTo("Home")
        self.botStatus = BotStatus.ATHOME
        ui.switchTo("main")
    
    def reset(self):
        self.goTo("Home")
        self.botStatus == BotStatus.ATHOME

        self.currentStation = None
        self.currentPass = None

        self.task = None
        self.taskStep = None

        # plus code to save records

    # LISTENERS
    def waitforUser(self, userPassword):
        audio.playfor('arrived')
        isUser = [0]
        userConfirmed = False
        confirmText = "Are you User?"
        newConfirmText = "Please notify other Users"
        self.confirm(isUser, confirmText)
        while not userConfirmed:
            if (isUser[0] == 1):
                audio.playfor('nothing')
                userConfirmed = ui.password.verify(userPassword)
            elif (isUser[0] == 2):
                audio.playfor('arrived')
                self.confirm(isUser, newConfirmText)

        self.botStatus = BotStatus.ATCMD
        return 
    
    def getUser(self):
        while self.senderStation == '':
            if IN_TRIAL_MODE:
                self.senderStation, self.senderPass = 'Home', '0000'
            else:
                userStation = 'insert server code'
                passCode = 'insert server code'
                self.senderStation, self.senderPass = userStation, passCode

            self.powerSave()

        self.currentStation = self.senderStation
        self.currentPass = self.senderPass
        self.botStatus = BotStatus.BEGINTASK
              
    def getCommand(self):
        ui.switchTo('control')
        ui.control.pushButton_5.clicked.connect(self.rundel)
        ui.control.pushButton_6.clicked.connect(self.runfec)
        ui.control.pushButton_7.clicked.connect(self.runret)
        while self.task == None:
            self.botStatus = BotStatus.ATCMD
        self.botStatus = BotStatus.ATTASK
    
    # ACTIONS 
    def runfec(self):
        
        ui.status.display("FETCHING...")
        ui.control.comboBox_4
        ui.control.comboBox_5

    def rundel(self):
        # Set Task Name
        self.task = 'DELIVER'

        # Confirm Task
        if self.taskStep == 0:
            isSure = [0]
            confirmText = "Are you Sure?"
            self.confirm(isSure, confirmText)
            if isSure == 2:
                self.botStatus = BotStatus.ATCMD
                self.taskStatus = None
        
        # Accept Load
        elif self.taskStep == 1:
            self.acceptLoad()
        
        # Show Password
        elif self.taskStep == 2:
            receiverPass = '1111'
            self.showPass(receiverPass)
            
        # Get Ready + Goto Receiver
        elif self.taskStep == 3:
            self.getReady()
            dest = ui.control.comboBox_7.currentText()
            self.currentStation = dest
            self.currentPass = receiverPass
            self.botStatus = BotStatus.TRAVELLING
            ui.status.display("DELIVERING...")
        
        # Open n Remove Items
        elif self.taskStep == 4:
            self.unLoad()

        elif self.taskStep == 5:
            toLeave = [0]
            while not toLeave[0] == 1:
                self.confirm(toLeave, 'leave na?') 
            self.botStatus = BotStatus.FINISHEDTASK
        self.taskStep += 1
        
        ui.control.comboBox_6
        ui.control.comboBox_7
             
    def runret(self):
        ui.status.display("RETRIEVING...")
        ui.control.comboBox_8
        ui.control.comboBox_9
         
    # CONFIRM
    def confirm(self, someList, confirmText, bt1Text, bt2Text):
        audio.playfor('confirm')
        someList = [0]
        ui.confirm.confirm(confirmText, lambda: self.setSomeList(someList, 0, 1), lambda: self.setSomeList(someList, 0, 2), bt1Text, bt2Text)
        while not someList:
            pass

    def setSomeList(somelist, dix, someValue):
        somelist[dix] = someValue
    
    # DRIVE
    def goTo(self, dest):
        nav.simpleDrive(destinationList, dest)
        while(not (nav.navigator.isTaskComplete())):
            ui.status.display("GOING to " + dest)
            audio.playfor('travelling')
            
        ui.status.display("Arrived!")
        audio.playfor('arrived')
        self.botStatus == BotStatus.WAITING

    # PREPS        
    def getReady(self):
        isReady = [0]   
        lock.setState("LOCKED")
        # lock get state
        audio.playfor('nothing')
        confirmText = "About to leave, Ready?"
        self.confirm(isReady, confirmText)
        if isReady == 1:
            return True
        elif isReady == 2:
            pass
    
    def showPass(self, receiverPass):
        isOkay = [0]
        confirmText = "Password is " + str(receiverPass)
        self.confirm(isOkay, confirmText)
        if isOkay:
            return
     
    def acceptLoad(self):
        threshold = 100
        lock.setState("UNLOCKED")
        while lock.getState() == "OPEN":
            if load.readLoadSensor() > threshold:
                ui.status.display("Too Heavy")
            else:
                ui.status.display("")
        lock.setState('LOCKED')
        return
    
    def unLoad(self):
        lock.setState("UNLOCKED")
        while not (load.readLoadSensor() == 0):
            ui.status.display("Please remove items")
        while not lock.getState == "CLOSED":
            ui.status.display("Please close door")
        isOkay = [0]
        while not isOkay[0] == 1:
            self.confirm(isOkay, "Is okay?")
        lock.setState("LOCKED")

    # SYSTEMS
    def powerSave(self):
        # some sleep code + add more options
        pass
    
    def checkUp(self):
        pass
    
    def record(self):
        self.botStatus = BotStatus.TRAVELLING

def main():
    bot = BotCommands()
    try:
        while not bot.botStatus == BotStatus.SHUTDOWN:
            bot.checkUp()

            if bot.botStatus == BotStatus.STARTUP:    
                bot.startUp()

            elif bot.botStatus == BotStatus.ATHOME:
                bot.getUser()
            
            elif bot.botStatus == BotStatus.BEGINTASK:
                bot.record()

            elif bot.botStatus == BotStatus.TRAVELLING:
                bot.goTo(bot.currentStation)

            elif bot.botStatus == BotStatus.WAITING:
                bot.waitforUser(bot.currentPass)
                if not bot.task == None or not bot.taskStep == None:
                    bot.botStatus = BotStatus.ATTASK

            elif bot.botStatus == BotStatus.ATCMD:
                bot.getCommand()

            elif bot.botStatus == BotStatus.ATTASK:
                if bot.taskStep == None:
                    bot.taskStep = 0

                if bot.task == 'DELIVER':
                    bot.rundel()

            elif bot.botStatus == BotStatus.FINISHEDTASK:
                bot.reset()

            else:
                bot.botStatus = BotStatus.STARTUP
           
    except:
        pass
    else:
        pass
    finally:
        pass

if __name__ == '__main__':
    main()