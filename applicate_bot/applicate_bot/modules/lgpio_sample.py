#  Blink an LED with the LGPIO library
#  Uses lgpio library, compatible with kernel 5.11
#  Author: William 'jawn-smith' Wilson

import time
import lgpio
from applicate_bot.modules.HX711_LGPIO.HX711_Python3 import hx711_revised as hx711

# LED = 23
BUTTON = 13
LOCK = 25

INPIN = 27
CLKPIN = 22

# open the gpio chip and set the LED pin as output
device = lgpio.gpiochip_open(0)
# lgpio.gpio_claim_output(device, LED) # use pin as output 
lgpio.gpio_claim_output(device, LOCK) # use pin as output 
lgpio.gpio_claim_input(device, BUTTON) # use pin as in put

try:
    hx = hx711.HX711(device=device, dout_pin=INPIN, pd_sck_pin=CLKPIN)
    hx.set_scale_ratio(1)
    hx.set_offset(0)
    while True:
        # Turn the GPIO pin on
        # print("on")
        # lgpio.gpio_write(device, LOCK, 1)
        # 0 = 210000 1 = 240000

        formula = (hx.get_raw_data_mean(readings=30) - 420000) / 60000
        print("Raw Data: " + str(hx.get_last_raw_data()) + " kilograms")

        # time.sleep(5)

        # Turn the GPIO pin off
        # lgpio.gpio_read(device, BUTTON)
        # print("off")
        # lgpio.gpio_write(device, LOCK, 0)
        # time.sleep(5)

except KeyboardInterrupt:
    # lgpio.gpio_write(device, LED, 0)
    lgpio.gpiochip_close(device)
    lgpio.gpiochip_close(device)
