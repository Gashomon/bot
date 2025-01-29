import applicate_bot.modules.load as load
import applicate_bot.modules.lock as lock
import applicate_bot.modules.audio as audio

import time
import lgpio

from enum import Enum

class GPIOpins(Enum):
    lockpin = 17
    loadinpin = 23
    loadoutpin = 24
    doorpin = 16

class Modules():
    
    def __init__(self):
        pass
    
    # set pins to 0 to deactivate
    def __init__(self, setlock=GPIOpins.lockpin, setloadin=GPIOpins.loadinpin, setloadout = GPIOpins.loadoutpin, setdoor=GPIOpins.doorpin, soundenable=True):
         
        self.device = lgpio.gpiochip_open(0)

        self.lockpin = setlock
        self.lockstat = True
        
        self.loadinpin = setloadin
        self.loadoutpin= setloadout

        self.doorpin = setdoor
        
        if setlock:
            self.LOCKENABLE = True
            lgpio.gpio_claim_output(self.device, 17)
        
        if setloadin and setloadout:
            self.LOADENABLE = True
            self.hx711 = load.init_load(self.device, 23, 24)

        if setdoor:
            self.DOORENABLE = True
            # lgpio.gpio_claim_input(self.device, 16)

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
        pass
    
    def getlockstate(self):
        if not self.LOCKENABLE:
            pass
        return self.lockstat

        pass
        
    def getdoorstate(self):
        if not self.DOORENABLE:
            return 'close'
        door = lock.getdoorState(self.device, self.doorpin)
        somevalue = 0
        if door > somevalue:
            return "open"
        else:
            return "close"
        pass
    
    def playonce(self, situation):
        audio.playfor(situation)
        pass
    
    def playloop(self, situation, duration_count=0, trigger=None):
        while True:
            audio.playfor(situation)
        pass
            

    def getLoad(self):
        if not self.LOADENABLE:
            return 0
        return load.getLoadinGrams(self.hx711)
        pass

    def closegpio(self):
        lgpio.gpiochip_close(self.device)
        pass