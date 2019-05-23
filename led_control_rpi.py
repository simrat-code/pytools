#
# date  : 24-May-19
#

import RPi.GPIO as gpio
import time

PIN=21

gpio.setmode(gpio.BCM)
gpio.setup(PIN, gpio.OUT)
gpio.output(PIN, gpio.HIGH)
time.sleep(2)
gpio.output(PIN, gpio.LOW)
gpio.cleanup()

print("its done!!!")
