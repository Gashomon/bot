#  Blink an LED with the LGPIO library
#  Uses lgpio library, compatible with kernel 5.11
#  Author: William 'jawn-smith' Wilson

import time
import lgpio

LOADPIN = 23
# open the gpio chip and set the LED pin as output
device = lgpio.gpiochip_open(0)
lgpio.gpio_claim_input(device, LOADPIN) # use pin as output 

def readLoadSensor(state):
    result = lgpio.gpio_read(device, LOADPIN)
    return result
