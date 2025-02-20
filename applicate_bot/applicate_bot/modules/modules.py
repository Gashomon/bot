import applicate_bot.modules.load as load
import applicate_bot.modules.lock as lock
import applicate_bot.modules.audio as audio

import time
import lgpio

from enum import Enum

# Actual Default
# class GPIOpins(Enum):
#     lockpin = 17
#     loadinpin = 23
#     loadoutpin = 24
#     doorpin = 16

# Applied Default for no automatic
class GPIOpins(Enum):
    lockpin = 0
    loadinpin = 0
    loadoutpin = 0
    doorpin = 0

class Modules():
    
    def __init__(self):
        pass
    
    # set pins to 0 to deactivate
    def __init__(self, setlock=GPIOpins.lockpin, setloadin=GPIOpins.loadinpin, setloadout = GPIOpins.loadoutpin, setdoor=GPIOpins.doorpin, soundenable=True, soundpath='sounds/'):
         
        self.device = lgpio.gpiochip_open(0)

        self.lockpin = setlock
        self.lockstat = True
        
        self.loadinpin = setloadin
        self.loadoutpin= setloadout

        self.doorpin = setdoor

        self.soundlibpath = soundpath
        
        if self.setlock>0:
            self.LOCKENABLE = True
            lgpio.gpio_claim_output(self.device, self.setlock)
        else:
            self.LOCKENABLE = False
        
        if self.setloadin>0 and self.setloadout>0:
            self.LOADENABLE = True
            self.hx711 = load.init_load(self.device, self.setloadin, self.setloadout)
        else:
            self.LOADENABLE = False

        if self.setdoor>0:
            self.DOORENABLE = True
            # lgpio.gpio_claim_input(self.device, 16)
        else:
            self.DOORENABLE = False

        if soundenable:
            self.SOUNDENABLE = True
            self.soundlibpath = soundpath
        else:
            self.SOUNDENABLE = False
            
    def setlock(self, state):
        if not self.LOCKENABLE:
            if state == "on":
                self.lockstat = True
                self.lockstat = "on"
            if state == "off":
                self.lockstat = False
                self.lockstat = "off" 
            return

        if state == "on":
            lock.setState(self.device, self.lockpin, "LOCKED")
            # self.lockstat = True
            self.lockstat = "on"
        if state == "off":
            lock.setState(self.device, self.lockpin, "UNLOCKED")
            # self.lockstat = False
            self.lockstat = "off" 
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
        audio.playfor(self.soundlibpath, situation)
        pass
    
    def playloop(self, situation, duration_count=3, trigger=None):
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