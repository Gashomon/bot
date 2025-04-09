import applicate_bot.modules.load as load
import applicate_bot.modules.lock as lock
import applicate_bot.modules.peripherals as perifs

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
        self.locktimer = 2.0
        self.countlock = False
        self.lockstarttime = -1.0
        
        self.loadinpin = setloadin
        self.loadoutpin = setloadout
        self.curr_weight = 0.0
        self.weightlist = []
        self.max_weight_counter = 30
        self.timer = time.perf_counter()
        self.loadstate = "light"
        self.midweight = 3000
        self.heavyweight = 5000

        self.doorpin = setdoor

        self.soundlibpath = soundpath
        
        if self.lockpin > 0:
            self.LOCKENABLE = True
            lgpio.gpio_claim_output(self.device, self.lockpin)
            print("i need to be one")
            self.setlock('on')
        else:
            self.LOCKENABLE = False
        
        if self.loadinpin > 0 and self.loadoutpin > 0:
            self.LOADENABLE = True
            self.hx711 = load.init_load(self.device, self.loadinpin, self.loadoutpin)
            self.backup_channel = self.hx711._current_channel
            self.backup_gain = self.hx711._gain_channel_A
            self.reference_unit = 1  # Default reference unit
        else:
            self.LOADENABLE = False

        if self.doorpin > 0:
            self.DOORENABLE = True
        else:
            self.DOORENABLE = False

        if soundenable:
            self.SOUNDENABLE = True
            self.soundlibpath = soundpath
        else:
            self.SOUNDENABLE = False

    def setload(self, value):
        if value > self.heavyweight:
            self.loadstate = 'heavy'
        elif value > self.midweight:
            self.loadstate = 'normal'
        else:
            self.loadstate = 'light'
    
    def setlock(self, state):
        if not self.LOCKENABLE:
            print("unabled lock")
            if state == "on":
                print("lon")
                self.lockstate = "on"
            if state == "off":
                print("loff")
                self.lockstate = "off" 
            return
        
        if state == "on" and self.lockstate == 'off':
            print("lock on")
            lock.setState(self.device, self.lockpin, "LOCKED")
            self.lockstate = "on"
        if state == "off" and self.lockstate == 'on':
            print("lock off")
            lock.setState(self.device, self.lockpin, "UNLOCKED")
            self.lockstate = "off" 
    
    def getlockstate(self):
        if not self.LOCKENABLE:
            pass

        return self.lockstate
        
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
        perifs.playfor(self.soundlibpath, situation)
    
    def playloop(self, situation, duration_count=3, trigger=None):
        while True:
            perifs.playfor(situation)

    def getLoad(self):
        if not self.LOADENABLE:
            return 0
        
        # Apply calibration to the weight reading
        readings = self.curr_weight
        conversionFormula = ((8.668880909258 * (10**-3)) * readings) - 3892.51 # Enter your conversion formula here
        return conversionFormula
    
    # v v v IMPORTANT STUFF v v v
    def getOLoad(self):
        if not self.LOADENABLE:
            return 0
        
        # Apply calibration to the weight reading
        readings = self.curr_weight
        return readings
    
    def calcWeight(self, val):

        conversionFormula = ((8.668880909258 * (10**-3)) * val) - 3892.51  # Enter your conversion formula here

        return conversionFormula
        
    def updateWeight(self):
        if not self.LOADENABLE:
            return

        try:
            load.addLoadRead(self.hx711, self.weightlist)
        except Exception as e:
            print("error reading, stopping..")
            return

        if len(self.weightlist) > self.max_weight_counter or (time.perf_counter()-self.timer > 1000.0  and len(self.weightlist) > 2):
            # Calculate the mean of the weight readings
            self.modlist = load.filter(self.hx711, self.weightlist)
            self.curr_weight = statistics.mean(self.modlist)
            self.hx711._save_last_raw_data(self.backup_channel, self.backup_gain, self.weightlist)
            self.timer = time.perf_counter()
            self.weightlist.clear()
        
    # Calibration Method for Load Sensor
    def calibrate_load_sensor(self, known_weight):
        """
        Calibrate the load sensor using a known weight.
        The `known_weight` should be in grams (e.g., 1000 for 1 kg).
        """
        print("Starting calibration...")
        
        # Reset the sensor and tare it (set to zero)
        self.hx711.reset()
        self.hx711.tare()
        
        print(f"Please place a known weight ({known_weight} grams) on the sensor.")
        time.sleep(5)  # Wait for the weight to settle

        # Read the raw weight with the known weight applied
        raw_value_with_known_weight = self.hx711.get_weight(5)
        print(f"Raw value with known weight: {raw_value_with_known_weight}")

        # Calculate the reference unit (calibration factor)
        self.reference_unit = raw_value_with_known_weight / known_weight
        print(f"Calculated reference unit: {self.reference_unit}")

        # Set the reference unit for the load sensor
        self.hx711.set_reference_unit(self.reference_unit)

        print("Calibration complete.")

    def toggleKeyboard(self):
        perifs.clickAt(835,10)
        pass

    def closegpio(self):
        lgpio.gpiochip_close(self.device)
