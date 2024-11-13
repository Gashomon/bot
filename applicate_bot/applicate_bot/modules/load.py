#  Blink an LED with the LGPIO library
#  Uses lgpio library, compatible with kernel 5.11
#  Author: William 'jawn-smith' Wilson

import time
import lgpio

def readLoadSensor(device, loadpin):
    result = lgpio.gpio_read(device, loadpin)
    return result
