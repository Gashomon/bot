from enum import Enum
import random

longsituationslist = {}
shortsituationslist = {}

destinationlist = {
    'Initial': (0.0, 0.0, 0.0), 
    'Home': (1.2123, 0.0458, 0.01636), 
    'Dean': (-28.0098, 1.37033, -1.5951), 
    'CE'  : (-19.2221, 1.4609, -0.5951),
    'EE' : (-3.50651, 1.3341, -0.0429),
    'CpE'  : (-7.8943, 1.4781, -0.0478),
    'ME'  : (-14.9598, 1.3366, -0.0428),
    'ECE'  : (-9.3469, 1.4631, -0.04289)
}

class TransacType(Enum):
    DELIVER = 1
    FETCH = 2
    RETRIEVE  = 3

class Transaction():
    sender = ""
    receiver = ""
    password = ""
    type = None
    dest1 = None
    dest2 = None
    
class Bot():

    def __init__(self) -> None:
        pass

    def __init__(self, modules, nav, server, ui) -> None:
        self.EXPERIMENTAL = True
        self.modules = modules
        self.nav = nav
        self.server = server
        self.ui = ui
        
    def lockon(self):
        self.modules.setlock('on')
    
    def lockoff(self):
        self.modules.setlock('off')
    
    def dooropen(self):
        door = self.modules.getdoorstate()
        if door == 'open':
            return True
        if door == 'close':
            return False
    
    def doorlocked(self):
        lock = self.modules.getlockstate()
        if lock == 'on':
            return True
        if lock == 'off':
            return False
        
    def playfor(self, situation):
        if longsituationslist.get(situation) is not None:
            self.modules.playloop(situation)
        if shortsituationslist.get(situation) is not None:
            self.modules.playonce(situation)

    def loadislighterthan(self, limit):
        load = self.modules.getLoad()
        if load > limit: #load is heavy
            return False
        else:
            return True
        
    def getcmd(self):
        if self.EXPERIMENTAL:
            self.ui.goto("control")
            t = Transaction()
            self.ui.control.pushButton_5.clicked.connect(
                lambda: self.ui.sendcmd(t, 'del'))
            self.ui.control.pushButton_6.clicked.connect(
                lambda: self.ui.sendcmd(t, 'fet'))
            self.ui.control.pushButton_7.clicked.connect(
                lambda: self.ui.sendcmd(t, 'ret'))
            while t is None:
                pass
            t.password = self
            return t
        else:
           return self.server.waitforcmd(t)
    
    def run(self, transaction):
        if transaction.type == TransacType.DELIVER:
            self.deliver(transaction)
        if transaction.type == TransacType.FETCH:
            self.fetch(transaction)
        if transaction.type == TransacType.RETRIEVE:
            self.retrieve(transaction)
    
        while not self.readydrive():
            self.ui.display("Not yet Ready")
        
        pose = self.nav.create_pose_stamped(destinationlist.get("Home"))
        self.nav.navigator.goToPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        self.playfor('nothing') 
    
    def deliver(self, transaction):
        t = transaction
        
        while not self.readydrive():
            self.ui.display("Not yet Ready")

        pose = self.nav.create_pose_stamped(t.dest1)
        self.nav.navigator.goToPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        self.playfor('nothing')
        
        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        while not self.ui.verifyuser(t.password):
            pass
        
        self.lockoff()

        while True:
            while self.dooropen() or self.loadislighterthan(0.01):
                if self.loadislighterthan(20000):
                    self.ui.display("Enter items. Close door if finished")
                else:
                    self.ui.display("Load too heavy")

            q = "ready to go?"
            if not self.dooropen:
                if self.ui.check(q):
                    break
                    
        while not self.readydrive():
            self.ui.display("Not yet Ready")

        pose = self.nav.create_pose_stamped(t.dest2)
        self.nav.navigator.goToPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        self.playfor('nothing')

        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        while not self.ui.verifyuser(t.password):
            pass

        self.lockoff()

        while True:
            while self.dooropen() or not self.loadislighterthan(0.01):
                self.ui.display("Take all items. Close door if finished")

            q = "ready to go?"
            if not self.dooropen():
                if self.ui.check(q):
                    break

    def fetch(self, transaction):
        t = transaction
        
        while not self.readydrive():
            self.ui.display("Not yet Ready")

        pose = self.nav.create_pose_stamped(t.dest1)
        self.nav.navigator.goToPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        self.playfor('nothing')
        
        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        while not self.ui.verifyuser(t.password):
            pass
        
        self.lockoff()

        while True:
            while self.dooropen() or self.loadislighterthan(0.01):
                if self.loadislighterthan(20000):
                    self.ui.display("Enter items. Close door if finished")
                else:
                    self.ui.display("Load too heavy")

            q = "ready to go?"
            if not self.dooropen:
                if self.ui.check(q):
                    break
                    
        while not self.readydrive():
            self.ui.display("Not yet Ready")

        pose = self.nav.create_pose_stamped(t.dest2)
        self.nav.navigator.goToPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        self.playfor('nothing')

        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        while not self.ui.verifyuser(t.password):
            pass

        self.lockoff()

        while True:
            while self.dooropen() or not self.loadislighterthan(0.01):
                self.ui.display("Take all items and Close the door first")
            
            while self.dooropen() or self.loadislighterthan(0.01):
                self.ui.display("Put back all items. Close door if finished") 

            q = "ready to go?"
            if not self.dooropen():
                if self.ui.check(q):
                    break
    
        pose = self.nav.create_pose_stamped(t.dest1)
        self.nav.navigator.goToPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        self.playfor('nothing')
        
        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        while not self.ui.verifyuser(t.password):
            pass
        
        self.lockoff()

        while True:
            while self.dooropen() and not self.loadislighterthan(0.01):
                self.ui.display("Take all items. Close door if finished")

            q = "ready to go?"
            if not self.dooropen():
                if self.ui.check(q):
                    break

    def deliver(self, transaction):
        t = transaction
        
        while not self.readydrive():
            self.ui.display("Not yet Ready")

        pose = self.nav.create_pose_stamped(t.dest2)
        self.nav.navigator.goToPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        self.playfor('nothing')
        
        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        while not self.ui.verifyuser(t.password):
            pass
        
        self.lockoff()

        while True:
            while self.dooropen() or self.loadislighterthan(0.01):
                if self.loadislighterthan(20000):
                    self.ui.display("Enter items. Close door if finished")
                else:
                    self.ui.display("Load too heavy")

            q = "ready to go?"
            if not self.dooropen:
                if self.ui.check(q):
                    break
                    
        while not self.readydrive():
            self.ui.display("Not yet Ready")

        pose = self.nav.create_pose_stamped(t.dest1)
        self.nav.navigator.goToPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        self.playfor('nothing')

        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        while not self.ui.verifyuser(t.password):
            pass

        self.lockoff()

        while True:
            while self.dooropen() or not self.loadislighterthan(0.01):
                self.ui.display("Take all items. Close door if finished")

            q = "ready to go?"
            if not self.dooropen():
                if self.ui.check(q):
                    break    
        
    def readydrive(self, limit=100):
        if self.dooropen():
            return False
        if not self.loadislighterthan(limit):
            return False
        self.lockon()
        return True

    def genpass(self):
        password = ""
        for i in range(4):
            password = password + random.randint(0,9)
        return password