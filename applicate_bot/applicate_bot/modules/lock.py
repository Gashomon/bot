#  Blink an LED with the LGPIO library
#  Uses lgpio library, compatible with kernel 5.11
#  Author: William 'jawn-smith' Wilson

import time
import lgpio

def setState(deviceid, lockpin, state):
    if state == 'LOCKED':
        lgpio.gpio_write(deviceid, lockpin, 1)
    if state == 'UNLOCKED':
        lgpio.gpio_write(deviceid, lockpin, 0)

def getdoorState(device, doorpin):
    result = lgpio.gpio_read(device, doorpin)
    return result
