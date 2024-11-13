import load
import lock
import audio

import time
import lgpio

import enum
class GPIOpins(enum):
    lockpin = 1
    loadpin = 2
    doorpin = 3

class Modules():
    
    def __init__(self):
        pass
    
    # set pins to 0 to deactivate
    def __init__(self, setlock=GPIOpins.lockpin, setload=GPIOpins.loadpin, setdoor=GPIOpins.doorpin, soundenable=True):
         
        self.device = lgpio.gpiochip_open(0)

        self.lockpin = setlock
        self.lockstat = True
        
        self.loadpin = setload

        self.doorpin = setdoor
        
        if setlock:
            self.LOCKENABLE = True
            lgpio.gpio_claim_output(id, self.lockpin)
        
        if setload:
            self.LOADENABLE = True
            lgpio.gpio_claim_input(id, self.loadpin)

        if setdoor:
            self.DOORENABLE = True
            lgpio.gpio_claim_input(id, self.doorpin)

        if soundenable:
            self.SOUNDENABLE = True
            
    def setlock(self, state):
        if not self.LOCKENABLE:
            return
        if state == "on":
            lock.setState(self.device, self.lockpin, "LOCKED")
            self.lockstat = True
        if state == "off":
            lock.setState(self.device, self.lockpin, "UNLOCKED")
            self.lockstat = False
    
    def getlockstate(self):
        if not self.LOCKENABLE:
            pass
        return self.lockstat

    def getdoorstate(self):
        if not self.DOORENABLE:
            return 'close'
        door = lock.getdoorState(self.device, self.doorpin)
        somevalue = 0
        if door > somevalue:
            return "open"
        else:
            return "close"
    
    def playonce(self, situation):
        audio.playfor(situation)
    
    def playloop(self, situation, duration_count=0, trigger=None):
        while True:
            audio.playfor(situation)
            

    def getLoad(self):
        if not self.LOADENABLE:
            return 0
        return load.readLoadSensor(self.device,self.loadpin)

    def closegpio(self):
        self.device = lgpio.gpiochip_close(0)