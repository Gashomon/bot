import time
import lgpio
from applicate_bot.modules.modules import Modules as Modules

modululu = Modules(setlock= 25, setloadin= 27, setloadout = 22, setdoor= -1, soundenable=False, soundpath="")
got_weight = 0.0
prev_w = 0.0
while(True):
    try:
        modululu.updateWeight()
        prev_w = got_weight
        got_weight = modululu.getLoad()
        modululu.setload(got_weight)
        if(not (prev_w  == got_weight)):
            print(f"weight: {got_weight}, state: {modululu.loadstate}")

    except KeyboardInterrupt:
        print("whoops")
        break
