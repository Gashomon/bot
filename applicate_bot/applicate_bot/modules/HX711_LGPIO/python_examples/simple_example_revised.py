#!/usr/bin/env python3
import lgpio # import GPIO
from hx711_Python3 import HX711_revised  # import the class HX711

device = lgpio.gpiochip_open(0)# set GPIO pin mode to BCM numbering
hx = HX711_revised.HX711(dout_pin=21, pd_sck_pin=20, device=0)  # create an object

print(hx.get_raw_data_mean())  # get raw data reading from hx711
lgpio.gpiochip_close()
