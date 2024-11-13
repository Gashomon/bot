import enum

listofLongSituations = {}
listofShoortSituations = {}

destinationList = {
    'Initial': (0.0, 0.0, 0.0), 
    'Home': (1.2123, 0.0458, 0.01636), 
    'Dean': (-28.0098, 1.37033, -1.5951), 
    'CE'  : (-19.2221, 1.4609, -0.5951),
    'EE' : (-3.50651, 1.3341, -0.0429),
    'CpE'  : (-7.8943, 1.4781, -0.0478),
    'ME'  : (-14.9598, 1.3366, -0.0428),
    'ECE'  : (-9.3469, 1.4631, -0.04289)
}

class TransacType(enum):
    DELIVER = 1

class Transaction():
    sender = ""
    receiver = ""
    password = ""
    type = None
    dest1 = None
    dest2 = None

EXPERIMENTAL = True
    
class Bot():

    def __init__(self) -> None:
        pass

    def __init__(self, modules, nav, server, ui) -> None:
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
        if listofLongSituations.get(situation) is not None:
            self.modules.playloop(situation)
        if listofShoortSituations.get(situation) is not None:
            self.modules.playonce(situation)

    def loadlight(self, limit):
        load = self.modules.getLoad()
        if load > limit:
            return False
        if load < limit:
            return True
        
    def getcmd(self):
        if EXPERIMENTAL:
            self.ui.goto("control")
            t = Transaction()
            self.ui.control.pushButton_2.clicked.connect(
                lambda: self.ui.sendcmd(t))
            self.ui.control.pushButton_2.clicked.connect(
                lambda: self.ui.sendcmd(t))
            self.ui.control.pushButton_2.clicked.connect(
                lambda: self.ui.sendcmd(t))
            while t is None:
                pass
            return t
        else:
           return self.server.waitforcmd()
    
    def run(self, transaction):
        if transaction.type == TransacType.DELIVER:
            self.deliver(transaction)
    
        


        while not self.readydrive():
            self.ui.display("Not yet Ready")
        
        pose = self.nav.create_pose_stamped(destinationList.get("Home"))
        self.nav.goToPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        self.playfor('arrived')
    
    def deliver(self, transaction):
        t = transaction
        
        while not self.readydrive():
            self.ui.display("Not yet Ready")

        pose = self.nav.create_pose_stamped(t.dest1)
        self.nav.goToPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        self.playfor('arrived')
        
        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        while not self.ui.verifyuser(t.password):
            pass
        
        self.lockoff()

        while True:
            while self.dooropen() and self.loadlight():
                if not self.loadlight():
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
        self.nav.goToPose(pose)
        while not self.nav.navigator.isTaskComplete():
            self.ui.display("travelling")
        self.playfor('arrived')

        q = "r u user?"
        while not self.ui.check(q):
            pass
        
        while not self.ui.verifyuser(t.password):
            pass

        self.lockoff()

        while True:
            while self.dooropen() and self.loadlight(0.0):
                self.ui.display("Take all items. Close door if finished")

            q = "ready to go?"
            if not self.dooropen():
                if self.ui.check(q):
                    break
        
    def readydrive(self, limit=100):
        if self.dooropen():
            return False
        if not self.loadlight(limit):
            return False
        self.lockon()
        return True

        
        