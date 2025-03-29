#  Blink an LED with the LGPIO library
#  Uses lgpio library, compatible with kernel 5.11
#  Author: William 'jawn-smith' Wilson

import time
import lgpio
from applicate_bot.modules.HX711_LGPIO.HX711_Python3 import hx711_revised as hx711

def init_load(deviceid, outpin, clkpin, 
            gain_ch=128, sel_ch='A',
            scale_ratio = 1, offset=0):
    hx = hx711.HX711(device=deviceid, dout_pin=outpin, pd_sck_pin=clkpin)

    # set other params
    hx.set_scale_ratio(scale_ratio)
    hx.set_offset(offset)
    return hx

# not used
def readLoadSensor(hx):
    result = hx.get_raw_data_mean()
    return result

def addLoadRead(hx, load_arr):
    # do backup of current channel befor reading for later use
    # print("getting new data")
    backup_channel = hx._current_channel
    backup_gain = hx._gain_channel_A
    # do required number of readings
    newval = hx._read()
    newarr = []
    
    if newval > -1 and newval:
        load_arr.append(newval)
    
        if len(load_arr) > 2  and hx._data_filter:
            # print(f"t1 is {tmp1}")
            newarr = hx._data_filter(load_arr)
            # print(newarr)
            
        load_arr = newarr
    # tmp1 = []
    # tmp1 = load_arr
    
    # tmp1.append(hx._read())
    
    # tmp2 = []
    # if len(tmp1) > 2  and hx._data_filter:
    #     print(f"t1 is {tmp1}")
    #     tmp2 = hx._data_filter(tmp1)
    # else:
    #     tmp2 = tmp1
    # load_arr = tmp2   
    # print(f" arr {load_arr}")
    return 

# not used
def getLoadinGrams(hx):
    readings = readLoadSensor(hx)
    conversionFormula = readings / 200 #enter the conversion rate
    return conversionFormula
