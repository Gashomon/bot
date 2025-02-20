from enum import Enum
import random

longsituationslist = {}
# shortsituationslist = {'load'} # unneeded list

destinationlist = {
    'Initial': (0.0, 0.0, 0.0), 
    'Home': (0.0, 0.0, 0.0), 
    'Dean': (1.0, 0.0, 0.0), 
    'CE'  : (2.0, 0.0, 0.0),
    'EE' : (0.0, 1.0, 0.0),
    'CpE'  : (0.0, 2.0, 0.0),
    'ME'  : (-1.0, 0.0, 0,0),
    'ECE'  : (0.0, -1.0, 0.0)
}

class TransacType(Enum):
    DELIVER = 1
    FETCH = 2
    RETRIEVE = 3

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

    def __init__(self, modules, nav, server, ui, logger) -> None:
        self.EXPERIMENTAL = True
        self.modules = modules
        self.nav = nav
        self.server = server
        self.ui = ui
        self.logger = logger

        self.playfor('loading')
        
    def lockon(self):
        self.modules.setlock('on')
        self.playfor('locked')
    
    def lockoff(self):
        self.modules.setlock('off')
        self.playfor('unlocked')
    
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
            t.password = self.genpass()
            self.playfor('cmd_got')
            return t
        else:
            self.playfor('cmd_got')
           return self.server.waitforcmd(t)
    
    def run(self, transaction):
        self.logger.logwrite("robot_begin")
        if transaction.type == TransacType.DELIVER:
            self.deliver(transaction)
        if transaction.type == TransacType.FETCH:
            self.fetch(transaction)
        if transaction.type == TransacType.RETRIEVE:
            self.retrieve(transaction)
    
        while not self.readydrive():
            self.ui.display("Not yet Ready")
        
        pose = self.nav.create_pose_stamped(destinationlist.get("Home"))
        self.nav.goPose(pose)
        self.playfor('running')
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        self.playfor('nothing') 
        self.logger.logwrite("robot_home")
    
    def deliver(self, transaction):
        t = transaction

        pose = self.nav.create_pose_stamped(t.dest1)
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

            q = "ready to go?"
            self.playfor('leaving')
            if self.ui.check(q):
                break

        pose = self.nav.create_pose_stamped(t.dest2)
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
        if self.dooropen():
            return False
        if not self.loadislighterthan(limit):
            return False
        self.playfor('locked')
        self.lockon()
        return True

    def genpass(self):
        password = ""
        for i in range(4):
            password = password + random.randint(0,9)
        return password