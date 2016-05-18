import smbus
import os
import RPi.GPIO as GPIO
import time
import random
import boto3

# Pins
LED_FLASH_LOW = 40
LED_GREEN = 38
LED_YELLOW = 37
LED_RED = 35
LED_FLASH_HIGH = 36
BUTTON = 33
LDR = 31

# Setup general outputs
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
leds = [LED_FLASH_LOW,LED_GREEN,LED_YELLOW,LED_RED,LED_FLASH_HIGH]
GPIO.setup(leds, GPIO.OUT)

# Setup general inputs


#Use button to switch sensor, switch monitoring, or shutdown
GPIO.setup(BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON, GPIO.RISING, callback=button_press_switch, bouncetime=200)

BUTTON_SHUTDOWN = 4
BUTTON_MONITOR_SWITCH = 2
BUTTON_SENSOR_SWITCH = 1
BUTTON_NONE = 0
SENSOR_TEMPERATURE = 0
SENSOR_LIGHT = 1

## FUNCTIONS

## Callback function from button pressed
def button_press_switch(BUTTON):
    pressed_time = time.monotonic()
    while GPIO.input(BUTTON):
        time.sleep(1)
    pressed_time = time.monotonic() - pressed_time
    if pressed_time < 3:
        button_status = BUTTON_SENSOR_SWITCH
    elif pressed_time < 6:
        button_status = BUTTON_MONITOR_SWITCH
    else:
        button_status = BUTTON_SHUTDOWN
##

##
def shutdown():  
    os.system("sudo shutdown -h now")
##

## Get temperature in degrees C
def getTemp(address):
    convTemp(address)
    byte_tmsb = bus.read_byte_data(address,0x11)
    byte_tlsb = bus.read_byte_data(address,0x12)
    tinteger = (byte_tmsb & 0x7f) + ((byte_tmsb & 0x80) >> 7) * -2**8
    tdecimal = (byte_tmsb >> 7) * 2**(-1) + ((byte_tmsb & 0x40) >> 6) * 2**(-2)
    return tinteger + tdecimal
##

## Force a conversion and wait until it completes
def convTemp(address):
    byte_control = bus.read_byte_data(address,0x0E)
    if byte_control & 32 == 0:
        bus.write_byte_data(address, 0x0E, byte_control|32)
    byte_control = bus.read_byte_data(address,0x0E)
    while byte_control & 32 != 0:
        time.sleep(1)
        byte_control = bus.read_byte_data(address,0x0E)
    return True
##

## Read Resistor Capacitor charge time
def RCtime (RCpin):
    level = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(RCpin) == GPIO.LOW):
        level += 1
    return level
##

##
# Release RTC 3231
os.system('sudo rmmod rtc_ds1307')

# Setup RTC 3231 for temperature reading
bus = smbus.SMBus(1)
address = 0x68

# Set some flags
button_status = 0
monitor_latch = True
sensor_select = SENSOR_LIGHT

# Main loop
while button_status < BUTTON_SHUTDOWN:
    if button_status == BUTTON_MONITOR_SWITCH:
        monitor_latch = !monitor_latch
    if monitor_latch:
        if sensor_select == SENSOR_TEMPERATURE:
            pass
        elif sensor_select == SENSOR_LIGHT:
            GPIO.output(leds, GPIO.LOW)
            GPIO.output(LED_GREEN, GPIO.HIGH)
            print(RCtime (LDR))
            time.sleep(5)
        else:
            #default
            sensor_select = SENSOR_LIGHT
    else:
        break
        time.sleep(2)
    button_status = BUTTON_NONE

#Run cleanup routines
print "LEDs off"
GPIO.output(leds, GPIO.LOW)
GPIO.cleanup()
os.system('sudo modprobe rtc_ds1307')

# Really should only get here to shutdown
if button_status == BUTTON_SHUTDOWN:
    shutdown()
