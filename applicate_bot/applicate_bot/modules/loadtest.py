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
        got_weight = modululu.getOLoad()
        new_weight = modululu.calcWeight(got_weight)
        modululu.setload(got_weight)
        if(len(modululu.weightlist)==0):
            # print(f"Original weight(raw): {got_weight}, Calculated weight(grams): {new_weight} state: {modululu.loadstate}")
            print(new_weight)

    except KeyboardInterrupt:
        print("whoops")
        break
