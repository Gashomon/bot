#  Blink an LED with the LGPIO library
#  Uses lgpio library, compatible with kernel 5.11
#  Author: William 'jawn-smith' Wilson

import time
import lgpio

LED = 23
BUTTON = 13
# open the gpio chip and set the LED pin as output
device = lgpio.gpiochip_open(1)
lgpio.gpio_claim_output(device, LED) # use pin as output 
lgpio.gpio_claim_input(device, BUTTON) # use pin as in put

try:
    while True:
        # Turn the GPIO pin on
        lgpio.gpio_write(device, LED, 1)
        time.sleep(1)

        # Turn the GPIO pin off
        lgpio.gpio_read(device, BUTTON)
        time.sleep(1)

except KeyboardInterrupt:
    lgpio.gpio_write(device, LED, 0)
    lgpio.gpiochip_close(device)
    lgpio.gpiochip_close(device)
