import applicate_bot.modules.load as load
import applicate_bot.modules.lock as lock
import applicate_bot.modules.audio as audio

import time, statistics
import lgpio

from enum import Enum

# Actual Default
# class GPIOpins(Enum):
#     lockpin = 23
#     loadinpin = 22 = dout
#     loadoutpin = 27 = sck
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
    def __init__(self, setlock= -1, setloadin= -1, setloadout = -1, setdoor= -1, soundenable=True, soundpath=''):
         
        self.device = lgpio.gpiochip_open(0)

        self.lockpin = setlock
        self.lockstate = "off"
        self.locktimer = 5.0
        self.countlock = False
        self.lockstarttime = -1.0
        
        self.loadinpin = setloadin
        self.loadoutpin= setloadout
        self.curr_weight = 0.0
        self.weightlist = []
        self.max_weight_counter = 30
        self.loadstate = "light"

        self.doorpin = setdoor

        self.soundlibpath = soundpath
        
        if self.lockpin > 0:
            self.LOCKENABLE = True
            lgpio.gpio_claim_output(self.device, self.lockpin)
        else:
            self.LOCKENABLE = False
        
        if self.loadinpin > 0 and self.loadoutpin > 0:
            self.LOADENABLE = True
            self.hx711 = load.init_load(self.device, self.loadinpin, self.loadoutpin)
        else:
            self.LOADENABLE = False

        if self.doorpin > 0:
            self.DOORENABLE = True
            # lgpio.gpio_claim_input(self.device, 16)
        else:
            self.DOORENABLE = False

        if soundenable:
            self.SOUNDENABLE = True
            self.soundlibpath = soundpath
        else:
            self.SOUNDENABLE = False

    def setload(self, value):
        if value > 5000:
            self.loadstate = 'heavy'
            pass
        elif value > 2500:
            self.loadstate = 'middle'
            pass
        else:
            self.loadstate = 'light'
            pass        
    
    def setlock(self, state):
        if not self.LOCKENABLE:
            print("unabled lock")
            if state == "on":
                # self.lockstate = True
                self.lockstate = "on"
            if state == "off":
                # self.lockstate = False
                self.lockstate = "off" 
            return
        
        if state == "on" and self.lockstate == 'off':
            print("lock on")
            lock.setState(self.device, self.lockpin, "LOCKED")
            # self.lockstate = True
            self.lockstate = "on"
        if state == "off" and self.lockstate == 'on':
            print("lock off")
            lock.setState(self.device, self.lockpin, "UNLOCKED")
            # self.lockstate = False
            self.lockstate = "off" 
        pass
    
    def getlockstate(self):
        if not self.LOCKENABLE:
            pass

        return self.lockstate
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
            
        readings = self.curr_weight
        conversionFormula = readings / 200 #enter the conversion rate
        return conversionFormula
        
    def updateWeight(self):
        if not self.LOADENABLE:
            return

        load.addLoadRead(self.hx711, self.weightlist)
        
        if len(self.weightlist) >= self.max_weight_counter:
            self.curr_weight = statistics.mean(self.weightlist)
            self.weightlist.clear()
        
        return self.curr_weight

    def closegpio(self):
        lgpio.gpiochip_close(self.device)
        pass