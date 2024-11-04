#  Blink an LED with the LGPIO library
#  Uses lgpio library, compatible with kernel 5.11
#  Author: William 'jawn-smith' Wilson

import time
import lgpio

RELAYPIN = 23
# open the gpio chip and set the LED pin as output
device = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(device, RELAYPIN) # use pin as output 

def setState(state):
    if state == 'LOCKED':
        lgpio.gpio_write(device, RELAYPIN, 1)
    if state == 'UNLOCKED':
        lgpio.gpio_write(device, RELAYPIN, 0)
def getState():
    return
